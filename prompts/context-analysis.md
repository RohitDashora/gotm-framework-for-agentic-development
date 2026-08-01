---
prompt: context-analysis
purpose: pin, decompose, and merge a project's facts into the cross-project context pool — the declarative write-out to the shared cold tier
audience: the driver (you read this, then produce/confirm the project's CONTEXT.md and merge it)
license: Apache 2.0
---

# Context-analysis prompt

This is the **produce-facts** prompt — the declarative sibling of
[`outcome-analysis.md`](outcome-analysis.md). Where that prompt distills a finished
project into transferable **learnings** (procedural — *what I've learned to do*),
this one governs a project's **facts** (declarative — *what I know is true*): how they
are pinned as they are discovered, decomposed from compound observations, and merged
into the shared context pool (framework `docs/09-learning-across-projects.md`). The
project-local output is `.gotm/CONTEXT.md`, scaffolded by
`templates/CONTEXT.md.template`; the shared output is the merged pool.

Think of the context pool as the **cross-project analog of the store, for facts** —
one level up. Inside a project the store reconstructs a worker's context; across
projects the context pool plays the same role for the **next project's driver**,
seeding it with facts it would otherwise re-verify from scratch. This prompt is the
**write-out to that cold tier**: point-in-time facts that never sit on any driver's
hot path, pulled only when a future project's `subject`/`tags` match (the consume
half, [`consult-facts.md`](consult-facts.md)).

Facts and learnings have **different trust semantics** — facts are *obeyed*,
learnings *inform* — so they get separate prompts on purpose. Do not conflate them;
that conflation is the exact error this split fixes.

## Two produce moments — the key difference from outcome-analysis

`outcome-analysis` runs **once, at the end**. A learning is useful only to the *next*
project. A fact is useful to **this** project's own downstream units too, so produce
has **two moments**:

1. **Pin-on-discovery (mid-project).** The moment a worker discovers a fact, it
   surfaces it; the driver pins it to `.gotm/CONTEXT.md` right away — making the fact
   a slice-able input for the workers that come after.
2. **Confirm-and-merge (project end).** A single pass reviews the pinned facts, sets
   the privacy and decay flags, decomposes anything still bundled, and merges the
   shareable facts up into the pool.

### Moment 1 — pin-on-discovery (the new mechanic)

When a worker, doing its unit, discovers a fact — *"this column lies", "this API
needs that header", "the prod warehouse is X"* — it **surfaces it in its ≤8-line
terse return**, never hoarding it. The convention adds one line to the worker return:

    FACT: <subject> — <assertion>      (0..n)

The architecture is unchanged: the **worker terse-returns, the driver writes.** As
the single writer, the driver decides **pin vs discard** — exactly as it decides
record vs discard for any result — and pins kept facts to `.gotm/CONTEXT.md` (the
project-local declarative store). This closes a real gap: today a mid-project
discovery lives only as `DECISIONS.md` prose or in chat. Formalizing it as a
`CONTEXT.md` fact makes it a **first-class, slice-able input** the driver can hand to
downstream workers as bounded context, instead of re-deriving it.

Pin a fact with the fields you have; leave `volatility`/`shareable`/`links` to be
firmed up at confirm-and-merge. A mid-project pin is provisional; it does not merge
up until the end.

### Moment 2 — confirm-and-merge (mirrors the learning merge)

Covered under **Confirm-and-merge** below.

## Decompose-on-produce — handling compound observations

A single observation often carries **both** a fact and a method — a `subject` that is
true, plus a way to act on it. Split it at produce time; do not bundle:

- the **fact** → `.gotm/CONTEXT.md` (declarative, `subject`-keyed),
- the **method** → `LEARNINGS.md` (procedural, `claim`-keyed — handed to
  [`outcome-analysis.md`](outcome-analysis.md) in the same end-of-project pass),
- **cross-linked**: the fact's `links` names the learning id, so consume can present
  them together (relink-on-consume).

**Worked example** — the `paid_usage` observation decomposes into:

- **fact** (→ `CONTEXT.md`):
  `subject: main.fin_live_gold.consolidated_active_contracts.paid_usage` —
  *"a NetSuite/financial field, not actual consumption; can read wildly high vs real
  spend"*, `kind: schema`, `value: "unreliable for consumption; the real source is
  paid_usage_metering"`.
- **method** (→ `LEARNINGS.md`): *"compute real consumption from the
  `paid_usage_metering` table with `SUM(usage_dollars)`"*.
- **link**: `fact.links: [<project>/L4]`.

Splitting is strictly better than a bundle: the fact ("this column lies") stays true
even after a better query **supersedes** the method. **Two artifacts, two decay
clocks** — a fact rots by *change*, a method by *contradiction*.

## The record — source of truth

Emit each fact as a structured record per `templates/CONTEXT.md.template`, matching
the schema `context.py` reads:

    - id: <project>/F<n>
      subject: "<entity+attribute>"        # THE MERGE KEY — fully-qualified col/path/convention
      fact: "<the assertion>"
      kind: <schema|resource|convention|constraint|entity|best-practice>
      value: "<the value / what it means / what to do about it>"
      tags: [<tech>, <domain>, <phase>]
      scope: <where this holds>
      asof: <YYYY-MM-DD>                    # facts are point-in-time
      volatility: <stable|slow|volatile>    # re-verify cadence
      provenance:                           # APPENDABLE across projects/users
        - {project: <this project>, user: <id>, ref: <D##/audit/note>, note: "<observed>"}
      trust: personal                       # personal | shared | canonical
      shareable: <yes|no>                   # privacy gate for the enterprise flow
      links: [<learning-id>, ...]           # cross-links into the learning pool (methods)
      superseded_by: <id>                   # set only when a newer value replaces this one

The merge key is `subject` (entity+attribute), **not** the whole assertion — so a
changed value *supersedes* the old rather than duplicating. **Six `kind`s** — `schema` ·
`resource` · `convention` · `constraint` · `entity` · `best-practice` (the last an
*endorsed/curated normative standard* — a fact about the recommended way — distinct from a
candidate `pattern` learning; it `links` to the method-learning that grounds it). `context.py` regenerates the Index at the top of the pool's
`CONTEXT.md`; you author records, the tool builds the index.

## Confirm-and-merge — the end-of-project write-back (L1 → L2)

At project end, run one pass that reads `.gotm/CONTEXT.md` + `DECISIONS.md` and:

1. **Decompose** any still-bundled observations into a fact + a method, cross-linked
   (per *Decompose-on-produce* above; the method goes to `outcome-analysis` in the
   same pass).
2. **Set `shareable` — the privacy gate. Default `yes`.** The **L2** pool (cross-project) holds **L1** (project-local) facts promoted at project end. At the L2 level (user's own pool), facts are shareable within their own pool by default — the flag is the **L2→L3 gate** (enterprise layer, pluggable, not built here), not an L1→L2 skip. So **assume `shareable: yes`** and set `shareable: no` **only** for genuinely private detail. A `shareable: no` fact **still merges** into the L2 pool but is flagged `NEVER-EXPORT`.
3. **Set `volatility`** — `stable` (a schema fact), `slow`, or `volatile` (a fact
   with an expiry, e.g. a transition date) — which sets the pool's re-verify cadence
   and staleness banner.
4. **Merge the L1 facts up to L2:**

       context.py merge .gotm/CONTEXT.md --project <name> --user <id>

   The tool backs up the pool first and verifies no `subject` is dropped
   (`MISSING: NONE`). Then **report** what the merge did: new subjects, superseded,
   promoted, and never-export count.

This mirrors `outcome-analysis`'s merge step; the difference is entirely in the
*merge semantics* below.

## Merge semantics — supersede, don't overwrite

`context.py merge` matches incoming records against **current** pool records on
`subject`, with **different rules than the learning merge** (which contests on
contradiction):

1. **Same subject, SAME value → append provenance.** Dedupe by `(project, user, ref)`;
   never duplicate the record. This is how a fact accumulates cross-project/cross-user
   evidence.
2. **Same subject, DIFFERENT value → SUPERSEDE (the freeze, applied to facts).** The
   old record is **retained** with its `value` and `asof`, its `superseded_by` set to
   the new record's id; the new value becomes current. **Nothing is overwritten** — a
   changed fact archives the old, it does not erase it. This is the declarative analog
   of the freeze: a superseded fact is frozen, not deleted, so history survives.
3. **Subject absent → add as `trust: personal`.** Everything a project deposits is
   born `personal`.

**Promotion (facts differ from learnings here).** Learnings promote by *independent
confirmation* (≥2 distinct projects). Facts promote by **commonality**: `personal →
shared` when provenance holds **≥2 distinct users** who pinned the same subject.
`shared → canonical` is **curation only** — an authority's endorsement, **never set by
merge**. A superseding record is born `personal` (unconfirmed), even if it replaces a
`shared` one. This is why the flow to enterprise is partly a **filter, not just a
promotion**: only `shareable: yes` facts are ever eligible to rise, and only
commonality (not one loud project) lifts them.

At **L2 (single user)** all facts stay `personal` — cross-user commonality and
`canonical` require the pluggable **L3** layer, not built here.

## Honesty — an empty pool is a valid pool

On a **first project**, or a pool no other user has touched, `context.py merge` may
promote nothing and the pool may hold only `personal` facts. That is correct, not a
failure — the honest state of one user's context is a pile of `personal` facts, and
only `shareable: yes` facts ever rise. Do not manufacture commonality, do not
hand-set `shared`/`canonical` (merge never mints them; curation does), and do not mark
a private fact `shareable: yes` to make the pool look richer. The privacy gate and the
commonality gate are what keep a consulted fact's `trust` meaningful rather than
self-asserted.

## Output

1. `.gotm/CONTEXT.md` — the project's own facts, pinned across the run and confirmed
   at the end, from `templates/CONTEXT.md.template`. This is the project's declarative
   contribution; it **merges up** at project end.
   - By contrast, `.gotm/CONSULTED-FACTS.md` holds facts read **in** from the pool
     (reference, produced by [`consult-facts.md`](consult-facts.md)); it does **not**
     merge up.
2. The **merged pool** at the default location (`~/.gotm/context/`), after
   `context.py merge` — the write-back that closes the loop.

A produce step with no consumer is a write-only void; a merge that never happens is
that void. The loop closes only once shareable facts reach the pool and a later
driver consults what this one deposited.

→ The consuming half is [`prompts/consult-facts.md`](consult-facts.md); the tool is
`context.py` (`init` · `merge` · `query` · `status`); the loop they close is described
in [`docs/09-learning-across-projects.md`](../docs/09-learning-across-projects.md). The
procedural sibling is [`outcome-analysis.md`](outcome-analysis.md).
