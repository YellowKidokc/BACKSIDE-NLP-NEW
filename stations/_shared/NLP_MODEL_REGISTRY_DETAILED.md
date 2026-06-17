# NLP Model Registry - Detailed HuggingFace Mapping
# POF 2828 | 2026-06-17
# Source: GPT model analysis mapped to Brain capability folders
# Cross-referenced with Core 8 stations (see CORE_8_NLP_CHEAT_SHEET.md)

## Station-to-Model Mapping (Specific)

| Station | Capability Folder | Primary Model | Backup |
|---------|-------------------|---------------|--------|
| ST_001 exec-summary | 08_SUMMARIZER | facebook/bart-large-cnn | allenai/led-large-16384-arxiv (long docs) |
| ST_002 plain-language | LLM (Ollama/OpenAI) | phi4 / gpt-4o | - |
| ST_003 claim-extraction | 18_QA_EXTRACTOR | deepset/roberta-base-squad2 | deepset/roberta-large-squad2 |
| ST_004 claim-classification | 07_ZERO_SHOT | MoritzLaurer/deberta-v3-large-zeroshot-v2.0 | sileod/deberta-v3-large-tasksource-nli |
| ST_005 load-bearing-claims | 07_ZERO_SHOT + LLM | same as ST_004 + Ollama reasoning | - |
| ST_006 falsification | 05_SCI_CLAIM_VERIFY | SciFact pipeline (retrieval + NLI) | shidey/deberta-v3-mednli-scifact |
| ST_007 evidence-map | 03/04_EMBED + 09_RERANK | Qwen3-Embedding-0.6B + BAAI/bge-reranker-v2-m3 | all-MiniLM-L6-v2 |
| ST_008 contradiction-scan | 01 + 15_CONTRADICTION | MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli | ensemble with cross-encoder + long-NLI |

## Full 18-Folder Capability Registry

| # | Folder | Primary Model | Notes |
|---|--------|---------------|-------|
| 01 | CONTRADICTION_PRIMARY | MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli | NLI: contradiction/entailment/neutral |
| 02 | CONTRADICTION_FAST | cross-encoder/nli-MiniLM2-L6-H768 | Low latency NLI screening |
| 03 | EMBEDDINGS_FAST | Qwen/Qwen3-Embedding-0.6B | Semantic search, clustering |
| 04 | EMBEDDINGS_QUALITY | Qwen/Qwen3-Embedding-4B or 8B | High-quality retrieval |
| 05 | SCIENTIFIC_CLAIM_VERIFY | SciFact pipeline (retrieval + NLI) | NOT a simple classifier |
| 06 | NER_GENERAL | dslim/bert-base-NER | PER/ORG/LOC/MISC |
| 07 | ZERO_SHOT_CLASSIFIER | MoritzLaurer/deberta-v3-large-zeroshot-v2.0 | NLI-based zero-shot |
| 08 | SUMMARIZER | facebook/bart-large-cnn | LED-Arxiv for long papers |
| 09 | RERANKER | Qwen/Qwen3-Reranker-0.6B or BAAI/bge-reranker-v2-m3 | Post-embedding reranking |
| 10 | SENTIMENT | cardiffnlp/twitter-roberta-base-sentiment-latest | pos/neg/neutral |
| 11 | MATH_OCR | breezedeus/pix2text-mfr-1.5 | Vision task, not NLP-only |
| 12 | DOC_OCR_HEAVY | PaddleOCR-VL-1.6 / olmOCR 2 | Scanned PDFs, tables, layouts |
| 13 | IMAGE_CAPTION | Salesforce/blip-image-captioning-large | Vision-language |
| 14 | CONTRADICTION_TINY | typeform/distilbert-base-uncased-mnli | Quick screening only |
| 15 | CONTRADICTION_ENSEMBLE | MoritzLaurer + cross-encoder + long-NLI | Majority vote wrapper |
| 16 | NER_ENHANCED | urchade/gliner_multi-v2.1 | Open-type entity extraction |
| 17 | DEDUP | Hash + MinHash/LSH + semantic embeddings | Multi-method pipeline |
| 18 | QA_EXTRACTOR | deepset/roberta-base-squad2 | Extractive QA (SQuAD2) |

## Architecture (from GPT analysis)

```
raw document / image / text
    -> OCR / parsing if needed
    -> chunking + dedup
    -> embeddings retrieval
    -> reranker
    -> task model (NLI / NER / classification / summarization / QA)
    -> stored result with confidence + evidence pointer
```

## Output Contract (per GPT recommendation)

Every task model result should include:
```json
{
  "claim": "...",
  "matched_evidence": "...",
  "source_path": "...",
  "model": "...",
  "label": "contradiction | entailment | neutral | unsupported",
  "confidence": 0.0,
  "reason": "short explanation"
}
```
