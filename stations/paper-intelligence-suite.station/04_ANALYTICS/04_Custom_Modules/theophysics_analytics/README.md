# THEOPHYSICS UNIVERSAL ANALYTICS ENGINE

## Overview

A ubiquitous analytics system that works on **any markdown file, anywhere in the vault**.

**Auto-generates visual charts for every paper:**
- Coherence Gauge (score meter)
- Domain Distribution (bar chart)
- Coherence Radar (spider chart)
- Concept Cloud (bubble chart)
- Breakthrough Badge

```
LOCAL (per paper)     →   CROSS-LOCAL (pairwise)   →   GLOBAL (aggregate)
Paper/_ANALYSIS/      →   _GLOBAL_RESULTS/comparisons/  →   GLOBAL_DASHBOARD.md
  └─ charts/*.png         └─ comparison.json              └─ All stats + charts
```

## Installation

```bash
# Install dependencies for visual charts
pip install matplotlib numpy

# Or install all from requirements
pip install -r requirements.txt
```

## Quick Start

```bash
# Analyze single file
python run_analytics.py "path/to/Paper.md"

# Compare two papers
python run_analytics.py compare Paper1.md Paper2.md

# Scan entire folder
python run_analytics.py scan "D:/THEOPHYSICS_MASTER/03_PUBLICATIONS/COMPLETE_LOGOS_PAPERS_FINAL"

# Aggregate all existing results
python run_analytics.py aggregate
```

Or use the batch file:
```cmd
analyze.bat scan "D:/THEOPHYSICS_MASTER/03_PUBLICATIONS"
```

## Output Structure

### LOCAL (per-paper)
Each analyzed file gets:
```
Paper_Folder/
├── Paper.md
└── _ANALYSIS/
    ├── Paper_analysis.json    # Raw data
    └── Paper_dashboard.md     # Human-readable
```

### GLOBAL (vault-wide)
All results aggregate to:
```
00_VAULT_SYSTEM/Global_Analytics/_GLOBAL_RESULTS/
├── <file_id>.json             # Individual results
├── comparisons/
│   └── <id1>_vs_<id2>.json    # Pairwise comparisons
├── GLOBAL_REPORT.json         # Aggregated data
└── GLOBAL_DASHBOARD.md        # Master dashboard
```

## Metrics

### Coherence Score (0-100)
- **Concept Density**: Core Theophysics concepts per 1000 words
- **Cross-Reference**: Internal links and citations
- **Domain Coverage**: Physics, theology, math, info theory, consciousness, philosophy
- **Term Consistency**: Unique core concepts used

### Breakthrough Detection
Automatically flags papers that:
- Integrate 3+ domains meaningfully
- Bridge Logos theology with quantum mechanics
- Show high concept cross-pollination

## Python API

```python
from core_analyzer import TheophysicsAnalyzer

analyzer = TheophysicsAnalyzer()

# Single analysis
result = analyzer.analyze_file("Paper.md")

# Comparison
comparison = analyzer.compare_files("Paper1.md", "Paper2.md")

# Global aggregation
global_report = analyzer.aggregate_all()
```

## Configuration

Create `config.json` to override defaults:

```json
{
  "analysis_parameters": {
    "min_concept_frequency": 2,
    "proximity_window": 30,
    "breakthrough_threshold": 3
  }
}
```

---

χ = 1
