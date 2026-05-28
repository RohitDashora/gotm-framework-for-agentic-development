---
title: "gotm-framework-for-agentic-development — GOTM (Goals · Objectives · Targets · Milestones)"
owner: Rohit Dashora
created: 2026-05-27
last_updated: 2026-05-27 (**🎯 MVP COMPLETE + AUDITED**; M17 ✅ verdict: MVP passes — HIGH 0 / MEDIUM 0 / LOW 2 (fixed inline) / UNVERIFIED 1 (frontmatter-shape variation, intentional); ready for Q2 push decision)
shape: g-o-t-m
target_style: deliverable
status: active
delivery_anchor: Public GitHub repo (timeline TBD by user)
mvp_target_file_count: 27
self_referential: true
---

# GOTM — gotm-framework-for-agentic-development

**Read this first.** Every new session resumes here. No in-chat planning — all plans land here. Discovery expands this ledger.

This project is **self-referential**: a public open-source distillation of the GOTM discipline, built USING the GOTM discipline. The discipline at v1.3 (the canonical fe-gotm source + the playbook curriculum) ships forward as a platform-neutral repo any LLM practitioner can use.

---

## Mission (one sentence)

Distill the GOTM discipline from the private fe-gotm plugin + gotm-playbook curriculum into a platform-neutral public repo of concept docs + standalone prompts + templates (**27 target files** across docs/ + prompts/ + templates/ + top-level), so any LLM practitioner running complex multi-pass work can adopt the framework with their tool of choice.

---

## Discipline rules (binding for every Milestone execution)

The 11 canonical R-rules from `fe-gotm:resources/discipline.md` v1.3, including the ratification ladder in R11:

1. GOTM.md is the single orchestration ledger — no in-chat planning.
2. Atomic milestones — one M = one execution pass = one output file (R2 tight-cluster exception for `init`-style scaffolds).
3. M = max context unit — read only the listed Inputs; carry nothing across Ms.
4. Foundation before drafts — drafts blocked until High/Med gaps closed.
5. Ledger updates pair with file edits — same turn, not later.
6. Chat is tight status — 1–2 sentences, ledger-referenced.
7. Temp docs liberally — write to the folder, not working memory.
8. Sub-numbering preserves atomicity — M1a, M1b each get their own row.
9. No ID recycling — sunset with strikethrough; never reuse.
10. Subagent delegation uses the prescribed prompt template — Inputs only.
11. The ledger expands as we discover — write new scope BEFORE acting. **Ratification ladder per D11 below:** Goal → OPEN_QUESTIONS; Objective → agent discretion; Target/Milestone → atomic.

---

## Project anchors (locked decisions)

- **Audience:** LLM practitioners running complex multi-pass work (engineers, consultants, researchers, SAs using any LLM).
- **Shape:** g-o-t-m.
- **Target style:** deliverable (each Target names a final public-repo file or folder).
- **Substrate:** Markdown, platform-neutral.
- **Repo name:** `gotm-framework-for-agentic-development`.
- **License:** MIT (default; user may override).
- **Source plugins:** `/Users/rohit.dashora/fe-vibe/fe-gotm/` (v1.3) and `/Users/rohit.dashora/fe-vibe/gotm-playbook/` (v1.3 — 8 Os, 68 Ms shipped).
- **Anonymization:** strip all internal references (Databricks, Epsilon, Publicis, customer names, employee names, fe-vibe paths). Generic placeholders only.
- **Voice:** match the gotm-playbook's locked voice profile (per `discovered/foundation-inventory.md §5` in gotm-playbook).
- **Dispatch policy (D5):** sequential, one phase at a time, checkpoint after each phase.

See [`decisions.md`](decisions.md) for the locked-decision ledger.

---

## What this project is NOT

- Not a fork of fe-gotm — it's a public distillation, smaller and platform-neutral.
- Not the full playbook curriculum — that's ~45K words; the MVP docs are ~15-20K.
- Not Claude Code-specific — strips slash-command syntax, mode-dispatch frontmatter, plugin-system assumptions.
- Not a marketing piece — direct, prescriptive, fit-test honest.
- Not finished day-one — meta-prompts (Phase 2) and examples (Phase 3) come later if user opts in.

---

## Goals → Objectives → Targets → Milestones

### G1 — Ship a public GOTM framework that any LLM practitioner can use to run complex multi-pass work, with their tool of choice.

Done means: the `gotm-framework-for-agentic-development` repo is ready to push to public GitHub. A reader who has never heard of GOTM can land on the README, read the 60-second pitch, choose to adopt, and have everything they need (concept docs + prompts they paste into their LLM + templates they fork) to start their first GOTM project.

---

### O1 — Foundation: source-to-target mapping locked

> Before any distillation drafting, name which playbook/plugin source feeds which public-repo file, what needs anonymization, what's lift vs rewrite vs new authoring.

#### T1 — `discovered/source-to-target-map.md`

| ID | Title | Inputs | Output | Status | Priority |
|---|---|---|---|---|---|
| M1 | Scaffold the project: 4 ledger files + folder structure (R2 tight-cluster) | this project's brief (user's 4 answered questions + recommended structure) | 4 ledger files + 5 sub-folders | **done 2026-05-27** | High |
| M2 | Source-to-target mapping + anonymization audit: for each of the **27** public-repo files (corrected from ~17 estimate), name source(s), classify lift/rewrite/new, flag anonymization needs | `fe-gotm/` v1.3, `gotm-playbook/` v1.3 Modules 0-7 published READMEs, foundation-inventory §5-§6, decisions.md D1-D7 | `discovered/source-to-target-map.md` (1791 words; 27 targets covered; **6 lift / 14 rewrite / 7 new authoring**; **5 high-risk / 8 med-risk / 14 low-risk** anonymization; 4 gaps surfaced) | **done 2026-05-27** | High |

---

### O2 — Concept docs distilled (LLM-agnostic)

> Six docs/*.md chapters distilling the playbook's canonical teaching into platform-neutral prose. Audience: a practitioner who picks up this repo cold.

#### T2 — `docs/01-why.md`, `docs/02-hierarchy.md`, `docs/03-discipline-rules.md`, `docs/04-modes.md`, `docs/05-audit-family.md`, `docs/06-archetypes.md`

| ID | Title | Inputs | Output | Status | Priority |
|---|---|---|---|---|---|
| M3 | docs/01-why.md — Why GOTM exists; failure modes; foundational principles; fit-test; comparison to other frameworks | M2 output, gotm-playbook/01-theory Ch 1.1+1.2+1.3+1.5, foundation-inventory §5 voice | `docs/01-why.md` (2353 words; voice PASS: 0 FPS, 0 FPP, 0 banned, 0 internal; vendor names contained to §5; 3 archetypes past-tense; voice-lock baseline established) | **done 2026-05-27** | High |
| M4 | docs/02-hierarchy.md — G/O/T/M layers; shapes; target styles; outcome-shaped Os; layer disambiguation heuristics | M2, M3 voice-lock, gotm-playbook/02-anatomy Ch 2.1, gotm-playbook/07-lessons Ch 7.2 §7.2.5 | `docs/02-hierarchy.md` (2299 words; voice PASS: 0 FPS, 0 FPP, 0 banned, 0 internal, 0 vendor names; all 9 sections + 4 H3 disambiguation subs; pitfall callout; generic project examples throughout) | **done 2026-05-27** | High |
| M5 | docs/03-discipline-rules.md — R1-R11 full catalog + ratification ladder | M2, M3+M4 voice/cross-ref, gotm-playbook Ch 2.5 + Ch 7.1 + Ch 7.5 | `docs/03-discipline-rules.md` (3068 words; voice PASS; 11/11 R-rules with 4-block structure; R2/R3/R4/R11 extra **In practice.** paragraphs; ratification-ladder 4-row table embedded in R11; §13 R12+ extensibility; §14 four compound failures; FPP=0 in authorial voice — 3 mentions all in canonical titles or quoted strings) | **done 2026-05-27** | High |
| M6 | docs/04-modes.md — 8 modes with 5-block per-mode structure | M2, prior docs voice/cross-ref, fe-gotm/SKILL.md v1.3 | `docs/04-modes.md` (2686 words; voice PASS: 0 FPS, 0 FPP, 0 banned, 0 internal, 0 vendor names; 8/8 modes; mode-dispatch table; workflow integration + boundaries + pitfall) | **done 2026-05-27** | High |
| M7 | docs/05-audit-family.md — Multi-kind audits, severity tiers, -v2 re-run, execution-vs-audit-agent | M2, prior docs (M3-M6 voice/cross-ref), gotm-playbook Ch 7.4+7.5+6.3 | `docs/05-audit-family.md` (2163 words; voice PASS: 0 FPS, 0 FPP, 0 banned, 0 internal, 0 vendor names; 8/8 audit kinds; 4-tier severity universal; 6-row execution-vs-audit table; -v2 vignette past-tense; standard pitfall format) | **done 2026-05-27** | High |
| M8 | docs/06-archetypes.md — 4 archetypes with 9-block per-archetype structure; HIGHEST anon risk per M2 | M2, prior docs voice/cross-ref, gotm-playbook/03-patterns/README.md (Module 3) | `docs/06-archetypes.md` (2542 words; voice PASS: 0 FPS, 0 banned, 0 vendor names; **anon check 0 hits on every banned term** — Acme/Databricks/AWS/Azure/GCP/S3/Snowflake/Epsilon/Publicis/fe-vibe/fe-gotm/Sammie/Rohit all 0; 4/4 archetypes with 9-block structure; rubric table + comparison table; straddle-cases; standard pitfall) | **done 2026-05-27** | High |

---

### O3 — Prompts: standalone, platform-neutral

> Each prompt is a markdown file a practitioner can paste into ChatGPT, Cursor, Claude API, Cline, etc. and have a working GOTM mode.

#### T3 — `prompts/plan.md`, `prompts/init.md`, `prompts/run.md`, `prompts/audit-*.md` (8 audit kinds), `prompts/subagent-execution.md`, `prompts/subagent-audit.md`

| ID | Title | Inputs | Output | Status | Priority |
|---|---|---|---|---|---|
| M9 | prompts/plan.md — ask→hierarchy decomposition (template-setter) | M2, docs/01-06, fe-gotm/SKILL.md `plan` mode | `prompts/plan.md` (1592 words; structural template LOCKED: practitioner-framing + `## Paste this into your LLM` divider + 8 H2 LLM sections; voice PASS — 0 banned, 0 exclam, R2/R4/R11 cited by number; anonymized example) | **done 2026-05-27** | High |
| M10 | prompts/init.md — formalize ratified plan into 5 scaffold files | M9 (template), docs/02-hierarchy.md, docs/04-modes.md, fe-gotm/SKILL.md `init` mode | `prompts/init.md` (1797 words; 8 H2 LLM sections match M9; R1/R2/R5/R8/R11 cited; T1.1/T2.1 IDs present; 5 fenced scaffolds with 4-backtick outer fences — RG3 bug avoided; voice PASS — 0 banned, 0 FPP, 0 vendor names; anonymized example `cloud-migration-briefing`) | **done 2026-05-27** | High |
| M11 | prompts/run.md — autonomous orchestration loop | M9 (template), M10, docs/04-modes.md, docs/03-discipline-rules.md R1/R2/R5/R10/R11, fe-gotm/SKILL.md `run` mode | `prompts/run.md` (1761 words; 8 H2 LLM sections; R1/R2/R5/R10/R11 cited; 7-step loop explicit; 4-row ratification table; RG3 nested-fence handled via 4-backtick outer; voice PASS — 0 banned, 0 FPP, 0 emojis, 0 exclam; `cloud-migration-briefing` anonymized example) | **done 2026-05-27** | High |
| M12 | prompts/audit-* (8 files) R2 tight-cluster | M9-M11 (template), docs/05-audit-family.md, fe-gotm/SKILL.md audit family table | 8 files: audit-ledger-shape (1212w) / audit-content-claim (1166w) / audit-foundation-files (1113w) / audit-code-artifact (1110w) / audit-ui-render (1135w) / audit-source-fidelity (1155w) / audit-density (1131w) / audit-completion-verification (1218w); total 9240w; severity-tier scheme identical across all 8; §3 differentiation verified per kind; 0 nested 3-backticks; voice PASS across cluster | **done 2026-05-27** | High |
| M13 | prompts/subagent-execution.md + subagent-audit.md R2 tight-cluster (RG3 fix) | M9-M12, docs/03-discipline-rules.md R10, fe-gotm subagent-prompt sources | 2 files: subagent-execution.md (1558w) + subagent-audit.md (1666w); both 8 H2 LLM sections matching M9-M12; **RG3 verified clean** via line-by-line fence scan (4-tick outer / 3-tick inner pattern at specific line numbers); R10 cited multiple times; audit-prompt embedding mechanism specified in §2 + §6; severity tiers in subagent-audit.md identical to docs/05-audit-family.md; anonymized `cloud-migration-briefing` example carried | **done 2026-05-27** | High |

---

### O4 — Templates: platform-neutral, fork-ready

> Five canonical ledger files a practitioner forks into their own project folder.

#### T4 — `templates/GOTM.md`, `templates/STATUS.md`, `templates/decisions.md`, `templates/OPEN_QUESTIONS.md`, `templates/README.md`

| ID | Title | Inputs | Output | Status | Priority |
|---|---|---|---|---|---|
| M14 | templates/*.md R2 tight-cluster — 5 platform-neutral scaffold files | M2, M9-M13, docs/02-hierarchy.md, fe-gotm/templates | 5 files: GOTM.md.template (843w) / STATUS.md.template (500w) / decisions.md.template (292w) / OPEN_QUESTIONS.md.template (237w) / README.md.template (378w); 2250w total; init-emission match verified file-by-file; placeholders `<...>` throughout; cross-refs verified; Apache 2.0 license ref per D8; voice PASS — 0 banned, 0 emojis, 0 vendor names, 0 internal refs | **done 2026-05-27** | High |

---

### O5 — Wrapping: public README + LICENSE + CONTRIBUTING

> The artifacts a reader encounters first when they land on the public repo.

#### T5 — Top-level `README.md`, `LICENSE`, `CONTRIBUTING.md`

| ID | Title | Inputs | Output | Status | Priority |
|---|---|---|---|---|---|
| M15 | Top-level README.md — repo front-door | docs/01-why.md, docs/02-hierarchy.md, prompts/plan.md, templates/README.md.template, decisions.md, GOTM.md | `README.md` (1107w; vanishing-plan hook cited by name + 2 sibling archetypes; 11 sections; 5-step quickstart; vendor-name exception used 1x in §What's-in-this-repo; voice PASS — 0 banned, 0 FPP, 0 emojis, 0 exclam; 0 internal refs; 0 specific cloud vendor names) | **done 2026-05-27** | High |
| M16 | LICENSE + CONTRIBUTING.md — R2 tight-cluster: Apache 2.0 LICENSE per D8 + brief CONTRIBUTING | D8, prior repo state | `LICENSE` (11,409 chars verbatim Apache 2.0; 9 numbered sections + APPENDIX + 2026 copyright) + `CONTRIBUTING.md` (496w; 6 sections; patent-grant section explicit; no-CLA stated; voice PASS — 0 banned, 0 internal refs, 0 vendor names) | **done 2026-05-27** | Med |
| M17 | Meta-validation audit (post-MVP): completion-verification across all 16 Ms using project's own audit prompt | GOTM.md + 27 target files + prompts/audit-completion-verification.md + prompts/subagent-audit.md | `discovered/audit-M17-completion-verification.md` (5.8KB; HIGH: 0, MEDIUM: 0, LOW: 2 (M6/M8 stale word counts — FIXED inline as M17a/b ledger edits), UNVERIFIED: 1 (frontmatter shape variation — intentional per file type); 3 out-of-kind audit candidates noted for future Ms: content-claim, source-fidelity, ledger-shape; **VERDICT: MVP passes — proceed to push**) | **done 2026-05-27** | High |

---

## Goals (recap)

| ID | Goal | Done means |
|---|---|---|
| G1 | Ship a public GOTM framework usable by any LLM practitioner | Repo ready to push to public GitHub; cold-read coherent |

## Objectives (recap)

| ID | Parent | Objective | Done means |
|---|---|---|---|
| O1 | G1 | Foundation locked | source-to-target map exists; anonymization needs flagged |
| O2 | G1 | Concept docs distilled | 6 docs/ chapters present; LLM-agnostic; ~15K-20K words |
| O3 | G1 | Prompts platform-neutral | 13 prompt files present; paste-able into any LLM |
| O4 | G1 | Templates fork-ready | 5 template files present; Claude Code specifics stripped |
| O5 | G1 | Public wrapping complete | README.md cold-read coherent + LICENSE + CONTRIBUTING |

## Targets (recap)

| ID | Parent | Title | Success criterion |
|---|---|---|---|
| T1 | O1 | source-to-target-map.md | mapping covers all ~17 MVP files; anonymization flagged |
| T2 | O2 | 6 docs/*.md chapters | each chapter standalone-readable; ~2000-3000 words each |
| T3 | O3 | 13 prompts/*.md files | each prompt paste-into-LLM-and-it-works |
| T4 | O4 | 5 templates/*.md files | platform-neutral; fork-and-use |
| T5 | O5 | README + LICENSE + CONTRIBUTING | repo is push-ready |

---

## Sunset / dropped milestones (provenance — never delete)

_None yet._

---

## Notes for resume

When picking up after a pause:

1. Read this file top-to-bottom.
2. Read [`STATUS.md`](STATUS.md) for the gap ledger and foundation-gate state.
3. Read [`decisions.md`](decisions.md) for locked choices.
4. Read [`OPEN_QUESTIONS.md`](OPEN_QUESTIONS.md) for anything needing user input.
5. Identify the next eligible M and proceed.

**Checkpoint policy (D5):** sequential phase-by-phase. After M2 (foundation), checkpoint #1. After M8 (docs complete), checkpoint #2. After M13 (prompts complete), checkpoint #3. After M16 (wrap complete), final review.
