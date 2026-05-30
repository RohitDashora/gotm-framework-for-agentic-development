---
prompt: audit
purpose: run a mechanical audit of a claimed-done unit
audience: orchestrating LLM (you read this, then build an audit dispatch)
license: Apache 2.0
---

# Audit prompt

Use this template to audit a claimed-done unit before downstream work consumes it (rule 4 of the protocol). Audits are mechanical: read target, read oracle, return findings in severity tiers. The auditor does not fix issues — fixes are separate units.

Audits run as dispatched subagents per `prompts/subagent-dispatch.md`, with the audit-specific shape below.

---

## Paste this into the orchestrating LLM

You are about to dispatch an audit subagent. Build the audit dispatch using the template below.

### 1. Audit kind

Name what is being checked. Common kinds:

    - existence: does the named output file exist at the stated path
    - structure: do the required sections appear; is the format what was promised
    - content-claim: do load-bearing claims in the output trace to the cited sources
    - source-fidelity: do quoted spans match the source verbatim
    - render: does the output render cleanly (markdown, tables, fences, images, links)
    - ledger: does `LEDGER.md` remain well-formed under the protocol's rules

Pick one. Audits are atomic — one kind per audit. If multiple kinds are needed, dispatch multiple audits.

### 2. Target

The file(s) being audited:

    Target: <path>
    Unit being audited: <Uxx>

### 3. Oracle

The reference the target is checked against (sources, spec, prior outputs):

    Oracle:
    - <path 1>
    - <path 2>

### 4. What to check

A short list, customized to the audit kind. Each item is one mechanical check phrased so it has a clear pass/fail answer.

    What to check:
    - <check 1, phrased as a question with pass/fail>
    - <check 2>
    - <check 3>

### 5. Severity tiers (universal)

The worker categorizes each finding into one of four tiers:

- **HIGH** — finding blocks the unit from being trusted as done; downstream work cannot consume the output until a fix unit lands.
- **MEDIUM** — finding degrades quality but the output can be cited downstream; fix is desirable, not blocking.
- **LOW** — cosmetic; fix if convenient.
- **UNVERIFIED** — auditor could not check due to missing context, ambiguous spec, or input absence; flag for the practitioner.

### 6. Return format

The audit report the worker writes (typically to `audits/<Uxx>.md`):

    # Audit report — <kind> — <date>

    ## Target audited
    File: <path>
    Unit: <Uxx>

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

    ## Summary
    HIGH: <n> · MEDIUM: <n> · LOW: <n> · UNVERIFIED: <n>
    Recommendation: <"fix units required before downstream consumes" / "passes; optional polish" / "blocked on UNVERIFIED">

### After the audit

The orchestrating agent reads the audit report and acts:

- For each **HIGH** finding, append a fix unit to `LEDGER.md`. The fix unit's row references the audit report.
- For **MEDIUM** findings, append as optional follow-on units (or batch into a single "polish" unit if many are minor).
- For **LOW** findings, decide whether to act now or defer; if deferring, note in `LEDGER.md` recent updates.
- For **UNVERIFIED** items, route the resolution to `QUESTIONS.md` if a human decision is needed, or refine the audit's "what to check" and re-run.

The audit cycle is part of the project's normal forward motion. Drift is not avoided by being careful; drift is caught by being checked.
