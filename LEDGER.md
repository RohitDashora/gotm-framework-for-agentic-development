---
project: gotm-framework-for-agentic-development
last_updated: 2026-05-30 (rewrite complete — 16/16 units done; ready for push or meta-audit)
---

# Project ledger

## Mission

Distill the GOTM discipline into a public-ready framework — concept docs, a project protocol, prompts, and templates — that any LLM practitioner can adopt to survive bounded-context agentic execution.

## Active unit

**U18** — Commit the rewrite (audit passed at HIGH 0 / MED 0 / LOW 3, all within tolerance; no fix units required).

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
| U17 | Meta-validation audit of the rewrite — existence + structure across all claimed-done units (U1-U16) | LEDGER.md as oracle, all U1-U16 outputs as targets, `prompts/audit.md` for shape | `audits/U17.md` (HIGH 0 / MED 0 / LOW 3 within tolerance / UNVERIFIED 0; recommendation: proceed to commit; out-of-kind notes: empty drafts/ cleaned, .DS_Store gitignored) | done |
| U18 | Commit the rewrite to git (single commit; message captures the reframe) | U17 verdict | git commit on `main` | pending |
| U19 | Push the rewrite to GitHub (visibility stays PRIVATE) | U18 | remote `main` updated | pending |

## Recent updates

- 2026-05-30: **Rewrite complete.** U15 (README ~732w) and U16 (CONTRIBUTING ~470w) done. All 16 units complete. Ready for meta-audit, commit, push, or visibility flip — each is a discrete next unit awaiting practitioner direction.
- 2026-05-30: Prompts phase closed (U13a-c done, 3 prompts ~1,500w). 13 old prompts deleted (U14). Active unit U15.
- 2026-05-30: Templates phase closed (U12a-e done, 5 templates ~1,200w). Old 5 templates deleted.
- 2026-05-30: Concept phase closed. Implementation phase opened with U5-U11 done in one batch.
- 2026-05-29: D9 locked — four-layer hierarchy demoted; five-primitive model adopted. Concept docs rewritten.
- 2026-05-27: Repo pushed to GitHub as private (predecessor framework state; under old model).
