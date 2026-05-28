# Decisions — gotm-framework-for-agentic-development

> Append-only ADR ledger. Never edit a prior entry. If a decision is reversed, append a new D# with `Status: superseded by D<n>`.

---

## D1 — Adopt GOTM for this project (self-referential)

**Date:** 2026-05-27
**GOTM node:** project
**Status:** locked

**Context.** This is a distillation project of moderate complexity — ~16 Milestones, foundation discovery before drafting, multi-subagent dispatch. The Module 1 fit-test (≥5 passes, multi-pass shape, evidence-heavy synthesis) clearly clears for GOTM.

**Decision.** Run this as a GOTM-orchestrated project. Self-referential by design: a public GOTM repo, built with the GOTM discipline.

**Consequences.** Discipline rules R1-R11 binding; D11 ratification ladder applies; outputs are tracked atomically; foundation precedes drafts.

---

## D2 — Audience: LLM practitioners running complex multi-pass work

**Date:** 2026-05-27
**GOTM node:** project
**Status:** locked (per user ratified question)

**Context.** Public-facing artifact; needs explicit audience choice. User picked "LLM practitioners running complex multi-pass work" over "agent/tooling builders specifically" and "broader open-source audience."

**Decision.** README, docs, and prompts target practitioners — engineers, consultants, researchers, SAs using any LLM to drive multi-week deliverables. Examples (when authored) are practitioner-flavored. The meta-prompts directory (deferred to Phase 2) would be the headliner if the audience were tooling-builders; this MVP keeps it practitioner-first.

**Consequences.** Voice is practitioner-friendly — concrete, prescriptive, not theoretical. Cold-readers from outside this audience may find some sections too operational; that's acceptable for the MVP.

---

## D3 — Repo name: `gotm-framework-for-agentic-development`

**Date:** 2026-05-27
**GOTM node:** project
**Status:** locked (user-chosen; "development" spelling confirmed standard)

**Context.** Original fe-gotm plugin name drops the `fe-` prefix for public release. User chose the longer descriptive name over the short `gotm`.

**Decision.** Folder name and eventual GitHub repo name: `gotm-framework-for-agentic-development`. The framework name in prose stays simply "GOTM" (Goals · Objectives · Targets · Milestones); the repo name positions GOTM as a framework specifically for agent-driven development.

**Consequences.** README headline says "GOTM" with the long name as the repo-slug. All internal refs in prose use "GOTM" or "the GOTM discipline."

---

## D4 — License: MIT (default, user may override)

**Date:** 2026-05-27
**GOTM node:** project
**Status:** locked-pending-override

**Context.** User did not explicitly choose; my Q3 default was MIT. Most permissive; encourages adaptation; no compliance overhead for adopters.

**Decision.** MIT for both code/prompts and docs. If user prefers Apache 2.0 + CC-BY-SA at any point pre-publication, append a D-entry that supersedes this one.

**Consequences.** LICENSE file at top-level. CONTRIBUTING notes the MIT terms.

---

## D5 — Dispatch policy: sequential phase-by-phase with 4 checkpoints

**Date:** 2026-05-27
**GOTM node:** project
**Status:** locked (per user ratified question)

**Context.** User picked "Checkpoint after each phase" over "checkpoint only after docs" and "no checkpoints."

**Decision.** Sequential dispatch one phase at a time. Checkpoints at:
- After M2 (foundation map) — checkpoint #1
- After M8 (docs complete) — checkpoint #2; voice/tone for public version is locked here
- After M13 (prompts complete) — checkpoint #3
- After M16 (wrap complete) — final review

**Consequences.** Lower throughput than parallel dispatch but higher course-correction opportunity. Module-equivalent reviews between phases let the user catch tone drift before it cascades.

---

## D6 — MVP scope: docs + prompts + templates only; meta-prompts deferred

**Date:** 2026-05-27
**GOTM node:** project
**Status:** locked (per user ratified question)

**Context.** User picked "MVP: concept + prompts only" over "MVP + meta-prompts" and "Full distillation including playbook curriculum."

**Decision.** Day-one repo contents:
- Top-level: `README.md`, `LICENSE`, `CONTRIBUTING.md`
- `docs/` — 6 concept chapters
- `prompts/` — 13 standalone prompt files
- `templates/` — 5 platform-neutral templates

Deferred to Phase 2 (post-MVP):
- `meta/` — meta-prompts that GENERATE per-platform skill files (Claude Code, Cursor, Cline, ChatGPT, raw API)
- `examples/` — anonymized worked-example excerpts

Deferred to Phase 3:
- GitHub Pages docs site
- Versioning / release model

**Consequences.** Smallest day-one footprint; ships the concept publicly without committing to ongoing maintenance of platform-specific generators. User can opt into Phase 2 once the MVP is shipped and validated.

---

## D7 — Prompts: truly platform-neutral

**Date:** 2026-05-27
**GOTM node:** project
**Status:** locked (per user ratified question)

**Context.** User picked "Truly platform-neutral" over "Claude-flavored with portability notes" and "Multiple parallel versions per platform."

**Decision.** Every prompt file in `prompts/` is pure markdown text a practitioner could paste into any LLM (ChatGPT, Claude API, Cursor, Cline, Continue, raw chat) and have it work. No slash-commands; no Claude Code frontmatter; no agent-framework-specific assumptions.

**Consequences.** Some translation from fe-gotm's SKILL.md syntax during distillation. The prompts read as standalone protocols rather than as commands in a specific tool.

---

## D8 — License: Apache 2.0 (supersedes D4)

**Date:** 2026-05-27
**GOTM node:** project
**Status:** locked (per user ratified question at checkpoint #3)

**Context.** D4 set MIT as default with explicit `locked-pending-override` status. At checkpoint #3 (prompts phase complete; M16 LICENSE file approaching) the user picked Apache 2.0 over MIT and over MIT-prompts/CC-BY-SA-docs.

**Decision.** Apache 2.0 for the entire repo — code, prompts, templates, and docs. D4 is superseded. M16 emits `LICENSE` as the verbatim Apache 2.0 text. `CONTRIBUTING.md` references the Apache 2.0 terms and the explicit patent grant.

**Consequences.** Adopters get an explicit patent grant. Adopters must preserve the LICENSE and any NOTICE file (a NOTICE is not strictly required for an originating work but is conventional). Header SPDX tags optional but recommended for any future code files. The MIT default mentioned in `docs/01-why.md` or any prompt frontmatter must be updated; sweep needed in M14-M16.

---

<!-- Append new decisions below this line. -->

