---
uuid: 67fa5806-46ad-5a6b-948f-2ca49966a82a
title: 🎛️ ADMIN DASHBOARD
author: David Lowe
type: workflow
created: '2025-11-22'
updated: '2025-11-22'
status: draft
file_path: Logos zright\Meta\ADMIN_DASHBOARD.md
uuid_generated_at: '2025-11-22T01:23:48.195136'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

# 🎛️ ADMIN DASHBOARD
## Metadata Master Control Center

> **Internal use only** | All tags, links, stats, and organizational metadata

---

## 📊 **VAULT STATISTICS**

### **Paper Count & Status**
```dataview
TABLE WITHOUT ID
  rows.file.link AS "Papers",
  length(rows) AS "Count"
FROM "Papers"
WHERE file.name = "MOST-DEFINITIVE"
GROUP BY choice(contains(file.folder, "P11"), "✅ Ready", "📝 In Progress") AS "Status"
```

### **File Distribution**
```dataview
TABLE WITHOUT ID
  file.folder AS "Location",
  length(rows.file) AS "File Count"
FROM ""
WHERE file.name != "ADMIN_DASHBOARD"
GROUP BY file.folder
SORT length(rows.file) DESC
LIMIT 20
```

### **Total Word Count Estimate**
```dataview
TABLE WITHOUT ID
  sum(rows.file.size) AS "Total Size (bytes)"
FROM "Papers"
WHERE contains(file.name, "MOST-DEFINITIVE") OR contains(file.name, "LATEST-DRAFT")
```

---

## 🏷️ **TAG REGISTRY**

### **Paper Tags**
| Tag | Purpose | Usage |
|-----|---------|-------|
| `#logos/paper1` | Paper 1 references | Cross-reference to Logos Principle |
| `#logos/paper2` | Paper 2 references | Cross-reference to Quantum Bridge |
| `#logos/paper3` | Paper 3 references | Cross-reference to Algorithm of Reality |
| `#logos/paper4` | Paper 4 references | Cross-reference to Hard Problem |
| `#logos/paper5` | Paper 5 references | Cross-reference to Soul as Observer |
| `#logos/paper6` | Paper 6 references | Cross-reference to Physics of Principalities |
| `#logos/paper7` | Paper 7 references | Cross-reference to Grace Function |
| `#logos/paper8` | Paper 8 references | Cross-reference to Stretched-Out Heavens |
| `#logos/paper9` | Paper 9 references | Cross-reference to Moral Universe |
| `#logos/paper10` | Paper 10 references | Cross-reference to Creatio ex Silico |
| `#logos/paper11` | Paper 11 references | Cross-reference to Protocols for Validation |
| `#logos/paper12` | Paper 12 references | Cross-reference to Decalogue of Cosmos |

### **Theme Tags**
| Tag | Purpose |
|-----|---------|
| `#logos/theme/consciousness` | Consciousness-related content |
| `#logos/theme/quantum` | Quantum mechanics topics |
| `#logos/theme/grace` | Grace Function & negentropy |
| `#logos/theme/entropy` | Entropy & information theory |
| `#logos/theme/prophecy` | Prophecy correlations |
| `#logos/theme/ai` | Artificial intelligence topics |
| `#logos/theme/cosmology` | Cosmological models |
| `#logos/theme/theology` | Theological integrations |

### **Evidence Tags**
| Tag | Purpose |
|-----|---------|
| `#logos/evidence` | Base evidence tag |
| `#logos/evidence/experimental` | Laboratory experiments |
| `#logos/evidence/observational` | Field observations |
| `#logos/evidence/computational` | Computer simulations |
| `#logos/evidence/historical` | Historical data |
| `#logos/evidence/statistical` | Statistical analysis |

### **Source Tags**
| Tag | Purpose |
|-----|---------|
| `#logos/source/PEAR` | Princeton Engineering Anomalies Research |
| `#logos/source/GCP` | Global Consciousness Project |
| `#logos/source/Wolfram` | Wolfram computational results |
| `#logos/source/Literature` | Academic literature |
| `#logos/source/Biblical` | Scriptural sources |

### **Status Tags**
| Tag | Purpose |
|-----|---------|
| `#status/draft` | Work in progress |
| `#status/review` | Under review |
| `#status/ready` | Publication ready |
| `#status/published` | Already published |
| `#status/archived` | Historical/archived |

---

## 📁 **COMPLETE FILE INVENTORY**

### **All Papers (MOST-DEFINITIVE versions)**
```dataview
TABLE WITHOUT ID
  file.link AS "Paper",
  file.size AS "Size (bytes)",
  file.mtime AS "Last Modified",
  file.folder AS "Location"
FROM "Papers"
WHERE file.name = "MOST-DEFINITIVE"
SORT file.folder ASC
```

### **All Core Reference Documents**
```dataview
TABLE WITHOUT ID
  file.link AS "Document",
  file.size AS "Size (bytes)",
  file.mtime AS "Last Modified"
FROM "Library/Core"
SORT file.name ASC
```

### **All Experimental Protocols**
```dataview
TABLE WITHOUT ID
  file.link AS "Protocol",
  file.size AS "Size (bytes)",
  file.mtime AS "Last Modified"
FROM "Library/Experimental-Protocols"
WHERE file.name != "README"
SORT file.name ASC
```

### **All Evidence Files**
```dataview
TABLE WITHOUT ID
  file.link AS "Evidence File",
  file.folder AS "Bundle",
  file.mtime AS "Last Modified"
FROM "Library/Evidence-Bundles"
WHERE file.name != "README"
SORT file.mtime DESC
```

---

## 🔗 **CROSS-REFERENCE MAP**

### **Equation Compendium (Auto-Generated)**
> Lists all core equations defined in [[DEEP_LAWS_CANON]]. Add `tags: [equations]` to the frontmatter of any note containing a canonical equation definition to include it here.

```dataview
TABLE WITHOUT ID
  id AS "ID",
  symbolic_form AS "Symbolic Form",
  equation_name AS "Name",
  domain AS "Domain",
  related_laws AS "Related Laws"
FROM "Library/Core"
WHERE file.name = "DEEP_LAWS_CANON"
FLATTEN file.lists as item
WHERE item.id
WITH KEY "equation"
EXTRACT
  equation.id as id,
  equation.symbolic_form as symbolic_form,
  equation.equation_name as equation_name,
  equation.domain as domain,
  equation.related_laws as related_laws
```

---

### **Papers Citing Core Reference**
```dataview
TABLE WITHOUT ID
  file.link AS "Paper",
  length(file.outlinks) AS "Outgoing Links",
  length(file.inlinks) AS "Incoming Links"
FROM "Papers"
WHERE file.name = "MOST-DEFINITIVE"
SORT length(file.outlinks) DESC
```

### **Most Linked Documents**
```dataview
TABLE WITHOUT ID
  file.link AS "Document",
  length(file.inlinks) AS "Incoming Links",
  file.folder AS "Location"
FROM ""
WHERE file.name != "ADMIN_DASHBOARD" AND file.name != "000_START_HERE"
SORT length(file.inlinks) DESC
LIMIT 20
```

### **Orphaned Files (No Links)**
```dataview
LIST file.link
FROM ""
WHERE length(file.inlinks) = 0 AND length(file.outlinks) = 0
AND file.name != "ADMIN_DASHBOARD"
AND file.name != "README"
SORT file.folder ASC
```

---

## 📋 **PUBLICATION CHECKLIST**

### **Paper 1 - The Logos Principle**
- [ ] Final draft review
- [ ] Images placed and captioned
- [ ] Entropy disambiguation added
- [ ] Proleptic defense inserted
- [ ] References formatted
- [ ] Cover letter drafted

### **Paper 11 - Protocols for Validation**
- [x] Pre-registration specs complete
- [x] Falsification table added
- [x] Statistical design specified
- [x] OSF registration ready
- [ ] Cover letter drafted
- [ ] Journal selected

### **Paper 12 - The Decalogue of the Cosmos**
- [ ] Final synthesis complete
- [ ] All 11 laws integrated
- [ ] Appendix updated
- [ ] References compiled

---

## 🔍 **SEARCH SHORTCUTS**

### **Find All TODOs**
```dataview
TASK
WHERE !completed
```

### **Find All References to Specific Term**
Search in Obsidian:
- Entropy: `path:Papers/ "entropy"`
- Grace Function: `path:Papers/ "Grace Function"`
- Quantum Observer: `path:Papers/ "quantum observer"`
- Information Theory: `path:Papers/ "information theory"`

### **Find All Images**
```dataview
LIST
FROM "Papers" OR "Library"
WHERE contains(file.name, ".png") OR contains(file.name, ".jpg")
```

---

## 📊 **QUALITY METRICS**

### **Papers with Multiple Drafts**
```dataview
TABLE WITHOUT ID
  file.folder AS "Paper",
  length(rows.file) AS "Draft Count"
FROM "Papers"
WHERE contains(file.path, "05_Drafts")
GROUP BY file.folder
SORT length(rows.file) DESC
```

### **Recently Modified Files (Last 7 Days)**
```dataview
TABLE WITHOUT ID
  file.link AS "File",
  file.mtime AS "Modified",
  file.folder AS "Location"
FROM ""
WHERE file.mtime >= date(now) - dur(7 days)
AND file.name != "ADMIN_DASHBOARD"
SORT file.mtime DESC
```

### **Oldest Files (Needs Review?)**
```dataview
TABLE WITHOUT ID
  file.link AS "File",
  file.mtime AS "Last Modified",
  file.folder AS "Location"
FROM "Papers"
WHERE contains(file.path, "05_Drafts")
SORT file.mtime ASC
LIMIT 10
```

---

## 🎨 **VAULT CUSTOMIZATION**

### **Required Plugins**
| Plugin | Purpose | Status |
|--------|---------|--------|
| **Dataview** | Database queries & auto-lists | ✅ Installed |
| **Homepage** | Set 000_START_HERE as landing page | ✅ Installed |
| **Canvas** | Visual mind mapping | ✅ Installed |
| **Templater** | Advanced templates | ✅ Installed |
| **Kanban** | Project boards | ✅ Installed |

### **Custom CSS Snippets** (Optional)
- `theophysics-theme.css` - Brand colors & fonts
- `paper-print-view.css` - Print-friendly paper view
- `dashboard-layout.css` - Custom dashboard styling

### **Workspace Layouts**
- **Writing Mode**: Editor + file tree
- **Research Mode**: Editor + backlinks + graph
- **Dashboard Mode**: 000_START_HERE pinned + Canvas

---

## 🚀 **DISTRIBUTION PACKAGE STRUCTURE**

### **Files to Include in Distribution**
```
Theophysics-Research-Suite-v1.0/
├── 000_START_HERE.md ✅
├── ADMIN_DASHBOARD.md ✅
├── Papers/ ✅
├── Library/ ✅
├── Site/ ✅
├── .obsidian/
│   ├── plugins/ ✅ (include configs)
│   ├── snippets/ (optional custom CSS)
│   ├── themes/ (optional custom theme)
│   ├── app.json ✅
│   └── workspace.json ✅
└── README.md (installation guide)
```

### **Files to Exclude**
- `.obsidian/workspace.json` (user-specific)
- `.obsidian/cache/` (generated)
- `.trash/` (if any)
- Personal notes with sensitive data

---

## 📝 **TEMPLATE DEFINITIONS**

### **Paper Template**
Location: `Templates/paper-template.md` (coming soon)
- YAML frontmatter
- Standard sections
- Citation format
- Image placeholders

### **Evidence Template**
Location: `Templates/evidence-template.md` (coming soon)
- Evidence type taxonomy
- Data source fields
- Paper support links
- Tagging structure

### **Research Note Template**
Location: `Templates/research-note-template.md` (coming soon)
- Quick capture format
- Linking helpers
- Tag suggestions

---

## ⚙️ **MAINTENANCE TASKS**

### **Weekly**
- [ ] Review orphaned files
- [ ] Update publication checklist
- [ ] Check for broken links
- [ ] Archive old drafts

### **Monthly**
- [ ] Run full vault statistics
- [ ] Review tag usage
- [ ] Update cross-reference map
- [ ] Backup vault

### **Before Publication**
- [ ] Run quality metrics check
- [ ] Verify all images load
- [ ] Check all internal links
- [ ] Export final PDFs

---

## 🔐 **BACKUP & VERSION CONTROL**

### **Git Repository**
- Remote: (set up if needed)
- Branch: `main`
- Last commit: (track here)

### **Backup Schedule**
- Daily: Automatic OS backup
- Weekly: Manual archive
- Pre-publication: Full export

---

**Last Updated:** 2025-10-13

*This dashboard contains all organizational metadata. Use Dataview queries to power 000_START_HERE.md* 🎛️

