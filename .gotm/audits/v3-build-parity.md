# Audit — GOTM v3 plugin port parity vs framework source

**Auditor:** independent (did not build either repo). **Date:** 2026-06-29.
**Scope:** does the plugin (`/Users/rohit.dashora/fe-vibe/gotm`) faithfully port the framework v3 source
(`/Users/rohit.dashora/fe-vibe/gotm-framework-for-agentic-development`), and are its `.gotm/` runtime paths correct + complete?
**Method:** file-tree enumeration; line-level `diff` of every shared file; grep sweeps for bad paths, phantom file refs, `subagent-dispatch`, `$CLAUDE_PLUGIN_ROOT`, v2 strings; bootstrap drop-list ↔ shipped-templates reconciliation; manifest/marketplace version check.

---

## Verdict

**PASS-FINDINGS.** The port is faithful. All six prompts and all shared templates carry the same v3 discipline as the framework, differing only by correct `.gotm/`-path adjustments and reference rewrites (docs→inline, `/gotm:` command pointers). No content drift, no contradiction, no missing section, no broken `$CLAUDE_PLUGIN_ROOT` source ref, no leftover `subagent-dispatch.md` reference, no v2/2.6.0 string outside the deliberate "supersedes" notes. Version 3.0.0 is consistent across plugin.json, the marketplace copy, and marketplace.json. The single substantive defect is a **bootstrap drop-list omission** (LEARNINGS.md.template) — MEDIUM, non-blocking, with a working fallback. Everything else is LOW/cosmetic.

---

## HIGH findings

None.

---

## MEDIUM findings

### M1 — `LEARNINGS.md.template` is shipped but absent from the bootstrap drop-list
`templates/LEARNINGS.md.template` exists and ships (`gotm/templates/LEARNINGS.md.template`), and the plugin README enumerates it as part of the file-set (`gotm/README.md:38`). But `commands/bootstrap.md` Step 1 (`bootstrap.md:21-43`) — the authoritative "drop the file-set into `.gotm/`" list — never drops it. It enumerates PROTOCOL/LEDGER/DECISIONS/QUESTIONS, the 6 prompts, the hook pair, `scripts/compact_ledger.py`, `CONSULTED.md.template` ("if present"), and the root `CLAUDE.md`/`README.md` — 16 of the 17 shipped templates. LEARNINGS is mentioned only as a *future* `/gotm:learn` output (`bootstrap.md:9`), never as a `.gotm/` drop.
- **Why it is only MEDIUM (not HIGH):** `/gotm:learn` reads the scaffold from the plugin root, not from `.gotm/`: "the scaffold is `$CLAUDE_PLUGIN_ROOT/templates/LEARNINGS.md.template`" (`commands/learn.md:14`). So the loop still closes even though the template was never dropped into the project. The omission is an inconsistency between README ("the plugin carries a self-contained copy of the v3 file-set") and bootstrap (which drops everything *except* LEARNINGS), not a runtime break. Contrast: `CONSULTED.md.template` *is* in the drop list ("if present", `bootstrap.md:38`) while its sibling LEARNINGS is not — asymmetric handling of the two halves of the learning loop.

### M2 — bootstrap claims the loop's checkpoint step "points at" `compact_ledger.py`; it does not
`bootstrap.md:36` describes `scripts/compact_ledger.py` as "the script the `hooks/README.md` **and the loop's checkpoint step point at**." Verified: only `hooks/README.md` points at the script (`templates/hooks/README.md:108-111`). Neither `templates/prompts/driver-loop.md` step 6, nor `templates/prompts/session-start.md`, nor `templates/PROTOCOL.md.template` references `compact_ledger.py` or `scripts/` at all (grep returns nothing in PROTOCOL; the prompts describe compaction conceptually but name no script). So the dropped script is reachable only via the hook README — a correct but narrower wiring than bootstrap advertises. Not a broken path; an over-claim in the bootstrap prose.

---

## LOW findings

### L1 — PROTOCOL.md.template never references the `.gotm/scripts/` it ships into
The plugin drops `scripts/compact_ledger.py → .gotm/scripts/` (`bootstrap.md:36`), but `templates/PROTOCOL.md.template` — the operating contract the driver reads every session — lists `.gotm/prompts/` (links table, lines 131-135), `.gotm/hooks/` (line 108), and `audits/` (line 86) but never `.gotm/scripts/`. The compaction step in PROTOCOL "Resilience" (line 119) is prose-only with no script pointer. Consequence: a driver re-hydrating from PROTOCOL alone would not learn the compaction script exists. Pairs with M2.

### L2 — Cosmetic: `LEDGER-ARCHIVE` vs `LEDGER-ARCHIVE.md`
The plugin's `LEDGER.md.template` correctly tightened the framework's generic `LEDGER-ARCHIVE` to `LEDGER-ARCHIVE.md` under `.gotm/` (diff lines 61-75) and the script writes a sibling `LEDGER-ARCHIVE.md` (`compact_ledger.py:8,229`). Consistent; noted only to confirm it was checked.

---

## What was checked and found CLEAN

- **Faithful-port check (the 6 prompts).** `diff` of `prompts/{audit,consult,driver-loop,outcome-analysis,session-start,worker-dispatch}.md` (framework) vs `templates/prompts/*` (plugin): every delta is a `.gotm/`-path adjustment or a reference rewrite (framework `docs/0x` citations replaced with inline phrasing or framework-repo pointers; `/gotm:*` command refs added). Zero discipline/content drift. The 7-point audit checklist, the three-way verdict, authored-done vs verified-done, fan-in-is-a-worker, worker minimalism, the candidate→validated confidence ladder — all preserved verbatim in substance.
- **Faithful-port check (templates).** PROTOCOL/LEDGER/DECISIONS/README/LEARNINGS/CONSULTED `.template` diffs are all `.gotm/`-path + reference adjustments. QUESTIONS.md.template is byte-identical. The framework's "Runtime layout is a platform binding" note (PROTOCOL line 7) was correctly *bound* in the plugin into a concrete `.gotm/` Layout note + a new `## CLAUDE.md auto-load` section — an intentional platform binding, not drift. The framework's "PLATFORM BINDING" trailer in LEDGER.md.template was correctly removed (now bound).
- **`.gotm/` path correctness.** Grep for bare sibling `prompts/`, `audits/`, `audits/` without the `.gotm/` prefix across `commands/` and `templates/prompts/`: none found outside intended internal-relative links. The hook (`gotm-immutability.py:109-110,129-134`) and `compact_ledger.py:21,35,66` all use correct `.gotm/` paths; the hook derives root from its own location (`<root>/.gotm/hooks/`). settings.json wiring uses `$CLAUDE_PROJECT_DIR/.gotm/hooks/gotm-immutability.py` (`hooks/README.md:52`) — correct for a dropped runtime hook.
- **`$CLAUDE_PLUGIN_ROOT` source refs all resolve.** audit/consult/learn/loop each cite `$CLAUDE_PLUGIN_ROOT/templates/prompts/<x>.md` (and learn additionally `…/templates/LEARNINGS.md.template`); every cited file exists in `templates/`.
- **No `subagent-dispatch.md` leftover.** All three hits (`README.md:41`, `worker-dispatch.md:11`, `bootstrap.md:34`) are deliberate "supersedes the v2 `subagent-dispatch.md`" historical notes — correct, not dangling references to a dropped file.
- **Bootstrap write-targets exist.** Bootstrap writes mission to PROTOCOL's `<one-sentence mission>` placeholder (present, PROTOCOL.md.template:141) and to LEDGER `## Mission` + sets `## Active unit` (both present, LEDGER.md.template:16,20).
- **Version/manifest consistency.** plugin.json: name `gotm`, version `3.0.0`. Marketplace copy (`plugin-marketplace/experimental/general/gotm`) is content-identical (only `.git`/`.claude`/`.gitignore` vs `REVIEWERS` differ) and also `3.0.0`; marketplace.json entry is `3.0.0`. The only `2.6.0` reference is the intentional `bootstrap.md:11` "supersedes the v2.6.0 bootstrap" + README changelog. No live v2 concepts.
- **6 commands, none named `gotm`.** `commands/` = audit, bootstrap, consult, learn, loop, what — exactly the six, correctly namespaced as `/gotm:<x>`.

---

## Summary

| Severity | Count | Items |
|---|---|---|
| HIGH | 0 | — |
| MEDIUM | 2 | M1 LEARNINGS.md.template not in bootstrap drop-list; M2 bootstrap over-claims the loop "points at" compact_ledger.py |
| LOW | 2 | L1 PROTOCOL never references `.gotm/scripts/`; L2 archive-name cosmetic (clean) |

The v3 build is a faithful, internally consistent port. The only real gap is documentary completeness around the LEARNINGS template / compaction-script wiring in the bootstrap + PROTOCOL prose (M1, M2, L1) — none of which breaks the runtime, because `/gotm:learn` and the hook README carry the working references. Recommended fixes: add `LEARNINGS.md.template → .gotm/` (or "if present", mirroring CONSULTED) to bootstrap Step 1; correct the M2 over-claim; add a `.gotm/scripts/` pointer to PROTOCOL.md.template's Resilience/compaction section.
