from __future__ import annotations

import json
from pathlib import Path
from pydantic import TypeAdapter
from campaign_graph.models import Edge, Event, Node

NodeList = TypeAdapter(list[Node])
EdgeList = TypeAdapter(list[Edge])
EventList = TypeAdapter(list[Event])


def read_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text())


def load_nodes(data_dir: Path) -> list[Node]:
    return NodeList.validate_python(read_json(data_dir / "nodes.json", []))


def load_edges(data_dir: Path) -> list[Edge]:
    return EdgeList.validate_python(read_json(data_dir / "edges.json", []))


def load_events(data_dir: Path) -> list[Event]:
    return EventList.validate_python(read_json(data_dir / "events.json", []))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, default=str) + "\n")
