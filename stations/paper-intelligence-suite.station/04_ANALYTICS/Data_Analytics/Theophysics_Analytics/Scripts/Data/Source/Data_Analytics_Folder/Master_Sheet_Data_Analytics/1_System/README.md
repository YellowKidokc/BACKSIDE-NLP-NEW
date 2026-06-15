---
uuid: e59ba6b9-3365-5fe9-87c1-fcd454c2207c
title: 🌌 THEOPHYSICS Workflow System
author: David Lowe
type: documentation
created: '2025-11-22'
updated: '2025-11-22'
status: draft
file_path: 00_VAULT_SYSTEM\05_Workflow\README.md
uuid_generated_at: '2025-11-22T01:23:02.670359'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

# 🌌 THEOPHYSICS Workflow System

**Location**: `O:\THEOPHYSICS\_WORKFLOW\`  
**Purpose**: Complete Obsidian admin and automation system  
**Status**: Ready to implement

---

## 📁 Folder Contents

```
_WORKFLOW\
├── README.md                        ← You are here
├── Admin-Dashboard.md               ← START HERE - Main entry point
├── Tags-Samples.md                  ← Tag taxonomy reference
├── Dataview-Templates.md            ← 50+ query templates
├── Templater-Scripts.md             ← Script documentation
├── Obsidian-Setup-Guide.md          ← Complete setup instructions
├── YAML-Master-Template.md          ← Complete YAML metadata schema (POF 2828)
└── .templater-scripts\              ← Automation scripts
    ├── apply-sample-tags.js
    ├── parse-pasted-headers.js
    ├── bulk-tag-folder.js
    ├── new-paper-template.js
    ├── find-untagged.js
    ├── quick-yaml.js
    └── insert-master-yaml.js         ← NEW: Auto-insert YAML template
```

---

## 🚀 Quick Start

### 1. Read the Setup Guide
Open `Obsidian-Setup-Guide.md` for complete instructions.

### 2. Install Plugins (15 min)
Required plugins:
- Homepage
- Dataview
- Templater
- Advanced Tables
- Linter
- Commander (optional)
- Style Settings (optional)

### 3. Configure Homepage
Settings → Homepage:
- File: `_WORKFLOW/Admin-Dashboard`
- Open on startup: ✅ ON
- Pin homepage: ✅ ON

### 4. Configure Templater
Settings → Templater:
- Script folder: `_WORKFLOW/.templater-scripts`
- Enable system commands: ✅ ON

### 5. Test
Close and reopen Obsidian → Dashboard should auto-open

---

## 📊 What This System Does

✅ **Guided Dashboard** - Auto-opens on startup, walks you through everything  
✅ **Smart Tagging** - 40+ organized tags with application scripts  
✅ **Powerful Queries** - 50+ Dataview templates for instant searching  
✅ **Automation** - 6 scripts for common tasks  
✅ **Import Tools** - Parse headers from external sources  
✅ **Bulk Operations** - Tag hundreds of notes in seconds  

---

## 🏷️ Tag System

### Categories
- `#pillar/` - Foundational domains (physics, theology, consciousness, mathematics)
- `#logos/` - Conceptual categories (field, grace, decay, coherence, master)
- `#χ_var/` - [[Theophysics_Glossary#Master Equation|Master Equation]] variables (G, M, E, S, T, K, R, Q, F, C)
- `#math_role/` - Mathematical functions (operator, field, metric, transform)
- `#paper/` - Paper identifiers
- `#law/` - The 10 Deep Laws
- `#miracle/` - Jesus miracle categories
- `#experiment/` - Experimental protocols

See `Tags-Samples.md` for complete reference.

---

## ⚙️ Available Scripts

### 1. Apply Sample Tags
**Command**: `Templater: apply-sample-tags`  
**Purpose**: Select and apply tags from reference table  
**Usage**: Open note → Run command → Select tags → Apply

### 2. Parse Pasted Headers
**Command**: `Templater: parse-pasted-headers`  
**Purpose**: Import headers from clipboard and create structure  
**Usage**: Copy headers → Create note → Run command

### 3. Bulk Tag Folder
**Command**: `Templater: bulk-tag-folder`  
**Purpose**: Apply tags to all notes in a folder  
**Usage**: Run command → Select folder → Enter tags → Confirm

### 4. New Paper Template
**Command**: `Templater: new-paper-template`  
**Purpose**: Generate complete paper template with YAML  
**Usage**: Run command → Answer prompts → Template created

### 5. Find Untagged Notes
**Command**: `Templater: find-untagged`  
**Purpose**: Generate report of notes without tags  
**Usage**: Run command → Review report → Tag notes

### 6. Quick YAML Insert
**Command**: `Templater: quick-yaml`  
**Purpose**: Insert common YAML templates  
**Usage**: Run command → Select template → YAML inserted

### 7. Insert Master YAML Template (NEW!)
**Command**: `Templater: insert-master-yaml`  
**Purpose**: Insert complete POF 2828 YAML metadata schema with auto-fill  
**Usage**: Create note → Run command → Answer prompts → Complete YAML inserted  
**Features**:
- Auto-generates UUID and timestamps
- Prompts for status, core concept, abstract
- Asks about miracle analysis
- Selects pillars and χ variables
- Comprehensive metadata structure

---

## 📈 Dataview Queries

50+ ready-to-use queries in `Dataview-Templates.md`:

- **Basic**: All tagged notes, recent notes, by folder
- **Papers**: By status, by topic, by equation
- **Tags**: By pillar, by χ variable, by law
- **Miracles**: By type, by scripture reference
- **Experiments**: By status, by priority
- **Scripture**: By reference, by topic
- **Math**: Equations, operators, metrics
- **Links**: Most connected, orphans, broken links
- **Maintenance**: Untagged, missing YAML, large notes
- **Statistics**: Tag usage, folder stats, word counts

---

## 🎯 Typical Workflows

### Workflow 1: Tag New Paper
1. Create note
2. Run `new-paper-template`
3. Fill in details
4. Auto-structured with proper YAML

### Workflow 2: Import External Content
1. Copy headers from source
2. Create new note
3. Run `parse-pasted-headers`
4. Auto-generates structure

### Workflow 3: Bulk Tag Folder
1. Run `bulk-tag-folder`
2. Select folder
3. Enter tags
4. Confirm → All notes tagged

### Workflow 4: Find Gaps
1. Run `find-untagged`
2. Review report
3. Tag individually or in bulk
4. Repeat weekly

### Workflow 5: Search Vault
1. Open `Admin-Dashboard.md`
2. Find relevant query
3. Copy and customize
4. Run in any note

---

## 🔧 Maintenance

### Daily (5 min)
- Check untagged notes query
- Tag 5-10 new notes
- Review dashboard

### Weekly (15 min)
- Run `find-untagged` script
- Bulk tag a folder
- Update tag taxonomy
- Review queries

### Monthly (30 min)
- Audit tag consistency
- Clean up duplicates
- Update scripts
- Backup vault

---

## 🚨 Troubleshooting

### Dashboard Won't Open
- Check Homepage plugin enabled
- Verify path: `_WORKFLOW/Admin-Dashboard`
- Check "Open on startup" is ON

### Scripts Not Found
- Check Templater script folder path
- Verify `.js` extension on files
- Restart Obsidian

### Queries Not Working
- Enable Dataview plugin
- Check query syntax
- Verify field names
- Check console for errors

### Tags Not Applying
- Check YAML syntax
- Verify Tags-Samples.md exists
- Check script permissions

---

## 📚 Documentation

- **Admin-Dashboard.md** - Main dashboard with all sections
- **Tags-Samples.md** - Complete tag reference with examples
- **Dataview-Templates.md** - 50+ query templates
- **Templater-Scripts.md** - Script documentation and code
- **Obsidian-Setup-Guide.md** - Step-by-step setup

---

## ✅ Setup Checklist

- [ ] Read Obsidian-Setup-Guide.md
- [ ] Install 7 required plugins
- [ ] Configure Homepage plugin
- [ ] Configure Templater plugin
- [ ] Test dashboard auto-opens
- [ ] Test Dataview queries work
- [ ] Test Templater scripts work
- [ ] Tag core papers
- [ ] Create custom queries
- [ ] Set up maintenance routine

---

## 💡 Pro Tips

1. **Use hotkeys** for frequent scripts
2. **Batch operations** instead of individual
3. **Tag as you go** - Don't leave for later
4. **Query first** before manual search
5. **Backup regularly** - Use Git or cloud sync

---

## 🎓 Next Steps

1. **Install plugins** (15 min)
2. **Configure settings** (10 min)
3. **Test system** (10 min)
4. **Tag core files** (30 min)
5. **Create custom queries** (15 min)
6. **Establish routine** (ongoing)

---

**Total Setup Time**: 60-90 minutes  
**Maintenance**: 20 minutes/week  
**Value**: Hundreds of hours saved organizing 15k+ files  

---

**Last Updated**: 2025-10-17  
**Version**: 1.0  
**Status**: ✅ Complete and Ready
