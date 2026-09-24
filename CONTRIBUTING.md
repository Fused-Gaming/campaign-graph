# Contributing

Campaign Graph welcomes adapters for public-record systems, campaign-finance APIs, lobbying registries, meeting systems, grants databases, records-request exports, and reusable investigation packages.

Before contributing, read:

- `AGENTS.md`
- `GOVERNANCE.md`
- `SECURITY.md`
- `docs/METHODOLOGY.md`
- `docs/INVESTIGATION_PACKAGES.md`

## Non-negotiable data rules

- Preserve source URLs and official record IDs.
- Do not merge people on name alone.
- Do not promote `UNRESOLVED` edges to `DOCUMENTED` without evidence.
- Do not infer financial transfers from access relationships.
- Do not infer a vote from membership on a board.
- Do not transform donor tiers into invented dollar amounts.
- Do not silently mutate original evidence records.
- Add contradictory evidence when found.
- Keep investigation-specific logic out of the generic engine.

PRs adding factual datasets should identify the primary source and explain entity-resolution decisions.

## Investigation contributions

New or adjacent investigations belong under `investigations/<slug>/` and should conform to `schemas/investigation.schema.json`. A new investigation should not require modifying core graph logic unless it exposes a genuinely generic capability gap.

## Change and release contract

Substantive PRs update `CHANGELOG.md` under `[Unreleased]`.

Before requesting review, run when available:

```bash
python -m pytest
python -m compileall -q src
npm run version:check
npm run gate
```

Do not report checks as passing unless they were actually run.

## Contribution and licensing terms

By submitting a contribution, you represent that you have the right to submit it and agree that the contribution may be distributed as part of Campaign Graph under the repository's licensing model.

Campaign Graph is source-available under PolyForm Noncommercial 1.0.0, with commercial rights reserved by Fused Gaming, LLC. See `LICENSE` and `COMMERCIAL_LICENSE.md` before contributing.
