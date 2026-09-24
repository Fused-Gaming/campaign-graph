from __future__ import annotations

from datetime import timedelta
from campaign_graph.models import Edge, MONEY_EDGE_TYPES, DECISION_EDGE_TYPES


def temporal_correlations(edges: list[Edge], days: int = 90) -> list[dict]:
    """Produce research leads only. Proximity is not evidence of causation."""
    money = [e for e in edges if e.type in MONEY_EDGE_TYPES and e.date]
    decisions = [e for e in edges if e.type in DECISION_EDGE_TYPES and e.date]
    leads = []
    for m in money:
        for d in decisions:
            delta = d.date - m.date
            if timedelta(0) <= delta <= timedelta(days=days):
                involved = {m.source, m.target} & {d.source, d.target}
                if involved:
                    leads.append({"flag": "TEMPORAL_CORRELATION_REQUIRES_INVESTIGATION", "money_edge_id": m.id, "decision_edge_id": d.id, "days_apart": delta.days, "shared_node_ids": sorted(involved)})
    return leads
