# SESSION HANDOFF — June 16-17, 2026
## Stations, Workflows, Templates, River FIS
**POF 2828 | For next Opus session**

---

## WHAT WE CONFIRMED TONIGHT

### 1. The Architecture Is Real and Connected

The repo at D:\GitHub\BACKSIDE-NLP-NEW is the master source of truth.

```
workflows/ → reference stations by name via dependencies.json  ✅
stations/  → reference templates via TEMPLATE_WIRING_MAP.md    ✅
templates/ → 40+ Excel/HTML/MD files exist in repo             ✅
models/    → M01-M16 NLP models defined                        ✅
engines/   → P01-P07 preference engines defined                ✅
orchestrator/ → nlp_layer.py, healthcheck scripts              ✅
```

Verified workflow→station wiring:
- chi-tagging.workflow → master-equation-canon, trinity-canon, fruits-spirit-canon, operators-canon
- first-article.workflow → conversion, executive-summary, overview, math-layer, image-notes, lossless-context
- semantic-snapshot.workflow → chains to first-article, chi-tagging, paper-proof-grader, axioms

### 2. The ONE Known Gap: Section 07 Stubs

Every station's pipeline.py follows SSS_v1 (13-section standard). Sections 00-05 and 08-12 are identical and working. Section 06 (NLP routing) works. Section 07 (the actual processing) is a passthrough stub in ALL stations — it reads the input file and wraps it in a result dict but does not call any NLP model or processing logic.

The real processing logic exists in some stations as separate .py files:
- sbert-embedder.station → sbert_runner.py (real SBERT via Infinity + Qdrant)
- paper-proof-grader.station → expanded_report.py, formal_verification.py, fruits_of_spirit_bridge.py, run_axiom_7q_stations.py

pipeline_legacy.py in most stations is ALSO a template stub, not the original code.

### 3. Changes Made Tonight

**Rename: 03_JOB_CARDS → 03_WORKFLOWS**
- X:\03_JOB_CARDS renamed to X:\03_WORKFLOWS
- SSS_TEMPLATE_v1.py updated on BOTH X: drive and repo (JOB_CARDS → WORKFLOWS, update_job_card → update_workflow)
- SSS_v1_STANDARD.md updated on both locations
- Repo already had workflows/ folder — now aligned

**River FIS Intelligence Scorer**
- Wrote intelligence_scorer.py at X:\08_DASHBOARDS\FILE SORTER\
- 5 priority detectors: duplicates, naming chaos, domain clusters, tiny folders, junk files
- Matches actual SQLite schema (files, folders, classifications tables)
- Wired /api/intelligence endpoint into api_server.py
- NOT yet in D:\GitHub\FIS repo — needs to go into engines/ there

**Excel Workbook Updated**
- universal_domain_mapping_with_coherence_v9.xlsx — added "Exhaustive CD Mapping" sheet
- 70 domains, 9 tiers, color-coded, synthesis findings
- Output file available for download

---

## THE NEXT JOB: Station-by-Station Wiring

### Strategy
Go one station at a time. For each:
1. List all .py files in the station folder
2. Read the real processing scripts (not pipeline.py — the separate runners)
3. Wire section 07 to import and call the real script
4. Test: drop a file in _inbox, run pipeline.py, check _outbox for real output
5. Move to next station

### Priority Order (suggested)
Start with stations that have KNOWN real scripts:

| Priority | Station | Real Script | What It Does |
|----------|---------|-------------|--------------|
| 1 | sbert-embedder | sbert_runner.py | Vectorize files via Infinity |
| 2 | classify-documents | (needs writing) | Classify by domain |
| 3 | paper-proof-grader | expanded_report.py, formal_verification.py | Grade papers |
| 4 | summarizer | (check for runner) | Summarize text |
| 5 | claim-extractor | (check for runner) | Extract claims |
| 6 | contradiction-detector | (check for runner) | Find contradictions |
| 7 | metadata-extractor | (check for runner) | Extract metadata |
| 8 | paper-intelligence-suite | (check for runner) | Full paper analysis |

### The Test Case
Use O:\_Theophysics_v5\ELON folder (23 markdown files, 3 subfolders):
1. sbert-embedder: vectorize all 23 files
2. classify-documents: classify by domain
3. Verify results make sense before moving to next station

### Infrastructure Check Needed
- Is Infinity running on NAS? (sbert_runner.py needs it for embeddings)
- Is Qdrant running? (vector storage)
- Is PostgreSQL at 192.168.1.177:2665 accessible? (some stations need it)

---

## TEMPLATE VERIFICATION NEEDED

David customized the Excel templates to look polished and final. Need to verify:
- Do the TEMPLATE_WIRING_MAP.md references match actual filenames in templates/?
- Do station config.json files reference the right template paths?
- Are the Excel field names/columns what the station scripts expect?

This is a separate audit from the section 07 wiring — but should happen alongside it.

---

## FILE LOCATION MAP

| What | Where |
|------|-------|
| Master repo (stations, models, engines, workflows, templates) | D:\GitHub\BACKSIDE-NLP-NEW |
| River FIS repo (GUI, core, engines, tests) | D:\GitHub\FIS |
| Working River FIS (running app) | X:\08_DASHBOARDS\FILE SORTER |
| Stations (live) | X:\04_STATIONS |
| Models (live) | X:\05_MODELS |
| Engines (live) | X:\06_ENGINES |
| Workflows (live) | X:\03_WORKFLOWS |
| Obsidian vault | O:\_Theophysics_v5 |
| SQLite cache (FIS) | \\192.168.2.50\brain\09_DATABASES\FIS\sorter_cache.sqlite |
| PostgreSQL | 192.168.1.177:2665 |

---

## COHERENCE PAPER STATUS (from earlier tonight)

- 70-domain mapping completed and added to Excel workbook
- Paper outline written at NAS: COHERENCE_PAPER_OUTLINE.md
- Deep research prompt deployed
- Second Law debate sharpened: don't say it "started" at the Fall, don't call it Yin/Yang
- Paper ending locked: "Either they are meaningless fluctuations awaiting erasure, or the system is not closed."
- Lean 4 verification located: COPY_PASTE_LEAN4.lean (150 lines, zero sorry, 4 theorems)
- GitHub: https://github.com/DavidLoweOKC/Lean-4-Proofs/tree/main/theophysics-lean-verification-package
- Templeton OFI deadline: August 14, 2026

---

## SESSION STATS

- Coherence/decoherence domain mapping (70 domains)
- Excel workbook updated to v9
- GPT adversarial review on Second Law, Genesis ages, GR/QM divide
- Three claims sharpened from GPT pushback
- Lean 4 proofs located and documented
- River FIS intelligence_scorer.py written and wired
- 03_JOB_CARDS → 03_WORKFLOWS renamed (X: + repo)
- SSS_TEMPLATE_v1.py synced across X: and repo
- Station audit: section 07 stubs confirmed across all checked stations
- Workflow→station→template wiring confirmed as real
- BACKSIDE-NLP-NEW repo confirmed as master source of truth
