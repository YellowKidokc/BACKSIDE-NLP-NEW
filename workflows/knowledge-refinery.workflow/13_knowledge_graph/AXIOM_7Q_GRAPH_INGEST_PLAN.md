# Axiom + 7Q Graph Ingest Plan

## Source Workbook

Use the latest reviewed workbook from:

```text
X:\paper-proof-grader\OUTPUT\station-runs\axiom-7q-YYYYMMDD_HHMMSS\axiom-7q-review.xlsx
```

Or resolve the latest run folder from:

```text
X:\knowledge-refinery\10_STATIONS\12_axiom_promotion\LATEST_OUTPUT_POINTER.txt
```

The graph candidate sheets are:

- `Tag Graph Review`
- `Graph Edges`

## Review Contract

Rows with `status=draft` are model or deterministic suggestions.

Rows with `status=accepted` are allowed into the graph.

Rows with `status=rejected` should be preserved for audit but not ingested.

Rows with `status=needs_review` require human review or O3 ranking.

## Minimal Edge Schema

```text
source_id
source_type
relationship_type
target_id
target_type
weight
status
evidence_excerpt
notes
```

## Relationship Types

Recommended starting vocabulary:

- `maps_to`
- `supports`
- `requires`
- `depends_on`
- `tests`
- `falsifies_if`
- `strengthens`
- `contradicts`
- `mentions`

## Next Build

Create a graph-ingest script that reads accepted rows and writes:

```text
X:\knowledge-refinery\20_REGISTRIES\graph.json
```

Do not ingest directly from model output. Ingest only from reviewed workbook
rows.
