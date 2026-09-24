# ChatGPT Project Context — Campaign Graph

## Canonical repository

- Repository: `Fused-Gaming/campaign-graph`
- Distribution model: public source-available tooling
- License: PolyForm Noncommercial 1.0.0; commercial rights reserved by Fused Gaming, LLC
- Core engine must remain politically neutral and investigation-agnostic.

## Purpose

Campaign Graph is an evidence-first graph engine for public-record research involving campaign contributions, PACs, lobbying contacts, grants, contracts, government meetings/votes/decisions, board/employment/vendor relationships, property/address relationships, and source documents.

The software must be equally capable of documenting facts consistent with an improper-influence theory and facts that weaken, contradict, or disprove it.

## Cross-agent contract

All coding/research agents must read `AGENTS.md` first. `AGENTS.md` is the canonical cross-agent contract. Tool-specific files such as `CLAUDE.md` may add workflow hints but cannot weaken the evidence, neutrality, entity-resolution, security, licensing, testing, or handoff rules.

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
14. The engine does not encode accusations or legal conclusions not established by evidence satisfying the relevant elements.
15. Existing source evidence should be append-only and never silently rewritten.
16. Named investigations must not be hard-coded into generic engine logic.

## Evidence state

Verification: `DOCUMENTED`, `INFERRED`, `UNRESOLVED`, `CONTRADICTED`.

Confidence: `A` primary government/official, `B` organization record, `C` reputable secondary, `D` unverified lead.

## Architecture

Core stack: Python 3.11+, pandas, NetworkX `MultiDiGraph`, FastAPI, Cytoscape.js, Pydantic.

Repository tooling: Node.js 20+, synchronized version gate, `CHANGELOG.md`, and Rock-Hardened release evidence/attestation.

Canonical datasets: `nodes.json`, `edges.json`, `sources.json`, `events.json`, `contributions.csv`, `lobbying.csv`, `grants.csv`, `unresolved_leads.json`.

Views: all evidence, money flow, influence/access, government decisions, timeline.

## Investigation packages

Investigation-specific research is a plugin/data package, not core code.

```text
investigations/
  <investigation-slug>/
    investigation.json
    nodes.json
    edges.json
    sources.json
    events.json
    contributions.csv
    lobbying.csv
    grants.csv
    unresolved_leads.json
    contradictions.json
    INVESTIGATION_FINDINGS.md
```

`investigation.json` is validated against `schemas/investigation.schema.json`.

A new or adjacent investigation should be creatable by adding a package and source records without modifying the generic graph engine. Packages can cover a candidate, committee, PAC ecosystem, lobbying network, grant network, procurement decision, TOD project, nonprofit/government funding network, or other evidence-backed research scope.

Packages may reuse entities through stable identifiers while keeping package-specific hypotheses and findings isolated.

## Hypothesis testing

Allowed evidentiary outcomes: `SUPPORTED`, `PARTIALLY_SUPPORTED`, `NOT_SUPPORTED`, `INSUFFICIENT_EVIDENCE`. The result applies only to a narrowly defined hypothesis and is not a political rating, endorsement, character judgment, or criminal finding.

## Version and release contract

The following versions must match:

- `VERSION`
- `package.json`
- `pyproject.toml`
- `src/campaign_graph/__init__.py`

Substantive changes update `CHANGELOG.md` under `[Unreleased]`.

Local gates:

```bash
npm run version:check
npm run gate
```

The release gate pins `@h4shed/rock-hardened@1.0.0`. It is intended to generate/verify changelog-derived manifests, SBOM/provenance, and attestations while leaving human approval as the publication gate.

## Licensing

Campaign Graph is source-available, not OSI open source. Noncommercial permissions are governed by PolyForm Noncommercial 1.0.0. Commercial use requires a separate written license from Fused Gaming, LLC. See `LICENSE` and `COMMERCIAL_LICENSE.md`.

## Current foundation

The foundation includes typed node/edge/evidence models, conservative entity resolution, NetworkX graph building, Cytoscape export/API, money/influence/decision views, evidence-status visualization, dashboard metrics, temporal lead detection, validation CLI, data schemas, methodology/findings templates, cross-agent instructions, investigation package schema/docs, governance/security docs, version synchronization, changelog contract, and Rock-Hardened release configuration.

## Next implementation stages

1. generic investigation package loader/validator
2. FEC ingestion
3. Oakland PEC lobbying report ingestion and enumeration
4. FPPC / Cal-Access adapter
5. generic government meeting / roll-call adapter
6. BART / Legistar / Granicus normalization
7. IRS Form 990 / nonprofit identity adapter
8. grants importers
9. address/property normalization
10. source-document registry with hashes/provenance
11. contradiction and unresolved-lead reports
12. reproducible findings generator

## Reference project

The architecture was inspired by the pipeline pattern in `AlejoPrietoDavalos/twitter_analysis`: collect persistent records, construct directional relationships, analyze a graph, and render interpretable output. Campaign Graph is a clean-room implementation for public-record evidence.
