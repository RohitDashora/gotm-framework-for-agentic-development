# Independent adversarial audit — GOTM v3 build tooling

**Auditor:** independent worker (did not build any of this).
**Date:** 2026-06-29.
**Method:** read each target + the oracle (`LEDGER.md.template`, `PROTOCOL.md.template`), built v3-shape fixtures in a scratch dir, and **executed** the hook / converter / compactor against them. Every finding below is backed by actual command output.

**Targets**
- Hook: `/Users/rohit.dashora/fe-vibe/gotm/templates/hooks/gotm-immutability.py`
- Compaction: `/Users/rohit.dashora/fe-vibe/gotm/templates/scripts/compact_ledger.py`
- Converter: `/Users/rohit.dashora/fe-vibe/gotm-framework-for-agentic-development/scripts/migrate_ledger_v2_to_v3.py`

**Oracle**
- `LEDGER.md.template` — born-tiered (`## Frontier` table + `## Archive` one-line bullets); FIVE states: `pending` / `in_progress` / `authored-done` / `verified-done` / `superseded`.
- `PROTOCOL.md.template` — freeze ("a `done`/`*-done` unit's output is frozen"); a `FAIL` keeps a unit blocking; downstream consumes only on `verified-done`.

---

## Summary

`HIGH: 2 · MED: 2 · LOW: 3 · Verdict: FAIL`

The two most load-bearing guarantees are silently broken under v3: (1) the immutability hook freezes **nothing** in a real v3 ledger, and (2) the converter's "lossless" verifier is **blind** to every Archive-tier unit, so its `MISSING: NONE` is meaningless on any already-tiered ledger.

---

## HIGH-1 — The hook does NOT freeze v3 `authored-done` / `verified-done` outputs (immutability silently broken in v3)

**Root cause:** `gotm-immutability.py:93` classifies a row as frozen only on an exact-string match `if status == "done"`. v3's terminal states are `authored-done` and `verified-done` (oracle: `LEDGER.md.template` Status conventions; `PROTOCOL.md.template` "a `done`/`*-done` unit's output is frozen"). Neither equals `"done"`, and the `elif` on `:95` matches only `in_progress`/`pending`, so v3 closed units fall through to **neither** `frozen` nor `active` → no protection.

**Evidence — hook run against a v3 fixture (Frontier table with all five states; real output files on disk; realistic PreToolUse payload):**

```
TEST: U10 authored-done -> per v3 oracle MUST FREEZE
  RESULT: ALLOW (empty stdout — hook permits the edit)
TEST: U11 verified-done -> per v3 oracle MUST FREEZE
  RESULT: ALLOW (empty stdout — hook permits the edit)
TEST: U12 plain done (legacy) -> freeze
  RESULT (deny JSON):  decision= deny
TEST: U13 verified-done + U14 in_progress follow-on -> MUST ALLOW
  RESULT: ALLOW (empty stdout — hook permits the edit)
TEST: U6 archived verified-done one-liner -> ?
  RESULT: ALLOW (empty stdout — hook permits the edit)
TEST: U15 pending output (n/a) -> ALLOW
  RESULT: ALLOW (empty stdout — hook permits the edit)
```

**Direct introspection of `parse_outputs()` on the same v3 ledger:**

```
FROZEN (status=='done' exactly):
    U12 -> plaindone.md            <-- ONLY the legacy plain-'done' row is frozen
ACTIVE (in_progress/pending):
    never.md
    shared.md
```

Only the one legacy `done` row is frozen. The `authored-done` (U10) and `verified-done` (U11) outputs — exactly the states a v3 project produces — are editable.

**Live proof on the real framework ledger** (`/Users/rohit.dashora/fe-vibe/gotm-framework-for-agentic-development/.gotm/LEDGER.md`):

```
FROZEN units in production ledger: 0
ACTIVE units: 0
```

The shipping v3 ledger has its 72 closed units as `## Archive` bullets (`- U72 — …`) which the hook's `UNIT_ROW` regex (`^\|\s*U\d+`) never matches, and the few in-text states are not `done`. Net: **the immutability hook would freeze nothing on the very repo that teaches the discipline.**

**Sub-checks requested (both confirmed correct *in isolation*, but moot given the above):**
- (a) Follow-on ownership: `shared.md` (U13 verified-done + U14 in_progress) → ALLOW. Correct intent, but only because U13's verified-done isn't frozen in the first place — the path lands in `active`, not via the frozen∩active follow-on path. So the follow-on logic is currently untested by real freezes.
- (b) Archived (`## Archive`) unit's output (`archived.md`) → ALLOW (not frozen). Archive bullets are invisible to the parser, so an aged-out done unit's output is never frozen — a second gap on the same root cause.

---

## HIGH-2 — Converter's losslessness verifier is BLIND to Archive-tier units (`MISSING: NONE` is false on any already-tiered ledger)

**Root cause:** `migrate_ledger_v2_to_v3.py` defines `is_unit_row` via `UID_RE = ^\|\s*(U\d+)\s*\|` (`:52, :67`). The losslessness check (`:308-313`) counts only those `| U |` **table** rows. v3 `## Archive` entries are **one-line bullets** (`- U2 — … `), which `is_unit_row` does not match. So they are excluded from `orig_ids`, `new_ids`, and the `missing` computation — the verifier cannot detect their loss.

**Evidence — a v2 ledger migrated once, then re-run on its own v3 output:**

```
=== Re-run converter on already-v3 output (idempotence) ===
orig units : 5 unique (5 rows)   present after : 5
MISSING    : NONE
```

The source had **7** units (U1–U7); after one migration U1/U2 became Archive bullets. The second run reports `orig units: 5` — it silently does not count U1/U2 at all:

```
Units in | U | TABLE rows (what verifier counts): ['U3', 'U4', 'U5', 'U6', 'U7']
Units in Archive BULLET lines (INVISIBLE to verifier): ['U2', 'U1']
=> Verifier sees 5; real total = 7
=> If a converter pass dropped U1/U2 from Archive, it would STILL print 'MISSING: NONE'.
```

**On the real production ledger:**

```
production LEDGER.md: TABLE units=0 ; ARCHIVE-bullet units=72 (invisible to converter & hook)
```

Running the converter on the actual v3 framework ledger would verify **zero** of its 72 units and report `MISSING: NONE` even if it mangled all of them. The script's headline safety claim ("verifies EVERY unit ID is still present") does not hold for tiered ledgers — i.e., for v3 ledgers, which is its target shape.

---

## MED-1 — `compact_ledger.py` does not recognize `verified-done` / `authored-done` as closed states (born-tiering broken; same `done`-only blindspot as the hook)

**Root cause:** `closed_and_compactable()` (`:49-60`) tests `re.search(r"\|\s*done\s*\|...|\|\s*superseded\s*\|", line)` plus an audit-marker fallback. The pattern `\|\s*done\s*\|` requires `done` bounded by pipes, so `| verified-done |` / `| authored-done |` do not match by status.

**Evidence:**

```
closed_and_compactable() at keep_from=99:
   verified-done, NO audit marker      -> False
   verified-done, WITH PASS marker     -> True
   authored-done, NO marker            -> False
   plain done                          -> True
   superseded                          -> True
```

A `verified-done` unit (the v3 consumable terminal state) is compacted only incidentally — when it happens to carry a `PASS→…/audits/` marker that trips the fallback regex on `:58`. A `verified-done` with `Audit: —` or a non-PASS marker is treated as still-open and never ages out of the frontier, defeating the born-tiered compaction the script exists to perform.

---

## MED-2 — Converter maps `done` + `FAIL` audit → `authored-done`, dropping the blocking signal from the state

**Root cause:** `v3_state()` (`:121-128`): `done` → `verified-done` iff `has_passing_audit`, else `authored-done`. A `done` row whose audit is `FAIL` therefore becomes `authored-done`.

**Evidence:**

```
v3_state(done+FAIL) = authored-done   (oracle: FAIL must keep it BLOCKING, not look authored-done)
audit_pointer: FAIL→.gotm/audits/U7.md
```

Per `PROTOCOL.md.template` ("a unit reaches `verified-done` only on PASS/PASS-FINDINGS; FAIL keeps it blocking"), a failed unit should not be normalized into the neutral `authored-done` (awaiting-an-auditor) state — that visually clears the failure. The `FAIL→audits/…` pointer is preserved (so it is traceable, not data loss), which is why this is MED not HIGH, but the **state token itself misrepresents a blocked unit as merely unaudited.**

---

## LOW-1 — `compact_ledger.py` prints a misleading `kept-full` count (double-counts Archive table rows)

`compact()` reports `kept-full=len(new_ids)` (`:189, :197`), where `new_ids` counts every `| U |` row in the new ledger — including the rows of the Archive **table** the script itself emits (`:122-125`). On the v3 fixture (3 frontier + 3 archived):

```
orig units=6  kept-full=6  archived=3  union=6
```

`kept-full=6` is wrong (only 3 stayed full); the true split is 3 full + 3 archived. The losslessness `union` is still correct (the double-counted IDs collapse in the set), so this is a reporting defect, not a data defect — but it makes the verification output untrustworthy at a glance.

## LOW-2 — Two tools emit two different `## Archive` shapes (no cross-tool agreement on the cold tier)

- Converter + `LEDGER.md.template`: one-line **bullets** — `- U<n> — title · \`out\` · state · verdict→audits/U<n>.md`.
- `compact_ledger.py`: a 5-column **table** — `| Unit | Title | Status | Audit | Output |` (`:122-125, :102`), and it hardcodes the archived status to `done`/`superseded` (`:73`), downgrading `verified-done`→`done`.

A project that migrates with one tool and later compacts with the other ends up with a mixed/contradictory Archive, and the downgraded status compounds HIGH-1/MED-1 (the hook & compactor already can't read either shape's v3 states).

## LOW-3 — Converter drops extensionless / directory outputs from the one-liner

`_find_output()` (`:140-148`) only matches backticked paths ending in a known code/doc extension. A unit whose Output is a directory or extensionless path is lost from the Archive one-liner:

```
parse_row output for `app/dashboard/`: None
one_liner: - U9 — Build the app dir · `see LEDGER-ARCHIVE.md` · verified-done · PASS→…/U9.md
```

The full cell survives in `LEDGER-ARCHIVE.md` (so recoverable), but the hot-tier pointer to the real output is replaced with a placeholder.

---

## Verdict

**FAIL.** Two HIGH findings each defeat a core v3 guarantee end-to-end, proven by execution against both synthetic fixtures and the real shipping ledger:

1. The immutability hook freezes **zero** v3 outputs — it matches only the legacy exact string `"done"`, never `authored-done`/`verified-done`, and never the `## Archive` bullets where real v3 closed units live.
2. The converter's losslessness verifier is **blind to every Archive-tier unit**, so `MISSING: NONE` is vacuously true on exactly the tiered ledgers it targets (0 of 72 production units verified).

Compaction (MED-1) shares the hook's `done`-only blindspot, and the converter's `FAIL→authored-done` mapping (MED-2) launders a blocking verdict. Until the three tools agree on the five v3 states **and** on the `## Archive` bullet shape, the v3 runtime does not enforce the discipline it documents.
