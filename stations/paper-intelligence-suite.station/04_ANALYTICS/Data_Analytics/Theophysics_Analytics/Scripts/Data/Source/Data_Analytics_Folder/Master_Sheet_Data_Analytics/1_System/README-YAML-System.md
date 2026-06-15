---
uuid: b6b8207f-542a-5997-be8c-183c638d2014
title: THEOPHYSICS YAML SYSTEM - COMPLETE GUIDE
author: David Lowe
type: documentation
created: '2025-11-22'
updated: '2025-11-22'
status: draft
file_path: 00_VAULT_SYSTEM\05_Workflow\README-YAML-System.md
uuid_generated_at: '2025-11-22T01:23:02.658801'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

# THEOPHYSICS YAML SYSTEM - COMPLETE GUIDE

## 🎯 Overview

This system provides comprehensive YAML frontmatter management for your entire Theophysics vault with:
- ✅ 4-domain publishing system (Private, Public, Research, Academia)
- ✅ AI-powered auto-tagging using OpenAI
- ✅ Batch processing for entire vault
- ✅ Respects existing YAML
- ✅ Hidden YAML option
- ✅ Theophysics tag ontology integration

---

## 📁 Files in This System

### 1. `YAML.md`
**Master configuration and template documentation**
- Complete theophysics-config.yaml
- Individual paper YAML template
- Usage guide

### 2. `auto-yaml-processor.py`
**Python script for batch processing**
- Adds YAML to all notes
- AI-powered content analysis
- Configurable options

### 3. `../Templates/YAML-Template-Theophysics.md`
**Obsidian template for new notes**
- Copy/paste into new notes
- Use with Obsidian Templates plugin
- Includes all fields

---

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
pip install pyyaml openai
```

### Step 2: Set Your OpenAI API Key

**Option A - Environment Variable (recommended):**
```bash
# Windows (PowerShell)
$env:OPENAI_API_KEY = "sk-your-key-here"

# Mac/Linux
export OPENAI_API_KEY="sk-your-key-here"
```

**Option B - Edit Script:**
Open `auto-yaml-processor.py` and set:
```python
OPENAI_API_KEY = "sk-your-key-here"
```

### Step 3: Configure Options

Edit these settings in `auto-yaml-processor.py`:

```python
VAULT_PATH = r"D:\THEOPHYSICS"  # Your vault path

HIDDEN_YAML = False  # True = wrap in HTML comments (hidden in reading mode)
SKIP_EXISTING = True  # True = skip files with existing YAML
DRY_RUN = True  # True = preview only, False = actually modify
```

### Step 4: Run Dry Run

```bash
cd D:\THEOPHYSICS\_WORKFLOW
python auto-yaml-processor.py
```

This will:
- ✅ Scan all markdown files
- ✅ Show what would be added
- ✅ Use AI to analyze content
- ✅ Preview tags and classifications
- ❌ **NOT modify any files**

### Step 5: Review and Execute

If the preview looks good, answer `y` when prompted to run actual processing.

---

## 📊 4-Domain Publishing System

Every note gets these fields at the top of YAML:

```yaml
publish_to:
  private: true      # ✓ All notes here by default
  public: false      # ☐ Manually set to true for public site
  research: false    # ☐ Manually set to true for research archive
  academia: false    # ☐ Manually set to true for academic papers
```

### How It Works:

1. **Private (default):** All notes live here, never publicly visible
2. **Public:** You manually set `public: true` when ready to publish
3. **Research:** For collaborators/research archive
4. **Academia:** For peer-review ready papers

**Notes can live in multiple domains simultaneously!**

Example - a paper that's public, in research, and academia:
```yaml
publish_to:
  private: true      # Always true
  public: true       # ✓ On public site
  research: true     # ✓ In research archive
  academia: true     # ✓ Available for peer review
```

---

## 🤖 AI-Powered Tagging

When OpenAI is enabled, the script will:

1. **Read your content** (first 2000 characters)
2. **Analyze and classify:**
   - Generate 2-3 sentence summary
   - Extract key points
   - Identify main concepts
   - Suggest Theophysics tags:
     - `pillars`: physics, theology, math, consciousness
     - `logos`: master, force, decay, restore, state
     - `theos`: D_LOGOS, D_FATHER, D_SPIRIT, D_ADVERSARY
     - `chi_vars`: Negentropy, Entropy, Time, etc.
3. **Add to YAML** with confidence score

### Cost Estimation:

Using `gpt-4o-mini` (fast and cheap):
- ~$0.0001 per note
- For 1000 notes: ~$0.10
- For entire vault (5000 notes): ~$0.50

Very affordable for batch processing!

---

## 🎨 Hidden YAML Option

Set `HIDDEN_YAML = True` to wrap frontmatter in HTML comments:

```html
<!--
---
title: "My Note"
publish_to:
  private: true
  public: false
---
-->

# My Note Content
```

**Benefits:**
- ✅ YAML exists and works for publishing
- ✅ Hidden in Obsidian reading view
- ✅ Clean appearance
- ❌ Can't edit in Properties panel (must edit as text)

**Normal YAML** (recommended):
```yaml
---
title: "My Note"
publish_to:
  private: true
  public: false
---

# My Note Content
```

---

## 🔧 Advanced Options

### Exclude Directories

Edit `EXCLUDE_DIRS` in script:

```python
EXCLUDE_DIRS = [
    '.git',
    '.obsidian',
    '.trash',
    'node_modules',
    '_gsdata_',
    'cloudflare-workers',
    'my-private-journal'  # Add your own
]
```

### Process Only New Files

Set `SKIP_EXISTING = True` to only add YAML to files without frontmatter.

### Update Existing Files

Set `SKIP_EXISTING = False` to update all files (will preserve manually-set fields but add AI analysis to all).

---

## 📝 Manual Workflow (For Individual Notes)

### Option 1: Use Obsidian Template

1. Create new note
2. Open command palette (`Ctrl/Cmd + P`)
3. Type "Templates: Insert template"
4. Select "YAML-Template-Theophysics"
5. Fill in title and write content

### Option 2: Copy from Templates Folder

Copy from `Templates/YAML-Template-Theophysics.md` and paste at top of your note.

---

## 🌐 Publishing to Cloudflare Pages

### Structure Your Vault:

```
D:\THEOPHYSICS\
├── _PRIVATE\          (never published)
├── _PUBLIC\           (publish_to.public: true)
├── _RESEARCH\         (publish_to.research: true)
├── _ACADEMIA\         (publish_to.academia: true)
└── _WORKFLOW\         (scripts and configs)
```

### Publishing Script:

Create `publish.py` to copy files based on `publish_to` settings:

```python
# Scan all markdown files
# Read YAML frontmatter
# Copy to appropriate output directories based on publish_to flags
# Deploy to Cloudflare Pages
```

Want me to create this script too?

---

## ❓ FAQ

### Q: Will this overwrite my existing notes?

**A:** No! The script:
- Runs in DRY_RUN mode first (preview only)
- Asks for confirmation before modifying
- Preserves existing YAML (with `SKIP_EXISTING = True`)
- Only adds YAML to files without frontmatter

### Q: What if I don't have OpenAI API key?

**A:** Script works fine without it!
- Will use simple keyword detection instead
- Won't charge you anything
- You can add API key later and re-run to get AI tagging

### Q: Can I run this multiple times?

**A:** Yes!
- With `SKIP_EXISTING = True`: Only processes new files
- With `SKIP_EXISTING = False`: Updates all files (preserves manual edits)

### Q: How do I make a note public?

**A:** Two ways:
1. **In YAML:** Change `public: false` to `public: true`
2. **In Properties panel:** Toggle "Publish To > Public" to true

### Q: Can a note be in multiple domains?

**A:** Yes! Set multiple to `true`:
```yaml
publish_to:
  private: true
  public: true
  research: true
  academia: true
```

---

## 🎯 Recommended Workflow

### For Ongoing Work:

1. **Use template** for new notes (includes YAML)
2. **Write content** as normal
3. **When ready to publish:**
   - Open Properties panel
   - Set `publish_to.public: true`
   - Or `research: true`, `academia: true`
4. **Run publishing script** to deploy

### For Existing Vault (One-Time):

1. **Backup your vault** (just in case!)
2. **Set your OpenAI API key**
3. **Run dry run** to preview
4. **Confirm and execute**
5. **Review results** in Obsidian
6. **Manually adjust** any misclassifications
7. **You're done!**

---

## 📞 Support

Questions? Issues?

1. Check this README
2. Review `YAML.md` for complete documentation
3. Examine `auto-yaml-processor.py` comments
4. Ask Claude/ChatGPT for help with script modifications

---

**This is your complete YAML management system, David!**

✅ Batch processing  
✅ AI-powered tagging  
✅ 4-domain publishing  
✅ Respects existing work  
✅ Ready for Cloudflare deployment

**Run the script whenever you want to add YAML to new notes or update classifications.**

