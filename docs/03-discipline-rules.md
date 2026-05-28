---
chapter: "docs/03-discipline-rules.md"
title: "The discipline rules (R1 through R11)"
audience: "LLM practitioners running complex multi-pass work"
word_target: 3000
produced_by: subagent
last_updated: 2026-05-27
project: gotm-framework-for-agentic-development
inputs:
  - docs/01-why.md (M3 voice-lock)
  - docs/02-hierarchy.md (M4 cross-ref)
  - gotm-playbook/02-anatomy/README.md (Ch 2.5)
  - gotm-playbook/07-lessons/README.md (Ch 7.1 + 7.5)
voice_calibrated_against: gotm-playbook/discovered/foundation-inventory.md §5.2
---

# The discipline rules (R1 through R11)

## How to read this chapter

`docs/01-why.md` named the three failure shapes and the four principles that resolve them. `docs/02-hierarchy.md` named the four layers the ledger sits on. This chapter names the eleven rules that bind the artifacts together. Each rule below carries the same four-block shape: a one-sentence statement of what the rule binds, a paragraph of rationale, the failure modes it prevents by name, and the enforcement signal that catches a violation. Four rules — R2, R3, R4, R11 — get an extra paragraph of motivation marked **In practice.** because they carry most of the discipline's load. The other seven stay compact. Read straight through on first pass. Return to one rule when the work in front of you needs it.

## R1 — GOTM.md is the single orchestration ledger

**Statement.** All planning lives in `GOTM.md`. No planning prose in chat. New scope writes into the ledger before it is acted on.

**Why.** Plans held in chat dissolve at the next context reset. The ledger is the artifact that survives the gap between sessions. Anything important enough to plan is important enough to land in the file the next reader will open. The chat window is a place for tight status; it is not the project.

**Failure modes prevented.** Vanishing plan; in-flight planning during a draft; scrollback-as-substrate; chat-only scope additions that never reach the ledger; resume-from-memory.

**Enforcement signal.** A session whose chat carries planning prose with no corresponding ledger update has slipped. The redirect is to append the plan to `GOTM.md` in the same turn and continue. The audit catches the downstream effect — Milestones executed without first being written to the ledger — and surfaces them as unledgered discoveries. Forward-ref: `docs/05-audit-family.md` carries the audit checks that key off this rule.

## R2 — Atomic milestones

**Statement.** Each Milestone produces exactly one named Output file in one execution pass. A description that hides several sub-tasks is several Milestones; split before writing the row.

**Why.** Aggregate Milestones break status math. A row marked "in progress" with five of six hidden sub-tasks done reads identically to a row with zero done. Aggregate rows also invite multi-pass execution, which violates the max-context rule that follows. Atomicity is the load-bearing constraint of the framework — most other rules depend on it holding.

**In practice.** The shape that triggers a split is a title joined by "and," or a row whose body carries bullet sub-items. When you see either, stop and split before writing the row. The fix replaces one parent row with sub-letter rows under R8 — each carrying its own Inputs, its own Output, and its own status flip. Splitting before work begins is cheap; splitting after work begins costs the partial output and the cascading status updates that follow.

**Failure modes prevented.** Aggregate milestones; hidden-sub-pass archetypes; Milestone-as-bucket; sibling Milestones with the same Output path; phantom completion that hides behind aggregate scope; the hidden-six shape from `docs/01-why.md`.

**Enforcement signal.** The ledger append protocol validates each new row against three checks: no bullet sub-items in the body, exactly one Output file in the Output column, no "and" connecting two output verbs in the title. The audit catches violations in existing rows by the same checks and proposes the sub-letter split.

## R3 — Milestone equals max context unit

**Statement.** Each Milestone declares the Inputs it reads and the Output it writes. The execution pass reads only the listed Inputs. State does not carry across passes.

**Why.** Working memory across passes produces paraphrase errors. A file read in week one and quoted from memory in week three reliably inverts a threshold, drops a qualifier, or shifts a figure. The reader of the output cannot see the drift. Re-reading the declared Inputs at the start of each pass costs seconds and prevents a class of silent error that no review reliably catches.

**In practice.** Treat each Milestone as a fresh read of its declared Inputs, no matter how recently you touched them. The work landed in a file; the file is what you read. Anything you remember between passes is suspect until the file confirms it. The discipline assumes one writer driving one ledger across the project's life — multi-writer topologies need different tooling.

**Failure modes prevented.** Paraphrase from memory; stale-input drift; cross-pass state assumptions; broken Input pointers that go undetected when the pass works from memory anyway.

**Enforcement signal.** The resume protocol prints only the Inputs the next Milestone declares, not the project-wide briefing. Subagent prompts pass only the listed Inputs. The audit flags Input pointers that reference files not on disk and Outputs that cite sources the Milestone's Inputs list does not name.

## R4 — Foundation before drafts

**Statement.** No draft-tier Milestone — one that writes to a `drafts/` folder or to a final deliverable file — may start until every High and Medium gap in `STATUS.md` is resolved or explicitly deferred by the user.

**Why.** Drafts on partial foundations read as shortcuts. The writer cannot see the gaps from inside the draft. The reader sees them on first read. A returned draft costs more than the foundation pull that would have closed the gap. The foundation gate is not paperwork; it is the discipline that keeps confidently-wrong output out of circulation.

**In practice.** When the temptation grows to draft because the foundation "looks close enough," the rule holds the line. Closure runs one of two paths. Either the foundation Milestone completes and the gap clears mechanically. Or the human signs off on a Deferred entry in `STATUS.md` with a stated reason. The agent cannot defer unilaterally — a unilateral deferral leaves no trace of the call, and the gap re-surfaces invisibly inside the draft.

**Failure modes prevented.** Draft on sand; foundation-deferred-for-speed; unledgered shortcuts; partial-evidence claims that pass internal review and fail external review; the silent-fill pattern where a writer substitutes expected values for missing data.

**Enforcement signal.** The resume protocol blocks draft-tier Milestones whenever the foundation gate is OPEN. The gate is OPEN whenever any High or Medium gap is unchecked in `STATUS.md`. The gate is CLOSED only when both lists are clean. Forward-ref: `docs/04-modes.md` carries the gate logic; `docs/05-audit-family.md` carries the foundation-bypass audit check.

## R5 — Ledger updates pair with file edits

**Statement.** When a Milestone completes or changes status, you update `GOTM.md` and re-derive the relevant `STATUS.md` fields in the same turn the Output file is written.

**Why.** Decoupled updates compound into drift. The pattern that grows — "update the ledger after this commit," then "tomorrow," then "next week" — produces a ledger that reflects yesterday's reality and a project that no resume protocol can recover from cleanly.

**Failure modes prevented.** Phantom completion; ledger drift across days; status reads that no longer match disk; the gap between what the chat reports and what the ledger holds.

**Enforcement signal.** Every mode that touches Outputs also writes to `GOTM.md` in the same turn. The audit flags `Status: done` rows whose Output file is absent on disk, and `Status: in_progress` rows whose Output file already exists at the declared path. Both are the visible signature of the rule slipping.

## R6 — Chat is tight status

**Statement.** Chat updates are one to two sentences referencing the ledger. Not planning prose. Not narrative summaries. Not bulleted progress reports.

**Why.** Chat narrative dissolves at the next context reset; the ledger persists. Anything important enough to say belongs in the ledger. The chat update points to it. Verbose chat updates feel productive in the moment and produce nothing the next session can read.

**Failure modes prevented.** Scrollback-as-plan; verbose status that crowds out the ledger; chat-only scope additions; the dissolved-plan pattern when the verbose chat history gets compacted.

**Enforcement signal.** Self-discipline at the keyboard. The pattern that holds reads close to "GOTM updated: M2c done, M2d in flight per the ledger." Audits do not detect verbosity directly. They catch the downstream effect — Milestones discussed in chat that never reached the ledger.

## R7 — Temp docs liberally

**Statement.** Scratch work, intermediate drafts, and per-section work-in-progress files all live in the project folder. Nothing is held in working memory across passes.

**Why.** The folder is the workspace, not just the final-output store. A synthesis that lives in someone's head for three passes never lands. One that lands on disk after each pass survives the next context reset. Intermediate files are encouraged, not discouraged.

**Failure modes prevented.** Synthesis-held-in-head; cross-pass state assumptions; the drift between what a writer thinks the draft says and what the draft actually says.

**Enforcement signal.** Encouragement, not blocking. Common temp paths sit under `drafts/sections/`, `scratch/`, and `notes/`. The audit catches the absence of intermediate files only indirectly — a final draft built from in-head state typically fails the foundation-gate check too.

## R8 — Sub-numbering preserves atomicity

**Statement.** When atomic Milestones cluster, they take sub-letter IDs — `M1a`, `M1b`, `M1c` — and each sub-letter is its own ledger row. Not bullets under one parent row.

**Why.** Status visibility. A reader of the ledger sees at a glance which sub-units are done and which remain. Bullets under one row hide the sub-status. Sub-letter rows reveal it. The split also enforces R2 mechanically: each sub-letter row carries one Output and one status flip.

**Failure modes prevented.** Hidden-sub-pass archetype; the hidden-six shape; aggregate rows that pass review because the bullets look manageable.

**Enforcement signal.** The audit flags Milestone rows whose description contains bulleted sub-items — the markdown signature of the hidden-sub-pass shape — and proposes the sub-letter expansion. Sub-numbering never nests beyond one level; a sub-letter that needs to fan out re-numbers at the parent's level.

## R9 — No ID recycling

**Statement.** Dropped Milestones, Targets, and Objectives are crossed out (`~~M5~~`) and retained in the ledger. The IDs never reuse.

**Why.** Provenance. A reader who sees a current `M5` and a struck-through `M5` from three months ago can trace the history of the project. A reader who sees only the current `M5` cannot. The same applies to dropped Targets and Objectives.

**Failure modes prevented.** Discovery loss; silent history rewrites; the lost-attempt pattern when an early scoping decision gets quietly replaced.

**Enforcement signal.** The append protocol always assigns the next-unused ID. Manual edits that recycle an ID are caught by the audit against the project's full Milestone history. Sub-letter expansion runs in one direction: once `M1` splits into `M1a` and `M1b`, the original `M1` row sunsets rather than being edited in place.

## R10 — Subagent delegation uses the prescribed prompt template

**Statement.** When a Milestone is delegated to a subagent, the prompt follows the prescribed template — Inputs only, no project-wide briefing.

**Why.** Subagents that receive too much context produce sprawling outputs that conflate scope. Subagents that receive exactly the foundation files the Milestone declared produce verifiable artifacts the parent can integrate. The template enforces the boundary; the boundary is what keeps subagent output composable.

**Failure modes prevented.** Subagent sprawl; outputs that exceed declared scope because the briefing exceeded scope; cross-Milestone bleed when one subagent absorbs context that belongs to another.

**Enforcement signal.** Compliance is parent-agent discipline at dispatch time. The audit spot-checks subagent prompts against the template structure. Forward-ref: the subagent prompt templates ship under `prompts/subagent-execution.md` and `prompts/subagent-audit.md`.

## R11 — The ledger expands as we discover

**Statement.** Executing a Milestone routinely uncovers new scope — new Milestones, sometimes new Targets, occasionally new Objectives, rarely new Goals. When that happens, you write the new scope into `GOTM.md` (and `STATUS.md` or `OPEN_QUESTIONS.md` where appropriate) before continuing the current pass.

**Why.** Foundation-first execution produces discovery. That is the system working as designed, not an exception. The failure mode is dropped scope — the come-back-to-it intention that never lands because nothing carried it forward. The append takes seconds. The drift it prevents costs days.

**In practice.** Discovery does not arrive at the same authority level across the hierarchy. A new Milestone is a routine atomic append. A new Goal reshapes what the project is for, and the agent does not invent Goals. The ratification ladder below names where the line sits. The reflex inside a pass is to note a discovery in chat and keep working. The rule reverses the reflex: stop, append the discovery to the ledger at the right layer, then resume.

| Layer | Discovery during execution | Plan-mode initial proposal |
|---|---|---|
| Goal | Route to `OPEN_QUESTIONS.md`; wait for human ratification | Route to `OPEN_QUESTIONS.md`; human ratifies before init |
| Objective | Agent discretion (heuristic: surface if material; else atomic with `decisions.md` rationale) | Agent proposes directly; human reviews full proposal once |
| Target | Atomic addition | Agent proposes directly |
| Milestone | Atomic addition | Agent proposes directly |

The Objective heuristic carries most of the load in practice. If adding the Objective would change what the human thinks the project is delivering — a new deliverable surface, a new audience, a new timeline — the agent surfaces it to `OPEN_QUESTIONS.md` and waits. If the new Objective is an internal refinement of an existing one, the agent appends to `GOTM.md` directly and logs a one-paragraph rationale in `decisions.md` so the move is auditable.

**Failure modes prevented.** Dropped scope; discovery loss; the come-back-to-it pattern; resolutions recorded but not applied; unilateral Goal invention; in-pass scope creep that lands in the output but never in the ledger.

**Enforcement signal.** The append protocol handles new Milestone, Target, Objective, and Goal additions per the ladder above. The audit flags Output files that mention scope ("we should also...", "discovered:", "TODO:") not reflected in any later ledger row. Forward-ref: `docs/04-modes.md` carries the append-mode mechanics that respect the ladder; `docs/06-archetypes.md` shows the ladder applied across archetypes.

## Extending the rules — project-specific R12+

The eleven rules above are the canonical layer. They are sufficient for every project that lands on the framework. Real projects sometimes produce real failures whose recovery generalizes, and at that point a project can extend the rule set for its own use without rewriting the canonical.

The loop has a shape. A failure surfaces during execution. The recovery is named in plain language. The recovery generalizes — the same fix would help future Milestones inside the same project. The recovery becomes a rule and lands under a "Project-specific additions" header inside the project's `GOTM.md` discipline-rules block. Numbering starts at R12 and continues forward, never recycling, in the same spirit as R9.

The bar for adding a rule is high. Add a project-specific R-rule when the same recovery has been needed twice AND the rule generalizes beyond a single Milestone. Otherwise the correction belongs in `decisions.md` as a D-entry, where the choice is recorded once and the project moves on. Inflating the rule set with single-incident additions dilutes the rules that actually bind.

Two example shapes, both illustrative and generic:

- **R12 — Default to subagent for bounded-input Milestones; foreground holds the ledger and synthesis only.** Codifies the operating mode when foreground execution hits context-budget pressure. Why: foreground cost accumulates as a multi-Milestone project grows; the foreground pass that holds the ledger cannot also afford to hold every Milestone's Inputs.
- **R13 — Workshop-slide authoring requires a story-foundation document before any content-tile drafts.** Emerged after content-tile drafts produced unusable output without a story spine — twice. Why: the deliverable shape carries an implicit dependency that R1 through R11 do not catch on their own.

Both rules are project-local. They are not promoted into the canonical until they have shown up across many projects and the recurrence is undeniable.

## Compound failure modes

The eleven rules each carry their own failure mode prevented. Most real violations cross several rules at once, and the cross-cutting shape is what makes the violation hard to see from inside the work. Four compound bundles recur often enough to name. Each repairs in a specific order — fix the rule the others depend on, and the cascading rules close on their own.

**Inflight planning during a draft (R1 + R4 + R6).** A half-written draft sits open. The chat fills with "let me think about which sections we need next." The foundation gate is OPEN but the draft is already running. The draft violates R4, the planning violates R1, and the chat verbosity violates R6. Repair starts with R1 — move the planning into the ledger first. The draft pauses until R4 closes. R6 self-corrects once R1 lands.

**Aggregate milestone executed in one pass (R2 + R3 + R8).** A row sits in_progress for an unusually long stretch. The Output file grows past its declared shape. The row is several Milestones in disguise, R3 cannot bind a max-context unit it cannot name, and R8's sub-letter expansion never ran. Repair starts with R2 — split the row into atomic sub-letter rows. R3 and R8 close on the same edit.

**Ledger drift across days (R1 + R5 + R11).** `last_updated` lags the most recent Output by days. The audit produces a long list of phantom completions. New scope landed in conversation but never in the file. The drift compounds because R5 (paired updates) has been slipping for long enough that R1 (single ledger) and R11 (discovery to ledger) have stopped binding too. Repair starts with R5 — reconcile every status against disk in one pass. R1 and R11 close as the paired updates resume.

**Foundation deferred for speed (R4 + R11).** A deferred section is overfull. The gate reads CLOSED. The draft is proceeding on shaky ground. R4 broke because R11 broke first — discoveries that should have surfaced as foundation gaps got absorbed into deferrals without a stated reason. Repair starts with R11 — surface the buried discoveries into the gap ledger. R4 then enforces correctly against the updated state.

Forward-ref: `docs/05-audit-family.md` covers the audit-M to fix-Ms cadence that drives these repairs at scale.

## Common pitfall

> **Common pitfall.** Reading the eleven rules as eleven separate disciplines to follow item-by-item. The intent is rigor; the result is that every rule reads in isolation and the larger shape goes unseen. The rules interlock. Most violations cross several rules at once, and the compound failure modes above name the most common bundles. Read the rules as a system, not a checklist.
