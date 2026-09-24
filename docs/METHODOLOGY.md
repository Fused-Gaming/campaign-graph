# Methodology

## Evidence hierarchy

| Confidence | Meaning |
|---|---|
| A | Primary government or official record |
| B | Organization's own record |
| C | Reputable secondary source |
| D | Unverified lead |

Confidence describes the source, not the moral or legal significance of the relationship.

## Verification state

- `DOCUMENTED`: the source supports the precise edge being drawn.
- `INFERRED`: analytically inferred from documented facts but not directly stated by the record.
- `UNRESOLVED`: plausible lead but insufficient evidence to assert the relationship.
- `CONTRADICTED`: documentary evidence cuts against the assertion.

## Entity resolution

Never merge records based only on a person's name. Prefer stable filing/entity IDs, committee IDs, EINs, bar numbers, official corporation identifiers, or multiple independent discriminators such as employer + occupation + city/ZIP + middle initial.

## Money versus access

A money edge requires evidence of an actual transfer. Access/influence edges describe non-financial relationships such as lobbying, meetings, board service, employment, FPC assignments, endorsements, and vendors. Never convert access into money.

## Government votes

Permitted states include `VOTED_YES`, `VOTED_NO`, `ABSTAINED`, `RECUSED`, `ABSENT`, and `PRESENT_NO_RECORDED_VOTE`. If the record does not establish one, leave the relationship unresolved.

## Temporal analysis

Temporal analysis may emit only `TEMPORAL_CORRELATION_REQUIRES_INVESTIGATION`. Temporal proximity is not causation and is not evidence of quid pro quo by itself.

## Hypothesis tests

Potentially concerning patterns should be framed as explicit tests. Allowed outcomes are `SUPPORTED`, `PARTIALLY_SUPPORTED`, `NOT_SUPPORTED`, and `INSUFFICIENT_EVIDENCE`. These statuses apply to the narrowly defined evidentiary hypothesis only.

## Contradictory evidence

Researchers should actively look for refunds, reattributions, recusals, absences, votes against an alleged beneficiary, transactions after a decision, public procurement procedures, competing bidders, pre-existing policy commitments, evidence of no communication, evidence of no financial interest, ordinary market explanations, and false entity matches.
