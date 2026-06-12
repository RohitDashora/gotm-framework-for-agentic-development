# CLAUDE.md

This project follows the GOTM operating protocol. Its orchestration file-set lives in [`.gotm/`](.gotm/), kept out of the root so the root stays reserved for the framework's deliverables (`docs/`, `prompts/`, `templates/`).

Before doing any work in this repo:

1. Read [`.gotm/PROTOCOL.md`](.gotm/PROTOCOL.md).
2. Read [`.gotm/LEDGER.md`](.gotm/LEDGER.md).
3. Read [`.gotm/QUESTIONS.md`](.gotm/QUESTIONS.md) for any open ratifications.

`.gotm/PROTOCOL.md` is canonical. This file lives at the repo root only because a root `CLAUDE.md` is what auto-loads across sessions — it is the thin bridge that points into `.gotm/`. Do not move it into `.gotm/`; that silently breaks the auto-load. (This repo uses the subfolder layout as a worked example of it; see `docs/05-in-practice.md`.)
