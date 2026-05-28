---
milestone: M2
project: gotm-framework-for-agentic-development
produced_by: subagent
last_updated: 2026-05-27
inputs:
  - gotm-playbook/discovered/foundation-inventory.md §5-§6
  - fe-gotm/ v1.3 files (SKILL, discipline, hierarchy, subagent-prompts, templates)
  - gotm-playbook/ Module 0/1/2/3/4/6/7 READMEs
  - gotm-framework-for-agentic-development/decisions.md (D1-D7)
feeds: M3-M16
---

# Source-to-target map — gotm-framework-for-agentic-development

## 1. The 27 MVP public-repo target files

The MVP repo (per D6) ships four artifact categories: six concept docs, thirteen standalone prompts, five fork-ready templates, three top-level wrapping files. The earlier "~17 files" framing undercounted — the audit-prompt cluster expands to eight files under R2 tight-cluster, subagent-prompts to two, templates to five. The corrected total is **twenty-seven files**.

This map is the foundation every downstream Milestone (M3-M16) consumes. Each chapter draft reads its row to know what to lift, what to rewrite, what to author fresh. The mapping is paired with an anonymization audit so each draft inherits a clean find/replace list rather than rediscovering banned references mid-pass.

## 2. Source-to-target mapping table

Columns: target path · primary source · secondary sources · classification (`lift` | `rewrite` | `new authoring`) · anonymization risk (`low` | `med` | `high`) · target word count.

### 2.1 Concept docs (T2 — six files)

| Target file | Primary source | Secondary sources | Class | Anon | Words |
|---|---|---|---|---|---|
| `docs/01-why.md` | playbook `01-theory/README.md` Ch 1.1 + 1.2 + 1.5 | `00-overview/README.md`; foundation-inventory §3 (F-mode anchors) | rewrite | med | ~2500 |
| `docs/02-hierarchy.md` | playbook `02-anatomy/README.md` Ch 2.1 + 2.3 | fe-gotm `resources/hierarchy.md` (full); playbook `07-lessons/README.md` §7.2.5 | rewrite | low | ~2200 |
| `docs/03-discipline-rules.md` | playbook `02-anatomy/README.md` Ch 2.5 (R1-R11 + ratification ladder) | fe-gotm `resources/discipline.md` (full, incl. compound failure modes); playbook `07-lessons/README.md` Ch 7.1 + 7.5 | rewrite | low | ~3000 |
| `docs/04-modes.md` | fe-gotm `SKILL.md` v1.3 (plan, init, run, resume, audit, append, status, decision) | playbook `07-lessons/README.md` Ch 7.5 (run loop, ratification ladder) | rewrite | med | ~2500 |
| `docs/05-audit-family.md` | fe-gotm `SKILL.md` audit family table + audit-M → fix-Ms cadence | playbook `07-lessons/README.md` Ch 7.4 + 7.5.6 (completion-verification); `04-execution/README.md` Ch 4.7 (worked audit) | rewrite | low | ~2200 |
| `docs/06-archetypes.md` | playbook `03-patterns/README.md` Ch 3.1-3.5 (rubric + 4 archetypes) | none | rewrite | high | ~2400 |

### 2.2 Orchestration prompts (T3 part 1 — three files)

| Target file | Primary source | Secondary sources | Class | Anon | Words |
|---|---|---|---|---|---|
| `prompts/plan.md` | fe-gotm `SKILL.md` `plan` mode section (lines 117-155) | playbook `07-lessons/README.md` §7.5.3 | rewrite | med | ~600 |
| `prompts/init.md` | fe-gotm `SKILL.md` `init` mode section (lines 156-210) | playbook `02-anatomy/README.md` Ch 2.2 (five ledger files) | rewrite | med | ~700 |
| `prompts/run.md` | fe-gotm `SKILL.md` `run` mode v1.3 section (lines 211-280) | playbook `07-lessons/README.md` §7.5.4 (run loop) | rewrite | high | ~900 |

### 2.3 Audit prompts (T3 part 2 — eight files, R2 tight-cluster)

| Target file | Primary source | Secondary sources | Class | Anon | Words |
|---|---|---|---|---|---|
| `prompts/audit-ledger-shape.md` | fe-gotm `SKILL.md` audit mode (lines 312-350) | foundation-inventory §3 | rewrite | low | ~500 |
| `prompts/audit-content-claim.md` | fe-gotm `SKILL.md` audit family table (content/claim row) | playbook `07-lessons/README.md` §7.4.2 | new authoring | low | ~500 |
| `prompts/audit-foundation-files.md` | fe-gotm `SKILL.md` audit family table (foundation-files row) | playbook `07-lessons/README.md` §7.4.2 | new authoring | low | ~500 |
| `prompts/audit-code-artifact.md` | fe-gotm `SKILL.md` audit family table (code-artifact row) | playbook `07-lessons/README.md` §7.4.2 | new authoring | low | ~500 |
| `prompts/audit-ui-render.md` | fe-gotm `SKILL.md` audit family table (UI/render row) | playbook `07-lessons/README.md` §7.4.2 | new authoring | low | ~500 |
| `prompts/audit-source-fidelity.md` | fe-gotm `SKILL.md` audit family table (source-fidelity row) | playbook `07-lessons/README.md` §7.4.2 | new authoring | low | ~500 |
| `prompts/audit-density.md` | fe-gotm `SKILL.md` audit family table (density row) | playbook `07-lessons/README.md` §7.4.2 | new authoring | low | ~500 |
| `prompts/audit-completion-verification.md` | fe-gotm `SKILL.md` audit family table (completion-verification row, v1.3) | playbook `07-lessons/README.md` §7.5.6 | rewrite | low | ~600 |

### 2.4 Subagent templates (T3 part 3 — two files, R2 tight-cluster)

| Target file | Primary source | Secondary sources | Class | Anon | Words |
|---|---|---|---|---|---|
| `prompts/subagent-execution.md` | fe-gotm `resources/subagent-prompt.md` (full) | playbook `04-execution/README.md` Ch 4.2 | rewrite | high | ~900 |
| `prompts/subagent-audit.md` | fe-gotm `resources/subagent-prompt-audit.md` (full, v1.3) | playbook `07-lessons/README.md` §7.5.5 | rewrite | high | ~900 |

### 2.5 Templates (T4 — five files, R2 tight-cluster)

| Target file | Primary source | Secondary sources | Class | Anon | Words |
|---|---|---|---|---|---|
| `templates/GOTM.md` | fe-gotm `templates/GOTM.md.template` | playbook `02-anatomy/README.md` §2.2.2 | lift | med | ~700 |
| `templates/STATUS.md` | fe-gotm `templates/STATUS.md.template` | playbook `02-anatomy/README.md` §2.2.3 | lift | low | ~250 |
| `templates/decisions.md` | fe-gotm `templates/decisions.md.template` | playbook `02-anatomy/README.md` §2.2.4 | lift | low | ~200 |
| `templates/OPEN_QUESTIONS.md` | fe-gotm `templates/OPEN_QUESTIONS.md.template` | playbook `02-anatomy/README.md` §2.2.5 | lift | low | ~200 |
| `templates/README.md` | fe-gotm `templates/README.md.template` | playbook `02-anatomy/README.md` §2.2.6 | lift | med | ~300 |

### 2.6 Wrapping (T5 — three files)

| Target file | Primary source | Secondary sources | Class | Anon | Words |
|---|---|---|---|---|---|
| `README.md` | all prior phase outputs (docs/, prompts/, templates/) | playbook `00-overview/README.md` (book-level intro) | new authoring | med | ~1200 |
| `LICENSE` | standard MIT text (per D4) | none | lift | low | ~200 |
| `CONTRIBUTING.md` | none (standard contribution norms) | none | new authoring | low | ~400 |

**Aggregate breakdown:** 6 `lift` · 14 `rewrite` · 7 `new authoring` · 5 high-risk · 8 med-risk · 14 low-risk anonymization.

## 3. Anonymization audit — banned-internal-references list

Per foundation-inventory §5.1, the public-repo voice profile bans internal references. The categories below are the find-list every chapter draft inherits.

- **Real organization names.** Databricks, Epsilon, Publicis, the FE org, customer names. High frequency in playbook Module 6 worked failures (RG10), `SKILL.md` line 20 in-flight-projects list (RG11), `subagent-prompt.md` worked example (RG13). Replace with generic categories ("an enterprise software company," "a consulting partner").
- **Canonical customer placeholders.** "Acme Industrial" in playbook Ch 2.1 + 2.3 + 3.2. Replace with a neutral name per chapter that does not echo an internal canonical.
- **Internal project names.** `perf/h1-2026`, `WAF`, `agentic-workshop`, `epsilon-multicloud-workshop`, `publicis-groupe-vault`, `genie-hackathon-deck`. Replace with abstract IDs ("a synthesis project," "an event-delivery project").
- **Internal employee names.** Found in `philosophy.md`. Replace with role archetypes ("the author," "an engineer").
- **Plugin path references.** `fe-gotm:...`, `fe-vibe/...`, absolute filesystem paths. Drop entirely or rewrite as the framework name in prose.
- **Internal Slack / Confluence / Glean handles.** Strip outright from any template comments or example links.

## 4. Per-target anonymization notes (med- and high-risk rows)

- `docs/01-why.md` (med). Playbook Ch 1.1 + 1.5 reference real "WAF" and "perf/h1-2026" projects implicitly in failure framing; replace with abstract examples ("a multi-week synthesis project").
- `docs/04-modes.md` (med). `SKILL.md` mode sections reference Claude Code primitives by name (sidebar at line 623); per RG12 the public version teaches modes tool-agnostically — strip Claude-Code-specific dispatch syntax and frontmatter conventions.
- `docs/06-archetypes.md` (high). Playbook Ch 3.2 ("data catalog tool"), 3.3 ("cross-team impact reflection"), 3.4 ("one-day technical workshop"), 3.5 ("churn reduction") all read as internal-project anonymizations already, but several retain plugin path tokens or real-name traces — re-anonymize cleanly per chapter.
- `prompts/plan.md` and `prompts/init.md` (med). `SKILL.md` mode sections embed example chat outputs that name real plugins and internal Ms — replace with abstract M-IDs.
- `prompts/run.md` (high). The run-loop's example chat outputs reference internal projects ("M4.2 closed. Ch 4.1 draft at...") and use Claude Code's slash-command syntax — strip both and rewrite the run-loop as platform-neutral protocol per D7.
- `prompts/subagent-execution.md` (high). The fe-gotm template's worked example (§"Example: a research-pull Milestone") names an internal customer-workshop M; per RG13 replace with a synthetic example (e.g., "Example: a competitor-pricing research pull"). Also resolve the nested-code-fence rendering issue noted in RG3.
- `prompts/subagent-audit.md` (high). Same pattern — the v1.3 worked completion-verification example is internal; rebuild with a synthetic ledger.
- `templates/GOTM.md` and `templates/README.md` (med). The template comments include `fe-gotm:` plugin paths and reference internal feedback files (RG14 memory-hooks block in README.md) — drop the memory-hooks section entirely; rewrite path references as relative ("see `resources/discipline.md`").
- `README.md` top-level (med). Drop author/email blocks from the colophon (RG15) and the plugin-runtime memory-hook references (RG14). Frame the framework as "GOTM" with the long name as repo-slug only (per D3).

## 5. Voice calibration for the public-repo audience

The playbook's voice profile (foundation-inventory §5.1) already targets an external audience — Flesch-Kincaid 9-11, second-person for instruction, third-person past for archetypes, present tense for principles, no banned phrases, no internal references. The public-repo audience per D2 is a strict subset. The profile transfers without adjustment.

**One recommended exception.** Public-repo prose may name LLM platforms when needed — "ChatGPT," "Cursor," "Cline," "Continue," "Claude API," "raw chat" — because they are the practitioner's tools and the audience needs concrete handles. Not a vendor endorsement; mirrors D7's platform-neutral framing where every prompt must work on every platform. Other vendor names remain banned. Module 4 and several prompts will lean on this exception; downstream Ms should not invent others without a D-entry.

## 6. Sequencing recommendation

Per D5 (sequential phase-by-phase with four checkpoints), the recommended order is:

1. **M3 (`docs/01-why.md`) first.** Sets the public-repo voice. Downstream docs Ms calibrate against M3's locked register.
2. **M4-M8 in numbered order.** Each doc reads cleanly from M2 + its named playbook chapter; cross-doc dependencies are light. Checkpoint #2 lands here.
3. **M9-M11 (orchestration prompts).** Depend on docs being voice-locked since the prompts cite the docs by chapter.
4. **M12 (audit-prompts tight-cluster, R2).** Eight files in one pass since they share the audit-family pattern. Checkpoint #3 lands here.
5. **M13 (subagent-prompts tight-cluster, R2).** Two files.
6. **M14 (templates tight-cluster, R2).** Five files.
7. **M15 (top-level `README.md`) last.** Needs all phase outputs to compose the 60-second pitch.
8. **M16 (`LICENSE` + `CONTRIBUTING.md`, R2).** Standard files; closes the project. Final checkpoint.

## 7. Gaps surfaced

- **Target-file count understated in GOTM.md ledger.** The ledger header says "~17 public-repo files" but the audit-prompt cluster alone is eight files. Recommend the parent update GOTM.md's mission and O3 success criterion to "27 MVP files" (13 prompts + 6 docs + 5 templates + 3 wrapping).
- **`docs/06-archetypes.md` is the highest-anon-risk doc** because every playbook archetype example carries internal-project traces. Recommend the parent flag this as needing an extra anonymization-audit pass before checkpoint #2.
- **Subagent-prompt nested-code-fence rendering bug (RG3 from foundation-inventory)** must be resolved during M13 — surface this in the M13 brief.
- **No discoverability of "GOTM vs OKRs/agile" framing in M3 brief.** Playbook Ch 1.5 covers it but the current M3 row only cites Module 1; recommend explicit citation of Ch 1.5 in the M3 Input list.
