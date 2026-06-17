# evidence-map.station

**ST_007** | Core NLP Pipeline Station

## Purpose

Map evidence to claims, identify gaps and unsupported claims

## NLP Model

- **Primary:** `M02_embedder`
- **Alternative:** `M06_llm`

## Existing Code Reference

New station — no prior implementation.

## Notes

New station. Semantic matching (SBERT) between claims and evidence passages. Output: evidence coverage map with gap flags.

## Pipeline Position

```
ST_001 -> ST_002 -> ST_003 -> ST_004 -> ST_005 -> ST_006 -> ST_007 -> ST_008
  exec     plain    claim     classify  load-     falsif   evidence  contradict
  summary  language extract   claims    bearing            map       scan
```

## Standard Folders

- `_inbox/` — inputs land here
- `_outbox/` — JSON artifacts go here
- `_processed/` — archived inputs
- `_logs/` — execution logs
- `_state/` — persistent state
