# Contributing

Campaign Graph welcomes adapters for public-record systems, campaign-finance APIs, lobbying registries, meeting systems, grants databases, and records-request exports.

## Non-negotiable data rules

- Preserve source URLs and official record IDs.
- Do not merge people on name alone.
- Do not promote `UNRESOLVED` edges to `DOCUMENTED` without evidence.
- Do not infer financial transfers from access relationships.
- Do not infer a vote from membership on a board.
- Do not transform donor tiers into invented dollar amounts.
- Do not silently mutate original evidence records.
- Add contradictory evidence when found.

PRs adding factual datasets should identify the primary source and explain entity-resolution decisions.
