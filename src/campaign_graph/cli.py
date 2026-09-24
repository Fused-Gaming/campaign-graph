from __future__ import annotations

from pathlib import Path
import typer
import uvicorn
from campaign_graph.graph import cytoscape_payload
from campaign_graph.io import load_edges, load_nodes, write_json
from campaign_graph.validation import validate_edges

app = typer.Typer(no_args_is_help=True)
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"


@app.command()
def validate():
    nodes = load_nodes(DATA)
    edges = load_edges(DATA)
    errors = validate_edges(edges, {n.id for n in nodes})
    if errors:
        for error in errors:
            typer.echo(f"ERROR: {error}")
        raise typer.Exit(code=1)
    typer.echo(f"OK: {len(nodes)} nodes, {len(edges)} edges")


@app.command()
def build():
    nodes = load_nodes(DATA)
    edges = load_edges(DATA)
    out = ROOT / "build"
    for view in ("all", "money", "influence", "decision"):
        write_json(out / f"{view}.json", cytoscape_payload(nodes, edges, view))
    typer.echo(f"Built Cytoscape payloads in {out}")


@app.command()
def serve(host: str = "127.0.0.1", port: int = 8000):
    uvicorn.run("campaign_graph.api:app", host=host, port=port, reload=False)
