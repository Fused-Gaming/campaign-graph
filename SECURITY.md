# Security Policy

## Supported versions

Until the first stable release, only the current default branch and active release-candidate branch are supported.

## Reporting vulnerabilities

Please report security vulnerabilities privately to the repository maintainers rather than opening a public issue containing exploit details, credentials, private records, or sensitive personal information.

## Secrets

Never commit:

- API keys
- OAuth tokens
- cookies or session material
- private signing keys
- database credentials
- private records obtained under restricted access

Use environment variables or local secret stores.

## Research-data safety

Campaign Graph is designed for public-record research. Public availability does not automatically make every datum appropriate to republish.

Contributors should:

- minimize personal information to what is relevant to entity resolution or the documented relationship
- avoid publishing unnecessary home addresses, personal phone numbers, private email addresses, or family details
- prefer official/professional records over people-search aggregators
- avoid turning unresolved identity matches into asserted relationships
- preserve evidence provenance without republishing sensitive source content unnecessarily

## Supply-chain gate

Release evidence is produced through Rock-Hardened. The gate records source/version metadata, manifests, SBOM/provenance where supported, and attestations. These artifacts establish traceability; they are not a warranty that the software is secure.

Run:

```bash
npm run gate
```

before release or merge when the gate is available.

## Dependency policy

New dependencies should be:

- actively maintained where practical
- pinned or constrained intentionally
- license-compatible with the repository distribution model
- added only when their functionality justifies supply-chain risk

## Evidence integrity

Do not alter original source evidence to remove inconvenient or contradictory facts. Derived records should preserve source identifiers and be reproducible from the underlying source material.
