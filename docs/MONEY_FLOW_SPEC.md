# Money-flow (Sankey) view — spec

Status: **draft, under review**. Nothing here is wired into the main Cytoscape app yet; this
describes a standalone, additive view for tracing aggregate or itemized money flow between
entities (committees, PACs, vendors, foundations, wallets — anything with an `amount` moving
between two parties).

## Why a separate view, not a new Cytoscape layer

Cytoscape graphs in this repo represent *relationships* (an edge = "this fact is asserted, with
this source"). A Sankey diagram represents *magnitude of flow* (a link's width = dollars), which
needs different visual grammar (ribbons, not lines) and different data shape (flows must net out
per node, or the diagram misleads). Keeping it separate also means a confidence-gap in flow data
can't accidentally leak into the relationship graph's edge set.

## Data shape: the money-flow edge

One normalized record per aggregated or itemized flow. This is deliberately a flat, narrow shape
so every flow edge is independently auditable — no inferred multi-hop chains are allowed into this
file; the transform script only aggregates real recorded transactions between two *directly*
recorded parties.

```jsonc
{
  "id": "flow-<slug>-<n>",                 // stable id, unique within one flow file
  "source_id": "committee-c00834291",      // node id (see node registry below)
  "target_id": "category-operating-expenditures",
  "amount_usd": 840533.32,
  "flow_type": "disbursement",             // contribution | disbursement | refund | grant | transfer
  "period_start": "2025-01-01",
  "period_end": "2026-06-30",
  "transaction_count": null,               // null when this is an aggregate total, not itemized rows
  "confidence": "A",                       // same A-D scale as schemas/contribution.schema.json
  "source_url": "https://api.open.fec.gov/v1/committee/C00834291/totals/",
  "source_title": "FEC committee totals API",
  "accessed_date": "2026-10-04",
  "note": "Aggregate figure from committee totals, not itemized Schedule B rows."
}
```

Rules enforced by the transform script (not just convention):

- `source_id` and `target_id` must both already exist in the flow file's `nodes` array (below) —
  no implicit node creation from a typo.
- No edge may be synthesized by chaining two other edges (`A->B` + `B->C` does **not** imply
  `A->C` in this file). Multi-hop visual flow comes for free from Sankey layout once both real
  edges exist; it is never pre-computed here.
- `amount_usd` must be `>= 0`. Refunds get their own `flow_type: "refund"` edge in the reverse
  direction rather than a negative number, so link width is never misleading.
- Every edge requires a `confidence` and `source_url` — same bar as every other evidence file in
  this repo. An edge with `confidence: "D"` (unverified lead) must still render, but visually
  de-emphasized (see rendering rules).

## Node registry

A flow file also declares its own small node list, independent of `nodes.json`'s investigation
graph (though `node_id`s should match where the same entity appears in both, to make cross-
referencing easy):

```jsonc
{
  "id": "committee-c00834291",
  "label": "Lateefah for Congress (C00834291)",
  "node_type": "committee",   // committee | pac | vendor | foundation | category | person | org
  "investigation_node_id": null  // optional: the matching id in that package's nodes.json
}
```

`category` nodes (like `category-operating-expenditures`) are allowed for aggregate totals where
the underlying data doesn't give a named counterparty — e.g. FEC committee totals break
disbursements into named buckets (operating expenditures, refunds, other disbursements) without
itemizing every vendor. This keeps the diagram honest about what's actually known: a named vendor
node only appears once a real itemized record names that vendor.

## File location and naming

One flow file per investigation package, alongside its other evidence files:

```
investigations/<slug>/money_flow.json
```

Shape:

```jsonc
{
  "schema_version": "1.0",
  "investigation_slug": "insight-housing-mvp-test",
  "generated_at": "2026-11-24",
  "generated_by": "scripts/build_money_flow.py",
  "nodes": [ /* node registry entries */ ],
  "edges": [ /* money-flow edge entries */ ]
}
```

## Rendering rules (for the prototype and any later production view)

- Link width proportional to `amount_usd`, scaled within one diagram (not across diagrams).
- Link color/opacity by `confidence`: A/B full opacity, C medium, D low + dashed stroke if the
  renderer supports it — a D-confidence flow should visually read as "reported, not verified,"
  never as equal-weight to an FEC-sourced total.
- Hover/tooltip shows: exact amount, `flow_type`, period, `confidence`, and a link to `source_url`.
  No flow renders without a visible way to reach its source — this mirrors the rest of the repo's
  evidence-first rule, just applied to a chart instead of a JSON ledger.
- A node with no outgoing edges and no incoming edges from another *named* node (i.e., an
  all-`category` leaf) should be visually marked as a terminus, not implied to go anywhere further.

## What this does NOT do (scope boundary)

- Does not trace cryptocurrency wallets or any blockchain data — there is none in this repo's
  domain (campaign finance, grants, lobbying). The user's blockchain-Sankey reference is the
  inspiration for the *visual grammar*, not a new data source to integrate.
- Does not infer pass-through/conduit relationships. If a future itemized dataset shows a specific
  earmarked/conduit contribution, that gets its own sourced edge with `flow_type` noting it
  explicitly (e.g. `"conduit_contribution"`) — never inferred from two aggregate edges sharing a
  node.
- Does not replace `contributions.json`/`committee_totals.json` as the source of truth; the
  transform script reads those and produces a *view* of them. If the view and the underlying file
  disagree, the underlying file is right (same rule the existing `FINDINGS.md` files already state
  for themselves).

## Open questions for review

1. Should `money_flow.json` be hand-maintained like other evidence files, or always regenerated by
   `scripts/build_money_flow.py` from the canonical ledgers (and therefore gitignored / build
   output)? Current prototype treats it as checked-in, generated output — regenerable, diffable,
   reviewable in a PR like any other evidence change.
2. Do we want itemized per-vendor disbursement flows once `disbursements.json` exists (lane 13 from
   the earlier 18-lane plan), or is the aggregate committee-totals view sufficient for now?
3. Confidence-based rendering (dashed/low-opacity D-confidence links) needs a design-system pass
   once this leaves prototype status — tracked here, not solved by the prototype.
