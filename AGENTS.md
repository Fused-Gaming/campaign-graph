# AGENTS.md — Campaign Graph Cross-Agent Contract

This file is the canonical operating contract for AI coding agents working in this repository. Tool-specific files such as `CLAUDE.md` may add workflow hints, but they MUST NOT weaken or contradict this document.

## Mission

Campaign Graph is a source-available, evidence-first engine for auditable campaign-finance, lobbying, grants, government-decision, contract, organizational, and influence-network analysis.

The engine must support evidence that confirms, weakens, contradicts, or leaves unresolved any investigative hypothesis. It must never encode a preferred political outcome.

## Priority order

1. User instructions for the current task.
2. This `AGENTS.md`.
3. Repository documentation and schemas.
4. Tool-specific guidance such as `CLAUDE.md`.
5. Existing implementation conventions.

If two instructions conflict, stop the conflicting change and preserve the stricter evidence/safety rule.

## Non-negotiable evidence rules

- Association alone is not wrongdoing.
- Every relationship edge requires evidence.
- Preserve source URL, source title, source date when known, accessed date, source type, evidence summary, confidence, and verification status.
- Keep `DOCUMENTED`, `INFERRED`, `UNRESOLVED`, and `CONTRADICTED` distinct.
- Never convert temporal proximity into causation.
- Never convert access into money.
- Never infer a government vote from membership or attendance.
- Never merge people on name similarity alone.
- Never merge similarly named organizations without documentary evidence.
- Never invent transaction amounts from donor tiers, ranges, or descriptions.
- Preserve atomic transactions even when aggregates are generated.
- Contradictory and exculpatory evidence is first-class data.
- Unknown facts remain unknown.

## Political neutrality

Agents may collect and compare documented political records. Agents must not rank candidates, recommend political choices, predict election outcomes, or alter data presentation to favor or disfavor a political actor.

## Architecture boundaries

Core engine code stays investigation-agnostic.

Investigation-specific material belongs under:

```text
investigations/<slug>/
```

Do not hard-code named politicians, organizations, donors, lobbyists, hypotheses, or conclusions into generic graph logic.

## Source hierarchy

Prefer primary records:

1. government/official records
2. organizations' own records
3. reputable secondary sources
4. unverified leads

Secondary sources should normally lead to primary records rather than replace them.

## Entity resolution

A name-only match is never sufficient for a person merge.

Prefer stable identifiers such as:

- FEC committee ID
- EIN
- government entity/filing number
- State Bar number
- official employee ID when public
- exact filing transaction ID

When stable IDs are unavailable, require multiple corroborators such as employer, occupation, city/ZIP, middle name/initial, dates, official biography, or filing context.

Ambiguous entities remain separate and may be linked by an `UNRESOLVED` lead.

## Source preservation

Do not destructively modify original evidence inputs. Normalize into derived datasets while preserving the original record identifier and URL.

Generated or normalized records should be reproducible from source inputs.

## Required validation before committing

Run the narrowest relevant checks plus the repository gate:

```bash
python -m pytest
python -m compileall src
npm run version:check
npm run gate
```

If `@h4shed/rock-hardened` cannot be resolved from npm, report that exact limitation and still run all local non-network checks. Do not silently bypass the release gate.

## Version contract

The following versions must match:

- `VERSION`
- `pyproject.toml` project version
- `package.json` version
- `src/campaign_graph/__init__.py` `__version__`

Version changes require a `CHANGELOG.md` entry.

## Changelog contract

Every substantive PR must update `CHANGELOG.md` under `[Unreleased]`.

Use categories such as:

- Added
- Changed
- Fixed
- Security
- Removed

Release evidence is generated with Rock-Hardened.

## Licensing

The repository is source-available under the PolyForm Noncommercial License 1.0.0 unless a file says otherwise.

Commercial use is reserved and requires a separate license from the licensor. Do not describe this repository as OSI open source.

Do not add dependencies whose license conflicts with the repository's intended distribution without documenting the conflict and obtaining human approval.

## Security

- Never commit secrets, API tokens, private keys, session cookies, or private records.
- Public-record research belongs in the repository only when lawful to redistribute.
- Do not add private personal data merely because it is technically obtainable.
- Avoid people-search aggregator data as final evidence for sensitive relationships.
- Prefer minimum necessary personal information.

See `SECURITY.md`.

## Agent handoff

When leaving work for another agent, record:

- branch
- files changed
- tests run
- unresolved failures
- evidence/schema migrations
- next concrete step

Do not claim tests passed unless they were actually executed.

## Commit discipline

Prefer focused commits. Never rewrite or delete existing evidence to make a narrative cleaner. Do not force-push shared branches unless explicitly instructed.
