---
uid: DA-local-index
type: local-analytics
created: 2025-11-29
purpose: Local Data Analytics Dashboard - Copy this folder to any paper
---

# Local Data Analytics

> **This folder runs analytics for the current paper/section.**
> Copy `_Data_Analytics/` to any folder to enable local analytics.

---

## Quick Stats

```dataview
TABLE
  length(file.tags) AS "Tags",
  length(file.outlinks) AS "Links",
  file.size AS "Size"
FROM "."
WHERE file.name != this.file.name
SORT file.name ASC
```

---

## Structure

```
_Data_Analytics/
├── _Index.md                 # This file - local dashboard
├── Dashboards/               # Generated metrics & visualizations
│   ├── Statistics.md         # Counts: tags, equations, links
│   ├── Mermaid_Maps.md       # Visual connection diagrams
│   └── Compression.md        # Six-layer compression status
│
├── Scripts/                  # Python analytics (run from here)
│   ├── extract_all.py        # Master extraction script
│   ├── count_stats.py        # Generate statistics
│   └── build_mermaid.py      # Generate connection maps
│
├── Master_Sheet/             # LOCAL source of truth
│   ├── Definitions.json      # Definitions in this paper
│   ├── Axioms.json           # Axioms in this paper
│   ├── Equations.json        # Equations in this paper
│   ├── Tags.json             # Tags in this paper
│   └── Links.json            # Links in this paper
│
└── Exports/                  # Generated outputs
    ├── stats.json            # Raw statistics
    ├── summary.md            # Generated summary
    └── reference_entry.md    # Final 1-3 page compression
```

---

## The Six-Layer Compression Hierarchy

| Layer | Name | Purpose | Status |
|-------|------|---------|--------|
| 1 | **Seed** | Why the idea exists | [ ] |
| 2 | **Branches** | How the idea evolves | [ ] |
| 3 | **Bridges** | Causal/logical connections | [ ] |
| 4 | **Skeleton** | High-level structure | [ ] |
| 5 | **Condensed** | Atomic facts | [ ] |
| 6 | **Reference** | Final summary | [ ] |

---

## Meta-Statistics (Auto-Generated)

| Metric | Count |
|--------|-------|
| Total Files | `= length(filter(file.folder = this.file.folder))` |
| Total Tags | TBD |
| Total Equations | TBD |
| Total Definitions | TBD |
| Total Links | TBD |
| Word Count | TBD |

---

## How To Use

1. **Copy this entire `_Data_Analytics/` folder** to any paper folder
2. **Run `python Scripts/extract_all.py`** to populate Master_Sheet
3. **View Dashboards/** for visualizations
4. **Check Exports/** for generated summaries

---

## Links

- [[00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Data/Source/Theophysics_Assets/04_Analysis/Global_Data_Analytics_OLD/_Data_Analytics_Template/Dashboards/Statistics|View Statistics]]
- [[00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Data/Source/Theophysics_Assets/04_Analysis/Global_Data_Analytics_OLD/_Data_Analytics_Template/Dashboards/Mermaid_Maps|View Connection Maps]]
- [[00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Data/Source/Theophysics_Assets/04_Analysis/Global_Data_Analytics_OLD/_Data_Analytics_Template/Dashboards/Compression|View Six-Layer Status]]
- [[Master_Sheet/Definitions|Local Definitions]]
