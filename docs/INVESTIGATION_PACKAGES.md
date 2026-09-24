# Investigation Packages

Campaign Graph core is investigation-agnostic. Named or adjacent investigations are loaded as data packages rather than encoded into graph logic.

## Directory contract

```text
investigations/<slug>/
├── investigation.json
├── nodes.json
├── edges.json
├── sources.json
├── events.json
├── contributions.csv
├── lobbying.csv
├── grants.csv
├── unresolved_leads.json
├── contradictions.json
└── INVESTIGATION_FINDINGS.md
```

Only files relevant to an investigation are required; empty optional datasets may be omitted.

## Manifest

`investigation.json` identifies the package without changing core code.

Example:

```json
{
  "schema_version": "1.0",
  "slug": "example-investigation",
  "title": "Example Investigation",
  "description": "Neutral description of the research scope.",
  "status": "active",
  "jurisdictions": ["US-CA"],
  "date_range": {
    "start": null,
    "end": null
  },
  "hypotheses": [],
  "entry_nodes": [],
  "tags": [],
  "maintainers": []
}
```

## Core rule

The engine must not contain conditionals such as:

```python
if candidate == "Named Person":
    ...
```

or styling, scoring, labels, or legal conclusions tied to a specific investigation subject.

Anything subject-specific belongs in the package.

## Adjacent investigations

A new investigation should be creatable by adding a new directory and manifest, not by modifying the graph engine.

Possible package scopes include:

- one candidate or committee
- a PAC ecosystem
- a lobbying network
- a procurement decision
- a grant network
- a transit-oriented development project
- a nonprofit/government funding network
- a cross-jurisdiction donor network

Packages may share resolved entities through stable identifiers, but package-specific conclusions and hypotheses remain isolated.

## Hypotheses

Hypotheses are research objects, not conclusions. They should define:

- claim under test
- required factual elements
- evidence supporting
- evidence contradicting
- alternative explanations
- missing records
- status: `SUPPORTED`, `PARTIALLY_SUPPORTED`, `NOT_SUPPORTED`, or `INSUFFICIENT_EVIDENCE`

No package may use hypothesis status as a proxy for guilt, corruption, candidate quality, or political recommendation.

## Portability

Investigation packages should remain plain JSON/CSV/Markdown wherever practical so that they can be:

- reviewed in Git
- exported
- independently audited
- ingested by other graph tools
- regenerated from source records

## Future loader

The intended CLI contract is:

```bash
campaign-graph validate-investigation investigations/<slug>
campaign-graph build --investigation <slug>
campaign-graph serve --investigation <slug>
```

The package loader must validate schemas before adding any edge to a graph.
