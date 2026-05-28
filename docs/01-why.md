---
chapter: "docs/01-why.md"
title: "Why GOTM exists"
audience: "LLM practitioners running complex multi-pass work"
word_target: 2500
produced_by: subagent
last_updated: 2026-05-27
project: gotm-framework-for-agentic-development
inputs:
  - discovered/source-to-target-map.md
  - gotm-playbook/01-theory/README.md (Modules 1.1, 1.2, 1.3, 1.5)
voice_calibrated_against: gotm-playbook/discovered/foundation-inventory.md §5.2
---

# Why GOTM exists

## 1. The view from inside complex work

Complex work fails in a way that is hard to see from inside. The plan lives in your head. You hold it together by re-reading scrollback and reconstructing the project at the start of every session. For a one-day task this is fine. For work that spans weeks and produces evidence-heavy output, this is the failure mode.

The shape of the failure is not dramatic. There is no crash. The work produces an output that looks complete and turns out, on review, to be wrong in a way nobody caught at the time. A reader asks where a number came from. A peer notices a claim with no source behind it. A status report reads "in progress" for the fourth week in a row, and no one can say whether the work is nearly done or barely started.

Three patterns recur across multi-pass work of this shape. Plans dissolve between sessions. Drafts get built on partial evidence. Milestones grow into aggregates that hide several sub-tasks under one row. If you have run a multi-week research project, an evidence-heavy report, or a curriculum build, you have probably already seen at least one of these in your own work.

This chapter sets up the discipline that resolves them. It names the three failures in archetype form, lays down the four principles that defend against each, gives you a rubric for deciding whether the discipline fits the work in front of you, and places GOTM against the planning frameworks you may already use. The aim is not to recruit. The aim is to give you enough to decide.

## 2. Three failure archetypes

Three short stories, drawn as archetypes from real multi-pass work. Each is anonymized. Each names one failure. Each ends with a lesson you can carry into your own projects.

### The vanishing plan

A team ran a market-research project across four working sessions. The lead analyst held the plan in a series of long chat messages with a coding agent. At the start of each session she pasted the goals, the open questions, and the current best guess at the customer segment back into the conversation. The re-grounding step took fifteen minutes at the top of each session. It felt like overhead.

By session four she was tired and skipped the step. The agent had no memory of the previous three sessions. It picked up from the last message in scrollback, which was a follow-up about pricing tiers. The agent produced confident output that drew on the wrong assumption about the customer segment. The output read clean. The analyst built a follow-on analysis on top of it the next morning. A peer reviewer caught the segment mismatch two days later. Both deliverables were rewritten. The original plan had never lived anywhere outside the chat window.

**Lesson: scrollback is not a plan.**

### The draft on sand

A report author was 90% through an annual reflection draft when she realized one of her sources had never actually been pulled. The export had timed out in week one. She had noted the gap in her head, intended to retry, and started drafting because the deadline was tightening. The draft read well. Each section connected to the next. Two conclusions in section three rested on the missing source — figures she had filled in with what she expected the export to show.

The review meeting opened the draft and worked through the claims in order. Three claims had no evidence behind them. One contradicted a log line nobody had pulled. The draft was returned. The two failed exports were retried, which took an afternoon. Both conclusions in section three had to be rewritten. The original draft had been built on a partial foundation. The gaps were invisible at the time the draft was written.

**Lesson: the cost of a partial foundation is invisible at draft time.**

### The hidden six

A quarterly-review author kept a single line on his task list: "polish the deck." His status flag read "in progress" for three weeks. The line was not one task. It hid six distinct sub-tasks. He needed to update three charts against fresh data. He needed to add a section that had been requested late. He needed to rebuild one diagram to match an architecture change. He needed to run a fact-check pass across the whole deck. He needed to refresh the screenshots. And he needed a final read-through against the brief.

By week three, five of the six were done. The sixth — the final read-through — required all the others to be at hand simultaneously, fresh enough to compare against the brief. The status board still read one milestone in progress. Nobody on the outside could tell whether the work was nearly done or barely started. The reality was five-of-six done and the hardest one not yet begun.

**Lesson: a milestone containing six outputs is six milestones.**

The three stories share one root. Working memory cannot hold a multi-pass project. The plan, the foundation, and the shape of each unit of work all need to live outside the chat window, outside scrollback, and outside the worker's own head between sessions. Each failure is invisible from inside the work and obvious from outside it. The fix in every case is the same shape: move the plan, the foundation, and the unit-of-work definition into a durable file the next session can read fresh.

## 3. The four foundational principles

Four principles resolve the three failures. Each is a present-tense rule. The four govern where the work lives, how big a unit of work is, what a unit of work can carry, and what must be true before a draft begins.

### P1 — The ledger is the project

A single external file holds every plan, every status change, every decision, and every newly discovered piece of scope. The file is not a description of the project or a report about it. It is the project. When the file and reality disagree, you fix the file first. The contents of working memory are not the project. The contents of the file are.

This principle works because durable text survives context resets, idle weeks, and the gap between Tuesday and Friday. The next session does not start from scrollback. It starts from the file. Treat the file this way and a context reset becomes a small event, not a recovery.

P1 prevents the vanishing plan. The plan no longer lives in working memory.

### P2 — Milestones are atomic

One Milestone equals one execution pass equals one named output file. If a Milestone hides two or more sub-tasks, it is two or more Milestones. You split it before you start.

This principle works because status math becomes honest. A Milestone is either done or not done. There is no halfway. The progress board reads what reality is. A single output file per Milestone also gives every fact a clear provenance. You can answer "where did this come from" by pointing to one file.

P2 prevents the hidden six. Aggregate Milestones cannot survive the rule.

### P3 — Milestone equals max context unit

Each Milestone declares its Inputs — the foundation files the pass will read — and produces one Output. The pass reads only the listed Inputs. Inside a Milestone, loops and revisions are fine. Across Milestones, working memory does not survive. The next pass reads its declared inputs fresh.

This principle works because paraphrase from memory is not paraphrase from source. A file read three weeks ago does not match a file re-read this morning. The threshold inverts, the figure shifts, the caveat goes missing. Re-reading costs seconds and prevents a class of silent error that no review catches reliably. The discipline assumes a single writer across the project's life — one parent driving one ledger. Multi-writer topologies need different tooling.

P3 prevents paraphrase-from-memory errors. Each pass reads the source.

### P4 — Foundation before drafts

For any evidence-heavy deliverable, the foundation is verifiably complete before a draft begins. Verifiable means the gap ledger holds no unresolved high or medium items, failed pulls were retried rather than silently deferred, and newly discovered sources were added to the gap ledger and processed before drafting starts.

This principle works because you cannot feel the gaps in your own draft. The reader can. A draft built on nine out of twelve sources fills the three missing ones with what you expected the evidence to show. Gating drafts on a closed foundation is the only reliable defense against confidently wrong output.

P4 prevents the draft on sand. The draft does not begin until the foundation closes.

These four principles are the load-bearing skeleton. The eleven discipline rules in `docs/03-discipline-rules.md` expand them. The modes in `docs/04-modes.md` operationalize them.

## 4. What "complex" actually means

The four principles assume the work is complex enough to need them. Applied to a half-hour task, they are overhead. This section is a calibration tool, not a recruiting pitch. The question is not whether the discipline is good. The question is whether your work is the shape that the discipline pays back.

### Use GOTM when

Run the eight criteria below against the work in front of you. Three or more true is a strong signal. Five or more is unambiguous.

1. The work has five or more distinct execution passes. You count passes, not pages.
2. The work spans days or weeks and must survive context resets across that span.
3. The work has heavy foundation requirements before any drafting starts.
4. Multiple sub-passes will be delegated to subagents or sub-sessions.
5. The deliverable is high-stakes — a draft that looks complete on partial data destroys credibility with the reader.
6. Discovery during execution routinely surfaces new scope you did not plan for.
7. The project will be paused and resumed across days or weeks.
8. Auditability matters — you, a reviewer, or a future-you needs to verify the work later.

### Do not use GOTM when

Run the six anti-criteria below against the same piece of work. Three or more true is a strong signal that the framework will add friction without value.

1. The work is a one-off task fitting one sitting.
2. The pace is real-time operational — incident response, live ops, on-call paging.
3. The deliverable is content writing with no research phase.
4. The spec is stable and there is no discovery — two or three known steps and done.
5. The work is pure open-ended exploration with no goal yet.
6. The work needs several humans writing to a shared plan at the same time.

The rule of thumb: if you can credibly imagine three sessions where the second needs context from the first, GOTM is worth it. If two sessions get you done and the second is mostly polish, a task list is enough.

## 5. How GOTM relates to frameworks you may already know

Every framework that survives external use names its neighbors. A reader who has run quarterly planning, shipped under sprint cadence, or moved cards across a board already owns tools that handle parts of what GOTM handles. The comparison is descriptive. The aim is to mark where each tool sits and where one ends and another begins.

**GOTM vs OKRs.** Shared: a hierarchy of intent, with broader outcomes above and narrower work below. Different: OKRs operate at quarterly or annual cadence and measure team-level outcomes as metrics. GOTM operates at per-Milestone execution cadence and produces atomic output files. A Milestone is a pass, not a metric to move. You reach for OKRs to align a team on outcomes over a quarter. You reach for GOTM to run one multi-pass project to a known finish.

**GOTM vs agile and scrum.** Shared: iteration with explicit work units, a durable backlog, regular plan-execute-review cadence. Different: scrum is team-oriented, sized for a sprint, with planning as a meeting. GOTM is single-writer; the ledger update is paired to the file edit, not to a scheduled ceremony. You reach for scrum when several humans coordinate a product over months. You reach for GOTM when one driver runs one project across many sessions.

**GOTM vs kanban.** Shared: work-in-flight discipline, limits on parallel work, a single visible source of truth. Different: kanban tracks cards through states. A card can move into in-progress with whatever foundation the worker has gathered. There is no atomic-output rule on a card and no gate that holds the draft column until foundation closes. GOTM names both. You reach for kanban when a steady stream of similarly-shaped work flows past a small team. You reach for GOTM when one project demands foundation before draft and the foundation is bigger than the draft.

**GOTM vs ad-hoc LLM prompting.** Shared: both use an LLM. Different: ad-hoc prompting in tools like ChatGPT, Cursor, Cline, Continue, or a direct Claude API session holds the plan inside the conversation. Each prompt is the whole world for that turn — no external ledger, no atomic units, no foundation gate. GOTM externalizes all three. The trade is overhead for durability: ad-hoc is faster to start, GOTM is faster to resume. Ad-hoc has its own fit zone — rapid prototyping, exploration, single-pass work — and is not lesser. It runs at a different cadence.

GOTM has a fit zone. The fit zone is narrower than its enthusiasts suggest. Use the framework where it earns its keep. Use other things elsewhere.

## Common pitfall

> **Common pitfall.** Adopting GOTM because the discipline sounds rigorous, on work that does not actually need it. The framework reads as serious, and seriousness gets mistaken for fit. Count execution passes before you scaffold. If the work fits one sitting, use a task list and move on. The fit-test in section 4 is the gate. Forty minutes scaffolding twelve minutes of work is theatre, not discipline.
