---
uid: DA-local-master-sheet
type: index
created: 2025-11-29
purpose: Local Master Sheet - Source of truth for this paper
---

# Local Master Sheet

> **Source of truth** for extracted data from this paper/section.

---

## Contents

| File | Purpose | Status |
|------|---------|--------|
| `Equations.json` | All equations extracted | [ ] Run extract |
| `Axioms.json` | All axioms extracted | [ ] Run extract |
| `Definitions.json` | All definitions extracted | [ ] Run extract |
| `Tags.json` | All tags used | [ ] Run extract |
| `Links.json` | All links (internal/external) | [ ] Run extract |
| `stats.json` | Summary statistics | [ ] Run extract |

---

## How to Populate

```bash
cd Scripts/
python run_all.py
```

This will:
1. Scan parent folder for .md files
2. Extract equations, axioms, definitions, tags, links
3. Save to JSON files here
4. Update dashboards

---

## Data Flows UP

```
Local Master_Sheet/
       │
       ▼
Global_Master_Sheet/
       │
       ▼
Dashboards (Global)
```

When ready, promote local data to Global by:
1. Running validation
2. Copying verified items to Global_Master_Sheet

---

*Empty until `extract_all.py` is run*
