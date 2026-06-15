---
project: gotm-framework-for-agentic-development
last_updated: 2026-06-15 (learning layer D20/U60-U63 audited; process-feedback check D21/U64 — L22 re-audit-dependents added, L15/L21/L23 already covered, U64 audit pending; plugin /gotm:learn + L22 → v2.5.0 unshipped; Q2 visibility still open)
---

# Project ledger

## Mission

Distill the GOTM discipline into a public-ready framework — concept docs, a project protocol, prompts, and templates — that any LLM practitioner can adopt to survive bounded-context agentic execution.

## Active unit

**(none active)** — this session's work is done and independently audited. Cross-project learning layer (D20, U60-U63 → PASS-FINDINGS/PASS) + GOTM core-process feedback check (D21, U64 → PASS-FINDINGS, 1 LOW accepted). L15/L21/L23 verified already-implemented; L22's re-audit-dependents added across both protocol templates + the meta-example + the plugin mirror. Plugin `/gotm:learn` + L22 = **v2.5.0, NOT yet pushed/published** (awaiting go). Open: the *consume* half of L1 + L2/L3 aggregation (future iteration); Q2 PRIVATE→PUBLIC visibility (standing). Per D19, per-unit auditing binds.

Latest: D20 locks the learning layer (project → user/harness → enterprise; one mergeable record + a generated index; confidence candidate→validated→core, no self-promotion past candidate, contradiction demotes). Producer shipped; *consume* + L2/L3 aggregation described, not shipped (platform bindings). Validated against the geniefy-v3 extraction (~23 lessons; scratch proof kept outside the repo). Prior arc: G12/G14/G13a (D19, U55-U59), 5-chapter docs (D17), `.gotm/` migration (D18), governance sync (U49-U51). Q2 (PRIVATE→PUBLIC visibility) remains the standing open ratification.

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

### G12/G14/G13a incorporation phase (2026-06-12)

> D19. Source: `geniefy-v3/docs/GOTM-FEEDBACK.md` G12 (audit cadence) · G14 (born-`in_progress`) · G13a (module+test grain). Paste-able discipline → deliverable templates + the meta-example's own protocol. U59 is the **final consolidated** audit; per-unit auditing (G12) binds from here.

| ID | Title | Inputs | Output | Status | Audit |
|---|---|---|---|---|---|
| U55 | `templates/PROTOCOL.md.template`: G12 cadence invariants (Audit gates) + G14 born-`in_progress` (Resilience) + G13a grain (Rule 2) | D19 | `templates/PROTOCOL.md.template` | done | PASS-FINDINGS→.gotm/audits/U59.md |
| U56 | `templates/LEDGER.md.template`: grain + cadence + born-`in_progress` conventions | D19 | `templates/LEDGER.md.template` | done | PASS-FINDINGS→.gotm/audits/U59.md |
| U57 | `prompts/audit.md`: one-report-per-unit + audit-promptly | D19 | `prompts/audit.md` | done | PASS-FINDINGS→.gotm/audits/U59.md |
| U58 | Sync meta-example's own `.gotm/PROTOCOL.md` to match (G12/G14/G13a) | D19, U55 | `.gotm/PROTOCOL.md` | done | PASS-FINDINGS→.gotm/audits/U59.md |
| U59 | **Independent** audit of U55-U58 (final consolidated audit; per-unit binds hereafter per D19) | U55-U58 | `.gotm/audits/U59.md` | done | — |

### Cross-project learning layer (2026-06-15)

> D20. Document the bottom-up learning layer + ship the *producing* half of L1 (the end-of-project retrospective + the LEARNINGS record/template). *Consume* + L2/L3 aggregation described, not shipped. The plugin mirrors the template/prompt and adds `/gotm:learn`. Validated against the geniefy-v3 extraction (a scratch proof kept outside the repo). Audits pending — dispatch per-unit (G12).

| ID | Title | Inputs | Output | Status | Audit |
|---|---|---|---|---|---|
| U60 | New ch6 — Learning across projects (3-level bottom-up flow; record + index + merge; confidence ladder) | D20 | `docs/06-learning-across-projects.md` | done | PASS-FINDINGS→.gotm/audits/U60.md |
| U61 | Draft `templates/LEARNINGS.md.template` — the learning-artifact scaffold (records + generated index + merge model) | D20 | `templates/LEARNINGS.md.template` | done | PASS-FINDINGS→.gotm/audits/U61.md |
| U62 | Draft `prompts/outcome-analysis.md` — the end-of-project retrospective that emits candidate records | D20 | `prompts/outcome-analysis.md` | done | PASS-FINDINGS→.gotm/audits/U62.md |
| U63 | README sync — ch6 in the chapter list, outcome-analysis in prompts, LEARNINGS in templates, tree counts | D20, U60-U62 | `README.md` | done | PASS→.gotm/audits/U63.md |

### GOTM core-process feedback check (2026-06-15)

> D21. Checked the geniefy outcome-analysis "Running GOTM itself" + tooling lessons (L15/L21/L22/L23) against the *current* protocol: **L15** (plugin hook restart), **L21** (audit cadence + independence), **L23** (size-to-loop + findings-become-units) are **already implemented** (G12/D19 + Resilience) — no change. Only **L22's re-audit-dependents** half was missing → added (D21). The meta-example's own `.gotm/PROTOCOL.md` was synced the same turn (living governance doc, in-bounds per the pre-edit carve-out).

| ID | Title | Inputs | Output | Status | Audit |
|---|---|---|---|---|---|
| U64 | `templates/PROTOCOL.md.template`: "a decision change can invalidate a prior pass" rule (Audit gates) + stale-by-decision reconciliation lint — closes the L22 gap | D21 | `templates/PROTOCOL.md.template` | done | PASS-FINDINGS→.gotm/audits/U64.md |

## Recent updates

- 2026-06-15: **GOTM core-process feedback check (D21, U64).** Checked the geniefy "Running GOTM itself" + tooling lessons against the *current* protocol: **L15** (hook restart), **L21** (audit cadence/independence), **L23** (size-to-loop + findings-become-units) are **already implemented** (G12/D19 + Resilience) — no change needed. Only **L22**'s "re-audit dependents when a decision is refined" half was missing → added as *Audit gates* → "a decision change can invalidate a prior pass" + a *stale-by-decision* reconciliation lint, in `templates/PROTOCOL.md.template` (U64) and the meta-example's own `.gotm/PROTOCOL.md` (governance sync, in-bounds). Plugin mirrored into its `templates/PROTOCOL.md.template`, folded into the unshipped v2.5.0. U64 independent audit → **PASS-FINDINGS** (0 HIGH / 0 MED / 1 LOW; zero drift across the three synced copies — verified byte-identical). The LOW is an optional `LEDGER.md.template` clarification that `Inputs` may cite decisions (the repo already does) — accepted/deferred, not a U64 defect.
- 2026-06-15: **Cross-project learning layer (D20, U60-U63).** Documented the bottom-up, three-level learning flow (project *consume*+*produce* → user/harness pool → enterprise traversable knowledge) as new ch6, and shipped the *producing* half of L1: `templates/LEARNINGS.md.template` (one mergeable record per learning + a generated index) and `prompts/outcome-analysis.md` (the end-of-project retrospective that reads `DECISIONS`/`audits`/`LEDGER` → candidate records). README synced (ch6, prompt, template, tree counts). Format: `claim` = merge key · appendable `evidence` · confidence `candidate→validated→core` (no self-promotion past candidate; contradiction demotes). *Consume* + L2/L3 aggregation described, not shipped (platform bindings, per D20). Validated against the geniefy-v3 extraction (~23 lessons; scratch proof outside the repo). Independent per-unit audits **passed** (U60/U61/U62 → PASS-FINDINGS, 0 HIGH / 0 MED / 2 LOW each — cosmetic, accepted; U63 → PASS) → `.gotm/audits/U60.md`–`U63.md`. Plugin mirror (`/gotm:learn`, v2.5.0) next.
- 2026-06-12: **Folded `geniefy-v3` feedback G12/G14/G13a (D19, U55-U58).** G12 audit-cadence invariants (one report per unit · own-report-only + `superseded by U<yy>` exception · audit promptly), G14 "a unit is born `pending`/`in_progress`, never `done`" (+ plugin hook deny-message hint), G13a "module+test = one unit" grain — into `templates/PROTOCOL.md.template`, `templates/LEDGER.md.template`, `prompts/audit.md`, and the meta-example's own `.gotm/PROTOCOL.md`. Declined G13b (P3). Plugin mirrors + ships **v2.4.0** (new marketplace PR). Transition: prior consolidated audits stand as history; per-unit auditing binds after U59. Independent audit **U59 → PASS-FINDINGS** (2 LOW; L1 gate-enumeration omission closed inline; L2 — the "covered-by" stamps — accepted as the sanctioned transitional consolidated audit).
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
