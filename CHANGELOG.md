# Changelog

All notable changes to Campaign Graph are documented here.

The format follows Keep a Changelog-style categories and the repository release gate requires an `[Unreleased]` section.

## [Unreleased]

### Added

- (Work toward 0.2.0 Investigation Runtime will be recorded here)

### Changed

### Fixed

## [0.1.1] — 2026-11-24

### Added

- Added a versioned `ROADMAP.md` with issue-linked release targets from 0.2.0 through 1.0.0.
- Added a money-flow (Sankey) view prototype: `docs/MONEY_FLOW_SPEC.md`, `schemas/money_flow.schema.json`, a `scripts/build_money_flow.py` transform script, generated `investigations/insight-housing-mvp-test/money_flow.json`, and a standalone D3/d3-sankey UI at `web/money_flow/index.html`. Not wired into the existing Cytoscape app or engine. The transform script fails loudly (rather than fabricating a date, guessing a source URL, silently dropping money, or silently merging two entities under one id) whenever committee-totals data doesn't match its known shape, and rejects negative amounts instead of passing them through un-validated; covered by `tests/test_money_flow.py`.

### Changed

- README now links the versioned project roadmap.

## [0.1.0] — 2026-11-24

### Added

- Added a reusable investigation package template and a source-indexed East Bay Housing / REALTOR / Political Finance / TOD investigation scaffold with documented findings and unresolved leads.
- Evidence-first graph foundation with typed nodes, edges, events, source evidence, and Cytoscape views.
- Cross-agent operating framework through `AGENTS.md` and `CLAUDE.md`.
- Canonical version synchronization gate.
- Rock-Hardened release evidence and attestation tooling.
- Investigation package architecture for reusable, adjacent investigations without core hard-coding.

### Changed

- Licensing changed from MIT to PolyForm Noncommercial 1.0.0 with commercial rights reserved by Fused Gaming, LLC.
