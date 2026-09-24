# ChatGPT Project Context — Campaign Graph

## Canonical repository

- Repository: `Fused-Gaming/campaign-graph`
- Public project type: open-source investigative research tooling
- Core engine must remain politically neutral and investigation-agnostic.

## Purpose

Campaign Graph is an evidence-first graph engine for public-record research involving campaign contributions, PACs, lobbying contacts, grants, contracts, government meetings/votes/decisions, board/employment/vendor relationships, property/address relationships, and source documents.

The software must be equally capable of documenting facts consistent with an improper-influence theory and facts that weaken, contradict, or disprove it.

## Hard rules

1. Association alone is not wrongdoing.
2. Every asserted edge requires evidence.
3. Preserve original source URLs and official record identifiers.
4. Do not merge people based on name similarity alone.
5. Do not merge similarly named organizations without documentary proof.
6. Keep money relationships separate from access/influence relationships.
7. Never draw a money arrow without evidence of an actual transfer.
8. Never infer a vote from board membership or attendance.
9. Unknown vote states remain unresolved until documented.
10. Shared buildings and adjacent suites do not establish shared organizations, coordination, or shared offices.
11. Donor tiers are not exact contribution amounts.
12. Temporal proximity is not causation.
13. Contradictory evidence belongs in the graph.
14. The engine does not label people or organizations corrupt, guilty, criminal, pay-to-play, quid-pro-quo, or otherwise unlawful without underlying evidence satisfying the relevant elements.
15. Existing source evidence should be append-only and never silently rewritten.

## Evidence state

Verification: `DOCUMENTED`, `INFERRED`, `UNRESOLVED`, `CONTRADICTED`.

Confidence: `A` primary government/official, `B` organization record, `C` reputable secondary, `D` unverified lead.

## Architecture

Core stack: Python 3.11+, pandas, NetworkX `MultiDiGraph`, FastAPI, Cytoscape.js, Pydantic.

Canonical datasets: `nodes.json`, `edges.json`, `sources.json`, `events.json`, `contributions.csv`, `lobbying.csv`, `grants.csv`, `unresolved_leads.json`.

Views: all evidence, money flow, influence/access, government decisions, timeline.

## Investigation datasets

Investigation-specific research must not be hard-coded into the generic engine. Preferred structure:

```text
investigations/
  <investigation-slug>/
    nodes.json
    edges.json
    sources.json
    events.json
    contributions.csv
    lobbying.csv
    grants.csv
    unresolved_leads.json
    INVESTIGATION_FINDINGS.md
```

A Bay Area Simon / REALTOR / Insight Housing investigation may be an initial demonstration dataset, but it is a consumer of Campaign Graph rather than part of the product's core assumptions.

## Entity collision warnings

Keep Bridge Association of REALTORS, BRIDGE Housing Corporation, and unrelated organizations/PACs using the word "BRIDGE" separate unless primary evidence proves otherwise. Ambiguous people remain separate until identity is corroborated with stable IDs or multiple independent discriminators.

## Hypothesis testing

Allowed evidentiary outcomes: `SUPPORTED`, `PARTIALLY_SUPPORTED`, `NOT_SUPPORTED`, `INSUFFICIENT_EVIDENCE`. The result applies only to a narrowly defined hypothesis and is not a political rating, endorsement, character judgment, or criminal finding.

## Current foundation

The initial scaffold includes typed node/edge/evidence models, conservative entity resolution, NetworkX graph building, Cytoscape export/API, money/influence/decision views, evidence-status visualization, dashboard metrics, temporal lead detection, validation CLI, data schemas, methodology/findings templates, and unit tests.

## Next implementation stages

1. FEC ingestion
2. Oakland PEC lobbying report ingestion and enumeration
3. FPPC / Cal-Access adapter
4. generic government meeting / roll-call adapter
5. BART / Legistar / Granicus normalization
6. IRS Form 990 / nonprofit identity adapter
7. grants importers
8. address/property normalization
9. source-document registry with hashes/provenance
10. investigation package loader (`--investigation <slug>`)
11. contradiction and unresolved-lead reports
12. reproducible findings generator

## Reference project

The architecture was inspired by the pipeline pattern in `AlejoPrietoDavalos/twitter_analysis`: collect persistent records, construct directional relationships, analyze a graph, and render interpretable output. Campaign Graph is a clean-room implementation for public-record evidence.
