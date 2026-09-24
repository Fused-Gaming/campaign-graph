# CLAUDE.md — Claude-Specific Guidance

Read `AGENTS.md` first. `AGENTS.md` is the canonical cross-agent contract and overrides this file on conflict.

## Repository orientation

- `src/campaign_graph/` — generic Python engine
- `web/` — Cytoscape.js client
- `data/` — canonical empty/default datasets
- `schemas/` — machine-readable schemas
- `investigations/<slug>/` — investigation-specific datasets (when added)
- `docs/` — methodology, licensing, governance, research guidance
- `scripts/` — local repository gates

## Working style

1. Inspect existing schemas and models before adding fields.
2. Preserve backward-compatible evidence semantics where possible.
3. Prefer deterministic transforms over generated narrative.
4. Add tests for entity-resolution and evidence-status behavior.
5. Keep money, access/influence, and government decisions separable.
6. Treat every asserted relationship as a provenance problem.

## Before editing political research data

Ask of each proposed edge:

- What exact relationship is asserted?
- What source proves that exact relationship?
- Is this fact, inference, unresolved lead, or contradiction?
- Is the entity identity resolved strongly enough?
- Is an alternative explanation represented?

If the answer is unclear, do not promote the edge to `DOCUMENTED`.

## Commands

```bash
python -m pytest
python -m compileall src
npm run version:check
npm run gate
```

`npm run gate` invokes the pinned Rock-Hardened release-evidence pipeline through `npx`.

## Handoffs

When another agent will continue the task, leave a concise handoff containing branch, changed files, validations executed, failures, and next steps. Never report a command as passing unless it actually ran.
