---
chapter: "docs/04-modes.md"
title: "The eight modes"
audience: "LLM practitioners running complex multi-pass work"
word_target: 2500
produced_by: subagent
last_updated: 2026-05-27
project: gotm-framework-for-agentic-development
inputs:
  - docs/01-why.md (M3 voice)
  - docs/02-hierarchy.md (M4)
  - docs/03-discipline-rules.md (M5 — R-rules referenced throughout)
  - fe-gotm/skills/gotm/SKILL.md v1.3
  - gotm-playbook/04-execution/README.md (Module 4)
  - gotm-playbook/07-lessons/README.md (Ch 7.5)
voice_calibrated_against: gotm-playbook/discovered/foundation-inventory.md §5.2
---

# The eight modes

## How to read this chapter

`docs/02-hierarchy.md` named the four layers. `docs/03-discipline-rules.md` named the eleven rules. This chapter names the operational surface — what you actually do with the discipline. Eight modes carry the work: `plan`, `init`, `run`, `resume`, `audit`, `append`, `status`, `decision`. Each mode is a protocol — what you instruct your LLM to do, what the LLM produces, what you do next. The modes are not commands tied to a specific tool; they are shapes the discipline takes when you run it. The paste-able prompts live in the `prompts/` directory. Per-mode entries below follow a fixed structure: Purpose, When to use, Inputs, Outputs, Next action.

## The mode-dispatch table

The eight modes are not invoked at random. Each has a trigger condition rooted in the state of the project. The table below pairs each mode with its one-line purpose and the moment in the project's lifecycle when you reach for it. Read straight down on first pass. Return to a row when the state it names shows up in your own work.

| Mode | One-line purpose | When you reach for it |
|---|---|---|
| `plan` | Propose a G/O/T/M hierarchy from a natural-language ask. | At the very start, when you have an ask but no hierarchy yet. |
| `init` | Scaffold the five ledger files from a ratified plan. | After `plan` has landed and the human has ratified the Goals. |
| `run` | Autonomously orchestrate execution of the next eligible Milestones. | After `init`, when the ledger holds work the LLM can pick up. |
| `resume` | Print the next eligible Milestone with its Inputs. | When a human is taking the next pass directly, without `run`. |
| `audit` | Check ledger shape and report findings. | After a heavy week, after a long pause, before a review, before a merge. |
| `append` | Add newly discovered scope per the ratification ladder. | When execution surfaces work the original plan did not name. |
| `status` | Regenerate `STATUS.md` as a derived view of `GOTM.md`. | After any ledger change of substance. |
| `decision` | Append a D# entry to `decisions.md`. | When a choice locks that future passes should not re-litigate. |

## `plan`

**Purpose.** Take a natural-language ask and propose a G/O/T/M hierarchy the practitioner can ratify. The mode does the cognitive work of decomposing an outcome into outcome-shaped Objectives, sized Targets, and atomic Milestones — without committing the project folder yet.

**When to use.** At the very start, when you have an ask but no hierarchy. Also when an existing project's scope shifts enough that the original plan no longer fits and proposing a new shape reads cleaner than patching the old one row at a time.

**Inputs.** The ask itself — a one-paragraph natural-language brief. Optional anchors strengthen the proposal: a delivery date, an audience, hard constraints, a preferred shape (`g-o-t-m` or `g-o-m`), a preferred target style (benchmark, deliverable, or workstream). If anchors are missing, the LLM infers what it can and surfaces the rest as questions.

**Outputs.** A draft `GOTM.md` carrying the proposed hierarchy as a tree, plus a routing of Goal-level proposals to `OPEN_QUESTIONS.md` for human ratification. The folder is not committed yet. The draft reads as a proposal — explicit about what was inferred and what still needs human input.

**Next action.** The human ratifies the proposed Goals. Once locked, the practitioner runs `init` to formalize the project folder. Outcome-shaped Objectives are required; if any proposed Objective could plausibly become a Milestone title, it is shaped as a process and needs reshaping before init lands. See `docs/02-hierarchy.md` §6 for the outcome-shape heuristic.

## `init`

**Purpose.** Scaffold the five ledger files from a ratified plan. Take what `plan` proposed and the human ratified, and turn it into the durable folder structure that holds the project for the rest of its life.

**When to use.** After `plan` has landed and the human has signed off on the Goals. Also as the first action when starting from a hand-written plan rather than from a `plan` proposal — in that case the human's plan stands in for the ratified draft.

**Inputs.** The ratified plan, plus the project anchors: project name, one-sentence mission, delivery anchor (date, audience, venue), shape (`g-o-t-m` or `g-o-m`), target style (`benchmark`, `deliverable`, or `workstream`). The folder location and creation date round out the inputs.

**Outputs.** Five ledger files scaffolded in a new project folder: `GOTM.md` carrying the hierarchy and the discipline rules block, `STATUS.md` carrying the derived view with the foundation gate set to OPEN, `decisions.md` empty and ready for append-only entries, `OPEN_QUESTIONS.md` carrying any questions routed from `plan`, and `README.md` carrying the mission and the project's reading order. A canonical M1 — foundation discovery — is seeded under the first Objective so the project starts with an inventory pass.

**Next action.** Usually `run`, which dispatches the seeded M1 and the Milestones that follow. The practitioner may also take the first pass manually, in which case the next action is `resume`.

## `run`

**Purpose.** Autonomous orchestration loop. Given a current ledger, the mode picks the next eligible Milestone, classifies the subagent role it needs, dispatches the subagent, absorbs the result, updates the ledger, and continues until a checkpoint. The mode turns the discipline into a runnable system rather than a manual protocol.

**When to use.** After `init`, whenever the ledger holds at least one eligible pending Milestone and the practitioner wants the LLM to drive execution. Bounded options let the loop stop after a fixed number of Milestones or at a checkpoint.

**Inputs.** The existing ledger files — `GOTM.md`, `STATUS.md`, `decisions.md`, `OPEN_QUESTIONS.md`. Optional caps bound the loop: a maximum number of Milestones, or an instruction to run until the next checkpoint.

**Outputs.** One or more Milestones executed, the ledger updated paired with each closure per R5, fix-Ms appended where an audit-agent surfaces them, and a tight chat report at the end naming what closed and what the next action is.

**Next action.** The loop one iteration: read the ledger, pick the next eligible M whose Inputs all exist and whose prerequisite Ms are all done, classify the subagent role (execution-agent for content production, audit-agent for ledger or content checks), dispatch with the M's Inputs only per R3, wait for completion, absorb the Output, update `GOTM.md` and re-derive `STATUS.md` in the same turn, then apply the ratification ladder to any surfaced discoveries per R11. The loop stops at a module or Objective boundary, when the foundation gate flips pending, when a Goal-level discovery surfaces, or when the max-Ms cap is reached. See `docs/03-discipline-rules.md` R11 for the ratification ladder that governs which discoveries the loop may absorb autonomously.

## `resume` (alias `next`)

**Purpose.** Print the next eligible Milestone with its Inputs, Output path, and discipline reminders. The mode does not execute the Milestone — it reports the readiness state so a human can pick up the next pass directly.

**When to use.** When a human is taking the next pass without running the autonomous loop. Common shapes: after a long pause, after a context reset, or when the practitioner wants to inspect the next pass before dispatching it.

**Inputs.** `GOTM.md` and `STATUS.md`. The mode reads the foundation-gate state from `STATUS.md` and the next pending row from `GOTM.md`.

**Outputs.** A chat status, not a file. The status names the next Milestone's ID and title, lists its Inputs as absolute paths, names the Output path, and reminds the practitioner of the rules that bind the pass — read only the listed Inputs, write exactly one Output, pair the ledger update with the file edit. If the next Milestone is draft-tier and the foundation gate is OPEN, the mode blocks the start and prints the gap ledger instead.

**Next action.** The practitioner reads the print, holds the scope it names, and executes the pass — directly or by handing it to an execution-agent. Execution is a separate user turn; the mode only reports.

## `audit`

**Purpose.** Check ledger shape and report findings. The mode runs against `GOTM.md`, `STATUS.md`, and the project folder, and reports violations against the discipline rules. The full audit family — six kinds beyond the canonical ledger-shape audit — is covered in `docs/05-audit-family.md`.

**When to use.** After a heavy week of execution, after a long pause, before a review meeting, and before merging two project branches. The trigger is human judgment, not a schedule.

**Inputs.** `GOTM.md`, `STATUS.md`, the project folder for filesystem checks, and the truth files relevant to the audit kind being run.

**Outputs.** An audit report with severity tiers: HIGH (blocks delivery; must fix before the next foundation-gate flip), MEDIUM (polish before delivery; non-blocking), LOW (nits), and UNVERIFIED (no source contradicts the claim, but no Input confirms it; flagged for human verification). The report is the Output of an audit Milestone, which is itself one execution pass per R2.

**Next action.** Fixes do not land inside the audit Milestone. They land as separate fix-Ms, typically split by severity tier. An audit-agent dispatched under `run` may append fix-Ms autonomously under its standing authority; the audit mode itself never edits the ledger content it audits. The non-destructive nature is what makes audit safe to run frequently.

## `append`

**Purpose.** Add newly discovered scope to the ledger at the correct layer per the ratification ladder. The mode handles new Milestones, new Targets, new Objectives, and — with explicit human approval — new Goals. Discovery during execution is expected per R11, not an exception, and `append` is the protocol that absorbs it.

**When to use.** Whenever execution surfaces scope the original plan did not name. The reflex inside a pass is to note a discovery in chat and keep working; the rule reverses the reflex. Stop, append the discovery at the right layer, then resume.

**Inputs.** The proposed scope plus its ratification-layer determination. A new Milestone names its parent, title, Inputs, Output path, and priority. A new Target names its parent Objective and reason. A new Objective names its parent Goal and reason. A new Goal routes to `OPEN_QUESTIONS.md` first and lands in `GOTM.md` only after human approval.

**Outputs.** The ledger updated. The new row carries the next unused ID per R9 — no recycling of dropped IDs, no reuse of sunset numbers. New Targets and Objectives carry a seed Milestone — "Scope and inventory" — so the new scope has a concrete first pass. Goal additions land paired with a `decisions.md` entry capturing the scope expansion.

**Next action.** Resume the pass that surfaced the discovery, now operating against a ledger that reflects reality. The chat update is one line per discovery; the ledger holds the detail. The ratification ladder per R11 governs whether each addition was atomic-appendable or required human approval.

## `status`

**Purpose.** Regenerate `STATUS.md` from `GOTM.md`. The mode holds the derived view in sync with the ledger that owns the truth. `STATUS.md` is not a source of truth; it is a view computed from one.

**When to use.** After any ledger change of substance. New Milestone added, Milestone closed, gap landed, decision locked — each is a trigger. R5 binds the trigger to a same-turn pair: the change to `GOTM.md` and the re-derivation of `STATUS.md` land together.

**Inputs.** `GOTM.md`. The mode reads the ledger and recomputes the derived fields.

**Outputs.** `STATUS.md` rewritten in place. The regenerated file carries completion counts (Goals, Objectives, Targets, Milestones), the active Milestone block (next pending row with its Inputs and Output path), the gap ledger (High, Med, Low), the blocked Milestones list, the deferred items section, and the recent updates list. The foundation gate state recomputes from the gap ledger: OPEN if any High or Med gap is unchecked, CLOSED only when both lists are clean.

**Next action.** The practitioner reads the regenerated `STATUS.md`, confirms the gate state, and continues execution. The mode runs cheaply enough that it can land after every meaningful change without friction.

## `decision`

**Purpose.** Append an ADR-style entry to `decisions.md`. The file is append-only; prior entries are never edited. When a choice is reversed, a new D# lands with `Status: superseded by D<n>` and the prior entry stays in place.

**When to use.** When a choice locks that future passes should not re-litigate. Architectural choices, scope cuts, target-style picks, shape decisions, audience definitions — each lands as a D# entry so the next reader can see what was decided and why.

**Inputs.** The decision ID (next D#), a one-line headline, the context that made the decision necessary, the decision itself, the alternatives considered, the consequences locked in or foreclosed, and the linked GOTM node (G, O, T, or M id) the decision binds to.

**Outputs.** A new D# block appended to `decisions.md` with the fields above. The relevant ledger node in `GOTM.md` may also gain a `→ see D<n>` reference so a reader can follow the decision back to its rationale.

**Next action.** Resume the pass that surfaced the decision. The chat update is one line referencing the new D#; the decision file holds the detail. Decisions land in the turn the choice was made, never retroactively.

## How the modes interact

The modes form a workflow that mirrors the project's lifecycle. A typical project flows like this. `plan` proposes the hierarchy from the ask. The human ratifies the Goals through `OPEN_QUESTIONS.md`. `init` formalizes the ratified plan into the five ledger files. `run` takes over and orchestrates execution autonomously, dispatching subagents and absorbing their Outputs. At each checkpoint — module boundary, foundation-gate flip pending, Goal-level discovery surfaced, max-Ms cap reached — the loop stops and the human reviews. The human may continue the loop, `append` discoveries that surfaced, `decision` choices that locked, or run `audit` to check the ledger's shape. Fix-Ms append from audit findings, and the loop continues.

The discipline rules in `docs/03-discipline-rules.md` constrain HOW the modes operate — the same-turn paired updates of R5, the Inputs-only constraint of R3, the atomic-Output constraint of R2, the ratification ladder of R11. The hierarchy in `docs/02-hierarchy.md` defines WHAT the modes operate on. The modes are the operational surface on top; the rules and the hierarchy are the underlying physics. Archetype-specific patterns appear in `docs/06-archetypes.md`.

## Mode boundaries — what each does NOT do

A short list of clarifications. Each names what a mode does not do, so the reader does not mistake one mode for another.

- `plan` does not commit folders — that is `init`'s job.
- `init` does not propose new Goals — Goals must be human-ratified before init.
- `run` does not edit Milestone content — subagents produce Outputs; the loop absorbs them.
- `resume` does not execute — it reports the next M and stops.
- `audit` does not fix violations — audit reports; fix-Ms (separate Ms) fix.
- `append` does not delete — IDs never recycle per R9; the file is append-only at the row level, with sunsets marked by strikethrough.
- `status` does not change underlying state — the file is derived from `GOTM.md`.
- `decision` does not edit prior decisions — the file is append-only; reversal lands as a new D#.

Each boundary maps to a discipline rule. Crossing a boundary collapses the rule the mode was built to enforce. The boundaries are what keep the modes composable.

## Common pitfall

> **Common pitfall.** Treating the modes as features of a specific tool — assuming that without slash commands, native skills, or a particular agent framework, GOTM is unavailable. The modes are protocols. The tool is whichever LLM the practitioner uses. A practitioner can run all eight modes through copy-pasted prompts in a raw chat session, through native skills in an agent framework, or through scripted orchestration in a notebook. The mode is what matters. The tool is incidental. The actual paste-able prompts live in the `prompts/` directory; the tool's role is to read them and act.
