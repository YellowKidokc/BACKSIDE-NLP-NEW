---
uuid: 747845bc-1dfb-5950-b886-5ed67352d48d
title: 🚀 QUICK START GUIDE
author: David Lowe
type: analysis
created: '2025-11-22'
updated: '2025-11-22'
status: draft
file_path: 00_VAULT_SYSTEM\Analysis\TOOLS\QUICK_START.md
uuid_generated_at: '2025-11-22T01:23:02.954997'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

# 🚀 QUICK START GUIDE

## Run Analysis on Single Paper

```bash
cd D:\THEOPHYSICS_MASTER\_ANALYSIS\TOOLS
python master_orchestrator.py --paper P03
```

## Run Analysis on All Papers

```bash
python master_orchestrator.py --all
```

## Just Regenerate Dashboard

```bash
python master_orchestrator.py --dashboard
```

## Create Archive Snapshot

```bash
python master_orchestrator.py --archive "post_refinement"
```

---

## View Results

**Master Dashboard:**
```
D:\_ANALYSIS\00_CURRENT\MASTER_DASHBOARD.md
```

**Individual Papers:**
```
D:\_ANALYSIS\LOCAL_PAPERS\P03_Algorithm_Reality\LOCAL_DASHBOARD.md
```

**Archives:**
```
D:\_ANALYSIS\ARCHIVE\2025-11-16_initial\
```

---

## What Each Folder Does

- **00_CURRENT** - Always the latest results, start here
- **LOCAL_PAPERS** - Individual paper analysis folders
- **GLOBAL** - Cross-paper integration analyses
- **ARCHIVE** - Historical snapshots
- **TOOLS** - Scripts and templates

---

## Next Steps

1. ✅ P03 already analyzed (52.2% coherence)
2. Deploy to remaining papers: `--all`
3. Tune thresholds in config.json
4. Re-run to find breakthroughs
5. Create archive before major changes
