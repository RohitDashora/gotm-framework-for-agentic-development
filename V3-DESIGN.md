# GOTM v3 — design blueprint (the foundation the rewrite derives from)

> **Status:** v0.1 blueprint, for redline. This is the single source of truth for the v3 rewrite of the framework: the architecture, the re-derived primitives, the scheduler loop, the deliverable map, and the open questions. Every chapter / prompt / template unit is written **reading this file**. It is not itself a published chapter — it is the design contract.
>
> **Method:** the rewrite is driven *as a GOTM v3 project* — the conversation agent is the driver; each unit (chapter, prompt, template) is produced by a stateless worker reading this blueprint + its bounded inputs; each is audited by a fresh worker. The rewrite is its own worked example.

---

## 1. Why v3 — the first-principles diagnosis

GOTM's one true invariant is **the durable store reconstructs working context** (transcript independence). v1/v2 honored that for *authoring* but quietly violated its spirit in two places, and both made the system **monotonic** — cost that grows without bound on a long project:

1. **The planner and the doer were the same context.** One long-lived agent planned, executed, fixed, deployed, and self-validated — accumulating state until it (a) self-certified its own work (audit independence eroded) and (b) grew until it stalled (~987K tokens, observed). Work lived in a context, not the store — exactly what the invariant forbids.
2. **The ledger only grew and was re-read every turn.** Rich recovery logs + freeze-don't-edit + write-back-everything gave a strong theory of *growth* and **none of ephemerality**. A unit closed weeks ago still paid its full ~600–2,000 token cell on every re-read, forever (measured: a 380 KB / ~95K-token ledger, re-read each turn, duplicating detail already in `audits/` + `DECISIONS.md` + `docs/`).

**The root cause is one thing:** GOTM had no concept of *ephemerality*. The fix is not "compact harder." It is to make **nothing on the hot path long-lived** — and to give the one unavoidably-long-lived context (the driver) only the *index*, never the *work*.

## 2. The thesis

> **GOTM is a context-economy discipline. The durable store is the system of record; every working context is disposable and reconstructable from it. Nothing on the hot path is long-lived.**

Everything below is a consequence of that sentence.

## 3. The architecture — driver / worker / store

| Role | Maps to (Spark) | Lifetime | Holds | Never holds |
|---|---|---|---|---|
| **Driver** — the conversation agent | the driver | long-lived, **checkpointed** (re-hydratable from the store) | the plan (the ledger DAG), the discipline (PROTOCOL), the human interface (ratification ladder), the scheduler loop | work artifacts, raw inputs, execution logs, build/deploy state |
| **Worker** — a dispatched subagent | an executor | **ephemeral** — one unit, then discarded | only its bounded inputs + its spec; produces exactly one output; returns a structured result | any cross-unit state; any context from a prior unit |
| **Store** — `.gotm/` + the repo | HDFS / shuffle | durable, **tiered** | hot frontier (active units + recovery window) + cold archive (closed detail) | — |

**The load-bearing rule:** *the driver plans and talks; all work — however small — is a worker dispatch.* The driver never edits a work artifact, never reads bulk input (it dispatches a read-and-summarize worker when it must inspect), and is the **single writer** of the store.

## 4. The non-monotonicity guarantee (and its honest limit)

- **Workers — structurally non-monotonic.** Born fresh per unit, gone after. A worker's context is bounded by *one unit's* work, forever. Rotation is not a rule to remember; it is the default shape.
- **Store — hot path non-monotonic.** The cold archive grows but is never on the hot path. The ledger is **born tiered** (frontier + archive), not compacted as an afterthought.
- **Driver — checkpointed, not stateless (the honest limit).** In interactive Claude Code the driver *is* the session: it cannot be made stateless and cannot self-trigger `/compact` (verified — `/compact` is human-only; no hook or model directive fires it; the auto-compact threshold is not tunable). The driver still grows — but *slowly*, because it carries only plan + discipline + terse ledger. **Re-hydration is runtime-agnostic and depends on no compaction hook:** on *any* fresh start (cold restart, `/clear`, or after an auto/manual compaction) the driver rebuilds its working set from the store via the **session-start reconcile** — the same transcript-independence guarantee GOTM already makes. (An optional `SessionStart(compact)` hook could auto-inject that manifest, but it is at most an accelerator, not a dependency — and we deliberately do **not** build on it.) In **SDK / headless mode** the driver *can* additionally compact itself programmatically (`context_management.edits`). The framework states this plainly and never sells a stateless interactive driver.

**Net principle:** *no context on the hot path is long-lived; the one long-lived context carries the index, not the work.*

## 5. The primitives, re-derived

| Primitive | v2 (monotonic) | v3 |
|---|---|---|
| **Mission** | one sentence | unchanged — the driver's north star |
| **Ledger** | flat append-only log, re-read whole | the **DAG + scheduler state**: a hot frontier table (ready/active + immediate inputs) and a cold archive table, *born* tiered. The driver reads the frontier, not the history |
| **Atomic unit** | one pass, one output | a **self-contained worker dispatch spec** — bounded inputs + one output + spec + constraints, complete without the conversation. The dispatch contract is the center of gravity |
| **Foundation gate** | sequencing rule | DAG **topology** — the scheduler respects deps natively; foundation units are upstream nodes |
| **Audit cycle** | auditor≠author as a *rule* that eroded | **structural independence** — a worker produces output and marks it **authored-done** only; it *never self-certifies*. The driver **always launches a separate audit/verification worker** (the executor is ephemeral and gone by audit time, so self-grading is impossible). For deploy/infra/data units that audit worker performs the **verified-done** check — exercising the live artifact as its real consumer. authored-done vs verified-done are distinct ledger states; **only an independent worker confers the latter** |
| **Ratification ladder** | human vs agent decisions | unchanged — lives in the driver (the only context that talks to the human) |
| **Anti-drift / freeze** | immutability hook (over-blocks file follow-ons) | freeze stays; the hook honors **follow-on ownership** (an active unit may own a change to a done output); **only the driver writes the store** (workers report results) — the dup-row race disappears by construction |
| **Resilience** | reconcile-from-disk | two-level: **worker crash = task retry** (idempotent; inputs are on disk = lineage recompute); **driver crash = re-hydrate** from the store |
| **Memory** | one tier (the ledger) | **three tiers** — T1 conversation (driver, checkpointed), T2 hot durable (frontier, compacted), T3 cold durable (archive/audits/decisions/docs, pulled on demand) |

## 6. The loop — the driver's scheduler (loop engineering)

The driver runs a deterministic scheduler loop over the DAG. This is where "loop engineering" lives:

1. **Read frontier** → compute the **ready set** (deps satisfied, audit gate open).
2. **Dispatch workers** for ready units; **fan out independent units in parallel** (Spark stages), bounded by a **concurrency cap** (backpressure).
3. **Collect results** → the driver (single writer) records status/outputs to the store.
4. **Dispatch audit workers** (fresh contexts; independence is free) → apply verdicts → unblock downstream. Runtime/deploy units also get a **verified-done** worker.
5. **On worker failure** → retry the task on a fresh worker (inputs on disk = safe recompute).
6. **Checkpoint** → compact the frontier (T2) when over budget; re-hydrate the driver (T1) after a compaction.
7. **Repeat** until the DAG drains.

### 6a. Fan-out / fan-in — the parallelism spine

Fan-out (dispatch N independent workers) and fan-in (collect/merge at a barrier) are the core scheduling primitives; getting them right is most of v3's leverage — and most of where v3 can *re-introduce* monotonicity if done naively.

- **Minimize barriers; default to pipeline.** Each unit should flow author → audit → done **independently** — siblings never wait for each other. Wall-clock then = the slowest single chain, not sum-of-stages. A **fan-in barrier is justified only** when a downstream genuinely needs *all* upstreams at once: a synthesis unit, a cross-unit consistency audit, a dedup/merge, or the foundation→drafts gate. Everywhere else, pipeline.
- **Fan-in is a fresh worker reading the store — NOT the driver holding N results.** This is the token-critical rule and the whole reason v3 doesn't relapse. When N outputs must be merged (10 chapter drafts → one arc; many findings → one report), dispatch a **fan-in worker** that reads the N outputs *from the store* and emits the merged output; the driver receives **one pointer**, never the N bodies. If the driver collects N full results to merge them itself, every barrier re-concentrates the work into the long-lived context — monotonicity, reintroduced at each join.
- **Workers return terse structured results (pointer + index facts), never prose.** The driver merges pointers; the substance stays on disk.
- **Fan-out is a tree, not a flat list.** A wide/large unit fans out to sub-workers that may fan out further; the driver sees only the root result. Driver context stays bounded regardless of total work width.
- **Backpressure.** Bound concurrent fan-out (a cap). Unbounded width spikes resource use *and* the fan-in re-concentration cost.
- **Failure semantics at the barrier.** A failed fanned-out worker → retry (lineage from disk) or drop-and-continue with survivors — an *explicit* policy, never a silent partial merge.
- **Order-independence.** Results return out of order; merges are commutative or the driver sorts by unit ID.

### 6b. Token economy — worker minimalism, not project budgets

The discipline is **worker-context minimalism**, *not* project-level budgeting (no forecasting, no budget-governed loop — **decided**). The asymmetry is the whole point: be frugal where there are *many* contexts (workers); be generous where there is *one* that is orchestrating (the driver).

- **Workers are kept lean — a worker gets only what it needs, nothing more.** Its dispatch payload = the bounded inputs it actually consumes + its spec + constraints. **Never** the whole ledger, never sibling outputs it doesn't read, never the conversation. A worker that needs more *reads it from the store itself* (pointed reads) or **fans out**. Many workers run, often on cheaper models — every needless token in a worker payload is paid *per dispatch*, so trimming worker payloads is the highest-leverage lever.
- **The driver may be larger — it is orchestrating, and that is legitimate.** It holds plan + discipline + frontier + the human conversation; **don't starve it** to hit an arbitrary ceiling. Its safety net is **re-hydration from the store on any fresh start** (runtime-agnostic, no compaction hook — see §4), not aggressive turn-by-turn trimming. Optimize the workers; let the driver be the orchestrator.
- **Amortized batching (decided).** Always dispatch — but batch trivia into one **partition-worker**; size a worker's payload to a sensible band so dispatch overhead is amortized without bloating. The target is "minimal sufficient," not "hit a forecasted number." A unit that would blow its band fans out.
- **Audit weight by risk** (worker economy, not a project budget): full independent audit for keystone/deploy units; a light existence+spec+compile worker for mechanical ones — don't spend a ~100K-token audit where it isn't warranted.
- **Cheap hot tier.** The store's hot tier is read by every consuming worker *and* every driver turn; terse cells + read-the-audit-file-not-the-ledger + a born-tiered ledger keep that recurring read small.

**Dropped by decision:** project token budgets, DAG cost-forecasting, and a budget-adaptive loop. The loop stays simple; economy comes from **lean workers + a fat-but-checkpointed driver + cheap store reads**, not a budget governor.

**Model tiering** rides on top: one strong driver + many cheap fast workers (small model for mechanical units, the strong model for keystone reasoning & audits). The driver is the single write-back **writer**; the §6a fan-in-worker rule is what keeps that role thin.

## 7. What survives from v2 (re-derived, not inherited)

These were validated in the field and re-emerge from first principles — keep them, recast: filesystem-as-memory (now the *store* tier); foundation-before-drafts (now DAG topology); independent audits (now *structural*); PASS / PASS-FINDINGS / FAIL verdicts; the ratification ladder; the immutability freeze (with the follow-on fix); the cross-project learning loop (consume/produce → the cold tier feeds future drivers). v3 is a re-architecture of the *mechanism*, not a repudiation of the *wins*.

## 8. Deliverable map (the rewrite plan — units derive from this file)

**Concept chapters (`docs/`):**
1. The problem & the thesis (context economy; the store reconstructs context; nothing long-lived on the hot path)
2. The architecture: driver / worker / store (roles, lifetimes, the non-monotonicity guarantee + honest limit)
3. Work as a DAG: units, the ledger, foundation (unit = dispatch spec; ledger = DAG + scheduler state, born tiered)
4. The loop: the driver scheduler — ready-set, dispatch, collect, retry (lineage recompute)
5. **Scaling & economy** *(dedicated, per decision)*: fan-out/fan-in (fan-in = a worker reading the store), worker-context minimalism, amortized batching, risk-tiered audits, model tiering
6. Keeping it honest: structural audit independence, authored-done vs verified-done, the freeze
7. Resilience & the three-tier memory economy (worker retry, driver re-hydrate, compaction)
8. In practice: adopting v3, interactive vs SDK driver, bootstrapping, the worked example (this rewrite)
9. Learning across projects (consume/produce; the cold tier feeds future drivers)

**Prompts (`prompts/`):** `driver-loop.md` (NEW — the scheduler), `worker-dispatch.md` (the central worker contract; supersedes `subagent-dispatch.md`), `audit.md` (fresh-worker audit + verified-done runtime checks), `session-start.md` (driver boot: re-hydrate + reconcile + compact), `consult.md`, `outcome-analysis.md` (learning loop — keep).

**Templates (`templates/`):** `PROTOCOL.md.template` (rewritten around driver/worker/store + the loop), `LEDGER.md.template` (DAG + born-tiered: frontier table + archive table), `DECISIONS.md.template`, `QUESTIONS.md.template`, `README.md.template`, `LEARNINGS.md.template`, `CONSULTED.md.template`. Runtime hooks (immutability w/ follow-on fix; `SessionStart` re-hydration) are *described* here, *shipped* by the plugin (the two-repo split holds).

## 9. Migration & dogfooding

- Drive the rewrite **as a v3 GOTM project**: foundation (this doc) → chapter/prompt/template units (each a worker dispatch reading this doc) → independent audit workers → meta-example migration.
- The framework's own `.gotm/` migrates to the **v3 ledger shape** (frontier + archive, DAG) as a late unit — the repo becomes a live demonstration of v3, as it is of v2 today.
- **v2 projects migrate (decided).** Ship a `MIGRATION.md` + a one-shot **v2→v3 ledger converter** (tier the flat ledger into frontier + archive, record the DAG deps); existing projects (geniefy, knowledge-graph, this repo) convert. The converter generalizes the knowledge-graph `compact_ledger.py`.
- Then the **plugin v3.0** is derived from the finished framework: the scheduler runtime + worker-dispatch command (driver loop = prompt-discipline baseline, plus command + Workflow-script tiers), the born-tiered ledger template, the compaction script, and the immutability hook (with the follow-on fix). Re-hydration is the **session-start reconcile, not a compaction hook**.

## 10. Decisions (all foundational questions resolved — the blueprint is stable)

- **Q-v3-1 — partitioning → AMORTIZED BATCHING.** Always dispatch; batch trivia into one partition-worker; the driver never edits a work artifact.
- **Q-v3-2 — re-hydration → STORE + SESSION-START RECONCILE (no compaction hook).** The driver rebuilds from the store on any fresh start; we do **not** depend on a `SessionStart(compact)` hook. Manifest = active-unit row + its inputs (pointers) + recovery-log window + open `QUESTIONS`.
- **Q-v3-3 — scheduler home → PROMPT DISCIPLINE (baseline) + all three tiers.** The driver loop is fundamentally a prompt discipline the driver follows; a plugin command and a Workflow-style script are additional adoption tiers.
- **Q-v3-4 — backward compatibility → MIGRATE.** v2 projects convert to v3 via a `MIGRATION.md` + ledger converter (§9).
- **Q-v3-5 — verification → WORKERS MARK `authored-done` ONLY; THE DRIVER ALWAYS LAUNCHES AUDIT WORKERS.** Producing workers never self-certify; an independent driver-launched audit worker verifies — and performs the runtime `verified-done` check for deploy/infra/data units.
- **Q-v3-6 — token budgets → NO PROJECT BUDGETS.** Worker-context minimalism; the driver may be larger because it orchestrates.
- **Q-v3-7 — fan-in → HARD RULE.** Merges always run as a fan-in worker reading the store; the driver never holds N results.
- **Spine → dedicated ch5 "Scaling & economy."**

## 11. Rewrite progress (driver log — terse; detail in `.gotm/audits/v3-*.md`)

| Chapter | File | Status | Audit |
|---|---|---|---|
| ch1 problem & thesis | `docs/01-the-problem-and-thesis.md` | done | PASS-FINDINGS (0H/1M/2L) → `.gotm/audits/v3-ch01.md` |
| ch2 driver/worker/store | `docs/02-driver-worker-store.md` | done | PASS-FINDINGS (0H/0M/1L) → `.gotm/audits/v3-ch02.md` |
| ch3 work as a DAG | `docs/03-work-as-a-dag.md` | done | PASS (0H/0M/2L) → `.gotm/audits/v3-ch03.md` |
| ch4 the loop | `docs/04-the-loop.md` | done | validated (coherence pass) |
| ch5 scaling & economy | `docs/05-scaling-and-economy.md` | done | PASS-FINDINGS (0H/1M/0L) → `.gotm/audits/v3-ch05.md` |
| ch6 keeping it honest | `docs/06-keeping-it-honest.md` | done | PASS-FINDINGS (0H/0M/1L) → `.gotm/audits/v3-ch06.md` |
| ch7 resilience & memory | `docs/07-resilience-and-memory.md` | done | PASS-FINDINGS (0H/0M/1L) → `.gotm/audits/v3-ch07.md` |
| ch8 in practice | `docs/08-in-practice.md` | done | validated (coherence pass) |
| ch9 learning across projects | `docs/09-learning-across-projects.md` | done | validated (coherence pass) |

**Risk-tiered audits (dogfooding ch5).** Full independent audits for the 3 decision-critical chapters (ch5 hard rule · ch6 structural independence/verified-done · ch7 honest re-hydration limit). Lower-risk descriptive chapters (ch4/8/9, derived from the audited foundation) are validated within the **fan-in coherence pass** rather than standalone audits — a deliberate, logged audit-budget tiering, not a silent skip.

**Coherence pass — DONE** (one fan-in worker reading all 9 from the store; driver never held them): terminology unified ("terse structured result", "context economy"); ch5/6/7 trimmed; ch1 ch2-encroachment fixed; ch4/8/9 validated; heading style uniform; **full ch1→9 forward chain + ch9→README/ch1 verified.** Length **ratified** (execution-level): ch5 ~1590w / ch6 ~1329w accepted at the substance floor — word bands were guidance, not hard limits.

**Diagram pass — DONE.** 8 Mermaid diagrams across ch2–7 + ch9 (one shared visual language: driver/worker/store nodes + labeled dispatch/result/read/write flows); ch1 & ch8 left prose by judgment. All render-validated — `mmdc` 9/9 exit 0. ch5 shows the hard rule vs the monotonicity anti-pattern; ch7 shows no compaction hook.

**✅ DOCS PHASE COMPLETE** — 9 chapters drafted (driver/worker), gated (zero HIGH/FAIL), harmonized, and diagrammed.

**Deferred to later phases (still open):** the `CLAUDE.md`/README ref to old `docs/05-in-practice.md` → fix in migration (in-practice is now `08-in-practice.md`); ch9's prose refs to `prompts/consult.md` + `outcome-analysis.md` + `LEARNINGS.md.template` → link once the prompts/templates units land; old v2 `docs/01–06` → removed in the meta-example migration.

**✅ PROMPTS PHASE COMPLETE** — `driver-loop` + `worker-dispatch` (new), `audit` + `session-start` (v3 rewrites), `consult` + `outcome-analysis` (recast to v3 cold-tier); harmonized + validated (worker-dispatch & audit PASS, no HIGH/FAIL). `subagent-dispatch.md` superseded → remove in migration.

**✅ TEMPLATES PHASE COMPLETE** — PROTOCOL.md.template (keystone, PASS) · born-tiered LEDGER.md.template (PASS) · DECISIONS/QUESTIONS/README/LEARNINGS (updated) · CONSULTED (new). Cross-refs resolved + terminology harmonized.

**✅✅ FRAMEWORK v3 CONTENT COMPLETE** — docs (9 chapters + 8 diagrams) · prompts (6) · templates (7) — all produced driver/worker and independently gated. Uncommitted in the working tree.

**Next phases:** (4) meta-example migration (repo README rewrite, delete v2 docs, MIGRATION.md + converter) · (5) plugin v3.0 (hook follow-on fix, compaction script, scheduler runtime).
