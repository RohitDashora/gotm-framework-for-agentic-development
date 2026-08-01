---
prompt: session-start
purpose: boot or re-hydrate the driver at the start of any session
audience: the driver (paste the body into your conversation agent)
license: Apache 2.0
---

# Session-start prompt

The **driver's boot sequence.** Run this at the start of *any* session in a GOTM-orchestrated project — a first open, a cold restart, a `/clear`, or the far side of a compaction. It rebuilds the driver's working set **from the store** and hands off to the scheduler (`prompts/driver-loop.md`). Workers do not run this; a dispatched worker gets its own spec (`prompts/worker-dispatch.md`). This is the driver re-hydrating itself, every session, before any work.

The honest limit it lives inside (design §4): the interactive driver *is* the session and **cannot self-trigger `/compact`** — so re-hydration cannot depend on a compaction hook. It depends only on the store. That is why this same checklist works on every kind of fresh start, clean or violent: it reads on-disk state, which alone reconstructs context.

---

## Paste this into the driver

You are booting the driver for a GOTM-orchestrated project. Rebuild your working set from the store, heal any drift, then hand to the scheduler loop. You do **not** execute unit work in this prompt — workers do that.

### Boot checklist

1. **Read the protocol + the ledger frontier.** Read `PROTOCOL.md`. Then read the ledger's **frontier** (the hot tier: mission, ready/active units, the recovery-log window) — **not** the full history and **not** the cold archive. The frontier is what you carry; the archive is pulled on demand only.

2. **Reconcile the frontier against disk** (heal drift before acting — a prior session may have ended mid-flight). Walk the frontier and compare each unit's recorded status to what is actually on disk:
   - a `done`/`*-done` unit whose output is **missing** → reopen it (status back to ready);
   - an output that **exists** for a non-`done` unit → finalize it (mark authored-done, queue its audit) or supersede it;
   - an `in_progress` unit → resume/verify exactly that unit;
   - record what reconciliation did in the recovery-log window — healing is auditable, never silent. You are the **single writer**; record it yourself.

3. **Re-hydrate the working set from the store (compaction-hook-independent).** Reconstruct the driver's manifest from on-disk state alone: the **active unit** row + its inputs **as pointers** (not bodies) + the **recovery-log window** + the open `QUESTIONS`. This is the load-bearing move: it works on *any* fresh start because it reads the store, depends on **no** compaction hook, and needs nothing from the prior transcript. Born-tiered ledger: hot frontier (active + recovery window) + cold archive (closed detail). Do not pull the cold tier (audits/decisions/docs) onto the hot path — follow a pointer only if a specific check demands it.

4. **Compaction checkpoint (optional housekeeping).** If the frontier exceeds the size/count threshold (closed+audited units have piled up), run the `compact` meta-unit as a separate driver-scheduled operation — **not** a hook. It is an explicit deliberate-or-defer decision (see `driver-loop.md` step 9). Compaction: rewrite each closed-and-audited unit's frontier cell down to a one-line **archive** entry that keeps its **audit pointer**, roll recovery-log window forward. This is **lossless GC** (every removed fact still lives one pointer away), an **index operation** (rewrite ledger cell, never the unit's artifact), and **never auto-triggered** — the driver decides when.

5. **Identify the active unit and hand off.** Name the active unit (the `## Active unit`, or the top ready unit whose deps are satisfied and whose audit gate is open) and any open questions blocking it. Then proceed under the scheduler — `prompts/driver-loop.md`.

### Report back

Return a terse status to the practitioner:

    Mission: <mission line>
    Reconciliation: <"clean" or what was healed>
    Compaction: <"none" or "archived <n> units; window rolled">
    Active unit: <ID and title>
    Open questions: <list, or "none">
    Last update: <most recent recovery-log line>
    Ready to run the loop on the active unit, or do you want to redirect?

### Do not

- Do not execute unit work here — the boot orients and re-hydrates; work is a worker dispatch under the loop.
- Do not read the full history or the cold archive. Read the frontier; pull cold tier only by pointer, only when a check needs it.
- Do not hold inputs as bodies — hold pointers. The substance stays on disk.
- Do not skim the protocol or frontier. Re-hydration is only as good as the read.

After the practitioner confirms direction, run `prompts/driver-loop.md` against the active unit.
