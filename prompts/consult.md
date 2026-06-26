---
prompt: consult
purpose: pull transferable learnings from past projects into the project at hand — the read-in from the cross-project cold tier
audience: the driver (you read this, then produce the project's CONSULTED.md)
license: Apache 2.0
---

# Consult prompt

Run this **at the start of a project** (in bootstrap) — and again whenever the work
turns to a new stack, surface, or phase. It is the *consuming* half of the
cross-project learning loop (framework `docs/09-learning-across-projects.md`), the
mirror of [`outcome-analysis.md`](outcome-analysis.md): where outcome-analysis
*writes out* learnings at the end of a project, this one *reads them in* at the
start of the next, so the build loop skips mistakes earlier projects already paid
for.

The learning pool is the **cross-project analog of the store** — the cold tier one
level up. Inside a project the store reconstructs a worker's context; across
projects the pool plays the same role for this **driver**, which (like every fresh
context) is born without history. This is the **read-in from that cold tier**: it
seeds the new driver the way the store seeds a worker, letting it skip lessons
earlier drivers already bought instead of re-discovering them at full cost.

This is **not** an audit and **not** a foundation unit that produces a deliverable.
It produces a short context note — the project's working set of relevant prior
lessons — and nothing it surfaces is binding; see *Confidence* below.

## The pool — where past learnings live

`outcome-analysis.md` writes one `LEARNINGS.md` per finished project. Consulting
reads across a **pool** of them. Where the pool lives is a **platform binding**, not
fixed by this framework (the same boundary `docs/09` draws around it). In ascending
order of reach:

- a **configured list** of `LEARNINGS.md` paths, or a **sibling-repo glob**;
- a **user-level pool** that a practitioner's projects deposit into and read from;
- an **enterprise** index / knowledge graph (the broadest sink — a context
  catalog).

If no pool exists yet, that is a valid result: record "no pool consulted" and move
on. A produce step with no consumer is the gap this prompt closes — so even a dumb
file-glob over one folder beats consulting nothing. Be honest about an empty pool;
"nothing relevant found" is a valid, auditable result, never a silent skip.

## What to do — scan the index, expand on match

The point is to spend **few tokens** — the same hot-path discipline the store uses
inside a project. Scan cheap one-line index entries, expand the full record only for
the handful that apply; the cold detail loads only when a tag pulls it onto the hot
path, and no further.

1. **Name this project's tags.** From the mission + the first units: the stack
   (languages, platforms, libraries, APIs), the domain, and the current phase
   (`design` / `build` / `deploy`). These are your filter.
2. **Scan the pool's indexes.** Each `LEARNINGS.md` leads with a generated Index —
   one tag-prefixed line per record. Read the indexes, not the full records.
3. **Tag-filter.** Keep index lines whose tags intersect this project's tags. Drop
   the rest unread.
4. **Expand the matches.** For the kept lines only, read the full record (`claim`,
   `fix`, `scope`, `evidence`, `confidence`). Discard any whose `scope` clearly
   does not fit this project after all.
5. **Surface them where the driver and its workers will look.** Write the survivors
   to a context note in the store — `CONSULTED.md` — grouped by the phase or area
   they bite. A `prerequisite` becomes an early to-do; a `gotcha`/`anti-pattern`
   becomes a thing to avoid; a `pattern` becomes a suggested approach. The driver
   carries the surviving lines; their detail still lives a pointer away.

## Confidence — a candidate is an anecdote, not a law

Carry each learning's `confidence` through to the note, and weight accordingly:

- **candidate** — seen in one project (n = 1). A hint to check, not a rule to follow
  blindly. If this project contradicts it, that is signal — flag it for the
  *produce* step (the contradiction demotes the learning; see `docs/09`).
- **validated** — independently confirmed by a second project. Trust more.
- **core** — broadly applicable, enterprise-curated. Treat as common knowledge.

Never let a consulted learning override a project decision silently. It informs;
`DECISIONS.md` still governs. A learning that shapes a decision is cited in that
decision's rationale (`evidence` flows both ways).

## Output

Write `CONSULTED.md` to the store: a short header naming the pool consulted and this
project's filter tags, then the surviving learnings grouped by where they apply,
each with its `claim`, `fix`, and `confidence`. If the pool was empty or none
matched, say so plainly. One file; it is context, not a frozen deliverable, and may
be refreshed when the work moves to a new area.

→ The producing half is [`prompts/outcome-analysis.md`](outcome-analysis.md); the
loop they close is described in
[`docs/09-learning-across-projects.md`](../docs/09-learning-across-projects.md).
