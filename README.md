# GOTM — Goals · Objectives · Targets · Milestones

A framework for running complex multi-pass agentic work without losing the thread.

## The problem GOTM solves

You are four sessions into a multi-week research project. The plan lives in your head. At the start of each session you paste the goals, the open questions, and the current best guess at the framing back into the conversation. The re-grounding step takes fifteen minutes at the top of every session. It feels like overhead.

Session four, you are tired, and you skip it. The LLM has no memory of the prior three. It picks up from the last message in scrollback, which happens to be a follow-up about something tangential. The model returns confident output that draws on the wrong assumption about the core question. The output reads clean. You build a follow-on analysis on top of it the next morning. Two days later a peer reviewer catches the mismatch. Both deliverables are rewritten. The original plan had never lived anywhere outside the chat window.

This is the *vanishing plan* — one of three recurring failure shapes when an LLM-driven workflow spans more than a single sitting. The other two: drafts built on partial evidence that nobody can feel are partial, and "milestones" that quietly contain six sub-tasks hiding under one row. All three are invisible from inside the work and obvious from outside it. GOTM is the discipline that prevents them.

## What GOTM is

GOTM is a four-layer hierarchy — Goals (why), Objectives (what), Targets (how much), Milestones (when) — held in a single external ledger file the next session reads fresh. The discipline runs on three load-bearing rules: the ledger is the project, Milestones are atomic (one pass, one output file), and the foundation closes before any draft begins. A small mode set (`plan`, `init`, `run`, `audit`) operationalizes the hierarchy as paste-able prompts you drop into your LLM.

GOTM is not a tool. There is no runtime to install, no agent framework to adopt, no SaaS to subscribe to, and no opinion about which model provider you use. It is a discipline and a set of prompts. The LLM you already use runs it.

## When to use GOTM

Use GOTM when:

- The work has five or more distinct execution passes
- The work spans days or weeks and must survive context resets
- The deliverable is evidence-heavy and a draft on partial data destroys credibility
- Sub-passes will be delegated to subagents or sub-sessions
- Discovery during execution routinely surfaces new scope
- A reviewer or future-you needs to audit the work later

Do not use GOTM when:

- The work fits one sitting
- The pace is real-time operational (incident response, live ops)
- The deliverable is content writing with no research phase
- The spec is stable — two or three known steps and done
- The work is open-ended exploration with no goal yet
- Several humans need to write to the shared plan at the same time

Rule of thumb: if you can credibly imagine three sessions where the second needs context from the first, GOTM is worth it. If two sessions get you done and the second is mostly polish, a task list is enough.

## What's in this repo

```
docs/         6 concept chapters (~15k words)
prompts/      13 self-contained prompts you paste into your LLM
templates/    5 scaffold files you copy into a new project folder
```

`docs/` carries the concept material — why the discipline exists, the four layers, the eleven rules, the modes, the audit family, the project archetypes. `prompts/` carries the orchestration prompts (`plan`, `init`, `run`), eight audit prompts, and two subagent dispatch templates. `templates/` carries the five ledger scaffolds (`GOTM`, `STATUS`, `decisions`, `OPEN_QUESTIONS`, `README`) you fork into your project folder.

Everything is platform-neutral markdown. Paste any prompt into ChatGPT, Cursor, Cline, Claude API, or raw chat — it works.

## Quickstart — your first GOTM project in 5 steps

1. **Pick a piece of work that fits.** Run the §When to use checklist against the work in front of you. Three or more use-when signals true, fewer than three do-not-use signals true, at least five multi-pass Milestones in view. If the work does not clear the test, stop here. A task list is enough.

2. **Plan.** Open [`prompts/plan.md`](prompts/plan.md), paste it into your LLM, and append one paragraph describing your ask. Add optional anchors (delivery date, audience, hard constraints) below the ask. The LLM returns a proposed Goal → Objective → Target → Milestone hierarchy with the Goals routed to a ratification block.

3. **Ratify the Goals.** Review the proposed Goals. Accept or comment. The Objectives, Targets, and Milestones below are the LLM's discretion to propose — you override later if needed.

4. **Init.** Open [`prompts/init.md`](prompts/init.md), paste it into your LLM along with your ratified plan. The LLM emits five scaffold files — `GOTM.md`, `STATUS.md`, `decisions.md`, `OPEN_QUESTIONS.md`, `README.md`. Save them in a new folder. That folder is now your project.

5. **Run.** Open [`prompts/run.md`](prompts/run.md) and use it iteratively. Each invocation advances one Milestone, either in-loop or by returning a subagent dispatch prompt you paste into a worker LLM. The ledger updates pair with the file edits — same turn, not later.

From there, the audit prompts (`prompts/audit-*.md`) let you verify your work as you go. See `docs/` for the concept chapters.

## Concept chapters

- [`docs/01-why.md`](docs/01-why.md) — why GOTM exists; the three failure archetypes; the four foundational principles; the fit-test
- [`docs/02-hierarchy.md`](docs/02-hierarchy.md) — the four layers; ID scheme; two project shapes; three target styles; layer disambiguation
- [`docs/03-discipline-rules.md`](docs/03-discipline-rules.md) — the eleven R-rules and the ratification ladder
- [`docs/04-modes.md`](docs/04-modes.md) — the eight modes and their dispatch rules
- [`docs/05-audit-family.md`](docs/05-audit-family.md) — the eight audit kinds and the severity tiers
- [`docs/06-archetypes.md`](docs/06-archetypes.md) — four project archetypes and which one fits your work

## Prompts and templates

- [`prompts/plan.md`](prompts/plan.md), [`prompts/init.md`](prompts/init.md), [`prompts/run.md`](prompts/run.md) — orchestration prompts
- [`prompts/audit-*.md`](prompts/) — eight audit prompts, one per audit kind
- [`prompts/subagent-execution.md`](prompts/subagent-execution.md), [`prompts/subagent-audit.md`](prompts/subagent-audit.md) — worker-prompt conventions
- [`templates/`](templates/) — copy-and-fill scaffolds for `GOTM.md`, `STATUS.md`, `decisions.md`, `OPEN_QUESTIONS.md`, and the per-project `README.md`

## Status

This repo is itself a GOTM-orchestrated project — a worked meta-example. The framework was distilled and assembled using the discipline the framework describes. The project's own [`GOTM.md`](GOTM.md), [`STATUS.md`](STATUS.md), and [`decisions.md`](decisions.md) are visible in the repo root; read them as a reference for what a real ledger looks like in flight, including sub-lettered Milestones, sunset rows, and a locked-decision chain.

## License

Apache 2.0 — see [`LICENSE`](LICENSE). Apache 2.0 includes an explicit patent grant, which matters for adopters who plan to build on top of the prompts or templates.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md).
