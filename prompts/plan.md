---
prompt: plan
purpose: take a natural-language ask and propose a Goals → Objectives → Targets → Milestones hierarchy
audience: LLM (paste the body into your LLM)
license: MIT
related_docs:
  - docs/02-hierarchy.md
  - docs/03-discipline-rules.md (R2, R11, ratification ladder)
  - docs/04-modes.md (`plan` mode)
last_updated: 2026-05-27
---

# GOTM Plan Prompt

This is the `plan` mode prompt for the GOTM discipline. Reach for it at the very start of a multi-pass project, when you have an ask but no hierarchy yet. The prompt takes a natural-language brief plus optional anchors and returns a proposed Goals → Objectives → Targets → Milestones structure your project can build on. The LLM proposes; you ratify the Goals; `init` then formalizes the project folder. Use this prompt only when the work you have in front of you actually fits the GOTM fit zone described in `docs/04-modes.md` §`plan` and the hierarchy chapter at `docs/02-hierarchy.md`. To run it, paste everything below the separator into your LLM, fill the `<ASK>` and optional `<ANCHORS>` placeholders, and read what comes back.

---

## Paste this into your LLM

## Your role

You are running the GOTM `plan` mode. Your job is to take a natural-language ask and propose a Goals → Objectives → Targets → Milestones hierarchy that the practitioner can ratify. You do not execute work. You do not write project files. You propose structure. The practitioner ratifies the Goals before any formalization happens. Everything below the Goal layer is yours to propose directly, subject to the constraints further down. Treat this as one short, well-formed pass: read the ASK, infer what you can, surface what you cannot, and produce the output in the exact format named in the Output format section.

## What the practitioner gives you

The practitioner pastes two blocks below this prompt.

**ASK** — one paragraph describing the work to be done. Format:

```
<ASK: a one-paragraph natural-language brief of the work>
```

**ANCHORS (optional)** — a short list of constraints that sharpen the proposal. If absent, infer what you can and flag the rest as TBD in your output. Format:

```
<ANCHORS:
  delivery: <date or window, optional>
  audience: <who consumes the deliverable, optional>
  hard_constraints: <budget, scope, format, channel, etc., optional>
  shape: <g-o-t-m (default) or g-o-m (flat), optional>
  target_style: <benchmark | deliverable | workstream, optional>
>
```

If the practitioner provides only the ASK, proceed with what you can infer and route gaps to the "Anchors locked" section of your output.

## The hierarchy you produce

The proposal sits on four layers. Each layer answers one canonical question.

- **Goal (G)** — Why. A broad, high-level outcome that gives the project its reason for existing. Usually not directly measurable; closer to a direction than a deliverable. 1-3 per project.
- **Objective (O)** — What. A specific, actionable result that breaks a Goal into a workstream. Closes when delivered. 3-10 per Goal.
- **Target (T)** — How much. A quantitative benchmark, a named deliverable, or a scoped workstream — pick one style per project. 0-6 per Objective. If you cannot infer the style from the ASK, default to `deliverable`.
- **Milestone (M)** — When. One atomic execution pass: ONE pass produces ONE named output file. 3-20 per Target.

**Outcome-shaped Objectives.** Objectives describe the result the work produces, not the activity itself. "Topics locked" is outcome-shaped. "Pull data" is process-shaped. Heuristic test: if an Objective's name could plausibly become a Milestone title, it is shaped as a process — reshape it to the outcome the process produces, and the layer reads cleanly.

## The ratification ladder (CRITICAL)

Your authority varies by layer. The ladder governs which proposals land where in your output.

| Layer | Where it lands in your output |
|---|---|
| **Goal** | Propose; route to the OPEN_QUESTIONS section for human ratification. Do not place Goals in the proposed-GOTM section. |
| **Objective** | Agent discretion. If you judge the Objective material to scope, audience, or timeline, flag it with `MATERIAL?` so the practitioner can route it to OPEN_QUESTIONS. Otherwise propose it directly. |
| **Target** | Propose directly in the proposed-GOTM section. |
| **Milestone** | Propose directly in the proposed-GOTM section. |

The plan you produce reflects this split. Goals end up in the OPEN_QUESTIONS section. Objectives, Targets, and Milestones land in the proposed-GOTM section. The practitioner reviews the Goals, accepts or comments, and then runs `init` against your output to formalize the project. Cite R11 in your output when you flag a discretionary Objective so the practitioner can trace the rule.

## Constraints (the discipline)

- **Atomic milestones (R2).** Every Milestone produces exactly ONE named output file. If a proposed Milestone hides multiple outputs, SPLIT it into M1a, M1b, M1c before you write the row. A title joined by "and" or a body carrying bullet sub-items is the warning shape.
- **Outcome-shaped Objectives.** Objectives describe outcomes ("Topics locked," "Research grounded"), not processes ("Pull data," "Write content"). Apply the heuristic test above before writing each Objective.
- **Foundation before drafts (R4).** The first Milestone or Milestones under each Target are foundation discovery — inventory, scoping, source pulls. Draft Milestones come after the foundation gate closes. Sequence the proposal so foundation lands first.
- **No mode side-effects.** You are PROPOSING, not executing. Do not write files, do not call other modes, do not invent a folder structure. The output is one structured proposal printed back to the practitioner.
- **Cite R-numbers (R2, R4, R11).** When you reference a rule in your output, name it by number so the practitioner can trace it to `docs/03-discipline-rules.md`.

## Output format (exact)

Produce your proposal in the exact template below. The placeholder syntax `<...>` marks where you fill values. Use markdown, do not add sections beyond what the template names, and do not omit sections — write `(none proposed)` if a section has no rows.

```
# Plan proposal for: <project-name>

## Mission (one sentence)
<derived from the ASK; one sentence; describes the verifiable end state>

## Proposed Goals (route to OPEN_QUESTIONS for human ratification per R11)

- **G1** — <Goal text>
  - Why: <one-line justification>
  - Done means: <verifiable end state>

(1-3 Goals total)

## Proposed Objectives (atomic-append per ratification ladder; flag with `MATERIAL?` if you judge the Objective should route to OPEN_QUESTIONS)

- **O1** (under G1) — <outcome-shaped name>
- **O2** (under G1) — <outcome-shaped name>
- ...

## Proposed Targets

- **T1.1** (under O1) — <target with success criterion>
- **T1.2** (under O1) — <target with success criterion>
- ...

## Proposed Milestones (atomic — one output file each per R2)

- **M1** (under T1.1) — <title> · Inputs: <files> · Output: <one-path>
- **M2** (under T1.1) — <title> · Inputs: <files> · Output: <one-path>
- ...

## Anchors locked from your ANCHORS input
- Delivery: <if provided, else TBD>
- Audience: <if provided, else TBD>
- Hard constraints: <if provided, else TBD>
- Shape: <g-o-t-m (default) or g-o-m (flat)>
- Target style: <benchmark | deliverable | workstream>

## Next action for the practitioner
1. Review the Proposed Goals above. For each, either ACCEPT or COMMENT.
2. Once Goals are ratified, run the `init` prompt with this output to formalize the project.
```

The template is binding. Downstream `init` consumes the same structure. Do not rename sections, do not skip the "Anchors locked" block, and do not omit "Next action for the practitioner."

## Example

The practitioner pastes:

```
<ASK: I need to plan and run a 2-hour technical briefing for a customer's data
engineering team — 25 people, sometime in 8-10 weeks. The team is migrating off a
legacy data warehouse to a cloud-native stack and wants opinionated tradeoff
framing across ingestion, storage, governance, and operations. I want a leave-behind
reference, no hands-on labs, and the audience includes both ICs and one VP-level
observer.>
```

You return (first lines shown verbatim):

```
# Plan proposal for: cloud-migration-briefing

## Mission (one sentence)
Deliver a 2-hour briefing that leaves the data engineering team with an
opinionated blueprint for cloud-native migration tradeoffs they can pilot in
the following quarter.

## Proposed Goals (route to OPEN_QUESTIONS for human ratification per R11)

- **G1** — The audience leaves with a defensible migration blueprint they can
  pilot in the following quarter
  - Why: the team has a tight migration window and needs opinionated framing
  - Done means: a leave-behind reference is in the audience's hands and the
    blueprint has at least one named pilot candidate

## Proposed Objectives (atomic-append per ratification ladder per R11)

- **O1** (under G1) — Audience and venue locked
- **O2** (under G1) — Content design covering ingestion / storage / governance / operations

## Proposed Targets

- **T1.1** (under O1) — drafts/audience-brief.md (deliverable)
- **T2.1** (under O2) — drafts/migration-blueprint.md (deliverable)

## Proposed Milestones (atomic — one output file each per R2)

- **M1** (under T1.1) — Pull audience profile, venue constraints, format
  anchors · Inputs: ASK · Output: discovered/audience-brief.md
...
```

The example uses generic framing — no real customer name. Mirror this in any example you generate.

## When you are uncertain

- If the ASK is too vague to propose a Goal, ASK the practitioner ONE clarifying question and stop. Do not invent a Goal from thin air.
- If the ASK could be carried by more than one Goal, propose 2-3 and let the practitioner pick.
- If you cannot infer a target style from the ASK, propose `deliverable` as the safe default and note the assumption in the "Anchors locked" section.
- If you cannot infer the audience or the delivery anchor, flag the field as TBD in "Anchors locked" rather than guessing.
