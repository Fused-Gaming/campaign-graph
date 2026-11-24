# Campaign Graph Roadmap

This roadmap converts the project scope in #13 into versioned release milestones. Dates are target windows, not promises. A release slips rather than bypassing evidence, testing, licensing, version, or Rock-Hardened gates.

## Current state

Current release line: `0.1.x`

`0.1.0` established the evidence-first graph foundation, cross-agent rules, source-available licensing, investigation package convention, initial Cytoscape/FastAPI graph views, and release/version contracts.

## Release schedule

| Version | Target | Theme | Exit criteria |
| --- | --- | --- | --- |
| **0.2.0** | **2026-12-05** | Investigation Runtime | Generic package loader, package validation, investigation-aware CLI/API, multi-package integration tests, restored release gate |
| **0.3.0** | **2027-01-15** | Public-Record Ingestion | Reusable FEC, Oakland PEC, FPPC/Cal-Access, Legistar/Granicus, nonprofit/grant/address adapters |
| **0.4.0** | **2027-02-15** | Evidence Workbench | Provenance registry, contradiction and entity-resolution reports, unresolved queue, investigation-aware UI and evidence filters |
| **0.5.0** | **2027-03-15** | Reproducible Public Packages | Findings generation, source hashing, public-package metadata, timeline/report exports, adapter hardening |
| **1.0.0** | **2027-04-15** | Stable Public Release | Stable package/schema contract, documented migrations, protected release workflow, reproducible end-to-end investigation builds |

## 0.2.0 — Investigation Runtime

**Goal:** make the documented `investigations/<slug>/` architecture executable without named-case core logic.

Tracked work:

- #14 — generic investigation package loader and CLI/API selection
- #15 — version and validate the complete investigation package schema surface
- #16 — repair release-contract CI, CodeQL failures, and protect `main`

Release requirements:

- `campaign-graph validate-investigation <path-or-slug>`
- `campaign-graph build --investigation <slug>`
- `campaign-graph serve --investigation <slug>`
- at least two unrelated packages load through unchanged core logic
- cross-reference validation for nodes, edges, sources, hypotheses, and entry nodes
- malformed packages fail safely
- required CI/release checks pass
- `main` protected by required checks/review rules

## 0.3.0 — Public-Record Ingestion

**Goal:** make investigations primarily data/configuration work rather than hand-built one-off research transformations.

Tracked work:

- #17 — reusable FEC ingestion adapter
- #18 — reusable Oakland PEC lobbying report enumerator/parser
- #19 — reusable FPPC / Cal-Access adapter
- #20 — generic Legistar/Granicus government-decision and roll-call adapter
- #22 — nonprofit identity, Form 990, grant/award, and address normalization adapters

Release requirements:

- adapters are ID/config driven and contain no named-investigation conditionals
- raw record IDs and source URLs survive normalization
- money edges require documented transfer evidence
- vote states never infer participation from membership/attendance
- donor/person merges remain conservative
- deterministic fixtures cover amendments, refunds, missing roll calls, aliases, adjacent addresses, and unresolved grant summaries

## 0.4.0 — Evidence Workbench

**Goal:** expose the evidence model as an auditable research interface rather than only a graph renderer.

Tracked work:

- #21 — provenance registry, contradiction/entity-resolution reports, and investigation-aware UI

Release requirements:

- investigation selector
- all-evidence, money, influence/access, decision, and timeline views
- confidence and verification-status filters
- source/provenance panel for every asserted edge
- contradiction report
- unresolved-lead queue
- entity-resolution audit report
- documented-money totals exclude inferred/unverified amounts

## 0.5.0 — Reproducible Public Packages

**Goal:** make a reviewed investigation exportable and independently auditable.

Planned capabilities:

- reproducible findings generator
- source-document hashes and acquisition metadata
- public package manifest with scope, review date, methodology, limitations, and license
- deterministic timeline/report exports
- evidence-table export
- migration tooling for package/schema evolution
- adapter replay from fixtures or preserved source snapshots where licensing permits
- publication checklist enforcement

New issues should be created as these capabilities become implementation-ready rather than hard-coding them into existing case packages.

## 1.0.0 — Stable Public Release

**Goal:** declare the generic investigation platform contract stable enough for external noncommercial use.

Release requirements:

- investigation package/schema compatibility policy documented
- stable CLI/API for validate/build/serve
- generic adapters have fixture-backed tests
- no named investigation required by core tests
- end-to-end build succeeds for multiple investigation packages
- provenance, contradiction, unresolved, entity-resolution, money, influence, decision, and timeline outputs are reproducible
- required release/version/security checks pass
- `VERSION`, `package.json`, `pyproject.toml`, and Python `__version__` synchronized
- release artifacts generated by the pinned Rock-Hardened gate or an explicitly approved equivalent

## Scheduling policy

1. Evidence correctness and provenance outrank schedule.
2. No version ships solely because its target date arrives.
3. A milestone may move later if required checks or primary-source handling are incomplete.
4. Investigation-specific research may continue in parallel, but it must not block or distort generic engine design.
5. New generic capabilities should be added to this roadmap only when they are reusable across adjacent investigations.
6. Every meaningful release PR updates `CHANGELOG.md` and records the checks actually run.

## Scope boundary

Campaign Graph remains investigation-agnostic. Named cases live under `investigations/<slug>/`.

The roadmap tracks reusable capabilities. It does not encode political conclusions, allegations, or case-specific assumptions into the engine.
