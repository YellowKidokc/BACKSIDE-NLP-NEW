# Finalized 04_Analysis Folder Structure

**Date:** 2025-11-29
**Status:** AUTHORITATIVE - This is the target structure
**Purpose:** Clean, scalable analytics system for Theophysics vault

---

## Target Structure

```
04_Analysis/
│
├── 00_CURRENT/                          # Status & Inventory
│   ├── CENTRAL_INVENTORY.md             # Master tracking file
│   ├── FINALIZED_STRUCTURE.md           # This document
│   └── CHANGELOG.md                     # Version history
│
├── 01_Scripts/                          # Python analytics scripts
│   ├── analysis/                        # Analysis scripts
│   │   ├── analyze_coherence.py
│   │   ├── extract_metrics.py           # NEW: Core metrics extraction
│   │   ├── cooccurrence_analyzer.py
│   │   └── matter_analysis.py
│   │
│   ├── utilities/                       # Utility scripts
│   │   ├── auto_linker.py
│   │   ├── concept_hub_generator.py
│   │   ├── duplicate_finder.py
│   │   ├── uid_generator.py
│   │   ├── vault_refresh.py
│   │   └── validation_scaffold.py
│   │
│   ├── charts/                          # NEW: Highcharts integration
│   │   ├── generate_charts.py           # Generate chart data
│   │   ├── chart_templates.py           # Reusable chart configs
│   │   └── export_to_highcharts.py      # Export JSON for Highcharts
│   │
│   └── api/                             # API scripts
│       └── api_server.py
│
├── 02_Foundations/                      # Atoms (8 total)
│   ├── _Index.md                        # Atom registry
│   ├── Entropy (S).md
│   ├── Grace (G).md
│   ├── Coherence (C).md
│   ├── Information (I).md
│   ├── Form (F).md
│   ├── Dynamics (D).md
│   ├── Resurrection (R).md
│   └── Logos (L).md
│
├── 03_Templates/                        # All templates
│   ├── README.md
│   ├── 01_Asset_Template.md
│   ├── 02_Foundation_Template.md
│   ├── 03_Analysis_Template.md
│   ├── 04_Integration_Template.md
│   ├── 05_Doctrine_Template.md
│   ├── 06_Publication_Template.md
│   └── yaml_frontmatter_template.md
│
├── 04_Integration/                      # Molecules (synthesized)
│   ├── _Index.md                        # Molecule registry
│   └── [Molecule files as created]
│
├── 05_Doctrine/                         # Laws
│   ├── _Index.md                        # Laws registry
│   └── LAW_Master_Equation.md
│
├── 06_Hubs/                             # Concept Hubs
│   ├── README.md
│   ├── Grace.md
│   ├── Entropy.md
│   ├── Trinity.md
│   ├── Resurrection.md
│   └── Coherence.md
│
├── 07_Data/                             # Raw data storage
│   ├── README.md
│   ├── profiles/                        # Paper profiles
│   ├── correlations/                    # Correlation data
│   ├── metrics/                         # NEW: Core metrics JSON
│   │   ├── paper_metrics.json           # Per-paper metrics
│   │   ├── global_metrics.json          # Global metrics
│   │   └── chart_data.json              # Ready for Highcharts
│   └── master_sheets/
│
├── 08_Tags/                             # Tag Taxonomy
│   ├── _Tag_Index.md                    # Master taxonomy
│   ├── Physics/
│   │   └── _Physics_Tags.md
│   ├── Theology/
│   │   └── _Theology_Tags.md
│   ├── Theophysics/
│   │   └── _Theophysics_Tags.md
│   ├── Information/
│   │   └── _Information_Tags.md
│   └── Philosophy/
│       └── _Philosophy_Tags.md
│
├── 09_MOCs/                             # Maps of Content
│   ├── _Master_MOC.md
│   ├── MOC_Atoms.md
│   ├── MOC_Molecules.md
│   ├── MOC_Laws.md
│   └── MOC_Analytics.md
│
├── 10_Dashboards/                       # NEW: Consolidated dashboards
│   ├── _Dashboard_Hub.md                # Main entry point
│   │
│   ├── Core_Metrics/                    # Core analytics
│   │   ├── MASTER_DASHBOARD.md          # Main dashboard
│   │   ├── Paper_Metrics.md             # Per-paper stats
│   │   └── Global_Metrics.md            # Vault-wide stats
│   │
│   ├── Coherence/                       # Coherence analytics
│   │   ├── Coherence_Dashboard.md
│   │   ├── Trinity_Heatmap.md
│   │   └── Theory_Validation.md
│   │
│   ├── Content/                         # Content dashboards
│   │   ├── Definitions_Dashboard.md
│   │   ├── Axioms_Dashboard.md
│   │   ├── Claims_Dashboard.md
│   │   ├── Mathematics_Dashboard.md
│   │   └── References_Dashboard.md
│   │
│   ├── Progress/                        # Progress tracking
│   │   ├── Growth_Tracker.md
│   │   ├── Timeline_Dashboard.md
│   │   └── Breakthroughs_Dashboard.md
│   │
│   └── Charts/                          # NEW: Highcharts outputs
│       ├── _Charts_Index.md
│       ├── chart_paper_comparison.html
│       ├── chart_coherence_trend.html
│       └── chart_domain_distribution.html
│
├── Global_Data_Analytics/               # GLOBAL HUB (source of truth)
│   ├── _Index.md
│   │
│   ├── Data_Analytics/
│   │   ├── _Index.md
│   │   ├── Mechanisms/                  # Data gathering
│   │   │   ├── Atoms/
│   │   │   ├── Molecules/
│   │   │   ├── Tags/
│   │   │   ├── MOCs/
│   │   │   └── Hubs/
│   │   │
│   │   └── Dashboards/
│   │       └── _Analytics_Config.md     # Toggle system
│   │
│   └── Global_Master_Sheet/             # SOURCE OF TRUTH
│       ├── _Index.md
│       ├── Definitions/
│       ├── Axioms/
│       ├── Claims/
│       ├── Evidence/
│       ├── Mathematics/
│       ├── References/
│       ├── Tags/
│       ├── Timeline/
│       ├── Breakthroughs/
│       ├── Links/
│       ├── Theories/                    # NEW: Extracted theories
│       ├── Validations/                 # NEW: Coherence validations
│       └── Reports/                     # NEW: Generated reports
│
├── _Archive/                            # Old/deprecated files
│   └── [archived content]
│
└── _System/                             # System documentation
    ├── README.md
    ├── Workflow.md
    ├── Prompts.md
    └── Tag_Reference.md
```

---

## Key Changes from Current State

### Consolidations

| Old Location | New Location | Reason |
|--------------|--------------|--------|
| `04_Dashboards/` | `10_Dashboards/` | Cleaner numbering |
| `02_System/` | `_System/` | System files shouldn't clutter numbering |
| `05_Hubs/` | `06_Hubs/` | Better flow after Integration |
| `06_Wizards/` | `_Archive/` or remove | Wizards can be CLI/scripts |
| `Data Analytics/` (root) | `Global_Data_Analytics/` | Consolidated |
| `Master Sheets/` (root) | `Global_Master_Sheet/` | Consolidated |
| `GLOBAL/` | `_Archive/` | Obsolete |
| `ARCHIVE/` | `_Archive/` | Consolidated |

### New Additions

| Folder | Purpose |
|--------|---------|
| `01_Scripts/charts/` | Highcharts integration scripts |
| `07_Data/metrics/` | Core metrics JSON storage |
| `10_Dashboards/Charts/` | Rendered Highcharts outputs |
| `Global_Master_Sheet/Theories/` | Extracted theory files |
| `Global_Master_Sheet/Validations/` | Coherence validation results |
| `Global_Master_Sheet/Reports/` | Generated reports |

---

## Core Metrics System

### Paper-Level Metrics

Every paper generates these metrics:

```json
{
  "paper_id": "P01",
  "paper_name": "The Logos Principle",
  "metrics": {
    "basic": {
      "word_count": 15234,
      "unique_words": 3456,
      "character_count": 87654,
      "paragraph_count": 234,
      "sentence_count": 567,
      "page_count_estimate": 45,
      "words_per_page": 338,
      "average_sentence_length": 26.8,
      "reading_time_minutes": 61
    },
    "content": {
      "definitions_count": 45,
      "axioms_count": 11,
      "claims_count": 78,
      "equations_count": 23,
      "references_count": 67,
      "internal_links_count": 34,
      "external_links_count": 12
    },
    "complexity": {
      "flesch_reading_ease": 32.5,
      "flesch_kincaid_grade": 14.2,
      "vocabulary_richness": 0.227,
      "technical_term_density": 0.15
    },
    "coherence": {
      "coherence_score": 0.85,
      "domain_coverage": 8,
      "trinity_balance": {
        "father": 0.8,
        "son": 0.7,
        "spirit": 0.6
      }
    },
    "domains": {
      "G": 0.75,
      "M": 0.45,
      "E": 0.82,
      "S": 0.38,
      "T": 0.91,
      "K": 0.67,
      "R": 0.54,
      "Q": 0.89,
      "F": 0.62,
      "C": 0.95
    }
  }
}
```

### Global Metrics

Aggregated across all papers:

```json
{
  "scope": "global",
  "papers_analyzed": 12,
  "metrics": {
    "totals": {
      "total_words": 182808,
      "total_unique_words": 12456,
      "total_pages": 540,
      "total_definitions": 320,
      "total_axioms": 45,
      "total_claims": 567,
      "total_equations": 234
    },
    "averages": {
      "avg_words_per_paper": 15234,
      "avg_definitions_per_paper": 26.7,
      "avg_coherence_score": 0.78
    },
    "coherence": {
      "global_coherence": 0.82,
      "combined_vs_individual": "+12%",
      "domain_distribution": {...}
    }
  }
}
```

---

## Highcharts Integration

### Chart Types Available

| Chart Type | Purpose | Data Source |
|------------|---------|-------------|
| **Bar Chart** | Paper comparison | `paper_metrics.json` |
| **Line Chart** | Coherence trends | `coherence_history.json` |
| **Pie Chart** | Domain distribution | `domain_scores.json` |
| **Heatmap** | Trinity balance | `trinity_metrics.json` |
| **Radar Chart** | Multi-domain comparison | `domain_scores.json` |
| **Treemap** | Content breakdown | `content_metrics.json` |

### Switchable Data Pattern

```javascript
// Same chart config, different data
const chartConfig = {
  chart: { type: 'column' },
  title: { text: '' },  // Set dynamically
  xAxis: { categories: [] },  // Set from data
  series: []  // Set from data
};

// Switch data source
function loadChartData(source) {
  // source: 'P01', 'P02', ..., 'global'
  const data = metrics[source];
  updateChart(chartConfig, data);
}
```

### Export Pipeline

```
Python Script                  JSON Files                    Highcharts
extract_metrics.py  →  07_Data/metrics/*.json  →  10_Dashboards/Charts/*.html
```

---

## Dashboard Hierarchy

### Main Entry Points

1. **`_Dashboard_Hub.md`** - Master navigation
2. **`MASTER_DASHBOARD.md`** - Quick stats overview
3. **`Global_Metrics.md`** - Full vault analysis

### Dataview + Highcharts Hybrid

Dashboards work two ways:

1. **In Obsidian:** Dataview queries show data in markdown tables
2. **Exported:** JSON feeds Highcharts for visual charts

```markdown
## Word Counts by Paper

```dataview
TABLE
  metrics.basic.word_count as "Words",
  metrics.basic.page_count_estimate as "Pages"
FROM "03_PUBLICATIONS/COMPLETE_LOGOS_PAPERS_FINAL"
WHERE type = "paper"
SORT paper_id ASC
```

**[View Chart](Charts/chart_paper_comparison.html)** ← Links to Highcharts version
```

---

## Next Steps

1. [ ] Clean up current scattered folders
2. [ ] Create missing folders from this structure
3. [ ] Move files to correct locations
4. [ ] Implement `extract_metrics.py` script
5. [ ] Generate initial metrics JSON
6. [ ] Create Highcharts templates
7. [ ] Build master dashboard

---

## Notes for Auto

This structure supports:
- Python integration via JSON in `07_Data/metrics/`
- Highcharts via exported HTML in `10_Dashboards/Charts/`
- Same metrics, switchable views
- Easy to add new papers
- Scalable to multiple vaults
