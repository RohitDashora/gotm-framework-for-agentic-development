---
chapter: "docs/02-hierarchy.md"
title: "The G/O/T/M hierarchy"
audience: "LLM practitioners running complex multi-pass work"
word_target: 2200
produced_by: subagent
last_updated: 2026-05-27
project: gotm-framework-for-agentic-development
inputs:
  - docs/01-why.md (M3 — voice-lock)
  - gotm-playbook/02-anatomy/README.md (Ch 2.1)
  - gotm-playbook/07-lessons/README.md (Ch 7.2 §7.2.5)
voice_calibrated_against: gotm-playbook/discovered/foundation-inventory.md §5.2
---

# The G/O/T/M hierarchy

## 1. What the hierarchy answers

The external ledger named in `docs/01-why.md` is not a free-form document. It sits on a four-layer hierarchy, and each layer answers one canonical question. The Goal answers why. The Objective answers what. The Target answers how much, or what shape "done" takes. The Milestone answers when. The four questions chain into one plan. A Goal carries Objectives, an Objective carries Targets, a Target carries Milestones, and a Milestone produces one named output file. Reading the hierarchy in that order reads the project's intent from purpose to action.

The shape is structural. It is also disciplined. Every row that enters the ledger occupies exactly one layer, and the layer choice is locked at the moment the row is written. This chapter teaches you the four layers, the ID scheme that names them, the two project shapes you can pick from, the three target styles, the outcome-shaped Objective heuristic, and the disambiguation tests that resolve the common layer confusions.

## 2. The four layers in detail

The four layers form a shape every reader of the ledger needs to hold in mind. Each layer has a canonical question, a definition, and a working range for how many of its kind a healthy project carries. The table below names all four. Read it once, and you have the spine of any GOTM project.

| Layer | Canonical question | Definition | Cardinality |
|---|---|---|---|
| **Goal** (G) | Why? | A broad, high-level, long-term outcome — the project's reason for existing. Usually not directly measurable; closer to a direction than a deliverable. | 1–3 per project |
| **Objective** (O) | What? | A specific short-to-medium-term result that breaks a Goal into actionable work. Closes when delivered. | 3–10 per Goal |
| **Target** (T) | How much? | A quantifiable benchmark, a named deliverable, or a scoped workstream — depending on the project's target style. Tied to one Objective. | 0–6 per Objective |
| **Milestone** (M) | When? | One atomic execution pass — one pass equals one named output file. | 1–20 per Target (or per Objective in the flat shape) |

The Goal sits at the top and is usually one row long; a project with more than three Goals is two projects pretending to be one. The Objective is the layer where most visible work lives, and closing one is a recognizable milestone for any reader of the ledger. The Target is overloaded by design — three legitimate interpretations live under one word, and the next sections unpack them. The Milestone is the atomic unit: one pass, one Output, one row.

## 3. The ID scheme

The hierarchy needs stable identifiers so any row can be referenced from any other file. The scheme is small and disciplined, and it is what lets a decision record point at a Goal three months later without ambiguity.

Goals number as `G1`, `G2`. Objectives number globally — `O1`, `O2`, `O3` — regardless of which Goal each belongs to, or hierarchically as `G1.O1`, `G1.O2` when the project carries multiple Goals and you want the parent visible in the ID. Targets take one of two forms. The global form (`T1`, `T2`) reads cleanly when Targets are sparse. The hierarchical form (`T1.1`, `T1.2`, `T2.1`) reads cleanly when each Objective carries several Targets. The project picks one Target form at init and stays with it. Milestones number under their parent — `M1`, `M2`, `M3` — and gain sub-letters when atomic units cluster, producing `M1a`, `M1b`, `M1c`. Each sub-letter row appears separately in the ledger.

Three properties bind every project. IDs are immutable once written. IDs never recycle. Sub-letter expansion runs in one direction: once `M1` splits into `M1a` and `M1b`, the original `M1` row sunsets rather than being edited in place. A sunset Milestone gets a strikethrough — `~~M5~~` — and stays in the ledger forever. The next Milestone takes the next unused number. Forward-ref: `docs/03-discipline-rules.md` R9 names the no-recycling rule formally.

## 4. Two project shapes — g-o-t-m and g-o-m

The hierarchy expresses itself in one of two shapes, and the choice locks at init. The full shape, `g-o-t-m`, makes the Target a first-class node between Objectives and Milestones. Pick this shape when the project carries multiple workstreams under one Objective, when Targets carry their own architectural decisions, or when the work runs across many months — multi-quarter platform builds, multi-workstream initiatives.

A sustainability program under the full shape might lay out as:

    G1 — Become a reference for industry sustainability
      O1 — Cut corporate emissions
        T1.1 — Energy: -30% by Q4 (benchmark)
          M1, M2, M3
        T1.2 — Fleet: 50% electric by next year (benchmark)
          M1, M2

The flat shape, `g-o-m`, folds the Target into the Objective. Pick this shape when each Objective has one named deliverable and the full tree would force compound IDs that do not earn their weight. Evidence-heavy synthesis work fits — a year-end reflection, an account transition, a postmortem. The "Targets" section of the ledger becomes a list of final deliverable file paths rather than a tree level.

A year-end reflection under the flat shape might lay out as:

    G — Produce a year-end self-reflection
      O1 — Project inventory
        M1a — Pull contribution history
        M1b — Pull training records
        M1c — Synthesize the inventory

Both shapes lock at init. Forward-ref: `docs/06-archetypes.md` carries the decision patterns that map a piece of work to the shape that fits it.

## 5. Target style — three interpretations

The Target layer is overloaded across three styles, and the project locks one style at init. The style determines what "done" means for any Target that lives in the project. The table below names the three.

| Style | Meaning | Fit zone | Example |
|---|---|---|---|
| **benchmark** (default) | A quantitative metric tied to a deadline. | Performance work, KPI-driven projects, sustainability targets, quota work. | `T1.1: Reduce p95 latency 850ms → 400ms by Q4` |
| **deliverable** | A named final output file. | Evidence-heavy synthesis, reflections, account transitions, curriculum chapters. | `T1: drafts/annual-reflection.md (final)` |
| **workstream** | A scoped initiative with its own decision record and plan. | Multi-quarter platform builds, software projects with sub-architectures. | `T1.1: Authoring service — see D7` |

The **benchmark** style is the default and fits any project where the success criterion is a number to hit by a date. The Target carries the metric and the deadline; the Milestones under it produce the evidence that the metric has moved. A Target with no measurable end state is not a benchmark, and the audit will flag it.

The **deliverable** style fits evidence-heavy synthesis work where the success criterion is a finished file. The Target names the final output path, and the Milestones under it produce the foundation, the drafts, and the final version. Reflections, reports, and account-transition memos all fit. A deliverable Target without an absolute file path is incomplete; resolve the path before locking it.

The **workstream** style fits multi-quarter platform builds where the Target carries its own architectural decisions and the success criterion is the workstream landing intact. The Target points at a referenced decision record — for example, "see D7." A workstream Target without a linked decision is incomplete; lock the decision first.

Pick one style at init and stay with it. Forward-ref: `docs/06-archetypes.md` walks the decision pattern.

## 6. Outcome-shaped Objectives over process-shaped

When you name an Objective, prefer the **outcome shape** over the **process shape**. An outcome-shaped Objective names the result the work produces — "Topics locked," "Research grounded," "Story-led deck delivered," "Stakeholders aligned." A process-shaped Objective names the activity itself — "Pull data," "Write content," "Run analysis."

The reason is verifiability. You can read the ledger and tell whether an outcome-shaped Objective is done. Outcome-shaped names carry a closure signal — the Objective is either delivered or it is not. A process-shaped Objective bleeds into the Milestones below it, which already carry the verbs. The Objective layer then leaves no clear closure signal at all, and the reader cannot tell whether the workstream has landed.

The heuristic test is short: **if an Objective's name could plausibly become a Milestone title, it is probably shaped as a process.** "Pull customer data" is a Milestone. "Customer data inventoried" is an Objective. Reshape the name to describe the outcome the process produces, and the layer reads cleanly.

A generic worked example. A workshop project once init'd with process-shaped Os — `Architectural credibility`, `Operational readiness`, `Stakeholder alignment`. After two weeks the team recognized those names did not name verifiable outcomes; they named processes. The team restructured to `Topics locked`, `Research grounded`, `Deck delivered`, `Stakeholders aligned` — preserving every Milestone ID below. Only the O layer and the M-to-O mapping changed. The earlier the outcome shape lands, the less re-orientation cost the project pays.

## 7. Layer disambiguation — common confusions

Most layer-assignment errors come from confusing two adjacent layers. Four heuristic tests resolve the common confusions. Read each as a short rule of thumb you can apply at the moment you write a new row.

### Is this a Goal or an Objective?

If you can imagine the project ending and the item still being open-ended, it is a Goal. If completing the item closes the question, it is an Objective. "Become a reference customer in a target industry" stays open after any single project ends — that is a Goal. "Deliver the multi-day workshop on a fixed date" closes when the workshop ends — that is an Objective. Goals point at directions; Objectives point at results. A row that names a direction and reads as "ongoing" sits at the Goal layer. A row that names a result and reads as "ships by a date" sits at the Objective layer.

### Is this an Objective or a Target?

An Objective is the workstream. A Target is the success criterion the workstream chases. `O1 — Cut corporate emissions` paired with `T1.1 — Energy: -30% by year-end` reads correctly — the Objective names what is being pursued; the Target names how much. An item with no measurable end state is probably an Objective in disguise. If the item describes a span of work, place it at the Objective layer. If the item describes the state that closes the work, place it at the Target layer.

### Is this a Target or a Milestone?

A Target is the named end state. A Milestone is one execution pass toward it. `T1: Energy reduction plan published` is a Target — it names the state that closes the workstream. `M3: Identify the top-five energy wasters → research/m3-wasters.md` is one of several Milestones that contribute to the Target. If the item names exactly one output file and represents one execution pass, it is a Milestone. If the item names a state that several passes together produce, it is a Target.

### Is this a Milestone or a sub-task?

If the item produces its own named output file in one pass without depending on a sibling's output, it is a Milestone. If the item cannot reasonably separate from a sibling's output — if running it alone would leave half a result — it is a sub-task, and the parent Milestone needs to be split into sub-letter rows where each carries its own Inputs and Output. A row that lists three or four bullet sub-items in its description is the warning shape. Split the row before the work begins; do not let the sub-items hide.

## 8. Anti-patterns at the hierarchy layer

A short list of common shape errors and the fix for each. Each names the pattern that breaks the hierarchy and the move that restores it.

- **Goal soup.** More than three or four Goals in one project. Either the work is several projects bundled together, or some "Goals" are actually Objectives. Demote the over-broad rows to Objectives, or split the project.
- **Empty Objective.** An Objective with no Targets (in `g-o-t-m`) or no Milestones (in `g-o-m`). The workstream has no work under it. Populate the Objective with at least one Target or Milestone, or drop the Objective.
- **Milestone with bullet sub-items.** A row whose description carries bulleted sub-tasks hides several atomic units under one ID. Split into sub-letter rows. Forward-ref: `docs/03-discipline-rules.md` R2 and R8 name the binding rules.
- **Target without a success criterion.** A Target that names a workstream but no measurable end state is not a Target. Either add the success criterion or demote the row to an Objective.
- **Milestone-as-bucket.** A row titled "M5: Polish" that contains demos, audit, screenshots, PDF export, and deploy is five Milestones, not one. Split into atomic rows, each producing one output.
- **Sibling Milestones with the same Output path.** Two Milestones whose Output column points at the same file. They will silently overwrite each other when the second runs. Split the outputs or split the Milestones into rows that produce distinct files.

## Common pitfall

> **Common pitfall.** Re-litigating layer choices mid-project — re-classifying a row from Goal to Objective two weeks in by editing the original row in place. The intent is to fix a mistake quietly. The result is a ledger whose history can no longer be reconstructed by a later reader. The layer assignment locks at the point the row enters the ledger. If the row was written at the wrong layer, sunset it (strikethrough) and add a new row at the correct layer. The sunset entry preserves the provenance; the new row carries the corrected layer forward. Forward-ref: `docs/03-discipline-rules.md` R9 names the no-recycling rule.
