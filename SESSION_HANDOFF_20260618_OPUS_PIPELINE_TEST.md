# SESSION HANDOFF — Opus to Opus
# 2026-06-17 (late night / early morning session)
# David Lowe | POF 2828

---

## WHAT THIS SESSION ACCOMPLISHED

### 1. Untangled Codex Merge Conflict (Critical Fix)
Codex's PR refactored all 8 Core NLP station pipelines to import from shared helpers instead of inline duplicates. The merge went wrong:
- `station_helpers.py` had a "both added" conflict — resolved by keeping the original version, but Codex's pipelines imported different function names
- Every pipeline had TWO `process_one` functions (Codex's new + old inline) — Python took the last one (old), so shared helpers were dead code
- **Fixed:** Added 6 aliases + 3 new functions to `station_helpers.py` (call_nlp, sentences, paragraphs, sections, cosine, embeddings, data_from_artifact, flesch_reading_ease, nlp_route). Fixed `base_result` signature. Removed duplicate Section 07 from 6 pipelines. All 8 compile + import clean.
- **Commit:** `b80bfcb` on `OBS-Plugin-Final-Claude`

### 2. Built smart_sync.py (Whitelist-Based Station Sync)
Old sync script used blacklist approach — still pulled too much crud. New script:
- Whitelist of 24 stations (Core 8 + shared + extended)
- Code files only (.py, .md, .json, .bat, etc.)
- Max 500KB per file
- Dry run by default (`--go` to actually copy)
- Bidirectional: `--push` for D:→NAS, default is NAS→D:
- `--core-only` flag for just the 8 NLP stations + _shared
- **Location:** `D:\GitHub\BACKSIDE-NLP-NEW\smart_sync.py`
- **Commit:** included in `b80bfcb`

### 3. Built WORKFLOW_STAGES.md (7-Stage Production Pipeline)
Full manufacturing line for MDA article processing with gate checks:
- Stage 0: Source verification (math translation blocks present)
- Stage 1: HTML → Markdown conversion
- Stage 2: Vectorization (ChromaDB)
- Stage 3: Core 8 NLP pipeline (8 substeps, some parallelizable)
- Stage 4: Enrichment (grading, proof explorer, glossary, knowledge graph)
- Stage 5: Assembly (rebuild HTML with all data)
- Stage 6: Publish
- Includes dependency diagram, tracking format, rules
- **Commit:** `76f6239`

### 4. Fixed NLP API Model Paths
Model folders on NAS use M-prefix naming (M23_08_SUMMARIZER) but API expected bare names (08_SUMMARIZER). Fixed all 14 paths in `nlp_api/main.py`. All 14 models now resolve to existing directories.
- **NOT YET COMMITTED** — main.py was modified but session ended before commit

### 5. Test Article Pipeline (MDA-039)
Pushed MDA-039-physics-of-coherence through Stages 0-1:
- **Stage 0 PASS:** 3 equation blocks with data-eq-id, MathJax loaded, MTL CSS linked
- **Stage 1 PASS:** Clean markdown output, 425 words, 6 headings, 3 equations with translations preserved
- **Stage 3a ATTEMPTED:** ST_001 exec-summary ran, called FastAPI, but hit transformers 5.x breaking change

### 6. Key Discovery: Two MDA Directories
- `D:\GitHub\faiththruphysics-site\mda\` — OLD version, no math translation layer
- `D:\GitHub\faiththruphysics-site\moral-decline\` — Kimi's version WITH math translation layer (mtl-equation.js, mtl-equations.json, data-eq-id blocks on all articles)
- **Source of truth is `moral-decline/`** — this is where the pipeline pulls from

---

## WHAT NEEDS TO BE DONE NEXT (in order)

### IMMEDIATE: Fix Transformers 5.x Compatibility (~15 min)
**File:** `D:\GitHub\BACKSIDE-NLP-NEW\nlp_api\main.py`
**Problem:** Transformers 5.5.4 dropped the `"summarization"` pipeline task name. The `/nlp/summarize` endpoint at line 216 uses `hf_pipeline("summarization", ...)` which throws `KeyError`.
**Fix options:**
1. **Best:** Replace `hf_pipeline("summarization")` with direct model loading:
   ```python
   from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
   tokenizer = AutoTokenizer.from_pretrained(str(path))
   model = AutoModelForSeq2SeqLM.from_pretrained(str(path))
   ```
2. **Quick:** Pin transformers to 4.x: `pip install transformers==4.44.0`
3. **Audit ALL endpoints** — NER, classify, sentiment may also use deprecated task names

### THEN: Re-run MDA-039 Through Full Pipeline
1. Fix the API, restart it on port 8700
2. Move test file back to inbox: `stations\exec-summary.station\_processed\MDA-039-physics-of-coherence.md` → `_inbox\`
3. Run ST_001 (exec-summary) — should produce summary + NER JSON artifact
4. Copy markdown to ST_002-ST_008 inboxes and run each
5. Check every artifact for `success: true` and populated `data` field

### THEN: Vectorize
1. The ChromaDB vector store is initialized at `D:\GitHub\BACKSIDE-NLP-NEW\nlp_api\vector_db`
2. Collection: `theophysics_corpus` (currently 0 documents)
3. Use `/vector/ingest` endpoint to push markdown chunks
4. Chunk by section headings, not whole documents
5. Include metadata: article_id, section, series_group

### THEN: Scale to All 61 MDA Articles
1. Batch convert all `moral-decline/*.html` → markdown
2. Run through pipeline
3. Track with WORKFLOW_STAGES.md status format

### EXPANDED WORKFLOW (from David's direction this session)
David clarified the full pipeline is more stages than originally documented:
1. Math translation layer (DONE — Kimi wired it into moral-decline/ HTML)
2. Vectorize into ChromaDB
3. HTML → Markdown conversion
4. Core 8 NLP (summaries, reading levels, claims, classification, load-bearing, falsification, evidence, contradictions)
5. Claims refinement — pull lexicon from templates folder, quantify claim strength with phrasing patterns, whittle 500-600 raw claims to load-bearing ones
6. Paper Intelligence System — 7Q classification, Fruits of Spirit scoring, CKG evaluation
7. Graph + Tags — route classification JSON to knowledge graphs, generate sidebar tags
8. Assembly — rebuild HTML, populate proof explorer tabs (Axioms, 7Q, Decision Tree, Swap Test, CKG, Fruits, Iron Chain)
9. Publish

The proof explorer (see uploaded `proof-explorer-fp-005-enhanced.html`) defines the data contract — every tab needs specific JSON data from specific stations.

---

## FILE LOCATIONS

| What | Path |
|------|------|
| Station code (D:) | `D:\GitHub\BACKSIDE-NLP-NEW\stations\` |
| Station code (NAS) | `\\192.168.2.50\brain\04_STATIONS\` |
| Models (NAS) | `\\192.168.2.50\brain\05_MODELS\` (M17-M30 prefix naming) |
| FastAPI service | `D:\GitHub\BACKSIDE-NLP-NEW\nlp_api\main.py` (port 8700) |
| Shared helpers | `stations\_shared\station_helpers.py` |
| Smart sync | `D:\GitHub\BACKSIDE-NLP-NEW\smart_sync.py` |
| Workflow stages | `D:\GitHub\BACKSIDE-NLP-NEW\WORKFLOW_STAGES.md` |
| MDA source (CANONICAL) | `D:\GitHub\faiththruphysics-site\moral-decline\` |
| MDA source (OLD, no MTL) | `D:\GitHub\faiththruphysics-site\mda\` (DO NOT USE) |
| MTL equation JS | `D:\GitHub\faiththruphysics-site\shared\js\mtl-equation.js` |
| MTL equation data | `D:\GitHub\faiththruphysics-site\shared\data\mtl-equations.json` |
| Service stack | `C:\Users\lowes\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\pof-service-stack\` |
| Test article output | `stations\exec-summary.station\_outbox\ART_20260617_020532__ST_001__MDA-039-physics-of-coherence.json` |
| Test article markdown | `stations\exec-summary.station\_processed\MDA-039-physics-of-coherence.md` |
| HTML→MD converter | `D:\GitHub\BACKSIDE-NLP-NEW\run_test_article.py` |
| Merge fix script | `D:\GitHub\BACKSIDE-NLP-NEW\fix_merge.py` |

---

## UNCOMMITTED CHANGES
- `nlp_api/main.py` — model path fixes (M-prefix naming). COMMIT THIS FIRST.
- `run_test_article.py` — Stage 0+1 test script
- `fix_merge.py` — merge cleanup script (already ran, safe to commit)
- `SESSION_HANDOFF_20260618_OPUS_PIPELINE_TEST.md` — this file

---

## CONTEXT FROM DAVID
- Order matters extensively. One miss at step 1 costs at step 7.
- Trial by fire approach — run it, see what breaks, fix, repeat.
- The lexicon/template folder has phrasing patterns that help classify claims vs filler.
- The proof explorer is the ultimate data consumer — every framework tab maps to a station.
- David called this "the least amount of headache and the farthest we've ever got in one day."
- FastAPI stays up as persistent service — all stations share it via HTTP, models load once lazily.

---

*Session ended: 2026-06-17 ~2:15 AM. Major infrastructure session — merge fix, sync tooling, workflow documentation, first test article through 2 stages. Transformers 5.x compatibility is the immediate blocker.*
