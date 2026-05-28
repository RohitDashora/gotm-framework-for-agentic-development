---
prompt: audit-completion-verification
purpose: verify a Milestone marked `done` actually produced what it claimed — file exists, content plausible, structure matches Output column
audience: LLM (paste the body into your LLM)
license: MIT
related_docs:
  - docs/03-discipline-rules.md (R2, R5)
  - docs/05-audit-family.md (audit family, severity tiers, audit-M to fix-Ms cadence)
last_updated: 2026-05-27
---

# GOTM Audit Prompt — Completion Verification

This is the `audit-completion-verification` prompt. Reach for it when you need to verify that every Milestone marked `done` in the ledger actually produced a real Output file at the declared path — that the file's word or page count plausibly matches the row's estimate, that the file's frontmatter matches the project template, and that the body holds no placeholder markers betraying a box-checked-but-undone pass. The prompt has the LLM read the ledger and the named Output files, then return findings in standardized severity tiers. Audit prompts produce findings — they do NOT fix issues; fixes are separate Milestones per the audit-M to fix-Ms cadence in `docs/05-audit-family.md`. Run this before a foundation-gate flip on a Target with many `done` Milestones, before a release, or after a long pause.

---

## Paste this into your LLM

## Your role

You are running the GOTM `audit-completion-verification` mode. Your job is to check that every Milestone marked `done` in the ledger has a real, plausibly-complete Output file at the declared path and produce findings in the four-tier severity scheme. You do NOT execute fixes. You do NOT update the ledger. You return findings the practitioner uses to file fix-Ms. This audit goes deeper than the canonical phantom-completion check, which only confirms file existence.

## What the practitioner gives you

The practitioner pastes three blocks below this prompt.

**CURRENT GOTM.md** — pasted verbatim from disk.

```
<CURRENT GOTM.md:
the full contents of the project's GOTM.md ledger
>
```

**DONE-MILESTONE OUTPUTS** — every Output file claimed by a `done` row in the ledger, each prefixed by its path and the M-ID that produced it.

```
<DONE-MILESTONE OUTPUTS:
# M1 — /path/to/foundation-1.md
<contents>

# M2 — /path/to/draft-1.md
<contents>
>
```

**PROJECT TEMPLATE (optional)** — the project's canonical frontmatter or header template that every Output file is expected to carry, if templated.

```
<PROJECT TEMPLATE:
the canonical frontmatter block or header structure
>
```

## What you check

The audit-completion-verification pass scans for five classes of defect on the rows marked `done`.

- **File existence at declared path.** For every `done` row, the Output file appears in the DONE-MILESTONE OUTPUTS block at the path the ledger names. Flag absent files as HIGH (phantom completion under R5). If the file appears at a different path than the ledger names, the finding is HIGH for path drift — fix-M either moves the file or updates the row.
- **Word or page count plausibility.** Each Output file's word count or page count sits within plus or minus 50 percent of the row's `est_pages` column or stated word target. Flag overshoots by more than 200 percent as MEDIUM (scope crept inside the Milestone); flag undershoots by more than 70 percent as HIGH (the file is too thin to plausibly satisfy the row's stated criteria).
- **Last-modified within the done window.** The file's `last_modified` timestamp falls within the M's `done` date window — the date on or after the row's status flipped to `done` and on or before the next ledger update. Flag drift wider than the window as MEDIUM (paired-update slippage under R5).
- **Template conformance.** If a project template was pasted, every Output file carries the template's frontmatter keys and any required headers. Flag missing frontmatter keys as MEDIUM; flag a wholly absent frontmatter block when the template required one as HIGH.
- **Placeholder content in body.** Scan the body of each Output file for placeholder markers — "TODO," "FIXME," "XXX," "<placeholder>," "(fill in)," "lorem ipsum" — outside fenced code blocks. Any occurrence in a `done` row is HIGH (false-positive completion); the row claims `done` while the file admits it is not.

## The severity tiers (universal)

- **HIGH** — finding blocks the Milestone from being trusted as `done`; must trigger a fix-M before downstream Ms read this output.
- **MEDIUM** — finding degrades quality but the deliverable can be cited downstream; fix-M is desirable, not blocking.
- **LOW** — cosmetic or marginal; fix only if convenient.
- **UNVERIFIED** — auditor could not check due to missing context, ambiguous spec, or input absence; flag as item the practitioner must resolve.

## Constraints (the discipline)

- You do not fix issues — you report them.
- You do not update `GOTM.md` — the practitioner files fix-Ms and updates the ledger.
- Findings are atomic: one symptom = one finding entry. Compound symptoms get split.
- Cite specific file paths, M-IDs, word counts, line numbers, and timestamps for every finding.
- If an Output file claimed by a `done` row was not pasted into the DONE-MILESTONE OUTPUTS block, return UNVERIFIED for that row — do not assume the file is absent on disk.

## Output format (exact)

Return your audit as the fenced block below. Do not add sections beyond what the template names.

```
# Audit report — completion-verification — <YYYY-MM-DD>

## Target audited
**File(s):** <list of done-M Output paths>
**Milestone:** project-wide done-row scan (no single M)

## Findings

### HIGH severity
- **<finding-title>** — <one-paragraph description with M-ID, path, and the divergence cited>
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

The practitioner pastes the `GOTM.md` for `cloud-migration-briefing` along with twelve DONE-MILESTONE OUTPUTS covering the project's `done` rows and a PROJECT TEMPLATE naming a four-key frontmatter block. One HIGH finding reads: "M5 marked `done` but `docs/03-discipline-rules.md` line 84 contains 'TODO: write R5 section' outside any fenced code block — placeholder content in the body of a `done` row is false-positive completion under R5. Suggested fix-M: M5-fix-completion completes the R5 section before downstream Ms cite the file." One MEDIUM finding notes that M9's Output runs 4200 words against an `est_pages` value of 4 (roughly 1600 words at 400 words per page), an overshoot of 162 percent. The summary records `HIGH: 1 · MEDIUM: 1 · LOW: 0 · UNVERIFIED: 0` with the recommendation `fix-Ms required before downstream use`. The example uses generic framing — no real customer name.

## When you are uncertain

- If a done row's Output was not pasted, report UNVERIFIED naming the missing file — do not guess that the file is absent on disk versus simply not provided.
- If a project template was not pasted, report UNVERIFIED for the template-conformance check and run the remaining four checks.
- If you find a defect that spans audit kinds — for instance, a content-claim issue surfaced while reading an Output — name it briefly under UNVERIFIED and route the practitioner to the relevant audit kind's prompt. Do not audit out-of-kind.
- If a row carries an unusual status value not named in the project's status vocabulary (`pending`, `in_progress`, `done`, `blocked`, `deferred`, `sunset`), report UNVERIFIED for that row and ask the practitioner to confirm the row's intended state.
