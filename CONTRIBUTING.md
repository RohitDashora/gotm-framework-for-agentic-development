# Contributing

## Welcome

This repo holds the GOTM framework — concept chapters, platform-neutral prompts, and scaffold templates for running multi-pass agentic work without losing the thread. Contributions of all sizes are welcome: typo fixes, voice-tightening on the concept chapters, additional worked examples, new audit kinds, or translation of prompts into other languages. See the `README.md` for the framework overview and the fit-test before contributing.

## How GOTM itself is organized

This project is itself GOTM-orchestrated. The ledger is `GOTM.md`, the derived status view is `STATUS.md`, ratified decisions live in `decisions.md`, and unresolved blocking questions in `OPEN_QUESTIONS.md`. New work follows the same discipline: atomic Milestones (R2 — one pass, one output file), a single ledger (R1), and paired updates (R5 — ledger edits ship in the same turn as the file edits, not later). See `docs/03-discipline-rules.md` for the full eleven-rule set and the ratification ladder.

## What we welcome

- Bug fixes — typos, broken links, fence-rendering issues, hierarchy ID mismatches across docs
- Voice-tightening on the concept chapters in `docs/` — keep the practitioner-friendly, no-hype tone
- Additional worked examples — anonymized, with no real customer, employer, or vendor names
- New audit kinds — extend the family of eight with rationale tying the kind to a recurring failure shape
- Translation of prompts in `prompts/` into other languages, preserving the mode contracts
- New project archetypes — extend the family of four with a clear fit-test and worked example

## What is out of scope

- Platform-specific bindings — runtime skill files, command shims, or raw-API wrappers belong in the deferred Phase 2 work tracked under `meta/`
- Marketing material, slide decks, or talks built on GOTM
- Branded assets, logos, or visual identity
- Tooling for automated GOTM-discipline enforcement — the discipline is paste-able prompts, not a runtime
- Vendor-coupled examples that name a specific model provider, cloud, or commercial tool

## How to contribute

- Open an issue first for anything larger than a typo or single-paragraph edit. Describe the gap and how it ties to the discipline rules.
- For substantial changes, sketch a Milestone in your issue using the M-row template from `templates/GOTM.md.template`.
- Pull requests are small and focused — one concern per PR, referencing the issue. Multi-concern PRs are returned for splitting.
- Run the relevant audit prompts from `prompts/audit-*.md` against your change as part of self-review. Include the verdict in the PR description.
- All contributions are licensed under Apache 2.0 per `LICENSE`.

## Apache 2.0 explicit patent grant

By contributing, you agree your contribution is licensed under the Apache License, Version 2.0. Apache 2.0 includes an explicit patent grant: contributors grant a perpetual, worldwide, royalty-free patent license for any patents they hold that are necessarily infringed by their contribution, terminated only on patent counter-litigation. See `LICENSE` Section 3 for the full grant text and Section 5 for the inbound-contribution terms. No separate Contributor License Agreement is required — Apache 2.0 governs the inbound license by default.
