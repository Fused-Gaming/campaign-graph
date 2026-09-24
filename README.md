# Campaign Graph

Evidence-first, source-available political finance and influence network analysis.

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
9. Named investigations never get hard-coded into the generic engine.

## Stack

- Python 3.11+
- pandas
- NetworkX `MultiDiGraph`
- Pydantic
- FastAPI
- Cytoscape.js
- Node.js 20+ repository tooling
- Rock-Hardened release evidence / attestation gate

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

## Cross-agent development

All coding agents must read `AGENTS.md` first. Tool-specific guidance such as `CLAUDE.md` may add workflow hints but cannot weaken the shared evidence, neutrality, testing, licensing, or entity-resolution rules.

## Investigation packages

The engine is deliberately investigation-agnostic. Named or adjacent investigations belong under:

```text
investigations/<slug>/
```

Each package can provide its own manifest, nodes, edges, sources, events, contribution/lobbying/grant datasets, contradictions, unresolved leads, hypotheses, and findings without changing the core graph implementation.

See `docs/INVESTIGATION_PACKAGES.md` and `schemas/investigation.schema.json`.

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

## Version and release gate

The version in `VERSION`, `package.json`, `pyproject.toml`, and `src/campaign_graph/__init__.py` must match.

```bash
npm run version:check
npm run gate
```

The release gate pins `@h4shed/rock-hardened@1.0.0` and generates/validates release evidence from `CHANGELOG.md`. See `release-contract.config.json`.

## Reference architecture

The project takes inspiration from the pipeline pattern in `AlejoPrietoDavalos/twitter_analysis`: collect persistent records, construct directional relationships, analyze a graph, and render interpretable output. Campaign Graph is a clean-room implementation for public-record evidence and does not copy that project's Twitter-specific code.

See `docs/METHODOLOGY.md`, `GOVERNANCE.md`, `SECURITY.md`, and `CHATGPT_PROJECT_CONTEXT.md`.

## License

Campaign Graph is source-available under the **PolyForm Noncommercial License 1.0.0**. Commercial rights are reserved by Fused Gaming, LLC and require a separate commercial license.

See `LICENSE` and `COMMERCIAL_LICENSE.md`.
