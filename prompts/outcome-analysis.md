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

- **`DECISIONS.md`** — the richest source. Every decision carries its rationale;
  reversals and refinements mark the **pivots** (a constraint forced plan A → B).
  Most learnings come from here.
- **`audits/`** — findings, especially a class of issue that **recurs across
  units**, are **anti-patterns**: a warning the auditor kept having to give.
- **`LEDGER.md`** — supersession chains and the recovery log show where work
  churned and why; weaker signal, useful context. Read the archive tier here, not
  just the frontier — closed units are exactly what holds the finished lessons.

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
4. **Dedupe.** Two records describing the same trap collapse into one `claim` with
   multiple `evidence` entries.
5. **Tag** for retrieval — tech, domain, and (optionally) the phase where the lesson
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
([`consult.md`](consult.md)) reads exactly this. A produce step with no consumer is
a write-only void, so the loop is only closed once a later driver consults what this
one deposited.

→ The consuming half is [`prompts/consult.md`](consult.md); the loop they close is
described in [`docs/09-learning-across-projects.md`](../docs/09-learning-across-projects.md).
