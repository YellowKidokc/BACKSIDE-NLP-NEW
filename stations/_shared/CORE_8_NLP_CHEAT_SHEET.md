# Core 8 NLP Pipeline Stations - Cheat Sheet
Generated: 2026-06-16T16:44:04

## Pipeline Sequence

```
ST_001 exec-summary       ->  M01_summarizer / M13_bart_summarizer
ST_002 plain-language      ->  M06_llm
ST_003 claim-extraction    ->  M09_claim_extract
ST_004 claim-classification -> M02_embedder + DeBERTa
ST_005 load-bearing-claims ->  M06_llm (claim_inventory.py logic)
ST_006 falsification       ->  M07_fact_verify + M06_llm
ST_007 evidence-map        ->  M02_embedder + M06_llm
ST_008 contradiction-scan  ->  M03_contradiction + M08_contradiction_deep
```

## NLP Model Registry (X:\05_MODELS\)

| ID  | Model | Used By |
|-----|-------|---------|
| M01 | summarizer | ST_001 |
| M02 | embedder (SBERT) | ST_004, ST_007, sbert-embedder.station |
| M03 | contradiction (DeBERTa NLI) | ST_008, deberta-runner.station |
| M04 | imager | image-processor.station |
| M05 | transcriber | whisper-transcribe.station |
| M06 | llm (Ollama/OpenAI) | ST_002, ST_005, ST_006, ST_007, llm-runner.station |
| M07 | fact_verify | ST_006, fact-verifier.station |
| M08 | contradiction_deep | ST_008, contradiction-deep.station |
| M09 | claim_extract | ST_003, claim-extractor.station |
| M10 | timeline | timeline-verifier.station |
| M11 | math_verify | math-verify.station |
| M12 | paper_review | paper-review.station |
| M13 | bart_summarizer | ST_001 (alt) |
| M14 | clip_vision | image-processor.station |
| M15 | mistral_7b | (reserved) |
| M16 | whisper_large_v3 | whisper-transcribe.station |

## Existing Code to Migrate

- **ST_001 exec-summary**: NEW — write from scratch
- **ST_002 plain-language**: readability-rewriter.station
- **ST_003 claim-extraction**: claim-extractor.station
- **ST_004 claim-classification**: classify-documents.station + mda-citation-spine.station/claim_inventory.py
- **ST_005 load-bearing-claims**: mda-citation-spine.station/claim_inventory.py (LOAD_BEARING_SECTION_WORDS, MODEL_CLAIM_TERMS)
- **ST_006 falsification**: fact-verifier.station
- **ST_007 evidence-map**: NEW — write from scratch
- **ST_008 contradiction-scan**: contradiction-detector.station + contradiction-deep.station

## What Codex Needs To Do

For each station, implement ONLY sections 06 and 07 in pipeline.py:
- Section 06 (NLP_ROUTE): Load the correct model, handle fallbacks
- Section 07 (PROCESS): The actual processing logic
Everything else (ingest, validate, artifacts, archive) is already handled by SSS_v1.

