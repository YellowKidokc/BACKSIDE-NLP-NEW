# SESSION HANDOFF — June 17, 2026
## Paper-Proof-Grader Deep Dive + Codex Status
**POF 2828 | For next Opus session**

---

## CODEX TASK STATUS

### Task 1: Section 07 Wiring Specs ✅ COMPLETE
- 20 wiring_spec.json files generated across all stations with runner scripts
- Automator ready: `python wire_section07.py wire --all` patches all 19 stations
- **NOT YET RUN** — David needs to execute the automator after review
- Location: `D:\GitHub\BACKSIDE-NLP-NEW\wire_section07.py`

### Task 2: Template Config Wiring ✅ COMPLETE
- templates key added to config.json for 22 stations
- TEMPLATES constant added to pipeline.py Section 01
- HTML templates added to TEMPLATE_REGISTRY.json (6 new entries)
- Missing template `paper-grade-dashboard-template.html` copied to templates/

### Task 3: Classification + Tracker + Front Doors — IN PROGRESS (sent to Codex)
- Prompt: `CODEX_CLASSIFY_AND_TRACKER_PROMPT.md`
- Part A: classify_runner.py for classify-documents station
  - 7 classification dimensions: doc_type, classification string, tags,
    spine_mappings, dependency_chain, word_count, reading_level
  - Uses keyword matching against universal_domain_mapping Excel
- Part B: tracker.py (the traveler system)
  - Paper gets tracking JSON, each station stamps it
  - Master Excel: PIPELINE_TRACKER.xlsx (3 sheets: status, output, classification)
  - Handles re-runs / loop-backs
- Part C: Front door BAT scripts for 9 key stations
  - Drop-and-run pattern from PI suite's 20_DROP_PAPER_ONLY

---

## INFRASTRUCTURE COMPLETED THIS SESSION

### sbert-embedder.station — WIRED AND SYNCED
- Section 07 wired to InfinityClient from sbert_runner.py
- Lazy client init (created once per run, reused across files)
- Per-file embedding via Infinity HTTP at 192.168.1.177:7997
- Optional Qdrant upsert (only if qdrant_collection set in config)
- Config merged: SSS fields + real Infinity/Qdrant/model settings
- JOB_CARDS → WORKFLOWS rename applied throughout
- Synced: NAS (X:\04_STATIONS) and repo (D:\GitHub\BACKSIDE-NLP-NEW\stations)
- **TO TEST:** Drop .md file in _inbox, run pipeline.py, check _outbox

### wire_section07.py — AUTOMATOR BUILT
- `python wire_section07.py scan` — shows all 63 stations: stub/wired/spec status
- `python wire_section07.py wire --all` — patches all stations with wiring specs
- `python wire_section07.py wire --station X --force` — rewire one station
- Uses section markers (# 07_PROCESS → # 08_ARTIFACTS) to find/replace
- Creates .py.bak07 backup before patching
- Auto-syncs NAS → repo after patching

### Template Registry Updated
- 6 HTML output templates added to TEMPLATE_REGISTRY.json
- paper-grade-dashboard-template.html copied from axioms.station to templates/
- All referenced template files verified present in repo

---

## THE NEXT JOB: Paper-Proof-Grader

### The Problem
The paper-proof-grader is the most complex station. It has 4 separate Python
scripts that need to run in sequence, each doing a different analysis layer.
The current Section 07 is a passthrough stub — none of these scripts are called.

Additionally, the claim extraction quality needs work:
- Currently generates ~700 claims per paper (too many, too noisy)
- Claims lack academic rigor — not enough formal variable creation
- Need claims cross-referenced against formal elements:
  - 10 Master Equation variables (χ factors)
  - 188 axiom spine chain nodes
  - Lean 4 verified theorems
  - 16 formal structure types

### The 4 Runner Scripts

#### 1. formal_verification.py (159 lines)
**What:** Regex-matches claims against 6 Lean theorem families
**Input:** List of claim dicts (from claim-extractor upstream)
**Output:** Per-claim verification status + Lean file dependencies
**Entry:** `attach_verification(claims)` — library call
**Theorem families:** closure, sign_invariance, targeted_openness,
external_grace, necessary_conditions, justice_mercy_transform
**Status values:** proven | formalizable | counterexample_found |
bridge_only | speculative | not_attempted

#### 2. expanded_report.py (292 lines)
**What:** Aggregates all analysis into a graded report (0-100 score)
**Input:** `*.paper-grade.json` files from OUTPUT directory
**Output:** Markdown + HTML report (executive verdict, score dashboard,
claim architecture, strongest/weakest claims, repair targets)
**Entry:** `load_reports()` → `md_report(data)` / `html_report(data)`
**Grade tiers:**
- 85+ = "Strong release candidate"
- 70-84 = "Promising with repair targets"
- 55-69 = "Useful draft, needs reviewer hardening"
- <55 = "High-risk draft, needs structural repair"

#### 3. fruits_of_spirit_bridge.py (630 lines)
**What:** Scores paper text against 9 fruit anchors + 8 anti-fruit anchors
**Input:** Paper text files (.md, .txt, .html)
**Output:** Per-file fruit scores (JSON, CSV, Excel), batch summary
**Entry:** `main()` via CLI with `--input` path
**Dependencies:**
- Truth Engine scripts at `\\dlowenas\github\Truth Engine (1)\scripts\fruits_pipeline`
- Lexicon Excel: `paper_grader_lexicons_master_enhanced.xlsx`
- Optional SBERT for semantic scoring
**Fruit anchors:** love, joy, peace, patience, kindness, goodness,
faithfulness, gentleness, self_control
**Anti anchors:** coercion, domination, deception, fear_shame,
fragmentation, exploitation, certainty_inflation, tribal_binding

#### 4. run_axiom_7q_stations.py (1074 lines) — THE MONSTER
**What:** Axiom detection (10 rule families) + 7Q forward/reverse scoring
**Input:** `*.claim-audit.csv` files from claim-extractor upstream
**Output:** Per-paper manifests, batch index (JSON, MD, Excel, HTML)
**Entry:** `main()` via CLI, optional `--openai` for o3 verification
**Axiom rules:** truth_ground, information_substrate, observer_actualization,
grace_repair, entropy_thermo, falsifiability, master_equation,
moral_conservation, experiment_protocol, model_coupling
**Key outputs:**
- Forward 7Q score (0-7 per claim)
- Reverse status (proven/supported/speculative)
- Axiom chain-node hit counts
- Optional OpenAI verification alongside deterministic scoring

### Dependency Chain (execution order)

```
UPSTREAM (must complete before paper-proof-grader runs):
  claim-extractor → produces claim-audit CSVs
  sbert-embedder  → produces embeddings (for semantic scoring)

PAPER-PROOF-GRADER INTERNAL SEQUENCE:
  Step 1: run_axiom_7q_stations.py
          Reads claim-audit CSVs, runs axiom + 7Q scoring
          Produces: per-paper manifests with scored claims

  Step 2: formal_verification.py
          Takes scored claims from Step 1
          Attaches Lean theorem dependencies and verification status

  Step 3: fruits_of_spirit_bridge.py
          Reads original paper text (not claims)
          Produces: 9-dim fruit vector + anti-fruit scores

  Step 4: expanded_report.py
          Aggregates Steps 1-3 into final grade (0-100)
          Produces: MD report, HTML report, grade JSON

OUTPUT: paper-grade JSON + expanded report → fills snapshot template
```

### What Needs to Happen Next Session

#### Phase 1: Read and understand each script deeply
- Read all 4 scripts line by line (not just headers)
- Identify what config values each expects
- Map every input/output format
- Find hardcoded paths that need to become config references

#### Phase 2: Fix claim quality
- Current: ~700 claims per paper, too noisy, not academic enough
- Need: fewer, higher-quality claims with formal variable names
- Claims should reference Master Equation variables by name
- Claims should map to axiom chain nodes explicitly
- Add academic variable creation (define terms before using them)
- Consider: claim deduplication / consolidation pass

#### Phase 3: Cross-reference claims against formal elements
- Master Equation canon: tag claims touching χ variables
- Axiom spine: tag claims grounding in the 188 nodes
- Lean theorems: attach machine-verified proof references
- May need new stations: master-equation-claims, axiom-chain-claims
  (these exist as shells — master-equation-canon.station, etc.)

#### Phase 4: Wire Section 07
- Write orchestration logic in process_one() that calls all 4 scripts
- Handle the internal dependency chain (Steps 1→2→3→4)
- Make sure each step's output feeds the next
- Config needs: output_dir, reference paths, lexicon path, Truth Engine path

#### Phase 5: End-to-end test
- Pick one paper (FP-005 or an MDA article)
- Run it through: sbert → classify → claim-extract → paper-proof-grader
- Check the output against the snapshot template fields
- Verify the grade score makes sense

---

## PIPELINE FLOW (canonical order, updated)

```
1. sbert-embedder         ✅ WIRED    → 384-dim embedding vector
2. classify-documents     🔨 CODEX    → doc_type, tags, spine, dependencies
3. metadata-extractor     ⬜ STUB     → title, author, date, word count
4. claim-extractor        ⬜ STUB     → extracted claims with 7Q pass
5. 7q-classifier          ⬜ HAS SPEC → Q0-Q7 grid filled
6. master-equation-canon  ⬜ HAS SPEC → claims tagged against χ variables
7. paper-proof-grader     🎯 NEXT     → grade, kill conditions, FACTS, report
8. reading-level-glossary ⬜ STUB     → hard words, definitions
9. readability-rewriter   ⬜ STUB     → 3 reading level versions
10. fruits-spirit-canon   ⬜ HAS SPEC → 9-dim fruit vector
11. html-article          ⬜ STUB     → final HTML from snapshot template
```

---

## FILE LOCATION MAP (same as previous handoff)

| What | Where |
|------|-------|
| Master repo | D:\GitHub\BACKSIDE-NLP-NEW |
| Stations (live, NAS) | X:\04_STATIONS (\\192.168.2.50\brain\04_STATIONS) |
| Templates | D:\GitHub\BACKSIDE-NLP-NEW\templates\ |
| Automator | D:\GitHub\BACKSIDE-NLP-NEW\wire_section07.py |
| Codex prompts | D:\GitHub\BACKSIDE-NLP-NEW\CODEX_*.md |
| Task queue | D:\GitHub\BACKSIDE-NLP-NEW\00_README_FOR_CODEX.md |
| Paper grader (live) | X:\04_STATIONS\paper-proof-grader.station\ |
| Paper grader (repo) | D:\GitHub\BACKSIDE-NLP-NEW\stations\paper-proof-grader.station\ |
| Snapshot template | templates\proof-explorer-fp-005-enhanced.html |
| Lexicon Excel | templates\paper_grader_lexicons_master_enhanced.xlsx |
| Domain mapping | templates\universal_domain_mapping_with_coherence.xlsx |
| Obsidian vault | O:\_Theophysics_v5 |
| PostgreSQL | 192.168.1.177:2665 |
| Infinity (SBERT) | 192.168.1.177:7997 |
| Qdrant (vectors) | 192.168.1.177:6333 |

---

## SESSION STATS — June 17, 2026

- sbert-embedder Section 07 fully wired and synced (NAS + repo)
- wire_section07.py automator built and tested (scan works, wire ready)
- 63 stations scanned: 62 stubs, 1 wired
- Config merged for sbert-embedder (SSS + real Infinity/Qdrant settings)
- JOB_CARDS → WORKFLOWS rename applied to sbert-embedder
- TEMPLATE_REGISTRY.json updated with 6 HTML output templates
- paper-grade-dashboard-template.html copied to templates/
- CODEX_WIRING_PROMPT.md written → Task 1 complete (20 specs generated)
- CODEX_TEMPLATE_WIRING_PROMPT.md written → Task 2 complete
- CODEX_CLASSIFY_AND_TRACKER_PROMPT.md written → Task 3 sent to Codex
- 00_README_FOR_CODEX.md updated with full task queue
- Paper-proof-grader: all 4 scripts read and mapped
- Dependency chain documented (4-step internal sequence)
- Snapshot template fully analyzed (6 framework layers, 7 data sections)
- Classification schema defined (7 dimensions for classify-documents)
- Front door concept captured (PI suite 20_DROP pattern)
- Workflow traveler concept captured (tracking JSON + master Excel)
