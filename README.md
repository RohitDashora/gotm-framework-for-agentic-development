# GOTM

A discipline for surviving bounded-context agentic execution — when complex work spans hundreds of LLM sessions and many subagents and can't fit in any one of them.

## The problem GOTM solves

Complex work with AI agents falls apart in predictable ways. State that an agent built up in one session evaporates at the session boundary. The next session starts cold and re-derives — usually slightly differently — and the project's working understanding drifts. Drafts run ahead of the evidence the agent never wrote down. Subagents inherit the task but not the project's discipline. "Done" markers accumulate without independent audit. Mission-level decisions get made unilaterally by the agent; trivial choices get escalated to the human. Session-level tooling — slash commands, custom instructions, system prompts — dies when the session does.

None of these are fixable inside the agent. The agent is, by construction, a bounded-context worker. The thing that gives the worker continuity has to live outside.

## What GOTM is

GOTM is the discipline of moving continuity outside the agent and into the **project filesystem**. The project carries five primitives — a mission, a ledger, atomic units of work, a foundation-before-drafts gate, and an audit cycle — plus a ratification ladder that says which decisions are the human's. Every agent that opens a session in the project reads the protocol, reads the ledger, and operates under the discipline. Subagents inherit the discipline through the dispatch. The agent stays stateless; the project stays stateful.

GOTM is not a hierarchy. It is not project management. It is not a methodology. It tells you how to carry context across many sessions of whatever methodology you use to plan the work.

## When to use it

Use GOTM when the work is multi-session, when the cost of drift is high, and when an agent (or several) will be doing meaningful chunks of the execution. Multi-week deliverables. Multi-author research projects. Systems that span hundreds of LLM sessions and dispatched subagents.

Do not use GOTM for one-shot tasks. A one-off email or a five-line script does not need a ledger. The ceremony is more than the work.

## What's in this repo

```
docs/         3 concept chapters (~3,900 words) — the framework from first principles
prompts/      3 operational prompts a practitioner pastes into their LLM
templates/    5 scaffold files to copy into a new project's root
PROTOCOL.md   the project's own protocol (working example)
LEDGER.md     the project's own ledger (working example)
DECISIONS.md  the project's own append-only decision log (working example)
QUESTIONS.md  the project's own open-questions file (working example)
```

Everything is platform-neutral markdown. Paste any prompt body into ChatGPT, Cursor, Cline, Claude API, or raw chat — it works. The repo's own root files (`PROTOCOL.md`, `LEDGER.md`, `DECISIONS.md`, `QUESTIONS.md`) are visible as a working meta-example: this project is itself GOTM-orchestrated.

## Quickstart — your first GOTM project in five steps

1. **Pick work that fits.** Multi-session, drift-cost high. See [When to use it](#when-to-use-it).
2. **Copy the templates into your project root.** From `templates/`: `PROTOCOL.md.template` → `PROTOCOL.md`; `LEDGER.md.template` → `LEDGER.md`; `DECISIONS.md.template` → `DECISIONS.md`; `QUESTIONS.md.template` → `QUESTIONS.md`. Fill in the mission line in `PROTOCOL.md` and `LEDGER.md`. Sketch your first two or three units in `LEDGER.md` (foundation first).
3. **Open `prompts/session-start.md` in your LLM.** Paste the body. The LLM reads `PROTOCOL.md`, `LEDGER.md`, and `QUESTIONS.md`, identifies the active unit, and reports back.
4. **Direct the LLM to act on the active unit.** When it finishes, it updates `LEDGER.md` and either appends a decision to `DECISIONS.md` or surfaces a question to `QUESTIONS.md`.
5. **When work exceeds a session or needs independent context, dispatch.** Use `prompts/subagent-dispatch.md` to construct a worker prompt that points back at `PROTOCOL.md`. Use `prompts/audit.md` to run a mechanical check before downstream work consumes any claimed-done output.

From there, the loop repeats. Pick the next active unit. Act. Write back. Audit when called for.

## Concept chapters

- [`docs/01-what-is-gotm.md`](docs/01-what-is-gotm.md) — what GOTM is, from first principles
- [`docs/02-what-agents-are-missing.md`](docs/02-what-agents-are-missing.md) — the specific gaps in agentic work today
- [`docs/03-gotm-with-agents.md`](docs/03-gotm-with-agents.md) — how the framework closes them

## Operational prompts and templates

- [`prompts/session-start.md`](prompts/session-start.md) — kickoff template; first move of every session
- [`prompts/subagent-dispatch.md`](prompts/subagent-dispatch.md) — how the orchestrator builds a bounded worker prompt
- [`prompts/audit.md`](prompts/audit.md) — generic audit template; one kind per dispatch
- [`templates/`](templates/) — copy-and-fill scaffolds for the four root files plus a project README

## License

Apache 2.0 — see [`LICENSE`](LICENSE). Contains an explicit patent grant.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md).
