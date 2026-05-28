---
chapter: "docs/05-audit-family.md"
title: "The audit family"
audience: "LLM practitioners running complex multi-pass work"
word_target: 2200
produced_by: subagent
last_updated: 2026-05-27
project: gotm-framework-for-agentic-development
inputs:
  - docs/01-why.md (M3 voice)
  - docs/02-hierarchy.md (M4)
  - docs/03-discipline-rules.md (M5)
  - docs/04-modes.md (M6)
  - gotm-playbook/07-lessons/README.md (Ch 7.4 + 7.5)
  - gotm-playbook/06-antipatterns/README.md (Ch 6.3)
voice_calibrated_against: gotm-playbook/discovered/foundation-inventory.md §5.2
---

# The audit family

## 1. Audit is a family, not a single mode

`docs/04-modes.md` named eight operational modes, and the `audit` mode entry there covered one shape — the canonical ledger-shape audit. That single shape is sufficient for the ledger itself. Real projects routinely demand more. A deliverable that carries claims pulled from sources needs a verification surface for those claims. A visual deliverable needs a rendering check. A software build needs a toolchain check. Each demand produces a different audit kind, and each kind is a Milestone in its own right per `docs/03-discipline-rules.md` R2. Each produces its own Output report file, uses the same severity-tier structure, and triggers fix-Ms split by tier. The audit mode does not get bigger to absorb the new kinds; the audit family grows alongside it, with each kind running on the same skeleton. This chapter names the eight kinds, the universal tier structure they share, the cadence that governs how findings turn into fixes, and the agent-role split that lets verification run cleanly without collapsing into execution.

## 2. Eight common audit kinds

The list below is not exhaustive. A project can invent its own audit kind when its deliverable demands a verification surface no existing kind covers. These are the kinds that recur often enough to name. Each one runs as its own Milestone with a declared Output file.

- **Ledger-shape audit (canonical).** Checks atomicity, status drift, foundation-gate consistency, decision orphans, and unledgered discovery. The cheapest of the eight to run, and the one that runs continuously alongside execution. Output usually lands inline in chat for small projects, or at `drafts/audit-ledger.md` once the ledger crosses the size where a structured report is easier to scan than a chat block.

- **Content / claim audit.** Verifies that every factual claim in the final deliverable traces to a truth-file or source citation. This is the most common kind in evidence-heavy synthesis projects where the deliverable carries hundreds of claims pulled from research artifacts. Each finding cites the claim location and the source it failed to match. Output at `synthesized/audit-log.md`.

- **Foundation-files audit.** Verifies that the ledger's own metadata — claimed file paths, claimed file sizes, claimed key tokens inside files — matches what is actually on disk. Catches the ledger drifting from reality on its own claims, which is a different failure from the ledger drifting from the work itself. Output at `drafts/audit-foundation-files.md`.

- **Code-artifact audit.** For software-build archetype projects. Verifies that claimed exports, imports, and line counts match the actual files, and that the build runs clean. Catches stale ledger metadata in software work, where a refactor moved a symbol but the ledger row that names it was never updated. Output at `drafts/audit-code-artifacts.md`.

- **UI / render audit.** For visual deliverables — decks, web apps, dashboards. Verifies that every route renders, no console errors fire, accessibility minimums are met, viewports work across the supported breakpoints, and themes render cleanly. A pass typically produces a per-route grid of pass, fail, and warning findings. Output at `drafts/audit-ui-qa.md`.

- **Source-fidelity audit.** For projects that certify content from external references. Verifies that lifted content matches the certified source verbatim or with a documented diff. Catches paraphrase drift on content that was supposed to be lifted directly. Output at `drafts/audit-source-fidelity.md`.

- **Density audit.** Per-section coverage scoring against a quality target. Scores each deliverable section's coverage against a defined floor and surfaces lift opportunities for any section that scores below the floor. Useful when coverage matters across sections rather than overall. Output at `drafts/audit-density.md`.

- **Completion-verification audit.** For each `done` Milestone, asks whether the Output file actually meets the Milestone's stated criteria — title match, declared structure present, declared gap-closure delivered, severity-tier mapping for any fix-Ms, word-count band hit. Deeper than the canonical phantom-completion check, which only confirms the Output file exists. Catches the box-checked-but-undone pattern that accumulates when a project moves fast. Output at `drafts/audit-completion.md`.

## 3. Severity tiers are universal

Every audit, regardless of kind, organizes its findings into the same four severity tiers. The structure is what makes audits cross-comparable. A reader who has read one audit report can read any other without re-learning the format.

- **HIGH** — blocks delivery; must fix before the next foundation-gate flip or release.
- **MEDIUM** — polish before delivery; non-blocking on the gate, blocking on the release.
- **LOW** — nits; parked for batching or quiet cleanup.
- **UNVERIFIED** — no source in the Inputs contradicts the claim, but no source confirms it either; flagged for human verification.

When you read a HIGH + MED + LOW + UNVERIFIED count line at the top of a report, you immediately know what is blocking, what is polish, and what is unresolved — without re-orienting to the specific audit kind. The tiering is the audit family's shared interface, and the rest of the discipline keys off it.

## 4. The audit-M → fix-Ms cadence

An audit is always a Milestone per R2 — one execution pass, one Output file. The Output IS the audit report. Fixes do NOT happen inside the audit Milestone. They land as separate fix-Ms, typically split by severity tier. The canonical three-M shape:

    Mxx         — audit pass; output: audit-report.md (HIGH + MED + LOW + UNVERIFIED)
    Mxx-fix     — apply HIGH fixes; output: surgical edits; verification (e.g., build pass)
    Mxx-fix-med — apply MED fixes (non-blocking; can defer or batch)

The split is structural, not stylistic. The audit pass is one atomic act of reading-and-reporting — the Output is the report. Each fix-M is one atomic act of editing — the Output is the set of surgical edits, optionally with a verification artifact such as a build log, a re-rendered route, or a re-run grep. R2 holds throughout. Collapsing the audit and its fixes into a single Milestone breaks R2 in two ways at once: the Milestone now has two Outputs (the report AND the fixes), and the editing pass loses its own report to anchor it. LOW-tier findings often skip a dedicated fix-M and roll into the next maintenance pass. UNVERIFIED items route to `OPEN_QUESTIONS.md` for human resolution.

## 5. The audit re-run cycle (-v2)

Major fixes change the surface the audit ran against. After substantial HIGH-tier fixes — especially fixes that ripple through multiple files — the original audit no longer reflects the deliverable's current state. The discipline is to run the audit again as a separate Milestone named `Mxx-v2`.

A generic worked example. A team's UI QA audit `M11e` flagged one CRITICAL finding — presentation-mode manifests rendered empty across every route. A cluster of fix-Ms rebuilt the story foundation and re-authored the manifests against the rebuilt foundation. `M11e-v2` was appended as a re-audit Milestone with the same Inputs and a new Output. The re-audit confirmed the CRITICAL resolved and produced a PASS verdict.

Both audit Milestones stay in the ledger for provenance. Sunset is not needed — both reports were valid in their moments, and the project's audit trail preserves the before-and-after pair. The `-v2` naming respects R9 in `docs/03-discipline-rules.md`: IDs never recycle, and `-v2` is a new ID, not a reuse of the original.

## 6. Execution-agent vs audit-agent

Run-mode dispatches two distinct subagent roles using two distinct prompt templates. The roles differ in what they produce and what authority they hold over the ledger. The table below names the six dimensions where the split matters.

| Capability | Execution-agent | Audit-agent |
|---|---|---|
| Prompt template | `prompts/subagent-execution.md` | `prompts/subagent-audit.md` |
| Output produced | One named Output file per Milestone | One audit report with HIGH/MED/LOW/UNVERIFIED tiers |
| Can edit GOTM.md? | No (parent updates the ledger) | No for content; YES it may append fix-Ms autonomously |
| Can call other modes? | No | Yes — calls `append` for fix-Ms; routes Goal findings to OPEN_QUESTIONS per the ratification ladder |
| Reads | Only declared Inputs (R3) | The audited M's Output + the M's stated criteria + relevant truth files |
| Returns | Output path + 1-line summary + gaps surfaced | Audit report path + counts per severity tier + appended-M IDs + Goal-level questions surfaced |

The split matters because execution and verification have different shapes. An execution-agent produces. Its single job is to read the declared Inputs and write the declared Output. It does not touch the ledger because the parent does that; it does not chase discoveries because the parent absorbs them. Bandwidth goes to producing one Output without distraction.

An audit-agent observes, reports, and amends the ledger within its authority. It needs that authority precisely because the audit family surfaces fix-Ms as a normal output. Forcing the parent to round-trip every fix-M back through `append` would slow the loop without adding correctness. The audit-agent appends fix-Ms autonomously, routes Goal-level findings to `OPEN_QUESTIONS.md`, and applies the discretion heuristic for Objective-level findings. It still cannot edit the content of an audited Milestone. The fix-Ms it appends will do that work in a later iteration. Verification needs append authority that execution does not; execution needs production bandwidth that verification does not. The two templates encode these different authorities so the orchestrator does not need to recompute them at every dispatch.

## 7. When to run each kind

Each kind has a trigger condition. Run the kind when the trigger lands. The canonical ledger-shape audit runs continuously alongside execution; the other kinds run at threshold events.

- **Content / claim audit** — before any delivery where the deliverable claims facts from sources. Evidence-heavy synthesis projects always need this audit at least once before release.
- **Foundation-files audit** — when the project has spanned multiple weeks and the ledger is large enough (more than around twenty Milestones) that drift risk between the ledger's claims and disk reality is real.
- **Code-artifact audit** — on every release boundary for software-build archetype projects. The build check alone is worth the pass.
- **UI / render audit** — before release for every project with a visual deliverable, AND after any major UI-affecting fix cluster. The `-v2` re-run discipline applies most often here.
- **Source-fidelity audit** — after every lift-M cluster completes, for projects that certify external content.
- **Density audit** — when coverage matters across sections — a curriculum, a deck where every section needs to clear a quality floor.
- **Completion-verification audit** — before a foundation-gate flip on a Target with many `done` draft-tier Milestones; before a release; after a long pause when human review has not caught up to the agent's pace.

The discipline of these audits is to run them at threshold events. The discipline of the canonical ledger-shape audit is to run it continuously, lightweight, as part of the orchestration loop.

## 8. Audit-fix integration with the foundation gate

The audit-M → fix-Ms cadence integrates cleanly with the foundation gate named in `docs/04-modes.md` under the `audit` mode and the `status` mode. A HIGH-tier audit finding becomes a HIGH-priority gap in `STATUS.md`. The gate does NOT close while a HIGH-tier audit fix is open. MED-tier findings become MED-priority gaps — they block published-deliverable release, not the foundation-gate flip. LOW-tier findings go to the parking lot. UNVERIFIED items become open questions (`Q#` entries) routed to the human for confirmation. The audit's severity tiers map one-to-one onto the gap-ledger's priority tiers — same vocabulary, different surface. The integration is what makes the audit-fix cadence work without a separate bookkeeping layer.

## 9. The Rule → Audit → Symptom mapping

Each R-rule's enforcement signal in `docs/03-discipline-rules.md` corresponds to an audit check. When the audit catches a violation, it surfaces as a symptom in the ledger. The mapping admits three reading directions, and each direction resolves to the same row.

- **By rule.** "You want to audit R3" — read R3's enforcement signal in `docs/03-discipline-rules.md` and apply the audit check it names.
- **By symptom.** "You see a Status: done row whose Output file is absent on disk" — that is R5's symptom, the phantom-completion shape.
- **By audit check.** "The audit scanned your Outputs for TODO markers" — that is the R11 check, the unledgered-discovery scan.

The full mapping table — eleven rules indexed against their audit checks and ledger symptoms — lives in the playbook's anti-patterns module. The public docs keep the mapping brief because the recovery paths live in the discipline-rules chapter, not here.

## Common pitfall

> **Common pitfall.** Running an audit, reading the report, and treating the findings as advisory. The discipline of the audit is binding only if the report is binding. An audit whose findings get filtered destroys the enforcement signal — the next audit will be ignored before it even runs. Fix: run audits where the team commits to honoring the findings. Otherwise, do not run them.
