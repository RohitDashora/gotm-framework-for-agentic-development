# Contributing

## Welcome

This repo holds the GOTM framework — concept chapters, platform-neutral prompts, and scaffold templates for surviving bounded-context agentic execution. Contributions of all sizes are welcome: typo fixes, voice-tightening on the concept chapters, additional worked examples, new audit kinds, or translation of prompts into other languages. See `README.md` for the framework overview and the fit-test before contributing.

## How GOTM itself is organized

This project is itself GOTM-orchestrated. The operating protocol is `PROTOCOL.md`. The ledger is `LEDGER.md`. Ratified decisions live in `DECISIONS.md`. Unresolved questions blocking work live in `QUESTIONS.md`. New work follows the same five rules:

1. Single ledger — `LEDGER.md` is authoritative.
2. Atomic units — one execution pass produces one named output file.
3. Foundation before drafts — foundation work precedes drafting.
4. Audit before downstream consumes — claimed-done units are checked.
5. Ratification ladder — the human owns mission-level decisions; the agent owns execution-level ones.

See `docs/` for the full framework and `PROTOCOL.md` for the operating contract.

## What we welcome

- Bug fixes — typos, broken links, render issues
- Voice-tightening on the concept chapters in `docs/` — keep the practitioner-friendly, no-hype tone
- Additional worked examples — anonymized, with no real customer, employer, or vendor names
- New audit kinds — `prompts/audit.md` lists common kinds; extensions are welcome with a worked example showing the kind in action
- Translation of `prompts/` into other languages, preserving structure and discipline
- Improvements to the templates in `templates/` that make adoption easier

## What is out of scope

- Platform-specific bindings — runtime skill files, command shims, or raw-API wrappers belong elsewhere
- Marketing material, slide decks, talks
- Branded assets or visual identity
- Tooling for automated GOTM-discipline enforcement — the discipline is paste-able prompts, not a runtime
- Vendor-coupled examples that name a specific model provider, cloud, or commercial tool

## How to contribute

- Open an issue first for anything larger than a typo or single-paragraph edit. Describe the gap and how it ties to the five rules.
- For substantial changes, sketch a unit in your issue using the row shape from `templates/LEDGER.md.template` (ID, title, inputs, output, status).
- Pull requests are small and focused — one concern per PR, referencing the issue. Multi-concern PRs are returned for splitting.
- Run `prompts/audit.md` against your change as part of self-review. Include the verdict in the PR description.
- All contributions are licensed under Apache 2.0 per `LICENSE`.

## Apache 2.0 explicit patent grant

By contributing, you agree your contribution is licensed under the Apache License, Version 2.0. Apache 2.0 includes an explicit patent grant: contributors grant a perpetual, worldwide, royalty-free patent license for any patents they hold that are necessarily infringed by their contribution, terminated only on patent counter-litigation. See `LICENSE` Section 3 for the full grant text and Section 5 for the inbound-contribution terms. No separate Contributor License Agreement is required — Apache 2.0 governs the inbound license by default.
