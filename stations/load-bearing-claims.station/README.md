# load-bearing-claims.station

**ST_005** | Core NLP Pipeline Station

## Purpose

Identify structurally load-bearing claims vs rhetoric/narrative/metadata

## NLP Model

- **Primary:** `M06_llm`

## Existing Code Reference

`mda-citation-spine.station/claim_inventory.py (LOAD_BEARING_SECTION_WORDS, MODEL_CLAIM_TERMS)`

## Notes

Separates claims into PAPER_CLAIM_QUEUE, CITATION_FACT_QUEUE, REVIEW_QUEUE, PARK. Key logic already in claim_inventory.py classify() function.

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
