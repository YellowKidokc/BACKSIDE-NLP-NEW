# CODEX TASK 2: Wire Template References into Station Configs

## Context

Every station's `pipeline.py` uses `_resolve()` to find paths that work on both
the NAS (`X:\15_TEMPLATES\`) and in the repo (`templates/`). But most station
`config.json` files don't reference their templates yet.

The templates are all in `templates/` in this repo. The registry at
`templates/TEMPLATE_REGISTRY.json` maps each template to its station(s).
The wiring map at `stations/_shared/TEMPLATE_WIRING_MAP.md` shows connection status.

## What to do

### Step 1: Add TEMPLATES constant to pipeline.py Section 01

Every station's pipeline.py has this block in Section 01:
```python
MODELS    = _resolve("05_MODELS",    "models")
ENGINES   = _resolve("06_ENGINES",   "engines")
WORKFLOWS = _resolve("03_WORKFLOWS", "workflows")
EXPORTS   = _resolve("10_EXPORTS",   "exports")
```

Add this line after EXPORTS (if not already present):
```python
TEMPLATES = _resolve("15_TEMPLATES", "templates")
```

Do this for ALL stations that have template dependencies per the registry.

### Step 2: Add template paths to config.json

For each station listed in TEMPLATE_REGISTRY.json, add a `templates` key
to its config.json. Format:

```json
{
  "templates": {
    "input": {
      "lexicon": "paper_grader_lexicons_master_enhanced.xlsx",
      "rubric": "7Q Full Method Template.xlsx"
    },
    "output": {
      "html_report": "mda-grades.html",
      "export_excel": "Email Template.xlsx"
    }
  }
}
```

Use the TEMPLATE_REGISTRY.json to determine which templates go with which station.
Use the `direction` field to classify as input or output.
Use descriptive keys (not the filename — a short purpose name).

### Step 3: Sync NAS copies

After updating config.json in the repo, copy each updated config.json to the
corresponding NAS location:
- Repo: `stations/{name}/config.json`
- NAS:  `X:\04_STATIONS\{name}\config.json` (if accessible)

If you can't access X:, just update the repo copies. David will sync manually.

## Station-to-Template Mapping (from TEMPLATE_REGISTRY.json)

| Station | Input Templates | Output Templates |
|---|---|---|
| 7q-classifier | 7Q Full Method Template.xlsx, 7Q Full Method.xlsx | |
| 7q-engine | 7Q Full Method Template.xlsx, 7Q Full Method.xlsx | |
| apologetic-pipeline | APOLOGETICS_MASTER_INDEX.xlsx, bible_prophecies_organized.xlsx, CODEX_MASTER.xlsx, Jesus_miracles.xlsx, KJV_with_links_full.xlsx, PROPHECY_MASTER_DATABASE.xlsx, Bible Names.xlsx | |
| axioms | Theophysics_Axiom_Spine_Master (3) (2).xlsx | paper-grade-dashboard-template.html |
| claim-extractor | GEMINI_CLAIMS_EXTRACTION_2.xlsx | |
| coherence-discoherence | Coherence_Analysis_Master_v2.xlsx, Universal_7Facet_TruthLayer.xlsx, universal_domain_mapping_with_coherence.xlsx, Universal_TruthLayer_v2.xlsx, CDCM.xlsx | |
| contradiction-detector | bible_contradictions_HUD_tagged (1).xlsx, contradictingbiblecontradictions.xlsx | |
| contradiction-deep | bible_contradictions_HUD_tagged (1).xlsx, contradictingbiblecontradictions.xlsx | |
| fruits-spirit-canon | Fruits Template (1).xlsx | |
| graph-linker | Domain_Laws_Master_Mapping.xlsx, Sankey_connections_bible.xlsx, KJV_with_links_full.xlsx, Bible Names.xlsx | |
| master-equation-canon | Master_EQ_Chain.xlsx, MASTER_EQUATION_WORKBOOK.xlsx | |
| math-translation-layer | MATH_TRANSLATION_MASTER_FIXED.xlsx, MATH_TRANSLATION_TABLE_REAL.xlsx | |
| mda-citation-spine | citation_map.xlsx | mda-grades.html |
| mda-publication | Enhanced_CRM_Contact_List.xlsx | mda-proof-packet.html, EMAIL_CAMPAIGN_TRACKER.xlsx, OUTREACH_TRACKER.xlsx |
| obsidian-export | | Email Template.xlsx |
| paper-grader-nlp | paper_grader_lexicons_master_enhanced.xlsx | |
| paper-intelligence-suite | paper_intelligence.xlsx | PI_MDA-001-story-introduction.html |
| paper-proof-grader | paper_grader_lexicons_master_enhanced.xlsx | fp-005-enhanced.html |
| reading-level-glossary | paper_grader_lexicons_master_enhanced.xlsx | |
| readability-rewriter | paper_grader_lexicons_master_enhanced.xlsx | |
| theophysics-engine | TRUTH_ENGINE_MASTER_TEMPLATE.xlsx, Consciousness_Theories_Scorecard_All_Subtheories.xlsx | |
| timeline-verifier | Bible Timeline.xlsx | |

## Rules

1. Only modify config.json — don't change pipeline.py Section 07 (that's Task 1)
2. Only add the TEMPLATES constant to pipeline.py Section 01 — nothing else
3. Preserve all existing config.json fields — ADD the templates key, don't replace
4. If a station already has a templates key, verify it's correct and update if needed
5. Use the exact filenames from TEMPLATE_REGISTRY.json (including spaces and parens)
6. Template filenames are relative to the templates/ directory
