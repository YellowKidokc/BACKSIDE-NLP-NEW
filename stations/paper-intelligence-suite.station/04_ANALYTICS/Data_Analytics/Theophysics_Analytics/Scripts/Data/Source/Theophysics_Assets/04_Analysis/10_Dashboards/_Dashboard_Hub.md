---
uid: DASH-hub-001
type: hub
created: 2025-11-29
purpose: Central navigation for all analytics dashboards
---

# Dashboard Hub

> **Analytics Command Center** - Navigate to any dashboard from here.

---

## Primary Dashboards

### Core Metrics

| Dashboard | Purpose | Status |
|-----------|---------|--------|
| [[00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Data/Source/Theophysics_Assets/04_Analysis/10_Dashboards/Core_Metrics/MASTER_DASHBOARD\|Master Dashboard]] | Main analytics view | Active |
| [[Core_Metrics/Paper_Metrics\|Paper Metrics]] | Individual paper stats | Pending |
| [[Core_Metrics/Global_Metrics\|Global Metrics]] | Vault-wide aggregates | Pending |

### Coherence Analytics

| Dashboard | Purpose | Status |
|-----------|---------|--------|
| [[Coherence/Coherence_Dashboard\|Coherence Dashboard]] | Theory coherence scores | Pending |
| [[Coherence/Trinity_Heatmap\|Trinity Heatmap]] | Father/Son/Spirit balance | Pending |
| [[Coherence/Theory_Validation\|Theory Validation]] | Combined vs individual | Pending |

### Content Dashboards

| Dashboard | Purpose | Status |
|-----------|---------|--------|
| [[Content/Definitions_Dashboard\|Definitions]] | All definitions tracking | Pending |
| [[Content/Axioms_Dashboard\|Axioms]] | 11 Laws + axioms | Pending |
| [[Content/Claims_Dashboard\|Claims]] | All claims made | Pending |
| [[Content/Mathematics_Dashboard\|Mathematics]] | Equations & formulas | Pending |
| [[Content/References_Dashboard\|References]] | Citation tracking | Pending |

### Progress Tracking

| Dashboard | Purpose | Status |
|-----------|---------|--------|
| [[Progress/Growth_Tracker\|Growth Tracker]] | Content growth over time | Pending |
| [[Progress/Timeline_Dashboard\|Timeline]] | Chronological events | Pending |
| [[Progress/Breakthroughs_Dashboard\|Breakthroughs]] | Key insights | Pending |

---

## Highcharts Visualizations

### Available Charts

| Chart | Type | Description |
|-------|------|-------------|
| [[Charts/_Charts_Index\|Charts Index]] | - | All available charts |
| Paper Comparison | Column | Word counts across papers |
| Content Breakdown | Stacked Bar | Definitions/Axioms/Claims/Equations |
| Domain Radar | Radar | 10-domain coverage profile |
| Complexity Trend | Line | Reading level across papers |
| Coherence Scores | Bar | Per-paper coherence |

### Chart Switching

All charts use the same data structure for easy switching:

```javascript
// Switch between papers
loadChart('P01');  // Single paper
loadChart('all');  // All papers
loadChart('global');  // Global aggregates
```

---

## Data Sources

| Source | Location | Purpose |
|--------|----------|---------|
| Paper Metrics | `07_Data/metrics/paper_metrics.json` | Per-paper stats |
| Global Metrics | `07_Data/metrics/global_metrics.json` | Aggregated stats |
| Chart Data | `07_Data/metrics/chart_data.json` | Highcharts-ready |
| Raw Papers | `03_PUBLICATIONS/` | Source documents |

---

## Quick Links

### Analytics System

- [[Global_Data_Analytics/_Index\|Global Data Analytics]] - Main hub
- [[Global_Data_Analytics/Data_Analytics/Dashboards/_Analytics_Config\|Analytics Config]] - Toggle system
- [[Global_Data_Analytics/Global_Master_Sheet/_Index\|Master Sheet]] - Source of truth

### Components

- [[02_Foundations/_Index\|Atoms]] - 8 foundational concepts
- [[04_Integration/_Index\|Molecules]] - Synthesized concepts
- [[05_Doctrine/_Index\|Laws]] - Core principles
- [[06_Hubs/\|Concept Hubs]] - Topic aggregators

### System

- [[_Tag_Index\|Tags]] - Tag taxonomy
- [[_Master_MOC\|MOCs]] - Maps of Content
- [[01_Scripts/\|Scripts]] - Python analytics

---

## Workflow

### Generate Fresh Data

```bash
# 1. Extract metrics from all papers
cd 04_Analysis
python 01_Scripts/analysis/extract_metrics.py --all

# 2. Generate Highcharts (if script exists)
python 01_Scripts/charts/generate_charts.py

# 3. Refresh Obsidian - Dataview auto-updates
```

### View Data

1. **In Obsidian:** Open any dashboard for Dataview tables
2. **In Browser:** Open `10_Dashboards/Charts/*.html` for Highcharts
3. **Raw JSON:** Check `07_Data/metrics/*.json` for raw data

---

## Status

| Component | Status | Last Updated |
|-----------|--------|--------------|
| Metrics Extraction | Ready | 2025-11-29 |
| Paper Metrics | Pending | - |
| Global Metrics | Pending | - |
| Chart Data | Pending | - |
| Highcharts HTML | Pending | - |
