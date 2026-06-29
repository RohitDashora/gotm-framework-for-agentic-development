---
project: gotm-framework-for-agentic-development
last_updated: 2026-06-26 (born-tiered v3 migration: this ledger compacted to the v3 shape it teaches — `## Active unit` = pointer · `## Frontier` = open/recent only · `## Archive` = U1–U72 one line each (lossless) · `## Recent updates` = rolling window. v3 content rewrite is complete + gated, tracked in `../V3-DESIGN.md §11`. Active protocol is now v3 — `.gotm/PROTOCOL.md` instantiates `templates/PROTOCOL.md.template`.)
---

# Project ledger

<!-- Born tiered (v3): a hot `## Frontier` re-read every turn + a cold `## Archive`
     pulled only on demand, so per-turn read cost stays flat as the project scales.
     Only the DRIVER writes this file. See .gotm/PROTOCOL.md -> Audit gates /
     Resilience, and ../docs/03-work-as-a-dag.md. -->

## Mission

Distill the GOTM discipline into a public-ready framework — concept docs, a project protocol, prompts, and templates — that any LLM practitioner can adopt to survive bounded-context agentic execution.

## Active unit

**v3 rewrite complete; see [`../V3-DESIGN.md §11`](../V3-DESIGN.md).** Framework v3 content (9 docs + 9 diagrams · 6 prompts · 7 templates) is produced driver/worker and independently gated (zero HIGH/FAIL). Next phases (not yet open as units here): meta-example migration (repo README rewrite, delete v2 docs, MIGRATION.md + converter) and plugin v3.0 (hook follow-on, compaction script, scheduler runtime).

## Frontier

<!-- THE HOT TIER — re-read every turn; keep it small: open units, the recent-
     closed window, and any closed unit a still-open unit still cites as an input.
     Right now there are no open mission units in *this* ledger — the v3 rewrite was
     driven as a self-contained GOTM project and tracked in `../V3-DESIGN.md §11`
     (driver log + risk-tiered audits in `audits/v3-*.md`), not re-registered as
     U-rows here. The U1–U72 history (the v2 framework build + feedback folds) is
     closed and compacted into `## Archive`. -->

_No open mission units in this ledger._

**Recent frontier note — the v3 rewrite (executed, gated, not registered as U-rows here).** The framework was rewritten to v3 — driver/worker/store, born-tiered ledger, structural audit independence (authored-done vs verified-done), the scheduler loop, and the cross-project learning loop. It was driven *as its own GOTM v3 project* (driver plans; stateless workers author each chapter/prompt/template; fresh workers audit). The full driver log + per-chapter audit verdicts live in [`../V3-DESIGN.md §11`](../V3-DESIGN.md) and `audits/v3-*.md`. Phase status there: ✅ DOCS (9 ch + 9 diagrams) · ✅ PROMPTS (6) · ✅ TEMPLATES (7) — all gated. This `.gotm/PROTOCOL.md` + this ledger were then migrated to the v3 shape (this turn) so the repo runs the protocol it teaches.

## Archive

<!-- THE COLD TIER — not on the hot path; pulled only on demand. The closed v2
     units U1–U72 (concept + implementation + every feedback fold), compacted to
     ONE LINE each, newest-first. The audit pointer is kept so the gate stays
     checkable; all other detail already lives in the output files, `audits/`,
     `DECISIONS.md`, and git history. Format:
       - U<n> — <title> · `<output>` · <status> · <verdict>→audits/U<n>.md -->

### geniefy completion-stage feedback G15–G18 (2026-06-23, D22)
- U72 — Close U69 LOW: forward link to `prompts/consult.md` in `prompts/outcome-analysis.md` · `prompts/outcome-analysis.md` · done · —
- U71 — Meta-example sync: mirror G15/G17/G18 into `.gotm/PROTOCOL.md` · `.gotm/PROTOCOL.md` · done · PASS→audits/U71.md
- U70 — README sync: add `prompts/consult.md` + tree/counts; "5-point"→"7-point" · `README.md` · done · PASS→audits/U70.md
- U69 — New `prompts/consult.md` — the consume-step prompt (mirror of outcome-analysis) · `prompts/consult.md` · done · PASS-FINDINGS→audits/U69.md
- U68 — `docs/06`: document the consume MVP (consult + bootstrap pull) · `docs/06-learning-across-projects.md` · done · PASS→audits/U68.md
- U67 — `prompts/audit.md`: G17 checklist 5→7 (enforcement + multi-site) · `prompts/audit.md` · done · PASS→audits/U67.md
- U66 — `templates/LEDGER.md.template`: G15 single recovery log (newest-first); active=pointer · `templates/LEDGER.md.template` · done · PASS→audits/U66.md
- U65 — `templates/PROTOCOL.md.template`: G15 one recovery log + reconcile lints · G17 checklist 5→7 · G18 ledger-parse lint · `templates/PROTOCOL.md.template` · done · PASS-FINDINGS→audits/U65.md

### GOTM core-process feedback check (2026-06-15, D21)
- U64 — `templates/PROTOCOL.md.template`: "a decision change can invalidate a prior pass" + stale-by-decision lint (closes L22 gap) · `templates/PROTOCOL.md.template` · done · PASS-FINDINGS→audits/U64.md

### Cross-project learning layer (2026-06-15, D20)
- U63 — README sync: ch6 + outcome-analysis + LEARNINGS + tree counts · `README.md` · done · PASS→audits/U63.md
- U62 — Draft `prompts/outcome-analysis.md` — end-of-project retrospective → candidate records · `prompts/outcome-analysis.md` · done · PASS-FINDINGS→audits/U62.md
- U61 — Draft `templates/LEARNINGS.md.template` — learning-artifact scaffold · `templates/LEARNINGS.md.template` · done · PASS-FINDINGS→audits/U61.md
- U60 — New ch6 — Learning across projects (3-level bottom-up flow) · `docs/06-learning-across-projects.md` · done · PASS-FINDINGS→audits/U60.md

### G12/G14/G13a incorporation (2026-06-12, D19)
- U59 — **Independent** audit of U55–U58 (final consolidated; per-unit binds hereafter) · `.gotm/audits/U59.md` · done · —
- U58 — Sync `.gotm/PROTOCOL.md` to match G12/G14/G13a · `.gotm/PROTOCOL.md` · done · PASS-FINDINGS→audits/U59.md
- U57 — `prompts/audit.md`: one-report-per-unit + audit-promptly · `prompts/audit.md` · done · PASS-FINDINGS→audits/U59.md
- U56 — `templates/LEDGER.md.template`: grain + cadence + born-`in_progress` conventions · `templates/LEDGER.md.template` · done · PASS-FINDINGS→audits/U59.md
- U55 — `templates/PROTOCOL.md.template`: G12 cadence + G14 born-`in_progress` + G13a grain · `templates/PROTOCOL.md.template` · done · PASS-FINDINGS→audits/U59.md

### README intro hook (2026-06-12)
- U54 — Close U53 LOW: reword intro payoff (stateless/stateful motif canonical) · `README.md` · done · —
- U53 — **Independent** audit of the README intro (U52) · `.gotm/audits/U53.md` · done · —
- U52 — Add pain-point → "what if" intro hook to the README · `README.md` · done · PASS-FINDINGS→audits/U53.md

### Meta-example sync (2026-06-12)
- U51 — **Independent** audit of the meta-example sync (U49–U50) · `.gotm/audits/U51.md` · done · —
- U50 — Sync root `CLAUDE.md` — add four Non-negotiables · `CLAUDE.md` · done · PASS→audits/U51.md
- U49 — Sync `.gotm/PROTOCOL.md` to current protocol (instantiate template w/ mission + `../` links) · `.gotm/PROTOCOL.md` · done · PASS→audits/U51.md

### Layout migration (2026-06-11, D18)
- U48 — Add Mermaid orchestrator diagram to the README · `README.md` · done · mermaid render check passed (mmdc exit 0)
- U47 — Migrate machinery into `.gotm/`; root `CLAUDE.md` → bridge; relocate audit paths · repo layout · done · mechanical link-resolution check passed

### Docs rewrite — 5-chapter arc (2026-06-11, D17)
- U46 — **Independent** publication audit of the rewrite (docs + prompts + README) · `.gotm/audits/U46.md` · done · —
- U45 — README sync — 5-chapter list, word count, prompt descriptions · `README.md` · done · PASS→audits/U46.md
- U44 — Refresh prompts (session-start reconcile; subagent-dispatch independence) · `prompts/session-start.md` + `prompts/subagent-dispatch.md` · done · PASS→audits/U46.md
- U43 — New ch5 — In practice (layouts, the loop, worked example) · `docs/05-in-practice.md` · done · PASS→audits/U46.md
- U42 — New ch4 — Keeping it honest (anti-drift + resilience + audit gates) · `docs/04-keeping-it-honest.md` · done · PASS→audits/U46.md
- U41 — Rewrite + rename ch3 (supersedes U3) · `docs/03-how-the-project-carries-it.md` · done · PASS-FINDINGS→audits/U46.md
- U40 — Rewrite + rename ch2 (supersedes U2) · `docs/02-why-agents-need-it.md` · done · PASS→audits/U46.md
- U39 — Rewrite ch1 — What GOTM is · `docs/01-what-is-gotm.md` · done · PASS→audits/U46.md
- U38 — Lay rewrite foundation — 5-chapter arc, beats, voice guide · (temp outline → locked as D17) · done · —

### Audit-verdict refinement (2026-06-11, D16)
- U37 — Close U36 LOW: align `prompts/audit.md` §4 labels with PROTOCOL/D16 · `prompts/audit.md` · done · —
- U36 — **Independent** audit of the verdict-refinement edits (U33–U35) · `.gotm/audits/U36.md` · done · —
- U35 — `prompts/audit.md`: 5-point default checklist + three-way verdict/stamp · `prompts/audit.md` · done · PASS-FINDINGS→audits/U36.md
- U34 — `LEDGER.md.template`: add `PASS-FINDINGS` to Audit vocab + consume rule · `templates/LEDGER.md.template` · done · PASS-FINDINGS→audits/U36.md
- U33 — `PROTOCOL.md.template` Audit gates: three-way verdict + 5-point checklist + deferral-before-code · `templates/PROTOCOL.md.template` · done · PASS-FINDINGS→audits/U36.md

### Audit-gate phase (2026-06-11, D15)
- U28 — **Independent** audit of feedback-integration + audit-gate edits (U20–U27, U29–U32) · `.gotm/audits/U28.md` · done · —
- U32 — docs/03 §6: strengthen audit cycle with independence + the gate · `docs/03-gotm-with-agents.md` · done · PASS→audits/U28.md
- U31 — `prompts/audit.md`: independence preamble + stamp-the-cell step · `prompts/audit.md` · done · PASS→audits/U28.md
- U30 — `LEDGER.md.template`: add `Audit` column + conventions · `templates/LEDGER.md.template` · done · PASS→audits/U28.md
- U29 — `PROTOCOL.md.template`: add *Audit gates* section + audit-gate lint + deferral/dispatch tie-ins · `templates/PROTOCOL.md.template` · done · PASS→audits/U28.md

### Feedback-integration phase (2026-06-11, D12–D14)
- U27 — CONTRIBUTING: point enforcement at adopter tooling · `CONTRIBUTING.md` · done · PASS→audits/U28.md
- U26 — README: primitives summary + `.gotm/` layout in quickstart/tree · `README.md` · done · PASS→audits/U28.md
- U25 — Update `DECISIONS.md.template` (Status-line edit is the documented mechanism) · `templates/DECISIONS.md.template` · done · PASS→audits/U28.md
- U24 — Update `LEDGER.md.template` conventions (in_progress-first, last_updated, off-mission) · `templates/LEDGER.md.template` · done · PASS→audits/U28.md
- U23 — Update `PROTOCOL.md.template` — anti-drift, resilience, layout note, deferral, off-mission, governance carve-out · `templates/PROTOCOL.md.template` · done · PASS→audits/U28.md
- U22 — docs/01: ledger-as-recovery-point sentence · `docs/01-what-is-gotm.md` · done · PASS→audits/U28.md
- U21 — docs/03: add §7 (anti-drift + resilience) + reconcile step in §3 · `docs/03-gotm-with-agents.md` · done · PASS→audits/U28.md
- U20 — docs/02: add gaps §8 (rules rely on memory) + §9 (non-graceful ends) · `docs/02-what-agents-are-missing.md` · done · PASS→audits/U28.md

### Implementation phase (2026-05-30)
- U19 — Push the rewrite to GitHub (visibility stays PRIVATE) · remote `main` 7f743e8..0f0933e · done · secret-scan: "No Databricks code found"
- U18 — Commit the rewrite to git (single commit) · git commit `0f0933e` on `main` · done · —
- U17 — Meta-validation audit of the rewrite (existence + structure, U1–U16) · `.gotm/audits/U17.md` · done · HIGH 0/MED 0/LOW 3 within tolerance
- U16 — Light pass on `CONTRIBUTING.md` (remove old-framework references) · `CONTRIBUTING.md` (~470w) · done · —
- U15 — Rewrite `README.md` for the new framing · `README.md` (732w) · done · —
- U14 — Delete old `prompts/*.md` (13 old-framework prompt files) · (13 deletions) · done · —
- U13c — Draft `prompts/audit.md` — generic audit prompt · `prompts/audit.md` · done · —
- U13b — Draft `prompts/subagent-dispatch.md` — worker dispatch convention · `prompts/subagent-dispatch.md` · done · —
- U13a — Draft `prompts/session-start.md` — session kickoff template · `prompts/session-start.md` · done · —
- U13 — Rewrite `prompts/` — split into U13a-c · (superseded by U13a-c) · superseded · —
- U12e — Draft `README.md.template` (project-bootstrap version) · `templates/README.md.template` · done · —
- U12d — Draft `QUESTIONS.md.template` · `templates/QUESTIONS.md.template` · done · —
- U12c — Draft `DECISIONS.md.template` · `templates/DECISIONS.md.template` · done · —
- U12b — Draft `LEDGER.md.template` · `templates/LEDGER.md.template` · done · —
- U12a — Draft `PROTOCOL.md.template` · `templates/PROTOCOL.md.template` · done · —
- U12 — Rewrite `templates/` — split into U12a-e · (superseded by U12a-e) · superseded · —
- U11 — Draft `LEDGER.md` (replaces old GOTM.md + STATUS.md) · `LEDGER.md` · done · —
- U10 — Delete old `GOTM.md`, `STATUS.md`, `discovered/` · (deletions) · done · —
- U9 — Append D9, D10, D11 to `DECISIONS.md` · `DECISIONS.md` updates · done · —
- U8 — Rename `OPEN_QUESTIONS.md` → `QUESTIONS.md` · `QUESTIONS.md` · done · —
- U7 — Rename `decisions.md` → `DECISIONS.md` · `DECISIONS.md` · done · —
- U6 — Create `CLAUDE.md` pointing to `PROTOCOL.md` · `CLAUDE.md` · done · —
- U5 — Draft `PROTOCOL.md` · `PROTOCOL.md` · done · —

### Concept phase (2026-05-29)
- U4 — Delete old `docs/01-why.md` through `docs/06-archetypes.md` · (6 deletions) · done · —
- U3 — Draft concept Chapter 3 — GOTM with agents (superseded by U41) · `docs/03-gotm-with-agents.md` · superseded · —
- U2 — Draft concept Chapter 2 — what agents are missing (superseded by U40) · `docs/02-what-agents-are-missing.md` · superseded · —
- U1 — Draft concept Chapter 1 — what GOTM is · `docs/01-what-is-gotm.md` · done · —

## Recent updates

<!-- THE single recovery log — newest-first, rolling window (~last 15). Older
     entries are in git history (and the dated archive sections above). Do not
     start a parallel dated stack under `## Active unit`. -->

- 2026-06-26: **Born-tiered v3 migration of the repo's own store.** Migrated `.gotm/PROTOCOL.md` → v3 (instantiated `templates/PROTOCOL.md.template` with the framework's real mission + `.gotm/` layout + `../docs`/`../prompts`/`../templates` links; fixed the dangling `subagent-dispatch.md` → `worker-dispatch.md`). Migrated this ledger to the born-tiered v3 shape it teaches: `## Active unit` = one-line pointer · `## Frontier` = open/recent only (no open mission units; v3-rewrite frontier note added) · `## Archive` = all 72 v2 units (U1–U72) compacted to one line each, **lossless** (ID · title · status · audit pointer kept; full detail remains in git + `DECISIONS.md` + `audits/`) · `## Recent updates` = this rolling window. The repo now runs the v3 protocol it teaches. (`DECISIONS.md` / `QUESTIONS.md` untouched — append-only.)
- 2026-06-23: **New geniefy feedback — completion-stage addendum (G15–G18), folded as D22.** Four framework-level gaps that surface only after a project runs to completion: G15 recovery-log fragmentation · G16 `/gotm:learn` produces `LEARNINGS.md` into a void (no consumer) · G17 the only two FAILs across ~113 audits fell outside the 5-point checklist · G18 hand-edited + hook-parsed unit table can be silently corrupted. Registered U65–U72; discipline cluster (U65/U66/U67/U71) + consume cluster (U68/U69/U70/U72) done + audited. Framework half of D22 complete. Plugin runtime → v2.6.0 (separate PR).
- 2026-06-23: **D22 consume cluster done + audited (G16).** Shipped `prompts/consult.md` (U69 → PASS-FINDINGS) — the consume-step prompt, mirror of `outcome-analysis.md`. Revised `docs/06` (U68 → PASS) to document both loop halves as paste-able steps. README synced (U70 → PASS): consult.md added, "4→5 prompts", "5-point"→"7-point" fixed. U72 closed the one U69 LOW. **Framework half of D22 fully complete (U65–U72).**
- 2026-06-15: **GOTM core-process feedback check (D21, U64).** L15/L21/L23 already implemented (G12/D19 + Resilience) — no change. Only L22's "re-audit dependents when a decision is refined" half was missing → added as *Audit gates* → "a decision change can invalidate a prior pass" + a *stale-by-decision* reconciliation lint. U64 independent audit → PASS-FINDINGS (0H/0M/1L; zero drift across the three synced copies).
- 2026-06-15: **Cross-project learning layer (D20, U60-U63).** Documented the bottom-up three-level learning flow as new ch6, shipped the *producing* half of L1: `templates/LEARNINGS.md.template` + `prompts/outcome-analysis.md`. README synced. Per-unit audits passed (U60/U61/U62 → PASS-FINDINGS; U63 → PASS). *Consume* + L2/L3 aggregation described, not shipped (platform bindings).
- 2026-06-12: **Folded `geniefy-v3` feedback G12/G14/G13a (D19, U55-U58).** G12 audit-cadence invariants · G14 born-`pending`/`in_progress` · G13a "module+test = one unit" grain. Declined G13b. Plugin ships v2.4.0. Per-unit auditing binds after U59. Independent audit U59 → PASS-FINDINGS (2 LOW).
- 2026-06-12: **Added a pain-point → "what if" intro hook to the README (U52-U54).** Independent audit U53 → PASS-FINDINGS; the one LOW closed by U54.
- 2026-06-12: **Synced the repo's own governance docs to the current discipline (U49-U51).** `.gotm/PROTOCOL.md` brought up to the then-current protocol; root `CLAUDE.md` gained four Non-negotiables. Independent audit U51 → PASS.
- 2026-06-11: **Added a Mermaid orchestrator diagram to the README (U48).** Render-checked with `mmdc` (exit 0).
- 2026-06-11: **Migrated the repo's own machinery into `.gotm/` (D18, U47).** Deliverables stay at root; root `CLAUDE.md` is a thin bridge. Audit paths relocated `audits/…` → `.gotm/audits/…`.
- 2026-06-11: **Concept docs rewritten from scratch → 5-chapter arc (D17, U38-U45).** Independent publication audit U46 → PASS-FINDINGS. (Later superseded by the v3 9-chapter rewrite; see `../V3-DESIGN.md §11`.)
- 2026-06-11: **Audit-verdict refinement done (U33-U37).** D16: three-way verdict (PASS/PASS-FINDINGS/FAIL) + 5-point checklist + deferral-can't-outlast-the-code-gate. U36 independent audit → PASS-FINDINGS; LOW closed by U37.
- 2026-06-11: **Audit-gate pass done (U28-U32).** D15: audit independence as a hard rule + a consume-gate. Added *Audit gates* section, `Audit` column, independence preamble. U28 independent audit → PASS.
- 2026-06-11: **Feedback-integration pass done (U20-U27).** Folded geniefy field feedback (G1-G10): anti-drift, resilience, `.gotm/` layout, governance carve-out, off-mission, sanctioned deferral. D12-D14 locked.
- 2026-05-30: **Rewrite shipped.** U17 meta-audit passed. U18 committed (`0f0933e`); U19 pushed to private GitHub. 19/19 units done. (Older U1–U16 detail is in `## Archive` + git history.)

<!--
Conventions (v3, aligned to templates/LEDGER.md.template):
- BORN TIERED. Hot `## Frontier` (open units + recent-closed window + any closed
  unit a still-open unit still cites as input) + cold `## Archive` (everything
  older, one line each). The driver re-reads the frontier every turn, the archive
  never — flat per-turn read cost as the project scales. Read the AUDIT FILE, not
  a fat ledger cell.
- SINGLE WRITER. Only the driver writes this file. Workers execute one unit and
  return a terse structured result (status + output pointer + index facts); the
  driver records it. Kills the v2 dup-row race by construction.
- IDs are flat (U1, U2, U3...). The DAG's structure lives in the `Inputs` edges,
  not in the IDs.
- Each row produces ONE named output file (atomicity). A module + its test file
  count as ONE unit — atomicity is one deliverable, not literally one file.
- Status — the v3 lifecycle: pending · in_progress · authored-done (output exists,
  NOT independently checked, NOT consumable on its own) · verified-done (an
  INDEPENDENT auditor ≠ author passed it; for deploy/infra/data the worker also
  exercises the live artifact — the consumable terminal state) · superseded.
  (The archive above carries v2 `done`/`superseded` verbatim — historical; new
  units use the v3 states.)
- `Audit` holds the verdict + pointer: `—` (n/a) | `pending` | `PASS→audits/U<id>.md`
  | `PASS-FINDINGS→audits/U<id>.md` | `FAIL→audits/U<id>.md` | `superseded by U<yy>`.
  A unit reaches `verified-done` only on PASS / PASS-FINDINGS. A downstream unit
  may CONSUME an input only when it is verified-done. One audit + one report PER
  UNIT, from its OWN report, by a DIFFERENT worker than the author.
- BORN pending/in_progress, NEVER done. Flip to authored-done only after the
  output exists; to verified-done only after an independent worker passes it.
- Closed units are never edited. To revise, append a follow-on unit.
- COMPACTION is an index op, not a freeze violation. When the ledger crosses a
  size/count threshold, move aged-out closed+verified units from `## Frontier` to
  a one-line `## Archive` entry and roll `Recent updates` past its window. LOSSLESS
  — the audit pointer is kept, detail lives in output/`audits/`/`DECISIONS.md` —
  so it touches no frozen output. (This very ledger demonstrates it: U1–U72 sit in
  `## Archive` as one-liners; full detail in git history.)
- Stamp `last_updated` (front matter) on every write-back.
- ONE recovery log, ONE ordering: `## Recent updates` is the single recovery log,
  newest-first; `## Active unit` is a one-line pointer, never a dated banner stack.
- Off-mission artifacts do NOT go in the Frontier table. Produce the file, then add
  a "Recent updates" line marked `(not a mission unit)`.
- LAYOUT (this repo): the store lives in `.gotm/`; deliverables at repo root.
  `docs/` and `prompts/` resolve as `../` from here. See .gotm/PROTOCOL.md -> Layout.
-->
