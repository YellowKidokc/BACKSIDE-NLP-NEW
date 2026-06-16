# CODEX TASK 3: Classification Station + Workflow Tracker

## Part A: classify-documents Station

### What It Does
First station after sbert-embedder in the pipeline. Reads a paper/article,
classifies it across multiple dimensions, outputs a classification artifact
that ALL downstream stations consume.

### Classification Schema

The output JSON must include ALL of these fields (they fill the snapshot template):

#### 1. doc_type (controlled vocabulary)
```
foundational_paper | empirical_study | story | apologetics |
technical_analysis | meta_analysis | devotional | infrastructure
```

#### 2. classification (human-readable string)
Examples: "Story / Foundational", "Technical / Physics", "Empirical / MDA"

#### 3. tags (array of strings, controlled vocabulary)
Pillar tags (which domains this paper touches):
- pillar/philosophy, pillar/theology, pillar/physics
- pillar/mathematics, pillar/consciousness, pillar/information-theory

Domain tags (specific framework elements):
- master_equation, logos/method, structural-isomorphism
- entropy, free_will, trinity, moral-conservation
- boundary-proof, fruits-of-spirit, seven-q, lean4-verified

Series tags (which series it belongs to):
- series/mda, series/gtq, series/convergence
- series/logos-papers, series/bible-study

Method tags (what formal methods are used):
- method/lean4, method/jax, method/statistical, method/formal-proof

#### 4. spine_mappings (domain coverage)
Six domains, each with a strength score (0-100) and status label:
```json
{
  "physics":         { "score": 85, "status": "Grounded" },
  "theology":        { "score": 90, "status": "Canonical" },
  "consciousness":   { "score": 45, "status": "Suggested" },
  "category_theory": { "score": 60, "status": "Framework" },
  "evidence":        { "score": 75, "status": "6.35σ" },
  "isomorphism":     { "score": 70, "status": "Verified" }
}
```
Status options: Grounded | Canonical | Framework | Suggested | Referenced | None
Evidence status is special: sigma value string OR "Theoretical"

#### 5. dependency_chain
```json
{
  "upstream": ["A1.1", "A2.1", "FP-001", "FP-002"],
  "downstream": ["PRED-001", "OP1", "OP2"]
}
```

#### 6. word_count (integer)

#### 7. reading_level
```json
{
  "flesch_kincaid_grade": 12.3,
  "hard_words": ["isomorphism", "substrate", "spontaneous symmetry breaking"],
  "hard_word_count": 47
}
```
This feeds the reading-level-glossary and readability-rewriter stations.

### Implementation Notes
- classify-documents has NO runner script yet — it needs one written
- For NLP classification: use sbert embeddings (from previous station) +
  keyword matching against the spine mapping Excel + LLM classification via
  ollama or API call
- Output goes to _outbox as standard artifact JSON with all fields above
- The artifact JSON IS the paper's "passport" — every downstream station reads it

---

## Part B: Workflow Tracker (The Traveler)

### Concept
When a paper enters the pipeline, it gets a **traveler** — a tracking record
that follows it through every station. Like a manufacturing traveler sheet.
Each station stamps it: what was done, when, pass/fail, what's next.

### How It Works

1. Paper drops into `_front_door/_inbox`
2. Orchestrator creates a traveler JSON:
```json
{
  "paper_id": "FP-005",
  "title": "The Turtles and the Floor",
  "entered_at": "2026-06-17T02:30:00",
  "workflow": "first-article",
  "stations_required": [
    "sbert-embedder",
    "classify-documents",
    "7q-classifier",
    "claim-extractor",
    "paper-proof-grader",
    "reading-level-glossary",
    "readability-rewriter",
    "html-article"
  ],
  "stations_completed": [],
  "stations_failed": [],
  "current_station": null,
  "artifacts": {}
}
```

3. As each station processes the paper, it updates the traveler:
```json
{
  "stations_completed": [
    {
      "station": "sbert-embedder",
      "completed_at": "2026-06-17T02:30:15",
      "success": true,
      "artifact": "ART_20260617_023015__ST_049__FP-005.json",
      "summary": "384-dim embedding generated"
    },
    {
      "station": "classify-documents",
      "completed_at": "2026-06-17T02:30:22",
      "success": true,
      "artifact": "ART_20260617_023022__ST_050__FP-005.json",
      "summary": "Classified: foundational_paper, 6 tags, 6 spine domains"
    }
  ]
}
```

4. When all required stations are done, traveler status = "complete"
5. If a station fails, traveler shows what's missing → re-run just that station

### The Excel Tracker

One master Excel file: `PIPELINE_TRACKER.xlsx`

**Sheet 1: Paper Status** (one row per paper)
| Paper ID | Title | Workflow | Entered | sbert | classify | 7q | claims | proof | glossary | rewrite | html | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FP-005 | The Turtles and the Floor | first-article | 2026-06-17 | ✅ | ✅ | ✅ | ❌ | ⏳ | — | — | — | IN PROGRESS |
| MDA-001 | Story Introduction | mda-full | 2026-06-16 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | COMPLETE |

**Sheet 2: Station Output** (one row per station execution)
| Paper ID | Station | Timestamp | Success | Artifact File | Key Output |
|---|---|---|---|---|---|
| FP-005 | sbert-embedder | 2026-06-17 02:30 | YES | ART_...json | 384-dim vector |
| FP-005 | classify-documents | 2026-06-17 02:30 | YES | ART_...json | foundational_paper, 6 tags |

**Sheet 3: Classification Data** (one row per paper, all classification fields)
| Paper ID | doc_type | classification | tags | physics_score | theology_score | consciousness_score | evidence_status | word_count | reading_grade |

### Where This Lives
- Traveler JSONs: `X:\03_WORKFLOWS\travelers\{paper_id}.json`
- Master Excel: `X:\03_WORKFLOWS\PIPELINE_TRACKER.xlsx`
- Updated by: orchestrator/nlp_layer.py after each station completes

### Re-run / Loop-back Logic

Some papers need to go back through a station after downstream processing:
- Paper goes through classify → 7q → proof-grader → discovers missing axiom
- Needs to loop back to classify with new axiom context
- Traveler tracks re-runs: same station can appear twice with different timestamps
- Rule: station reads the LATEST artifact from upstream, not the first one

### Station Ordering (canonical pipeline order)

```
1. sbert-embedder         → vectorize text (always first)
2. classify-documents     → doc_type, tags, spine, dependencies
3. metadata-extractor     → title, author, date, word count, reading level
4. claim-extractor        → extract claims with 7Q pass
5. 7q-classifier          → run Q0-Q7 grid
6. paper-proof-grader     → grade proof structure, kill conditions
7. reading-level-glossary → find hard words, build definition set
8. readability-rewriter   → generate reading-level versions
9. fruits-spirit-canon    → run fruits vector analysis
10. html-article          → generate final HTML from template
```

Not all papers go through all stations. The workflow definition (in workflows/)
determines which stations a paper hits. "first-article" workflow hits 1-10.
"quick-classify" workflow hits just 1-3.

---

## What Codex Should Build

### For classify-documents:
1. Write `classify_runner.py` in `stations/classify-documents.station/`
   - Read input text from _inbox
   - Run classification across all 7 dimensions above
   - For now: use keyword matching + heuristics (no LLM required)
   - Match against spine mappings from `universal_domain_mapping_with_coherence.xlsx`
   - Output classification artifact JSON with all fields
2. Write `wiring_spec.json` for classify-documents
3. Generate config.json with template references

### For the tracker:
1. Write `tracker.py` in `orchestrator/`
   - Create traveler JSON when paper enters pipeline
   - Update traveler after each station completes
   - Aggregate all travelers into PIPELINE_TRACKER.xlsx
   - Can be called standalone: `python tracker.py --status` shows all papers
   - Can be called per-paper: `python tracker.py --paper FP-005` shows that paper's status
2. Write the Excel generation logic (openpyxl, 3 sheets as defined above)

### Reference Files
- Snapshot template: `templates/proof-explorer-fp-005-enhanced.html`
- Domain mapping: `templates/universal_domain_mapping_with_coherence.xlsx`
- Wiring spec schema: `WIRING_SPEC_SCHEMA.md`
- Station template: `stations/_shared/SSS_TEMPLATE_v1.py`


---

## Part C: Front Door System

### Concept
Some stations are useful standalone — you just want to drop a paper in and
get one thing back. Don't need the full pipeline. The PI suite already does
this with its 20_DROP_PAPER_ONLY folder pattern.

### Every station already has the bones
- `_inbox/` — drop files here
- `RUN.bat` — runs pipeline.py
- `_outbox/` — results land here

What's missing: a human-friendly front door that explains what to do.

### Front Door Pattern (add to key stations)

Create `FRONT_DOOR.bat` in the station root:
```bat
@echo off
echo ================================================
echo  SUMMARIZER — Drop papers, get summaries
echo ================================================
echo  Drop .md or .txt files into _inbox\ then press any key
echo  Results will appear in _outbox\
echo ================================================
pause
python pipeline.py
echo.
echo Done. Check _outbox\ for results.
pause
```

Create `FRONT_DOOR_README.md`:
```markdown
# Summarizer — Quick Use

1. Drop one or more .md/.txt files into `_inbox\`
2. Double-click `FRONT_DOOR.bat`
3. Results appear in `_outbox\`

## What You Get
- JSON artifact with summary, key claims, word count
- Original file archived to `_processed\`

## What This Station Does
Generates a concise summary of any paper or article.
```

### Stations That Need Front Doors
| Station | What you drop in | What you get back |
|---|---|---|
| summarizer | paper.md | summary artifact JSON |
| classify-documents | paper.md | classification (doc_type, tags, spine) |
| readability-rewriter | paper.md | 3 reading level versions (easy/med/hard) |
| 7q-classifier | paper.md | Q0-Q7 grid filled out |
| claim-extractor | paper.md | extracted claims with evidence |
| paper-proof-grader | paper.md | proof grade, kill conditions, FACTS |
| html-article | paper.md + classification JSON | formatted HTML page |
| sbert-embedder | paper.md | 384-dim embedding vector |
| whisper-transcribe | audio.mp3 | transcript.md |

### Fetch Source (optional)
Some front doors support `FETCH_SOURCE.txt` — put a folder path in there
and the BAT will copy files from that folder into _inbox before running.
Useful for "process everything in this Obsidian folder."

### Codex Task
For each station in the table above:
1. Create `FRONT_DOOR.bat` with the station name and description
2. Create `FRONT_DOOR_README.md` explaining input/output
3. Make sure `RUN.bat` calls `pipeline.py` correctly
4. Optionally add `FETCH_SOURCE.txt` support
