---
uuid: 218f0363-30e0-5ebe-ad77-9c1e1cda32a7
title: FOLDER CLEANUP GUIDE
author: David Lowe
type: note
created: '2025-11-22'
updated: '2025-11-22'
status: draft
file_path: _DELETE\Word-ontology\FOLDER-CLEANUP-GUIDE.md
uuid_generated_at: '2025-11-22T01:23:47.700511'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

# FOLDER CLEANUP GUIDE

**Current Issue:** Word-ontology folder contains Obsidian plugin files mixed with ontology system files.

---

## What You Can DELETE

### Safe to Remove (Plugin-Related):

```
❌ DELETE THESE:
├── .git/                          (Git repository - not needed)
├── node_modules/                  (Node dependencies - huge, not needed)
├── classification.ts              (Plugin file)
├── database.ts                    (Plugin file)
├── esbuild.config.mjs            (Plugin file)
├── main.ts                        (Plugin file)
├── manifest.json                  (Plugin file)
├── package-lock.json              (Plugin file)
├── package.json                   (Plugin file)
├── profiles.ts                    (Plugin file)
├── settings.ts                    (Plugin file)
├── styles.css                     (Plugin file)
├── tsconfig.json                  (Plugin file)
├── types.ts                       (Plugin file)
├── ui/                            (Plugin folder)
├── version-bump.mjs              (Plugin file)
└── versions.json                  (Plugin file)
```

**Total size saved:** ~150-200 MB (mostly node_modules)

---

## What You Should KEEP

### Essential Ontology Files:

```
✅ KEEP THESE:
├── 00-SYSTEM-OVERVIEW.md          (System documentation)
├── QUICK-START.md                 (User guide)
├── TERM_MAPPING_ROSETTA_STONE.md  (Master reference)
├── SYSTEM-COMPLETE.md             (Complete docs)
├── ACTION-SUMMARY.md              (Status report)
├── AMBIENT-DECOHERENCE-INSIGHT.md (Your breakthrough)
├── LAUNCH-ONTOLOGY.bat            (Launcher script)
├── ontology-cli.py                (CLI program)
├── README.md                      (Can keep or replace)
│
├── Terms/                         (All term files)
│   ├── 01-Participatory-Actualization.md
│   ├── 02-Trinitarian-Actualization.md
│   ├── 05-Decoherence-S.md
│   └── 06-Grace-Function-G.md
│
├── Templates/                     (Template files)
│   └── new-term-template.md
│
├── Scripts/                       (Validation tools)
│   ├── validate_term.py
│   ├── requirements.txt
│   └── README.md
│
└── Word-Breakdowns/               (Knowledge breakdown)
    └── Knowledge.md
```

---

## Option 1: Clean Current Folder (Recommended)

**Batch script to delete unnecessary files:**

```batch
@echo off
echo Cleaning Word-ontology folder...
echo.

REM Delete plugin files
del /q classification.ts database.ts esbuild.config.mjs main.ts manifest.json
del /q package-lock.json package.json profiles.ts settings.ts styles.css
del /q tsconfig.json types.ts version-bump.mjs versions.json
del /q .gitignore

REM Delete folders
rmdir /s /q .git
rmdir /s /q node_modules
rmdir /s /q ui

echo.
echo ✅ Cleanup complete!
echo.
echo Remaining: Only ontology system files
pause
```

Save this as `CLEAN-FOLDER.bat` and run it.

---

## Option 2: Move to New Clean Folder

**Create fresh structure:**

```
D:\THEOPHYSICS_MASTER\Word-Ontology-Clean\
├── Core-Docs/
│   ├── 00-SYSTEM-OVERVIEW.md
│   ├── QUICK-START.md
│   ├── TERM_MAPPING_ROSETTA_STONE.md
│   ├── SYSTEM-COMPLETE.md
│   └── ACTION-SUMMARY.md
│
├── Terms/
│   └── (all .md files)
│
├── Templates/
│   └── new-term-template.md
│
├── Scripts/
│   └── (all Python files)
│
├── Insights/
│   └── AMBIENT-DECOHERENCE-INSIGHT.md
│
├── LAUNCH-ONTOLOGY.bat
└── ontology-cli.py
```

---

## What About .gitignore?

**If you want version control later, keep:**
- `.gitignore` (useful for Git)

**Otherwise, delete it.**

---

## Recommended Action

### Quick Clean (5 minutes):

```batch
cd D:\THEOPHYSICS_MASTER\Word-ontology

REM Delete the big stuff
rmdir /s /q node_modules
rmdir /s /q .git

REM Delete plugin files
del /q *.ts *.mjs *.json
del /q styles.css

REM Keep only .md, .py, .bat, .txt files
```

### Result:

```
Word-ontology/
├── [All .md documentation]
├── Terms/
├── Templates/
├── Scripts/
├── Word-Breakdowns/
├── LAUNCH-ONTOLOGY.bat
└── ontology-cli.py
```

**Clean, organized, ~200MB smaller.**

---

## Do You Want Me To:

1. **Create the cleanup script?** (`CLEAN-FOLDER.bat`)
2. **Move files to new clean folder?** (fresh structure)
3. **Just delete specific files?** (tell me which)

The plugin files are NOT needed for the ontology system — they were from a different project that happened to be in the same folder.

---

**Recommendation:** Run cleanup script to delete plugin files, keep only ontology system.
