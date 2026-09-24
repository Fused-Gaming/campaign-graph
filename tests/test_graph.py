from datetime import date
from campaign_graph.graph import dashboard_metrics, select_edges
from campaign_graph.models import Confidence, Edge, EdgeType, Evidence, Node, NodeType, VerificationStatus


def evidence():
    return Evidence(source_url="https://example.gov/record/1", source_title="Official record", accessed_date=date(2026, 9, 24), source_type="government", evidence_quote_or_summary="Example documented transfer.", confidence=Confidence.A, verification_status=VerificationStatus.DOCUMENTED)


def test_money_view_excludes_access_edge():
    edges = [
        Edge(id="e1", source="a", target="b", type=EdgeType.CONTRIBUTION, amount=100, date=date(2026,1,1), evidence=[evidence()]),
        Edge(id="e2", source="a", target="b", type=EdgeType.MET_WITH, date=date(2026,1,2), evidence=[evidence()]),
    ]
    assert [e.id for e in select_edges(edges, "money")] == ["e1"]


def test_total_money_only_documented_amounts():
    nodes = [Node(id="a", label="A", type=NodeType.PERSON), Node(id="b", label="B", type=NodeType.CAMPAIGN)]
    edges = [Edge(id="e1", source="a", target="b", type=EdgeType.CONTRIBUTION, amount=100, evidence=[evidence()])]
    assert dashboard_metrics(nodes, edges)["total_documented_money"] == 100
