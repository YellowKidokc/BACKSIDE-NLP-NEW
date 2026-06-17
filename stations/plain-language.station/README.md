# plain-language.station

**ST_002** | Core NLP Pipeline Station

## Purpose

Rewrite content at multiple reading levels (easy / standard / academic)

## NLP Model

- **Primary:** `M06_llm`

## Existing Code Reference

`readability-rewriter.station`

## Notes

LLM-based rewrite at 3 levels. Existing prompt in readability-rewriter.station/prompt.md.

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
