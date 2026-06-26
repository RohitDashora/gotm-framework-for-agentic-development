#!/usr/bin/env python3
"""Migrate a flat v2 GOTM LEDGER.md to the v3 born-tiered shape.

GENERAL + parameterized — pass the ledger path; nothing here is hardcoded to any
one repo. Generalizes the knowledge-graph `compact_ledger.py` prototype: same
robust LINE-LEVEL parsing (never column-splits prose cells with embedded pipes),
with all hardcoded paths / unit IDs removed and the v2->v3 state mapping added.

What it does (see MIGRATION.md §2.2 / §3, templates/LEDGER.md.template):
  - Reads a flat v2 ledger: one or more `| Uxx | ... | <status> | ... |` tables
    (typically under `## Units`) + an optional `## Recent updates` list.
  - Emits the v3 born-tiered shape:
      * `## Frontier` — open units (pending/in_progress) + the most-recent N
        closed units (by ID) kept FULL.
      * `## Archive`  — older CLOSED (done / verified-done / superseded) units
        compacted to ONE LINE each, newest-first, KEEPING the audit pointer.
      * `## Recent updates` — rolled to the last RECENT_KEEP entries.
  - Maps v2 statuses -> v3 states conservatively:
      done + passing-audit -> verified-done ;  done + no pass -> authored-done ;
      in_progress/pending/superseded -> unchanged.
  - LOSSLESS: backs up the original to LEDGER.md.bak FIRST; full original cells +
    old Recent-updates overflow to LEDGER-ARCHIVE.md; verifies EVERY unit ID is
    still present (prints `MISSING: NONE` or lists the lost IDs) + before/after
    sizes.

Usage:
    python3 migrate_ledger_v2_to_v3.py --ledger path/to/.gotm/LEDGER.md
    python3 migrate_ledger_v2_to_v3.py --ledger LEDGER.md --keep-recent-units 12 \
        --recent-updates 20 --dry-run

Or set DEFAULT_LEDGER below and run with no args.
"""

import argparse
import os
import re
import sys

# ----------------------------------------------------------------------------
# Clearly-marked constants (override on the CLI). NOT a hardcoded repo path —
# leave None to require --ledger, or set a path for convenience in one repo.
# ----------------------------------------------------------------------------
DEFAULT_LEDGER = None            # e.g. ".gotm/LEDGER.md"; None => --ledger required
KEEP_RECENT_UNITS = 10           # keep this many most-recent CLOSED units FULL in Frontier
RECENT_UPDATES_KEEP = 20         # keep this many most-recent `## Recent updates` entries

# v2 statuses that count as CLOSED (compactable once aged out of the window).
CLOSED_STATUSES = ("done", "verified-done", "superseded")
# v2 statuses that are OPEN (always kept full in the Frontier).
OPEN_STATUSES = ("pending", "in_progress", "in-progress", "authored-done", "blocked")

UID_RE = re.compile(r"^\|\s*(U\d+)\s*\|")
# A passing audit verdict anywhere relevant in a row (used for v2 done -> v3 mapping).
PASS_RE = re.compile(r"\bPASS-FINDINGS\b|\bPASS\b")
FAIL_RE = re.compile(r"\bFAIL\b")


def uid_of(line):
    m = UID_RE.match(line)
    return m.group(1) if m else None


def uid_num(uid):
    return int(uid[1:])


def is_unit_row(line):
    return uid_of(line) is not None


def status_of(line):
    """Pull the v2 status token from a `| Uxx | ... | <status> | ... |` row.
    Line-level + tolerant: scan cells for the FIRST recognized status word so
    prose cells with embedded pipes don't throw off a positional split."""
    cells = [c.strip() for c in line.split("|")]
    known = set(CLOSED_STATUSES) | set(OPEN_STATUSES)
    for c in cells:
        if c in known:
            return "in_progress" if c == "in-progress" else c
    # Fallback: regex for a bare status cell anywhere in the line.
    m = re.search(r"\|\s*(pending|in_progress|in-progress|authored-done|verified-done|done|superseded|blocked)\s*\|", line)
    if m:
        s = m.group(1)
        return "in_progress" if s == "in-progress" else s
    return None


def is_closed(line):
    return status_of(line) in CLOSED_STATUSES


def audit_pointer(line, uid):
    """The unit's OWN audit pointer, robust to other units' pointers / stray
    PASS/FAIL words in prose. Prefers `<VERDICT>-><...>audits/<uid>.md`; falls
    back to the last `AUDIT = <verdict>` marker, then a bare verdict."""
    own_pat = re.compile(
        r"(PASS-FINDINGS|PASS|FAIL)[^|]{0,80}?→\s*\.?/?[\w./-]*audits/" + re.escape(uid) + r"\.md"
    )
    matches = own_pat.findall(line)
    own_path = None
    pm = re.search(r"(\.?/?[\w./-]*audits/" + re.escape(uid) + r"\.md)", line)
    if pm:
        own_path = pm.group(1).lstrip("/")  # keep a leading dot (".gotm/…"); strip only "/"
    if matches and own_path:
        return f"{matches[-1]}→{own_path}"
    am = re.findall(r"AUDIT = (PASS-FINDINGS|PASS|FAIL)", line)
    if am and own_path:
        return f"{am[-1]}→{own_path}"
    if own_path:
        return f"see→{own_path}"
    if status_of(line) == "superseded":
        return "superseded"
    return "—"


def has_passing_audit(line, uid):
    ptr = audit_pointer(line, uid)
    return ptr.startswith("PASS")


def v3_state(line, uid):
    """Map a v2 status -> a v3 lifecycle state (conservative)."""
    s = status_of(line)
    if s == "done":
        return "verified-done" if has_passing_audit(line, uid) else "authored-done"
    if s == "in-progress":
        return "in_progress"
    return s or "pending"


def _clean_title(raw):
    """Title = the leading **bold** phrase (the unit name) if present, else the
    cell prefix. Strip markdown + collapse whitespace."""
    mt = re.match(r"\s*\*\*(.+?)\*\*", raw)
    title = mt.group(1) if mt else raw.strip()
    title = re.sub(r"[`*]", "", re.sub(r"\s+", " ", title)).strip()
    return title[:80]


def _find_output(*texts):
    """First backticked code/doc path across the given text fragments."""
    for t in texts:
        if not t:
            continue
        mo = re.search(r"`([^`]+?\.(?:py|ts|tsx|js|jsx|md|sql|sh|ya?ml|json|toml|txt))`", t)
        if mo:
            return mo.group(1)
    return None


def parse_row(line, uid):
    """Normalize EITHER source table shape into (title, inputs, output) — line-level,
    so prose cells with embedded pipes never mis-split. Two shapes are handled:
      * v2 native     : | ID | Title | Inputs | Output | Status | Audit |
      * prototype arch : | ID | Title | Status | Audit | Output |  (no Inputs col)
    Detected by the column index of the status token. Status + audit are derived
    by the line-level helpers (status_of / audit_pointer), not by position."""
    cells = [c for c in line.split("|")]           # cells[1]=ID, cells[2]=Title, ...
    body = [c.strip() for c in cells[2:-1]] if len(cells) >= 4 else []
    known = set(CLOSED_STATUSES) | set(OPEN_STATUSES) | {"in-progress"}
    status_idx = next((k for k, c in enumerate(body) if c in known), None)
    title = _clean_title(body[0]) if body else uid
    inputs, output = "—", None
    if status_idx is None:
        # No bare status cell (e.g. an annotated v2 row) — assume native layout.
        inputs = re.sub(r"\s+", " ", body[1]).strip() if len(body) > 1 else "—"
        output = _find_output(body[2] if len(body) > 2 else None, line)
    elif status_idx == 1:
        # prototype-archive shape: Title | Status | Audit | Output
        output = _find_output(body[3] if len(body) > 3 else None, line)
    else:
        # native shape: Title | Inputs | Output | Status | Audit
        inputs = re.sub(r"\s+", " ", body[1]).strip() if len(body) > 1 else "—"
        output = _find_output(body[2] if len(body) > 2 else None, line)
    return title, (inputs or "—"), (output or _find_output(line))


def one_liner(line, uid):
    """v3 Archive one-line entry (templates/LEDGER.md.template):
       - U<n> — <title> · `<output>` · <state> · <verdict>→audits/U<n>.md"""
    title, _inputs, out = parse_row(line, uid)
    state = v3_state(line, uid)
    audit = audit_pointer(line, uid)
    return f"- {uid} — {title} · `{out or 'see LEDGER-ARCHIVE.md'}` · {state} · {audit}"


def frontier_row(line, uid):
    """Re-emit a kept unit as a CANONICAL v3 Frontier row (6 cols), state-mapped
    to v3. Normalizes both source shapes so a partially-compacted v2 ledger
    doesn't leak stray `done`/`Audit:` cells into the hot tier."""
    title, inputs, output = parse_row(line, uid)
    state = v3_state(line, uid)
    audit = audit_pointer(line, uid)
    if audit == "—" and state == "in_progress":
        audit = "pending"
    # For a kept FULL native row, preserve the verbatim Title cell (rich detail)
    # rather than the truncated clean title — only the Status/Audit are re-mapped.
    cells = [c for c in line.split("|")]
    body = [c.strip() for c in cells[2:-1]] if len(cells) >= 4 else []
    known = set(CLOSED_STATUSES) | set(OPEN_STATUSES) | {"in-progress"}
    status_idx = next((k for k, c in enumerate(body) if c in known), None)
    if status_idx is None or status_idx >= 3:
        # native layout (status in col 4+): keep the full Title/Inputs/Output verbatim
        full_title = body[0] if body else title
        inputs = body[1] if len(body) > 1 else inputs
        output_cell = body[2] if len(body) > 2 else (output or "—")
        return f"| {uid} | {full_title} | {inputs} | {output_cell} | {state} | {audit} |"
    # prototype-archive layout: rebuild from the normalized parse
    return f"| {uid} | {title} | {inputs} | {output or '—'} | {state} | {audit} |"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Migrate a flat v2 GOTM LEDGER.md to the v3 born-tiered shape.")
    ap.add_argument("--ledger", default=DEFAULT_LEDGER, help="path to the v2 LEDGER.md (required unless DEFAULT_LEDGER is set)")
    ap.add_argument("--archive", default=None, help="overflow file path (default: LEDGER-ARCHIVE.md beside the ledger)")
    ap.add_argument("--keep-recent-units", type=int, default=KEEP_RECENT_UNITS, help="keep this many most-recent CLOSED units FULL in Frontier")
    ap.add_argument("--recent-updates", type=int, default=RECENT_UPDATES_KEEP, help="keep this many most-recent Recent-updates entries")
    ap.add_argument("--dry-run", action="store_true", help="report what would change without writing")
    args = ap.parse_args(argv)

    if not args.ledger:
        ap.error("no ledger path: pass --ledger PATH or set DEFAULT_LEDGER at the top of the script")
    led = os.path.abspath(args.ledger)
    if not os.path.isfile(led):
        ap.error(f"ledger not found: {led}")
    arc = os.path.abspath(args.archive) if args.archive else os.path.join(os.path.dirname(led), "LEDGER-ARCHIVE.md")

    src = open(led, encoding="utf-8").read().split("\n")
    orig_size = sum(len(l) + 1 for l in src)

    # ---- determine the cutoff: keep the N most-recent CLOSED units FULL ----
    closed_ids = sorted({uid_num(uid_of(l)) for l in src if is_unit_row(l) and is_closed(l)})
    keep_from = closed_ids[-args.keep_recent_units] if len(closed_ids) > args.keep_recent_units else (closed_ids[0] if closed_ids else 0)

    def compactable(line):
        uid = uid_of(line)
        return uid is not None and is_closed(line) and uid_num(uid) < keep_from

    # ---- walk lines: split into archived rows + new ledger body ----
    out_lines, archived_rows, archive_oneliners = [], [], []
    in_recent = False
    recent_buf = []
    archive_emitted = False

    i = 0
    while i < len(src):
        line = src[i]
        if line.strip() == "## Recent updates":
            # Emit the v3 ## Archive section just BEFORE Recent updates.
            out_lines.append("## Archive")
            out_lines.append("")
            out_lines.append("<!-- COLD tier — one line per aged-out closed unit, newest-first; audit pointer kept. Full original cells in LEDGER-ARCHIVE.md. -->")
            out_lines.append("")
            out_lines.extend(reversed(archive_oneliners))  # newest-first
            out_lines.append("")
            out_lines.append(line)
            archive_emitted = True
            in_recent = True
            i += 1
            continue
        if in_recent:
            recent_buf.append(line)
            i += 1
            continue
        # Rename a v2 `## Units` heading to the v3 `## Frontier`.
        if line.strip() == "## Units":
            out_lines.append("## Frontier")
            i += 1
            continue
        # Drop any pre-existing `## Archive` heading from a prior compaction run —
        # its rows are re-tiered below; we re-emit one clean v3 Archive section.
        if line.strip().startswith("## Archive"):
            i += 1
            continue
        if is_unit_row(line):
            uid = uid_of(line)
            if compactable(line):
                archived_rows.append(line)
                archive_oneliners.append(one_liner(line, uid))
            else:
                # kept in the hot tier — re-emit with v3 state mapping
                out_lines.append(frontier_row(line, uid))
        else:
            out_lines.append(line)
        i += 1

    # If there was no `## Recent updates` section, append the Archive at the end.
    if not archive_emitted and archive_oneliners:
        out_lines.append("")
        out_lines.append("## Archive")
        out_lines.append("")
        out_lines.append("<!-- COLD tier — one line per aged-out closed unit, newest-first; audit pointer kept. Full original cells in LEDGER-ARCHIVE.md. -->")
        out_lines.append("")
        out_lines.extend(reversed(archive_oneliners))

    # ---- roll Recent updates: keep last RECENT_UPDATES_KEEP entries ----
    entry_idxs = [k for k, l in enumerate(recent_buf) if re.match(r"^\s*[-*]\s", l) or re.match(r"^\s*\d+\.\s", l)]
    old_recent, kept_recent = [], recent_buf
    if len(entry_idxs) > args.recent_updates:
        cut = entry_idxs[-args.recent_updates]
        old_recent = recent_buf[:cut]
        kept_recent = recent_buf[cut:]
    out_lines.extend(kept_recent)

    new_led = "\n".join(out_lines)

    # ---- verify losslessness BEFORE writing ----
    orig_ids = [uid_of(l) for l in src if is_unit_row(l)]
    new_ids = [uid_of(l) for l in new_led.split("\n") if is_unit_row(l)]
    arc_ids = [uid_of(l) for l in archived_rows]
    orig_unique = set(orig_ids)
    present = set(new_ids) | set(arc_ids)
    missing = sorted(orig_unique - present, key=lambda u: uid_num(u))
    dups = sorted({u for u in orig_unique if orig_ids.count(u) > 1}, key=lambda u: uid_num(u))

    def _count_entries(lines):
        return sum(1 for l in lines if re.match(r"^\s*[-*]\s", l) or re.match(r"^\s*\d+\.\s", l))

    print("=" * 64)
    print(f"ledger             : {led}")
    print(f"keep-from (CLOSED) : U{keep_from}  (kept {len(new_ids)} full, archived {len(arc_ids)})")
    print(f"orig units         : {len(orig_unique)} unique ({len(orig_ids)} rows)   present after : {len(present)}")
    if dups:
        print(f"DUP IDs in source  : {', '.join(dups)}  (kept; not a loss)")
    print(f"MISSING            : {'NONE' if not missing else ', '.join(missing)}")
    print(f"recent-updates     : kept {_count_entries(kept_recent)}, archived {_count_entries(old_recent)}")

    if missing:
        print("\nABORT: unit IDs would be lost — not writing. (Inspect the rows above.)", file=sys.stderr)
        return 2

    if args.dry_run:
        new_size = len(new_led.encode("utf-8"))
        print(f"size (DRY RUN)     : {orig_size} -> {new_size} bytes  (no files written)")
        print("=" * 64)
        return 0

    # ---- write: back up original first, then ledger + archive overflow ----
    bak = led + ".bak"
    open(bak, "w", encoding="utf-8").write("\n".join(src))
    open(led, "w", encoding="utf-8").write(new_led)

    arc_doc = [
        "# LEDGER archive (v2->v3 migration overflow)",
        "",
        "Lossless overflow from the born-tiered `LEDGER.md`. NOT read at session start; consult on demand.",
        "Per-unit audit detail also lives in `audits/`. Generated by `scripts/migrate_ledger_v2_to_v3.py`.",
        "",
        "## Archived unit cells (verbatim v2 rows)",
        "",
    ] + archived_rows + [
        "",
        "## Archived Recent-updates (older entries)",
        "",
    ] + old_recent
    open(arc, "w", encoding="utf-8").write("\n".join(arc_doc))

    new_size = os.path.getsize(led)
    print(f"backup             : {bak}")
    print(f"archive overflow   : {arc}")
    print(f"size               : {orig_size} -> {new_size} bytes")
    print("=" * 64)
    print("DONE — converted to v3 born-tiered shape (Frontier + Archive + rolled Recent updates).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
