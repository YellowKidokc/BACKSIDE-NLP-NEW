# graph-linker.station

## Purpose
Takes section vectors + claims and produces edge candidates for the knowledge graph. Generates typed edges: claim overlap, variable overlap, contradiction, citation linkage, thematic similarity.

## Input
- Section vectors (output of sbert-embedder)
- Claim packets (output of claim-extractor)
- Existing graph state (optional, from postgres-sync)

## Output
- Edge list: { source_section_id, target_section_id, edge_type, weight, evidence }
- Node candidates for new graph entries
- Postgres-ready payload

## Model Dependencies
- 02_embedder (cosine similarity for thematic edges)
- 03_contradiction (NLI for contradiction edges)
- 09_claim_extract (claim overlap detection)

## Workflow Lanes
- 09_GRAPH_LINKS (primary)
- Brain Layer (downstream consumer)

## Status: SKELETON — needs implementation

## Notes
Edge types to support:
- THEMATIC_SIMILARITY (cosine > threshold)
- CLAIM_OVERLAP (shared claim structure)
- VARIABLE_OVERLAP (shared chi variables)
- CONTRADICTION (NLI contradiction score)
- CITATION (explicit reference)
- LAW_FAMILY (same Law referenced)
- CROSS_DOMAIN (physics<->theology bridge)
Must be idempotent — running twice produces same edges.
