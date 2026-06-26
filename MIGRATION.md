# Migrating a v2 GOTM project to v3

You already ran a GOTM v2 project — a single long-lived agent that planned, executed,
audited, and re-read a flat ledger every turn. v3 is the same discipline re-architected
so that **nothing on the hot path is long-lived**. This guide is how you carry an
existing v2 project across, mechanically and conceptually.

> **The decision is settled (V3-DESIGN.md §9, ch8).** v3 is for new projects **and**
> existing v2 projects migrate — they are not left on v2. In-flight v2 ledgers convert
> with `scripts/migrate_ledger_v2_to_v3.py` (below); the rest is adopting the new
> protocol and prompts and changing how you *run* the loop.

---

## 1. The mindset shift: one doer → driver / worker / store

v2's defining flaw was that the planner and the doer were the **same context**. One
agent accumulated every input, every build log, every self-validation until it both
graded its own work and stalled under its own weight. v3 splits that one role into
three (V3-DESIGN.md §3, docs/02):

| Role | What it does | What it must never do |
|---|---|---|
| **Driver** (the conversation agent) | Plans (owns the ledger DAG), talks to the human (ratification ladder), runs the scheduler loop, and is the **single writer** of the store. | Never edits a work artifact, never reads bulk input, never self-certifies. |
| **Worker** (a dispatched subagent) | Takes **bounded inputs + a spec**, produces **exactly one output**, returns a **terse structured result** (status + output pointer + index facts). | Never carries cross-unit state; is discarded after its one unit. |
| **Store** (`.gotm/` + the repo) | The durable system of record — born tiered (hot frontier + cold archive). | — |

**The load-bearing rule: the driver plans and talks; all work — however small — is a
worker dispatch.** If you find the driver editing a file or reading a 500-line input,
you have relapsed into v2. The driver dispatches a read-and-summarize worker instead.
Workers are **stateless**: each one is born fresh, sees only its dispatch payload, and
is gone before the next unit starts. That is not a rule to remember — it is the default
shape, and it is what makes the system non-monotonic.

The honest limit (V3-DESIGN.md §4, ch8): in interactive Claude Code the **driver is the
session** — it cannot be made stateless and cannot self-trigger `/compact`. It still
grows, but *slowly*, because it carries only plan + discipline + a terse frontier. Its
safety net is **re-hydration from the store**, not statelessness (see §2.5).

---

## 2. The mechanical changes

### 2.1 Adopt the v3 protocol + the 6 prompts

Replace your v2 `PROTOCOL.md` with the v3 `templates/PROTOCOL.md.template` (rewritten
around driver / worker / store + the scheduler loop). Adopt the six v3 prompts:

- `driver-loop.md` — **new**: the scheduler the driver runs by hand.
- `worker-dispatch.md` — the central worker contract (**supersedes** v2's
  `subagent-dispatch.md` — delete that one).
- `audit.md` — fresh-worker audit + the runtime `verified-done` check.
- `session-start.md` — driver boot: re-hydrate + reconcile (no compaction hook).
- `consult.md`, `outcome-analysis.md` — the cross-project learning loop (kept, recast).

Keep your `CLAUDE.md` root bridge; point it at the v3 `PROTOCOL.md`.

### 2.2 Convert the flat ledger to the born-tiered shape

This is the one step a script does for you. Your v2 ledger is a flat `## Units` table
(plus, perhaps, a `## Recent updates` log). The v3 ledger is **born tiered**
(templates/LEDGER.md.template, docs/03):

- **`## Frontier`** — the hot tier, re-read every turn. Holds every open unit
  (`pending` / `in_progress`), the last ~N closed units (recent-completion window), and
  any older closed unit a still-open unit still cites as an input.
- **`## Archive`** — the cold tier, never on the hot path. Closed units that have aged
  out compact to **one line each**, newest-first, **keeping the audit pointer** so the
  gate stays checkable.
- **`## Recent updates`** — one recovery log, newest-first, a rolling window of the last
  ~N entries; older ones roll into the archive.

Run the converter:

```
python3 scripts/migrate_ledger_v2_to_v3.py --ledger path/to/.gotm/LEDGER.md
```

It backs up the original, tiers the table, rolls the recovery log, and verifies no unit
ID was lost. See §3 for the lossless guarantee.

### 2.3 Adopt the 5 v3 states

v2 had `pending / in_progress / done / superseded`. v3 splits the terminal "done" into
two states to make audit independence **structural** (V3-DESIGN.md §5, docs/06):

| v3 state | Meaning |
|---|---|
| `pending` | Born, not yet dispatched (a ready-set leaf once inputs clear). |
| `in_progress` | A worker is executing it (or it is mid-recovery). |
| `authored-done` | A worker produced the output; the artifact **exists** but has **not** been independently checked. **Not consumable downstream.** |
| `verified-done` | An **independent** audit/verification worker (auditor ≠ author) passed it. For deploy/infra/data units that worker also exercised the live artifact. **The only consumable terminal state.** |
| `superseded` | Scope changed; replaced by a follow-on. |

The converter maps your v2 rows conservatively (see §3): a v2 `done` row whose audit
passed becomes `verified-done`; a `done` row with no passing audit becomes
`authored-done` (it still needs an independent check under v3). **From the conversion
forward, a producing worker may only mark `authored-done` — the driver always launches a
separate audit worker to confer `verified-done`.** Never let the worker that wrote an
output be the one that blesses it.

### 2.4 The freeze + follow-on ownership

The immutability freeze survives, with the v2 over-blocking fixed (V3-DESIGN.md §5,
docs/06). Closed units' outputs stay frozen — **to revise a done output, append a
follow-on unit and put the change there**, never edit in place. The v3 hook honors
**follow-on ownership**: an active unit may own a change to a previously-done output.
And because **only the driver writes the store** (workers report results), the v2
dup-row write-back race is gone by construction.

### 2.5 Re-hydration via session-start reconcile (no compaction hook)

v3 has **no compaction hook dependency**. On *any* fresh start — cold restart, `/clear`,
or after an auto/manual compaction — the driver rebuilds its working set from the store
via the **session-start reconcile** (`session-start.md`): read the frontier, reconcile
it against disk (a crash can orphan an output or strand a unit `in_progress`), rebuild
the manifest (active-unit row + its input pointers + the recovery-log window + open
`QUESTIONS`), then act. This is the same transcript-independence guarantee GOTM always
made. An optional `SessionStart(compact)` hook could auto-inject that manifest, but it
is at most an accelerator — **do not build on it.** (In SDK/headless mode the driver may
*additionally* self-compact; that is a bonus, not the foundation.)

---

## 3. What the converter guarantees (lossless)

`scripts/migrate_ledger_v2_to_v3.py` is general and parameterized — give it any v2
`LEDGER.md` path; it has no hardcoded repo paths or unit IDs. It:

1. **Backs up the original** to `LEDGER.md.bak` before writing anything.
2. **Tiers losslessly** — closed (`done` / `verified-done` / `superseded`) units older
   than a rolling window (default: keep the most-recent N by ID) compact to one-line
   `## Archive` entries that **keep the audit pointer**; the full original cells overflow
   to `LEDGER-ARCHIVE.md` (nothing is dropped — the detail also lives in the output
   files, `audits/`, and `DECISIONS.md`).
3. **Rolls `## Recent updates`** to the last N entries; older ones move to the archive.
4. **Verifies every unit ID** is still present afterward and prints `MISSING: NONE` (or
   lists any lost IDs), plus before/after byte sizes.

Always read the converter's verification line. `MISSING: NONE` is the migration's
acceptance gate.

---

## 4. Post-migration checklist

- [ ] v3 `PROTOCOL.md` + the 6 prompts in place; `subagent-dispatch.md` removed.
- [ ] Ledger converted; `MISSING: NONE` confirmed; `## Frontier` / `## Archive` /
      `## Recent updates` present.
- [ ] v2 `done` rows re-classified — anything not independently audited is
      `authored-done` and queued for an audit worker before it is consumed downstream.
- [ ] The driver/worker split declared on turn one: driver plans + talks + single-writes;
      all work is a worker dispatch.
- [ ] Re-hydration tested: start a fresh session and confirm the driver rebuilds from the
      store alone (no chat memory) via session-start reconcile.
