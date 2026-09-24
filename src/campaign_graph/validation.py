from __future__ import annotations

from campaign_graph.models import Edge, VerificationStatus


def validate_edges(edges: list[Edge], node_ids: set[str]) -> list[str]:
    errors = []
    seen = set()
    for edge in edges:
        if edge.id in seen:
            errors.append(f"duplicate edge id: {edge.id}")
        seen.add(edge.id)
        if edge.source not in node_ids:
            errors.append(f"{edge.id}: unknown source node {edge.source}")
        if edge.target not in node_ids:
            errors.append(f"{edge.id}: unknown target node {edge.target}")
        if not edge.evidence:
            errors.append(f"{edge.id}: missing evidence")
        for ev in edge.evidence:
            if not ev.source_url:
                errors.append(f"{edge.id}: evidence missing source_url")
            if not ev.evidence_quote_or_summary.strip():
                errors.append(f"{edge.id}: evidence missing quote/summary")
        if edge.amount is not None and edge.amount < 0:
            errors.append(f"{edge.id}: amount must be non-negative; model refunds explicitly")
        if any(ev.verification_status == VerificationStatus.DOCUMENTED for ev in edge.evidence) and not any(ev.confidence.value in {"A", "B", "C"} for ev in edge.evidence):
            errors.append(f"{edge.id}: DOCUMENTED edge has no A/B/C evidence")
    return errors
