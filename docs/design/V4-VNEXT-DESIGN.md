# GOTM vNext — the user context pool (declarative memory) — design

> **Status:** v0.3 — all decisions ratified, **building**. Foundation doc for GOTM's *second* cross-project store **+ the trust-model restructure** (2-axis + `grounding`). Ships as **v4.0**. See §6/§6a (trust), §11 (decisions), §13 (unit DAG).
> **Why:** external feedback ("GOTM vNext: from agent framework to organizational learning system") argued execution should compound into organizational knowledge. Unpacking it: the *shared-learning* half is already built (v3.36 learning pool); the genuinely-missing half is **organizational context — facts, not experience**. GOTM today has a home for *what I've learned* (procedural) and none for *what I know* (declarative). This doc adds the second store.
> **Reframe (locked in discussion):** the context tier is **bottom-up and user-first** — it accumulates from *your* projects at the user tier, then rises to enterprise by a *different flow*, mirroring the learning pool's L1→L2→L3. Not a top-down enterprise catalog pushed down.
> **Method:** design first, on disk not chat. Build driver/worker, execution-proven, independently audited — same as v3.36.

---

## 1. The thesis in one line

GOTM already recursed the store one level up for **experience** (the learning pool). vNext recurses it once more, in parallel, for **facts**: a user-tier **context pool** that is the declarative sibling of the procedural learning pool. Two stores, same bottom-up shape, different rules — because facts and experience decay, promote, and are trusted differently.

## 2. Procedural vs declarative — the two stores

The vNext doc split "memory" into *session / organizational-context / shared-learning*. GOTM already has session memory (the worker + T1/T2) and shared learning (the pool). The one gap is organizational context — and the clean underpinning is the classic **procedural vs declarative** memory distinction:

| | **Learning pool** (v3.36, have) | **Context pool** (v4, new) |
|---|---|---|
| answers | *"what have I learned to **do**?"* | *"what do I **know** is true?"* |
| memory type | procedural (experience) | declarative (facts) |
| record | `claim` + `fix` | `subject` + `fact`/`value` |
| store | `~/.gotm/learnings/POOL.md` | `~/.gotm/context/CONTEXT.md` |
| decays by | **contradiction** → `contested` + demote | **change** → `superseded` + archive |
| promotes by | **independent confirmation** (≥2 projects) | **commonality + curation** (≥N users, then endorsement) |
| trust ladder | candidate → validated → core | personal → shared → canonical |
| privacy | (rarely private) | **shareable flag is load-bearing** |
| produced | distilled at **project end** | **pinned on discovery** + confirmed at end |

## 3. The empirical basis (stress test — 14 real memory records)

Sorting 14 records from the practitioner's own memory into procedural/declarative: **5 clean-context, 5 clean-learning, 4 compound** (~70% unambiguous). The findings that settle the design:

- **Compound ≠ ambiguous.** The 4 "ambiguous" records each *decompose* into a fact + a method (e.g. `contract_paid_usage` = fact *"the `paid_usage` column is a NetSuite field, not consumption"* **+** method *"compute from `paid_usage_metering` with `SUM(usage_dollars)`"*). They span the split; they don't defy it. → produce must **decompose-on-produce, relink-on-consume**.
- **The experiment already ran.** `services/` appears twice in the wild — once filed as a *fact* (`reference_services_folder`), once as a *method* (`feedback_services_pattern`). Two stores occurring spontaneously, months apart, cross-referencing one subject.
- **The `type` field already is this taxonomy.** `user`/`reference`/`project` → declarative; `feedback` → procedural.
- **Both decay models observed live.** Facts carry expiry ("JLL transitioning by May 1", "OOO Mar 31–Apr 4") and rot by change; the per-read staleness banner *is* the freshness discipline. Learnings hold until contradicted, no expiry.
- **Privacy line is legible by eye.** `user_profile` (accounts, comp) = private; `contract_paid_usage` (a shared internal table) and `lakeview_filters` (a product fact) = shareable.

## 4. The fact record (declarative sibling of the learning record)

```yaml
- id: <project>/F<n>
  subject: "main.fin_live_gold.consolidated_active_contracts.paid_usage"  # MERGE KEY: entity+attribute
  fact: "a NetSuite/financial field, not actual consumption — can read wildly high vs real spend"
  kind: schema            # schema | resource | convention | constraint | entity | best-practice
  value: "unreliable for consumption; the real source is paid_usage_metering"
  tags: [databricks, finance, consumption]
  scope: <where this holds>
  asof: 2026-03-27        # when observed/true — facts are point-in-time
  volatility: stable      # stable | slow | volatile → re-verify cadence
  provenance:             # APPENDABLE across projects/users
    - {project: <name>, ref: <D##/audit>, note: "<observed>"}
  trust: personal         # personal | shared | canonical
  shareable: yes          # privacy gate for the enterprise flow
  links: [<project>/L4]   # cross-link to the METHOD in the learning pool (decompose/relink)
  superseded_by: <id>     # optional — when a newer fact replaces this value (never overwrite)
```

Merge key is `subject` (entity+attribute), **not** the whole assertion — so a changed value *supersedes* the old rather than duplicating. **Six `kind`s:** `schema` (a data-source/column truth) · `resource` (where something lives) · `convention` (a standard followed) · `constraint` (a hard rule/limit/policy) · `entity` (a fact about a person/account/project) · `best-practice` (an *endorsed/curated normative standard* — the recommended way; distinct from a `pattern` *learning*, which is "worked for me, not yet endorsed"; a `best-practice` trends `shared`/`canonical` and `links` to the method-learning that grounds it).

## 5. Produce (the core of this design)

Facts differ from learnings in *when* they are produced: a learning is useful only to the **next** project (distill at end); a fact is useful to **this** project's own downstream units (pin the moment it's discovered). So produce has **two moments**, and a decompose discipline.

### 5.1 Pin-on-discovery (mid-project) — the new mechanic

When a worker, doing its unit, discovers a fact ("this column lies"; "this API needs that header"), it **surfaces the fact in its ≤8-line terse return** (never hoards it). The **driver, as single writer, pins it to `.gotm/CONTEXT.md`** (project-local declarative store). This respects the architecture unchanged — worker terse-returns, driver writes. It closes a real gap: today a mid-project discovery lives only as `DECISIONS.md` prose or in chat; formalizing it as a `CONTEXT.md` fact makes it a first-class, **slice-able input** the driver can hand to downstream workers as bounded context.

> Worker return convention gains one line: `FACT: <subject> — <assertion>` (0..n). The driver decides pin vs discard, exactly as it decides record vs discard for a result.

### 5.2 Decompose-on-produce — handling compound observations

A compound observation (fact + method) is **split at produce time**:
- the **fact** → `CONTEXT.md` (declarative, `subject`-keyed),
- the **method** → `LEARNINGS.md` (procedural, `claim`-keyed, existing flow),
- **cross-linked** (`fact.links → learning.id`).

Splitting is strictly better than today's bundle: the fact ("this column lies") stays true even after a better query supersedes the method. Two artifacts, two decay clocks.

### 5.3 Confirm-and-merge (project end) — mirrors the learning merge

At project end, a produce step reads `.gotm/CONTEXT.md` + `DECISIONS.md`, (a) decomposes any still-bundled observations, (b) confirms which facts are transferable and sets `shareable`, (c) sets `volatility`, and (d) **merges the shareable facts into `~/.gotm/context/CONTEXT.md`** via `context.py merge`. Cross-links to the learning records `outcome-analysis` produced in the same pass.

> Dedicated sibling `context-analysis.md` (**LOCKED** — separate from `outcome-analysis.md`; facts and learnings have different trust, so one prompt must not conflate them).

## 6. Consume — relink-on-consume, two-phase, trust-ordered

- **Two-phase consult at bootstrap.** `consult-facts` queries the context pool by `subject`/`tags` → pins relevant facts to project `CONTEXT.md`; the existing `consult` queries the learning pool. Kept as two steps because trust differs (facts are *obeyed*; learnings *inform*) — conflating them is the exact error being fixed.
- **Relink-on-consume.** When a pulled fact has `links`, its linked method is surfaced with it — the `paid_usage` fact arrives *with* its query. Store separate, present together.
- **Trust is 2-axis (RATIFIED — supersedes the old single line; detail in §6a).** Authority and evidence are orthogonal, so a driver resolving a conflict asks two questions:
  > **Axis A — authority:** `canonical` context and `DECISIONS.md` *constrain*. A learning/fact that contradicts either **raises a `QUESTION`**, never silently wins.
  > **Axis B — evidence:** among *informing* knowledge (learnings, `personal`/`shared` facts), weight by **`grounding`** (`observed`/`audited` > `decided`) then by cross-project confirmation count.
  >
  > **The exception that answers the redline:** a well-grounded (`observed`/`audited`), `validated` learning that *directly contradicts* a `DECISIONS.md` choice does **not** silently win **and** is **not** ignored — it **forces re-ratification** (raises a `QUESTION` so the human re-decides with the evidence in view). A `candidate` observed learning surfaces as a note, not a forced QUESTION.

  A consulted fact/learning that shapes a decision is cited in that decision's rationale.

## 6a. Learning-pool ripple — `grounding` + ledger elevation (V4 also touches v3.36)

The 2-axis model needs an **evidence-origin** field on learnings the pool never had. This is V4's ripple into the shipped v3.36 learning pool — additive and back-compatible.

- **`grounding: observed | audited | decided`** on the learning record (`LEARNINGS.md` + the pool): *how* the lesson was known — `observed` (a LEDGER revert/pivot/supersession — reality corrected the agent), `audited` (an independent FAIL→fix verdict), `decided` (a `DECISIONS.md` choice — may be untested). The *within-record* evidence axis; the existing candidate→validated count is the *cross-record* axis. Both feed weight — a `grounding: observed` candidate (n=1, reality-tested) outweighs a `grounding: decided` candidate (n=1, untested) on a tie.
- **Invert `outcome-analysis`'s source ranking.** Today it calls `DECISIONS.md` "the richest source" and the ledger "weak signal" — backwards for transferability. Elevate `LEDGER.md` reverts/supersession-chains + `audits/` FAILs to *primary* sources; recast `DECISIONS.md` as authoritative-but-possibly-untested; **stamp each emitted learning with `grounding`**.
- **Back-compat.** Existing pool records lack `grounding` → absent means `decided`/unknown; the freeze-protected pool is **not** rewritten. `pool.py` still merges on `claim` and may ignore `grounding` initially (weighting promotion by it is a follow-on).
- **Symmetry.** Facts carry authority via `trust`; learnings now carry evidence-origin via `grounding` — the two pools become structurally parallel.
- **`consult.md`** (learning consume) gains a line: read `grounding`, apply Axis B when weighing a learning.

## 7. The bidirectional flow — one store, `trust` encodes origin

The top-down/bottom-up tension dissolves: the context pool is **one store facts flow through in both directions**, and `trust` records which end they came from.

```
   canonical  ▲  curation / endorsement (authority)          ← top-down: org policy DESCENDS,
   shared     │  commonality (≥N users pin same subject)        consumed into a project as a
   personal   │  pinned from my own projects                     `canonical` `constraint` fact
              ▼  consume: tag/subject-filtered into a project
```

- **Bottom-up (the reframe):** my conventions/facts are pinned `personal`; they rise to `shared` when many users independently pin the same subject, to `canonical` when an authority endorses.
- **Top-down (my original framing, now unified):** an enterprise policy/canonical schema is a fact *consumed into* a project's `CONTEXT.md` with `trust: canonical` — received, not earned, obeyed.
- Same store, same schema; the ladder just runs both ways.

## 8. The "different flow" to enterprise (vs the learning pool's)

The practitioner flagged this explicitly. It differs in three concrete ways:
1. **Promotion signal:** learnings promote by *independent confirmation*; facts by *commonality + curation* (recurrence across **users**, then an authority's endorsement — never automatic to `canonical`).
2. **A privacy gate the learning pool lacks:** only `shareable: yes` facts are ever exported upward. The flow is partly a **filter**, not just a promotion.
3. **Supersession not contradiction:** a changed fact archives the old value with its `asof` and takes over; nothing is overwritten (the freeze, applied to facts).

At **L2 (single user)** all facts are `personal`; `shared`/`canonical` + cross-user commonality require the **L3** layer — kept **pluggable**, not built here (exactly as v3.36 left L3 pluggable).

## 9. `context.py` — the tool (sibling of `pool.py`)

Lives in the **plugin** `scripts/context.py` (cross-project → machine-global, not per-project templates). Default dir `$HOME/.gotm/context/`. Every mutating op backs up first and verifies no `subject` dropped.

```
context.py init   [--pool DIR]
    Create context dir + empty CONTEXT.md (header + Index + Records) + .backups/. Idempotent.

context.py merge  <CONTEXT.md> [--project NAME] [--pool DIR]
    - subject exists, same value → APPEND provenance (dedupe by (project,ref)).
    - subject exists, DIFFERENT value → SUPERSEDE: archive old (with asof) as superseded_by; new value takes over.
    - subject absent → add as trust:personal.
    - PROMOTION (personal→shared) requires ≥2 distinct USER ids in provenance → L3-only; never auto at L2.
    - canonical is NEVER set by merge (curation only).
    - shareable:no records are stored locally but flagged NEVER-EXPORT.
    Regenerate Index; print summary (+new, +provenance, superseded, never-export count).

context.py query  --subject S | --tags a,b [--kind K] [--min-trust personal|shared|canonical] [--pool DIR]
    Scan Index; return terse subject-matches (subject · value · trust · asof · volatility). Empty is valid.
    Follows `links` on request (--with-methods) → relink-on-consume.

context.py status [--pool DIR]
    Counts by trust + kind; #subjects; #superseded; #never-export; last-merged; stale (asof past volatility window).
```

## 10. Framework vs plugin (the two-repo split holds)

- **Framework (neutral, the product):** a new short chapter or a §in `docs/07` names the **provenance axis** (session / context / learning) and the facts-vs-experience distinction; `docs/09` gains the context pool as the declarative sibling; new `prompts/{consult-facts, context-analysis}.md` (or extensions) specify the *steps + default location* — prompts, not a runtime. A newcomer with no plugin can adopt from docs alone (docs are the product).
- **Plugin (runtime):** ships `scripts/context.py`, a `/gotm:context` command (init/status/query), the `FACT:` worker-return convention, and wiring in `learn`/`consult`/`bootstrap`. Templates gain `CONTEXT.md.template`.

## 11. Decisions & open questions

> **Trust hierarchy — RATIFIED → 2-axis (see §6 + §6a).** The old single line conflated *authority* (`canonical` context, `DECISIONS.md`) with *evidence* (grounding + confirmation), which are orthogonal. Resolved: Axis A authority (contradiction → `QUESTION`), Axis B evidence (`grounding` + count); a well-grounded `validated` learning vs a `DECISIONS.md` choice **forces re-ratification**, not silent override. Adds `grounding` to learnings and inverts `outcome-analysis`'s ledger ranking (ripples into v3.36, back-compatible). Build units in §13 Phase 1.

**Decided (this redline):**
- **Two stores** confirmed (procedural learning pool + declarative context pool) — the empirical stress test settled it (5 clean-context / 5 clean-learning / 4 compound-that-decompose).
- **Bidirectional flow** confirmed (§7): one store, `trust` encodes origin.
- **`best-practice` — a 6th context `kind`** (`schema | resource | convention | constraint | entity | best-practice`): an *endorsed / curated normative standard* — a **fact about the recommended way** — distinct from a candidate `pattern` *learning* ("worked for me, not yet endorsed"). Trends `shared`/`canonical`; decompose/relink to the method-learning that grounds it. (cf. WAF BPs — curated, authoritative artifacts.) *(Ratified; build units in §13 Phase 1.)*
- **Two produce prompts** — a dedicated `context-analysis.md`, separate from `outcome-analysis.md`. Trust semantics differ; one prompt must not conflate facts and learnings.
- **Two consume steps** — a dedicated `consult-facts.md`, separate from `consult.md`.
- **`context.py` is a separate tool** from `pool.py` (different merge semantics: supersession vs contradiction); may share a small library.

**Still open (resolvable at build):**
1. **Fact merge-key robustness.** `subject` exact-match is brittle (same column, different reference strings). Normalize? Accept manual dedup at L2? Flag.
2. **Mid-project pin — command or discipline?** A `/gotm:pin` command vs pure driver discipline on the `FACT:` return line. (Lean: discipline first; command if friction.)
3. **`CONTEXT.md` bloat.** Facts pinned mid-project accumulate; does the project context store need the born-tiered treatment the ledger has? Likely yes at scale.
4. **Canonical-collision (L3).** An incoming value diverging from a `canonical` record is stored as a separate personal record, leaving two *current* records for one subject; future-merge subject-matching among them is order-dependent (`index_current` takes the first). Dormant at L2 (merge never mints `canonical`) — resolve in the L3/curation design. *(Surfaced by the W-context-tool audit.)*
5. **`--min-trust` vs supersession (consume).** A trust floor can return a superseded-but-trusted record while hiding the current-but-personal one (both observed in the audit). `consult-facts` should prefer *current* records and present trust as a caveat, not hard-filter to stale; consider a `query --current-only` flag. Resolve in **W-consume**. *(Surfaced by the W-context-tool audit.)*

## 12. Version (LOCKED)

**v4.0.** Introduces the second store + the declarative/procedural memory-model reframe — a peer of the learning pool, not an enhancement. (History: "v3.1" drafted → shipped v3.35; naming the shipped version deliberately to avoid that drift — see `design/README.md`.)

## 13. Build plan (driver/worker, dogfooded)

- **W-context-tool** ✅ **verified-done** — `scripts/context.py` (init/merge/query/status) shipped. Worker authored; **driver re-ran an independent proof with its own test data** (auditor ≠ author): supersession retains old value + `asof` & sets `superseded_by`; ≥2-distinct-user promotion `personal→shared`; a superseding record is born `personal` (unconfirmed); `shareable:no` flagged never-export & excluded from `--min-trust shared`; `MISSING: NONE` ×3; relink via `--with-methods`; 3 backups before 3 mutates. Findings → §11 Q4–Q5 (downstream, non-blocking).
- **W-record+templates** ✅ **verified-done** — `templates/CONTEXT.md.template` (mirrors `LEARNINGS.md.template`; declarative analog). Driver re-proved a filled copy merges via `context.py` (`MISSING: NONE`, relink OK). Born-tiering (§11 Q3) deferred — not needed at current scale.
- **W-produce** ✅ **verified-done** — `prompts/context-analysis.md` (two produce moments: pin-on-discovery `FACT:` + confirm-and-merge; decompose/relink; supersede-not-overwrite). Mirrors `outcome-analysis.md`; cross-coherent.
- **W-consume** ✅ **verified-done** — `prompts/consult-facts.md` (two-phase obey-vs-weight; trust hierarchy; §11 Q5 resolved — prefer current + trust-as-caveat, not a stale-preferring filter; relink). Mirrors `consult.md`; cross-coherent.
- **W-docs** ✅ **verified-done** — `docs/07` gained a tight provenance-axis subsection (defers to 09; T1/T2/T3 + diagram intact); `docs/09` gained the context pool as the declarative sibling (comparison table, two-moment produce, bidirectional flow, trust hierarchy, a second mermaid — **driver-validated via mmdc**; learning-pool narrative preserved byte-for-byte).
### Phase 1 — consolidation sweep ✅ **VERIFIED-DONE (both themes)** (framework; one file per unit; fan-out → driver batch-audit)
> Batch audit: `grounding` enum identical across all files; **no stale single-line hierarchy**; `consult`↔`consult-facts` cross-ref fixed; `docs/09` kind enum corrected (`attribute`/`source`→`schema`/`resource`); both mermaids valid; `context.py --kind best-practice` re-proved (merge+query+relink); nit `≥N`→`≥2` fixed.
*Trust theme:*
- **U-learnings-schema** — `templates/LEARNINGS.md.template`: add `grounding: observed|audited|decided` (schema + Index legend + a 2-axis weight line; absent = `decided`). *(new)*
- **U-outcome-analysis** — `prompts/outcome-analysis.md`: invert source ranking (LEDGER reverts/supersessions + audit FAILs = primary; DECISIONS = authoritative-but-untested); add the `grounding` stamp step. *(new)*
- **U-consult** — `prompts/consult.md`: read `grounding`; apply Axis B; note the 2-axis + re-ratification rule. *(new)*
- **U-consult-facts** — `prompts/consult-facts.md`: replace the trust-hierarchy section with the 2-axis rule (facts = Axis A authority). *(edit)*
- **U-docs09-trust** — `docs/09`: rewrite the trust-hierarchy subsection to 2-axis + `grounding`; add `best-practice` to the context-kind mention. *(edit; preserve both mermaids)*

*Best-practice theme:*
- **U-context-analysis-kinds** — `prompts/context-analysis.md`: six kinds; `best-practice` framing (endorsed standard vs pattern-learning); "five kinds"→six; align the worked-example subject. *(edit)*
- **U-context-template-kinds** — `templates/CONTEXT.md.template`: add `best-practice` to the kind enum (2 spots); "≥N users"→"≥2". *(edit)*
- **U-contextpy-kinds** — `scripts/context.py`: add `best-practice` to `KINDS` + docstring; driver re-proves `--kind best-practice`. *(driver-done)*

### Phase 2 — plugin wiring (driver-managed; release mechanics)
> **Note:** plugin `templates/prompts/` are *adapted* copies (orchestrating-LLM voice; `/gotm:` refs; `.gotm/` paths; `$CLAUDE_PLUGIN_ROOT`) — changes were **merged** in, not copied.
> **⚠ Safety event:** a commands-worker ran `rm -rf ~/.gotm/context` during CLI verification. Driver-audited: **no data lost** (home pools never populated on this machine; `~/.gotm/` empty). Memoized → `feedback-worker-destructive-ops`. Drives **U-worker-guard**.
- **U-plugin-prompts** ✅ — merged into adapted copies: `outcome-analysis` (ledger inversion + `grounding` stamp), `consult` (grounding + 2-axis), `worker-dispatch` (`FACT:`), `LEARNINGS.md.template` (grounding); created adapted `context-analysis`, `consult-facts`, `CONTEXT.md.template` (round-trips via `context.py`).
- **U-plugin-commands** ✅ — new `commands/context.md` (`/gotm:context`); wired `consult`/`learn`/`bootstrap` (both pools; grounding stamp). *(deviation flagged: `learn.md` merge-semantics wording inferred from CLI — verify in audit.)*
- **U-plugin-version** ✅ — `plugin.json` → **4.0.0**, description **188 chars**. *(marketplace.json sync = release step.)*
- **U-worker-guard** ✅ — destructive-op guard added to both `worker-dispatch.md` (framework + plugin voices; new rule in "Rules the worker obeys").
- **U-plugin-readme** ✅ — plugin README **body** updated (8 commands incl. `/gotm:context`, 8 prompts, `context.py`, context pool + 2-axis + grounding overview, 4.0.0 changelog — body, not just changelog).
- **U-plugin-audit** ✅ — driver coherence pass done; `learn.md` nits fixed (promotion = ≥2 users not projects; supersede-on-differing-value; `shareable` default-yes; never-export merges-flagged, not skipped).

### Phase 3 — finalize
- **U-coherence-audit** ✅ — cross-repo sweep **GREEN**: 8 commands / 8 prompts; worker-guard ×2; shareable-default-yes ×4; `grounding` enum consistent; **no stale hierarchy**; README 14 v4 markers; framework `CONTEXT.md.template` round-trips via `context.py` (`MISSING: NONE`).
- **Release** ✅ **SHIPPED / LIVE** — **Framework:** PR #1 → `main` (`0d80729`); positioning follow-ups #2–#4. **Marketplace:** PR [#8637](https://github.com/databricks-eng/plugin-marketplace/pull/8637) **MERGED 2026-07-09 18:52 UTC** (owner-approved; auto-merge squash via merge queue) — **v4.0.0 live on the experimental marketplace** (`plugin.json` 4.0.0 on monorepo main). Consistency verified (4.0.0 / 188-char); `__pycache__` excluded, `REVIEWERS` preserved.
