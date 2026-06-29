# Fix report — GOTM v3 runtime tooling cluster (the two HIGH bugs)

**Worker:** runtime-tooling fix worker (owns the whole cluster so tools + ledger format stay mutually consistent).
**Date:** 2026-06-29.
**Source findings:** [`v3-build-tooling.md`](v3-build-tooling.md) (HIGH-1, HIGH-2, MED-1, MED-2, LOW-1, LOW-2).
**Method:** every fix proven by execution against synthetic v3 fixtures **and** the real shipping ledger. Command output pasted below is the gate.

**Root cause (all findings):** v3 renamed the terminal states (`done` → `authored-done` / `verified-done`) and the ledger gained a `## Archive` section of one-line bullets, but the tools still keyed on the literal `done` and on `| U |` table rows only.

**Standardized archive format (one canonical shape — hook + compaction + converter + templates all agree):**

```
- U<n> — <title> · `<output>` · <status> · <verdict>→audits/U<n>.md
```

A one-line **bullet** per unit. Fields are separated by ` · `; Output is the backticked path; Status is the 3rd ` · ` field. (The compaction script previously emitted a 5-column *table* — LOW-2 — now also emits this bullet form.)

---

## Fix 1 — Hook (`plugin/templates/hooks/gotm-immutability.py`) — closes HIGH-1

**Before:** `if status == "done"` (exact) over `| U |` table rows only. Froze nothing in v3.
**After:**
- Freezes a unit whose status ∈ {`verified-done`, `authored-done`, legacy `done`} (substring-tolerant, so `verified-done (live)` still classifies).
- Does NOT freeze `pending` / `in_progress` (active follow-on → editable) or `superseded` (output replaced).
- Reads frozen units from **both** the `## Frontier` table (header-aware) **and** the `## Archive` bullets (` · `-delimited), plus a `LEDGER-ARCHIVE.md` sibling if present.
- Kept the follow-on-ownership allow, fail-open, deny-via-stdout.

### PROOF — FIXED hook vs the REAL `framework/.gotm/LEDGER.md`

```
=== FIXED hook vs REAL framework LEDGER.md ===
FROZEN count: 20
ACTIVE count: 0
frozen units (sample):
  U45 -> README.md
  U60 -> docs/06-learning-across-projects.md
  U59 -> .gotm/audits/U59.md
  ...
  U1 -> docs/01-what-is-gotm.md

=== OLD hook (done-exact, table-only) vs REAL ledger ===
FROZEN count: 0
ACTIVE count: 0
```

**Hook FROZEN-count on the real ledger: 0 (before) → 20 (after).** (72 archive bullets collapse to 20 distinct output paths; superseded U2/U3/U12/U13 correctly excluded.)

### PROOF — synthetic v3 Frontier + Archive

```
=== Synthetic v3 Frontier + Archive acceptance ===
U10 authored-done out/authored.md                       -> DENY  (expect DENY)  PASS
U11 verified-done out/verified.md                        -> DENY  (expect DENY)  PASS
U12 superseded out/superseded.md                         -> ALLOW (expect ALLOW)  PASS
U13 pending out/pending.md                               -> ALLOW (expect ALLOW)  PASS
U14 verified-done w/ in_progress U20 owner               -> ALLOW (expect ALLOW)  PASS
U6 ARCHIVE verified-done out/archived.md                 -> DENY  (expect DENY)  PASS
U5 ARCHIVE legacy done out/legacy.md                     -> DENY  (expect DENY)  PASS

=== LEDGER-ARCHIVE.md sibling freeze ===
out/sib.md (sibling archive) -> DENY  PASS
```

Both an `authored-done` and a `verified-done` frontier output DENY; a path also owned by an `in_progress` follow-on ALLOWs (the frozen∩active follow-on path now actually exercises — the audit noted it was previously untested because nothing was frozen); `superseded`/`pending` ALLOW; archive bullets (frontier-absent) freeze; a `LEDGER-ARCHIVE.md`-only unit freezes.

---

## Fix 2 — Compaction (`plugin/templates/scripts/compact_ledger.py`) — closes MED-1, LOW-1, LOW-2

**Before:** `closed_and_compactable()` matched `| done |` / `| superseded |` only (`verified-done` compacted only incidentally via a PASS marker). Losslessness counted `| U |` rows only. Emitted a *table* Archive and downgraded `verified-done`→`done`. `kept-full` double-counted archive rows (LOW-1).
**After:**
- Compacts `verified-done` and `superseded` past the window; compacts `authored-done` ONLY if it already carries a passing audit; NEVER compacts `pending` / `in_progress` / unaudited `authored-done`.
- Emits the canonical **bullet** Archive (LOW-2), preserving the v3 status token verbatim (no `verified-done`→`done` downgrade).
- Merges a pre-existing `## Archive` into ONE section (no duplicate heading), newest-first, de-duped.
- Losslessness counts ALL unit IDs (table rows + archive bullets); `kept-full` reports table rows only, archive count separately (LOW-1).

### PROOF — v3-state recognition + lossless compaction with a pre-existing archive

```
=== closed_and_compactable() v3-state recognition (keep_from=108) ===
  U101 verified-done (PASS)        -> compactable=True
  U102 authored-done unaudited     -> compactable=False
  U103 authored-done + PASS        -> compactable=True
  U104 superseded                  -> compactable=True
  U106 pending                     -> compactable=False
  U107 in_progress                 -> compactable=False

=== full compaction run (keep_from=108) ===
orig units=9  kept-full=4  archived(bullets)=5  spilled-cells=3  union=9
MISSING: NONE
Active-unit block present: True
```

Resulting single merged `## Archive` (newest-first, v3 tokens kept, pre-existing U49/U50 carried forward):

```
- U104 — old superseded · `s.md` · superseded · superseded
- U103 — old authored PASSED · `ap.md` · authored-done · PASS→.gotm/audits/U103.md
- U101 — old verified · `v.md` · verified-done · PASS→.gotm/audits/U101.md
- U50 — pre-existing archive unit · `arch50.md` · verified-done · PASS→.gotm/audits/U50.md
- U49 — pre-existing archive unit · `arch49.md` · done · —
```

`MISSING: NONE` now covers the 2 pre-existing archive units (orig units=9, union=9).

---

## Fix 3 — Converter (`framework/scripts/migrate_ledger_v2_to_v3.py`) — closes HIGH-2, MED-2

**Before:** losslessness verifier counted `| U |` table rows only — blind to `## Archive` bullets (`MISSING: NONE` vacuous on any tiered ledger; 0 of 72 real units verified). `done+FAIL` → `authored-done`, silently archivable.
**After:**
- `any_uid_of()` counts unit IDs in BOTH shapes (table + archive bullets); verifier headline counts both.
- State map: `done+PASS`→`verified-done`; `done+pending/no-verdict`→`authored-done`; `done+FAIL`→`authored-done` **with the `FAIL→audits/U<id>.md` pointer preserved AND kept FULL in the Frontier (flagged, not silently archived)**; `superseded`→`superseded`.

### PROOF — state mapping + losslessness counts archive units

```
  U1: v2=done         -> v3=verified-done  audit=PASS→.gotm/audits/U1.md
  U5: v2=done         -> v3=authored-done  audit=FAIL→.gotm/audits/U5.md   (FAIL kept, blocking)
  U7: v2=superseded   -> v3=superseded     audit=superseded

############ RE-RUN converter on its OWN v3 output (idempotence) ############
keep-from (CLOSED) : U7  (kept 3 full, archived 4 bullets)
orig units         : 7 unique (7 ids: table+archive)   present after : 7
MISSING            : NONE
```

The idempotence re-run now reports **7 unique units** (audit's HIGH-2 evidence showed `5`) — the 4 archive bullets (U1–U4) are counted. U5 (`done+FAIL`) stays FULL in the Frontier as `authored-done` with its `FAIL` pointer, never aged into the cold Archive.

### PROOF — `MISSING: NONE` now actually means it (regression guard)

```
orig unit IDs (table+archive): ['U1','U2','U3','U4','U5','U6','U7']
new  unit IDs (U1 bullet dropped): ['U2','U3','U4','U5','U6','U7']
MISSING: U1  <-- correctly DETECTS the loss
```

---

## Fix 4 — Standardized archive format (templates + meta-example)

- `plugin/templates/LEDGER.md.template` + `framework/templates/LEDGER.md.template`: the `## Archive` example was already the bullet form; added a Conventions note "ARCHIVE ENTRIES ARE ALSO MACHINE-PARSED, AND IN ONE CANONICAL SHAPE" spelling out the exact bullet (` · `-delimited, parseable status + backticked output) so the hook can freeze aged-out closed units, and that `verified-done`/`authored-done`/legacy `done` bullets freeze while `superseded` does not.
- `framework/.gotm/LEDGER.md`: already in the bullet form — no format change needed; the compactor + converter now both emit/parse exactly this shape.

### PROOF — cross-tool agreement on the SAME bullets

The hook freezes the compactor-emitted bullets, and the converter parses them:

```
hook FROZEN:  {au.md:U102, rv.md:U108, ap.md:U103, v.md:U101, arch50.md:U50, arch49.md:U49}
hook ACTIVE:  {ip.md, p.md}
converter any_uid_of sees: [U49, U50, U101, U102, U103, U104, U106, U107, U108]
```

(Superseded U104 correctly NOT frozen; active U106/U107 in ACTIVE.)

---

## Fix 5 — `framework/.gotm/LEDGER.md` stale count

`8 Mermaid diagrams` → `9` at both sites (lines ~19 and ~33: `9 docs + 9 diagrams` / `9 ch + 9 diagrams`).

---

## Parse check

```
=== py_compile all three ===
hook: OK
compact_ledger: OK
migrate: OK
```

## Verdict

All HIGH (1, 2) + MED (1, 2) + LOW (1, 2) findings fixed and proven by execution. **Hook FROZEN-count on the real ledger: 0 → 20.** The three tools now agree on the five v3 states and on the one canonical `## Archive` bullet shape; the v3 runtime enforces the discipline it documents.
