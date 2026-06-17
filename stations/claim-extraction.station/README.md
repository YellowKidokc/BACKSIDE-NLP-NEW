# claim-extraction.station

**ST_003** | Core NLP Pipeline Station

## Purpose

Extract all claims from text with section context

## NLP Model

- **Primary:** `M09_claim_extract`

## Existing Code Reference

`claim-extractor.station`

## Notes

Core logic in claim-extractor.station/extract.py. Outputs claim-audit CSV.

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
