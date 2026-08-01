---
prompt: consult-facts
purpose: read authoritative facts in from the shared context pool into the project at hand — the declarative read-in from the cross-project cold tier
audience: the driver (you read this, then produce the project's CONSULTED-FACTS.md)
license: Apache 2.0
---

# Consult-facts prompt

Run this **at the start of a project** (in bootstrap) — and again whenever the work
turns to a new stack, surface, or domain. It is the *consuming* half of the
cross-project **fact** loop, the mirror of [`context-analysis.md`](context-analysis.md):
where context-analysis *writes out* facts at the end of a project, this one *reads
them in* at the start of the next, so the build loop starts already knowing what
earlier projects established as true instead of re-discovering it at full cost.

It is the **declarative sibling of [`consult.md`](consult.md)**. `consult.md`
consumes *learnings* (procedural — what past projects learned to **do**); this one
consumes *facts* (declarative — what past projects established is **true**). The
context pool is the **cross-project analog of the store for facts** — the cold tier
one level up, `context.py` fronting `~/.gotm/context/CONTEXT.md`. Like every fresh
context, this driver is born without history; this is the **read-in from that cold
tier**, seeding the new driver with facts earlier drivers already paid to learn.

This is **not** an audit and **not** a foundation unit that produces a deliverable.
It produces a short reference note — the project's working set of relevant
authoritative facts — that does **not** merge back up; see *Output* below.

## Facts are obeyed; learnings are weighted — why this is a separate step

Keep this **separate from `consult.md`** on purpose. Conflating facts and experience
is the exact error being fixed: a fact is *obeyed* (authoritative, per its trust); a
learning is *weighted* (an anecdote to consider). Run `consult.md` for the learning
pool; run this for the context pool; keep the two working sets distinct.

**Trust is 2-axis — facts sit on the authority axis, learnings on the evidence axis.**
Authority and evidence are *orthogonal*: how much a claim *constrains* is a different
question from how well it is *grounded*. Do not collapse them into one ranking.

- **Axis A — authority (what constrains).** `canonical` context and `DECISIONS.md`
  *constrain* the work. A learning, or a `personal`/`shared` fact, that contradicts
  either **raises a `QUESTION`** — it never silently wins. Facts consulted here carry
  Axis-A authority **per their `trust`**: `canonical` is **obeyed**; `personal`/`shared`
  are **strong defaults to verify** before an irreversible step.
- **Axis B — evidence (what informs).** Among *informing* knowledge — learnings, and
  `personal`/`shared` facts — weight by **`grounding`** (`observed` / `audited` beat
  `decided`), then by cross-project confirmation count. This is the axis on which a
  consulted fact and a consulted learning are compared as evidence.
- **Re-ratification exception.** A well-grounded (`observed`/`audited`), `validated`
  learning that contradicts a `DECISIONS.md` choice **forces a `QUESTION`** — neither
  silently wins, and neither is ignored: the tension goes to ratification. A
  `candidate` observed learning is only a *note*, not a challenge.

`DECISIONS.md` still governs; a consulted fact that shapes a decision is cited in that
decision's rationale.

## The pool — a real merged store (L2 context pool)

`context-analysis.md`'s produce step doesn't just write a lonely `CONTEXT.md`; it
**merges** each project's shareable facts into a shared pool. So consulting is not a
glob over scattered files — it is a **query over one merged store**: a single corpus
holding one current record per `subject` (its merge key — a fully-qualified
column / path / convention name), with provenance appended across the projects and
users that hit it, older values retained behind `superseded_by`, fronted by a
regenerated Index. The **L2** pool lives at the **user tier** — a convention location,
default `~/.gotm/context/` (resolved from `$HOME`, so cross-project by construction);
reading it is a **platform binding** (`context.py query` over the pool dir),
overridable with `--pool DIR`. It is the second rung (L1 = project-local facts, L2 = user-scoped context, L3 = enterprise — pluggable, not built here).

If the pool is empty or does not exist yet, that is a valid result: record "no
context pool consulted" and move on. "Nothing relevant found" is a valid, auditable
result, never a silent skip.

## What to do — scan the index, expand on match

The point is to spend **few tokens** — the same hot-path discipline `consult.md`
uses. Scan cheap one-line Index entries, expand the full record only for the handful
that apply; cold detail loads only when a tag or subject pulls it onto the hot path,
and no further.

1. **Name this project's filter.** From the mission + the first units: the stack
   (languages, platforms, libraries, APIs), the domain, and — where a specific
   entity is already known — its `subject`s (a table, a path, a convention). These
   are your filter.
2. **Query the pool.** Run the query over its generated Index, filtered to those tags
   (and/or a known subject), asking it to relink methods:
   `context.py query --tags <this project's stack/domain> --with-methods`
   (or `--subject <entity+attribute> --with-methods` for a point lookup). Read the
   Index line, not every full record; the query returns the matches tersely.
3. **Tag/subject-filter.** Keep the entries whose tags intersect this project's tags
   (or whose subject you asked for). The query does this; sanity-check its output.
   Drop the rest unread.
4. **Expand the matches.** For the kept entries only, read the full record
   (`subject`, `value`, `kind`, `scope`, `asof`, `volatility`, `trust`,
   `superseded_by`, `links`). Discard any whose `scope` clearly does not fit this
   project after all.
5. **Surface them where the driver and its workers will look.** Write the survivors
   to a reference note — `CONSULTED-FACTS.md` — grouped by where they apply (the
   schema / resource / convention / constraint / entity they bite). Each is a
   bounded input the driver can hand to a downstream worker; its detail stays a
   pointer away.

## Prefer current records; treat trust as a caveat, not a filter

A naive `--min-trust` floor is a trap. It can return a *superseded-but-trusted*
record (say a `shared` value that a newer observation has already replaced) while
hiding the *current-but-personal* one that is actually live. Never present a
superseded value as live. So:

- **Prefer CURRENT records.** Among records for one subject, take the current one
  (no `superseded_by`); never surface a superseded value as the live fact. If a
  superseded value is relevant history, mention it *as* history, dated by its `asof`.
- **Read `trust` as a caveat, not a hard filter.** Carry each fact's `trust` through
  to the note and weigh it there rather than filtering the current record out:
  **obey `canonical`**; treat `shared`/`personal` as a **strong default to verify**
  (a `personal` fact is one user's observation — trust it, but confirm before it
  drives an irreversible step). Reach for `--min-trust` only to *rank* what you show,
  not to drop the current record in favour of a stale-but-trusted one.
- A `query --current-only` flag is a possible future refinement that would make
  "current-preferred" the tool's default; until it exists, apply the preference here.
- Respect the freshness signals the query surfaces: a `STALE` flag (asof past the
  record's `volatility` window) means re-verify before relying on it; a
  `NEVER-EXPORT` flag means the record is private — usable in-project, never
  propagated upward.

## Relink — a fact arrives with its how-to

Because you queried `--with-methods`, each pulled fact surfaces its cross-linked
method (`links` → the learning pool). Carry that pointer into the note: the
`paid_usage`-lies fact arrives *with* the "compute from `paid_usage_metering`" query.
Store separate, present together — a fact and its method land on the driver's desk as
one usable unit.

## Output

Write `CONSULTED-FACTS.md` to the store: a short header naming the pool consulted
(its location) and this project's filter (tags and/or subjects), then the surviving
facts grouped by where they apply, each with its `subject`, `value`, `trust`, `asof`,
and any linked method. If the pool was empty or none matched, say so plainly. One
file; it is **reference context, not a frozen deliverable** — it may be refreshed
when the work moves to a new area, and it **does NOT merge back up** (it records
facts read *in* from the pool; it is distinct from `.gotm/CONTEXT.md`, the facts this
project *owns* and later merges out via `context-analysis.md`).

→ The producing half is [`prompts/context-analysis.md`](context-analysis.md); the
procedural sibling of this prompt is [`prompts/consult.md`](consult.md); the loop
they close is described in
[`docs/09-learning-across-projects.md`](../docs/09-learning-across-projects.md).
