# Audit report — v3 build consistency (independent / adversarial) — 2026-06-29

Independent auditor. Did not author any v3 content. Scope: `templates/PROTOCOL.md.template`,
`docs/01..09`, `prompts/{driver-loop,worker-dispatch,audit,session-start,consult,outcome-analysis}.md`,
oracle `V3-DESIGN.md`. Method: cross-read PROTOCOL ↔ chapters ↔ prompts for agreement on the
load-bearing invariants, then applied v3's own lenses (enforcement check, multi-site claim check,
stale-reference check) to v3 itself.

The core machinery is, on the whole, strikingly consistent — the 5 ledger states, the single-writer
rule, the fan-in hard rule, no-compaction-hook re-hydration, worker minimalism, and the freeze all
agree across the three layers. The findings below are the real cracks.

---

## HIGH severity

**H1 — verified-done is produced by *two different mechanisms* across the corpus (a real architectural split, not a wording nit).**
The framework cannot decide whether the runtime `verified-done` check is a *second, separate worker*
the driver dispatches alongside the audit worker, or *part of the audit worker's own job*. Both models
are stated flatly, in the operational prompts an operator would actually follow:

- **Two-worker model** ("the driver *also* dispatches a separate verified-done worker"):
  - `templates/PROTOCOL.md.template:58` (loop step 4) — "Dispatch a separate audit worker per authored-done unit; **runtime units also get a `verified-done` worker.**"
  - `prompts/driver-loop.md:28` (loop step 4) — "...also dispatch a **verified-done** worker that exercises the live artifact..."
  - `docs/04-the-loop.md:17` — "...the driver **also dispatches a verified-done worker** that exercises the live artifact as its real consumer."
- **One-worker model** (the audit worker itself performs the runtime check, one verdict, one report):
  - `prompts/audit.md:70-78` (§4a) — "...**the audit must additionally exercise the live artifact** as its real consumer" (folded into the single audit report + verdict at lines 122-128).
  - `prompts/worker-dispatch.md:112-115` — "...**that audit worker performs** the live `verified-done` check as the real consumer."
  - `docs/06-keeping-it-honest.md:21` — "**The audit worker reads** the bounded inputs, the output, and the spec... for deploy/infra/data units the bar is higher: the **verification worker performs a runtime check**" (treated as the same audit worker raising its bar, with a single verdict in the ch6 mermaid at lines 49-51).
  - `templates/PROTOCOL.md.template:80` — "**verified-done** = **an independent worker** checked it — and... *exercised the live artifact*" (one worker).

PROTOCOL is internally self-contradictory on this: its *loop* section (line 58) says two workers, while
its *Audit gates* section (line 80) describes one. An operator running PROTOCOL's loop or `driver-loop.md`
would dispatch a distinct verified-done worker; an operator running `audit.md` (the prompt the audit
worker actually pastes) would run a single combined audit that ends in one verdict and one
`audits/<Uxx>.md`. `audit.md` has no second-worker handoff and no separate verified-done verdict — so
the two-worker model has no operational prompt behind it. This is exactly the kind of seam v3 preaches
catching, and it lands on the keystone honesty mechanism. **Suggested fix unit:** pick one model
(audit.md's "one audit worker that also runs §4a for runtime units" is the implemented one) and reword
PROTOCOL:58, driver-loop.md:28, docs/04:17 to "the same audit worker additionally exercises the live
artifact" rather than "also dispatch a verified-done worker."

---

## MEDIUM severity

**M1 — ch6 overclaims enforcement that this repo does not ship — the documented-but-unenforced blind spot v3 itself names.**
`docs/06-keeping-it-honest.md:31`: "**The enforcement is real, not honor-system.** ... **The v3 hook
honors follow-on ownership**: a write to a frozen output is rejected *unless* an active follow-on unit
owns that output." Stated in present tense with no caveat. But this is the platform-neutral *framework*
repo, which ships **no hook** — every other artifact says so explicitly:
- `templates/PROTOCOL.md.template:100` — "**Mechanical enforcement lives in tooling, not here.** ...runtime enforcement bindings (the immutability hook...) belong in adopter tooling, e.g. a plugin."
- `templates/PROTOCOL.md.template:96` — hedges with "a **wired** immutability hook honors it."
- `docs/09-learning-across-projects.md:66` — a whole "What ships, and what is a binding" section.
- `README.md:92` — "the templates only *describe*" the hook; "the companion `gotm` plugin... ships... the immutability hook."

ch6 is the lone chapter that asserts the enforcement is live without the binding caveat. By v3's own
audit check #6 (enforcement check), "the freeze is enforced" with nothing in this repo enforcing it is a
finding. **Suggested fix unit:** add the same one-line binding caveat to ch6 §"The freeze" (e.g. "the
*wired* hook honors follow-on ownership — runtime enforcement is an adopter/plugin binding, ch9 / PROTOCOL").

**M2 — PROTOCOL internally contradicts itself on whether the auditor always runs all seven checks.**
`templates/PROTOCOL.md.template:82`: "**the auditor runs all seven**" (unconditional). Six lines later,
`:88`: "a **light** existence+spec+compile worker for mechanical ones." `prompts/audit.md:85` resolves
it correctly ("Low-risk mechanical units → a lighter check: existence + spec-match + compile/scan only"),
but PROTOCOL's flat "runs all seven" contradicts its own risk-tiering paragraph and the audit prompt.
An operator reading only the checklist paragraph would over-audit every mechanical unit. **Suggested fix
unit:** soften :82 to "for a full audit the auditor runs all seven (mechanical units take the light tier —
see *Weight the audit by risk*)."

---

## LOW severity

**L1 — Oracle (V3-DESIGN.md) miscounts the diagrams it claims shipped.**
`V3-DESIGN.md:151`: "**8 Mermaid diagrams** across ch2–7 + ch9." Actual count is **9** (ch2:1, ch3:2,
ch4:1, ch5:2, ch6:1, ch7:1, ch9:1 = 9). The same line's "`mmdc` **9/9** exit 0" already implies 9, so the
file disagrees with itself in one sentence. `README.md:98`/`:99` correctly avoid a diagram count.
This is a multi-site-claim-check failure on the design ledger itself (the doc that "every unit is written
reading"). Not in a shipped target, hence LOW.

**L2 — `audit.md` "this is the entire context you get (target + oracle)" sits in mild tension with the 7-point checklist.**
`prompts/audit.md:40`: "**This is the entire context you get** (target + oracle), by design." Yet checks
#3 and #5 require the cited `D<n>`/`U<n>`/`Q<n>` and the "relevant `DECISIONS.md` entries." This is
*reconcilable* — PROTOCOL:78 defines the oracle as "the unit's inputs / spec / **the relevant ledger**,"
so DECISIONS/ledger must be packed into the Oracle list — but `audit.md`'s Oracle example (lines 42-44)
shows only generic "path 1 / path 2" and never says "include the DECISIONS entries and ledger rows the
checks need." A worker handed a thin oracle literally cannot run #3/#5. **Suggested fix:** add a line to
audit.md §3 that the Oracle must include any DECISIONS/ledger rows checks 3/5 will need.

**L3 — `driver-loop.md:28` step header says "per *done* unit"; body says "*authored-done*."**
Minor internal slip in the same step; "done" is ambiguous against the 5-state lifecycle (where bare
`done` is not a state). PROTOCOL:58 and ch4:17 correctly say "authored-done." Cosmetic.

**L4 — `CLAUDE.md` cross-refs PROTOCOL sections by names that don't match the actual headers.**
CLAUDE.md (root) points to "→ *Architecture*", "→ *Resilience & re-hydration*", "→ *Freeze*"; the actual
PROTOCOL headers are "The three roles", "Resilience — no context loss across any session end", and
"Anti-drift & the freeze." Prose pointers, not anchors, so they don't 404 — but they don't name-match.
(CLAUDE.md is bridge/context, outside the primary target set; noted for completeness.)

**L5 — ch9 scopes "the mechanics inside a project are settled (chapters 1–7)", silently excluding ch8.**
`docs/09-learning-across-projects.md:3`. ch8 ("In practice": adoption, bootstrapping, the worked example)
is in-project material too. Defensible (ch8 is "doing it," not new mechanics) but the bracket is loose;
"chapters 1–8" or "the build mechanics (chapters 1–7)" would be cleaner. Cosmetic.

---

## UNVERIFIED / not findings (checked and cleared, recorded so the next auditor doesn't re-walk them)

- **5 ledger states** — agree everywhere they're enumerated. `LEDGER.md.template` is the canonical
  enumeration (pending / in_progress / authored-done / verified-done / superseded); PROTOCOL, the
  prompts, and the chapters use a consistent subset and never introduce a sixth. PROTOCOL's bare word
  "`done`" (e.g. :86, :94, :109) is used as a *category* ("done"/"`*-done`"), not as a competing state —
  acceptable, though :86's "`done` (the output exists)" reads loosely against the lifecycle.
- **Audit gate / verdicts** — PASS, PASS-FINDINGS, FAIL and the "HIGH⇒FAIL; MED/LOW⇒PASS-FINDINGS;
  clean⇒PASS" mapping agree across PROTOCOL:84, audit.md:128, ch6:37-39. Gate ("downstream consumes only
  on a passing verdict") agrees across PROTOCOL:86, ch6:41, driver-loop:22, LEDGER template.
- **authored-done vs verified-done** distinction (who confers, self-cert impossible) — agree across
  PROTOCOL:80, ch3:86, ch6:9-23, worker-dispatch:110-116, audit.md:72-78. (The *how-many-workers*
  split is H1; the *concept* is consistent.)
- **Fan-in hard rule** (a worker reads the store; driver never holds N bodies) — agree across PROTOCOL:62,
  driver-loop:36-40, ch5:22-60, ch8:47. Strong.
- **Re-hydration = session-start reconcile, NO compaction hook** — agree across PROTOCOL:107,
  session-start.md:12/30, ch2:68, ch7:13-17, ch8:31, CLAUDE.md. Very consistent; the "honest limit" is
  told identically everywhere.
- **Worker-context minimalism / "exactly five things"** — the five-item list matches between
  PROTOCOL:68 and worker-dispatch:31-81.
- **Freeze + follow-on ownership** (concept) — agree across PROTOCOL:94-96, ch6:29-31, CLAUDE.md;
  register follow-on pending/in_progress-never-done is consistent. (Enforcement *claim* is M1.)
- **Stale refs** — the V3-DESIGN-flagged `docs/05-in-practice.md` stale ref is **resolved**: README and
  all docs point to `docs/08-in-practice.md`. No `subagent-dispatch`/`GOTM.md`/`STATUS.md` leftovers in
  shipped artifacts (only the intentional "supersedes v2's subagent-dispatch" note).
- **Counts** — "9 concept chapters" (README:97) and "7 templates" (README:99) match the filesystem;
  prose "nine chapters" (ch8:47) correct; field numbers (987K tokens, 380 KB / ~95K) consistent ch1 ↔
  V3-DESIGN. (Diagram count is L1.)

---

## Summary

Findings: **1 HIGH · 2 MEDIUM · 5 LOW** (plus a cleared/UNVERIFIED ledger of 9 invariants checked and
agreeing). HIGH ⇒ FAIL.

**Verdict: FAIL** — on the strength of H1. The framework's keystone honesty mechanism (verified-done)
is described by two incompatible operational models — a separate verified-done worker (PROTOCOL loop /
driver-loop / ch4) vs. a runtime check folded into the single audit worker (audit.md / worker-dispatch /
ch6 / PROTOCOL audit-gates) — and PROTOCOL contradicts itself between its own loop and audit sections.
Only the one-worker model has an operational prompt behind it; the two-worker model is asserted but never
specified. Pair this with M1 (ch6 claiming live freeze enforcement this repo doesn't ship — the exact
documented-but-unenforced trap v3's own check #6 exists to catch) and the two most load-bearing honesty
claims in v3 are the two least internally consistent. Everything else is in good shape.
