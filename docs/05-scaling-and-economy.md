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
- **Model tiering.** The economy compounds with the obvious move: one **strong driver** plus many **cheap, fast workers** — mechanical units on a small model, keystone reasoning and full audits on the strong one. The fan-in-worker rule makes this safe: because the driver stays thin, it can afford to be the strong, expensive model while the breadth of cheap workers absorbs the volume. This is the compute-economy analog of everything above — *frugal in the many, generous in the one* applied to model spend, not just context — and it has enough moving parts to earn its own section, next.

### Model tiering — the mechanism

The bullet above states the principle; this is how the driver actually spends it. The prose version — "mechanical → small, keystone + audit → strong" — is a slogan until something decides *which worker gets which model on which unit*. That decision has a shape, and getting the shape right is what separates a real cost lever from a cheap router that mis-assigns models and quietly degrades the whole project.

**The driver is the allocator; workers are tiered per task.** The driver stays pinned at the user's strongest setting (§ *the driver may be larger*) and does one extra job at plan time: for each worker it dispatches, it chooses that worker's resources. This is the compute-economy twin of the fan-in rule — the long-lived context holds the *allocation authority*, not the cheap work. Crucially, **the allocator is the frontier model.** The dominant failure mode in the cost-routing literature is *bad routing*: a small, cheap classifier picks the model and picks wrong. GOTM never runs that classifier. The entity choosing each worker's tier is the SOTA driver at max effort — the same context that just planned the unit — so routing quality is your best model's judgment, and the decision **piggybacks on the dispatch reasoning the driver already does.** No separate router, no extra pass, nothing to train.

**Two knobs, not one: model × effort.** A worker's tier is a *pair* — `(model, effort)` — because effort (the reasoning / thinking budget) is a **cheaper lever than a model-swap**. A task that needs the strong model's *knowledge* but only shallow *reasoning* keeps the model and drops the effort: no quality loss, less thinking spend. The driver trades either knob per task, and reaches for effort first because it is the cheaper adjustment. Where a runtime cannot set per-worker effort, tiering degrades gracefully to model-only — still agnostic, still working.

**Three abstract tiers, bound by the runtime.** GOTM names three tiers and **never hardcodes model names** — the runtime maps each to a concrete `(model, effort)`:

- **economy** — small/fast model, low effort — mechanical extraction, reformatting, renames.
- **standard** — mid model, medium effort — routine authoring and data work. **(the default)**
- **frontier** — strong model, high effort — diagnosis, design, keystone units, anything irreversible.

The driver itself sits at the user's choice, **≥ frontier**, and never escalates — it is already at the top.

**The rubric — complexity → tier.** At plan time the driver reads a handful of signals, all cheaply inferable from the unit spec: `Kind`; reasoning depth (single- vs multi-hop); critical-path fan-out; audit-risk (how hard the output is to verify); input size and heterogeneity; novelty / ambiguity; and **blast radius** (reversible scratch vs an irreversible or external side-effect). It applies them as a short ordered rubric, first match wins — kept short so a driver actually applies it:

| # | Condition | Tier |
|---|---|---|
| R1 | irreversible blast radius **OR** diagnosis / design **OR** deep-reasoning + high-novelty | **frontier** |
| R2 | critical-path hub **OR** authoring / synthesis **OR** multi-hop **OR** hard-to-audit | **standard** |
| R3 | mechanical, low-reasoning, reversible, easily audited | **economy** |
| — | unsure | **standard** (default) |

Because a frontier model applies it, the rubric is **guidance for judgment, not a rigid router table** — and it uses *semantic* signals (Kind, reasoning depth, blast radius), never the classic "length ≈ difficulty" heuristic that mis-routes. In practice `Kind` largely **predicts** Tier (eval / deploy-infra / diagnosis → frontier; ui / mechanical → economy); the exception is `authoring`, which splits on keystone-ness, so tier stays its own decision rather than a mechanical function of `Kind`.

**Escalation — kill and respawn one tier up.** A cheap worker that is out of its depth is not a disaster, because the audit gate makes cheapness safe: a failed cheap worker is **killed and respawned one tier up**, capped, until it passes or a human takes it. This reuses the loop's crash model exactly — "a worker crash is a task retry" (chapter 4, chapter 7): re-dispatch a fresh worker on the same on-disk inputs, a lineage recompute — plus a tier bump. There are **three triggers, cheapest first**:

1. **Self-escalate** — a worker sensing it is out of its depth returns `ESCALATE: <reason>` instead of producing garbage, skipping the wasted bad-output → audit round. It is a *hint*, not trusted (small models over-estimate themselves), so the audit remains the backstop.
2. **Watchdog kill** — a worker that hangs, loops, or blows a liveness timer is **killed** and re-dispatched a tier up, without waiting for a bad return.
3. **Audit-FAIL** — the reliable backstop; the worker is already gone, so the FAIL re-dispatches fresh, a tier up.

The ladder: start at the rubric tier, and on any trigger re-dispatch fresh **one tier up** (economy → standard → frontier), **capped at frontier** (**max two bumps per unit**). A frontier failure is a **hard stop → human** via the ratification ladder — never a loop. Every escalation is **recorded** (start tier, final tier, trigger, reason): a mis-tiering signal for tuning the rubric, and a fact for the learning pool.

```mermaid
flowchart TB
    P["driver plans unit<br/>reads rubric signals"]
    T{"tier?"}
    E["economy"]
    S["standard"]
    F["frontier"]
    TR{"trigger?<br/>self-escalate ·<br/>watchdog · audit-FAIL"}
    K["kill + respawn fresh<br/>one tier up"]
    H(["hard stop → human<br/>(ratification ladder)"])
    P --> T
    T -->|R3 mechanical| E
    T -->|R2 / default| S
    T -->|R1 irreversible / design| F
    E --> TR
    S --> TR
    TR -->|pass| DONE(["audit PASS → done"])
    TR -->|"trigger (cap 2 bumps)"| K
    K --> TR
    F --> FTR{"trigger?"}
    FTR -->|pass| DONE
    FTR -->|"any FAIL at frontier"| H
    classDef driverC fill:#e8f0fe,stroke:#1a73e8,color:#1a1a1a;
    classDef workerC fill:#fef7e0,stroke:#f9ab00,color:#1a1a1a;
    classDef stopC fill:#fce8e6,stroke:#d93025,color:#1a1a1a;
    class P driverC;
    class E,S,F,K workerC;
    class H stopC;
```

*The escalation ladder: the driver tiers each unit by rubric, and any of the three triggers kills the worker and respawns it fresh one tier up — capped at frontier, where a failure stops for a human rather than looping.*

**The safety keystone: blast-radius = kill-safety (one rule, two jobs).** Killing and respawning is clean only because of two facts that turn out to be the same fact. First, **the driver is the single writer**: a killed worker's partial output never lands in the ledger (the driver records only results it *receives*), so a kill mid-run leaves the store untouched and the fresh worker re-runs from clean inputs — chapter 7's worker-retry guarantee. Second, **irreversible workers are never cheap-tiered**: rubric **R1** sends anything with an external side-effect to **frontier from the start**, so the only workers ever killed-and-respawned are reversible / scratch ones. You never kill a worker mid-`deploy`, mid-write. So the blast-radius rubric rule and the kill-safety rule are **the same rule** — escalation is safe *by construction*, not by luck.

**Audit reverse-tiering.** The audit's tier tracks the *unit's* risk, and here it can run *against* the worker's tier. **Reverse-tier the audit to frontier for cheap-but-hard-to-verify or irreversible units even when the worker ran economy**: cheap-to-produce plus costly-if-wrong earns a strong auditor over a weak producer. This composes with "audit weight by risk" above — that lever sizes *how much* audit; this one sizes *how strong*. The gate's *independence* (auditor ≠ author, chapter 6) does the primary safety work; tiering only sizes it. And the standing rule holds: **never skip or cheapen the audit to save money on economy units** — the whole safety of cheap workers rests on the gate.

**One honest guardrail, so this doesn't contradict the next section.** `Tier` is a **static per-unit label** — like `Kind`, a property the driver assigns once at dispatch — **not a cost governor.** It does not watch a meter, forecast spend, or steer the scheduler. A worker never even reads its own tier; the driver resolves `tier → (model, effort)` and sets it at spawn, exactly as the worker writes its output and never parses the hook's key. This is why model tiering coexists with everything in the next section rather than contradicting it: a static label attached to each unit is a world apart from a budget-governed loop that allocates a ceiling and reacts to consumption. Tiering picks the right-sized tool per unit up front; it never becomes a governor watching the bill.

### What we deliberately did *not* build

The omission is a decision, not an oversight. GOTM has **no project token budgets, no DAG cost-forecasting, and no budget-governed loop.** We do not predict total spend, allocate a ceiling per branch, or let a governor steer the scheduler. The loop stays simple (chapter 4); economy comes from **lean workers + a fat-but-checkpointed driver + cheap store reads** — plus the per-unit model tiering above — not from a governor watching a meter. Model tiering is not a counter-example to this: a static per-unit `Tier` label is a *choice of tool*, not a *scheduler that steers by cost*. The driver never sums tiers into a budget, never throttles dispatch when spend climbs, never re-plans to hit a number. The tier is set once and read once, at spawn — the same shape as `Kind`. There is no meter anywhere in the loop.

One honest framing, so the chapter does not oversell: **GOTM does not necessarily spend fewer total tokens.** Fan-out runs more work in parallel; risk-tiered audits add passes a single self-certifying agent skipped. What changes is the *shape* of the spend, not its sum. The spend becomes **bounded** (no context grows without limit), **attributable** (each unit's cost is its own), **parallelizable** (independent chains run at once), and **tier-able** (cheap models do cheap work). A monotonic system's cost is unbounded and unattributable; GOTM's is bounded and accounted for. That, not a lower bill, is the win.

---

Fan-out and fan-in scale the work; worker minimalism and a fat-but-checkpointed driver pay for it — and both reduce to one rule: the long-lived context holds the index, never the work. The next chapter turns to the other thing the driver/worker split buys for free: **keeping it honest** — structural audit independence, the authored-done / verified-done distinction, and the freeze.
