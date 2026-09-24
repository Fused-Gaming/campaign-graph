from __future__ import annotations

from pathlib import Path
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from campaign_graph.analysis import temporal_correlations
from campaign_graph.graph import cytoscape_payload, dashboard_metrics
from campaign_graph.io import load_edges, load_events, load_nodes

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
WEB = ROOT / "web"
app = FastAPI(title="Campaign Graph API", version="0.1.0")
app.mount("/static", StaticFiles(directory=WEB), name="static")


@app.get("/")
def index():
    return FileResponse(WEB / "index.html")


@app.get("/api/graph")
def graph(view: str = Query("all", pattern="^(all|money|influence|decision)$")):
    return cytoscape_payload(load_nodes(DATA), load_edges(DATA), view)


@app.get("/api/metrics")
def metrics():
    return dashboard_metrics(load_nodes(DATA), load_edges(DATA))


@app.get("/api/timeline")
def timeline():
    return [e.model_dump(mode="json") for e in load_events(DATA)]


@app.get("/api/temporal-leads")
def temporal_leads(days: int = Query(90, ge=1, le=3650)):
    return temporal_correlations(load_edges(DATA), days)
