# Scaling & economy

The previous chapter set the DAG in motion, one unit at a time. This chapter is about what happens when there are *many* — dozens of independent units ready at once, wide projects, deep fan-out trees — and about the token cost of running them. Scaling and economy answer one question: *how do we do more work without anything on the hot path growing without bound?* Get the parallelism wrong and the driver re-concentrates work into its own context at every join — monotonicity, smuggled back in. Get the economy wrong and you starve the one context that should be generous while padding the thousand that should be lean. Both fixes are the same shape.

## Fan-out and fan-in — the parallelism spine

Two primitives carry all the parallelism. **Fan-out** is dispatching N independent workers at once. **Fan-in** is joining their outputs at a **barrier** — where a downstream unit needs several upstreams before it can run. Getting these right is most of GOTM's leverage and most of where it can relapse, so the rules are worth stating sharply.

**Minimize barriers; default to pipeline.** The batch-systems instinct is to think in stages — author *all* the units, then audit *all*, then mark *all* done — with a barrier between each. That is wrong here: a barrier makes every unit wait for the slowest sibling in its stage, so wall-clock becomes the *sum* of stage maxima. The default instead is a **pipeline** — each unit flows author → audit → done **independently**, going straight to its own audit while siblings still draft. Wall-clock collapses to the **slowest single chain** through the DAG, not the sum of stages.

A **barrier is earned, not assumed** — justified only when a downstream genuinely needs *all* of its upstreams at once:

| Genuine fan-in (barrier earned) | Not a barrier (pipeline instead) |
|---|---|
| **Synthesis** — N drafts merged into one arc | Auditing each draft (per-unit, independent) |
| **Cross-unit consistency audit** — checking N outputs *against each other* | Compiling/spec-checking one output |
| **Dedup / merge** — reconciling overlapping findings | Producing the next downstream that needs only one upstream |
| **Foundation → drafts gate** — drafts wait on the shared groundwork | Two foundation units that don't depend on each other |

Everywhere else, pipeline. The foundation→drafts gate from chapter 3 is a real barrier — an all-upstreams join — but it is the *exception* the topology encodes, not the rhythm of the whole project.

### The hard rule: fan-in is a fresh worker reading the store

This is the single most important rule in the chapter, and the reason GOTM does not relapse into the failure mode chapter 1 diagnosed:

> **A fan-in is a fresh worker that reads the N outputs from the store and emits the merged output. The driver receives one pointer — never the N bodies.**

When ten chapter drafts must become one coherent arc, or fifty findings one report, the merge is *itself a unit*: the driver dispatches a **fan-in worker** whose bounded inputs are pointers to the N outputs. That worker reads the N bodies *from the store*, merges them, writes one new output, and returns a terse pointer-result. The driver records one row; at no point do the N bodies enter its context.

```mermaid
flowchart LR
    subgraph good["RULE — fan-in worker reads the store"]
        direction LR
        GS[("store")]
        GFI["fan-in worker"]
        GD(["driver"])
        GS -->|"read N outputs"| GFI
        GFI -->|"write merged output"| GS
        GFI -->|"ONE pointer"| GD
    end
    subgraph bad["ANTI-PATTERN — driver holds N results"]
        direction LR
        BS[("store")]
        BD(["driver"])
        BS -->|"N bodies"| BD
        BD -->|"merges in-context<br/>(monotonicity)"| BD
    end
    classDef driverC fill:#e8f0fe,stroke:#1a73e8,color:#1a1a1a;
    classDef workerC fill:#fef7e0,stroke:#f9ab00,color:#1a1a1a;
    classDef storeC fill:#e6f4ea,stroke:#188038,color:#1a1a1a;
    class GD,BD driverC;
    class GFI workerC;
    class GS,BS storeC;
    classDef badbox fill:#fce8e6,stroke:#d93025;
    class bad badbox;
```

*The hard rule (left) versus the relapse (right): a fan-in worker reads the N outputs from the store and hands the driver one pointer; the anti-pattern pulls all N bodies into the long-lived driver, re-concentrating work at every join.*

The obvious-but-wrong alternative is for the driver to collect the N full results and merge them itself — it has the pointers, why not read and stitch? Because the driver is the *one long-lived context*. Pull N bodies in to merge them and that work now lives there **at every barrier** — a dozen joins re-concentrate a dozen piles of work into the driver, each permanent for the rest of the session. That is monotonicity, reintroduced one join at a time, the exact thing the driver/worker split exists to forbid. The fix is the load-bearing rule from chapter 2: *the driver carries the index, not the work.* A merge is work, so a merge is a worker. This is also why workers return **terse structured results** — a pointer plus a few index facts (status, output path, headline verdict), never the body. The driver merges *pointers*; the substance stays on disk.

This economy cannot rest on the driver *choosing* not to hoard, because a worker that returns a long report will get its body absorbed no matter how disciplined the driver means to be. So the discipline is made **mechanical, in the dispatch contract**: every worker writes its full detail to its output or report file and **returns a pointer plus verdict plus blocker in roughly eight lines or fewer** — never the body. An over-cap return is treated as a **defect**, the same way a failing check is, not as verbosity to tolerate. The driver records the pointer and moves on; it never reads a body to record a status. This is the mechanical form of the fan-in-is-a-worker rule turned on every dispatch, not just merges: detail lives on disk, the long-lived context holds only the index.

### The rest of the spine

Four more properties make fan-out scale cleanly:

- **Fan-out is a tree, not a flat list.** A large unit need not be one giant worker; it fans out to sub-workers, which may fan out further, and the driver sees only the **root** result. A research unit can spawn ten search workers and a fan-in worker beneath it, returning the driver one pointer to the synthesized finding. Driver context stays bounded *regardless of total work width* — the tree absorbs the breadth.

  ```mermaid
  flowchart TB
      DR(["driver"])
      W["worker (large unit)"]
      SW1["sub-worker"]
      SW2["sub-worker"]
      SW3["sub-worker"]
      FI["fan-in worker"]
      DR -->|dispatch| W
      W --> SW1
      W --> SW2
      W --> SW3
      SW1 --> FI
      SW2 --> FI
      SW3 --> FI
      FI -->|"one root pointer"| DR
      classDef driverC fill:#e8f0fe,stroke:#1a73e8,color:#1a1a1a;
      classDef workerC fill:#fef7e0,stroke:#f9ab00,color:#1a1a1a;
      class DR driverC;
      class W,SW1,SW2,SW3,FI workerC;
  ```

  *Fan-out is a tree: a large unit spawns sub-workers (which may fan out further) and a fan-in worker beneath it; the driver dispatches once and receives only the single root pointer, so its context stays bounded no matter how wide the tree grows.*
- **Backpressure.** Fan-out is bounded by a concurrency cap. Unbounded width is doubly costly: it spikes resource use at dispatch *and* inflates the eventual fan-in re-concentration. A cap — dispatch K at a time, refill as they finish — keeps both bounded.
- **Explicit barrier-failure policy.** When a fanned-out worker fails, the barrier must not silently merge a partial set. The policy is explicit, chosen per barrier: **retry** on a fresh worker (inputs on disk — lineage recompute, chapter 4), or **drop-and-continue** with the survivors, recording what was dropped. Never an unannounced partial merge.
- **Order-independent merges.** Results return out of order, so fan-in merges are either commutative or the fan-in worker sorts by unit ID first. The driver never depends on completion order.

## Token economy — worker minimalism, not project budgets

The second half of scaling is cost. GOTM's economy rests on one deliberate asymmetry: **be frugal where there are many contexts; be generous where there is one.** This is **worker minimalism**, and it is emphatically *not* project-level budgeting.

**Workers are kept lean.** A worker's dispatch payload is exactly the bounded inputs it consumes, plus its spec and constraints — nothing else. **Never** the whole ledger, never sibling outputs it won't read, never the conversation. A worker that needs more either **reads from the store itself** or **fans out**; it is never handed extra context "just in case." The reason is arithmetic: dozens of workers run per project, and every needless token is paid *per dispatch*. Trimming a worker payload is the highest-leverage economy lever there is — a hundred tokens of slop times a hundred dispatches is real money that buys nothing.

**The driver may be larger — and that is legitimate.** It is orchestrating: it holds the plan, the discipline, the frontier, and the human conversation. Do **not** starve it to hit an arbitrary ceiling. Its safety net is not turn-by-turn trimming but **re-hydration from the store on any fresh start** (chapter 2 — runtime-agnostic, no compaction hook). Optimize the workers, which are many; let the driver be the orchestrator, which is one. A driver trimmed too aggressively just re-reads the store more often and ratifies worse — a false economy on the one context whose health gates the whole project.

The rest of the economy is four concrete levers riding on that asymmetry:

- **Amortized batching.** The rule never bends — *always dispatch*, the driver never edits a work artifact. But dispatch has overhead, so a litter of one-line fixes is not N tiny workers; it is one **partition-worker** carrying the batch, its overhead paid once across the lot. Size each payload to a sensible band — minimal sufficient, neither padded nor starved; a unit that would blow past its band fans out instead. The target is "minimal sufficient," never "hit a forecasted number."
- **Audit weight by risk.** A keystone chapter, a deploy unit, or an infra change earns a **full independent audit** — a fresh worker re-deriving the verdict from scratch. A mechanical unit (a rename, a formatting pass) earns a **light check**: existence, spec-match, compile. A hundred-thousand-token audit on a one-line change is waste; skipping the deep audit on a deploy is negligence. Match the audit to the risk. (The independence and verdict mechanics are chapter 6; here it is purely an economy lever.)
- **Cheap hot tier.** The store's **hot tier** is read by every consuming worker *and* every driver turn — squarely on the **hot path**, so its size recurs forever. Three habits keep it small: terse frontier cells (an index entry, not a record of the work); read the audit *file* for a verdict's detail, not the whole ledger; and a born-tiered ledger so closed detail never sits in the part that gets re-read. (Compaction keeps it bounded over time — chapter 7.)
- **Model tiering.** The economy compounds with the obvious move: one **strong driver** plus many **cheap, fast workers** — mechanical units on a small model, keystone reasoning and full audits on the strong one. The fan-in-worker rule makes this safe: because the driver stays thin, it can afford to be the strong, expensive model while the breadth of cheap workers absorbs the volume.

### What we deliberately did *not* build

The omission is a decision, not an oversight. GOTM has **no project token budgets, no DAG cost-forecasting, and no budget-governed loop.** We do not predict total spend, allocate a ceiling per branch, or let a governor steer the scheduler. The loop stays simple (chapter 4); economy comes from **lean workers + a fat-but-checkpointed driver + cheap store reads** — three structural properties — not from a governor watching a meter.

One honest framing, so the chapter does not oversell: **GOTM does not necessarily spend fewer total tokens.** Fan-out runs more work in parallel; risk-tiered audits add passes a single self-certifying agent skipped. What changes is the *shape* of the spend, not its sum. The spend becomes **bounded** (no context grows without limit), **attributable** (each unit's cost is its own), **parallelizable** (independent chains run at once), and **tier-able** (cheap models do cheap work). A monotonic system's cost is unbounded and unattributable; GOTM's is bounded and accounted for. That, not a lower bill, is the win.

---

Fan-out and fan-in scale the work; worker minimalism and a fat-but-checkpointed driver pay for it — and both reduce to one rule: the long-lived context holds the index, never the work. The next chapter turns to the other thing the driver/worker split buys for free: **keeping it honest** — structural audit independence, the authored-done / verified-done distinction, and the freeze.
