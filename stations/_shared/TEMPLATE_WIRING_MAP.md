# TEMPLATE WIRING MAP
## BACKSIDE NLP System — Station ↔ Template Connections
**Generated: 2026-06-15**

---

## EXCEL TEMPLATES (INPUT — lexicons, rubrics, data)

| Template | Station(s) | Direction | Status |
|---|---|---|---|
| `paper_grader_lexicons_master_enhanced.xlsx` | paper-grader-nlp, paper-proof-grader, reading-level-glossary, readability-rewriter | INPUT | **CRITICAL** — synonyms, lexicons, grading vocabulary |
| `Fruits Template (1).xlsx` | fruits-spirit-canon | INPUT | Fruit/anti-fruit canonical definitions |
| `paper_intelligence.xlsx` | paper-intelligence-suite | INPUT/OUTPUT | Paper grading rubric template |
| `Theophysics_Axiom_Spine_Master (3) (2).xlsx` | axioms | INPUT | 188 axiom spine reference |
| `bible_contradictions_HUD_tagged (1).xlsx` | contradiction-detector, contradiction-deep | INPUT | Tagged contradiction corpus |
| `CDCM.xlsx` | coherence-discoherence | INPUT | TBD — needs verification |
| `Email Template.xlsx` | (email workflows) | OUTPUT | Email export formatting |
| `OpenIntel_Master_Data_Template.xlsx` | (data business) | OUTPUT | OpenIntel data export format |


## HTML TEMPLATES (OUTPUT — export formatting)

| Template | Station(s) | Direction | Status |
|---|---|---|---|
| `fp-005-enhanced.html` | paper-proof-grader | OUTPUT | Proof explorer visual |
| `mda-grades.html` | mda-citation-spine, paper-grader-nlp | OUTPUT | MDA grading dashboard |
| `mda-proof-packet.html` | mda-publication | OUTPUT | MDA proof packet export |
| `PI_MDA-001-story-introduction.html` | paper-intelligence-suite | OUTPUT | PI HTML report |
| `paper-3-DAvid.html` | html-article | OUTPUT | Article shell template |
| `paper-4-GTQ-05*.html` | html-article | OUTPUT | GTQ article template |
| `paper-5-*.html` | html-article | OUTPUT | Physics article template |
| `index.html` / `2index.html` | series-flow-auditor | OUTPUT | Site index pages |
| `seven-qs-proof-packet-template.html` | series-flow-auditor | OUTPUT | 7Q proof packet |
| `paper-grade-dashboard-template.html` | axioms | OUTPUT | Axiom dashboard |

## MARKDOWN TEMPLATES (INPUT — structure scaffolding)

| Template | Station(s) | Direction |
|---|---|---|
| `axiom_template.md` | axioms, obsidian-export | INPUT |
| `theorem_template.md` | master-equation-canon | INPUT |
| `claim_template.md` | claim-extractor | INPUT |
| `definition_template.md` | reading-level-glossary | INPUT |
| `evidence_template.md` | fact-verifier | INPUT |
| `mapping_template.md` | graph-linker | INPUT |
| `operator_template.md` | operators-canon | INPUT |
| `field_template.md` | theophysics-engine | INPUT |
| `boundary_condition_template.md` | paper-proof-grader | INPUT |


## WIRING STATUS — WHAT'S CONNECTED vs BROKEN

### CONNECTED (template path in config.json or pipeline.py)
- fruits-spirit-canon → Fruits Template ✅ (template in station folder)
- html-article → prompts/ folder ✅ (17 run_prompt.md files)
- series-flow-auditor → templates/ folder ✅ (proof packet, chart block)
- math-layer / math-translation-layer → templates/ folder ✅ (reading levels, prompts)

### NOT YET WIRED (template exists but station doesn't reference it)
- paper-grader-nlp → needs `paper_grader_lexicons_master_enhanced.xlsx` path in config
- paper-proof-grader → needs lexicon + `fp-005-enhanced.html` output template
- reading-level-glossary → needs lexicon for synonym lookup
- readability-rewriter → needs lexicon for vocabulary alternatives
- contradiction-detector → needs `bible_contradictions_HUD_tagged.xlsx`
- contradiction-deep → needs same
- mda-citation-spine → needs `mda-grades.html` output template
- mda-publication → needs `mda-proof-packet.html` output template
- axioms → needs `Theophysics_Axiom_Spine_Master.xlsx` + dashboard template

### CRITICAL INPUT PATH
```
NAS:    \\192.168.2.50\brain\15_TEMPLATES\paper_grader_lexicons_master_enhanced.xlsx
X:      X:\15_TEMPLATES\paper_grader_lexicons_master_enhanced.xlsx
Repo:   15_TEMPLATES\ (needs to be added to repo or referenced via _resolve shim)
```

### RESOLUTION PATTERN
Station config.json should reference templates via the `_resolve` shim:
```json
{
  "templates": {
    "lexicon": "15_TEMPLATES/paper_grader_lexicons_master_enhanced.xlsx",
    "output_html": "15_TEMPLATES/mda-grades.html"
  }
}
```
The `_resolve("15_TEMPLATES", "templates")` shim in pipeline.py handles NAS vs repo paths.

## NEXT STEPS
1. Add `templates` key to config.json for every station that uses one
2. Copy critical Excel templates into repo (or add _resolve path)
3. Verify each station's section 08 (ARTIFACTS) writes to _outbox using the correct template
4. Run end-to-end test: drop file in _inbox → check _outbox output matches template
