#!/usr/bin/env python3
"""Build investigations/<slug>/money_flow.json from that package's existing evidence files.

Prototype transform script (see docs/MONEY_FLOW_SPEC.md). Currently reads only
committee_totals.json's aggregate FEC committee-totals breakdown, since that's the only
money-flow-shaped data this repo has pulled so far. Extend read_*() functions here as
itemized sources (contributions.json Schedule A rows, a future disbursements.json) come
online -- do not hand-edit money_flow.json; it is generated output.

Usage:
    python scripts/build_money_flow.py <investigation-slug>
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def read_committee_totals(investigation_dir: Path) -> list[dict]:
    """Read committee_totals.json and return its per-cycle total rows, skipping notes.

    Rows with a committee_id but no cycle (e.g. a lifetime/non-cycle-scoped total) are
    skipped and reported via dropped_no_cycle so callers can warn instead of silently
    losing data. Rows that share the same (committee_id, cycle) are deduplicated,
    keeping only the row with the most recent-looking accessed/fetch date in its
    "source" text (falling back to the last one seen) so an appended amendment never
    gets summed alongside the snapshot it supersedes.
    """
    path = investigation_dir / "committee_totals.json"
    if not path.exists():
        return [], []
    rows = json.loads(path.read_text())
    with_cycle = [r for r in rows if "committee_id" in r and "cycle" in r]
    dropped_no_cycle = [r for r in rows if "committee_id" in r and "cycle" not in r]

    by_key: dict[tuple, dict] = {}
    for row in with_cycle:
        key = (row["committee_id"], row["cycle"])
        if key not in by_key:
            by_key[key] = row
            continue
        existing = by_key[key]
        new_date = _extract_accessed_date(row.get("source", "")) or ""
        existing_date = _extract_accessed_date(existing.get("source", "")) or ""
        if new_date >= existing_date:
            by_key[key] = row
    return list(by_key.values()), dropped_no_cycle


def committee_node_id(committee_id: str) -> str:
    return f"committee-{committee_id.lower()}"


CATEGORY_NODES = {
    "category-individual-itemized": "Individual contributions (itemized)",
    "category-individual-unitemized": "Individual contributions (unitemized)",
    "category-other-committee-contributions": "Other political committee contributions",
    "category-operating-expenditures": "Operating expenditures",
    "category-refunds": "Contribution refunds",
    "category-other-disbursements": "Other disbursements",
}


def build_flow(investigation_slug: str) -> dict:
    investigation_dir = REPO_ROOT / "investigations" / investigation_slug
    totals_rows, dropped_no_cycle = read_committee_totals(investigation_dir)
    if dropped_no_cycle:
        print(
            f"WARNING: skipping {len(dropped_no_cycle)} committee_totals.json row(s) "
            f"with a committee_id but no 'cycle' field -- not represented in this "
            f"money-flow view: {[r.get('committee_id') for r in dropped_no_cycle]}",
            file=sys.stderr,
        )
    if not totals_rows:
        raise SystemExit(
            f"No committee_totals.json rows found for '{investigation_slug}' -- "
            "nothing to build a money-flow view from yet."
        )

    nodes: dict[str, dict] = {}
    edges: list[dict] = []
    edge_n = 0

    def add_node(node_id: str, label: str, node_type: str) -> str:
        existing = nodes.get(node_id)
        if existing is None:
            nodes[node_id] = {
                "id": node_id,
                "label": label,
                "node_type": node_type,
                "investigation_node_id": None,
            }
        elif existing["label"] != label or existing["node_type"] != node_type:
            raise SystemExit(
                f"Node id collision: '{node_id}' was already defined as "
                f"({existing['label']!r}, {existing['node_type']!r}) but a second, "
                f"conflicting definition was seen: ({label!r}, {node_type!r}). "
                "Refusing to silently merge two different entities under one id."
            )
        return node_id

    for row in totals_rows:
        committee_id = row["committee_id"]
        committee_label = f"{row.get('committee_name', committee_id)} ({committee_id})"
        committee_node = add_node(committee_node_id(committee_id), committee_label, "committee")
        period_start = row.get("coverage_start_date")
        period_end = row.get("coverage_end_date")
        source_url = _extract_source_url(row.get("source", ""))
        if not source_url:
            raise SystemExit(
                f"Could not extract a source URL from committee_totals.json's "
                f"'source' field for committee {committee_id}, cycle {row.get('cycle')} "
                f"(source text: {row.get('source')!r}). Refusing to emit evidence with "
                "no path back to its source."
            )
        source_title = f"FEC committee totals API, cycle {row.get('cycle')}"
        accessed_date = _extract_accessed_date(row.get("source", ""))
        if accessed_date is None:
            raise SystemExit(
                f"Could not extract an accessed_date from committee_totals.json's "
                f"'source' field for committee {committee_id}, cycle {row.get('cycle')} "
                f"(source text: {row.get('source')!r}). Refusing to fabricate today's "
                "date in its place -- fix the source string or extend "
                "_extract_accessed_date to recognize its format."
            )

        def add_flow(category_id: str, amount: float | None, *, direction: str, flow_type: str) -> None:
            nonlocal edge_n
            if amount is None:
                return
            if amount < 0:
                print(
                    f"WARNING: committee {committee_id}, cycle {row.get('cycle')}: "
                    f"{category_id} amount is negative ({amount}) -- skipping rather "
                    "than emitting a flow edge the schema (amount_usd >= 0) forbids. "
                    "This usually means an FEC amendment restated a prior total; "
                    "investigate before trusting this cycle's other figures.",
                    file=sys.stderr,
                )
                return
            if amount == 0:
                return
            if category_id not in CATEGORY_NODES:
                raise SystemExit(f"Unknown category id: {category_id!r}")
            add_node(category_id, CATEGORY_NODES[category_id], "category")
            source_id, target_id = (
                (category_id, committee_node) if direction == "in" else (committee_node, category_id)
            )
            edge_n += 1
            edges.append({
                "id": f"flow-{investigation_slug}-{edge_n}",
                "source_id": source_id,
                "target_id": target_id,
                "amount_usd": round(amount, 2),
                "flow_type": flow_type,
                "period_start": period_start,
                "period_end": period_end,
                "transaction_count": None,
                "confidence": "A",
                "source_url": source_url,
                "source_title": source_title,
                "accessed_date": accessed_date,
                "note": f"Aggregate figure from FEC committee totals, cycle {row.get('cycle')}. Not itemized.",
            })

        add_flow(
            "category-individual-itemized",
            row.get("individual_itemized_contributions_usd"),
            direction="in", flow_type="contribution",
        )
        add_flow(
            "category-individual-unitemized",
            row.get("individual_unitemized_contributions_usd"),
            direction="in", flow_type="contribution",
        )
        add_flow(
            "category-other-committee-contributions",
            row.get("other_political_committee_contributions_usd"),
            direction="in", flow_type="contribution",
        )

        add_flow(
            "category-operating-expenditures",
            row.get("operating_expenditures_usd"),
            direction="out", flow_type="disbursement",
        )
        add_flow(
            "category-refunds",
            row.get("contribution_refunds_usd"),
            direction="out", flow_type="refund",
        )
        disbursements = row.get("disbursements_usd")
        operating = row.get("operating_expenditures_usd")
        if disbursements is not None and operating is not None:
            other_disb = disbursements - operating
            if other_disb > 0.005:
                add_flow(
                    "category-other-disbursements", other_disb,
                    direction="out", flow_type="disbursement",
                )
        elif disbursements is not None:
            # operating_expenditures_usd is absent/null for this row -- we cannot tell
            # how much of disbursements_usd was operating vs. other, so record the
            # whole amount under "other" rather than guessing a split, and flag it.
            print(
                f"WARNING: committee {committee_id}, cycle {row.get('cycle')} has "
                f"disbursements_usd but no operating_expenditures_usd -- recording "
                "the full amount as 'other disbursements' since the split is unknown.",
                file=sys.stderr,
            )
            add_flow(
                "category-other-disbursements", disbursements,
                direction="out", flow_type="disbursement",
            )

    used_node_ids = {e["source_id"] for e in edges} | {e["target_id"] for e in edges}
    final_nodes = [n for n in nodes.values() if n["id"] in used_node_ids]

    return {
        "schema_version": "1.0",
        "investigation_slug": investigation_slug,
        "generated_at": date.today().isoformat(),
        "generated_by": "scripts/build_money_flow.py",
        "nodes": final_nodes,
        "edges": edges,
    }


def _extract_accessed_date(source_text: str) -> str | None:
    """Extract an ISO date from a committee_totals.json "source" string.

    Expects this pipeline's own fixed "... fetched directly YYYY-MM-DD: ..." shape.
    Returns None -- never a fabricated date -- when no such date is present. Per
    AGENTS.md ("Unknown facts remain unknown"), a missing date must be surfaced as an
    error by the caller, not silently replaced with today's date in a confidence-"A"
    evidence record.
    """
    match = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", source_text)
    return match.group(1) if match else None


_URL_RE = re.compile(r"https?://\S+")


def _extract_source_url(source_text: str) -> str:
    """Extract an http(s) URL from a committee_totals.json "source" string.

    Uses a URL pattern match rather than assuming any particular surrounding text
    shape (e.g. "label: url"), so a differently formatted source string still yields
    a real link instead of silently returning descriptive text as if it were one.
    Returns "" (never a non-URL string) when no URL is present -- the caller/schema
    layer is responsible for treating an empty source_url as missing evidence.
    """
    match = _URL_RE.search(source_text)
    return match.group(0).rstrip(").,;") if match else ""


def main() -> None:
    if len(sys.argv) != 2:
        print(__doc__)
        raise SystemExit(1)
    slug = sys.argv[1]
    flow = build_flow(slug)
    out_path = REPO_ROOT / "investigations" / slug / "money_flow.json"
    out_path.write_text(json.dumps(flow, indent=2) + "\n")
    print(f"Wrote {out_path} ({len(flow['edges'])} edges, {len(flow['nodes'])} nodes)")


if __name__ == "__main__":
    main()
