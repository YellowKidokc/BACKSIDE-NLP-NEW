---
uid: DASH-master-001
type: dashboard
created: 2025-11-29
updated: 2025-11-29
scope: global
data_source: 07_Data/metrics/chart_data.json
---

# Master Analytics Dashboard

> **The Command Center** - Real-time metrics across all 12 Logos Papers.

---

## Quick Stats

| Metric | Value | Trend |
|--------|-------|-------|
| **Total Words** | `= this.total_words` | - |
| **Total Pages** | `= this.total_pages` | - |
| **Papers Analyzed** | 12 | - |
| **Definitions** | `= this.total_definitions` | - |
| **Axioms** | `= this.total_axioms` | - |
| **Avg Reading Level** | Grade `= this.avg_grade_level` | - |

---

## Paper Overview

### Word Counts by Paper

```dataviewjs
// This would be replaced by actual Highcharts embed
const chartContainer = dv.el("div", "", {
  attr: {
    id: "chart-word-counts",
    style: "height: 300px; border: 1px solid #ccc; border-radius: 8px; display: flex; align-items: center; justify-content: center; background: #f5f5f5;"
  }
});

chartContainer.innerHTML = `
<div style="text-align: center; color: #666;">
  <p><strong>Word Counts Chart</strong></p>
  <p>Run <code>python extract_metrics.py --all</code> to generate data</p>
  <p>Then open <a href="Charts/chart_paper_comparison.html">Highcharts View</a></p>
</div>
`;
```

**Data Table:**

```dataview
TABLE WITHOUT ID
  file.name as "Paper",
  metrics.basic.word_count as "Words",
  metrics.basic.page_count_estimate as "Pages",
  metrics.basic.reading_time_minutes as "Read Time (min)"
FROM "03_PUBLICATIONS/COMPLETE_LOGOS_PAPERS_FINAL"
WHERE type = "paper"
SORT file.name ASC
```

---

## Content Analysis

### Definitions, Axioms, Claims, Equations

```dataviewjs
const chartContainer = dv.el("div", "", {
  attr: {
    id: "chart-content",
    style: "height: 300px; border: 1px solid #ccc; border-radius: 8px; display: flex; align-items: center; justify-content: center; background: #f5f5f5;"
  }
});

chartContainer.innerHTML = `
<div style="text-align: center; color: #666;">
  <p><strong>Content Breakdown Chart</strong></p>
  <p>Shows: Definitions | Axioms | Claims | Equations per paper</p>
  <p><a href="Charts/chart_content_comparison.html">Open Highcharts View</a></p>
</div>
`;
```

**Summary:**

| Category | Total | Avg/Paper | Top Paper |
|----------|-------|-----------|-----------|
| Definitions | - | - | - |
| Axioms | - | - | - |
| Claims | - | - | - |
| Equations | - | - | - |
| References | - | - | - |

---

## Domain Distribution

### 10-Domain Coverage (G-M-E-S-T-K-R-Q-F-C)

```dataviewjs
const chartContainer = dv.el("div", "", {
  attr: {
    id: "chart-domains",
    style: "height: 350px; border: 1px solid #ccc; border-radius: 8px; display: flex; align-items: center; justify-content: center; background: #f5f5f5;"
  }
});

chartContainer.innerHTML = `
<div style="text-align: center; color: #666;">
  <p><strong>Domain Radar Chart</strong></p>
  <p>G=Grace | M=Mass | E=Energy | S=Entropy | T=Time</p>
  <p>K=Knowledge | R=Revelation | Q=Quantum | F=Faith | C=Coherence</p>
  <p><a href="Charts/chart_domain_radar.html">Open Highcharts View</a></p>
</div>
`;
```

**Domain Scores (Global Average):**

| Domain | Symbol | Score | Description |
|--------|--------|-------|-------------|
| Grace | G | - | Divine favor, mercy, blessing |
| Mass/Moral | M | - | Physical and moral momentum |
| Energy | E | - | Electromagnetic, power, force |
| Entropy | S | - | Disorder, sin, decay |
| Time/Truth | T | - | Temporal, eternal, chronology |
| Knowledge | K | - | Epistemology, information |
| Revelation | R | - | Divine disclosure, prophecy |
| Quantum | Q | - | Wave function, entanglement |
| Faith | F | - | Trust, belief, confidence |
| Coherence | C | - | Consciousness, integration |

---

## Complexity Analysis

### Reading Level Across Papers

```dataviewjs
const chartContainer = dv.el("div", "", {
  attr: {
    id: "chart-complexity",
    style: "height: 250px; border: 1px solid #ccc; border-radius: 8px; display: flex; align-items: center; justify-content: center; background: #f5f5f5;"
  }
});

chartContainer.innerHTML = `
<div style="text-align: center; color: #666;">
  <p><strong>Complexity Trend Chart</strong></p>
  <p>Flesch Reading Ease | Grade Level</p>
  <p><a href="Charts/chart_complexity.html">Open Highcharts View</a></p>
</div>
`;
```

**Complexity Metrics:**

| Paper | Reading Ease | Grade Level | Tech Density |
|-------|--------------|-------------|--------------|
| P01 | - | - | - |
| P02 | - | - | - |
| ... | - | - | - |

---

## Coherence Metrics

### Lowe's Coherence Lagrangian

$$L_{LC} = \chi(t) \cdot \left(\frac{d}{dt}\sum domains\right)^2 - S \cdot \chi(t)$$

```dataviewjs
const chartContainer = dv.el("div", "", {
  attr: {
    id: "chart-coherence",
    style: "height: 300px; border: 1px solid #ccc; border-radius: 8px; display: flex; align-items: center; justify-content: center; background: #f5f5f5;"
  }
});

chartContainer.innerHTML = `
<div style="text-align: center; color: #666;">
  <p><strong>Coherence Scores Chart</strong></p>
  <p>Individual paper coherence vs Combined framework</p>
  <p><a href="Charts/chart_coherence.html">Open Highcharts View</a></p>
</div>
`;
```

**Coherence Summary:**

| Metric | Value |
|--------|-------|
| Global Coherence (χ) | - |
| Average Individual | - |
| Combined Improvement | - |
| Entropy (S) | - |

---

## View Selector

Switch between different data views:

| View | Description | Link |
|------|-------------|------|
| **Single Paper** | Deep dive into one paper | [[Paper_Metrics]] |
| **Paper Comparison** | Side-by-side analysis | [[Paper_Comparison]] |
| **Global Overview** | Full vault metrics | [[Global_Metrics]] |
| **Domain Analysis** | 10-domain deep dive | [[Domain_Analysis]] |
| **Coherence Report** | Theory validation | [[Coherence_Report]] |

---

## Highcharts Gallery

All charts available for export:

| Chart | Type | Data Source | Status |
|-------|------|-------------|--------|
| Word Counts | Column | paper_metrics.json | Pending |
| Content Breakdown | Stacked Bar | paper_metrics.json | Pending |
| Domain Radar | Radar/Spider | chart_data.json | Pending |
| Complexity Trend | Line | paper_metrics.json | Pending |
| Coherence Comparison | Bar | global_metrics.json | Pending |
| Page Distribution | Pie | paper_metrics.json | Pending |
| Trinity Balance | Heatmap | domain_profiles | Pending |

---

## Data Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                      DATA PIPELINE                              │
│                                                                 │
│   12 Papers (P01-P12)                                          │
│         │                                                       │
│         ▼                                                       │
│   ┌─────────────────────┐                                      │
│   │  extract_metrics.py │  ← Run: python extract_metrics.py    │
│   └─────────────────────┘                                      │
│         │                                                       │
│         ▼                                                       │
│   ┌─────────────────────┐                                      │
│   │ 07_Data/metrics/    │                                      │
│   │ ├── paper_metrics   │  ← Per-paper JSON                    │
│   │ ├── global_metrics  │  ← Aggregated JSON                   │
│   │ └── chart_data      │  ← Highcharts-ready JSON             │
│   └─────────────────────┘                                      │
│         │                                                       │
│    ┌────┴────┐                                                 │
│    ▼         ▼                                                 │
│ Dataview   Highcharts                                          │
│ (Obsidian) (HTML/JS)                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Quick Actions

- **Generate Metrics:** `python 01_Scripts/analysis/extract_metrics.py --all`
- **View Raw Data:** Open `07_Data/metrics/chart_data.json`
- **Generate Charts:** `python 01_Scripts/charts/generate_charts.py`
- **Refresh Dashboard:** Dataview auto-refreshes on file changes

---

## Last Updated

- **Metrics Generated:** Not yet run
- **Charts Generated:** Pending
- **Dashboard Refreshed:** 2025-11-29

---

## Related

- [[_Dashboard_Hub]] - Main navigation
- [[Global_Metrics]] - Full global analysis
- [[Paper_Metrics]] - Individual paper details
- [[00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Data/Source/Theophysics_Assets/Dashboards/Coherence_Dashboard]] - Theory validation
- [[_Analytics_Config]] - Toggle analytics
