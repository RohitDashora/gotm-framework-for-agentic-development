---
title: In practice
last_updated: 2026-06-11
---

# In practice

The first four chapters are the framework: what GOTM is, why agent work needs it, how the project carries it, and how it stays honest under real conditions. This chapter is how you actually run it — where the files live, what one session looks like end to end, and a worked example of a software project from first unit to first line of code. It stays tool-neutral; the mechanics described here work whatever agent or editor you drive them with.

## Where the file-set lives

The orchestration file-set — protocol, ledger, decisions, open questions, audit outputs — has to live somewhere in the project tree. There are two sensible layouts, and which one fits depends on the shape of the work.

**Root layout.** The files sit at the project root. This is fine for a writing or research project that produces few files of its own: the orchestration files and the deliverable coexist without crowding each other.

**Subfolder layout.** The files sit in a dedicated folder — `.gotm/` is a natural name — so the project root stays reserved for produced assets. This is the better fit for a software or multi-asset project, where mixing the machinery with the code and docs clutters the root and risks collisions.

There is one dependency to respect when you choose the subfolder layout. Many agent tools auto-load a context file from the *project root* at session start — the file that tells the agent to read the protocol first. That auto-load is what makes the discipline carry across sessions, and it only happens at the root. If you move the whole file-set into a subfolder, that continuity *silently* stops — no error, just quiet erosion. So if you use a subfolder, keep a thin pointer file at the root: a few lines that name the protocol's real location inside the subfolder. It is a small thing and it is easy to forget, which is exactly why it is worth stating.

Pick by project shape: writing and research, root is fine; software and multi-asset, use the subfolder and keep the root pointer.

## One session, end to end

A session is the unit of work in time, and it has the same shape every time, whether it is the third session or the three-hundredth:

1. **Read** the protocol, the ledger, and the open questions. Not a skim — the point is to align with the project's actual state, including state an earlier session left.
2. **Reconcile** the ledger against disk. If a previous session ended badly, heal the disagreement now — a done row with no file, an orphaned file from an interrupted unit — before doing anything new.
3. **Pick** the active unit: the top row that is not yet done and whose inputs are ready.
4. **Act** — do exactly that unit, producing its one named output. Mark it in-progress before you start, so a crash mid-way is recoverable.
5. **Write back, in the same turn** — update the unit's ledger row, append any decision to the decisions log, log any question that opened or closed. The work and its bookkeeping end the turn together or the unit isn't done.
6. **Audit before downstream consumes.** When the unit's output is about to feed another unit, have it checked by an independent context, and let the gate hold until it passes.

That is the whole loop. Chapters 3 and 4 are the why behind each step; this is the sequence you run.

## A worked example: a software project

Foundation-before-drafts has a specific shape for software: **design before code**. The natural foundation units are a high-level design, then a low-level design per component; the natural draft units are the code that implements them. Between the two sits an audit — because code is the most expensive thing to build on a shaky foundation, and the audit gate is what stops you from doing that.

A ledger for such a project starts like this:

| ID | Title | Inputs | Output | Status | Audit |
|---|---|---|---|---|---|
| U1 | High-level design | — | `docs/design/HLD.md` | done | PASS→audits/U4.md |
| U2 | LLD — ingestion component | U1 | `docs/design/LLD-ingestion.md` | done | PASS→audits/U4.md |
| U3 | LLD — serving component | U1 | `docs/design/LLD-serving.md` | done | PASS-FINDINGS→audits/U4.md |
| U4 | Independent audit of the design (U1–U3) | U1, U2, U3 | `audits/U4.md` | done | — |
| U5 | Implement ingestion | U2 | `src/ingestion/` | pending | — |
| U6 | Implement serving | U3 | `src/serving/` | pending | — |

A few things the table makes concrete. Each row produces one named output. The two implementation units name the LLDs they consume as inputs, so the foundation gate is visible in the graph: U5 reads U2, U6 reads U3. The audit unit, U4, is its own row, run by an independent context, and it is what stamped the `Audit` column on the design units — `PASS` on two, `PASS-FINDINGS` on the third, meaning U3 is consumable but carries a tracked non-blocking finding (which becomes its own follow-on unit). The gate now reads cleanly: U5 and U6 may begin, because the inputs they consume have passed. Had U4 returned `FAIL` on a design unit, the implementation unit that consumes it would wait until a fix landed and a re-audit passed.

If, mid-project, someone asks for something off the mission — a one-off export, a note, a piece of meta-feedback about the process — it does not become a unit. Forcing it into the ledger pollutes the unit graph with work that doesn't serve the mission. Instead, produce the file and drop a one-line breadcrumb in the recent-updates log marked *not a mission unit*. You keep the traceability without distorting the scope.

## Automating the bootstrap

Everything above can be done by hand — copying the file-set into a new project, filling in the mission, sketching the first units. It can also be automated: dropping the file-set, wiring the optional enforcement hook, leaving the root pointer in place are mechanical steps a tool can take for you. Adopter tooling exists for this — a Claude Code plugin, for instance — but the automation is a convenience around the discipline, not the discipline itself. The discipline is the paste-able files in this repository, and it works the same whether a tool laid them down or you did.

## The discipline is small

It is worth ending on the scale of the thing. The mission is one sentence. The ledger is one file. The protocol is one read at session start. The safeguards are a handful of checks, the resilience rules a handful more, the audit a checklist and a verdict. None of it is heavy, and that is deliberate — a discipline you have to fight is a discipline you abandon by session ten.

What the smallness buys is large. The same five primitives that carry a one-week deliverable carry a multi-author research project and a system that spans hundreds of agent sessions. Drift is not avoided by being careful, because carefulness is a property of a context that closes at the session boundary. Drift is caught by being checked — by the ledger, by the gate, by an auditor who isn't the author. That is the whole bet of GOTM, and it is one that real use has now had the chance to test.

→ Start here: the [repository README](../README.md) walks through bootstrapping your first GOTM project.
