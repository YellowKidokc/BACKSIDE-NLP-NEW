# summarizer.station

## Purpose
Wraps BART summarizer (01_summarizer) into a station interface. Produces faithful reductions with traceability back to source sections.

## Input
- Full document text or individual sections
- Target summary length (short/medium/long)
- Optional: preference bias for detail level, domain emphasis

## Output
- Summary text
- Source span pointers (which sections contributed to which summary sentences)
- Compression ratio

## Model Dependencies
- 01_summarizer (BART Large CNN)
- Optional: 06_llm via Ollama for abstractive summaries

## Workflow Lanes
- Summary Layer (primary)
- 15_SECTION_PACKETS (section-level summaries)
- Session handoff generation

## Status: SKELETON — needs implementation

## Notes
Gate rule: summaries must point back to source chunks or section spans.
Summary should come AFTER claim extraction in the workflow — summarizing before claims washes out structure.
