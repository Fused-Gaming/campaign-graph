# Campaign Graph

Evidence-first, open-source political finance and influence network analysis.

Campaign Graph turns public records into an auditable, typed graph of campaign contributions, PAC transfers, lobbying contacts, grants, contracts, government decisions, board/employment relationships, addresses, source documents, and unresolved research leads.

> **Association is not wrongdoing. Every graph edge must be backed by evidence and preserve its source.**

The engine is designed to test hypotheses in both directions: it can surface evidence consistent with an improper-influence theory while also preserving contradictory evidence, alternative explanations, recusals, absent votes, refunds, and other facts cutting against a theory.

## Core design rules

1. Evidence before edges.
2. Transactions remain atomic.
3. Entity resolution never merges people on name alone.
4. Money and access are separate graph views.
5. Unknown stays unknown.
6. `DOCUMENTED`, `INFERRED`, `UNRESOLVED`, and `CONTRADICTED` are visually distinct.
7. Every significant conclusion must be reproducible from source records.
8. Political conclusions are not encoded in the software.

## Stack

- Python 3.11+
- pandas
- NetworkX `MultiDiGraph`
- Pydantic
- FastAPI
- Cytoscape.js

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
campaign-graph validate
campaign-graph build
campaign-graph serve
```

Then open `http://127.0.0.1:8000`.

## Data model

Canonical datasets live under `data/`:

- `nodes.json`
- `edges.json`
- `sources.json`
- `events.json`
- `contributions.csv`
- `lobbying.csv`
- `grants.csv`
- `unresolved_leads.json`

Investigation-specific data should eventually live under `investigations/<slug>/` and must not be hard-coded into the generic engine.

## Evidence model

Confidence:

- `A` — primary government/official record
- `B` — organization's own record
- `C` — reputable secondary source
- `D` — unverified lead

Verification status:

- `DOCUMENTED`
- `INFERRED`
- `UNRESOLVED`
- `CONTRADICTED`

## Views

- all evidence
- money flow
- influence/access
- government decisions
- timeline

Temporal proximity may produce only the research flag `TEMPORAL_CORRELATION_REQUIRES_INVESTIGATION`; it does not produce a causation finding.

## Reference architecture

The project takes inspiration from the pipeline pattern in `AlejoPrietoDavalos/twitter_analysis`: collect persistent records, construct directional relationships, analyze a graph, and render interpretable output. Campaign Graph is a clean-room implementation for public-record evidence and does not copy that project's Twitter-specific code.

See `docs/METHODOLOGY.md` and `CHATGPT_PROJECT_CONTEXT.md`.

## License

MIT
