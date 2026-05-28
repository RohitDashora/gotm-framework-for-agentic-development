---
chapter: "docs/06-archetypes.md"
title: "The four project archetypes"
audience: "LLM practitioners running complex multi-pass work"
word_target: 2400
produced_by: subagent
last_updated: 2026-05-27
project: gotm-framework-for-agentic-development
inputs:
  - docs/01-why.md through docs/05-audit-family.md (M3-M7 — voice + cross-ref)
  - gotm-playbook/03-patterns/README.md (Module 3 source)
voice_calibrated_against: gotm-playbook/discovered/foundation-inventory.md §5.2
---

# The four project archetypes

## 1. Why archetypes matter

`docs/01-why.md` §4 named the fit-test. `docs/02-hierarchy.md` taught the four layers. With both in hand, one question remains: what shape does the work take in your situation. The archetype is the answer.

Four canonical archetypes cover most of the multi-pass work practitioners encounter — a software or platform build, an evidence-heavy synthesis, a time-bound event delivery, and a quantitative goal pursuit. The shape differs across them. The discipline does not. Every archetype runs on the same G/O/T/M hierarchy, the same eleven rules, the same eight modes. What changes is where the foundation gate falls, which target style fits, and which rules carry the most weight.

This chapter teaches recognition (which archetype fits your project) and decomposition (what G/O/T/M looks like once the archetype is named).

## 2. The four-question rubric

The rubric is four anchor questions. Read them in order; the first "yes" names the archetype. Ordering matters — the more structurally constraining shapes are tested first, because mis-typing them produces the most expensive rework.

| Order | Anchor question | Archetype |
|---|---|---|
| 1 | Is the deliverable a running system that other people use? | A — Software / platform build |
| 2 | Is the deliverable a documented finding that aggregates evidence from multiple sources? | B — Evidence-heavy synthesis |
| 3 | Is there an external delivery date with an audience, and is the artifact consumed live? | C — Time-bound event delivery |
| 4 | Is success defined by a measurable target that must be hit? | D — Quantitative goal pursuit |

A project may answer "yes" to more than one question. The first "yes" wins. When two questions both apply, name the archetype whose foundation gate locks the first phase. §8 walks the two common straddles.

## 3. Archetype A — Software / platform build

**Defining attributes.** The output is a running system that downstream users depend on across versions. Releases land on a cadence; each cycle reopens scope. The work is architectural-decision-heavy and repository-anchored — the codebase is the source of truth, the ledger sits alongside it.

**Typical Goal shape.** Open-ended platform vision — rarely fully achievable inside one planning horizon. The Goal names a system and a class of user and stays stable while the work below it changes shape every cycle. Example: a self-service data catalog tool for an engineering organization, where engineers register, discover, and govern internal datasets without routing requests through a central team.

**Typical Objective shape.** Workstreams under the platform vision — authoring surface, deployment and runtime, governance, telemetry.

**Typical Target style.** Workstream (`docs/02-hierarchy.md` §5). Each Target is a scoped initiative with its own decision record. Benchmark and deliverable do not fit.

**Typical Milestone shape.** Component build → integration → release. Each cycle produces fresh atomic Milestones. Decision-record references appear in the Inputs block of every component-build pass.

**Worked decomposition.** A team set out to build the data catalog tool above. They split the work into three workstreams and wrote architectural decisions before any component build started.

        G1 — A self-service data catalog tool for the engineering organization
          O1 — Authoring surface
            T1.1 — Schema editor (see D7)
              M1.1a — Schema editor component build
              M1.1b — Preview renderer component build
              M1.1c — Save and validation flow build
              M1.1d — Integration pass — wire components together
          O2 — Ingest pipeline

The team identified three components under T1.1 that could build in parallel and sub-numbered them M1.1a, M1.1b, M1.1c. Each produced one component as its Output. Integration landed as M1.1d once the three closed.

**Foundation pattern.** Research → architecture → decision records → component builds → release. The gate holds component-build Milestones closed until the decisions for the active Target have landed in `decisions.md`.

**R-rules most active.** R5 carries the most weight because software work has a high commit cadence and decoupled updates compound into drift fast. R10 governs the parallel component-build fanout; each sub-numbered Milestone gets its own subagent with the decision record and component contract as Inputs.

**Common pitfall.** Skipping decision records and proceeding straight to component builds. The work feels faster for two days; then unwritten decisions get re-litigated mid-build inside pull-request threads. The fix: treat decisions as foundation. No component build starts while a contested decision is unwritten.

## 4. Archetype B — Evidence-heavy synthesis

**Defining attributes.** The work aggregates facts from many sources into a verified, traceable finding. There is no running output to test against. The deliverable is a named document, trustworthy only if every claim walks back to a raw extract.

**Typical Goal shape.** A finding to be produced, the period it covers, the audience that consumes it. The Goal has a fixed scope window and a single named reader. Example: an annual cross-team impact reflection covering eight projects across the last four quarters, written for senior leadership.

**Typical Objective shape.** Evidence tracks — one Objective per source family. Calendar and events. Financial and contract records. Stakeholder conversations. Telemetry and system metrics.

**Typical Target style.** Deliverable. Each Target names the final file with a word-count band and a voice expectation. The file at the named path is the success criterion.

**Typical Milestone shape.** Strict layering — raw extract → discovered → research → synthesized → drafts → final. Each evidence pull and each synthesis pass is one atomic Milestone with one named Output.

**Worked decomposition.** A team scoped the annual reflection above into three evidence tracks and two deliverable Targets. Foundation pulls were lined up before any drafting began.

        G1 — Produce a verified annual reflection across the last four quarters
          O1 — Calendar and event evidence
            M1a — Pull Q1 calendar export → raw/q1-cal.csv
            M1b — Pull Q2 calendar export → raw/q2-cal.csv
            M1c — Pull Q3 calendar export → raw/q3-cal.csv
            M1d — Synthesize the three pulls → discovered/cal-summary.md
          O2 — Financial and contract evidence
          T1 — drafts/annual-reflection.md (~3,500 words)

The team identified three atomic pulls under O1 that could run in parallel — one per quarter — and sub-numbered them M1a, M1b, M1c. M1d synthesized the three into a per-source view at the discovered tier. Each pull ran with foundation-only Inputs; the synthesis pass read all three at once rather than reconstructing them from memory.

**Foundation pattern.** Bottom-up filling — raw extracts arrive untouched, discovered files reconcile each source against the raw layer, synthesized files reconcile across families, and only then does the draft tier unlock. The gate is the strictest expression of `docs/03-discipline-rules.md` R4 across the four archetypes.

**R-rules most active.** R3 governs each evidence pull as its own pass with foundation-only Inputs. R4 is the central discipline. R11 carries the constant load because pulls routinely uncover sources the original scope did not name.

**Common pitfall.** Drafting because the foundation "looks close enough." High-confidence sections get written; low-confidence sections get softened; the reader is left to spot the difference. The fix: drafts block until the gap ledger shows zero High and Med entries.

## 5. Archetype C — Time-bound event delivery

**Defining attributes.** The work centers on an external delivery date that cannot slip — a workshop, a launch, a customer briefing, a partner session. A live audience consumes the artifact in real time. The foundation gate falls on audience and venue closure.

**Typical Goal shape.** A defined audience, a defined moment, and the value the audience walks away with. The Goal carries a fixed delivery date. Example: a one-day workshop for roughly thirty mid- and senior-level engineers at a client organization, giving the audience a working blueprint they can apply after the event.

**Typical Objective shape.** The canonical phases of event delivery — audience analysis, content design, logistics, materials.

**Typical Target style.** Deliverable, or workstream at larger scale. Deliverable is dominant when the agenda, slides, and leave-behind are the named outputs. Workstream fits when multi-track agendas or venue complexity warrant decision-record coordination.

**Typical Milestone shape.** Discover audience and constraints → research content → synthesize agenda and visuals → produce the final deliverable. Each phase is one atomic Milestone. No slide work starts while audience or venue gaps sit open.

**Worked decomposition.** A team set out to deliver the workshop above. They locked the audience profile and venue first, then sequenced content and materials behind that lock.

        G1 — Deliver a one-day workshop with a working blueprint the audience can apply
          O1 — Audience and venue
            M1 — Produce the audience brief → discovered/audience-brief.md
          O2 — Content
            M2 — Produce the content research file → research/content-research.md
          O3 — Materials
            M3 — Produce the agenda and visuals plan → synthesized/agenda.md
            M4 — Produce the leave-behind deck → drafts/leave-behind.md

M1 produced the audience brief — seniority mix, prior context, entry point, venue constraints. M2 ran content research against the brief. M3 synthesized the agenda; M4 produced the leave-behind. Audience and venue closed before materials work began. When the host added a session-length constraint two weeks before the date, the ledger absorbed the change before drafting resumed.

**Foundation pattern.** Audience and venue lock → content research → agenda and visuals synthesis → materials drafts. The lock prevents a late audience pivot from invalidating materials drafted on stale assumptions.

**R-rules most active.** R1 carries the most weight near the delivery date when rapid late-stage edits demand one source of truth. R4 holds materials behind audience-and-venue closure. R11 carries the constant late surface as audience research uncovers new constraints.

**Common pitfall.** Drafting slides before the audience profile and format are signed off. The deck looks complete; the audience profile lands two weeks out and forces a rewrite. The fix: slides do not start until audience, venue, and format are locked.

## 6. Archetype D — Quantitative goal pursuit

**Defining attributes.** The work centers on a single measurable target — one named metric — and a time-bound deadline. Success is binary. The work runs as multiple parallel hypothesis tracks, each a distinct causal path toward the metric.

**Typical Goal shape.** The metric, the starting value, the target value, the deadline. The Goal names a number that must move. Example: reduce a product's monthly customer churn from 8% to 5% in two quarters.

**Typical Objective shape.** Hypothesis tracks — one Objective per lever. Onboarding friction. Pricing. Support response time. In-product friction. Each closes when its hypothesis is either validated against the target metric or ruled out by a clean negative.

**Typical Target style.** Benchmark (`docs/02-hierarchy.md` §5). Each Target is a quantitative success criterion paired with a deadline — the same metric as the Goal, scoped to one Objective's lever.

**Typical Milestone shape.** Baseline measurement → hypothesis test → implementation → post-change measurement → iterate. Baseline pulls land first and lock the comparison frame. Post-change measurement runs against the same instrument and cohort as the baseline.

**Worked decomposition.** A team chased the churn-reduction target above. They scoped three hypothesis tracks and sequenced foundation — instrumentation, cohort definition, locked baseline — before any experiment Milestone began.

        G1 — Reduce monthly customer churn from 8% to 5% in two quarters
          O1 — Onboarding friction
            T1.1 — Week-one activation ≥ 70% by the end of Q3
              M1 — Baseline measurement (locked cohort)
              M2 — Change deployment — ship the revised onboarding flow
              M3 — Post-change measurement on the same cohort
          O2 — Pricing
          O3 — Support response time

Under O1, the team identified week-one activation as the sub-target. M1 instrumented the metric and captured baseline; M2 deployed the change; M3 re-measured on the same instrument. The baseline closed before M2 ran. When M3 surfaced movement on a second metric the team had not expected, the discovery landed as a new Objective rather than as inline scope on the active Target.

**Foundation pattern.** Instrumentation → cohort definition → baseline measurement → experiment cycles. Without a locked baseline, attribution is impossible — the team cannot tell whether the metric moved because of the intervention or because of background drift.

**R-rules most active.** R4 reads here as baseline before experiments; changes do not ship until the baseline file lands. R11 carries the second-most weight because measurement routinely surfaces unexpected drivers, and new levers land as new Objectives.

**Common pitfall.** Declaring success on a proxy metric that did not move the target. Activation rises; churn does not. The proxy looks good in the dashboard and the team marks the Target done. The fix: success requires post-change measurement against the same baseline, metric definition, and cohort.

## 7. What the archetypes share and how they differ

The shared discipline holds across all four. Every archetype uses the G/O/T/M hierarchy, is gated by R4, expands the ledger via R11, and locks decisions append-only in `decisions.md`. The modes in `docs/04-modes.md` and the audit family in `docs/05-audit-family.md` operate identically. Variation lives in foundation shape and dominant target style.

| Archetype | Target style | Foundation shape | Time-to-first-deliverable | Most-active R-rules |
|---|---|---|---|---|
| A — Software build | Workstream | Research → architecture → decision records | Longer | R5, R10 |
| B — Evidence synthesis | Deliverable | Multi-source extraction → reconciliation | Shorter | R3, R4, R11 |
| C — Event delivery | Deliverable or workstream | Audience and venue lock | Shorter | R1, R4, R11 |
| D — Quantitative pursuit | Benchmark | Baseline metrics and instrumentation | Longer | R4, R11 |

A and D run longer because serial foundation work gates every draft-tier Milestone. B and C reach a first deliverable faster but carry heavier discovery. The audit kinds in `docs/05-audit-family.md` distribute accordingly: A leans on code-artifact, B on content-claim, C on UI/render, D on foundation-files and completion-verification.

## 8. Straddle cases — how to pick when two archetypes apply

Real projects sometimes straddle. Two combinations recur often enough to name.

The first is the platform launch with a live demo — A and C together. One team built an authoring environment over six months and ran a live demo at the end. Decision records gated every component build for five of those six months; the audience-and-venue lock applied only to the final phase. The team carried the work as A, with the demo as a final-phase Objective.

The second is the reduction effort that publishes a written report — D and B together. One team chased a churn-rate target across two quarters and produced an end-of-quarter report. Baseline measurement gated every experiment before any draft began. The team carried the work as D, with the report as a final synthesis Objective.

The rule resolves both: name the archetype whose foundation gate governs the first phase.

## Common pitfall

> **Common pitfall.** Declaring an archetype from the deliverable's surface label rather than from the foundation shape. A launch project gets called Archetype A because the team builds a platform — but if the live event drives every late-stage Milestone and the gate is audience plus venue plus format, the project is Archetype C. The fix: walk the rubric in §2 in order, then name the archetype whose foundation gate governs the first phase. Straddle mis-identification is a leading source of the compound failures named in `docs/03-discipline-rules.md`.
