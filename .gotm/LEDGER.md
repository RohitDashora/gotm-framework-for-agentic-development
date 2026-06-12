---
project: gotm-framework-for-agentic-development
last_updated: 2026-06-12 (README intro hook U52-U54, audit PASS-FINDINGS; governance sync U49-U51; diagram U48; .gotm migration U47; docs rewrite U38-U46; publication-ready; Q2 visibility still open)
---

# Project ledger

## Mission

Distill the GOTM discipline into a public-ready framework — concept docs, a project protocol, prompts, and templates — that any LLM practitioner can adopt to survive bounded-context agentic execution.

## Active unit

**(none active)** — the repo's own governance docs are now synced to the current discipline (U49 `.gotm/PROTOCOL.md`, U50 `CLAUDE.md`), independently audited (U51 → **PASS**). The meta-example now runs the full protocol it teaches.

Recent arc: docs rewritten to a 5-chapter arc (D17, U38-U46, audit `.gotm/audits/U46.md`); machinery migrated into `.gotm/` (D18, U47); README orchestrator diagram (U48); governance-doc sync (U49-U51). Every pass independently audited (`.gotm/audits/U28.md`, `U36.md`, `U46.md`, `U51.md`). Q2 (visibility flip from PRIVATE to PUBLIC) remains the standing open ratification — the repo is publication-ready.

## Units

> Grouping by phase is convenience only. There is no hierarchy — only an ordered list of atomic units.

### Concept phase (done)

| ID | Title | Inputs | Output | Status |
|---|---|---|---|---|
| U1 | Draft concept Chapter 1 — what GOTM is | — | `docs/01-what-is-gotm.md` | done |
| U2 | Draft concept Chapter 2 — what agents are missing | U1 | `docs/02-what-agents-are-missing.md` | done |
| U3 | Draft concept Chapter 3 — GOTM with agents | U1, U2 | `docs/03-gotm-with-agents.md` | done |
| U4 | Delete old `docs/01-why.md` through `docs/06-archetypes.md` | — | (6 deletions) | done |

### Implementation phase

| ID | Title | Inputs | Output | Status |
|---|---|---|---|---|
| U5 | Draft `PROTOCOL.md` | docs/01-03 | `PROTOCOL.md` | done |
| U6 | Create `CLAUDE.md` pointing to `PROTOCOL.md` | `PROTOCOL.md` | `CLAUDE.md` | done |
| U7 | Rename `decisions.md` → `DECISIONS.md` | — | `DECISIONS.md` | done |
| U8 | Rename `OPEN_QUESTIONS.md` → `QUESTIONS.md` | — | `QUESTIONS.md` | done |
| U9 | Append D9, D10, D11 to `DECISIONS.md` | — | `DECISIONS.md` updates | done |
| U10 | Delete old `GOTM.md`, `STATUS.md`, `discovered/` | — | (deletions) | done |
| U11 | Draft `LEDGER.md` (this file; replaces old GOTM.md + STATUS.md) | U1-U10 | `LEDGER.md` | done |
| U12 | Rewrite `templates/` — split into U12a-e per atomicity | — | (superseded by U12a-e) | superseded |
| U12a | Draft `PROTOCOL.md.template` | `PROTOCOL.md` | `templates/PROTOCOL.md.template` | done |
| U12b | Draft `LEDGER.md.template` | `LEDGER.md`, `docs/02` | `templates/LEDGER.md.template` | done |
| U12c | Draft `DECISIONS.md.template` | `DECISIONS.md` | `templates/DECISIONS.md.template` | done |
| U12d | Draft `QUESTIONS.md.template` | `QUESTIONS.md` | `templates/QUESTIONS.md.template` | done |
| U12e | Draft `README.md.template` (project-bootstrap version) | `PROTOCOL.md`, `LEDGER.md` | `templates/README.md.template` | done |
| U13 | Rewrite `prompts/` — split into U13a-c per atomicity | — | (superseded by U13a-c) | superseded |
| U13a | Draft `prompts/session-start.md` — session kickoff template | `PROTOCOL.md` | `prompts/session-start.md` | done |
| U13b | Draft `prompts/subagent-dispatch.md` — worker dispatch convention | `PROTOCOL.md`, U13a | `prompts/subagent-dispatch.md` | done |
| U13c | Draft `prompts/audit.md` — generic audit prompt | `PROTOCOL.md`, docs/03 §6 | `prompts/audit.md` | done |
| U14 | Delete old `prompts/*.md` (13 old-framework prompt files) | — | (13 deletions) | done |
| U15 | Rewrite `README.md` for the new framing | all prior implementation units | `README.md` (732w) | done |
| U16 | Light pass on `CONTRIBUTING.md` (remove old-framework references) | U15 | `CONTRIBUTING.md` (~470w) | done |
| U17 | Meta-validation audit of the rewrite — existence + structure across all claimed-done units (U1-U16) | LEDGER.md as oracle, all U1-U16 outputs as targets, `prompts/audit.md` for shape | `.gotm/audits/U17.md` (HIGH 0 / MED 0 / LOW 3 within tolerance / UNVERIFIED 0; recommendation: proceed to commit; out-of-kind notes: empty drafts/ cleaned, .DS_Store gitignored) | done |
| U18 | Commit the rewrite to git (single commit; message captures the reframe) | U17 verdict | git commit `0f0933e` on `main` | done |
| U19 | Push the rewrite to GitHub (visibility stays PRIVATE) | U18 | remote `main` at `7f743e8..0f0933e`; Databricks secret-scan: "No Databricks code found" | done |

### Feedback-integration phase (2026-06-11)

> Source: `geniefy-v3/docs/GOTM-FEEDBACK.md` (G1-G10). Conceptual/paste-able items only; runtime enforcement (the hook) folded into the `gotm` plugin per D12, not here.

| ID | Title | Inputs | Output | Status | Audit |
|---|---|---|---|---|---|
| U20 | docs/02: add gaps §8 (rules rely on memory) + §9 (non-graceful ends) | GOTM-FEEDBACK G1, G10 | `docs/02-what-agents-are-missing.md` | done | PASS→.gotm/audits/U28.md |
| U21 | docs/03: add §7 (anti-drift safeguards + resilience) + reconcile step in §3 | U20, GOTM-FEEDBACK G1, G10 | `docs/03-gotm-with-agents.md` | done | PASS→.gotm/audits/U28.md |
| U22 | docs/01: ledger-as-recovery-point sentence | GOTM-FEEDBACK G10 | `docs/01-what-is-gotm.md` | done | PASS→.gotm/audits/U28.md |
| U23 | Update `PROTOCOL.md.template` — anti-drift, resilience, layout note, audit-deferral, off-mission, governance carve-out | D13, D14, U20, U21 | `templates/PROTOCOL.md.template` | done | PASS→.gotm/audits/U28.md |
| U24 | Update `LEDGER.md.template` conventions (in_progress-first, last_updated stamp, off-mission) | D13 | `templates/LEDGER.md.template` | done | PASS→.gotm/audits/U28.md |
| U25 | Update `DECISIONS.md.template` (Status-line edit is the documented mechanism) | D13 | `templates/DECISIONS.md.template` | done | PASS→.gotm/audits/U28.md |
| U26 | README: primitives summary + `.gotm/` layout in quickstart/tree; word count | D14 | `README.md` | done | PASS→.gotm/audits/U28.md |
| U27 | CONTRIBUTING: point enforcement at adopter tooling (don't forbid safeguards) | D12 | `CONTRIBUTING.md` | done | PASS→.gotm/audits/U28.md |

### Audit-gate phase (2026-06-11)

> Follow-up ask: "proper audit checks + gates; auditor ≠ author." Conceptual/paste-able only; the `/gotm audit` command + header-aware hook live in the `gotm` plugin (D12, D15). U29/U32 are follow-ons that further evolve U23/U21's outputs.

| ID | Title | Inputs | Output | Status | Audit |
|---|---|---|---|---|---|
| U29 | `PROTOCOL.md.template`: add *Audit gates* section + audit-gate lint + deferral/dispatch tie-ins | D15, U23 | `templates/PROTOCOL.md.template` | done | PASS→.gotm/audits/U28.md |
| U30 | `LEDGER.md.template`: add `Audit` column + conventions | D15 | `templates/LEDGER.md.template` | done | PASS→.gotm/audits/U28.md |
| U31 | `prompts/audit.md`: independence preamble + stamp-the-cell step | D15 | `prompts/audit.md` | done | PASS→.gotm/audits/U28.md |
| U32 | docs/03 §6: strengthen audit cycle with independence + the gate | D15, U21 | `docs/03-gotm-with-agents.md` | done | PASS→.gotm/audits/U28.md |
| U28 | **Independent** audit of the feedback-integration + audit-gate edits (existence + render + cross-doc consistency) — dispatched fresh auditor, not self-audit | U20-U27, U29-U32 | `.gotm/audits/U28.md` | done | — |

### Audit-verdict refinement phase (2026-06-11)

> Source: updated `geniefy-v3/docs/GOTM-FEEDBACK.md` G11 + Appendix D. D16. Follow-ons to U29/U31. The plugin mirrors these + updates `/gotm audit` stamp logic (D12).

| ID | Title | Inputs | Output | Status | Audit |
|---|---|---|---|---|---|
| U33 | `PROTOCOL.md.template` Audit gates: add three-way verdict (PASS/PASS-FINDINGS/FAIL) + 5-point checklist + deferral-before-code | D16, U29 | `templates/PROTOCOL.md.template` | done | PASS-FINDINGS→.gotm/audits/U36.md |
| U34 | `LEDGER.md.template`: add `PASS-FINDINGS` to Audit vocab + consume rule | D16, U30 | `templates/LEDGER.md.template` | done | PASS-FINDINGS→.gotm/audits/U36.md |
| U35 | `prompts/audit.md`: 5-point default checklist + three-way verdict/stamp | D16, U31 | `prompts/audit.md` | done | PASS-FINDINGS→.gotm/audits/U36.md |
| U36 | **Independent** audit of the verdict-refinement edits (U33-U35) — dispatched fresh auditor | U33-U35 | `.gotm/audits/U36.md` | done | — |
| U37 | Close U36 LOW: align `prompts/audit.md` §4 labels ("cross-reference integrity" / "internal consistency") with PROTOCOL/D16 | U36 | `prompts/audit.md` | done | — |

### Docs rewrite phase (2026-06-11)

> D17. Concept docs rewritten from scratch into a 5-chapter arc now that the framework is battle-tested. U40/U41 supersede U2/U3 and rename their files (old files deleted; historical rows above left intact per append-only). Foundation outline was a temp doc, consumed and deleted.

| ID | Title | Inputs | Output | Status | Audit |
|---|---|---|---|---|---|
| U38 | Lay rewrite foundation — 5-chapter arc, per-chapter beats, voice guide | D17 | (temp outline → arc, deleted; locked as D17) | done | — |
| U39 | Rewrite ch1 — What GOTM is | D17, U38 | `docs/01-what-is-gotm.md` | done | PASS→.gotm/audits/U46.md |
| U40 | Rewrite + rename ch2 — Why agents need it (supersedes U2) | D17, U38 | `docs/02-why-agents-need-it.md` | done | PASS→.gotm/audits/U46.md |
| U41 | Rewrite + rename ch3 — How the project carries the discipline (supersedes U3) | D17, U38 | `docs/03-how-the-project-carries-it.md` | done | PASS-FINDINGS→.gotm/audits/U46.md |
| U42 | New ch4 — Keeping it honest under real conditions (anti-drift + resilience + audit gates) | D17, U38 | `docs/04-keeping-it-honest.md` | done | PASS→.gotm/audits/U46.md |
| U43 | New ch5 — In practice (layouts, the loop, worked software example) | D17, U38 | `docs/05-in-practice.md` | done | PASS→.gotm/audits/U46.md |
| U44 | Refresh prompts for consistency (session-start reconcile; subagent-dispatch independence) | D17 | `prompts/session-start.md` + `prompts/subagent-dispatch.md` | done | PASS→.gotm/audits/U46.md |
| U45 | README sync — 5-chapter list, word count, prompt descriptions | D17, U39-U44 | `README.md` | done | PASS→.gotm/audits/U46.md |
| U46 | **Independent** publication audit of the rewrite (docs + prompts + README) — dispatched fresh auditor | U39-U45 | `.gotm/audits/U46.md` | done | — |

### Layout migration phase (2026-06-11)

> D18. Dogfood the `.gotm/` subfolder layout: move the repo's own machinery into `.gotm/`, keep deliverables at root, convert root `CLAUDE.md` to a bridge.

| ID | Title | Inputs | Output | Status | Audit |
|---|---|---|---|---|---|
| U47 | Migrate machinery into `.gotm/` (PROTOCOL/LEDGER/DECISIONS/QUESTIONS/audits); root `CLAUDE.md` → bridge; update refs in README/CONTRIBUTING/PROTOCOL + relocate audit paths | D18 | repo layout (`.gotm/` + root bridge) | done | mechanical link-resolution check passed |
| U48 | Add a Mermaid orchestrator/architecture diagram to the README (What GOTM is) | docs/01,03,04 | `README.md` | done | mermaid render check passed (mmdc, exit 0) |

### Meta-example sync phase (2026-06-12)

> The repo's own governance docs had fallen behind the discipline they teach. Bring them up to the current protocol (D13 anti-drift, D15/D16 audit gates, D18 layout). Governance docs are living (editable), per the pre-edit carve-out.

| ID | Title | Inputs | Output | Status | Audit |
|---|---|---|---|---|---|
| U49 | Sync `.gotm/PROTOCOL.md` to the current protocol (anti-drift, resilience, audit gates, reconcile step, .gotm Layout note) — instantiate `templates/PROTOCOL.md.template` with the framework's mission + `../` links | D13, D15, D16, D18, `templates/PROTOCOL.md.template` | `.gotm/PROTOCOL.md` | done | PASS→.gotm/audits/U51.md |
| U50 | Sync root `CLAUDE.md` — add the four Non-negotiables (frozen units · write-back · resilience/cold-start · audit independence) | D13, D15, D16, U49 | `CLAUDE.md` | done | PASS→.gotm/audits/U51.md |
| U51 | **Independent** audit of the meta-example sync (U49-U50) — dispatched fresh auditor | U49, U50 | `.gotm/audits/U51.md` | done | — |

### README intro hook (2026-06-12)

| ID | Title | Inputs | Output | Status | Audit |
|---|---|---|---|---|---|
| U52 | Add a catchy pain-point → "what if" intro hook to the README (neutral; above "The problem GOTM solves") | docs/01,04 | `README.md` | done | PASS-FINDINGS→.gotm/audits/U53.md |
| U53 | **Independent** audit of the README intro (U52) — neutrality, voice, render, links | U52 | `.gotm/audits/U53.md` | done | — |
| U54 | Close U53 LOW: reword the intro payoff so the stateless/stateful motif stays canonical at "What GOTM is" (was repeated 3× in ~65 lines) | U53 | `README.md` | done | — |

## Recent updates

- 2026-06-12: **Added a pain-point → "what if" intro hook to the README (U52-U54).** Neutral lead-in above "The problem GOTM solves": session context surviving a crash, an independent untainted-subagent audit, "done" = checked. Independent audit U53 → **PASS-FINDINGS**; the one LOW (stateless/stateful motif repeated 3× in ~65 lines) closed by U54 (reworded the intro payoff).
- 2026-06-12: **Synced the repo's own governance docs to the current discipline (U49-U51).** `.gotm/PROTOCOL.md` was behind its own template — brought up to the current protocol (Anti-drift safeguards, Resilience, Audit gates, reconcile step, `.gotm/` Layout note), instantiating `templates/PROTOCOL.md.template` with the framework's real mission + `../` links. Root `CLAUDE.md` gained the four Non-negotiables (frozen units · write-back · resilience/cold-start · audit independence). Independent audit U51 → **PASS** (one pre-existing LOW noted in `docs/04` prose, accepted). The meta-example now runs the full protocol it teaches.
- 2026-06-11: **Added a Mermaid orchestrator diagram to the README (U48).** Designed by a dispatched subagent, render-checked with `mmdc` (exit 0). One at-a-glance picture: stateless session loop (read+reconcile → act → write-back) around the stateful project file-set, subagent dispatch incl. the independent auditor → audit gate, and the human entering only via the ratification ladder.
- 2026-06-11: **Migrated the repo's own machinery into `.gotm/` (D18, U47).** PROTOCOL/LEDGER/DECISIONS/QUESTIONS/audits moved under `.gotm/`; deliverables (`docs/`, `prompts/`, `templates/`) stay at root; root `CLAUDE.md` is now a thin bridge into `.gotm/PROTOCOL.md`. The repo is now a live demonstration of the subfolder layout it recommends. Audit paths relocated `audits/…` → `.gotm/audits/…` (mechanical).
- 2026-06-11: **Concept docs rewritten from scratch → 5-chapter arc (D17, U38-U45).** Now that the framework is battle-tested: ch1 What GOTM is · ch2 Why agents need it · ch3 How the project carries the discipline · ch4 Keeping it honest (anti-drift + resilience + audit gates) · ch5 In practice. Renamed ch2/ch3 files to match titles (old files deleted). Refreshed prompts (session-start reconcile, subagent-dispatch independence) + README. Independent publication audit U46 → **PASS-FINDINGS** (HIGH 0 / MED 0 / LOW 1 cosmetic, accepted; UNVERIFIED Apache-section citation verified correct). docs/ now ~6,650w. Repo publication-ready.
- 2026-06-11: **U36 independent audit → PASS-FINDINGS** (HIGH 0 / MED 0 / LOW 1 → `.gotm/audits/U36.md`; dispatched fresh auditor, dogfooding the new 5-point checklist + three-way verdict — the `PASS-FINDINGS` state exercised itself). The one LOW (audit.md §4 label shorthand) closed by U37. U33-U35 stamped `Audit: PASS-FINDINGS`.
- 2026-06-11: **Audit-verdict refinement done (U33-U35).** D16 locked from updated `geniefy-v3` feedback (G11 + Appendix D): three-way verdict (`PASS`/`PASS-FINDINGS`/`FAIL`), a default 5-point checklist (existence/spec-match/cross-ref/consistency/decision-fidelity), and deferral-can't-outlast-the-code-gate.
- 2026-06-11: **U28 independent audit PASSED** (HIGH 0 / MED 0 / LOW 1 within tolerance → `.gotm/audits/U28.md`). Ran via a *dispatched fresh auditor* (not the authoring session), dogfooding the new audit gate; U20-U27 + U29-U32 stamped `Audit: PASS`. The one LOW (README word count) was fixed.
- 2026-06-11: **Audit-gate pass done (U29-U32).** D15 locked — audit independence is a hard rule + a consume-gate. Added an *Audit gates* section + audit-gate lint to `PROTOCOL.md.template`, an `Audit` column to `LEDGER.md.template`, an independence preamble + stamp step to `prompts/audit.md`, and strengthened docs/03 §6. Runtime (the `/gotm audit` command + header-aware hook) lives in the plugin (D12). U28 now run as an **independent dispatched audit** of U20-U27 + U29-U32 (no longer just deferred).
- 2026-06-11: **Feedback-integration pass done (U20-U27).** Folded `geniefy-v3` field feedback (G1-G10) into docs + templates: anti-drift safeguards, resilience (crash-safe ordering + session-start reconciliation), `.gotm/` layout option, governance-vs-frozen-outputs carve-out, off-mission convention, sanctioned audit deferral. D12-D14 locked. Runtime enforcement (the hook) folded into the `gotm` plugin, not here (D12). U28 mechanical audit **deferred to human review** (recorded, not skipped).
- 2026-05-30: **Rewrite shipped.** U17 meta-audit passed (HIGH 0 / MED 0 / LOW 3 within tolerance). U18 committed (`0f0933e`). U19 pushed to private GitHub. 19/19 units done. Q2 visibility flip remains open.
- 2026-05-30: U15 (README ~732w) and U16 (CONTRIBUTING ~470w) done. All concept + implementation units complete.
- 2026-05-30: Prompts phase closed (U13a-c done, 3 prompts ~1,500w). 13 old prompts deleted (U14). Active unit U15.
- 2026-05-30: Templates phase closed (U12a-e done, 5 templates ~1,200w). Old 5 templates deleted.
- 2026-05-30: Concept phase closed. Implementation phase opened with U5-U11 done in one batch.
- 2026-05-29: D9 locked — four-layer hierarchy demoted; five-primitive model adopted. Concept docs rewritten.
- 2026-05-27: Repo pushed to GitHub as private (predecessor framework state; under old model).
