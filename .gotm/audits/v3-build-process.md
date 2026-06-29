# Process Audit — Did the v3 BUILD honor GOTM's own fundamentals?

**Subject:** the v3 rewrite of the framework (docs + prompts + templates + meta-example migration + converter), driven as a "dogfooded" GOTM v3 project.
**Oracle:** `templates/PROTOCOL.md.template` — the five rules + the *Audit gates* section (structural independence; the gate; one audit per unit; weight-by-risk-but-never-skip-the-gate; logged tiering).
**Auditor stance:** independent, adversarial. I did not author any build unit. Claims of "we dogfooded it" are treated as claims to be falsified, not accepted.
**Date:** 2026-06-29

---

## Summary

The v3 build honored GOTM's *authoring* fundamentals (DAG, foundation-first, born-tiered store) but **broke the audit/ledger fundamentals it spent the most ink teaching**. Only **6 of ~24 build units got an independent audit file**; the entire prompts phase, templates phase, README, MIGRATION.md, and the 368-line converter went to a now-**PUBLIC** repo with **zero** independent audit artifact. The build ran off a **side tracker (`V3-DESIGN.md §11`), not a gated `.gotm/LEDGER.md`** — so the gate ("downstream consumes only a passed input") was never structurally enforceable, and the keystone claim "all 80 v2 units archived losslessly" is provably false from disk.

**Verdict: FAIL (process).** Multiple HIGH process gaps; the build did not run under the discipline it ships, and at least two gaps carry concrete, shipped deliverable risk.

---

## Scorecard — the five rules + audit gates

| GOTM fundamental | Honored? | Evidence |
|---|---|---|
| **1. Single gated ledger (single writer)** | **NO** | The build was tracked in `V3-DESIGN.md §11` ("Rewrite progress — driver log"), a free-text table, **not** `.gotm/LEDGER.md`. The real ledger explicitly says *"there are no open mission units in this ledger… tracked in V3-DESIGN §11… not re-registered as U-rows here."* No `Audit` column, no per-unit gate, for any v3 unit. |
| **2. Atomic units = dispatch specs** | **PARTIAL** | Chapters were atomic (one file each, audited individually for ch1–7). But "PROMPTS PHASE", "TEMPLATES PHASE", and "Migration (step 1/2)" were tracked as **phase-level blobs**, not atomic gated units — 6 prompts + 7 templates + README + MIGRATION + converter collapsed into ~3 §11 bullets. |
| **3. Foundation before drafts** | **YES** | `V3-DESIGN.md` is a real locked blueprint; §10 marks "all foundational questions resolved — the blueprint is stable" before chapter units ran; every audit names it as the oracle. The DAG-topology intent was followed for the docs spine. *(But see Gap D — "locked" was self-asserted by the build, never independently ratified before drafting.)* |
| **4. Audit before downstream consumes — by an independent worker** | **NO (largely)** | 6 chapter audits exist (`v3-ch01/02/03/05/06/07.md`), all genuinely independent and rigorous. **ch4, ch8, ch9 got NO audit** ("validated (coherence pass)"). **All 6 prompts, all 7 templates, README, MIGRATION.md, the converter — NO audit file at all.** Downstream (the live meta-example `.gotm/PROTOCOL.md`, `CLAUDE.md`, README, public repo) **consumed un-audited templates/prompts** — a direct gate violation. |
| **Audit gates — one audit per unit** | **NO** | Where audits happened they were 1-per-chapter (good). But the **dominant pattern was batched coherence/validation**, not per-unit audit. §11 itself admits ch4/8/9 are "validated within the fan-in coherence pass rather than standalone audits." For prompts/templates the §11 claim "worker-dispatch & audit PASS… PROTOCOL.md.template keystone PASS… LEDGER.md.template PASS" has **no corresponding audit artifact** — the PASS verdicts are asserted in prose with nothing on disk to check them against. |
| **Audit gates — weight by risk, but never skip the gate + LOG the tiering** | **PARTIAL** | The chapter tier-down (ch4/8/9 → coherence pass) **was logged** (§11 line 147, "a deliberate, logged audit-budget tiering, not a silent skip") — credit where due. But the **prompts/templates/migration/converter tier-down was NOT logged as a decision** — it is simply absent. D23 even *claims* "independent audit workers" ran across the rewrite; the disk shows that's true only for 6 chapters. |

### Coverage quantified

Enumerated v3 build units and their audit status:

| Unit | Independent audit file? |
|---|---|
| docs ch1 | ✅ `v3-ch01.md` (PASS-FINDINGS) |
| docs ch2 | ✅ `v3-ch02.md` (PASS-FINDINGS) |
| docs ch3 | ✅ `v3-ch03.md` (PASS) |
| docs ch4 | ❌ "coherence pass" only |
| docs ch5 | ✅ `v3-ch05.md` (PASS-FINDINGS) |
| docs ch6 | ✅ `v3-ch06.md` (PASS-FINDINGS) |
| docs ch7 | ✅ `v3-ch07.md` (PASS-FINDINGS) |
| docs ch8 | ❌ "coherence pass" only |
| docs ch9 | ❌ "coherence pass" only |
| prompt `driver-loop.md` | ❌ none |
| prompt `worker-dispatch.md` | ❌ none (§11 asserts "PASS" — no file) |
| prompt `audit.md` | ❌ none (§11 asserts "PASS" — no file) |
| prompt `session-start.md` | ❌ none |
| prompt `consult.md` | ❌ none |
| prompt `outcome-analysis.md` | ❌ none |
| template `PROTOCOL.md.template` (keystone) | ❌ none (§11 asserts "keystone, PASS" — no file) |
| template `LEDGER.md.template` | ❌ none (§11 asserts "PASS" — no file) |
| templates DECISIONS/QUESTIONS/README/LEARNINGS/CONSULTED (5) | ❌ none |
| `README.md` rewrite | ❌ none |
| `MIGRATION.md` | ❌ none |
| `scripts/migrate_ledger_v2_to_v3.py` (368 lines, runtime/data unit) | ❌ none — **and never verified-done** (see Gap B) |
| meta-example `.gotm/` migration | ❌ none |

**Independent-audit coverage ≈ 6 / 24 build units ≈ 25%.** The 75% with no audit includes the **keystone template** (`PROTOCOL.md.template` — the thing this whole report is judged against) and the **only executable unit** (the converter), i.e. exactly the unit types PROTOCOL says get the *heaviest* audit ("full independent audit for keystone/deploy/runtime units").

---

## Gap → deliverable-risk table (ranked by real risk)

| # | Process gap | Concrete deliverable defect it could let through | Risk |
|---|---|---|---|
| **A** | **Keystone `PROTOCOL.md.template` shipped un-audited.** §11 asserts "keystone, PASS" but no `audits/v3-*template*.md` exists. PROTOCOL says keystone units get the *full* independent audit. | This template is what every adopter pastes in as their operating contract — and is the oracle this very report uses. An unaudited error here (a wrong gate rule, a self-contradiction, a broken cross-ref) propagates to *every* downstream project. The build's own missing-audit pattern means no fresh context ever ran the 7-point checklist against it. | **HIGH** |
| **B** | **Converter `migrate_ledger_v2_to_v3.py` never verified-done; "all 80 v2 units archived losslessly" (D23) is false on disk.** PROTOCOL: deploy/infra/**data** units must be *exercised by a real consumer*; a green run is not verification. The repo's own ledger archives **U1–U72 (72 units), not 80**, and there is **no `LEDGER.md.bak` / `LEDGER-ARCHIVE.md`** — the artifacts the converter is documented to emit. The repo's own migration was done **by hand**, not by the tool it ships. | Adopters run this converter on *their* real ledgers trusting "MISSING: NONE = lossless." An un-exercised parser (line-level pipe handling, status mapping) can silently drop or mis-tier units. The framework ships an unverified data-migration tool with a lossless guarantee it never demonstrated on a real ledger — and its headline number (80) is already wrong in the published decision log. | **HIGH** |
| **C** | **Prompts + templates consumed downstream before/without audit; gate never enforceable (no `Audit` column anywhere).** The live meta-example (`.gotm/PROTOCOL.md`, `CLAUDE.md`, README) and the **public** repo were built on un-audited prompts/templates. The "gate" cannot have held because there was no gated ledger to hold it. | Any defect in the 6 prompts or 7 templates (a dangling link, a stale "5-point" vs "7-point", a wrong path, an instruction that contradicts PROTOCOL) shipped publicly unchecked by an independent context. The build's *own* history shows this class is real: prior v2 audits repeatedly caught exactly these (link drift, "5→7" mismatches). 75% of v3 units skipped that net. | **HIGH** |
| **D** | **Blueprint "locked" was self-asserted, not ratified before drafting.** §10 says "all foundational questions resolved — the blueprint is stable," but D23/D24 (the decisions that record the v3 architecture and the public flip) were **only written into `.gotm/DECISIONS.md` in the final commit (8bcb5f8), after the whole build was done and pushed.** Foundation-before-drafts in spirit requires the design ratified *before* the drafts depend on it. | The 9 chapters + all prompts/templates were authored against a blueprint whose governing decisions were back-filled at the end. If the blueprint had a flaw, the ratification step that exists to catch it ran *after* everything already depended on it — defeating the gate's purpose. Lower risk than A–C because the blueprint is genuinely detailed and the chapter audits did check fidelity to it. | **MEDIUM** |
| **E** | **Atomicity violated: phase-blob tracking.** Prompts/templates/migration tracked as ~3 §11 bullets, not per-unit rows. | Obscures coverage: it *looks* like "PROMPTS PHASE COMPLETE ✅" is one green checkmark, hiding that 6 distinct deliverables got 0 audits. The blob framing is *how* gaps A–C stayed invisible. | **MEDIUM** |

---

## What the build got right (to be fair)

- The **6 chapter audits that exist are excellent** — genuinely independent (each header states "did not author"), each runs a multi-tier checklist, decision-fidelity-against-the-blueprint is rigorous, findings are honest LOW/MEDIUM with no rubber-stamping.
- **Foundation-first** for the docs spine was real: a substantive locked blueprint preceded the chapters.
- The **born-tiered ledger migration** is conceptually sound and the ledger is genuinely tiered (frontier/archive) — the repo does demonstrate that primitive.
- The **chapter-level audit tier-down was logged** (§11), which is exactly the "log it, don't skip silently" rule — the build followed it for *that* tier-down, then failed to extend the same honesty to prompts/templates/migration.

---

## Verdict

**FAIL (process).** The v3 build is a partial dogfood: it honored the *authoring* half of GOTM (DAG, foundation, atomic chapters, born-tiered store) but **violated the audit-and-gate half** that v3 exists to enforce. The discipline's central promise — *nothing downstream consumes an un-audited input; every keystone/runtime unit gets a full independent audit; one audit per unit on a single gated ledger* — was not met for ~75% of the build, including the keystone template and the only executable artifact, all now public.

The irony is load-bearing: a framework whose thesis is "you cannot self-certify your own work" largely **self-certified its own rewrite**, recording PASS verdicts in a prose tracker with no independent audit artifacts behind them.
