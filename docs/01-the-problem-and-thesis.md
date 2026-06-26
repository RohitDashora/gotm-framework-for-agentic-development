# The problem & the thesis

## The work is bigger than any one context

Serious agentic work does not fit in a single LLM session. A real project — a research report, a migration, a multi-part deliverable, a deployed system — spans hundreds of model invocations and many dispatched subagents. It runs longer than any one context window, longer than any one session, longer than any one model's patience.

This exposes the defining constraint of the medium: **context is the scarce, lossy, expensive resource.** Every token in a context is paid for, on every turn it survives. Context is lossy — quality degrades as a window fills, long before it overflows. And context is bounded — when the window ends, *nothing survives the session boundary unless it is on disk.* An agent's working memory is not durable. The transcript is not a system of record. The only thing that crosses a session boundary is what was written down.

We call this regime **bounded-context agentic execution**: real work, much larger than one context, where the binding question is not "can the model do the task?" but "how do we move work across context boundaries without losing it, and without paying for it forever?" Get the economy of context wrong and a long project does not fail loudly — it slowly grinds to a halt under its own weight.

GOTM's founding invariant answered the first half: **the durable store reconstructs working context.** We call this *transcript independence* — any context can be thrown away and rebuilt from disk, because the disk, not the conversation, is the system of record. Earlier versions of GOTM honored this for authoring. But they quietly violated its spirit in two places, and both failures share a single shape.

## The failure mode: monotonicity

A system is **monotonic** when its cost only ever grows. On a short task you never notice. On a project that spans hundreds of sessions, monotonic cost is fatal — it is the asymptote the whole effort runs into.

GOTM's earlier design was monotonic in two places.

**The single durable artifact only grew, and was re-read every turn.** The ledger — GOTM's record of units — was append-only, frozen-not-edited, write-back-everything. That gave the system a strong theory of *growth* and no theory of *ephemerality*. A unit closed weeks ago still paid its full cell — six hundred to two thousand tokens — on every single re-read, forever. In the field this produced a 380 KB ledger, roughly ninety-five thousand tokens, re-read on every turn, duplicating detail that already lived in the audit files, the decisions log, and the docs. The record of the work had become heavier than the work.

**One long-lived agent accumulated all execution state.** A single "doer" context planned, executed, fixed, deployed, and validated — and never let go of any of it. Two consequences followed, both structural. First, because the same context that produced the work also judged it, audit independence eroded: the agent **self-certified its own work**, which is no audit at all. Second, the context grew without bound until it stalled — a real, observed death at roughly **987,000 tokens**, a single agent so swollen with accumulated state that it could no longer function. The work had been living in a context instead of in the store — exactly what the founding invariant forbids.

The root cause is one thing, not two. The design **conflated the planner and the doer in one ever-growing context**, and it had **no theory of ephemerality**. The fix is not "compact harder" or "summarize more aggressively." Those treat the symptom. The cure is architectural: make nothing on the hot path long-lived.

## The thesis

> **GOTM is a context-economy discipline. The durable store is the system of record; every working context is disposable and reconstructable from it. Nothing on the hot path is long-lived.**

Read that sentence as three commitments. *Context economy* names the discipline: we manage context the way a careful system manages a scarce, metered resource — frugal where there are many of it, generous only where there is one. *The durable store is the system of record* restates and hardens transcript independence: the disk is the truth; any context is a cache of it. *Nothing on the hot path is long-lived* is the new law, the one the earlier design broke: the contexts that do work are born for one job and discarded, so their cost is bounded by that one job and can never accumulate.

The **hot path** is everything read or run on a recurring basis — every working context, every per-turn read. The cure for monotonicity is to forbid anything long-lived from living there. Work happens in disposable **units**; each unit is done by a fresh, short-lived context that is gone before its cost can compound. The durable record is born tiered, so the recurring read stays cheap no matter how much cold history piles up behind it. And the one context that genuinely must persist is given only the *index* of the work — never the work itself.

## Everything that follows is a consequence

This chapter argues a thesis; it does not yet build the machine. But the machine is already implied. Separating the planner from the doer points toward a long-lived coordinator and short-lived executors talking only through a durable record. Making the doers disposable hints that no context can grade its own work, because it is gone by the time that work is judged. Making the durable record cheap to read suggests how the hot path can stay flat while history piles up out of the way. And making the work decompose into self-contained pieces is what opens the door to running them in parallel and recovering any one of them from disk. None of those are built here — they are only the shapes the thesis casts ahead of itself.

The architecture, the scheduler loop, scaling and economy, audit independence, resilience and tiered memory — none of these are independent inventions. Each is a **consequence** of the single sentence above. The rest of this framework is that derivation, made concrete.

The next chapter builds the first and most important consequence: the architecture — **driver, worker, and store** — and the non-monotonicity guarantee it buys, along with the one honest limit on it.
