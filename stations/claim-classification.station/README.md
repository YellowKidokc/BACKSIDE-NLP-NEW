# claim-classification.station

**ST_004** | Core NLP Pipeline Station

## Purpose

Classify extracted claims by type, maturity, and domain

## NLP Model

- **Primary:** `M02_embedder`
- **Alternative:** `deberta-runner (DeBERTa NLI)`

## Existing Code Reference

`classify-documents.station + mda-citation-spine.station/claim_inventory.py`

## Notes

Two-stage: SBERT embedding for similarity, then DeBERTa NLI for maturity labels. Triage logic in claim_inventory.py.

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
