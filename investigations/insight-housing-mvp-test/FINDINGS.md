# Findings memo: Insight Housing / BRIDGE Housing / Lateefah Simon MVP investigation

**Status:** in progress, evidence-first pipeline validation. **This memo reflects the record as of 2026-09-26 and will go stale as the underlying JSON ledgers change — treat it as a snapshot, not the source of truth. The JSON files in this directory are canonical; if this memo and a JSON file disagree, the JSON file is right.**

## What this is

This package tests the campaign-graph pipeline end to end against two real, independently identifiable entities — Insight Housing (a Berkeley nonprofit) and Rep. Lateefah Simon (U.S. House, CA-12) — and a working assumption that "Bridge" in the parent investigation (fused-gaming/campaign-graph#2) refers to BRIDGE Housing Corporation, a San Francisco-based affordable-housing developer. **That assumption is unconfirmed** — see Unresolved Questions.

## Facts (source-backed, not in dispute)

- **Insight Housing**: 501(c)(3) nonprofit, EIN 94-2979073, exempt since Feb. 1986, headquartered at 2855 Telegraph Ave Ste 601, Berkeley, CA 94705-1161. Formerly named Berkeley Food and Housing Project. FY2023 revenue $23,079,014. (`nodes.json`, `identity_resolution.json`, `financials.json`)
- **BRIDGE Housing Corporation**: 501(c)(3) nonprofit, EIN 94-2827909, exempt since 1983, headquartered at 350 California St Ste 1600, San Francisco, CA 94104-1429. FY2023 revenue $78,595,410. Current President & CEO: Ken Lombard. Current General Counsel: Hallock Svensk. (`nodes.json`, `addresses.json`, `roles.json`, `financials.json`)
- **Rep. Lateefah Simon**: U.S. Representative for CA-12, took office 2025-01-03. FEC candidate ID H4CA12154. Principal campaign committee: LATEEFAH FOR CONGRESS, FEC ID C00834291. (`nodes.json`, `events.json`)
- **Federal funding**: Insight Housing has received 14 federal grant/cooperative-agreement awards (~$50M total, 2017–2026) from the VA, DOL, and HUD. BRIDGE Housing Corporation has received 2 Treasury awards ($12.7M total, 2019 and 2022), consistent with CDFI Fund Capital Magnet Fund grants. All are standard competitive/formula programs scored by agency staff. (`grants.json`)

## Checked and not found

Every item below was checked against an official, primary-source system directly (not a secondary aggregator), with the exact query preserved in `unresolved_leads.json` for reproducibility:

- **No FEC-itemized campaign contribution** to Rep. Simon's committee from either organization, their known officers, or an affiliated PAC.
- **No FEC-registered committee/PAC** affiliated with either organization.
- **No Oakland lobbying activity** (client relationship, official contact, or matter) naming either organization in the city's official Public Ethics Commission disclosure data.
- **No congressional decision-maker or CA-12-specific involvement** in any of the 16 federal awards found — all are agency-scored, not member-decided.

## Correlation flagged, and why it doesn't hold up

One HUD award to Insight Housing (CA2234L9T022300) starts 2025-10-01, after Rep. Simon took office. The gap is 271 days — outside every proximity window this package defines (7/30/90/180 days) — and HUD Continuum of Care awards follow an annual, agency-scored cycle that predates her tenure by years for this same organization. `temporal_analysis.json` records this explicitly as `correlation_only` and concludes it does not support any relationship. This is the single timing question the investigation has surfaced, and it resolves toward "ordinary process," not toward a lead.

## Unresolved (genuinely open, not just unresearched)

1. **Which "Bridge" issue #2 means.** This package assumed BRIDGE Housing Corporation as the most plausible referent given the shared Bay Area/housing context, but this has not been confirmed by the person who opened #2. Everything BRIDGE-Housing-specific in this package inherits that assumption's uncertainty.
2. **CA Secretary of State entity numbers** for both organizations — CA SoS's business search and OpenCorporates are both unreachable from this environment (JS-driven form; hard bot-block respectively). Needs a human with browser access.
3. **Individual officer/director names (IRS Form 990 Part VII)** for Insight Housing, and beyond the two already-sourced BRIDGE Housing officers — the actual PDF filings return HTTP 403 from ProPublica's download endpoint even though the JSON metadata API works, and the public IRS bulk-data S3 bucket returned zero keys. Needs a human to download a 990 directly, or a different bulk-data source.
4. **CA state and City of Berkeley lobbying disclosures** — only Oakland's has been checked.
5. **Congressional appropriations/earmark records for CA-12**, and **City of Berkeley grant/contract records** for Insight Housing — not yet checked at all.

## Explicitly not established (and this investigation should not imply otherwise)

- No improper relationship, coordination, or influence between any of these entities and Rep. Simon.
- No violation of any framework in `rules_ledger.json` — that ledger identifies frameworks that *would* apply *if* a fact triggering them is documented; none has been.
- No conclusion about "Bridge" at all, pending item 1 above.

## What would change this memo

Per `investigation.json`'s hypotheses, any of the following would warrant re-opening a hypothesis: a primary-source contribution record under a different employer-name spelling or from an unlisted officer/board member; a CA state or local disclosure naming either organization; a congressional appropriations record naming Insight Housing or BRIDGE Housing for CA-12; or confirmation (or correction) of the "Bridge" identity assumption itself.
