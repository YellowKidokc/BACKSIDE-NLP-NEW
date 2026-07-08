# falsification.station

**ST_006** | Core NLP Pipeline Station

## Purpose

Test claims for falsifiability, generate kill conditions

## NLP Model

- **Primary:** `M07_fact_verify`
- **Alternative:** `M06_llm`

## Existing Code Reference

`fact-verifier.station`

## Notes

For each load-bearing claim: generate explicit kill condition, evidence bar, falsification test. LLM reasoning required.

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
