# GOTM — the shared learning pool (L2) — design

> **Status:** v0.1, for redline. Foundation doc for the cross-project learning pool. Ships as **v3.36** (next above 3.35.0).
> **Why:** the learning loop has produce (`/gotm:learn`) + consume (`/gotm:consult`) *prompts*, but **no shared store** — produce writes into a void (one lonely `LEARNINGS.md` on disk; merge is prose, not a step). Cohesion = a real cross-project store **with its own discipline** — GOTM recursed one level up (pool = store · record = unit · merge-by-claim = write-back · independent confirmation = audit gate · contradiction-demotes = anti-drift).
> **Method:** built driver/worker, execution-proven, independently audited. On disk, not chat.

---

## 1. The scope decision (locked, per the discussion)
- **Location:** `~/.gotm/learnings/` — the **user home**, so it's cross-project by construction (same as `~/.npm`, `~/.config`). Same `.gotm` name as the project store; different *location* → different scope.
- **Tooling home:** `pool.py` lives in the **plugin** (`$CLAUDE_PLUGIN_ROOT/scripts/pool.py`), **not** in per-project `templates/scripts/`. Cross-project tools belong to the machine-global thing (the plugin), not the per-project copy. One `pool.py`, one pool, all projects.
- **Wiring:** **convention, not config** — the pool is always `~/.gotm/learnings/` (resolve `$HOME`); no per-project setup. A `--pool <dir>` override enables a team/shared pool later (L2→L3 bridge).
- **Out of scope (this build):** L3 (enterprise semantic index / knowledge graph, e.g. a context catalog) — kept *pluggable*, not built.

## 2. The store layout
```
~/.gotm/learnings/
  POOL.md         ← the merged corpus: a generated tag Index (top) + Records (the schema)
  .backups/       ← a timestamped POOL.md snapshot taken BEFORE every merge (losslessness)
```
Single merged `POOL.md` (not a folder of raw project files, not a `records/` dir) — greppable, one readable pool, same record schema as `LEARNINGS.md`. The Index is regenerated on every merge.

## 3. The record (reuse the shipped schema — do not reinvent)
```
- id: <project>/L<n>            # provenance of first sighting
  claim: "<generalized lesson>"  # THE MERGE KEY
  kind: gotcha|prerequisite|pivot|pattern|anti-pattern
  tags: [<tech>, <domain>, <phase>]
  fix: "<what to do>"
  scope: <where it applies>
  evidence:                      # APPENDABLE across projects
    - {project: <name>, ref: <D##/audit Uxx>, note: "<observed>"}
  confidence: candidate|validated|core
  contested: <optional true + note, when a later project conflicts>
```

## 4. `pool.py` — the tool (CLI contract — LOCKED; all workers build to this)
Default pool dir = `$HOME/.gotm/learnings/` (expand `~`). Every mutating op **backs up `POOL.md` to `.backups/POOL-<ts>.md` first** and **verifies no `claim` is dropped** (prints `MISSING: NONE` or lists).

```
pool.py init   [--pool DIR]
    Create the pool dir + an empty POOL.md (header + empty Index + Records) + .backups/. Idempotent.

pool.py merge  <LEARNINGS.md> [--project NAME] [--pool DIR]
    Merge a project's records into the pool:
      - claim exists  → APPEND this project's evidence (dedupe by (project,ref)); never duplicate the record.
      - claim absent  → add it as `candidate`.
      - PROMOTION: after append, if a claim's evidence has ≥2 DISTINCT `project` values → candidate→validated.
      - CONTRADICTION: incoming record whose `fix`/`claim` opposes an existing one → do NOT overwrite;
        set the existing record `contested: true` + append the conflicting evidence with a note; if it was
        `validated`, demote → `candidate` (contested). Flag every contested claim in the summary.
      - `core` is NEVER set/changed by merge (L3/enterprise-curated only).
    Then regenerate the Index. Print a summary: +N new candidates, +M evidence appends, P promoted, C contested.

pool.py query  --tags a,b[,c] [--kind K] [--min-confidence candidate|validated|core] [--pool DIR]
    Scan the Index, return the tag-intersecting records TERSELY (claim · fix · confidence · kind · #projects).
    For /gotm:consult. Empty/no-match is a valid, clearly-stated result.

pool.py status [--pool DIR]
    Counts by confidence + kind; #claims; #contested; pool size; last-merged timestamp.
```

**The promotion/demotion gate is the pool's audit gate** — it is what keeps shared knowledge from rotting: `validated` requires an *independent* project (auditor≠author across projects, mechanized as ≥2 distinct `project`s), and a contradiction *demotes + flags* rather than silently overwriting.

## 5. Wiring the loop through the pool
- **`/gotm:learn`** — after writing `.gotm/LEARNINGS.md`, run `pool.py merge .gotm/LEARNINGS.md --project <name>`. Report what merged/promoted/contested.
- **`/gotm:consult`** — default pool = `~/.gotm/learnings/` via `pool.py query --tags <this project's stack/domain/phase>`; write survivors to `.gotm/CONSULTED.md`. Keep the `--pool` override.
- **`/gotm:bootstrap`** — the Step 4.5 consult-pull now hits the real pool (`pool.py init` if missing, then query).
- **New `/gotm:pool`** command — `init` / `status` / `query` for direct pool inspection.

## 6. Framework vs plugin (the two-repo split holds)
- **Framework (neutral):** `docs/09` + `prompts/{outcome-analysis,consult}.md` describe the L2 pool **concretely** now — the home-dir store, the merge/promote *steps*, the promotion-gate discipline, and the scope ladder. The framework still ships *prompts, not a runtime*: it specifies the steps + the default location; the *store lives on the user's machine*, the *tool ships in the plugin*.
- **Plugin (runtime):** ships `scripts/pool.py` (plugin top-level, not `templates/`), the `/gotm:pool` command, and the wiring in `learn`/`consult`/`bootstrap`.

## 7. Scope ladder
```
<project>/.gotm/     →     ~/.gotm/learnings/     →     a shared git repo  /  enterprise catalog
   L1 project (have)          L2 user (THIS build)         L3 team / org (pluggable via --pool / an index)
```

## 8. Decisions (LOCKED — recommendations accepted)
- **Single `POOL.md`** (merged records + generated Index), not a `records/` dir. Simpler, greppable.
- **Independent-project detection** = ≥2 distinct `project` values in a claim's `evidence`.
- **Contradiction** = mark `contested` + append conflicting evidence + demote `validated→candidate`; never overwrite; flag in summary (human resolves).
- **`pool.py` lives in the plugin top-level `scripts/`** (cross-project), invoked via `$CLAUDE_PLUGIN_ROOT`.
- **Version: v3.36** (next above 3.35.0).

## 9. Build plan (driver/worker, dogfooded)
- **W-pool** — `scripts/pool.py` (init/merge/query/status) + the promotion/demotion gate. **Execution-gated:** merge two synthetic project LEARNINGS files → same claim promotes to `validated`; a conflicting fix marks `contested` + demotes; lossless (`MISSING: NONE`); query returns tag-matches. Paste proof.
- **W-wire** — new `commands/pool.md`; wire `commands/{learn,consult,bootstrap}.md` to `pool.py` + the home pool.
- **W-prompts** — update plugin + framework `prompts/{outcome-analysis,consult}.md` to the pool.
- **W-docs** — framework `docs/09-learning-across-projects.md`: the L2 pool made concrete (home store, `pool.py`, the promotion gate, the scope ladder).
- **Then:** independent coherence + audit (re-run the `pool.py` proof myself), version → 3.36.0, commit + publish.
