# contradiction-scan.station

**ST_008** | Core NLP Pipeline Station

## Purpose

Scan for internal contradictions between claims across articles

## NLP Model

- **Primary:** `M03_contradiction`
- **Alternative:** `M08_contradiction_deep`

## Existing Code Reference

`contradiction-detector.station + contradiction-deep.station`

## Notes

Two-pass: shallow DeBERTa NLI scan (M03), then deep LLM analysis on flagged pairs (M08). Cross-article scope.

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
