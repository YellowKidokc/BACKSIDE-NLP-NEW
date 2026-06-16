---
uuid: f673d593-d9da-5b47-8313-49b78057f77b
title: 🚀 THEOPHYSICS Obsidian Setup Guide
author: David Lowe
type: workflow
created: '2025-11-22'
updated: '2025-11-22'
status: draft
file_path: 00_VAULT_SYSTEM\05_Workflow\Obsidian-Setup-Guide.md
uuid_generated_at: '2025-11-22T01:23:02.641509'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

# 🚀 THEOPHYSICS Obsidian Setup Guide

> Complete step-by-step guide to set up your Obsidian vault as a guided admin system.

---

## ✅ Phase 1: Install Core Plugins (15 minutes)

### Step 1: Enable Community Plugins

1. Open Obsidian
2. Settings (gear icon) → Community plugins
3. Click "Turn on community plugins"
4. Click "Browse" to open plugin marketplace

### Step 2: Install Required Plugins

Install these plugins in order:

| Plugin | Purpose | Priority |
|--------|---------|----------|
| **Homepage** | Auto-open Admin Dashboard | CRITICAL |
| **Dataview** | Dynamic queries and tables | CRITICAL |
| **Templater** | Automation scripts | CRITICAL |
| **Advanced Tables** | Editable tag tables | High |
| **Linter** | YAML consistency | High |
| **Commander** | Custom buttons | Medium |
| **Style Settings** | Dashboard styling | Low |

**How to install each:**
1. Click "Browse" in Community Plugins
2. Search for plugin name
3. Click "Install"
4. Click "Enable"

---

## ⚙️ Phase 2: Configure Plugins (10 minutes)

### Homepage Plugin Settings

1. Settings → Homepage
2. **File**: Type `Admin-Dashboard` (or full path if needed)
3. **Open on startup**: ✅ ON
4. **Open when empty**: ✅ ON
5. **Use when opening normally**: ❌ OFF
6. **Pin the homepage when opening**: ✅ ON
7. **Auto-create**: ✅ ON

### Dataview Plugin Settings

1. Settings → Dataview
2. **Enable JavaScript Queries**: ✅ ON
3. **Enable Inline Queries**: ✅ ON
4. **Enable Inline JavaScript Queries**: ✅ ON

### Templater Plugin Settings

1. Settings → Templater
2. **Template folder location**: Create and select `.templater-scripts`
3. **Script files folder location**: Point to `.templater-scripts`
4. **Trigger Templater on new file creation**: ✅ ON
5. **Enable System Commands**: ✅ ON

---

## 📁 Phase 3: Create Folder Structure (5 minutes)

Create these folders in your vault:

```
O:\THEOPHYSICS\
├── .templater-scripts\      (for Templater JS files)
├── Admin-Dashboard.md        (already created)
├── Tags-Samples.md          (already created)
├── Dataview-Templates.md    (already created)
├── Templater-Scripts.md     (already created)
└── (your existing folders)
```

**To create `.templater-scripts` folder:**
1. Open File Explorer
2. Navigate to `O:\THEOPHYSICS\`
3. Right-click → New → Folder
4. Name it `.templater-scripts`

---

## 🔧 Phase 4: Set Up Templater Scripts (10 minutes)

### Create Script Files

For each script in `Templater-Scripts.md`:

1. Open `.templater-scripts` folder
2. Create new text file
3. Name it exactly as shown (e.g., `apply-sample-tags.js`)
4. Copy script code from `Templater-Scripts.md`
5. Paste into file
6. Save

**Scripts to create:**
- `apply-sample-tags.js`
- `parse-pasted-headers.js`
- `bulk-tag-folder.js`
- `new-paper-template.js`
- `find-untagged.js`
- `quick-yaml.js`

### Test Scripts

1. Open Command Palette: `Ctrl/Cmd + P`
2. Type "Templater"
3. You should see your scripts listed
4. Try running `find-untagged.js` to test

---

## 🎨 Phase 5: Customize Dashboard (Optional, 5 minutes)

### Add Custom CSS (Optional)

Create `O:\THEOPHYSICS\.obsidian\snippets\dashboard.css`:

```css
/* Dashboard styling */
.dashboard-section {
    background: rgba(100, 100, 255, 0.1);
    border-left: 4px solid [[4a9eff]];
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 8px;
}

/* Tag pills */
.tag {
    background: rgba(74, 158, 255, 0.2);
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.9em;
}

/* Dataview tables */
.dataview.table-view-table {
    border-collapse: collapse;
}

.dataview.table-view-table th {
    background: rgba(74, 158, 255, 0.3);
    font-weight: bold;
}
```

Enable in Settings → Appearance → CSS snippets

---

## 🏁 Phase 6: First Run & Testing (10 minutes)

### Test 1: Dashboard Opens Automatically

1. Close Obsidian completely
2. Reopen Obsidian
3. **Expected**: Admin-Dashboard.md opens automatically
4. **If not**: Check Homepage plugin settings

### Test 2: Dataview Queries Work

1. Scroll to "Dataview Templates" section in dashboard
2. **Expected**: See live query results
3. **If not**: 
   - Check Dataview plugin is enabled
   - Verify query syntax
   - Check console for errors (`Ctrl/Cmd + Shift + I`)

### Test 3: Templater Scripts Work

1. Open Command Palette: `Ctrl/Cmd + P`
2. Type "Templater: find-untagged"
3. Run the script
4. **Expected**: See report of untagged notes
5. **If not**:
   - Check script file exists in `.templater-scripts`
   - Verify Templater settings
   - Check console for errors

### Test 4: Tag Application

1. Create a new note
2. Open Command Palette
3. Run "Templater: apply-sample-tags"
4. Select tags from list
5. **Expected**: YAML frontmatter added with tags
6. **If not**: Check Tags-Samples.md exists

---

## 🎯 Phase 7: Initial Tagging (Ongoing)

### Tag Your Core Files

1. **Start with Papers**: Tag all 12 Logos Papers
   - Use `bulk-tag-folder.js` for efficiency
   - Apply: `pillar/physics, logos/field, paper/P#_NAME`

2. **Tag [[Theophysics_Glossary#Master Equation|Master Equation]] Components**:
   - Apply: `pillar/mathematics, logos/master, χ_var/[component]`

3. **Tag Miracle Analyses**:
   - Apply: `pillar/theology, pillar/physics, miracle/[type]`

4. **Tag Deep Laws**:
   - Apply: `law/Law##, logos/[category], χ_var/[variable]`

### Monitor Progress

Run this Dataview query daily:

```dataview
TABLE length(tags) AS "Tags", file.mtime AS "Modified"
FROM ""
WHERE !tags OR length(tags) = 0
SORT file.mtime DESC
LIMIT 20
```

---

## 📊 Phase 8: Customize Queries (Ongoing)

### Create Your Own Queries

1. Copy from `Dataview-Templates.md`
2. Modify for your needs
3. Add to dashboard or separate notes
4. Test and refine

### Common Customizations

**Filter by date range:**
```dataview
WHERE file.mtime >= date(2025-10-01)
```

**Group by category:**
```dataview
GROUP BY category
```

**Count items:**
```dataview
TABLE length(rows) AS "Count"
GROUP BY tags
```

---

## 🔄 Maintenance Routine

### Daily (5 minutes)

- [ ] Check untagged notes query
- [ ] Tag 5-10 new/modified notes
- [ ] Review dashboard for broken links

### Weekly (15 minutes)

- [ ] Run `find-untagged.js` script
- [ ] Bulk tag a folder
- [ ] Update Tags-Samples.md with new tags
- [ ] Review Dataview queries for accuracy

### Monthly (30 minutes)

- [ ] Audit tag consistency
- [ ] Clean up duplicate tags
- [ ] Update Templater scripts
- [ ] Backup vault

---

## 🚨 Troubleshooting

### Dashboard Not Opening

**Problem**: Dashboard doesn't open on startup

**Solutions**:
1. Check Homepage plugin is enabled
2. Verify file name is exact: `Admin-Dashboard.md`
3. Check "Open on startup" is ON
4. Try manual: Settings → Homepage → "Open homepage"

### Dataview Queries Not Working

**Problem**: Queries show "No results" or error

**Solutions**:
1. Enable Dataview plugin
2. Check query syntax (case-sensitive)
3. Verify field names match your YAML
4. Check console for errors
5. Try simple query first: `LIST FROM ""`

### Templater Scripts Not Found

**Problem**: Scripts don't appear in Command Palette

**Solutions**:
1. Check script folder path in Templater settings
2. Verify `.js` file extension
3. Restart Obsidian
4. Check file permissions
5. Test with simple script first

### Tags Not Applying

**Problem**: Tags don't insert into notes

**Solutions**:
1. Check YAML syntax (no spaces in tag names)
2. Verify Tags-Samples.md exists
3. Check script has file permissions
4. Try manual YAML first
5. Check console for errors

### Slow Performance

**Problem**: Vault is slow with many files

**Solutions**:
1. Limit Dataview query results (`LIMIT 50`)
2. Disable unused plugins
3. Use file exclusions in Dataview settings
4. Index fewer folders
5. Consider splitting vault

---

## 💡 Pro Tips

### Hotkeys to Set Up

1. **Quick Switcher**: `Ctrl/Cmd + O` (default)
2. **Command Palette**: `Ctrl/Cmd + P` (default)
3. **Apply Sample Tags**: Assign custom hotkey
4. **Find Untagged**: Assign custom hotkey
5. **New Paper Template**: Assign custom hotkey

### Workflow Optimization

1. **Use Templates**: Create note templates for common types
2. **Batch Operations**: Tag folders, not individual notes
3. **Regular Maintenance**: Schedule weekly cleanup
4. **Backup Often**: Use Git or cloud sync
5. **Document Changes**: Keep changelog in dashboard

### Advanced Features

1. **Graph View**: Visualize note connections
2. **Backlinks**: See all notes linking to current
3. **Outline**: Navigate long notes easily
4. **Search Operators**: Use regex in search
5. **Canvas**: Visual project planning

---

## 📚 Next Steps

Once setup is complete:

1. **Tag Core Content**: Start with most important notes
2. **Create Custom Queries**: Build queries for your workflow
3. **Develop Templates**: Create templates for common note types
4. **Automate More**: Write custom Templater scripts
5. **Share Knowledge**: Document your workflow

---

## 🎓 Learning Resources

### Obsidian Basics
- Official Obsidian Help: https://help.obsidian.md
- Obsidian Forum: https://forum.obsidian.md

### Dataview
- Dataview Docs: https://blacksmithgu.github.io/obsidian-dataview/
- Query Examples: Community plugins showcase

### Templater
- Templater Docs: https://silentvoid13.github.io/Templater/
- Script Examples: GitHub community

---

## ✅ Setup Checklist

- [ ] Phase 1: Installed all core plugins
- [ ] Phase 2: Configured plugin settings
- [ ] Phase 3: Created folder structure
- [ ] Phase 4: Set up Templater scripts
- [ ] Phase 5: Customized dashboard (optional)
- [ ] Phase 6: Tested all functionality
- [ ] Phase 7: Tagged initial core files
- [ ] Phase 8: Created custom queries
- [ ] Set up maintenance routine
- [ ] Assigned hotkeys
- [ ] Backed up vault

---

**Estimated Total Setup Time**: 60-90 minutes
**Difficulty**: Intermediate
**Maintenance**: 20 minutes/week

**Last Updated**: 2025-10-17
**Version**: 1.0
