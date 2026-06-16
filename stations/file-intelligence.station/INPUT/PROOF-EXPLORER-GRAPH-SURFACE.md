# Proof-Explorer — Graph Surface (consumer contract)

**File:** `proof-explorer-fp-005-enhanced.html`
**Built:** 2026-05-31 · visual surface only (JSON-only, no backend/orchestrator)
**Backup of pre-graph version:** `proof-explorer-fp-005-enhanced.html.bak-20260531-graphsurface`

The page is the **consumer**. The Treaties workflow is the **producer**
(`POST /exports/structured` → `exports/json/`). Contract: `treaties.knowledge_graph.v0`.

## What the page reads (manifest-driven)

It loads **one manifest**, then loads exactly what the manifest's `files` block names:

```
graph-contract-latest.json            ← manifest (read first)
  files.series_knowledge_graph   → knowledge-graph-latest.json   (Whole-corpus scope)
  files.paper_knowledge_graphs[] → paper-{id}-knowledge-graph-latest.json (Per-paper scope, lazy)
  files.structured_export        → latest.json   (papers[].uuid_metadata.series, axiom_mappings)
  files.seven_q_claims           → seven-q-claims-latest.json     (loaded; light enrichment)
```

Graph file shape (already matches the live exporter — verified, 0 dropped edges):
```
nodes: { id:"paper:5"|"claim:96"|"axiom:2"|"evidence:95"|"category:x"|"keyword:y"|"series:all",
         type:"Paper"|"Claim"|"Axiom"|"Evidence"|"Category"|"Keyword"|"Series", label, ... }
edges: { source, target, type:"PAPER_HAS_CLAIM"|"CLAIM_SUPPORTED_BY_EVIDENCE"|..., strength? }
```

## Where the JSON must live (deployment)

The HTML is at `X:\Backside\`; the JSON is emitted to `…\Treaties\exports\json\`.
`fetch()` needs the files reachable from the page over **http://** (file:// is blocked).
Point the page at the data in any one of these ways:

1. **Meta tag** (simplest): add to `<head>`
   `<meta name="graph-data-base" content="/exports/json/">`
2. **Global**: `<script>window.GRAPH_DATA_BASE = "https://host/exports/json/";</script>`
3. **Co-locate**: copy `exports/json/*` next to the HTML (base defaults to same folder).
4. **Inline** (fully standalone snapshot): embed any file as
   `<script type="application/json" id="data-file:graph-contract-latest.json">…</script>`
   (and `id="data-file:knowledge-graph-latest.json"`, etc.). Inline always wins over fetch.

No manifest present → the page falls back to generic `graph.json` /
`graph_nodes.json` / `graph_edges.json` (+ inline) for standalone use.

## UI

- **Top-right launcher** (collapsible): three view buttons + live status dots
  (`✓` loaded · `◐` inline · `✗` missing · `—` optional) and a contract/papers line.
  It launches — it is not the graph.
- **Full-screen overlay** ("its own page"): Cytoscape canvas, view tabs
  (Knowledge / Dependencies / Understand-Anything), **scope toggle
  (Per-paper → Series → Whole-corpus)**, paper picker, search, fit, node-details
  panel, legend, Esc to close.
  - Per-paper → the `paper-{id}` graph. Series → corpus filtered by
    `uuid_metadata.series` via **directed** BFS (no cross-series leak; verified).
    Whole-corpus → full `knowledge-graph-latest.json`.
- Existing placeholders wired to launch the overlay: nav **Graph** link,
  **Axioms** panel, **CKG** panel, right-sidebar **Dependency Graph** (Expand).
- FP-005's own static panels are left intact unless `latest.json` describes this
  paper by uuid (it doesn't, so they stay as authored).

## Understand-Anything view

Optional. The contract marks the `understand_anything` adapter as
"available_not_ingested", so the view shows a clear empty state until that
adapter emits `nodes/edges` (it reads the same normalized shape).

## Verified against live exports (run 20260601T012455Z)

- Manifest parse ✓ · corpus 162n/392e, **0 dropped edges** ✓ · all per-paper graphs ✓
- Series scope: TH → papers 1,2,3,5 · GTQ → paper 4 · **no leak** ✓
- `node --check` on the module ✓
