# CLAUDE.md

This project follows the GOTM v3 operating protocol. Its orchestration file-set lives in [`.gotm/`](.gotm/), kept out of the root so the root stays reserved for the framework's produced assets (`docs/`, `prompts/`, `templates/`).

Before doing any work in this repo:

1. Read [`.gotm/PROTOCOL.md`](.gotm/PROTOCOL.md).
2. Read [`.gotm/LEDGER.md`](.gotm/LEDGER.md) — read the **frontier**, not the history.
3. Read [`.gotm/QUESTIONS.md`](.gotm/QUESTIONS.md) for any open ratifications.

`.gotm/PROTOCOL.md` is canonical. This file lives at the repo root only because a root `CLAUDE.md` is what auto-loads across sessions — it is the thin bridge that points into `.gotm/`. Do not move it into `.gotm/`; that silently breaks the auto-load. (This repo uses the subfolder layout as a worked example of it; see [`docs/08-in-practice.md`](docs/08-in-practice.md).)

## Non-negotiables (v3)

These are the load-bearing rules of v3. Guard them every turn (full detail in `.gotm/PROTOCOL.md`):

- **Driver / worker / store.** You are the **driver**: you plan, you talk to the human, you run the scheduler loop — and you are the **single writer** of the store. You never edit a work artifact and never read bulk input directly; **all work, however small, is a worker dispatch** (a fresh, ephemeral context with bounded inputs that produces one output). See `.gotm/PROTOCOL.md` → *Architecture* / *The loop*.
- **Workers mark authored-done; they never self-certify.** A worker's strongest claim is *the artifact exists* (**authored-done**). It cannot grade its own work — by the time anything checks a unit, its author is gone. The driver therefore **always dispatches a separate audit worker** (auditor ≠ author) with bounded context. Downstream waits for a passing verdict — `PASS` or `PASS-FINDINGS`; a `FAIL` blocks and its findings become new units. Deploy/infra/data units get a **verified-done** check that exercises the live artifact. See `.gotm/PROTOCOL.md` → *Audit*.
- **Born-tiered ledger; re-hydrate from the store.** The ledger is born tiered (hot frontier + cold archive) — read the frontier, never the history. Hold no decision-relevant state only in chat; the on-disk store alone must reconstruct context. On **any** fresh start (cold restart, `/clear`, or after a compaction) re-hydrate via the **session-start reconcile** — reconcile the ledger against disk before acting. **There is NO compaction hook**; re-hydration depends on none. See `.gotm/PROTOCOL.md` → *Resilience & re-hydration*.
- **Freeze + follow-on ownership.** Done units are frozen: never edit a `done` unit's output — append a follow-on unit (an active unit may own a change to a done output) and put the change there. Same for prior `DECISIONS.md` / `QUESTIONS.md` entries — append, don't rewrite (marking a Status line answered/superseded is the one allowed exception). Living governance docs (`PROTOCOL.md`, `CLAUDE.md`, `README.md`) stay editable. Because the driver is the single writer, the duplicate-row race cannot occur. See `.gotm/PROTOCOL.md` → *Freeze*.
