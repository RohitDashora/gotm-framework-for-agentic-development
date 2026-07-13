# GOTM — per-worker model tiering — design

> **Status:** v0.1, for redline. Blueprint for **driver-assigned, per-worker model tiering** — the compute-economy layer over GOTM's context economy. Proposed ship: candidate **v4.1** (naming at ship — §13).
> **Why:** `docs/05` *asserts* model tiering ("one strong driver + many cheap, fast workers; mechanical→small, keystone+audit→strong") as a principle, but stops at prose — no per-unit mechanism, no ledger field, no loop step. This operationalizes it: the driver assigns each worker's **model × effort** by task.
> **Reframe:** the **compute-economy analog of the context economy.** `docs/05`'s asymmetry — *frugal in the many (workers), generous in the one (driver)* — applied to compute spend, not just context.
> **Method:** design-first, on disk; researched in parallel (prior-art landscape · GOTM integration points · the rubric). Build driver/worker + execution-proven when we build.

---

## 1. Thesis

> The driver stays pinned at the user's strongest setting and acts as the **allocator**; every worker runs at the **cheapest tier the task allows**; the **audit gate** makes that safe — a failed cheap worker is **killed and respawned one tier up**, capped, until it passes or a human takes it.

The one line that makes it defensible: **the allocator is the frontier model.** The field's dominant failure mode is *bad routing* — a cheap classifier mis-assigns models. GOTM dodges it because the entity choosing each worker's tier is the SOTA driver at max effort — the same context that just planned the unit. Routing quality = your best model's judgment, and the decision **piggybacks on the dispatch reasoning the driver already does** (no separate router, no extra pass).

## 2. Architecture — driver fixed, workers tiered

- **Driver — fixed, not tiered.** User-selected model + effort (generally SOTA + xhigh). It is the orchestrator, the single long-lived context, *and* the tier-decider — exactly `docs/05`'s "generous where there is one." It sits at or above the top worker tier and **never escalates** (already at the top).
- **Workers — tiered per task, by the driver.** At dispatch the driver assigns each worker its resources, *guided* (not ruled) by the rubric (§5). Because a frontier model makes the call, the rubric is **guidance for judgment**, not a rigid router table.

## 3. Two knobs — model × effort

A worker's tier is **(model, effort)**, not model alone. Effort (reasoning / thinking budget) is a **cheaper lever than a model-swap**: a task that needs the strong model's *knowledge* but shallow *reasoning* keeps the model and drops effort — no quality loss, less thinking spend. The driver can trade **either** knob per task. Where the runtime can't set per-worker effort, GOTM degrades to model-only tiering (still agnostic).

## 4. The tiers (abstract; the runtime binds them)

Three abstract tiers; the **runtime** maps each to a concrete `(model, effort)`. GOTM never hardcodes model names.

- **economy** — small/fast model, low effort — mechanical extraction/reformat.
- **standard** — mid model, medium effort — routine authoring/data. **(default)**
- **frontier** — strong model, high effort — diagnosis/design/keystone/irreversible.

Driver = the user's choice, **≥ frontier**.

## 5. The rubric — complexity → tier

Signals the driver reads at plan time (all cheaply inferable from the unit spec): `Kind`; reasoning depth (single- vs multi-hop); critical-path fan-out; audit-risk (how hard to verify); input size/heterogeneity; novelty/ambiguity; **blast radius** (reversible scratch vs irreversible/external side-effect).

Rubric — ordered, first match wins (kept this short so drivers actually apply it):

| # | Condition | Tier |
|---|---|---|
| R1 | irreversible blast radius **OR** diagnosis/design **OR** deep-reasoning + high-novelty | **frontier** |
| R2 | critical-path hub **OR** authoring/synthesis **OR** multi-hop **OR** hard-to-audit | **standard** |
| R3 | mechanical, low-reasoning, reversible, easily audited | **economy** |
| — | unsure | **standard** (default) |

`Kind` largely **predicts** Tier (eval/deploy-infra/diagnosis → frontier; ui/mechanical → economy) — the exception is `authoring`, which splits on keystone-ness, so **Tier stays its own column** rather than being derived from `Kind`.

## 6. Escalation — kill-and-respawn one tier up

Escalation reuses GOTM's crash model ("a worker crash is a task retry" — re-dispatch a fresh worker on the same on-disk inputs), plus a tier bump. **Three triggers, cheapest first:**

1. **Self-escalate** — a worker out of its depth returns `ESCALATE: <reason>` instead of producing garbage (skips the bad-output→audit round). A hint, not trusted (small models over-estimate themselves) — the audit remains the backstop.
2. **Watchdog kill** — a worker that hangs / loops / blows a liveness timer is **killed** and re-dispatched a tier up, without waiting for a bad return.
3. **Audit-FAIL** — the reliable backstop; the worker is already gone, so re-dispatch fresh a tier up.

**Ladder:** start at the rubric tier → on any trigger, re-dispatch fresh **one tier up** (economy → standard → frontier). **Cap** at frontier; a frontier failure is a **hard stop → human** (the ratification ladder), never a loop; **max 2 bumps / unit**. **Record** every escalation (start tier, final tier, trigger, reason) — a mis-tiering signal for rubric tuning and a learning-pool fact.

## 7. Safety keystone — blast-radius = kill-safety (one rule, two jobs)

Killing + respawning is clean only because:

1. **The driver is the single writer.** A killed worker's partial output never lands in the ledger (the driver records only results it *receives*), so kill-mid-run leaves the store untouched and the fresh worker re-runs from clean inputs (`docs/07`'s worker-retry guarantee).
2. **Irreversible workers are never cheap-tiered.** Rubric **R1** sends anything with an external side-effect to **frontier from the start**, so the only workers ever killed-and-respawned are reversible/scratch ones. You never kill a worker mid-`deploy` / mid-write.

So the **blast-radius rubric rule and the kill-safety rule are the same rule.** Escalation is safe *by construction*, not by luck.

## 8. Audit interaction

The audit worker's tier tracks the *unit's* risk (`Kind` already drives audit depth — `docs/05` risk-tiered audits, `docs/06` typed-by-kind). **Reverse-tier the audit** to frontier for **cheap-but-hard-to-verify / irreversible** units even when the worker ran economy: cheap-to-produce + costly-if-wrong = a strong auditor. The gate's *independence* (auditor ≠ author) does the primary safety work; tiering just sizes it. **Never skip or cheapen the audit to save money on economy units** — the whole safety rests on the gate.

## 9. Integration points

- **Ledger:** a new `Tier` column in the frontier table, beside `Kind` — a **static per-unit label** (like `Kind`, **not** a cost governor). Conventions block gets it, default `standard`.
- **Dispatch:** the driver resolves `Tier → (model, effort)` and sets it **at spawn** — the worker never reads its own tier (parallels how the worker just writes `Output` and never parses the hook's key).
- **Loop:** assigned in step 1→2 (ready-set → dispatch), the same seam that already reads `Kind`; escalation lives in step 5 (collect/retry), which becomes *retry-with-escalation + kill*.

## 10. Runtime binding — what ships vs what the platform provides

- **GOTM ships the discipline:** the abstract tiers, the rubric, the escalation ladder, the `Tier` column, the safety rules — runtime-agnostic prose + templates.
- **The runtime binds:** `tier → (model, effort)`, the per-worker model at spawn, and the kill capability.
- **Concreteness (Claude Code):** the subagent dispatch already accepts a `model` parameter and background workers are stoppable — so model-tiering + kill are implementable **today**; per-worker *effort* binding depends on what the runtime exposes (degrade to model-only where absent). Same discipline-not-engine line GOTM always draws.

## 11. Prior art + the discipline-vs-platform line

The cost literature backs the approach and warns off the wrong version:

- **Cascade (cheap → verify → escalate)** is the most cost-effective lever (FrugalGPT: ~best-model quality at up to **98% cost cut**; RouteLLM: ~95% quality at ~85% lower cost). Its hard part is *the verifier* — normally a trained confidence-scorer (**platform**: data, drift, retraining). **GOTM already has the verifier for free: the independent audit gate.** That is the unlock — GOTM runs the winning cascade as a *discipline*.
- **Take (discipline):** difficulty/complexity → tier mapping + orchestrator-assigns-per-task, with escalation via the audit. **Skip (platform):** trained routers (RouteLLM/Morph) and confidence-scored cascades — telemetry/retraining GOTM doesn't want.
- **Heed the field's #1 finding:** *rubric quality > mechanism*; "length ≈ difficulty" is the classic misroute. Our rubric uses **semantic** signals (Kind, reasoning depth, blast radius), never length — and the allocator is the frontier model, the best possible rubric-applier.

## 12. Decisions & open questions

**Decided (from the discussion):**
- Driver **fixed** at the user's model+effort (not tiered); only **workers** are tiered.
- The **allocator is the driver** (frontier model), not a separate router.
- Tier = **(model, effort)**; effort is a distinct, cheaper knob.
- **Three abstract tiers** (economy/standard/frontier); the runtime binds them to models.
- Escalation = **kill-and-respawn one tier up**; three triggers; cap 2 → human; record.
- **Blast-radius rule = kill-safety**; irreversible → frontier from the start.
- `Tier` is a **static label**, never a cost-governed scheduler (`docs/05` consistency).

**Open (for redline / build):**
1. **Effort model** — coupled tiers (each tier = a fixed model+effort preset) vs a decoupled model×effort matrix with an effort override. *(Lean: coupled presets + an optional effort override.)*
2. **Watchdog thresholds** — per-tier liveness timers: fixed, or driver-judged per unit? Keep it a *safety timer*, **not** budget-governance.
3. **Ledger-shape change** — a new `Tier` column shifts the immutability hook's positional indices; the parser must update **in lockstep** + run on a real ledger (the v3.35 lesson). Land it after `Kind`, before `Status`.
4. **Self-escalate reliability** — how far to trust a small worker's `ESCALATE`; treat as a hint, audit stays the backstop.

## 13. Version

Candidate **v4.1** — an enhancement on the v4 base (adds a ledger column + a loop-step behavior; **no new store**), not a peer like v4.0. Name the shipped version deliberately (the v3.1→v3.35 drift lesson — see [`README.md`](README.md)).

## 14. Build plan (driver/worker, dogfooded) — NOT STARTED

- **U-ch05-operationalize** — `docs/05`: turn the model-tiering prose into the mechanism (driver-fixed / worker-tiered, the tiers, the rubric, escalation) + `docs/04`/`docs/07` cross-refs for kill-and-escalate.
- **U-ledger-tier** — `templates/LEDGER.md.template`: `Tier` column + Conventions + default; **and** the immutability-hook index update (lockstep) + a real-ledger parse test.
- **U-dispatch** — `prompts/worker-dispatch.md` + `prompts/driver-loop.md`: driver resolves `Tier → (model, effort)` at spawn; the `ESCALATE:` worker-return convention; retry-with-escalation + kill in the loop.
- **U-audit** — `prompts/audit.md`: audit tier tracks the unit; the reverse-tier rule.
- **U-plugin** — plugin mirror of the above + any `/gotm:*` wiring; version bump; README **body**.
- **Then:** independent coherence audit, version per §13, commit + publish.
