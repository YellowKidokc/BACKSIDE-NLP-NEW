# exec-summary.station

**ST_001** | Core NLP Pipeline Station

## Purpose

Generate executive summary of a paper or article

## NLP Model

- **Primary:** `M01_summarizer`
- **Alternative:** `M13_bart_summarizer`

## Existing Code Reference

New station — no prior implementation.

## Notes

Produces 3-5 sentence executive summary plus key claims list. Can use BART (local) or LLM (Ollama/OpenAI).

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
