# Entity Resolution Notes

## Rules

- Keep each identity distinct until supported by a primary record or multiple reliable corroborating records. Record exact legal name, stable identifier, source, date interval, aliases, and unresolved collisions.
- Names in the target list are scope entries, not verified connections. `nodes.json` and `edges.json` are intentionally empty until schema-compatible records and source-backed claims are ready.

## Protected distinctions

- Bridge Association of REALTORS is distinct from BRIDGE Housing Corporation.
- A “Bridge PAC”/Building Relationships in Diverse Geographic Environments PAC is a separate committee unless official filings establish otherwise.
- Berkeley Food & Housing Project / Insight Housing: the organization's current contact page says “formerly Berkeley Food & Housing Project.” Verify continuity against legal filings/EIN before canonical merging.
- Nicole M. Egan and Nicole Marie Egan may be a name variant; identity requires official records.
- Nicole Egan and Calleene Egan: relationship status UNRESOLVED; do not infer kinship.
- Suite 600 and Suite 601 are separate address strings. A shared street/building is not a shared office or organizational relationship.
