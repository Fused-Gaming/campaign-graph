from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from campaign_graph.models import Node, NodeType


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def stable_node_id(node_type: NodeType, canonical_name: str, discriminator: str = "") -> str:
    raw = f"{node_type}:{canonical_name.strip().lower()}:{discriminator.strip().lower()}"
    digest = hashlib.sha256(raw.encode()).hexdigest()[:12]
    return f"{node_type.lower()}:{_slug(canonical_name)[:50]}:{digest}"


@dataclass(frozen=True)
class CandidateMatch:
    node_id: str
    score: int
    reasons: tuple[str, ...]


class EntityRegistry:
    """Conservative resolver. Name similarity alone never authorizes a merge."""

    def __init__(self, nodes: list[Node] | None = None):
        self.nodes = {n.id: n for n in (nodes or [])}

    def add(self, node: Node) -> None:
        if node.id in self.nodes and self.nodes[node.id] != node:
            raise ValueError(f"Node id collision: {node.id}")
        self.nodes[node.id] = node

    def candidates(self, label: str, node_type: NodeType, identifiers: dict[str, str]) -> list[CandidateMatch]:
        label_norm = label.casefold().strip()
        results = []
        for node in self.nodes.values():
            if node.type != node_type:
                continue
            score = 0
            reasons = []
            if any(x.casefold().strip() == label_norm for x in [node.label, *node.aliases]):
                score += 1
                reasons.append("exact_name")
            for key, value in identifiers.items():
                if value and node.identifiers.get(key) == value:
                    score += 10
                    reasons.append(f"identifier:{key}")
            if score:
                results.append(CandidateMatch(node.id, score, tuple(reasons)))
        return sorted(results, key=lambda x: x.score, reverse=True)

    def resolve_for_merge(self, label: str, node_type: NodeType, identifiers: dict[str, str]) -> str | None:
        matches = self.candidates(label, node_type, identifiers)
        if not matches or matches[0].score < 10:
            return None
        if len(matches) > 1 and matches[1].score == matches[0].score:
            return None
        return matches[0].node_id
