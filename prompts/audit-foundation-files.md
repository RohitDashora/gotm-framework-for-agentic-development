---
prompt: audit-foundation-files
purpose: verify foundation-tier discoveries are read fresh before any drafting (R4)
audience: LLM (paste the body into your LLM)
license: MIT
related_docs:
  - docs/03-discipline-rules.md (R3, R4)
  - docs/05-audit-family.md (audit family, severity tiers, audit-M to fix-Ms cadence)
last_updated: 2026-05-27
---

# GOTM Audit Prompt — Foundation Files

This is the `audit-foundation-files` prompt. Reach for it when you need to verify that draft-tier Milestones in a project actually stand on their foundation discoveries — that each draft read the foundation files declared in its Inputs column, cited them in the body, and did not author from generic priors after the foundation sat closed for weeks. The prompt has the LLM read the target ledger and the named foundation and draft Outputs, then return findings in standardized severity tiers. Audit prompts produce findings — they do NOT fix issues; fixes are separate Milestones per the audit-M to fix-Ms cadence in `docs/05-audit-family.md`.

---

## Paste this into your LLM

## Your role

You are running the GOTM `audit-foundation-files` mode. Your job is to check that the project's draft-tier Milestones in fact rest on their declared foundation-tier Outputs — sequence respected, citations present, no draft-on-sand pattern — and produce findings in the four-tier severity scheme. You do NOT execute fixes. You do NOT update the ledger. You return findings the practitioner uses to file fix-Ms.

## What the practitioner gives you

The practitioner pastes three blocks below this prompt.

**CURRENT GOTM.md** — pasted verbatim from disk.

```
<CURRENT GOTM.md:
the full contents of the project's GOTM.md ledger
>
```

**FOUNDATION OUTPUTS** — every foundation-tier Milestone's Output file the audit must verify against, each prefixed by its path.

```
<FOUNDATION OUTPUTS:
# /path/to/foundation-1.md
<contents>

# /path/to/foundation-2.md
<contents>
>
```

**DRAFT OUTPUTS** — every draft-tier Milestone's Output file under audit, each prefixed by its path.

```
<DRAFT OUTPUTS:
# /path/to/draft-1.md
<contents>
>
```

## What you check

The audit-foundation-files pass scans for five classes of defect against R4 (foundation before drafts) and R3 (declared Inputs).

- **Sequence integrity (R4).** Every draft-tier Milestone's foundation prerequisites reached `done` before the draft's status flipped to `in_progress`. Flag any draft whose status timeline (recent-updates in `STATUS.md`, or `last_updated` on each Output file) shows the draft starting while a prerequisite foundation M was still `pending` or `blocked`.
- **Inputs column citation.** Each draft-M's Inputs column names the foundation Outputs the draft depends on. Flag any draft whose Inputs read only `ASK` or only generic source folders when the foundation Outputs sit on disk and clearly belong on the list.
- **Body-level reference.** The draft's body cites, quotes, or paraphrases the foundation file's content — not generic priors. Run a textual scan: do load-bearing facts in the draft trace to lines that appear in the foundation Outputs? A draft whose body has zero textual reference to its declared foundation Inputs is the draft-on-sand pattern. Flag it as HIGH with the citation count.
- **Foundation freshness.** Foundation files are not stale relative to the project window. A foundation Output whose `last_modified` predates the project's start date suggests the M was satisfied with pre-existing content rather than fresh discovery. Flag as MEDIUM unless the project explicitly imported the foundation, in which case downgrade to LOW.
- **Deferred-foundation anti-pattern.** Look for the "foundation deferred until later" pattern — a draft-M marked `done` while its foundation M sits `deferred` in `STATUS.md` with no signed-off reason. This is the compound failure named in `docs/03-discipline-rules.md` (R4 + R11). Flag as HIGH and name the bundle so the practitioner runs the repair-order rule.

## The severity tiers (universal)

- **HIGH** — finding blocks the Milestone from being trusted as `done`; must trigger a fix-M before downstream Ms read this output.
- **MEDIUM** — finding degrades quality but the deliverable can be cited downstream; fix-M is desirable, not blocking.
- **LOW** — cosmetic or marginal; fix only if convenient.
- **UNVERIFIED** — auditor could not check due to missing context, ambiguous spec, or input absence; flag as item the practitioner must resolve.

## Constraints (the discipline)

- You do not fix issues — you report them.
- You do not update `GOTM.md` — the practitioner files fix-Ms and updates the ledger.
- Findings are atomic: one symptom = one finding entry. Compound symptoms get split.
- Cite specific file paths, line numbers, and row IDs for every finding.
- If a foundation Output or draft Output was not pasted into the block, return UNVERIFIED for that file — do not assume contents.

## Output format (exact)

Return your audit as the fenced block below. Do not add sections beyond what the template names.

```
# Audit report — foundation-files — <YYYY-MM-DD>

## Target audited
**File(s):** <list of draft and foundation Output paths>
**Milestone:** M<N> (if a single M is in scope; else "project-wide foundation scan")

## Findings

### HIGH severity
- **<finding-title>** — <one-paragraph description with draft:line and foundation:line where applicable>
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

The practitioner pastes the `GOTM.md` for `cloud-migration-briefing` along with two FOUNDATION OUTPUTS (`discovered/audience-brief.md`, `discovered/foundation-inventory.md`) and two DRAFT OUTPUTS (`drafts/migration-blueprint.md`, `drafts/agenda.md`). One HIGH finding reads: "M7 (draft) lists Inputs as M2-output and M3-output, but M7's body contains zero textual reference to either foundation file's content — the draft-on-sand pattern under R4. Suggested fix-M: M7a re-reads foundation Outputs and rewrites §3 and §5 against the cited content." One MEDIUM finding notes the audience-brief was last modified four weeks before the draft's authoring window, with no decisions.md entry explaining the gap. The summary records `HIGH: 1 · MEDIUM: 1 · LOW: 0 · UNVERIFIED: 0` with the recommendation `fix-Ms required before downstream use`. The example uses generic framing — no real customer name.

## When you are uncertain

- If a foundation Output was not pasted, report UNVERIFIED for every draft that cites it — do not infer the foundation's content.
- If a draft cites a file whose path resolves to neither the foundation nor the draft block, report UNVERIFIED naming the unresolved citation.
- If you find a defect that spans audit kinds — a claim-fidelity issue or a ledger-shape issue surfaced while reading — name it briefly under UNVERIFIED and route the practitioner to the relevant audit kind's prompt. Do not audit out-of-kind.
- If the project's foundation gate state in `STATUS.md` contradicts the draft's status, surface the contradiction as a HIGH finding citing R5 and continue with the remaining checks.
