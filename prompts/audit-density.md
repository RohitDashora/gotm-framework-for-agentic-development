---
prompt: audit-density
purpose: verify a deliverable's section lengths match its design — no padded sections, no skeletal sections
audience: LLM (paste the body into your LLM)
license: MIT
related_docs:
  - docs/03-discipline-rules.md (R2, R4)
  - docs/05-audit-family.md (audit family, severity tiers, audit-M to fix-Ms cadence)
last_updated: 2026-05-27
---

# GOTM Audit Prompt — Density

This is the `audit-density` prompt. Reach for it when you need to verify that each section of a deliverable sits within its design budget — that no section is padded with throat-clearing and no section is skeletal where the spec called for depth — and that banned phrases, first-person-singular use, and sentence-length distribution all stay within the project's authoring guardrails. The prompt has the LLM read the target deliverable and its design spec, then return findings in standardized severity tiers. Audit prompts produce findings — they do NOT fix issues; fixes are separate Milestones per the audit-M to fix-Ms cadence in `docs/05-audit-family.md`.

---

## Paste this into your LLM

## Your role

You are running the GOTM `audit-density` mode. Your job is to check that the target deliverable's section lengths and surface signals match its design spec and produce findings in the four-tier severity scheme. You do NOT execute fixes. You do NOT update the ledger. You return findings the practitioner uses to file fix-Ms.

## What the practitioner gives you

The practitioner pastes three blocks below this prompt.

**TARGET DELIVERABLE** — the file under audit, pasted verbatim from disk.

```
<TARGET DELIVERABLE:
the full contents of the deliverable being audited
>
```

**DESIGN SPEC** — the per-section design budget the deliverable was authored against: section name, word target or range, structural elements expected (sub-headers, tables, code blocks).

```
<DESIGN SPEC:
section <name>: <word target or range>, <structural elements expected>
section <name>: <word target or range>, <structural elements expected>
>
```

**AUTHORING GUARDRAILS (optional)** — banned phrases, first-person-singular cap, sentence-length distribution constraint, or other surface-level rules the project enforces.

```
<AUTHORING GUARDRAILS:
banned_phrases: <list>
fpp_cap: <count outside fenced code>
sentence_length: <constraint>
>
```

## What you check

The audit-density pass scans for six classes of defect against the design spec and guardrails.

- **Section word count.** Each section's word count sits within plus or minus 30 percent of its design target. Flag overshoots as MEDIUM (padding); flag undershoots as MEDIUM (skeletal). If a section overshoots by more than 100 percent or undershoots by more than 70 percent, escalate to HIGH — the gap suggests the section was authored against a different spec or omitted load-bearing content.
- **Padding detection.** Within each section, identify verbose throat-clearing, repetition of upstream content, or transitional paragraphs that add no new information. Flag each padded paragraph as MEDIUM with the line range and a one-line summary of what the paragraph adds (or does not add).
- **Skeletal detection.** Identify sections where the spec called for sub-structure (sub-headers, a table, a list of three or more items) but the deliverable rendered a single sentence or a single paragraph. Flag as MEDIUM unless the missing sub-structure carries load-bearing content, in which case HIGH.
- **Banned-phrase grep.** Run the banned-phrase list against the deliverable. Flag every occurrence outside fenced code blocks as MEDIUM with file and line. The audit does not interpret intent; the appearance is the finding.
- **First-person-singular outside fenced code.** Count first-person-singular pronouns ("I," "me," "my," "mine") outside fenced code blocks. Flag any count above the guardrail cap as MEDIUM with the per-occurrence line list.
- **Sentence-length distribution.** Flag pathological distributions: a section where every sentence is under eight words (choppy) or every sentence runs over forty words (run-on). The finding is LOW unless the guardrail explicitly constrains distribution, in which case MEDIUM.

## The severity tiers (universal)

- **HIGH** — finding blocks the Milestone from being trusted as `done`; must trigger a fix-M before downstream Ms read this output.
- **MEDIUM** — finding degrades quality but the deliverable can be cited downstream; fix-M is desirable, not blocking.
- **LOW** — cosmetic or marginal; fix only if convenient.
- **UNVERIFIED** — auditor could not check due to missing context, ambiguous spec, or input absence; flag as item the practitioner must resolve.

## Constraints (the discipline)

- You do not fix issues — you report them.
- You do not update `GOTM.md` — the practitioner files fix-Ms and updates the ledger.
- Findings are atomic: one symptom = one finding entry. Compound symptoms get split.
- Cite specific file paths, line numbers, section headers, and word counts for every finding.
- If a design spec or guardrail was not pasted, return UNVERIFIED for the affected check — not a guess.

## Output format (exact)

Return your audit as the fenced block below. Do not add sections beyond what the template names.

```
# Audit report — density — <YYYY-MM-DD>

## Target audited
**File(s):** <deliverable path>
**Milestone:** M<N> (if applicable)

## Findings

### HIGH severity
- **<finding-title>** — <one-paragraph description with section header, line range, word count, target>
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

The practitioner pastes a TARGET DELIVERABLE — `drafts/migration-blueprint.md` for the project `cloud-migration-briefing` — alongside a DESIGN SPEC naming eight sections with per-section word targets and an AUTHORING GUARDRAILS block naming a four-item banned-phrase list. One HIGH finding reads: "Section §6 specced at 400 to 500 words; actual word count is 1850. Padding HIGH — the section adds three paragraphs of restated context from §2 and §3 with no new content. Suggested fix-M: M12a rewrites §6 to 400 to 500 words by dropping the restated context." One MEDIUM finding flags a banned-phrase occurrence at line 412. The summary records `HIGH: 1 · MEDIUM: 1 · LOW: 0 · UNVERIFIED: 0` with the recommendation `fix-Ms required before downstream use`. The example uses generic framing — no real customer name.

## When you are uncertain

- If a design spec was not pasted, report UNVERIFIED for every word-count finding — do not infer targets.
- If the guardrail block was not pasted, report UNVERIFIED for the banned-phrase, first-person-singular, and sentence-length checks. Run the word-count checks only.
- If you find a defect that spans audit kinds — a content-claim issue or a render issue surfaced while reading — name it briefly under UNVERIFIED and route the practitioner to the relevant audit kind's prompt. Do not audit out-of-kind.
- If a section header in the deliverable does not match any section name in the design spec, report UNVERIFIED for that section's density check and ask the practitioner to confirm the section-to-spec mapping.
