# GOTM design records

The internal design blueprints (ADRs + dogfood logs) behind the framework — *how* GOTM was built, version by version, as it dogfooded itself. These are **not the product**: the product is the concept chapters (`../01`–`../09`), the `prompts/`, and the `templates/`. These records are kept for transparency and contributors; you do **not** need to read them to adopt GOTM (start at [`../01-the-problem-and-thesis.md`](../01-the-problem-and-thesis.md)).

| Blueprint | Shipped as | What it designed |
|---|---|---|
| [`V3-DESIGN.md`](V3-DESIGN.md) | **v3.0** | The from-first-principles rewrite to **driver / worker / store** — the 9-chapter spine, the scheduler loop, and the 8 locked decisions. |
| [`V3.1-ENHANCEMENT-DESIGN.md`](V3.1-ENHANCEMENT-DESIGN.md) | **v3.35** | Field-hardening from the first real v3 run — the 5 structural gaps (E1–E5): ledger micro-schema, typed `verified-done`, the destructive-op pre-gate, forced detail-to-disk, proof-stamped dispatch. *(Drafted under the working name "v3.1"; shipped as v3.35.)* |
| [`LEARNING-POOL-DESIGN.md`](LEARNING-POOL-DESIGN.md) | **v3.36** | The shared cross-project **learning pool (L2)** — `~/.gotm/learnings/` + `pool.py` + the promotion gate (candidate → validated via an independent project; contradiction demotes). |
| [`V4-VNEXT-DESIGN.md`](V4-VNEXT-DESIGN.md) | **v4.0** *(shipped)* | The declarative **context pool** — *facts*, not experience, as a second cross-project store: `subject`-keyed, supersede-on-change, commonality+curation promotion, the `shareable` privacy gate, and the bidirectional trust flow. Ships `context.py` + `context-analysis`/`consult-facts` prompts + `CONTEXT.md.template`. From the "GOTM vNext / organizational learning system" feedback. |
| [`MODEL-TIERING-DESIGN.md`](MODEL-TIERING-DESIGN.md) | **v4.1** *(design / for-redline)* | Driver-assigned **per-worker model tiering** — the compute-economy layer over the context economy. Driver fixed at the user's SOTA+xhigh as the *allocator*; workers tiered **(model × effort)** per task by rubric; **kill-and-respawn one tier up** on self-escalate / watchdog / audit-FAIL; made safe by the *blast-radius = kill-safety* rule and the audit gate as the free cascade verifier. |

> These carry internal IDs (`Q-v3-*`), version bumps, and dogfood ledgers — the honest record of GOTM building GOTM. The concept chapters distill what's durable; these keep the reasoning.
