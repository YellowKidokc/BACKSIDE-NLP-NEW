# Phase 2: SSS_v1 Logic Migration
## Migrate station logic from pipeline_legacy.py into pipeline.py section 07

### Context
Phase 1 (complete) created a standardized `pipeline.py` (SSS_v1 skeleton) and `pipeline_legacy.py` (original code) in every station. The skeleton has 13 sections — only sections 06 (NLP_ROUTE) and 07 (PROCESS) are station-specific. Currently section 07 is a generic passthrough stub. The real logic lives in `pipeline_legacy.py`.

### Task
For each station in `stations/`, migrate the core logic from `pipeline_legacy.py` into section 07 of `pipeline.py`. After migration, the station should actually perform its real action when `pipeline.py` runs.

### Rules

1. **Read `stations/_shared/SSS_v1_STANDARD.md`** before starting. It defines the 13-section structure.

2. **Read `stations/_shared/SSS_TEMPLATE_v1.py`** for the canonical section format.

3. **For each station that has both `pipeline.py` and `pipeline_legacy.py`:**
   a. Read `pipeline_legacy.py` to understand what the station actually does
   b. Extract the core processing logic (the ONE action)
   c. Wire it into section `07_PROCESS` of `pipeline.py` inside the `process_one()` function
   d. Move any station-specific imports to section `00_IMPORTS`
   e. Update section `06_NLP_ROUTE` if the legacy code calls a specific NLP model
   f. Update `config.json` with correct `input_extensions` and `workers` based on what the legacy code processes

4. **Do NOT change sections 02-05 or 08-12.** Those are identical across all stations and must stay that way.

5. **Do NOT delete `pipeline_legacy.py`.** It stays as reference.

6. **The `process_one()` function signature must not change:**
   ```python
   def process_one(path: Path, nlp_info: dict, cfg: dict[str, Any],
                   log: logging.Logger) -> dict[str, Any]:
   ```
   It receives one input file path, returns a result dict.

7. **Result dict must include these keys:**
   ```python
   {
       "input_file": str,
       "station_id": str,
       "station_name": str,
       "nlp_used": str,
       "processed_at": str,
       "success": bool,
       "artifacts": list,
       "errors": list,
       "data": dict  # <-- the actual output goes here
   }
   ```

8. **Path resolution uses `_resolve()` shim** (already in every pipeline.py):
   - `MODELS` resolves to `05_MODELS/` or `models/`
   - `ENGINES` resolves to `06_ENGINES/` or `engines/`
   - `BRAIN` resolves to the brain root
   - Templates live at `BRAIN / "15_TEMPLATES"` (NAS) or `BRAIN / "templates"` (repo)

9. **If a legacy station has multiple actions**, extract only the PRIMARY action into `process_one()`. Secondary actions can become helper functions called from `process_one()`.

10. **If a legacy station is too complex to migrate safely** (>300 lines of core logic, heavy class hierarchies, external service dependencies), leave section 07 as the passthrough stub and add a comment: `# PHASE2_SKIP: [reason]`. Do not force a migration that would break.

### Priority Order
Start with stations that have the simplest legacy code and work up:
- Simple stations first (< 100 lines of logic): summarizer, fact-verifier, section-splitter, metadata-extractor, contradiction-detector, contradiction-deep
- Medium stations next (100-300 lines): claim-extractor, classify-documents, sbert-embedder, hdbscan-cluster, deberta-runner, whisper-transcribe, youtube-scrape
- Complex stations last: paper-proof-grader, harvest-links, mda-citation-spine, reading-level-glossary, file-intelligence, html-article

### Testing
After migrating each station:
1. Verify `pipeline.py` compiles: `python -c "import ast; ast.parse(open('pipeline.py').read())"`
2. Verify config loads: `python -c "import json; json.load(open('config.json'))"`
3. If a canary/test input exists in the station, run it

### Commit
One commit per station batch (simple, medium, complex). Commit message format:
```
Phase 2: Migrate logic for [station-name] — [brief description of what it does]
```