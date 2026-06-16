# CODEX TASK: Paper Grader End-to-End Workflow
## POF 2828 | June 16, 2026

### Goal
Wire the paper grader as a complete workflow inside `paper-intelligence-suite.station/15_PAPER_GRADER/`.
Input: a paper (markdown or HTML). Output: one Excel workbook with all scores.

### What exists
The 4 scripts are in `15_PAPER_GRADER/`:
1. `run_axiom_7q_stations.py` — reads claim-audit CSVs, matches against 188 axiom chain nodes, scores 7Q forward/reverse, optional OpenAI o3 verification
2. `formal_verification.py` — library (not CLI), entry: `attach_verification(claims)`, regex-matches claims against 6 Lean theorem families
3. `fruits_of_spirit_bridge.py` — reads raw paper text, scores fruit/anti-fruit/grounding/contradiction/propaganda, semantic anchor scoring
4. `expanded_report.py` — reads `*.paper-grade.json`, generates expanded review MD + HTML

### What's missing
A. **No claim extraction step.** The axiom-7Q script expects pre-extracted claim-audit CSVs. The claim extractor is at `X:\04_STATIONS\claim-extractor.station\extract.py` — it splits papers by section, chunks into 20-500 char blocks, classifies as definition/theorem/prediction/axiom/evidence/theological. That needs to run FIRST.

B. **No orchestration.** The 4 scripts don't call each other. Need a `workflow.py` that:
   1. Takes a paper path as input
   2. Runs claim extraction → produces claim-audit CSV
   3. Runs axiom-7Q stations on the CSV
   4. Runs formal verification on the claims (library call, not CLI)
   5. Runs fruits-of-spirit bridge on the original paper text
   6. Runs expanded report
   7. Consolidates ALL outputs into one Excel workbook

C. **No unified Excel output.** Each script writes its own format. Need one workbook with sheets:
   - Summary (paper ID, overall grade, key metrics)
   - Claims (every extracted claim with classification, 7Q scores, axiom hits, formal status)
   - Axiom Coverage (which chain nodes were hit, which weren't)
   - Fruits Profile (fruit/anti-fruit/grounding/contradiction/propaganda scores)
   - Semantic Anchors (per-fruit alignment scores)
   - Formal Verification (Lean status per claim family)
   - Repair Targets (top weaknesses, recommended fixes)

D. **Lexicon path.** The fruits bridge should load terms from the master lexicon at:
   `\\dlowenas\h_hp\Desktop\Combine\paper_grader_lexicons_master_COMBINED.xlsx`
   Update `fruits_of_spirit_config.json` to point there.

### Execution order
```
paper.md
  ↓
[1] extract.py → claims.csv
  ↓
[2] run_axiom_7q_stations.py → axiom_7q.json
  ↓
[3] formal_verification.attach_verification(claims) → claims + formal layer
  ↓
[4] fruits_of_spirit_bridge.py → fruits_scores.json
  ↓
[5] expanded_report.py → expanded_review.md + .html
  ↓
[6] consolidate → PAPER_GRADE_{paper_id}.xlsx
```

### Config
- Claim extraction config (signals, min/max length) is in `X:\04_STATIONS\claim-extractor.station\config.json`
- Axiom registry source: `REFERENCE/canonical_chain_nodes.psv` (copy or symlink from paper-proof-grader.station)
- Axiom source HTMLs: `REFERENCE/axiom_sequence_sources/` (same)
- Lexicon: `\\dlowenas\h_hp\Desktop\Combine\paper_grader_lexicons_master_COMBINED.xlsx`

### Test
Run end-to-end on one paper from `INPUT/` (any GTQ article).
The test passes when:
1. No crashes
2. Excel workbook is produced with all 7 sheets populated
3. Claims are actual sentences (not section dumps or tree diagrams)
4. 7Q scores are populated for every claim
5. At least some axiom chain nodes get matched
6. Fruits scores are non-zero

### Deliverables
1. `15_PAPER_GRADER/workflow.py` — the orchestrator
2. `15_PAPER_GRADER/RUN_PAPER_GRADE.bat` — one-click runner
3. Updated `fruits_of_spirit_config.json` with lexicon path
4. Copy or symlink REFERENCE data into 15_PAPER_GRADER
5. One test output Excel workbook proving it works
