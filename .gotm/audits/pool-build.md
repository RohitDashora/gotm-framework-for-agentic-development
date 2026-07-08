# W-pool build proof — `scripts/pool.py`

**Unit:** W-pool (LEARNING-POOL-DESIGN.md §9). **Artifact:** `/Users/rohit.dashora/fe-vibe/gotm/scripts/pool.py`
(plugin top-level `scripts/`, cross-project — NOT `templates/`). **Status:** authored-done, execution-proven.

Deterministic, stdlib-only Python 3. Records parsed from / written to `POOL.md` in the §3
YAML-ish list form (round-trip stable; file sorted by id, Index regenerated each write).
Every mutating op backs up `POOL.md` to `.backups/POOL-<ts>.md` first (sub-second ts so
rapid merges never collide) and verifies no `claim` dropped (`MISSING: NONE`).

Tested with a temp pool (`--pool /private/tmp/gotm-pool-test`), NOT the real `~/.gotm`.

## Fixtures (synthetic project LEARNINGS)
- `project-A.md` — L1 (claim: x-goog-user-project header; fix: SET it), L2 (Lakeview :param).
- `project-B.md` — L1 with the SAME claim as A/L1, SAME fix, different project → promotes.
- `project-C.md` — L1 with the SAME claim, OPPOSING fix ("Do NOT set the header") → contested.

## Acceptance run (commands + output)

### TEST 1 — init → pool created; status shows 0 claims
```
$ python3 pool.py init --pool /private/tmp/gotm-pool-test
Initialized pool: /private/tmp/gotm-pool-test/POOL.md
  .backups/ ready at /private/tmp/gotm-pool-test/.backups
$ python3 pool.py status --pool /private/tmp/gotm-pool-test
  claims: 0
  by confidence: candidate=0, validated=0, core=0
```
PASS.

### TEST 2 — merge project-A (2 records) → 2 candidates
```
$ python3 pool.py merge project-A.md --project project-A --pool /private/tmp/gotm-pool-test
  backup: .../.backups/POOL-20260708T144700.940427.md
  MISSING: NONE
  +2 new candidate(s), +0 evidence append(s), 0 promoted, 0 contested
```
PASS.

### TEST 3 — merge project-B (same claim, different project) → PROMOTE to validated
```
$ python3 pool.py merge project-B.md --project project-B --pool /private/tmp/gotm-pool-test
  MISSING: NONE
  +0 new candidate(s), +1 evidence append(s), 1 promoted, 0 contested
  PROMOTED → validated: project-A/L1
```
A/L1 promoted (evidence from project-A + project-B = 2 distinct projects). A/L2 stayed candidate. PASS.

### TEST 4 — merge project-C (opposing fix) → contested + demoted; NOT overwritten
```
$ python3 pool.py merge project-C.md --project project-C --pool /private/tmp/gotm-pool-test
  MISSING: NONE
  +0 new candidate(s), +1 evidence append(s), 0 promoted, 1 contested
  CONTESTED (flagged, demoted if validated): project-A/L1
```
Resulting record (original fix preserved; conflicting evidence appended with `[CONFLICT]`;
`contested: true`-note set; validated→candidate demote):
```
- id: "project-A/L1"
  fix: "Set the x-goog-user-project header on every API call"   # NOT overwritten
  evidence:
    - {project: "project-A", ref: "D12", ...}
    - {project: "project-B", ref: "D3", ...}
    - {project: "project-C", ref: "D9", note: "[CONFLICT] header caused wrong project to be billed"}
  confidence: candidate                                          # demoted from validated
  contested: "conflicts with existing fix from project=project-C"
```
PASS.

### TEST 5 — query
```
$ python3 pool.py query --tags auth --pool ...
1 match(es) for tags=auth:
- Serverless jobs need explicit x-goog-user-project quota header · fix: Set the x-goog-user-project header on every API call · candidate · gotcha · 3 project(s) [CONTESTED]

$ python3 pool.py query --tags lakeview --pool ...
1 match(es) for tags=lakeview:
- Lakeview filters must use explicit :param bindings · fix: Use :param placeholders in SQL, not invisible filter injection · candidate · pattern · 1 project(s)

$ python3 pool.py query --tags doesnotexist --pool ...
No records match (tags=doesnotexist). Empty result.
```
PASS (tag match terse w/ claim·fix·confidence·kind·#projects; non-match clean-empty).

### TEST 6 — lossless: every merge prints MISSING: NONE; a .backups/ snapshot per merge
```
$ ls -1 /private/tmp/gotm-pool-test/.backups/
POOL-20260708T144700.940427.md
POOL-20260708T144701.000228.md
POOL-20260708T144701.063917.md      # 3 backups = 3 merges
```
All three merges printed `MISSING: NONE`. PASS.

### TEST 7 — syntax check
```
$ python3 -c "import ast; ast.parse(open('/Users/rohit.dashora/fe-vibe/gotm/scripts/pool.py').read())"
AST PARSE OK
```
PASS.

## Extra edge checks (beyond the 7)
- **Idempotent re-merge:** re-merging project-A → `+0 new, +0 evidence` (evidence deduped by
  `(project,ref)`); `MISSING: NONE`. PASS.
- **`core` never touched by merge:** hand-set A/L1 to `core`, then merged project-B (same claim)
  → `+0 new, +0 evidence, 0 promoted`; record stayed `core`, no B evidence appended. PASS.

## Notes
- Contradiction rule (§8, conservative): same normalized `claim` + differing normalized `fix`
  → contested (identical fixes = agreement/append; different claims = different key). Human resolves.
- `last-merged` marker stored as an HTML comment in POOL.md; Index regenerated deterministically
  (tag → sorted ids). File written sorted by id for stable round-trip.
