# Independent Audit — v3 Migrated Governance + Chapter Diagrams

**Auditor:** independent (did not build this). **Date:** 2026-06-29.
**Scope:** README.md, CLAUDE.md, .gotm/PROTOCOL.md, .gotm/LEDGER.md, MIGRATION.md, and the Mermaid diagrams in docs/02–07,09.
**Method:** whole-repo grep for v2 dangling refs; markdown-link-vs-inline-code resolution against disk; U-ID count in the LEDGER archive; converter-script claims cross-check; per-diagram comparison to its chapter prose (focus: ch5 fan-in, ch7 no-compaction-hook, ch2 role table).

---

## Summary

The migrated governance surface is in good shape. **Every markdown *link* in the live publishable files (README, CLAUDE.md, PROTOCOL.md) and in the operational prompts resolves to a file that exists on disk** — there are **no dangling links in the publishable surface.** PROTOCOL.md is a clean v3 instantiation (real mission filled in, no v2 leftovers, no unfilled placeholders). LEDGER.md is correctly born-tiered and its Archive is **complete: 80 unique U-IDs (U1–U72 incl. U12a–e and U13a–c), lossless, format-consistent, audit pointers kept.** MIGRATION.md accurately describes the v2→v3 migration and references the real, parameterized converter at `scripts/migrate_ledger_v2_to_v3.py`. **All 9 Mermaid diagrams accurately depict their chapters' prose** — including the three load-bearing ones (ch5 fan-in shows the driver getting ONE pointer; ch7 shows NO compaction hook; ch2 matches the role table).

The defects found are **count/traceability inaccuracies in the project's own records**, not broken publishable artifacts: a repeated "8 diagrams" undercount (there are 9), and three "all-gated" chapters with no audit file on disk. The v2 paths that still appear in the LEDGER archive and audits/ are legitimate frozen history (inline code, not links), per the migration design.

---

## HIGH

_None._ No dangling markdown link in the publishable surface; no diagram contradicts its chapter.

---

## MEDIUM

### M1 — "8 diagrams" is a wrong count; there are 9 (self-contradicted in the same line)
The project records claim **8 Mermaid diagrams**, but the repo contains **9**.
- `V3-DESIGN.md:151` — "**8 Mermaid diagrams** across ch2–7 + ch9 … All render-validated — `mmdc` **9/9** exit 0." The line states "8" and "9/9" in the same breath: the prose count is wrong, the render count is right.
- `V3-DESIGN.md:161`, `.gotm/LEDGER.md:19`, `.gotm/LEDGER.md:33` — all repeat "9 docs + **8 diagrams**".

Actual count = 9 (`grep -c '```mermaid'`): ch02=1 (`docs/02-driver-worker-store.md:37`), ch03=**2** (`docs/03-work-as-a-dag.md:24` DAG, `:47` born-tiered ledger), ch04=1 (`docs/04-the-loop.md:27`), ch05=**2** (`docs/05-scaling-and-economy.md:30` fan-in rule/anti-pattern, `:68` fan-out tree), ch06=1 (`docs/06-keeping-it-honest.md:43`), ch07=1 (`docs/07-resilience-and-memory.md:29`), ch09=1 (`docs/09-learning-across-projects.md:33`). The "8" undercounts one of the two-per-chapter diagrams. (The audit brief inherited the same "8" figure.) Stale claim — does not affect the published docs, but the governance/design ledger misreports its own output.

### M2 — "all gated (zero HIGH/FAIL)" for 9 chapters, but 3 chapters have no audit file on disk
`.gotm/LEDGER.md:19` and `:33` and `V3-DESIGN.md:153,161` assert the 9 v3 chapters were "produced driver/worker and **independently gated**," with per-chapter verdicts said to live in `audits/v3-*.md` (`.gotm/LEDGER.md:33`). On disk, `.gotm/audits/v3-ch*.md` exists for **ch01, ch02, ch03, ch05, ch06, ch07 only** — there is **no `v3-ch04.md`, `v3-ch08.md`, or `v3-ch09.md`.** Two of the missing three (ch04 the loop, ch09 the learning layer) are diagram-bearing chapters. The verified-done gate the LEDGER points to is unbacked for these three: the "all gated" claim cannot be followed to a verdict artifact for ch04/ch08/ch09. Either the audits were never filed (gate gap) or the claim overstates coverage.

---

## LOW

### L1 — ch2 diagram omits the worker→store *write* edge
`docs/02-driver-worker-store.md:37–54` draws four flows: driver→dispatch→worker, worker→terse result→driver, worker→read inputs→store, driver→write→store. The prose (`:17`) says a worker "writes its one output" to the store, and the role table has the worker producing exactly one output. The diagram shows the worker *reading* from the store but not *writing* its output to it. Not a contradiction (the caption at `:56` scopes the figure to "read their inputs … return only a terse result"), but the diagram is an incomplete picture of the worker↔store relationship the chapter describes. Cosmetic.

### L2 — LEDGER front-matter date vs migration-log date
`.gotm/LEDGER.md:3` front-matter is dated `2026-06-26` and the Recent-updates migration entry (`:156`) is `2026-06-26`; the file mtime is 26 Jun. Internally consistent; noted only because the born-tiered migration narrative is the load-bearing claim of the file and rests on that single date. No action.

---

## NOT defects (verified, called out to forestall false positives)

- **v2 paths in the LEDGER Archive and `.gotm/audits/`** — e.g. `docs/06-learning-across-projects.md` (`.gotm/LEDGER.md:49,61`), `prompts/subagent-dispatch.md` (`.gotm/LEDGER.md:87,127`), `docs/0{1..5}-{old names}` (`.gotm/LEDGER.md:88–92,104,115–117,145–148`). These are **frozen historical archive rows rendered as inline code, not markdown links**, and the migration was explicit about keeping them lossless. They are correct history, not dangling links. Same for the `subagent-dispatch.md` mentions in `.gotm/audits/U17,U46,U51,U53,U63,U67,U70.md` and `DECISIONS.md:131,145,255,297,299`.
- **README.md:80 / MIGRATION.md:51,147 / prompts/worker-dispatch.md:11** referencing `subagent-dispatch` — all are *supersession* statements ("supersedes v2's `subagent-dispatch`" / "delete that one"), inline code, intentional. Correct.
- **prompts/outcome-analysis.md:87** `docs/06-keeping-it-honest.md` and **:13,104 / consult.md:12,93** `docs/09-learning-across-projects.md` — semantically correct (ch6 *is* keeping-it-honest, ch9 *is* learning-across-projects in v3) and resolve on disk.
- **U72 audit = `—`** (`.gotm/LEDGER.md:45`) — U72 was a LOW-closing follow-on; `audits/U72.md` legitimately absent. Consistent with the `—` verdict cell, not a missing-artifact defect (distinct from M2, where the cells/claims assert a gate).
- **PROTOCOL.md** (`.gotm/PROTOCOL.md`) — clean v3: real mission at `:135`, layout note for the subfolder example, all 6 prompts linked (`../prompts/*`), `../docs/01-…` and `../docs/08-…` links resolve. No v2 content, no `{{placeholder}}` left unfilled.
- **LEDGER Archive U-ID count = 80** (U1–U72 with U12a–e, U13a–c) — matches the expected ~80; all present; one-line-each, newest-first, audit pointer kept; format consistent across the dated sections.
- **MIGRATION.md** — converter path real and parameterized (`scripts/migrate_ledger_v2_to_v3.py`: `argparse`, `--ledger` required unless `DEFAULT_LEDGER` set, `.bak` backup, `LEDGER-ARCHIVE.md` overflow, `MISSING: NONE` gate — all as described). Role table matches PROTOCOL/ch2; the 5-state mapping matches the ledger conventions.
- **Diagram fidelity, all 9:**
  - **ch5 fan-in (load-bearing) — CORRECT.** `docs/05:30–56`: left "RULE" = fan-in worker reads N from store → writes merged → hands driver **ONE pointer**; right "ANTI-PATTERN" = store→**N bodies**→driver merges in-context (monotonicity). Driver never gets N bodies in the rule. Matches `:26` hard-rule prose.
  - **ch7 (load-bearing) — CORRECT.** `docs/07:29–46`: only T2→re-hydrate→T1 and T3→pull-on-demand→T2. **No compaction-hook node or edge** — consistent with the chapter's emphatic "re-hydration depends on no compaction hook" (`:17`).
  - **ch2 (load-bearing) — CORRECT** (see L1 for the one omitted edge): roles/flows match the role table (`:9–13`) and "single writer" (`:33`).
  - ch3 DAG (`:24`) + born-tiered ledger (`:47`), ch4 loop (`:27`), ch5 fan-out tree (`:68`), ch6 audit flow (`:43`), ch9 three-level learning (`:33`) — each matches its prose; verdict colors, gate logic, confidence ladder all consistent.

---

## Verdict

**PASS-FINDINGS.** The migrated governance docs and all 8/9 chapter diagrams are accurate and publishable: no dangling links on the published surface, no diagram contradicts its chapter, PROTOCOL.md is a clean v3 instantiation, the LEDGER archive is complete and lossless (80 U-IDs), and MIGRATION.md is accurate. Two non-blocking record-accuracy defects remain: **M1** — the "8 diagrams" count is wrong (there are 9, self-contradicted against "mmdc 9/9" in the same line); **M2** — "all 9 chapters independently gated" is unbacked for ch04, ch08, ch09 (no `audits/v3-ch{04,08,09}.md` on disk). Both should become follow-on units: correct the count in V3-DESIGN.md:151,161 + LEDGER:19,33, and either file or downgrade the gate claim for the three chapters.
