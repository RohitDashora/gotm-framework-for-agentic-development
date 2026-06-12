# CLAUDE.md

This project follows the GOTM operating protocol. Its orchestration file-set lives in [`.gotm/`](.gotm/), kept out of the root so the root stays reserved for the framework's deliverables (`docs/`, `prompts/`, `templates/`).

Before doing any work in this repo:

1. Read [`.gotm/PROTOCOL.md`](.gotm/PROTOCOL.md).
2. Read [`.gotm/LEDGER.md`](.gotm/LEDGER.md).
3. Read [`.gotm/QUESTIONS.md`](.gotm/QUESTIONS.md) for any open ratifications.

`.gotm/PROTOCOL.md` is canonical. This file lives at the repo root only because a root `CLAUDE.md` is what auto-loads across sessions — it is the thin bridge that points into `.gotm/`. Do not move it into `.gotm/`; that silently breaks the auto-load. (This repo uses the subfolder layout as a worked example of it; see `docs/05-in-practice.md`.)

## Non-negotiables (anti-drift)

These are the ways the discipline erodes. Guard against them, every turn (full detail in `.gotm/PROTOCOL.md` → *Anti-drift safeguards*, *Resilience*, and *Audit gates*):

- **Done units are frozen.** Before any edit/write, check `.gotm/LEDGER.md`: if the target is a `done` unit's output, do **not** edit it — append a follow-on unit and put the change there. Same for prior `DECISIONS.md` / `QUESTIONS.md` entries — append, don't rewrite (marking a Status line answered/superseded is the one allowed exception). Living governance docs (`PROTOCOL.md`, `CLAUDE.md`, `README.md`) stay editable.
- **Write-back gate.** Never end a turn that created or changed a unit's output without updating `.gotm/LEDGER.md` (and `DECISIONS.md` / `QUESTIONS.md` as needed) in the *same* turn. Output without write-back means the unit is not done.
- **Resilience / cold start.** On session start, *reconcile the ledger against disk before acting* — a crash can orphan an output or leave a unit `in_progress`. Never hold decision-relevant state only in chat; the on-disk state alone must reconstruct context. When executing a unit, mark it `in_progress` before producing its output. See `.gotm/PROTOCOL.md` → *Resilience*.
- **Audit independence & gate.** A done unit is checked by a *different* agent than its author — dispatch the audit as a fresh subagent with bounded context (inputs + output + spec only); never bless your own work. Downstream/code units wait for a passing verdict — `PASS` or `PASS-FINDINGS` (the `Audit` column); a `FAIL` blocks. Findings become new units. See `.gotm/PROTOCOL.md` → *Audit gates*.
