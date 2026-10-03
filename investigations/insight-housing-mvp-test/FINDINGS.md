# Findings memo: Insight Housing / BRIDGE Housing / Lateefah Simon MVP investigation

**Status:** in progress, evidence-first pipeline validation. **This memo reflects the record as of 2026-10-03 and will go stale as the underlying JSON ledgers change — treat it as a snapshot, not the source of truth. The JSON files in this directory are canonical; if this memo and a JSON file disagree, the JSON file is right.**

## What this is

This package tests the campaign-graph pipeline end to end against real, independently identifiable entities — Insight Housing (a Berkeley nonprofit), Rep. Lateefah Simon (U.S. House, CA-12, formerly a BART director), and a working assumption that "Bridge" in the parent investigation (fused-gaming/campaign-graph#2) refers to BRIDGE Housing Corporation, a San Francisco-based affordable-housing developer. **That assumption is still unconfirmed by #2's author** — see Unresolved Questions — and it now has a second plausible candidate (BRIDGE Housing Corporation - Southern California, confirmed as a subordinate organization of the same entity) and a confirmed false lead (the Bridge Association of REALTORS, a same-name but entirely unrelated trade association).

## Facts (source-backed, not in dispute)

- **Insight Housing**: 501(c)(3) nonprofit, EIN 94-2979073, exempt since Feb. 1986, headquartered at 2855 Telegraph Ave Ste 601, Berkeley, CA 94705-1161. Formerly named Berkeley Food and Housing Project. FY2023 revenue $23,079,014.
- **BRIDGE Housing Corporation**: 501(c)(3) nonprofit, EIN 94-2827909, exempt since 1983, headquartered at 350 California St Ste 1600, San Francisco. FY2023 revenue $78,595,410. President & CEO Ken Lombard.
- **BRIDGE Housing Corporation - Southern California**: EIN 94-3233154, confirmed as a subordinate organization of the above (CauseIQ, corroborated by overlapping executives).
- **Rep. Lateefah Simon**: U.S. Representative for CA-12, took office 2025-01-03. Previously an elected BART (Bay Area Rapid Transit) Board of Directors member, District 7, 2016-2024 (board president from 2020). A March 2022 residency-boundary removal attempt by BART staff was reversed within two weeks after outside counsel found staff lacked the authority; she retained her seat throughout.
- **Federal funding**: Insight Housing has received 16 federal grant/cooperative-agreement awards (~$50M total, 2017-2026) from the VA, DOL, and HUD, all standard competitive/formula programs. BRIDGE Housing Corporation has received 2 Treasury awards ($12.7M, 2019/2022), consistent with CDFI Fund Capital Magnet Fund grants.
- **Bridge Association of REALTORS**: EIN 94-0727300, a 501(c)(6) real estate trade association in Suite 600 at Insight Housing's building — a **distinct, unrelated entity**, not BRIDGE Housing Corporation. Its registered lobbyist, Kiran Shenoy, has a documented 6-year (2020-2026) Oakland lobbying history entirely on local housing-ordinance matters, never mentioning Simon, Insight Housing, or BRIDGE Housing Corporation.

## The one documented institutional link found: BART / North Berkeley TOD

BART's Board of Directors — on which Rep. Simon sat as an elected director from 2016-2024 — authorized an Exclusive Negotiating Agreement with BRIDGE Housing Corporation for a Transit-Oriented Development at the North Berkeley station on 2022-12-01. Insight Housing is reported (not yet confirmed against a primary document) as a co-member of the same development team, "North Berkeley Housing Partners," alongside BRIDGE Housing, EBALDC, and AvalonBay Communities. **This is the first and only documented institutional link between Insight Housing and BRIDGE Housing Corporation found anywhere in this investigation** — everything else treats them as unrelated organizations with only incidental Bay Area geography in common.

This is recorded carefully and should not be over-read: Rep. Simon is included in the event record only because she was one of nine sitting BART directors at the time of a routine, multi-member board vote on a real-estate negotiating framework (not a funding award or final contract). **Her actual presence, vote, or recusal on that specific 2022-12-01 action has not been confirmed** — no roll-call record has been located. This is explicitly the single most load-bearing unconfirmed fact in the entire package.

## REALTOR advocacy lane (Bridge AOR, NAR, CREPAC) — real relationships, none touching Simon or the two nonprofits

- Tia Hunnicutt is NAR's assigned Federal Political Coordinator (advocacy liaison) for CA-12/Rep. Simon — a standard structure every member of Congress has one of. Her own published bio confirms she was Bridge Association of REALTORS' President (2014) and Chair (2019), board member 2010-2023 — substantiating the "Alameda County REALTOR delegation" context raised earlier, but as **history, not a current role** (her current professional home is her own brokerage). She's also a current (2025) member of CREPAC, the California Association of REALTORS' state PAC.
- CREPAC's own stated purpose, per C.A.R.'s materials, is funding **CA state candidates specifically** — not federal ones. A contribution to Rep. Simon's federal committee couldn't come from this exact vehicle; a separate FEC-registered entity would need to exist and be identified. CREIEC (C.A.R.'s independent-expenditure arm) is also not yet confirmed as a federal-level actor. None of this has been checked against actual FEC contribution/IE data yet — blocked on the rate limit below.
- Checked Oakland's Schedule D (contribution solicitations disclosed by lobbyists) directly for any link between Bridge AOR/Shenoy and Simon/Insight Housing/BRIDGE Housing Corporation, in either direction — zero results.

## Checked and not found (unchanged from earlier passes, still holding)

- No FEC-itemized campaign contribution to Rep. Simon's committee (C00834291) from either nonprofit, their known officers, or an affiliated PAC — *though "known officers" has grown substantially since this was first checked; see Unresolved below.*
- No Oakland lobbying activity naming either nonprofit.
- No congressional decision-maker involvement in any of the 16 federal awards found; neither nonprofit appears in Rep. Simon's own FY26/FY27 Community Project Funding (earmark) request pages.
- Neither Berkeley's nor Alameda County's open-data portals have any grant/contract/vendor dataset at all — confirmed by getting real results for broader queries on the same endpoints, not a tooling failure.

## Leadership data: real names found, with honest contradictions preserved

A reliable third-party aggregator (CauseIQ, which republishes dated IRS Form 990 Part VII key-personnel data) substantially deepened officer rosters for Insight Housing, BRIDGE Housing Corporation (and its Southern California subordinate), EBALDC, and the Bridge Association of REALTORS. Two genuine contradictions surfaced and were preserved rather than silently resolved:

1. **Calleene Egan** is CEO per earlier web-search synthesis, but CFO per CauseIQ's dated 990 data.
2. **BRIDGE Housing Corporation's General Counsel**: Hallock Svensk per the org's own site (Sept. 24), Lisa Laffer per CauseIQ (Jan. 2026).
3. (Minor, not a hard contradiction) **BRIDGE Housing - Southern California's CEO**: Ken Lombard and Nadia Sager both listed within days of each other — plausibly an org-wide-president-vs-subsidiary-operational-CEO structure, not confirmed.

None of these new names have yet been cross-checked against FEC contributor data (blocked, see below) — that cross-check is the natural next step once the rate limit clears, and the plan explicitly asked for every discovered name to feed back into that check.

## FEC data lane: blocked, not abandoned

`api.open.fec.gov`'s DEMO_KEY (40 calls/hour) is shared across this environment's proxy and has been exhausted for most of this session. Issue #10 tracks the exact batched call plan (committee totals, full Schedule A/B/E pagination, every newly-discovered officer name as a `contributor_name` check, CREPAC/CREIEC committee resolution). An hourly Routine checks remaining budget and executes whatever batch fits automatically. **Nothing about Rep. Simon's actual campaign finances — receipts, disbursements, independent expenditures — has been directly examined yet.** This is the largest remaining gap in the investigation, not a minor one.

## Explicitly not established (and this investigation should not imply otherwise)

- No improper relationship, coordination, or influence between any of these entities and Rep. Simon. The BART/North Berkeley link is a documented institutional fact about an agency she sat on, not a transaction involving her personally.
- No violation of any framework in `rules_ledger.json`.
- No conclusion about which "Bridge" issue #2 means — now with two plausible BRIDGE Housing Corporation-family candidates (main org, Southern California subordinate) plus one confirmed false lead (Bridge Association of REALTORS).
- No characterization of CREPAC membership, NAR committee roles, or REALTOR advocacy generally as improper — trade-association political activity and advocacy are lawful, routine, and disclosed by design.

## What would change this memo

Per `investigation.json`'s hypotheses (h1-h5): a primary-source contribution record from any of the newly-discovered officer names or the CREPAC/CREIEC family; the BART board's actual 2022-12-01 roll-call vote; confirmation of Insight Housing's North Berkeley Housing Partners membership against a primary document; or confirmation/correction of the "Bridge" identity assumption itself.
