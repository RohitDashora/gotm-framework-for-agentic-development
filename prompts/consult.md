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

## The pool — a real merged store

`outcome-analysis.md`'s produce step doesn't just write a lonely `LEARNINGS.md`; it
**merges** each project's records into a shared pool. So consulting is not a glob over
scattered files — it is a **query over one merged store**: a single corpus holding one
record per `claim` (with `evidence` appended across the projects that hit it), fronted
by a regenerated tag Index. The pool lives at the **user tier** — a convention
location, default `~/.gotm/learnings/` (resolved from `$HOME`, so it is cross-project
by construction); reading it is a **platform binding** (a generically-named query
operation over the pool dir), the same boundary `docs/09` draws around the store. It is
the L2 rung of a scope ladder that reaches, higher up, a team git repo or an enterprise
index / knowledge graph — pluggable via a `--pool`-style override, not built here.

If the pool is empty or does not exist yet, that is a valid result: record "no pool
consulted" and move on. Be honest about an empty pool; "nothing relevant found" is a
valid, auditable result, never a silent skip.

## What to do — scan the index, expand on match

The point is to spend **few tokens** — the same hot-path discipline the store uses
inside a project. Scan cheap one-line index entries, expand the full record only for
the handful that apply; the cold detail loads only when a tag pulls it onto the hot
path, and no further.

1. **Name this project's tags.** From the mission + the first units: the stack
   (languages, platforms, libraries, APIs), the domain, and the current phase
   (`design` / `build` / `deploy`). These are your filter.
2. **Query the pool by tag.** Run the pool's query over its generated Index — one
   tag-prefixed line per record — filtering to the tags from step 1. Read the Index,
   not the full records; the query returns the tag-intersecting entries tersely.
3. **Tag-filter.** Keep the entries whose tags intersect this project's tags. (The
   query does this; sanity-check its output.) Drop the rest unread.
4. **Expand the matches.** For the kept entries only, read the full record (`claim`,
   `fix`, `scope`, `evidence`, `confidence`). Discard any whose `scope` clearly
   does not fit this project after all.
5. **Surface them where the driver and its workers will look.** Write the survivors
   to a context note in the store — `CONSULTED.md` — grouped by the phase or area
   they bite. A `prerequisite` becomes an early to-do; a `gotcha`/`anti-pattern`
   becomes a thing to avoid; a `pattern` becomes a suggested approach. The driver
   carries the surviving lines; their detail still lives a pointer away.

## Confidence — a candidate is an anecdote, not a law

The confidence a consulted record carries is **meaningful** because the pool's merge
enforces a promotion gate: `candidate → validated` happens only when an *independent*
project confirms the same `claim` (≥2 distinct projects in its evidence), and a
contradiction *demotes + flags* rather than silently overwriting. So the weight below
is earned, not self-asserted — carry each record's `confidence` through to the note
and weight accordingly:

- **candidate** — seen in one project (n = 1). A hint to check, not a rule to follow
  blindly. If this project contradicts it, that is signal — flag it for the
  *produce* step; the merge marks it `contested` and demotes it (see `docs/09`).
- **validated** — independently confirmed by a second project (it cleared the gate).
  Trust more.
- **core** — broadly applicable, enterprise-curated (never set by merge). Treat as
  common knowledge.

Never let a consulted learning override a project decision silently. It informs;
`DECISIONS.md` still governs. A learning that shapes a decision is cited in that
decision's rationale (`evidence` flows both ways).

## Output

Write `CONSULTED.md` to the store: a short header naming the pool consulted (its
location) and this project's filter tags, then the surviving learnings grouped by
where they apply, each with its `claim`, `fix`, and `confidence`. If the pool was
empty or none matched, say so plainly. One file; it is context, not a frozen
deliverable, and may be refreshed when the work moves to a new area.

→ The producing half is [`prompts/outcome-analysis.md`](outcome-analysis.md); the
loop they close is described in
[`docs/09-learning-across-projects.md`](../docs/09-learning-across-projects.md).
