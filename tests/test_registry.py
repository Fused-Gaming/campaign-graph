from campaign_graph.models import Node, NodeType
from campaign_graph.registry import EntityRegistry


def test_name_only_does_not_merge():
    existing = Node(id="person:alex-smith:1", label="Alex Smith", type=NodeType.PERSON, identifiers={"city": "Oakland"})
    registry = EntityRegistry([existing])
    assert registry.resolve_for_merge("Alex Smith", NodeType.PERSON, {}) is None


def test_stable_identifier_can_merge():
    existing = Node(id="campaign:test:1", label="Example Committee", type=NodeType.CAMPAIGN, identifiers={"fec_id": "C00000000"})
    registry = EntityRegistry([existing])
    assert registry.resolve_for_merge("Example Committee", NodeType.CAMPAIGN, {"fec_id": "C00000000"}) == existing.id
