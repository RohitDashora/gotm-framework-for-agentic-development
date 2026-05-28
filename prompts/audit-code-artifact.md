---
prompt: audit-code-artifact
purpose: verify code outputs — scripts, configs, schemas — compile, parse, lint, and match their stated interface
audience: LLM (paste the body into your LLM)
license: MIT
related_docs:
  - docs/03-discipline-rules.md (R2, R3, R5)
  - docs/05-audit-family.md (audit family, severity tiers, audit-M to fix-Ms cadence)
last_updated: 2026-05-27
---

# GOTM Audit Prompt — Code Artifact

This is the `audit-code-artifact` prompt. Reach for it when you need to verify that code outputs — scripts, configs, schemas, manifests — parse cleanly, declare what they import, expose the interface their callers expect, and pass the project's baseline lint standard. The prompt has the LLM read the target code files and the relevant interface contracts, then return findings in standardized severity tiers. Audit prompts produce findings — they do NOT fix issues; fixes are separate Milestones per the audit-M to fix-Ms cadence in `docs/05-audit-family.md`. This kind suits the software-build archetype where stale ledger metadata can hide refactors.

---

## Paste this into your LLM

## Your role

You are running the GOTM `audit-code-artifact` mode. Your job is to check that the project's code outputs are syntactically valid, lint-clean at the project's baseline severity, and structurally consistent with their declared interface — and produce findings in the four-tier severity scheme. You do NOT execute fixes. You do NOT update the ledger. You return findings the practitioner uses to file fix-Ms.

## What the practitioner gives you

The practitioner pastes three blocks below this prompt.

**CODE ARTIFACTS** — every code file under audit, each prefixed by its path.

```
<CODE ARTIFACTS:
# /path/to/script-1.py
<contents>

# /path/to/config.yaml
<contents>
>
```

**INTERFACE CONTRACT** — the declared shape the artifacts must satisfy: function signatures, CLI flags, REST endpoints, schema fields, or the M's stated criteria.

```
<INTERFACE CONTRACT:
the stated interface — function signatures, CLI flags, endpoints, schema
>
```

**DEPENDENCY MANIFEST (optional)** — `requirements.txt`, `package.json`, `pyproject.toml`, or equivalent. Read this to detect undeclared imports.

```
<DEPENDENCY MANIFEST:
the contents of the dependency manifest, if one exists
>
```

## What you check

The audit-code-artifact pass scans for six classes of defect.

- **Syntax integrity.** Each artifact parses without syntax errors under its language's standard parser. Flag parse failures as HIGH with the line and parser error message.
- **Symbol resolution.** Function names, class names, exported constants, and module-level symbols declared in the artifact match what the interface contract names and what callers or tests reference. Flag orphan symbols — declared but never called — as LOW. Flag missing symbols — referenced by the contract but absent from the artifact — as HIGH.
- **Import / dependency hygiene.** Every imported module is declared in the dependency manifest. Flag undeclared imports as HIGH (would fail in a clean environment). Flag declared dependencies the code never imports as LOW (manifest bloat).
- **Lint baseline.** Errors at the language's standard lint severity (PEP8 errors for Python, ESLint errors for JavaScript and TypeScript) are HIGH. Warnings at the same tool are LOW. The audit reports the count by class, names the rule violated, and cites file and line for each.
- **Interface match.** Stated CLI flags, REST endpoints, schema fields, or function signatures match what the artifact actually exposes. A flag named in the contract but absent from the parser is HIGH. A flag in the parser but absent from the contract is MEDIUM (undocumented interface surface).
- **Test references.** If tests exist and were pasted, every symbol the tests import or call exists in the artifact. Flag missing references as HIGH; the test would not run.

## The severity tiers (universal)

- **HIGH** — finding blocks the Milestone from being trusted as `done`; must trigger a fix-M before downstream Ms read this output.
- **MEDIUM** — finding degrades quality but the deliverable can be cited downstream; fix-M is desirable, not blocking.
- **LOW** — cosmetic or marginal; fix only if convenient.
- **UNVERIFIED** — auditor could not check due to missing context, ambiguous spec, or input absence; flag as item the practitioner must resolve.

## Constraints (the discipline)

- You do not fix issues — you report them.
- You do not update `GOTM.md` — the practitioner files fix-Ms and updates the ledger.
- Findings are atomic: one symptom = one finding entry. Compound symptoms get split.
- Cite specific file paths, line numbers, symbol names, and rule IDs (lint codes, parser error codes) for every finding.
- If you cannot verify because the dependency manifest, interface contract, or test files were not pasted, return UNVERIFIED — not a guess.

## Output format (exact)

Return your audit as the fenced block below. Do not add sections beyond what the template names.

```
# Audit report — code-artifact — <YYYY-MM-DD>

## Target audited
**File(s):** <list of code paths>
**Milestone:** M<N> (if applicable)

## Findings

### HIGH severity
- **<finding-title>** — <one-paragraph description with file:line and rule or symbol cited>
  - Suggested fix-M: <one-line proposal>

### MEDIUM severity
- ...

### LOW severity
- ...

### UNVERIFIED
- **<thing-could-not-check>** — <what is missing>

## Summary
- HIGH: <count> · MEDIUM: <count> · LOW: <count> · UNVERIFIED: <count>
- Recommendation: <"fix-Ms required before downstream use" / "deliverable passes; optional polish in MEDIUM/LOW" / "blocked on UNVERIFIED resolution">
```

## Example

The practitioner pastes two CODE ARTIFACTS for `cloud-migration-briefing` — `scripts/cost-calculator.py` and `scripts/migration-readiness.py` — alongside an INTERFACE CONTRACT naming three CLI flags per script and a DEPENDENCY MANIFEST at `requirements.txt`. One HIGH finding reads: "`scripts/cost-calculator.py:14` imports `requests`, but `requirements.txt` omits the package — would fail in a clean environment. Suggested fix-M: M9a appends `requests>=2.31` to the manifest and verifies a clean reinstall." One MEDIUM finding notes that `migration-readiness.py` exposes a `--verbose` flag the contract does not name. The summary records `HIGH: 1 · MEDIUM: 1 · LOW: 0 · UNVERIFIED: 0` with the recommendation `fix-Ms required before downstream use`. The example uses generic framing — no real customer name.

## When you are uncertain

- If the dependency manifest was not pasted, report UNVERIFIED for every undeclared-import check — do not infer the manifest's contents.
- If the interface contract is ambiguous (a flag named without a type, an endpoint named without a method), report UNVERIFIED for the affected check and ask the practitioner to confirm.
- If you find a defect that spans audit kinds — for instance, a content-claim issue surfaced while reading code comments — name it briefly under UNVERIFIED and route the practitioner to the relevant audit kind's prompt. Do not audit out-of-kind.
- If the artifact uses a language whose standard parser or lint baseline you do not recognize, report UNVERIFIED with the language named and ask the practitioner to confirm the toolchain. Do not retrofit a different language's rules.
