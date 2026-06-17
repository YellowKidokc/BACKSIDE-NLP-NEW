# SESSION HANDOFF — Opus to Opus
# 2026-06-17 (late night session)
# David Lowe | POF 2828

---

## WHERE WE ARE

Tonight was a major infrastructure sprint. We built the complete NLP pipeline architecture from stations through models through API through workflow. The processing logic is implemented, the models are downloaded, the API service exists. We're at roughly 65-70% complete — the decisions are made, the code is written, what remains is wiring and testing.

---

## WHAT WAS BUILT TONIGHT

### 1. Eight Core NLP Stations (ST_001 through ST_008)
**Location:** `D:\GitHub\BACKSIDE-NLP-NEW\stations\` and `\\192.168.2.50\brain\04_STATIONS\`

Each station has a full SSS_v1 pipeline.py with sections 06 (NLP_ROUTE) and 07 (PROCESS) implemented by Codex. These are the core document analysis pipeline:

| Station | What It Does |
|---------|-------------|
| ST_001 exec-summary | Executive summary + entity extraction |
| ST_002 plain-language | Rewrite at 3 reading levels (grade 6, 10, graduate) |
| ST_003 claim-extraction | Extract every claim with paragraph/sentence position |
| ST_004 claim-classification | Classify claims by maturity + domain |
| ST_005 load-bearing-claims | Triage: PAPER_CLAIM / CITATION_FACT / REVIEW / PARK |
| ST_006 falsification | Generate kill conditions + evidence bars |
| ST_007 evidence-map | Map evidence to claims, find gaps |
| ST_008 contradiction-scan | Cross-claim contradiction detection |

### 2. Fourteen HuggingFace Models Downloaded
**Location:** `\\192.168.2.50\brain\05_MODELS\` (weights on NAS only)
**Registry:** `D:\GitHub\BACKSIDE-NLP-NEW\models\MODEL_REGISTRY.json`

New capability folders (01-18 numbering) alongside legacy M01-M16:
- 01_CONTRADICTION_PRIMARY (MoritzLaurer/DeBERTa-v3-large)
- 02_CONTRADICTION_FAST (cross-encoder/nli-MiniLM2)
- 03_EMBEDDINGS_FAST (all-MiniLM-L6-v2)
- 05_SCIENTIFIC_CLAIM_VERIFY (cross-encoder/nli-deberta-v3-base)
- 06_NER_GENERAL (dslim/bert-base-NER)
- 07_ZERO_SHOT_CLASSIFIER (MoritzLaurer/deberta-v3-large-zeroshot)
- 08_SUMMARIZER (facebook/bart-large-cnn)
- 09_RERANKER (BAAI/bge-reranker-v2-m3)
- 10_SENTIMENT (cardiffnlp/twitter-roberta-base-sentiment)
- 13_IMAGE_CAPTION (Salesforce/blip-image-captioning-large)
- 14_CONTRADICTION_TINY (typeform/distilbert-base-uncased-mnli)
- 15_CONTRADICTION_ENSEMBLE_LONG (tasksource/deberta-base-long-nli)
- 16_NER_ENHANCED (urchade/gliner_multi-v2.1)
- 18_QA_EXTRACTOR (deepset/roberta-base-squad2)

D: drive has configs/tokenizers only (no weights) — sync script at `sync_models_structure.py`.

### 3. FastAPI NLP Service
**Location:** `D:\GitHub\BACKSIDE-NLP-NEW\nlp_api\main.py`
**Port:** 8700 | **Docs:** http://localhost:8700/docs
**Registered in service manager** at `D:\GitHub\Theophysics-OS-\service_manager.py` (port 9999 dashboard)

Endpoints: `/nlp/contradiction`, `/nlp/classify`, `/nlp/embed`, `/nlp/summarize`, `/nlp/ner`, `/nlp/sentiment`, `/nlp/qa`
Plus ChromaDB vector store: `/vector/ingest`, `/vector/query`, `/vector/stats`

Models load lazily from NAS on first API call, stay in memory. All stations call this service instead of loading models locally.

### 4. Shared Infrastructure Created
- `stations/_shared/station_helpers.py` — all shared functions (api_call, strip_html, split_sections, cosine_similarity, etc.)
- `stations/_shared/job_card.py` — workflow tracking system (check_in/check_out per station, progress reporting)
- `stations/_shared/__init__.py` — package init
- `stations/_shared/job_cards/` — directory for job card JSON files
- 3 prompt.md files for LLM stations (plain-language, falsification, load-bearing-claims)

### 5. Bug Fixes Applied
- **ST_008 contradiction-scan:** Fixed parameter mismatch (`text_a/text_b` → `premise/hypothesis`) — would have caused 422 errors
- **ST_003 claim-extraction:** Added prefilter to skip short/non-claim sentences — was making ~200 individual API calls per article

### 6. Sync Scripts
- `sync_stations_clean.py` — syncs station CODE from NAS to D: (skips _outbox, _processed, EXPORTS, logs, __pycache__). Reduced 199,274 files to 3,973.
- `sync_models_structure.py` — syncs model configs from NAS to D: without weight files. Creates .WEIGHT_ON_NAS placeholders.
- `download_nlp_models.py` — downloads models from HuggingFace to NAS. Resumable.

### 7. Documentation (all on D: and NAS)
- `CODEX_BUILD_CORE_8_STATIONS.md` — detailed spec for all 8 stations (JSON output schemas, processing logic, testing instructions). 420 lines.
- `CODEX_FOLLOWUP_FIX_GAPS.md` — follow-up Codex prompt for remaining mechanical work. 297 lines. 8 priorities.
- `WORKFLOW_MAP_ARTICLE_PRODUCTION.md` — full 5-phase workflow from article to website. 321 lines.
- `PROOF_EXPLORER_COMPONENT_MAP.md` — every proof explorer component mapped to its producing station. 167 lines.
- `stations/_shared/CORE_8_NLP_CHEAT_SHEET.md` — station-to-model mapping quick reference.
- `stations/_shared/NLP_MODEL_REGISTRY_DETAILED.md` — full 18-folder HuggingFace model reference from GPT analysis.

---

## WHAT STILL NEEDS TO BE DONE

### Immediate (hand to Codex via CODEX_FOLLOWUP_FIX_GAPS.md):
1. **Refactor all 8 pipeline.py** to import from `_shared/station_helpers.py` instead of inline duplicates. Currently helper functions are copy-pasted in all 8 files.
2. **Update all 8 config.json** with real model paths, API settings, upstream/downstream wiring.
3. **Create 8 wiring_spec.json** files defining input/output contracts per station.
4. **Update all 8 README.md** to describe what the station actually does now.
5. **Wire job card** into Section 09 of each station (import JobCard, call check_in/check_out).
6. **Add glossary extraction** to ST_002 — flag terms above 8th grade, output glossary_candidates array.

### Next working session priorities:
7. **Vectorize MDA articles** — the vectorize_mda.py script exists in A_BIL but the source path needs updating. Need to know where the MDA HTML files currently live. Then run SBERT embeddings → ChromaDB.
8. **HTML→Markdown conversion** — the math-translation-layer station already has an HTML extractor. Need a clean conversion station or use the existing extractor in reverse.
9. **Math Translation Layer** — the station at `math-translation-layer.station/` has a full TypeScript pipeline (parse → translate → render) with a Theophysics canon dictionary. Has `RUN_MATH_TTS_WORKFLOW.bat` that chains math translation + TTS. This needs to run BEFORE TTS so audio reads equations in plain English.
10. **Test end-to-end** — drop one MDA article through the full pipeline and verify each station produces correct output.

### Future:
11. Knowledge graph station + series aggregation
12. Master Equation classification (which χ variables each paper touches)
13. Series-level proof explorer (aggregate all per-paper scores)
14. Standalone installer/packaging (core app + model plugins pattern — see conversation for details)

---

## KEY ARCHITECTURE DECISIONS

- **Stations call FastAPI, not models directly.** Every NLP call goes through `http://localhost:8700/nlp/{endpoint}`. One service loads models, all stations share them.
- **SSS_v1 standard:** Every station has the same 13-section structure. Only sections 06 and 07 change. Everything else is template.
- **Models on NAS, code on D:.** Weight files (multi-GB) stay at `\\192.168.2.50\brain\05_MODELS\`. Station code lives at `D:\GitHub\BACKSIDE-NLP-NEW\`. Sync scripts bridge them.
- **Two naming schemes coexist:** Old M01-M16 (legacy) + new 01-18 capability folders. Both mapped in MODEL_REGISTRY.json. FastAPI uses logical keys (contradiction_primary, embeddings_fast, etc.).
- **Job card tracking:** Each document gets a JOB_{doc_id}.json that records which stations it passed through, what succeeded, what failed. Located at `_shared/job_cards/`.
- **Workflow is 5 phases:** Intake → Core NLP (ST_001-008) → Enrichment (grading, vectorization, math, TTS) → Assembly (rebuild HTML) → Publish (deploy to site).

---

## FILE LOCATIONS (quick reference)

| What | Path |
|------|------|
| Station code (D:) | `D:\GitHub\BACKSIDE-NLP-NEW\stations\` |
| Station code (NAS) | `\\192.168.2.50\brain\04_STATIONS\` |
| Models (NAS, with weights) | `\\192.168.2.50\brain\05_MODELS\` |
| Models (D:, configs only) | `D:\GitHub\BACKSIDE-NLP-NEW\models\` |
| FastAPI service | `D:\GitHub\BACKSIDE-NLP-NEW\nlp_api\main.py` |
| Service manager | `D:\GitHub\Theophysics-OS-\service_manager.py` |
| Website source | `D:\GitHub\faiththruphysics-site\` |
| Shared helpers | `stations\_shared\station_helpers.py` |
| Job card system | `stations\_shared\job_card.py` |
| Codex build prompt | `CODEX_BUILD_CORE_8_STATIONS.md` |
| Codex follow-up | `CODEX_FOLLOWUP_FIX_GAPS.md` |
| Workflow map | `WORKFLOW_MAP_ARTICLE_PRODUCTION.md` |
| Proof explorer map | `PROOF_EXPLORER_COMPONENT_MAP.md` |
| Model registry | `models\MODEL_REGISTRY.json` |
| Station registry | `stations\STATION_REGISTRY.json` |
| Download manifest | `models\DOWNLOAD_MANIFEST.json` |

---

## CONTEXT FROM DAVID

- David wants the pipeline to produce everything the website needs automatically: reading levels, glossary, claims tab, math translations, audio, proof explorer data.
- The auto-glossary is important: anything above 8th grade reading level gets defined and linked automatically.
- The proof explorer (see uploaded FP-005 HTML) has 7 framework tabs (Axioms, 7Q, Decision Tree, Swap Test, CKG, Fruits, Iron Chain) — each maps to an existing station. See PROOF_EXPLORER_COMPONENT_MAP.md.
- David is considering packaging this as a standalone product (core app + model plugins). Architecture discussion happened but this is a future track.
- Postgres NAS container is currently down. When it comes back up, there's a correction to do (10 seconds).
- The MDA HTML source path in vectorize_mda.py needs updating — old path was `\\dlowenas\HPWorkstation\Desktop\Master HTMl\K-Production-Ready\MDA final David` which didn't resolve. Need to ask David for current location.

---

## HOW TO START NEXT SESSION

1. Check if Codex completed the follow-up prompt (CODEX_FOLLOWUP_FIX_GAPS.md)
2. If yes: review the changes, test one station
3. If no: either hand it to Codex or do it directly
4. Ask David where the MDA HTML files live now (for vectorization)
5. Start the FastAPI service (`D:\GitHub\BACKSIDE-NLP-NEW\nlp_api\RUN.bat`) and test with a real article

---

*Session ended: 2026-06-17 late night. Good session — heavy infrastructure work, clean architecture, ready for testing.*
