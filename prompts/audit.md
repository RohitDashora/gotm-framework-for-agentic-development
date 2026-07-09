---
prompt: audit
purpose: run an independent audit of a claimed-done unit and return a verdict
audience: the driver (you read this, then dispatch an audit worker) + the audit worker
license: Apache 2.0
---

# Audit prompt

Use this to check an **authored-done** unit before any downstream consumes it. An audit is mechanical: a fresh worker reads the target and its oracle, categorizes findings by severity, and **returns a verdict**. The auditor does not fix anything and does not write the ledger — findings become new units, and the driver stamps the gate (`driver-loop.md` step 4).

The audit runs as a worker dispatch (`worker-dispatch.md`) with the audit-specific shape below.

### Independence is structural (not a rule to remember)

In GOTM the executor that produced the unit is an **ephemeral worker, already discarded** by the time anything checks the unit. So **auditor ≠ author** is not vigilance — there is no author left to grade itself. Therefore:

- **The driver dispatches a separate audit worker, every time.** Fresh context, no memory of producing anything.
- **The audit worker receives only the Target + the Oracle + the checks below** — never the authoring session's transcript, plan, or reasoning. The producing context is gone; do not reconstruct it.
- **One unit per audit.** One dispatch → one report (`audits/<Uxx>.md`) for one unit. No multi-unit reports, no "covered by another unit's audit." (A superseded unit is the only no-own-audit case; its cell reads `superseded by U<yy>`.)
- The auditor **returns a verdict**; it does **not** edit the ledger, does **not** stamp its own `Audit` cell, and does **not** fix the output. The driver applies the verdict and turns findings into follow-on units.

---

## Paste this into the audit worker

You are a fresh audit worker. You did not author this unit. Check the target against the oracle using the checks below, then return a verdict. Do not edit the target, the ledger, or anything else — report only.

### 1. Audit kind

Name what is being checked. Common kinds: `existence`, `structure`, `content-claim`, `source-fidelity`, `render`, `ledger`, `runtime`. One kind per audit (audits are atomic); if multiple are needed the driver dispatches multiple audits.

### 2. Target

    Target: <path>
    Unit being audited: <Uxx>

### 3. Oracle

The reference the target is checked against — inputs, spec, prior outputs. **This is the entire context you get** (target + oracle), by design:

    Oracle:
    - <path 1>
    - <path 2>

### 4. What to check

Default to the **7-point checklist** below unless the unit calls for a specialized kind. Each item is one mechanical check with a clear pass/fail answer:

    What to check (default 7-point):
    1. existence              — output exists at the ledger's stated path
    2. spec match             — content matches what the unit promised (sections/structure/length)
    3. cross-reference integrity — every D<n>/U<n>/Q<n> cited exists and says what's claimed
    4. internal consistency   — no contradictions across the audited set
    5. decision fidelity      — output honors the relevant DECISIONS entries
    6. enforcement check      — for each BEHAVIORAL decision the unit cites, is it held by a
                                gate / config / assertion, or only prose? documented-but-
                                unenforced is a finding (NOT the same as #5: fidelity asks
                                "does it honor the decision", enforcement asks "is it gated")
    7. multi-site claim check — any "wired into BOTH / applied across N / replaced everywhere"
                                claim is verified by grep/count, not trusted prose; expect a
                                guard (test/assertion) per site

Add or substitute kind-specific checks (render, source-fidelity, …) where the unit warrants.

> Checks 6–7 earn their place: in a ~113-audit project the only two FAILs both landed in
> exactly these blind spots — a decision documented but not enforced (no gate behind it),
> and a multi-site fix a bulk-replace silently half-applied. The 5-point core misses both.

### 4a. Runtime check — verified-done, for deploy/infra/data units

`authored-done` says the artifact exists and the author saw it work. That is **self-validation**, not verification: a green build or a clean local run, watched by the hand that built it, proves nothing independent. For any unit that **deploys, provisions infra, or produces data**, the audit must additionally **exercise the live artifact as its real consumer**:

- **Endpoint / service** → call it as the **real identity** a consumer uses (real auth, real route), and confirm the real response — not a localhost smoke test the author already ran.
- **Table / dataset** → **re-query the target** the way a downstream unit will, and confirm the rows/schema are actually there.
- **Config / gate** → trigger the behavior it's supposed to control and confirm it actually fires.

A thing is **verified-done** only when someone who was *not* the author drove it the way reality will. The author's own green result does not count.

### 4b. Kind → extra checks (typed verified-done)

The §4a runtime check is generic; "exercise the live artifact" means something **different per unit kind**. Read the unit's **Kind** (the ledger's `Kind` column; default `authoring`, kinds: `authoring` · `ui` · `eval` · `deploy-infra` · `data` · `diagnosis`) and run the kind-specific dimensions **atop** the 7-point + the §4a runtime check. A unit is not verified-done because it *ran* — it is verified-done when the kind-specific yardstick passes:

    Kind → extra checks:

    ui / visual
      - artifact-freshness: rebuild the artifact from CURRENT source, then audit
        that build — never a stale served bundle. (A "renders fine" on an old
        bundle is a self-validation, not a check.)
      - objective machine checks: assert DOM presence, bounding-box geometry,
        element counts — not worker prose about what it "looks like."
      - firsthand: the auditor views the rebuilt artifact itself; it does not
        trust a description of the visuals.

    eval / judge / measurement
      - harness-fairness (correctness IS fairness for these units — a biased
        harness yields confident-wrong conclusions the whole project leans on):
        * equal-fidelity inputs to BOTH arms (same evidence depth, same context
          budget — not titles-only on one side, full text on the other).
        * symmetric yardstick: the scoring rubric penalizes/credits both arms by
          the same rule; a cap that flags one arm's shown-but-uncited content as
          "fabricated" is a rigged yardstick.
        * A/B-swap for position bias: re-run with arms swapped; a verdict that
          flips on order is position bias, not signal.
        * confounds controlled or labelled: no arm carries an unrelated handicap
          (weaker model, different config); if one does, it is controlled or the
          result is labelled with the confound.
      - An eval unit that merely runs and emits a number is NOT verified-done.

    deploy-infra
      - exercise end-to-end AS THE DEPLOYED IDENTITY: call/query as the service
        principal / role the deployment actually runs under — "app is RUNNING"
        proves nothing if every query fails under the real identity's grants.
      - a hardcoded identity or endpoint is a check-6 enforcement finding: the
        binding is a fragile default that breaks on recreation.

    data
      - re-query the target AS THE CONSUMER: read it exactly how the downstream
        unit will (same identity, same query shape), confirm rows/schema are
        really there — not the author's write-side confirmation.

    diagnosis
      - reproduce under controlled conditions BEFORE root-causing: strip
        model / harness / config confounds and reproduce the symptom in
        isolation. A root cause named from a confounded signal (e.g. "X
        underperforms") risks fixing the wrong thing.

### 5. Risk-tier the audit weight

Spend the audit budget where the risk is (worker economy, not vigilance):

- **Keystone / deploy / infra / data units** → the **full** independent audit: the 7-point checklist *plus* the §4a runtime check.
- **Low-risk mechanical units** → a **lighter** check: existence + spec-match + compile/scan only. Record explicitly in the report that the light tier was used and why — a deliberate, logged tiering, never a silent skip.

### 6. Severity tiers (universal)

Categorize each finding into one of four tiers:

- **HIGH** — blocks the unit from being trusted as done; downstream cannot consume until a fix unit lands.
- **MEDIUM** — degrades quality but the output can be cited downstream; fix is desirable, not blocking.
- **LOW** — cosmetic; fix if convenient.
- **UNVERIFIED** — could not be checked (missing context, ambiguous spec, absent input); flag for the driver.

### 7. Report format

Write the report to `audits/<Uxx>.md`:

    # Audit report — <kind> — <date>

    ## Target audited
    File: <path>
    Unit: <Uxx>
    Tier: <full | light (reason)>

    ## Findings

    ### HIGH severity
    - <finding>: <one-paragraph description with cited file:line>
      - Suggested fix unit: <one-line proposal>

    ### MEDIUM severity
    - ...

    ### LOW severity
    - ...

    ### UNVERIFIED
    - <thing-could-not-check>: <what is missing>

    ## Runtime check (deploy/infra/data only)
    - Exercised as: <real consumer / identity / query>
    - Result: <what the live artifact actually returned>

    ## Summary
    HIGH: <n> · MEDIUM: <n> · LOW: <n> · UNVERIFIED: <n>
    Verdict: <PASS | PASS-FINDINGS | FAIL>   (HIGH ⇒ FAIL; MEDIUM/LOW-only ⇒ PASS-FINDINGS; clean ⇒ PASS)

### 8. Return format (what the worker hands back to the driver)

Return terse — a pointer plus index facts, never the report body:

    Audited: <Uxx>  ·  Report: audits/<Uxx>.md
    Verdict: <PASS | PASS-FINDINGS | FAIL>
    HIGH: <n> · MED: <n> · LOW: <n> · UNVERIFIED: <n>
    Fix units proposed: <one-liners, if any>

---

## After the audit — the driver acts (worker does not)

The driver reads the returned verdict and:

- **Stamps the ledger `Audit` cell** to match: `PASS→audits/<Uxx>.md`, `PASS-FINDINGS→audits/<Uxx>.md`, or `FAIL→audits/<Uxx>.md`. `PASS` / `PASS-FINDINGS` **open the gate** for downstream; a `FAIL` holds it shut until a follow-on unit lands and an independent re-audit passes.
- **Turns findings into units.** Each **HIGH** becomes a follow-on fix unit referencing the report. **MEDIUM** findings become optional follow-on units (or one batched "polish" unit). **LOW** findings are acted on now or deferred with a note. Findings never reach back and patch the audited output — the freeze means every change is an owned follow-on unit.
- **Routes UNVERIFIED** to `QUESTIONS` if a human decision is needed, or refines the audit's "what to check" and re-runs.

The audit cycle is part of normal forward motion. Drift is not avoided by being careful; drift is caught by being checked — by someone who didn't do the work.
