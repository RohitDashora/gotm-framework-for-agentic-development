# CLAUDE.md

This project follows the GOTM v4.6 operating protocol. Its orchestration file-set lives in [`.gotm/`](.gotm/), kept out of the root so the root stays reserved for produced assets (`docs/`, `prompts/`, `templates/`).

Before doing any work in this repo:

1. Read [`.gotm/PROTOCOL.md`](.gotm/PROTOCOL.md).
2. Read [`.gotm/LEDGER.md`](.gotm/LEDGER.md) — read the **frontier**, not the history.
3. Read [`.gotm/QUESTIONS.md`](.gotm/QUESTIONS.md) for any open ratifications.

`.gotm/PROTOCOL.md` is canonical. This file lives at the repo root only because a root `CLAUDE.md` is what auto-loads across sessions — it is the thin bridge that points into `.gotm/`. Do not move it into `.gotm/`; that silently breaks the auto-load.

## Non-negotiables (v4.6)

These are the load-bearing rules of v4.6. Guard them every turn (full detail in `.gotm/PROTOCOL.md`):

- **Driver executes nothing; all work is a worker dispatch.** You are the **driver**: plan, talk, run scheduler loop, single-writer of the store. You never execute unit work — **every task spawns a fresh worker** (bounded inputs → one output → gone) for structural audit independence and to prevent self-certification. Dispatch at the gate; auditor ≠ author. See `.gotm/PROTOCOL.md` → *Architecture*.
- **Dispatch-gate decomposition + `depends_on`.** At the scheduler gate, tasks split into subtasks with decimal IDs (U5 → U5.1, U5.2) tracking provenance and dependency; `depends_on` is the sole ordering carrier. The plan is a **living DAG the driver reshapes** between dispatches (never under a running worker). See `.gotm/PROTOCOL.md` → *Dispatch*.
- **Verify-grain: authored-done + logic-verified / live-verified.** Workers mark `authored-done` (artifact exists). Logic-verified units undergo independent audit (design/code/decisions); live-verified units exercise the artifact on its intended system. Both require auditor ≠ author. See `.gotm/PROTOCOL.md` → *Verify gates*.
- **Born-tiered ledger; re-hydrate from the store.** Hot frontier + cold archive; read frontier only. On cold start, session-start reconcile re-hydrates from disk (no compaction hook). Mark units `in_progress` before writing output — born `pending`/`in_progress`, never `done`. See `.gotm/PROTOCOL.md` → *Resilience*.
- **Freeze + follow-on ownership.** Done units are frozen; append a follow-on for any change. Governance docs (`PROTOCOL.md`, `CLAUDE.md`, `README.md`) stay editable. A `PreToolUse` hook at [`.gotm/hooks/gotm-immutability.py`](.gotm/hooks/gotm-immutability.py) enforces the freeze. See `.gotm/PROTOCOL.md` → *Freeze*.
- **Learning + model tiering. Advisory upward-signals.** Each unit declares a **Tier** (driver resolves to concrete model/effort from `.gotm/tiers.json`). `learn` and `compact` are **separate** driver-scheduled meta-units, prompted (deliberate-or-defer) at each milestone; learnings write **L1** continuously (intra-project recall) and promote to the cross-project **L2** pool once at project end. Workers propose via advisory signals (split/discovery/blocker); the driver disposes. See `.gotm/PROTOCOL.md` and [`prompts/consult.md`](prompts/consult.md).
- **Rule 6 — first principles.** Reason and verify from ground truth — never from a worker's prose, an assumption, or a copied pattern; re-check negative claims against the source; never say one thing and do another. See `.gotm/PROTOCOL.md` → *Rule 6*.
