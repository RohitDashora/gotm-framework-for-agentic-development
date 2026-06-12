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

## D15 — Audit independence is a hard rule; add a consume-gate to the ledger

**Date:** 2026-06-11
**Scope:** framework
**Status:** locked

**Context.** Rule 4 ("audit before downstream consumes") named the right idea, but independence lived only in prose (docs/02 §5, one PROTOCOL dispatch line) and was never operationalized: a working agent could self-audit in its own session, reproducing its own blind spots. There was no per-unit audit state, so `done` (output exists) was indistinguishable from "independently checked," and nothing stopped a downstream unit from consuming un-audited work. Field ask: auditors must be a *different* agent than the worker for a fair assessment.

**Decision.** (1) **Independence is non-negotiable** — an audit is valid only if produced by a context that did not author the unit; it is dispatched as a fresh auditor subagent that receives only the target + oracle + `prompts/audit.md`, never the authoring transcript. (2) Add an **`Audit` column** to the ledger schema: `—` / `pending` / `deferred→U<n>` / `PASS→audits/U<id>.md` / `FAIL→audits/U<id>.md`. (3) **Gate:** a downstream unit consumes an input only when that input is `PASS` or `deferred→U<n>` (follow-up present). Findings become new fix units; a `FAIL` blocks downstream until a re-audit passes. The framework states this as paste-able discipline; the runtime that constructs the independent auditor, and a header-aware enforcement hook, live in the plugin (D12).

**Consequences.** `PROTOCOL.md.template` gains an *Audit gates* section + an audit-gate lint in session-start reconciliation; `LEDGER.md.template` gains the column; `prompts/audit.md` gains an independence preamble + a stamp-the-cell step; docs/03 §6 is strengthened. In the plugin: a `/gotm audit <Uxx>` command dispatches the independent auditor, and the immutability hook is made header-aware so the new column doesn't shift cells and break the freeze.

---

## D16 — Audit verdicts are three-way; a default 5-point checklist; deferral can't outlast the code gate

**Date:** 2026-06-11
**Scope:** framework
**Status:** locked

**Context.** D15 operationalized audit gates with a binary `PASS`/`FAIL`. Updated `geniefy-v3` feedback (G11 + Appendix D) refined three points: a three-way verdict (`PASS` / `PASS-WITH-FINDINGS` / `FAIL`) so "clean" is distinct from "passed but has tracked follow-ups"; an explicit default checklist so the auditor isn't improvising what to check; and a tightening of deferral so it can't quietly extend past the point where code consumes the design.

**Decision.** (1) Add **`PASS-FINDINGS`** as a third verdict / `Audit` value — passed and consumable, but carrying MEDIUM/LOW findings that become tracked non-blocking follow-on units (HIGH ⇒ FAIL; MEDIUM/LOW-only ⇒ PASS-FINDINGS; clean ⇒ PASS); the gate treats `PASS` and `PASS-FINDINGS` alike for consumption. (2) Adopt a **default 5-point checklist** in `prompts/audit.md`: existence · spec match · cross-reference integrity · internal consistency · decision fidelity. (3) **Deferral** is allowed during human review but the independent audit must run **before any code/build unit consumes the design**.

**Consequences.** Updated `PROTOCOL.md.template` (Audit gates), `LEDGER.md.template` (Audit vocab), and `prompts/audit.md` (checklist + verdict + stamp). The plugin mirrors these and updates its `/gotm audit` stamp logic + `CLAUDE.md` bridge bullet. Kept the `audits/<Uxx>.md` naming (not Appendix D's `audit-NNN.md`) for consistency with existing audit files. The "consider later" deterministic consume-gate hook (G11) remains a documented future option, not built — a hard edit-time block on consumption is fragile.

---

## D17 — Rewrite the concept docs from scratch into a 5-chapter arc

**Date:** 2026-06-11
**Scope:** framework
**Status:** locked

**Context.** The three concept chapters predated real use. The hardening that running GOTM for real produced — anti-drift safeguards, resilience, audit gates (D13–D16) — had been folded into the docs as bolt-on sections (§7–§9 of chapter 3). Now that the framework is battle-tested, a from-scratch rewrite was warranted: give the operational discipline first-class treatment and add a practitioner-facing chapter.

**Decision.** Rewrite `docs/` as **five** chapters: (1) What GOTM is — five primitives + ratification ladder; (2) Why agents need it — the gaps, including the battle-tested ones; (3) How the project carries the discipline — the mechanism; (4) Keeping it honest under real conditions — anti-drift + resilience + audit gates as a first-class chapter; (5) In practice — layouts, the loop end to end, a worked software example. Rename the middle two files to match their new titles (`02-what-agents-are-missing.md` → `02-why-agents-need-it.md`; `03-gotm-with-agents.md` → `03-how-the-project-carries-it.md`) and add `04-keeping-it-honest.md` + `05-in-practice.md`. Refresh `prompts/` (session-start reconcile step; subagent-dispatch audit-independence note) and `README.md` for consistency. Keep the docs platform-neutral; bootstrap/runtime detail stays in adopter tooling.

**Consequences.** `docs/` is now five chapters (~6,650 words). The old chapter files are deleted; historical ledger rows (U2, U3, U20, U21, U32) and decision D9 still name them — that is append-only history and is left intact, with the rename documented here. The rewrite was checked by an independent publication audit (U46 → PASS-FINDINGS; one accepted cosmetic LOW on a filename slug). `README.md` chapter list, word count, and prompt descriptions updated.

---

## D18 — Migrate the repo's own machinery into `.gotm/` (dogfood the subfolder layout)

**Date:** 2026-06-11
**Scope:** framework
**Status:** locked

**Context.** The repo's own GOTM files lived at the root (a legacy of D11, before the `.gotm/` layout existed). The framework now documents `.gotm/` as the recommended subfolder layout (D14) and ships a plugin that defaults to it. For a repo about to be published, a reader seeing the machinery strewn across the root — while the docs tout `.gotm/` — reads as not eating our own cooking. Root layout is a *sanctioned* choice for a writing/research project, but the showcase value of conforming won out.

**Decision.** Move `PROTOCOL.md`, `LEDGER.md`, `DECISIONS.md`, `QUESTIONS.md`, and `audits/` into `.gotm/`. Keep the deliverables at the root (`docs/`, `prompts/`, `templates/`, `README.md`, `CONTRIBUTING.md`, `LICENSE`). Convert the root `CLAUDE.md` into a thin bridge that points into `.gotm/PROTOCOL.md` (so the discipline still auto-loads at session start — the exact pattern from D14 / ch5). Update all references in `README.md`, `CONTRIBUTING.md`, and this file-set to the `.gotm/` paths.

**Consequences.** The repo is now a live demonstration of the `.gotm/` subfolder layout. Audit-output paths in `LEDGER.md` were relocated `audits/…` → `.gotm/audits/…` — a mechanical path relocation, not a substantive revision of any unit's content or verdict (the immutability rule governs *what a unit produced and how it was judged*, not where a documented restructure later moves the file). Generic `audits/U<id>.md` references in the templates and in prior decision text stay root-relative, since those describe the neutral default layout, not this repo's instance.

---

## D19 — Audit cadence (G12), born-`in_progress` (G14), module+test grain (G13a)

**Date:** 2026-06-12
**Scope:** framework
**Status:** locked

**Context.** A long autonomous run on `geniefy-v3` surfaced three more gaps even with the audit gates (D15/D16) in place. **G12:** the gate's *spirit* eroded — done units sat `Audit: pending` while downstream built, audits got batched, two units shared one report, four were stamped "covered by the module's audit." **G14:** registering a follow-on unit as `done` *before* writing its output trips the immutability hook (it freezes done outputs) and locks you out of your own file. **G13a:** the frozen-file + atomicity rules make a module+test pair feel like two units.

**Decision.** Adopt three additions as paste-able discipline. **G12 cadence (three invariants):** one audit dispatch + one `audits/<Uxx>.md` per unit (no multi-unit reports); the `Audit` cell comes only from the unit's *own* report (sole exception `superseded by U<yy>`); audit promptly — right after a unit goes `done`, before the next. **G14:** a new unit is born `pending`/`in_progress`, never `done` — flip to `done` only after its output exists (stated in Resilience + Anti-drift; the plugin hook's deny message now names this fix). **G13a:** a module + its test file count as one unit (atomicity is one *deliverable*, not one file). Declined **G13b** (the speculative "cleanup unit" pattern + immutability-hook companion) — P3, only if findings-sweeps recur.

**Consequences.** Updated `templates/PROTOCOL.md.template`, `templates/LEDGER.md.template`, `prompts/audit.md`, and the repo's own `.gotm/PROTOCOL.md`. The plugin mirrors these + the hook-message hint and ships as **v2.4.0** (new marketplace PR). **Transition note:** G12 ("one report per unit") means this repo's prior *consolidated* audits (U28 covered U20–U32; U46 covered U39–U45; U51, U53) stand as history; per-unit auditing binds from here. This pass's own audit (below) is the final consolidated one.

---

<!-- Append new decisions below this line. -->

