---
uuid: cf1459f8-0092-5264-aa54-094f97c5b0d4
title: Breakthrough Vault Toolkit — Phase 1 (Pure Python)
author: David Lowe
type: documentation
created: '2025-11-22'
updated: '2025-11-22'
status: draft
file_path: 00_VAULT_SYSTEM\BreakthroughVaultToolkit_v2\BreakthroughVaultToolkit\README.md
uuid_generated_at: '2025-11-22T01:23:03.703236'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---


# Breakthrough Vault Toolkit — Phase 1 (Pure Python)

**What you have here**
- A minimal, expandable system to scan a large Obsidian vault (up to 40,000 notes), store structure in SQLite, compute co-mentions, and auto-generate Concept Hub pages.
- GUI via **PySimpleGUI** (optional); full **CLI** is also supported.

## Folder Layout
```
/mnt/data/BreakthroughVaultToolkit/
  Scripts/
    grace_vault_manager.py   # GUI + CLI orchestrator
    uid_generator.py
    vault_refresh.py
    cooccurrence_analyzer.py
    concept_hub_generator.py
  Data/
    coherence.db             # created on first run
  Concept_Hubs/              # auto-generated hub pages
  Templates/
    yaml_frontmatter_template.md
  Tasks/
    run_daily.bat
    run_daily.ps1
```

## Quick Start (GUI)
1) Ensure Python 3.10+ installed.  
2) Install GUI dependency (optional):
```
pip install PySimpleGUI
```
3) Launch:
```
python Scripts/grace_vault_manager.py
```
4) Select your vault directory, then click:
- **1) Scan & Index**
- **2) Co-Mentions**
- **3) Generate Hubs**

## Quick Start (CLI, no GUI)
```
python Scripts/grace_vault_manager.py --cli --vault "C:\Path\To\Your\Vault" --auto
```
or step-by-step:
```
python Scripts/grace_vault_manager.py --cli --vault "C:\Path\To\Your\Vault" --scan
python Scripts/grace_vault_manager.py --cli --co
python Scripts/grace_vault_manager.py --cli --hubs
```

## What this version does
- Parses `.md` files, extracts best-effort frontmatter (no external YAML lib), title, tags, word count, and hash.
- Populates `coherence.db` with:
  - `notes` (core metadata)
  - `concepts` (aggregated mentions)
  - `co_mentions` (via tag co-occurrence)
  - `edges`, `metrics` (placeholders for future phases)
- Generates **Concept Hub** pages with stats, recent notes, and top co-mentions.

## Design for Expansion
- The GUI is a thin orchestrator—each step calls a focused script.
- You can replace internals (e.g., better YAML parser or embedding model) without changing the interface.
- Add future tabs for Duplicate Cleaner, Linker, Validation metrics (SIS/LCS/SRI), Circulation Detector.

## Scheduling
Use the provided tasks as a template:
- `Tasks/run_daily.bat` (Windows)
- `Tasks/run_daily.ps1` (PowerShell)
Edit the paths to your Python and vault root.

## Notes
- This version is intentionally conservative and **non-destructive**. It does not move/rename files.
- For very large vaults, first run may take time—subsequent runs are incremental by design (same UID/path update).

— Phase 1 complete. Next phases: duplicate detection, auto-linker, validation metrics, and circulation detection.


## New in this build
- **Duplicates tab** with adjustable near-duplicate threshold (0–100%). Suggested: **75–90%** depending on your corpus.
- **Auto-Linker tab** that writes `supports / contradicts / analogy / related` edges to the DB and optionally appends links back into notes as `[[wikilinks]]` or Markdown links.
- **Validation tab** to compute SIS / LCS / SRI and generate `Dashboards/validation_dashboard.md`.

### Suggested settings
- Duplicates threshold: start at **80%**, raise to **90%** for aggressive pruning.
- Auto-link min tag overlap (Jaccard): start at **33%**, increase to **50–66%** for stricter linking.
