---
uid: MOC-master-001
type: moc
created: 2025-11-29
purpose: Master navigation hub for the entire Theophysics vault
---

# Theophysics Master MOC

> **Map of Content** - Your navigation hub for exploring the Theophysics knowledge system.

---

## Quick Navigation

| Destination | Purpose | Link |
|-------------|---------|------|
| Inventory | Current vault state | [[CENTRAL_INVENTORY]] |
| Atoms | Foundational concepts | [[MOC_Atoms\|Atoms MOC]] |
| Molecules | Synthesized concepts | [[MOC_Molecules\|Molecules MOC]] |
| Laws | Doctrinal principles | [[MOC_Laws\|Laws MOC]] |
| Analytics | Data dashboards | [[MOC_Analytics\|Analytics MOC]] |

---

## By Domain

### Physics Path
```
[[08_Tags/Physics/_Physics_Tags|Physics Tags]] → [[Entropy (S)]] → [[Grace (G)]] → [[Coherence (C)]]
```

### Theology Path
```
[[08_Tags/Theology/_Theology_Tags|Theology Tags]] → [[Logos (L)]] → [[Trinity]] → [[Resurrection (R)]]
```

### Bridge Path (Theophysics)
```
[[08_Tags/Theophysics/_Theophysics_Tags|Theophysics Tags]] → [[Information (I)]] → [[Form (F)]] → [[Dynamics (D)]]
```

---

## By Component Type

### Atoms (Foundations)
```dataview
TABLE coherence_score AS Coherence, trinity_aspect AS Trinity
FROM "02_Foundations"
WHERE type = "atom"
SORT coherence_score DESC
```

### Molecules (Integrations)
```dataview
TABLE coherence_score AS Coherence
FROM "04_Integration"
WHERE type = "molecule"
SORT coherence_score DESC
```

### Laws (Doctrines)
```dataview
TABLE validation_status AS Status, coherence_score AS Coherence
FROM "05_Doctrine"
WHERE type = "law"
SORT coherence_score DESC
```

### Hubs (Concepts)
```dataview
LIST
FROM "05_Hubs"
WHERE type = "hub"
```

---

## By Phase

| Phase | Folder | Purpose | Count |
|-------|--------|---------|-------|
| 1 | Assets | Raw sources | TBD |
| 2 | Foundations | Atoms | 8 |
| 3 | Analysis | Exploration | TBD |
| 4 | Integration | Molecules | 0 |
| 5 | Doctrine | Laws | 1 |
| 6 | Publication | Papers | TBD |

---

## System Components

### Dashboards
- [[00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Data/Source/Theophysics_Assets/04_Analysis/04_Dashboards/_Index|Dashboard Index]]
- [[00_VAULT_SYSTEM/Global_Analytics/ARCHIVE/Gemini_delete/03_Docs/03_Concepts/Atoms]] - Atom tracking
- [[00_VAULT_SYSTEM/Global_Analytics/ARCHIVE/Gemini_delete/03_Docs/03_Concepts/Molecules]] - Molecule tracking
- [[03_PUBLICATIONS/10-Laws/Miscellaneous/Laws]] - Law tracking
- [[Validation_Dashboard]] - Metrics
- [[00_VAULT_SYSTEM/Global_Analytics/ARCHIVE/Gemini_delete/03_Docs/03_Concepts/Trinity_Heatmap]] - Trinity scores

### Tags
- [[_Tag_Index|Tag Index]]
- [[_Physics_Tags|Physics Tags]]
- [[_Theology_Tags|Theology Tags]]
- [[_Theophysics_Tags|Theophysics Tags]]

### Templates
- [[00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Data/Source/Theophysics_Assets/04_Analysis/03_Templates/02_Foundation_Template|Atom Template]]
- [[00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Data/Source/Theophysics_Assets/04_Analysis/03_Templates/04_Integration_Template|Molecule Template]]
- [[00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Data/Source/Theophysics_Assets/04_Analysis/03_Templates/05_Doctrine_Template|Law Template]]

---

## Vault Statistics

```dataviewjs
const atoms = dv.pages('"02_Foundations"').where(p => p.type == "atom").length;
const molecules = dv.pages('"04_Integration"').where(p => p.type == "molecule").length;
const laws = dv.pages('"05_Doctrine"').where(p => p.type == "law").length;
const hubs = dv.pages('"05_Hubs"').length;

dv.table(["Component", "Count"], [
    ["Atoms", atoms],
    ["Molecules", molecules],
    ["Laws", laws],
    ["Hubs", hubs],
    ["**Total**", atoms + molecules + laws + hubs]
]);
```
