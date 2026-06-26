# In practice

The previous seven chapters built the machine: a thin driver, disposable workers, a tiered store, a scheduler loop over a DAG, parallel fan-out, structural audit independence, and the three-tier memory economy. This chapter is about *doing it* — how a practitioner picks the framework up, what to build first, which constraints actually apply to them, what happens to existing projects, and a concrete demonstration that all of it works. It re-explains nothing; it points back and puts the pieces to use.

## Adopting v3: three tiers, one discipline

The driver loop is, at its base, a **prompt discipline** — a way the driver agent behaves, not a piece of software you have to install. That is the most important practical claim in this chapter, because it means adoption has no floor. You can run v3 with nothing but the protocol in front of the agent.

There are three adoption tiers, and they share the same underlying discipline:

1. **Prompt discipline (baseline — works anywhere).** The driver follows the scheduler loop by hand: read the frontier, compute the ready set, dispatch a **worker** per ready unit, collect the terse result, dispatch an audit worker, record status, repeat. Nothing here depends on a particular runtime or plugin. If your agent can read a file, dispatch a subagent, and write a file, it can run v3. This is the tier the rest of this section bootstraps, and it is the tier the worked example below actually used.
2. **Plugin command.** A **plugin command** packages the loop as an invocable step — it loads the protocol, reads the ledger, and drives a turn of the scheduler for you. It removes the burden of remembering the loop and standardizes dispatch, but it changes nothing architecturally: it is the same discipline, scripted into a command.
3. **Workflow-style script.** At the top tier a **Workflow-style script** runs the loop programmatically outside an interactive turn — useful for headless or batch operation where you want the scheduler to grind the DAG to completion without a human in the seat for each step.

Pick the lowest tier that meets your need. Most people should *start* at the prompt-discipline baseline, because it teaches the loop and costs nothing to set up; reach for the command or the script only when the manual loop becomes a chore you want to amortize.

### Bootstrapping a fresh v3 project

A new project is three things in place before the first unit runs:

- **The store.** Create `.gotm/` alongside the repo. This is the system of record (chapter 2). It holds the protocol, the ledger, the decisions and questions logs, and the `audits/` and `docs/` detail that the cold tier points into.
- **The born-tiered ledger.** The ledger is **born tiered** from the first unit, not flattened and compacted later (chapter 3). Create it with two tables: a hot **frontier** (ready and active units plus their immediate input pointers) and a cold archive (closed units as one-line pointers). Seed the frontier with your foundation units — the upstream DAG nodes everything else depends on. Do not start with a flat log you intend to tier "once it gets big"; that is the v2 mistake, re-introduced.
- **The driver/worker split.** Establish the load-bearing rule at the outset: the driver plans and talks, and *all* work is a worker dispatch. The driver writes the store; workers read inputs, produce one output, and return a terse structured result. Setting this expectation on turn one is what keeps work from leaking back into the long-lived context later.

With the store, a born-tiered ledger seeded with foundation, and the split declared, the driver runs its loop and the project is live.

## Interactive vs SDK driver: the honest limit

Which constraints apply to you depends entirely on *how the driver runs*, and the framework is deliberate about not over-promising here (chapter 2, chapter 7).

In **interactive** Claude Code, the driver *is* the session. It cannot be made stateless, and it cannot self-trigger compaction — that action is human-only, no hook or model directive fires it, and the auto-compact threshold is not tunable. So in interactive use the driver grows, slowly, across a long project. What rescues it is not statelessness but re-hydration: on *any* fresh start — a cold restart, a `/clear`, or after an auto- or manual compaction — the driver rebuilds its working set from the store through the **session-start reconcile**. This is the same transcript-independence guarantee GOTM has always made, and it depends on no compaction hook. An optional hook could auto-inject the re-hydration manifest, but the framework deliberately does not build on it; the store-plus-reconcile path works without it. If you are an interactive user, this is your reality: keep the driver thin, and trust re-hydration to carry you across every session boundary.

In **SDK** or headless mode, the driver gains one capability the interactive driver lacks — it *can* compact itself programmatically, mid-run, without a human. That is a genuine bonus where the runtime allows it. But it is additive, not foundational: the architecture leans on re-hydration, which both runtimes have, not on self-compaction, which only the SDK has. The rule is the same in both worlds — never sell a stateless interactive driver. Know which world you are in, and apply the matching constraint.

## Migration: existing v2 projects convert

The decision is settled — **v2 projects migrate to v3** rather than being left behind. Two artifacts make that practical.

A `MIGRATION.md` documents the conversion: what changes in the ledger shape, how the driver/worker split maps onto a project that previously ran as one long-lived doer, and what to verify after converting. Alongside it, a one-shot **v2→v3 ledger converter** does the mechanical work: it takes the old flat, append-only ledger and tiers it — recent and open units become the hot frontier, closed units collapse into one-line archive pointers, and the dependency edges are recorded so the flat log becomes a proper DAG. The converter generalizes the `compact_ledger.py` already proven on the knowledge-graph project. Existing projects — geniefy, knowledge-graph, this framework's own repo — convert through it. The **migration** is a tiering-and-edge-recording pass, not a rewrite of the work itself; the docs, decisions, and audits all survive untouched.

## The worked example: this rewrite itself

The most honest demonstration of v3 is that **this framework's own v3 documentation was produced driver/worker.** The rewrite was run as a v3 GOTM project, and you are reading its output.

It worked like this. The design blueprint was the single foundation unit — the upstream DAG node every chapter depended on. With foundation in place, the driver **fanned out** chapter workers: each chapter was an independent unit whose dispatch carried the blueprint plus its bounded slice of prior chapters, and nothing else. No chapter worker saw the conversation; none held a sibling's draft. Each produced exactly one file and returned a terse pointer — the driver never held the chapter bodies. Then each chapter was **independently audited by a fresh worker** — the author was ephemeral and gone by audit time, so self-certification was structurally impossible (chapter 6); the worker that wrote a chapter could not be the one that blessed it. Chapters reached authored-done from their writer and verified-done only from that separate auditor.

Finally, because nine chapters written in parallel will drift in terminology and cross-references, the rewrite closed with a **fan-in coherence worker** — a single worker that read all nine outputs *from the store* and harmonized them: reconciling canonical terms, fixing the forward and backward links between chapters, and resolving the small encroachments the per-chapter audits had deliberately deferred to this barrier. The driver received one pointer to the harmonized result, never the nine bodies — the token-critical fan-in rule (chapter 5) held even at the final join. The result is a repo that is its own live demonstration of the discipline: foundation as topology, parallel fan-out, structural audit independence, and a fan-in that reads the store instead of swelling the driver. v3 is not described here so much as exhibited.

---

That is the practice: adopt at the tier that fits, know your runtime's honest limit, convert your v2 projects, and trust that the discipline is real because it built the very thing you are reading. The next chapter looks beyond a single project to how the cold tier feeds forward — **learning across projects**.
