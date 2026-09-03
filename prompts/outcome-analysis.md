---
prompt: outcome-analysis
purpose: distill a finished GOTM project's record into transferable learnings — the write-out to the cross-project cold tier
audience: the driver (you read this, then produce the project's LEARNINGS.md)
license: Apache 2.0
---

# Outcome-analysis prompt

Run this **once, when a project is done** (or at a major milestone). It reads the
project's own GOTM record and distills the **transferable** lessons a future
project shouldn't have to re-learn — the *producing* half of the cross-project
learning loop (framework `docs/09-learning-across-projects.md`). The output is the
project's `LEARNINGS.md`, scaffolded by `templates/LEARNINGS.md.template`.

Think of `LEARNINGS.md` as the **cross-project analog of the store** — one level
up. Inside a project the store reconstructs a worker's context; across projects the
learning pool plays the same role for the **next project's driver**, seeding it so
it skips the mistakes earlier drivers already paid for. This prompt is the
**write-out to that cold tier**: closed-out lessons that never sit on any driver's
hot path, pulled only when a future project's tags match (the consume half,
[`consult.md`](consult.md)).

Run it as a single pass — not as a fan-in over many workers. It reads the whole
finished record (the store) and generalizes across it. Like any pass it is
transcript-independent: the on-disk record is sufficient.

This is **not** an audit. An audit checks one unit against its spec; this reads the
*whole* project and generalizes across it.

## What to read — the record already holds the "why"

A GOTM project wrote its reasoning down as it went; that is the raw material. You
do **not** need the chat transcript — transcript-independence means the store is
sufficient.

- **`LEDGER.md`** — the **primary, richest** source. Reverts, supersession chains,
  and retries record what **reality did to the plan** — the strongest gotchas and
  anti-patterns, because a revert is *evidence* (something actually went wrong), not
  intention. Read the archive tier here, not just the frontier — closed units are
  exactly what holds the finished lessons.
- **`audits/`** — equally primary. An independent FAIL→fix verdict, especially a
  class of issue that **recurs across units**, is an **anti-pattern**: a warning the
  auditor kept having to give, grounded in a real correction.
- **`DECISIONS.md`** — **authoritative but possibly untested**. Every decision
  carries its rationale, so still read it — it is where the *why* lives. But a
  decision is an **intention** that may never have been exercised; it is weaker
  evidence than an observed correction (a ledger revert or an audit FAIL).

**Graph-evolution telemetry is instrumentation, not a learning source — do not
distill learnings from it.** It is an append-only record of DAG mutations
(actor + reason), captured for operational visibility. Learning *from* the
shape of graphs is a later version's subject; the sources above are unchanged.

## How to extract — filter, generalize, dedupe

1. **Filter to transferable.** Keep only claims a *different* project could act on.
   Drop one-off, project-specific detail (a typo'd field, a local naming choice) —
   it stays in the record; it is not a learning.
2. **Generalize.** Strip the project-specific nouns; keep the load-bearing
   specifics (a platform, a library, an API behavior *is* the reusable part). State
   each as advice to a future project, not a diary entry.
3. **Classify** each into a `kind`: **gotcha** (trap / use-X-not-Y),
   **prerequisite** (do/grant/verify X before Y), **pivot** (a constraint forced a
   change), **pattern** (worked, repeatable), **anti-pattern** (failed, repeatable —
   often a recurring audit finding).
4. **Stamp `grounding`** — how the learning was *known*: **`observed`** (from a
   `LEDGER.md` revert / pivot / supersession — reality corrected the agent),
   **`audited`** (from an independent `audits/` FAIL→fix verdict), or **`decided`**
   (from a `DECISIONS.md` choice — an intention that may be untested). `observed` and
   `audited` are the strongest evidence; `decided` is authoritative-but-possibly-untested.
5. **Dedupe.** Two records describing the same trap collapse into one `claim` with
   multiple `evidence` entries.
6. **Tag** for retrieval — tech, domain, and (optionally) the phase where the lesson
   bites (`design` / `build` / `deploy`).

## The record — source of truth

Emit each learning as a structured record per `templates/LEARNINGS.md.template`:

    - id: <project>/L<n>
      claim: "<generalized lesson — the merge key>"
      kind: <gotcha|prerequisite|pivot|pattern|anti-pattern>
      tags: [<tech>, <domain>, <phase>]
      fix: "<what to do instead — actionable>"
      scope: <where it applies>
      evidence:
        - {project: <this project>, ref: <D## / audit Uxx>, note: "<observed>"}
      confidence: candidate
      grounding: <observed|audited|decided>
      strength: "<within-project weight>"

Then generate the **Index** at the top of `LEARNINGS.md` — one tag-prefixed line
per record. The index is the cheap hot-tier read: future projects scan it, not the
full records; the records are what an aggregation layer ingests.

## Confidence — be honest about n = 1

Everything a single project produces is a **`candidate`**. Recurrence *within* the
project raises `strength`, not confidence — a lesson reaches **`validated`** only
when an **independent** project confirms the same `claim` (the *auditor ≠ author*
rule of `docs/06-keeping-it-honest.md`, lifted across the project boundary). The
authoring project can never self-promote; only a different, later project confers
validation, and a contradiction demotes. Aggregation, validation, and any user- or
enterprise-level pool are downstream of this prompt; your job here is to emit
well-formed, honest **candidate** records.

## Output

Write `LEARNINGS.md` to the store (project root, or under the subfolder layout),
from the template: header, generated Index, Records, and the merge model. One file.
It ships with the project as its contribution to the pool — the project's down
payment on the next one. A future project's *consume* step
([`consult.md`](consult.md)) reads exactly this.

## Learn as a meta-unit (GOTM 4.5 discipline)

The `learn` unit is **dependency-gated** on the settled subtree it distills (cannot run on un-audited work). It is **independently audited for faithfulness** (not sufficiency — every learning traces to a real settled unit; contradictions flagged). It is **tier-matched and delegated** like any unit. Results go to **L1 (project-local store)** — high-volume, private, allowed to be messy/contradictory. At project end, a deliberate reconciliation pass promotes **verified L1 → L2** (cross-project pool) as concise, curated, transfer-grade records. The `learn` unit is separate from milestone closure; the driver must **explicitly decide** (deliberate-or-defer prompt) whether to harvest learnings at each milestone.

## Merge into the shared pool — the write-back step

Emitting `LEARNINGS.md` is only half the produce step. The pool is a **real merged
store**, not a folder of lonely per-project files — so the loop **merges this project's records into it now**. The pool is the **L2** cross-project store at the **user tier** — a merged corpus that lives at a
convention location (default `~/.gotm/learnings/`, resolved from `$HOME`), holding one record per `claim` with an appendable
`evidence` list, fronted by a regenerated tag Index. Merge is a distinct, concrete
step run after the file is written (a platform binding — a generically-named merge
operation over the pool dir):

1. **Merge by claim key.** For each record, if its `claim` already lives in the pool,
   **append** this project's `evidence` (dedupe by `(project, ref)`) to the existing
   record — never duplicate the record. If the `claim` is absent, **add** it as a new
   `candidate`.
2. **Promote on independent projects.** After appending, a claim whose `evidence`
   now spans **≥2 distinct projects** promotes `candidate → validated` — an
   *independent* project confirmed it (the *auditor ≠ author* rule of
   `docs/06-keeping-it-honest.md`, lifted across the project boundary, mechanized as
   distinct `project` values). The authoring project can never self-promote.
3. **Contradiction demotes.** An incoming record whose `fix`/`claim` **opposes** an
   existing one does **not** overwrite it: mark the existing record `contested`,
   append the conflicting evidence with a note, and if it was `validated`, demote it
   `→ candidate`. Every contested claim is flagged in the merge summary for a human
   to resolve. `core` is never set by merge (enterprise-curated only).
4. **Regenerate the Index and report** what merged: new candidates, evidence
   appends, promotions, contested claims.

This promotion gate is what keeps the shared pool from rotting — so the confidence a
record carries when a later project *consults* it is meaningful, not self-asserted.
A produce step with no consumer is a write-only void; a merge that never happens is
that void. The loop closes only once records reach the pool and a later driver
consults what this one deposited.

→ The consuming half is [`prompts/consult.md`](consult.md); the loop they close is
described in [`docs/09-learning-across-projects.md`](../docs/09-learning-across-projects.md).
