from __future__ import annotations

from collections import Counter
from typing import Iterable
import networkx as nx
from campaign_graph.models import DECISION_EDGE_TYPES, MONEY_EDGE_TYPES, Edge, Node, VerificationStatus


def build_graph(nodes: list[Node], edges: list[Edge]) -> nx.MultiDiGraph:
    g = nx.MultiDiGraph()
    for node in nodes:
        g.add_node(node.id, **node.model_dump(mode="json"))
    for edge in edges:
        g.add_edge(edge.source, edge.target, key=edge.id, **edge.model_dump(mode="json"))
    return g


def select_edges(edges: Iterable[Edge], view: str) -> list[Edge]:
    edges = list(edges)
    if view == "money":
        return [e for e in edges if e.type in MONEY_EDGE_TYPES]
    if view == "decision":
        return [e for e in edges if e.type in DECISION_EDGE_TYPES]
    if view == "influence":
        return [e for e in edges if e.type not in MONEY_EDGE_TYPES and e.type not in DECISION_EDGE_TYPES]
    return edges


def _edge_status(statuses: list[str]) -> str:
    for status in ["CONTRADICTED", "UNRESOLVED", "INFERRED", "DOCUMENTED"]:
        if status in statuses:
            return status
    return "UNRESOLVED"


def cytoscape_payload(nodes: list[Node], edges: list[Edge], view: str = "all") -> dict:
    chosen = select_edges(edges, view)
    used = {e.source for e in chosen} | {e.target for e in chosen}
    if view == "all":
        used = {n.id for n in nodes}
    cy_nodes = [{"data": n.model_dump(mode="json")} for n in nodes if n.id in used]
    cy_edges = []
    for edge in chosen:
        raw = edge.model_dump(mode="json")
        raw["verification_status"] = _edge_status([x.verification_status.value for x in edge.evidence])
        raw["confidence"] = min([x.confidence.value for x in edge.evidence], default="D")
        raw["source_url"] = edge.evidence[0].source_url if edge.evidence else None
        raw["description"] = edge.evidence[0].evidence_quote_or_summary if edge.evidence else ""
        cy_edges.append({"data": raw})
    return {"elements": {"nodes": cy_nodes, "edges": cy_edges}, "view": view}


def dashboard_metrics(nodes: list[Node], edges: list[Edge]) -> dict:
    documented = [e for e in edges if any(x.verification_status == VerificationStatus.DOCUMENTED for x in e.evidence)]
    money_edges = [e for e in documented if e.type in MONEY_EDGE_TYPES and e.amount is not None]
    counts = Counter(e.type.value for e in documented)
    return {
        "documented_connections": len(documented),
        "financial_transactions": len(money_edges),
        "total_documented_money": round(sum(e.amount or 0 for e in money_edges), 2),
        "lobbying_contacts": counts["LOBBIED"],
        "political_contributions": counts["CONTRIBUTION"] + counts["PAC_CONTRIBUTION"],
        "grants": counts["GRANTED"],
        "government_decisions": sum(counts[x] for x in ["VOTED_YES", "VOTED_NO", "RECUSED", "ABSTAINED", "ABSENT", "PRESENT_NO_RECORDED_VOTE", "APPROVED"]),
        "shared_addresses": counts["SHARED_ADDRESS"] + counts["SAME_BUILDING"],
        "unresolved_connections": sum(1 for e in edges if any(x.verification_status == VerificationStatus.UNRESOLVED for x in e.evidence)),
        "contradicted_claims": sum(1 for e in edges if any(x.verification_status == VerificationStatus.CONTRADICTED for x in e.evidence)),
    }
