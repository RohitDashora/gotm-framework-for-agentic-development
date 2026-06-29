# Fix note — H1 (verified-done architectural split) — 2026-06-29

Reconciled the HIGH consistency finding (H1 in `v3-build-consistency.md`): v3 described
`verified-done` via two incompatible operational models — a *separate* verified-done worker
dispatched alongside the audit worker (PROTOCOL loop step 4, driver-loop step 4, docs/04 loop
step + mermaid) vs. a runtime check folded into the *single* audit worker (audit.md §4a,
worker-dispatch, docs/06, PROTOCOL *Audit gates*). The decision: standardize on the
one-worker model that already has an operational prompt — **the single audit worker performs
the runtime verified-done check** (one worker, one verdict, one `audits/<Uxx>.md` report); there
is no separate verified-done worker. Reworded the loop step in all five affected files
(`framework/templates/PROTOCOL.md.template`, `framework/prompts/driver-loop.md`,
`framework/docs/04-the-loop.md` including its mermaid node, `plugin/templates/PROTOCOL.md.template`,
`plugin/templates/prompts/driver-loop.md`) so the loop sections match the Audit-gates sections,
eliminating PROTOCOL's internal loop-vs-audit self-contradiction. Post-edit grep across the five
files confirms no residual language implies a second/distinct verified-done worker — every
remaining `verified-done` mention is either the audit worker raising its bar, the
authored-done/verified-done state distinction, or the never-self-certify rule. H1 resolved.
