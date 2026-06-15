# Stats System Deployment Guide

## Overview

The stats system can operate in two modes:

1. **Global Instance** - Master/source of truth
2. **Local Instance** - Deployed copy that aggregates back to global

---

## Setup: Global Instance (Master)

This is already your current setup:
- Location: `D:\THEOPHYSICS_MASTER\00_VAULT_SYSTEM\04_Analysis\01_Scripts\`
- Type: Global (master)
- All local instances aggregate to this

### Configuration

Edit `config.yaml`:
```yaml
instance:
  type: "global"
  name: "THEOPHYSICS_MASTER"

scanning:
  include_folders:
    - "03_PUBLICATIONS/COMPLETE_LOGOS_PAPERS_FINAL"
  exclude_patterns:
    - "**/DRAFT/**"
    - "**/drafts/**"
```

---

## Deploy Local Instance

### Step 1: Create Deployment Package

**Option A: Use batch script**
```bash
DEPLOY_STATS_SYSTEM.bat
# Choose 1: Create deployment package
```

**Option B: Use Python**
```bash
python deploy_stats_system.py package D:\Backup
```

This creates a portable folder with everything needed.

### Step 2: Deploy to Another Vault

```bash
python deploy_stats_system.py deploy D:\AnotherVault MyInstance D:\THEOPHYSICS_MASTER
```

Arguments:
- `D:\AnotherVault` - Target vault
- `MyInstance` - Name for this instance
- `D:\THEOPHYSICS_MASTER` - Path to global master

This will:
- Copy all scripts to target vault
- Create local `config.yaml` pointing to global
- Register instance in global registry
- Create Stats folders

---

## Configuration Options

### Scanning Configuration

```yaml
scanning:
  # What to scan
  include_folders:
    - "03_PUBLICATIONS/COMPLETE_LOGOS_PAPERS_FINAL"
    - "02_LIBRARY/Concepts"
  
  # What to skip
  exclude_patterns:
    - "**/DRAFT/**"      # Skip draft folders
    - "**/drafts/**"
    - "**/WIP/**"
    - "**/temp/**"
    - "**/backup/**"
  
  # Scan recursively?
  recursive: true
  
  # Or only root level?
  root_only: false
```

### Aggregation Configuration

```yaml
aggregation:
  # Enable sending stats to global?
  enabled: true
  
  # When to aggregate
  mode: "manual"  # manual | auto | scheduled
```

---

## Usage

### Generate Stats (Any Instance)

```bash
# Single paper
python generate_stats.py Paper-01.md

# All papers
python generate_stats.py --all
```

### Aggregate to Global (Local Instance Only)

```bash
# Manual aggregation
python deploy_stats_system.py aggregate
```

This copies all local stats to the global instance with instance prefix.

### List Instances (Global Only)

```bash
python deploy_stats_system.py list
```

Shows all registered local instances.

---

## File Structure

### Global Instance
```
D:\THEOPHYSICS_MASTER\
├── 00_VAULT_SYSTEM\
│   ├── 04_Analysis\
│   │   └── 01_Scripts\
│   │       ├── generate_stats.py
│   │       ├── config.yaml (type: global)
│   │       └── ...
│   └── global_instance_registry.yaml  ← Tracks all instances
└── Stats\
    ├── Local\          ← Local stats + aggregated from instances
    ├── Comparisons\
    └── Global\
```

### Local Instance
```
D:\AnotherVault\
├── 00_VAULT_SYSTEM\
│   └── 04_Analysis\
│       └── 01_Scripts\
│           ├── generate_stats.py
│           ├── config.yaml (type: local, points to global)
│           └── ...
└── Stats\
    ├── Local\          ← Only this instance's stats
    ├── Comparisons\
    └── Global\
```

---

## Workflow

### 1. Global Instance (Master)

```bash
# Generate stats
RUN_ALL_STATS.bat

# View results
Stats\Global\vault.stats.json
```

### 2. Local Instance

```bash
# Generate stats
RUN_ALL_STATS.bat

# Aggregate to global
python deploy_stats_system.py aggregate
```

### 3. Global Receives Aggregated Data

Local stats appear in `Stats\Local\` with instance prefix:
- `MyInstance_Paper-01.stats.json`
- `MyInstance_Paper-02.stats.json`

---

## Exclude Patterns

Common exclusion patterns:

```yaml
exclude_patterns:
  # Drafts
  - "**/DRAFT/**"
  - "**/drafts/**"
  - "**/WIP/**"
  
  # System folders
  - "**/.obsidian/**"
  - "**/.trash/**"
  - "**/.git/**"
  
  # Archives
  - "**/archive/**"
  - "**/backup/**"
  - "**/old/**"
  
  # Temp
  - "**/temp/**"
  - "**/tmp/**"
```

---

## Example Deployment Scenario

### Setup

1. **Global Master**: `D:\THEOPHYSICS_MASTER`
2. **Local Instance 1**: `D:\WorkingCopy`
3. **Local Instance 2**: `D:\LaptopVault`

### Deploy

```bash
# Deploy to working copy
python deploy_stats_system.py deploy D:\WorkingCopy WorkCopy D:\THEOPHYSICS_MASTER

# Deploy to laptop
python deploy_stats_system.py deploy D:\LaptopVault Laptop D:\THEOPHYSICS_MASTER
```

### Use

```bash
# On working copy
cd D:\WorkingCopy\00_VAULT_SYSTEM\04_Analysis\01_Scripts
RUN_ALL_STATS.bat
python deploy_stats_system.py aggregate

# On laptop
cd D:\LaptopVault\00_VAULT_SYSTEM\04_Analysis\01_Scripts
RUN_ALL_STATS.bat
python deploy_stats_system.py aggregate
```

### Result

Global master receives stats from both:
- `WorkCopy_Paper-01.stats.json`
- `Laptop_Paper-01.stats.json`

Global can compare across all instances.

---

## Benefits

✅ **One source of truth** (global master)  
✅ **Multiple working copies** (local instances)  
✅ **Automatic aggregation** to master  
✅ **No conflicts** (instance prefix)  
✅ **Portable** (zip & deploy anywhere)  
✅ **Configurable** (exclude drafts, etc.)  
✅ **Tracked** (registry of all instances)  

---

## Troubleshooting

**"This is not a local instance"**
- Check `config.yaml` → `instance.type` should be "local"
- Redeploy with deploy command

**"Global path not found"**
- Check `config.yaml` → `instance.global_path` is correct
- Update path if master moved

**"No instances registered"**
- Normal if no local instances deployed yet
- Deploy a local instance to populate registry

