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

## D9 — Drop the four-layer hierarchy; adopt the five-primitive model

**Date:** 2026-05-29
**Scope:** framework
**Status:** locked (supersedes the load-bearing structure implied by D1-D7)

**Context.** Observed across multiple GOTM-orchestrated projects: the Goals/Objectives/Targets layers were filing labels — present in specs, absent from the actual decisions that moved work forward. The strategic decomposition was post-hoc; the real work happened at the Milestone layer. The framework's stated value (strategic hierarchy) and its actual mechanism (atomic units + ledger + foundation gate + audit) had drifted apart.

**Decision.** GOTM is reframed as a discipline for surviving bounded-context agentic execution, not as a strategic decomposition framework. The framework reduces to five primitives — mission, ledger, atomic unit, foundation gate, audit cycle — plus the ratification ladder. Hierarchy becomes optional grouping, not load-bearing structure. The acronym G-O-T-M is retained as a name but is no longer a structural claim.

**Consequences.** The four-layer hierarchy is removed from concept docs, prompts, and templates. Concept chapters `docs/01-06` deleted; replaced by three first-principles chapters at `docs/01-what-is-gotm.md`, `02-what-agents-are-missing.md`, `03-gotm-with-agents.md`. Prompts and templates require a full rewrite.

---

## D10 — `PROTOCOL.md` canonical; `CLAUDE.md` references it

**Date:** 2026-05-30
**Scope:** framework
**Status:** locked

**Context.** The reframe in D9 implies the discipline must live in the project filesystem, not in agent tooling. A single canonical protocol file is needed that every agent reads on session start. Two paths considered: a tool-specific name (e.g., `CLAUDE.md` as protocol) or a concept-pure name (`PROTOCOL.md`) with tool-specific files pointing to it.

**Decision.** `PROTOCOL.md` at project root is canonical. `CLAUDE.md` (and analogous files for other tools — `.cursorrules`, etc.) point to `PROTOCOL.md`. This keeps the protocol portable across tools and leaves `CLAUDE.md` free to carry tool-specific guidance that is not part of the discipline itself.

**Consequences.** Every project bootstrapped from this framework gets `PROTOCOL.md` at root. Tool-specific pointer files are minimal — a few lines naming the protocol.

---

## D11 — Keep the framework repo as a working meta-example

**Date:** 2026-05-30
**Scope:** framework
**Status:** locked

**Context.** The framework repo can either be pure documentation (just templates and prompts), or it can dogfood itself by maintaining its own `LEDGER.md`, `DECISIONS.md`, `QUESTIONS.md`, and `PROTOCOL.md` at the project root.

**Decision.** Keep the framework repo as a working meta-example. The repo's own files use the new model. Forkers see a working project, and bugs in the framework surface here first.

**Consequences.** The old `GOTM.md` + `STATUS.md` collapse into a single `LEDGER.md` at root. `decisions.md` is renamed `DECISIONS.md`; `OPEN_QUESTIONS.md` is renamed `QUESTIONS.md`. The `discovered/` directory (foundation outputs from the old build) is deleted; its content audited the old framework and is not relevant under the new model.

---

## D12 — Two repos: public-idea framework vs private runtime plugin

**Date:** 2026-06-11
**Scope:** framework
**Status:** locked

**Context.** Field feedback from running GOTM on a real software project (`geniefy-v3`) recommended shipping a `PreToolUse` enforcement hook "in the framework." That collides with this repo's stated scope (`CONTRIBUTING.md`: runtime enforcement is out of scope; "the discipline is paste-able prompts, not a runtime"). The author resolved it by naming the structure explicitly.

**Decision.** GOTM lives in **two repos with a deliberate boundary.** (1) This repo — `gotm-framework-for-agentic-development` — is the *idea*: concept docs, platform-neutral prompts, scaffold templates, publishable publicly. It stays prompts-not-a-runtime. (2) The `gotm` Claude Code plugin is the *runtime*: the `/gotm` bootstrap, the `.gotm/` layout, the immutability hook + `settings.json` wiring — private, internal-marketplace-bound. Runtime/enforcement bindings live in the plugin, never here.

**Consequences.** Conceptual feedback (paste-able discipline) folds into this repo's docs + templates; runtime feedback (the hook, harness wiring) folds only into the plugin. `CONTRIBUTING.md` is refined to point enforcement at adopter tooling rather than forbid it outright. This repo keeps its root layout and meta-example role (D11); the plugin defaults to `.gotm/`.

---

## D13 — Adopt anti-drift safeguards + resilience as paste-able discipline

**Date:** 2026-06-11
**Scope:** framework
**Status:** locked

**Context.** The original five rules stated *what* the discipline is but had no operational catch for the two ways it erodes — silent work (acting without writing back) and quiet edits (mutating a frozen artifact). Both relied on agent memory, the exact dependency GOTM exists to remove. A further gap (G10): the "no context loss" promise held only at clean turn-ends; a mid-turn crash or cold restart with no resume could leave on-disk state inconsistent with the ledger, with no procedure to heal it.

**Decision.** Add an **Anti-drift safeguards** section (pre-edit check, write-back gate, done-means-written, turn-end self-check) and a **Resilience** section (transcript independence, crash-safe write ordering, size-to-the-loop, session-start reconciliation) to `PROTOCOL.md.template`, plus a session-start reconciliation step and the governance-docs-vs-frozen-outputs carve-out. All as paste-able prose. Mechanical *enforcement* of the pre-edit check is described as an option that lives in adopter tooling (per D12), not shipped here.

**Consequences.** Concept chapters gain two gaps (docs/02 §8–§9) and one solution section (docs/03 §7). The bar for the core promise is restated as "no *unrecoverable* context loss" — the achievable guarantee under accidental ends.

---

## D14 — Document the `.gotm/` subfolder layout as a first-class option

**Date:** 2026-06-11
**Scope:** framework
**Status:** locked

**Context.** The bootstrap dropped the file-set at the project root. For software/multi-asset projects that produce many files, mixing orchestration with deliverables clutters the root. But cross-session continuity depends on a root-level session-context file (e.g. `CLAUDE.md`) auto-loading — moving the whole set into a subfolder silently breaks that.

**Decision.** Document two layouts in the framework: *root* (default; writing/research) and *subfolder* (`.gotm/`; software/multi-asset). For the subfolder layout, require a thin pointer file kept at the root so the tool's auto-load still works; call out the silent-break failure mode. The framework states this tool-agnostically; the plugin makes `.gotm/` its default with a concrete root `CLAUDE.md` bridge.

**Consequences.** `PROTOCOL.md.template` gains a Layout note; README quickstart and repo-tree mention the subfolder option. No change to this repo's own (root) layout.

---

<!-- Append new decisions below this line. -->

