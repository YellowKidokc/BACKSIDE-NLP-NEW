---
uuid: 599e311f-616e-5aac-8270-ec27833eff55
title: 🏠 HOMEPAGE SETUP GUIDE
author: David Lowe
type: note
created: '2025-11-22'
updated: '2025-11-22'
status: draft
file_path: [[Theophysics_Glossary#Logos|Logos]] zright\Meta\HOMEPAGE-SETUP-GUIDE.md
uuid_generated_at: '2025-11-22T01:23:48.809044'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

# 🏠 HOMEPAGE SETUP GUIDE
## How to Set 000_START_HERE as Your Obsidian Homepage

> **Make 000_START_HERE open automatically** every time you launch Obsidian

---

## ✅ **YOU'VE ALREADY INSTALLED THE PLUGIN!**

You mentioned you downloaded the **Homepage** plugin. Perfect! Now let's configure it.

---

## 🚀 **QUICK SETUP (3 Steps)**

### **Step 1: Open Settings**
1. Click the **⚙️ Settings** icon (bottom-left corner)
2. Or use hotkey: `Ctrl + ,` (Windows) or `Cmd + ,` (Mac)

### **Step 2: Find Homepage Plugin**
1. In the left sidebar, scroll down to **Community plugins**
2. Look for **"Homepage"** in the installed plugins list
3. Click on **"Homepage"** to open its settings

### **Step 3: Configure Homepage**
Set these options:

| Setting | Value | Why |
|---------|-------|-----|
| **Open on startup** | ✅ Enabled | Opens automatically when Obsidian launches |
| **Homepage file** | `000_START_HERE.md` | Your navigation hub |
| **Open mode** | `Reading view` (recommended) or `Live Preview` | Cleaner navigation in reading view |
| **Replace tabs** | `Replace last note` | Keeps your workspace clean |
| **Always open** | ✅ Enabled | Opens even if you had other notes open |

---

## 📝 **DETAILED SETTINGS EXPLANATION**

### **Homepage File**
- **What to set:** `000_START_HERE.md`
- **How to set it:** 
  1. Click the folder icon next to "Homepage file"
  2. Navigate to `Logos_AER_reorganized/`
  3. Select `000_START_HERE.md`
  4. Click "Open"

### **Open Mode**
Choose one:
- **Reading view** ✅ Recommended - Clean, clickable links, no editing distractions
- **Live Preview** - Can edit and preview at the same time
- **Source mode** - Raw markdown view
- **Default** - Uses your default editor mode

### **When Opening Homepage**
Choose one:
- **Replace the last note** ✅ Recommended - Opens homepage, keeps other tabs
- **Replace all open notes** - Closes everything, opens only homepage
- **Keep all notes** - Adds homepage as a new tab

### **Always Open Homepage**
- ✅ **Enabled** - Opens every time, even if you had other notes open
- ❌ **Disabled** - Only opens if no notes were open

### **Revert View on Opening Another Note**
- ✅ **Enabled** - Homepage stays in reading view, other notes use default view
- ❌ **Disabled** - All notes use the same view mode

---

## 🎨 **RECOMMENDED CONFIGURATION**

Here's my recommended setup for the **best experience**:

```yaml
Open on startup: ✅ Enabled
Homepage file: 000_START_HERE.md
Open mode: Reading view
When opening homepage: Replace the last note
Always open homepage: ✅ Enabled
Revert view on opening another note: ✅ Enabled
```

**Why this works:**
- Homepage opens automatically in clean reading view
- You can click links without accidentally editing
- Your other tabs stay open
- Homepage always appears when launching Obsidian
- Other notes open in your preferred view mode

---

## 🔧 **ADDITIONAL FEATURES**

### **Ribbon Button**
The Homepage plugin adds a **🏠 Home icon** to your left ribbon (sidebar).

**Use it to:**
- Quickly return to 000_START_HERE from anywhere
- Reset your workspace to the homepage
- Navigate back after deep diving into papers

### **Command Palette**
You can also open the homepage via command palette:
1. Press `Ctrl + P` (Windows) or `Cmd + P` (Mac)
2. Type "Open homepage"
3. Press Enter

### **Hotkey (Optional)**
Set a custom hotkey for "Open homepage":
1. Go to Settings → Hotkeys
2. Search for "Open homepage"
3. Click "+" to add a hotkey
4. I recommend: `Ctrl + H` or `Alt + H`

---

## 📊 **USING THE HOMEPAGE EFFECTIVELY**

### **What 000_START_HERE Gives You:**
- ✅ **Quick links** to all 12 papers
- ✅ **Core Reference** library access
- ✅ **Experimental Protocols** shortcuts
- ✅ **Evidence Bundles** navigation
- ✅ **Status dashboards** (with Dataview)
- ✅ **Recent updates** auto-generated lists

### **Best Practices:**
1. **Always start from homepage** - Orient yourself before diving in
2. **Use it as a launchpad** - Click to papers, edit, return home
3. **Check status dashboards** - See what's recently updated
4. **Bookmark important sections** - Homepage links to everything

---

## 🔍 **TROUBLESHOOTING**

### **Problem: Homepage doesn't open on startup**
**Solution:**
1. Check that Homepage plugin is **enabled** (Settings → Community plugins)
2. Verify "Open on startup" is ✅ checked
3. Make sure file path is correct: `000_START_HERE.md` (not a full path)
4. Try closing and reopening Obsidian

### **Problem: Wrong file opens**
**Solution:**
1. Click folder icon next to "Homepage file" setting
2. Re-select `000_START_HERE.md`
3. Ensure there are no typos in the filename

### **Problem: Homepage opens but looks broken**
**Solution:**
1. Install **Dataview** plugin (if not already installed)
2. Check that Dataview is enabled
3. Open 000_START_HERE in edit mode to verify content
4. Some queries may need Dataview to render

### **Problem: Links don't work**
**Solution:**
1. Obsidian uses [[wiki-style links]]
2. Ensure files are in the correct folders
3. Check that folder names match after renaming
4. Try refreshing: `Ctrl + R` (reload Obsidian)

---

## 🎯 **NEXT STEPS**

### **After Setting Homepage:**
1. ✅ Close Obsidian
2. ✅ Reopen Obsidian
3. ✅ Confirm 000_START_HERE opens automatically
4. ✅ Test navigation links (click a paper, then 🏠 to return)
5. ✅ Explore the dashboards

### **Optional Enhancements:**
- Set up a **hotkey** for "Open homepage"
- Customize **workspace layout** (split view, sidebar position)
- Create **bookmarks** for frequently accessed papers
- Configure **graph view** to visualize connections

---

## 📚 **RELATED PLUGINS**

These plugins work great with Homepage:

| Plugin | Purpose | Why It's Useful |
|--------|---------|-----------------|
| **Dataview** ✅ | Query vault like a database | Powers the dashboards in 000_START_HERE |
| **Canvas** ✅ | Visual mind mapping | Create visual paper relationships |
| **Templater** ✅ | Advanced templates | Quickly create new papers/notes |
| **Kanban** ✅ | Project boards | Track paper status visually |
| **Breadcrumbs** | Visual navigation trails | See where you are in the vault |
| **Outliner** | Better list management | Organize nested navigation |

---

## 💡 **PRO TIPS**

### **Tip 1: Pin the Homepage Tab**
Right-click the 000_START_HERE tab → "Pin"
- Keeps homepage always visible
- Prevents accidental closing

### **Tip 2: Use Split View**
- Open homepage in left pane (pinned)
- Open papers in right pane
- Navigate from homepage, read in right pane

### **Tip 3: Create a "Dashboard" Workspace**
1. Arrange windows: Homepage (left), Graph view (top-right), Backlinks (bottom-right)
2. Save workspace: Settings → Workspace → Manage workspace layouts
3. Name it "Dashboard"
4. Load it anytime to restore this layout

### **Tip 4: Use CSS for Custom Styling**
Create `snippets/homepage-style.css` in `.obsidian/`:
```css
/* Make homepage headers purple */
[data-path="000_START_HERE.md"] h1 {
  color: #8b5cf6;
}
```

---

## 🚀 **YOU'RE ALL SET!**

Your Obsidian vault now has:
- ✅ **Automatic homepage** opening on startup
- ✅ **One-click navigation** to all papers
- ✅ **Status dashboards** showing recent updates
- ✅ **Quick access** via ribbon button or command palette

**Next time you open Obsidian, 000_START_HERE will greet you!** 🎉

---

**Last Updated:** 2025-10-13

*Your navigation command center is ready to go.* 🏠

