# Project protocol

This file is the operating contract for this project. Every agent that opens a session here reads it first and works under it — every session, not once.

The framework this protocol implements is described in [`../docs/`](../docs/01-the-problem-and-thesis.md) — read those once for understanding, this file every session. The operational moves it points to (the loop, dispatch, audit, boot) live in [`../prompts/`](../prompts/); read the relevant prompt when you make that move.

> **Layout (this repo).** This project keeps its store in `.gotm/` (this file, `LEDGER.md`, `DECISIONS.md`, `QUESTIONS.md`, `audits/`), so the repo root stays reserved for the framework's produced assets (`docs/`, `prompts/`, `templates/`). Paths to `docs/` and `prompts/` resolve as `../` from here; the other store members are siblings. *Where the store physically sits is a layout choice bound by the harness, not by the framework* — this repo is a live worked example of the subfolder layout (see [`../docs/08-in-practice.md`](../docs/08-in-practice.md)).
>
> **Session-context dependency (don't break this).** Many harnesses auto-load a context file from the *project root* on session start (a root `CLAUDE.md`, `.cursorrules`, or equivalent). Moving that file into `.gotm/` silently stops the auto-load — no error, just quiet erosion. The root `CLAUDE.md` stays at the root as a thin bridge that points here, for exactly this reason.

## The thesis (why any of this)

> **GOTM is a context-economy discipline. The store is the system of record; every working context is disposable and reconstructable from it. Nothing on the hot path is long-lived.**

Everything below is a consequence of that sentence. The store reconstructs working context — so a session can end at any moment (crash, `/clear`, compaction, closed terminal) and lose nothing. State that lives only in a context is not real state.

## The three roles

| Role | Lifetime | Holds | Never holds |
|---|---|---|---|
| **Driver** — the conversation agent | long-lived, **checkpointed** (re-hydratable from the store) | the plan (the ledger DAG), this protocol, the human interface (ratification ladder), the scheduler loop | work artifacts, raw inputs, execution/build/deploy state |
| **Worker** — a dispatched subagent | **ephemeral** — one unit, then discarded | only its bounded inputs + its spec; produces exactly one output; returns a terse structured result | any cross-unit state; any context from a prior worker |
| **Store** — the durable file-set + the repo | durable, **tiered** | hot **frontier** (active units + recovery window) + cold **archive** (closed detail) | — |

**The load-bearing rule:** *the driver plans, talks, and gates; **all work — however small — is a worker dispatch**.* The driver is the **single writer** of the store. It never edits a work artifact, never reads bulk input (it dispatches a read-and-summarize worker when it must inspect), and never holds a worker's output body — only a pointer. The one long-lived context carries the index, not the work.

This is *not* optional for "small" tasks. A one-line fix is still a worker dispatch (batched into a partition-worker if there are several — see [`../prompts/worker-dispatch.md`](../prompts/worker-dispatch.md)). The moment the driver edits an artifact itself, the discipline is gone.

## The five rules

**1. Single writer, single ledger.** The ledger is authoritative, and **only the driver writes it**. State not in the ledger is not real state; if two documents disagree, the ledger wins. Workers report results; the driver records them. (One hand writing the ledger is what makes the v2 duplicate-row race impossible by construction.)

**2. Atomic units = dispatch specs.** Each row in the ledger is one **self-contained worker dispatch** — bounded inputs + one named output + spec + constraints, complete without the conversation. One deliverable, not two, not "and a small revision." A thing and its test are one unit (build-and-test is one pass); *unrelated* outputs in one unit are forbidden. If a planned unit hides more than one output, split it before dispatching.

**3. Foundation before drafts — enforced by the DAG, not vigilance.** The ledger is a **DAG**: foundation units are upstream nodes; drafts depend on them. A unit with an unmet dependency is simply absent from the ready set. Drafts that begin before foundation closes fail by producing fluent prose grounded in nothing — the topology prevents it.

**4. Audit before downstream consumes — by an independent worker.** Every authored-done unit is checked by a *fresh* context (never its author) before anything downstream depends on it. Findings become new ledger units, not edits to closed ones. See *Audit gates*.

**5. Ratification ladder routes human decisions.** Some decisions are the human's; the ladder names which and routes them to `QUESTIONS.md`. See next section.

## The ratification ladder

When a question or decision arises during work, classify it and route:

| Layer | What it covers | What happens |
|---|---|---|
| **Mission** | mission, audience, scope, license, what counts as done | Route to `QUESTIONS.md`. The driver waits. |
| **Execution** | next unit, sequencing, length band, atomic split, dispatch shape, audit weight | The driver decides, records in the ledger or `DECISIONS.md`, proceeds. |
| **Ambiguous** | could be either; judge materiality | Surface with a `MATERIAL?` flag. The human routes it. |

The boundary is fixed: the human is never surprised by a mission-level decision made unilaterally, and never pulled into an execution choice. The ladder lives in the driver — the only context that talks to the human.

## The loop — the driver's scheduler

The driver runs a deterministic scheduler over the DAG. Full discipline: [`../prompts/driver-loop.md`](../prompts/driver-loop.md). In brief, repeat until the DAG drains:

1. **Read the frontier → compute the ready set** (deps satisfied *and* audit gate open). Read the frontier, never the history.
2. **Fan out** — dispatch a fresh worker per ready unit, in parallel, bounded by a **concurrency cap** (backpressure). Each carries only its bounded payload.
3. **Collect → record (single writer).** Each worker returns a **terse result** (pointer + index facts, never the body); the driver records status + pointer.
4. **Audit → advance the gates.** Dispatch a separate audit worker per authored-done unit; runtime units also get a `verified-done` worker. A passing verdict opens the gate for downstream.
5. **On failure → retry on a fresh worker** (inputs on disk = lineage recompute).
6. **Checkpoint** — compact the frontier when over band; re-hydrate on any fresh start.

**The hard rule — fan-in is a worker, never the driver.** When N outputs must be merged (drafts → an arc, findings → a report), the merge **is a unit**: dispatch a fan-in worker that reads the N bodies *from the store* and returns one pointer. The driver records one row. Never pull N bodies into the driver to stitch them — that re-concentrates work into the long-lived context at every join, the exact monotonicity the role split exists to forbid. Default to **pipeline** (siblings flow author → audit → done independently); use a **barrier** only when a downstream genuinely needs all upstreams at once (synthesis, cross-unit audit, dedup/merge, the foundation→drafts gate), with an explicit barrier-failure policy.

## The worker contract

Full contract: [`../prompts/worker-dispatch.md`](../prompts/worker-dispatch.md). A worker is born **stateless** — it has never seen the conversation, the mission, the ledger, or any prior worker — so everything it needs is in the dispatch. The test: *a fresh worker executes it from the dispatch alone.*

- **Worker-context minimalism.** The dispatch carries exactly five things: a discipline pointer (read this protocol), unit identity, the **bounded inputs it actually consumes** (never the whole ledger, sibling outputs, or the conversation), one output path, and spec + constraints. A worker that needs more **reads it from the store itself** or **fans out** — the driver never broadens context "just in case."
- **Terse structured result, not work product.** A worker returns a pointer plus a few index facts. The body stays on disk.
- **Workers do not write the ledger** (or decisions, or questions). They produce one output and report; the driver — single writer — records.
- **Workers mark `authored-done` only — never self-certify.** A producing worker can state the artifact exists; it can **not** confer `verified-done`. By audit time the executor is already discarded, so self-grading is structurally impossible.
- **Amortized batching.** Always dispatch — but a litter of one-line fixes is one **partition-worker** (overhead paid once), and a unit that would blow its band **fans out** into a tree. Size every payload to *minimal sufficient* — neither padded nor starved. There are no project token budgets; economy comes from lean payloads.

## Audit gates

Rule 4 in full. Two properties make the check meaningful — **structural independence** and a **gate** — and the ledger tracks audit state in its own `Audit` column. The auditor's own dispatch is [`../prompts/audit.md`](../prompts/audit.md).

**Independence is structural, not a rule to remember.** The executor that produced the unit is an ephemeral worker, **already discarded** by the time anything checks it — so auditor ≠ author is not vigilance, there is no author left to grade itself. The driver dispatches a **separate audit worker every time**: fresh context, given only the **target output + the oracle** (the unit's inputs / spec / the relevant ledger), never the authoring session's transcript. One unit per audit, one report (`audits/<Uxx>.md`).

**authored-done vs verified-done are distinct states.** **authored-done** = the output exists and a producing worker reported it. **verified-done** = an independent worker checked it — and for any **deploy / infra / data** unit, *exercised the live artifact as its real consumer* (a green build or a clean exit is **not** verification — only a real-consumer check is). Only an independent worker confers verified-done.

**The 7-point checklist.** Unless the unit calls for a specialized check, the auditor runs all seven: (1) **existence** — output exists at the stated path; (2) **spec match** — content matches what the unit promised; (3) **cross-reference integrity** — every `D<n>`/`U<n>`/`Q<n>` cited exists and says what's claimed; (4) **internal consistency** — no contradictions; (5) **decision fidelity** — honors the relevant `DECISIONS.md` entries; (6) **enforcement check** — for each *behavioral* decision, is there a gate/config/assertion that makes it hold, or is it only prose? (a documented-but-unenforced decision is a finding); (7) **multi-site claim check** — any "wired into both X and Y" / "applied across N sites" / "replaced everywhere" claim is verified by grep/count, not by trusting the prose. *(Checks 6–7 close the two blind spots that produced the only field FAILs: a documented-but-unenforced decision, and a half-applied bulk fix.)*

**Verdict — one of three.** **`PASS`** (no findings above trivial); **`PASS-FINDINGS`** (consumable, but carries MEDIUM/LOW findings that become tracked non-blocking follow-on units); **`FAIL`** (one or more HIGH findings — blocks). HIGH ⇒ FAIL; MEDIUM/LOW-only ⇒ PASS-FINDINGS; clean ⇒ PASS.

**The gate.** A downstream unit may **consume** an input only when that input's `Audit` is a passing verdict (`PASS` / `PASS-FINDINGS`). Drafts and code do not build on `pending` or `FAIL`. `done` (the output exists) and a passing verdict (an independent context checked it) are distinct — the column keeps them honest. **Findings become units, never edits:** the auditor does not fix; HIGH findings become fix units, MEDIUM/LOW become tracked follow-ons, and the audited output stays frozen.

**Weight the audit by risk** (worker economy, not a project budget): a full independent audit for keystone/deploy/runtime units; a light existence+spec+compile worker for mechanical ones — don't spend a heavy audit where it isn't warranted, but never skip the gate.

## Anti-drift & the freeze

The discipline erodes two ways — **silent work** (acting without writing back) and **quiet edits** (changing a frozen artifact instead of appending). Guard against both, every turn.

**Done outputs are frozen — change comes through a follow-on unit.** Before any edit/write, check the ledger: if the target is a `done`/`*-done` unit's output, **do not edit it**. Append a follow-on (or superseding) unit and put the change in the *new* unit's output. Same for prior substantive `DECISIONS.md` / `QUESTIONS.md` entries — append, don't rewrite (marking a Status line `answered` or `superseded by D<n>` is the one allowed exception). **Living governance docs** (`PROTOCOL.md`, `README.md`, the root context file) stay editable.

**Follow-on ownership.** A follow-on unit *may* legitimately own a change to a done output (a fix, a refinement). This is not a freeze violation — it is the sanctioned mechanism, and a wired immutability hook **honors it**: the active follow-on owns the change, so the edit is allowed under that unit while every *unowned* edit to a frozen output is still refused. Register a follow-on `pending`/`in_progress`, never `done` — registering it `done` before its output exists would freeze the very file you were about to write.

**Write-back is the same turn as the work.** Never end a turn that created or changed a unit's output without, in that turn, updating the ledger (and `DECISIONS.md` / `QUESTIONS.md` as needed). Output without write-back means the unit is **not** done. A finding is *never* a silent edit — it becomes a unit.

> **Mechanical enforcement lives in tooling, not here.** The freeze can be *enforced* — a pre-tool hook can refuse an edit whose target is an unowned frozen output. This framework is paste-able prompts by design; runtime enforcement bindings (the immutability hook, the session-start re-hydration hook) belong in adopter tooling, e.g. a plugin.

## Resilience — no context loss across any session end

The core promise: on-disk state alone reconstructs full working context, so an accidental session end with no resume loses nothing. There are two failure modes and two recoveries.

- **Worker crash = retry / lineage.** A crashed, timed-out, or failing worker → dispatch the *same* unit to a *new* worker. Safe by construction: a unit is a function of its bounded inputs, and those inputs live on disk — re-running is a **lineage recompute**, not a salvage of partial state. A unit that keeps failing escalates via the ratification ladder.
- **Driver crash = re-hydrate from the store via the session-start reconcile.** On *any* fresh start (cold restart, `/clear`, or the far side of a compaction) the driver rebuilds its working set from the store — there is **NO compaction hook dependency**. The honest limit (design §4): the interactive driver *is* the session and cannot self-trigger `/compact`; so re-hydration depends only on the store, which is exactly why the same boot works on every kind of fresh start. Full sequence: [`../prompts/session-start.md`](../prompts/session-start.md) — read protocol + frontier, reconcile against disk (heal drift before acting), re-hydrate the manifest (active unit + inputs as **pointers** + recovery-log window + open questions), then hand to the loop.

**Reconciliation heals drift, never silently.** A `done` unit whose output is missing → reopen it. An output that exists for a non-`done` unit → finalize or supersede. An `in_progress` unit → resume/verify exactly it. Record what reconciliation did in the recovery-log window — recovery is auditable.

**Compaction is born-tiered, lossless, and not a freeze violation.** The ledger is *born* tiered (hot frontier + cold archive), not compacted as an afterthought. At reconcile, when the frontier exceeds a size/count threshold, **compact**: rewrite each closed-and-verified unit's frontier cell down to a one-line **archive** entry that keeps its audit pointer, and roll the **recovery-log window** forward. This is **lossless** (every removed fact lives one pointer away in the cold tier) and an **index operation, not an edit to a frozen output** — you rewrite a ledger cell, never a unit's artifact. It is therefore *not* a freeze violation. Below threshold, skip it.

## Off-mission artifacts

Sometimes the human asks for something that does not serve the mission — a side note, a one-off export, meta-feedback about the process. "Everything is a unit" tempts you to file it in the unit table, but it isn't mission work and would pollute the DAG.

Convention: **produce the file, then drop a one-line breadcrumb in the ledger's recovery log marked _not a mission unit_.** Do not add it to the Units table. Traceability without distorting scope.

## Common moves

| Move | Prompt |
|---|---|
| Starting / re-hydrating a session | [`../prompts/session-start.md`](../prompts/session-start.md) |
| Running the scheduler loop | [`../prompts/driver-loop.md`](../prompts/driver-loop.md) |
| Dispatching a worker | [`../prompts/worker-dispatch.md`](../prompts/worker-dispatch.md) |
| Auditing a claimed-done unit | [`../prompts/audit.md`](../prompts/audit.md) |
| Consulting / producing cross-project learnings | [`../prompts/consult.md`](../prompts/consult.md), [`../prompts/outcome-analysis.md`](../prompts/outcome-analysis.md) |

If a move has no prompt yet, do it carefully and add the prompt as you go.

## Mission (this project)

> Distill the GOTM discipline into a public-ready framework — concept docs, a project protocol, prompts, and templates — that any LLM practitioner can adopt to survive bounded-context agentic execution.
