---
prompt: worker-dispatch
purpose: build a self-contained dispatch for a bounded worker, and the rules that worker obeys
audience: the driver (you read this, then build a worker dispatch)
license: Apache 2.0
---

# Worker dispatch prompt

This is the central worker contract: how the driver builds a dispatch, and the
rules a worker obeys. It supersedes the v2 `subagent-dispatch.md`. Every unit of
work — however small — is a worker dispatch (the load-bearing rule of
`docs/02-driver-worker-store.md`): the driver plans and talks, the worker does.

A worker is born **stateless**. It has never seen the conversation, the mission,
the ledger, the other units, or any prior worker. So everything it needs must be
**in the dispatch**. The test of a well-formed dispatch is one sentence: *a fresh
worker executes it from the dispatch alone, with no access to the conversation
that created it.* If the worker would have to ask "what did we decide earlier?",
the dispatch is underspecified — the missing context belongs in it (as a bounded
input or a constraint), not in the worker's imagination.

When the dispatch *is* an audit, the worker contract still holds but the shape is
audit-specific — see [`audit.md`](audit.md). The driver's scheduling of these
dispatches (ready-set, fan-out, collect) lives in [`driver-loop.md`](driver-loop.md).

---

## The dispatch payload

A dispatch carries exactly five things. Nothing more, by design.

### 1. Discipline pointer

The first line the worker reads. One line, no project state:

    Read `<store>/PROTOCOL.md` before continuing. You will not see the broader
    project; the protocol is the rules of engagement.

### 2. Unit identity

So the result is traceable back to the ledger:

    Unit: <id>
    Title: <unit title>

### 3. Bounded inputs (only what this unit consumes)

The specific files, pointers, or values the worker reads — and nothing more:

    Inputs:
    - <path or pointer 1>
    - <path or pointer 2>

This is the highest-leverage economy lever. **Never** hand the worker the whole
ledger, sibling outputs it won't read, or the conversation — those are paid *per
dispatch*, across dozens of workers (`docs/05-scaling-and-economy.md` → worker
minimalism). A worker that turns out to need more does **not** get it pushed in
"just in case": it **reads it from the store itself** (a pointed read) or **fans
out** to sub-workers. The driver filters context *down* to this unit; it never
broadens it.

### 4. Output path (concrete backticked path(s))

    Output: `<one/path.ext>`

One named artifact per output. The declared Output is a **concrete backticked
path** — the machine ownership key the immutability hook matches on. Therefore:

- **No globs, no directories** (`pipelines/`, `{server,client}/src`, `*.py`). A
  dir/glob realpaths to a literal that matches no concrete file, so ownership
  never registers and legitimate follow-on edits get false-blocked.
- **No raw `|`** anywhere in the cell (it is the ledger's column delimiter — a
  literal pipe shifts columns and the hook reads Output at the wrong index). Use
  `/` or escape it.
- **Multi-file = comma-separated backticks** (`` `a`, `b` ``). Atomicity means
  one *deliverable*, not one *file* — a module plus its test is one unit; list
  every file it owns so the hook can freeze all of them. If the unit hides more
  than one *deliverable*, the dispatch is wrong — split the unit before
  dispatching.

### 5. Spec + constraints

What the output must be, complete enough to execute blind:

    Spec:
    - Sections / shape: <required structure>
    - Length: <target band — minimal sufficient, not padded, not starved>
    - Voice / format: <voice references, markdown/yaml/etc., canonical terms>

    Constraints:
    - <banned phrases, anonymization rules, fence/table conventions, …>

## What the worker returns — a terse structured result

**Detail-to-disk is mandatory, not a preference.** The worker writes its full
detail — the artifact, the report, the findings, the numbers — to its output
file, and **returns ≤ ~8 lines**: a pointer plus a few index facts, plus a
blocker if any. **Never the body.** The body stays on disk; the driver merges
*pointers*, not bodies. This is what makes context economy mechanical rather than
aspirational: if the driver absorbed worker bodies, every join would
re-concentrate work into the one long-lived context — monotonicity, reintroduced
at each barrier (`docs/05` → the hard rule).

    Return (≤ ~8 lines):
    - Output path written: <path>
    - Status: authored-done   (see "no self-certification" below)
    - One-line summary: <what it is>
    - Index facts: <e.g. word count, section list, headline number>
    - Blocker / gaps surfaced: <missing input / ambiguous spec, or "none">

An **over-cap return is a defect** — a worker that returns the body instead of a
pointer has broken the contract, and the driver treats it as a failed dispatch
(the detail belongs on disk; re-dispatch or trim). If the result would not fit in
a handful of lines, the worker is returning work, not an index.

## Rules the worker obeys

These three rules are what make the dispatch safe to run by the thousand.

**A worker does not write the ledger, decisions, or questions.** It produces its
one output and **reports** the result; the **driver** — the single writer of the
store — records status, the output pointer, and any surfaced gap. Workers never
touch shared governance files. This is by construction what kills the v2
duplicate-row race: many contexts read the store, exactly one writes it.

**A worker marks its unit `authored-done` only — it never self-certifies.** The
producing worker can state that the artifact exists; it can **not** confer
`verified-done`. Verification is a separate, independent audit dispatch run by a
context that did **not** author the unit (`audit.md`); for deploy / infra / data
units that audit worker performs the live `verified-done` check as the real
consumer. By the time the check runs the executor is already gone, so
self-grading is structurally impossible — which is the point.

**A worker reads only its inputs.** It does not range across the project to "get
context." If a bounded input proves insufficient, the worker reads from the store
or fans out — it never silently widens its own scope or invents missing decisions.

## Amortized batching — size the payload to a band

The rule never bends: *always dispatch; the driver never edits a work artifact,
however small.* But dispatch has overhead, so a litter of one-line fixes is **not**
N tiny workers — it is one **partition-worker** carrying the batch, its overhead
paid once across the lot. Conversely, a unit whose payload would blow past a
sensible band **fans out** into sub-workers (a tree; the driver sees only the root
result). Size every dispatch to *minimal sufficient* — neither padded nor
starved. The target is never "hit a forecasted number"; there are no project
budgets (`docs/05`), only lean payloads.

## Paste-ready dispatch template

The driver fills this in and sends it to the worker runner:

    Read `<store>/PROTOCOL.md` before continuing. You will not see the broader
    project; the protocol is the rules of engagement.

    Unit: <id>
    Title: <unit title>

    Inputs (read only these):
    - <path or pointer 1>
    - <path or pointer 2>

    Output (write exactly this — concrete backticked path(s), no globs/dirs, no raw `|`):
    - `<one/path.ext>`   (multi-file: `<a>`, `<b>`)

    Spec:
    - Sections / shape: <required structure>
    - Length: <target band>
    - Voice / format: <voice refs, format, canonical terms>

    Constraints:
    - <banned phrases / anonymization / fence + table conventions / other>

    Return (≤ ~8 lines — pointer + index facts, NOT the work product; over-cap = defect):
    - Output path written
    - Status: authored-done
    - One-line summary
    - Index facts (word count / sections / headline number)
    - Blocker / gaps surfaced, or "none"

## After the worker returns

The driver — single writer — folds the result into the store **in the same turn**:

- Record the unit `authored-done` in the ledger with its output pointer; append a
  terse recent-updates line. Output without write-back means the unit is not done.
- **Dispatch the audit/verification** as its own fresh worker before anything
  downstream consumes the output — never let the author bless its own work. Stamp
  the `Audit` cell with the verdict and, for runtime units, the `verified-done`
  result (`audit.md`).
- If the worker surfaced a gap, route it: a mission-level gap → `QUESTIONS.md`; an
  execution-level gap → refine the dispatch and re-dispatch. A worker that crashed
  is simply retried on a fresh worker — its inputs are on disk (lineage recompute).

The dispatch never short-circuits the discipline: the worker reads the protocol,
consumes its bounded inputs, produces one output, returns a terse result, and is
discarded. The driver carries the index, not the work.
