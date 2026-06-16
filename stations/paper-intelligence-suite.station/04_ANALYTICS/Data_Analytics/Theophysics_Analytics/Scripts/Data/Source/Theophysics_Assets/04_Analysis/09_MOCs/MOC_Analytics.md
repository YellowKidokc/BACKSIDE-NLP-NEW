---
uid: MOC-analytics-001
type: moc
created: 2025-11-29
purpose: Navigation hub for all analytics and dashboards
---

# Analytics MOC

> **Data & Metrics** - Understanding your knowledge system through data.

---

## Dashboard Navigation

### Core Dashboards (04_Dashboards/)

| Dashboard | Purpose | Key Metric |
|-----------|---------|------------|
| [[00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Data/Source/Theophysics_Assets/04_Analysis/04_Dashboards/Atoms\|Atoms]] | Track atomic concepts | Coherence score |
| [[00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Data/Source/Theophysics_Assets/04_Analysis/04_Dashboards/Molecules\|Molecules]] | Track synthesized concepts | Predictive power |
| [[00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Data/Source/Theophysics_Assets/04_Analysis/04_Dashboards/Laws\|Laws]] | Track doctrinal laws | Validation status |
| [[Validation_Dashboard\|Validation]] | SIS/LCS/SRI metrics | Quality scores |
| [[00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Data/Source/Theophysics_Assets/04_Analysis/04_Dashboards/Trinity_Heatmap\|Trinity Heatmap]] | Trinity aspect distribution | Balance |

### Analytics Dashboards

| Dashboard | Purpose |
|-----------|---------|
| [[Vault_Statistics\|Vault Statistics]] | Overall vault health |
| [[Graph_Analytics\|Graph Analytics]] | Link density & structure |
| [[Growth_Tracker\|Growth Tracker]] | Content over time |
| [[Coherence_Trends\|Coherence Trends]] | Quality evolution |

---

## Key Metrics Explained

### Coherence Score (0-1)
Measures internal consistency and integration:
- **0.9+** = Highly coherent, production-ready
- **0.7-0.9** = Good coherence, minor refinement needed
- **0.5-0.7** = Moderate coherence, needs work
- **<0.5** = Low coherence, major revision needed

### Trinity Coherence Index
Balance across Father/Son/Spirit aspects:
- Ideal: Balanced scores across all three
- Warning: Any single aspect >0.8 while others <0.3

### SIS (Semantic Integrity Score)
How well concepts maintain meaning across contexts.

### LCS (Logical Consistency Score)
Absence of contradictions within the system.

### SRI (Scar Resolution Index)
How well apparent contradictions have been resolved.

---

## Quick Stats

```dataviewjs
const all = dv.pages('"02_Foundations" OR "04_Integration" OR "05_Doctrine" OR "05_Hubs"');
const withCoherence = all.where(p => p.coherence_score);
const avgCoherence = withCoherence.values.reduce((sum, p) => sum + p.coherence_score, 0) / withCoherence.length;

dv.table(["Metric", "Value"], [
    ["Total Knowledge Notes", all.length],
    ["Notes with Coherence Score", withCoherence.length],
    ["Average Coherence", avgCoherence.toFixed(3)],
    ["Highest Coherence", Math.max(...withCoherence.values.map(p => p.coherence_score)).toFixed(3)],
    ["Lowest Coherence", Math.min(...withCoherence.values.map(p => p.coherence_score)).toFixed(3)]
]);
```

---

## Component Health

```dataviewjs
const atoms = dv.pages('"02_Foundations"').where(p => p.type == "atom");
const molecules = dv.pages('"04_Integration"').where(p => p.type == "molecule");
const laws = dv.pages('"05_Doctrine"').where(p => p.type == "law");
const hubs = dv.pages('"05_Hubs"');

dv.table(["Component", "Count", "Status"], [
    ["Atoms", atoms.length, atoms.length >= 8 ? "✓ Complete" : "⚠ Incomplete"],
    ["Molecules", molecules.length, molecules.length > 0 ? "✓ Started" : "○ Not started"],
    ["Laws", laws.length, laws.length > 0 ? "✓ Started" : "○ Not started"],
    ["Hubs", hubs.length, hubs.length >= 5 ? "✓ Core complete" : "⚠ Incomplete"]
]);
```

---

## Links to Analytics Tools

### Python Scripts
- `analyze_coherence.py` - Coherence calculation
- `cooccurrence_analyzer.py` - Concept co-occurrence
- `validation_scaffold.py` - Metric generation

### External Integrations
- PostgreSQL database connection
- API server at localhost:8001
