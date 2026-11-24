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
import sys
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def read_committee_totals(investigation_dir: Path) -> list[dict]:
    """Read committee_totals.json and return its per-cycle total rows, skipping notes."""
    path = investigation_dir / "committee_totals.json"
    if not path.exists():
        return []
    rows = json.loads(path.read_text())
    return [r for r in rows if "committee_id" in r and "cycle" in r]


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
    totals_rows = read_committee_totals(investigation_dir)
    if not totals_rows:
        raise SystemExit(
            f"No committee_totals.json rows found for '{investigation_slug}' -- "
            "nothing to build a money-flow view from yet."
        )

    nodes: dict[str, dict] = {}
    edges: list[dict] = []
    edge_n = 0

    def add_node(node_id: str, label: str, node_type: str) -> str:
        if node_id not in nodes:
            nodes[node_id] = {
                "id": node_id,
                "label": label,
                "node_type": node_type,
                "investigation_node_id": None,
            }
        return node_id

    for cat_id, cat_label in CATEGORY_NODES.items():
        add_node(cat_id, cat_label, "category")

    for row in totals_rows:
        committee_id = row["committee_id"]
        committee_label = f"{row.get('committee_name', committee_id)} ({committee_id})"
        committee_node = add_node(committee_node_id(committee_id), committee_label, "committee")
        period_start = row.get("coverage_start_date")
        period_end = row.get("coverage_end_date")
        source_url = row.get("source", "").split(": ", 1)[-1] if row.get("source") else ""
        source_title = f"FEC committee totals API, cycle {row.get('cycle')}"
        accessed_date = _extract_accessed_date(row.get("source", ""))

        def inflow(category_id: str, amount: float | None, flow_type: str = "contribution") -> None:
            nonlocal edge_n
            if not amount:
                return
            edge_n += 1
            edges.append({
                "id": f"flow-{investigation_slug}-{edge_n}",
                "source_id": category_id,
                "target_id": committee_node,
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

        def outflow(category_id: str, amount: float | None, flow_type: str = "disbursement") -> None:
            nonlocal edge_n
            if not amount:
                return
            edge_n += 1
            edges.append({
                "id": f"flow-{investigation_slug}-{edge_n}",
                "source_id": committee_node,
                "target_id": category_id,
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

        inflow("category-individual-itemized", row.get("individual_itemized_contributions_usd"))
        inflow("category-individual-unitemized", row.get("individual_unitemized_contributions_usd"))
        inflow("category-other-committee-contributions", row.get("other_political_committee_contributions_usd"))

        outflow("category-operating-expenditures", row.get("operating_expenditures_usd"))
        outflow("category-refunds", row.get("contribution_refunds_usd"), flow_type="refund")
        other_disb = row.get("disbursements_usd", 0) - row.get("operating_expenditures_usd", 0)
        if other_disb and other_disb > 0.005:
            outflow("category-other-disbursements", other_disb)

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


def _extract_accessed_date(source_text: str) -> str:
    # committee_totals.json sources look like "FEC API, fetched directly 2026-10-03: https://..."
    for token in source_text.replace(",", " ").split():
        candidate = token.strip(":;.")
        try:
            datetime.strptime(candidate, "%Y-%m-%d")
            return candidate
        except ValueError:
            continue
    return date.today().isoformat()


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
