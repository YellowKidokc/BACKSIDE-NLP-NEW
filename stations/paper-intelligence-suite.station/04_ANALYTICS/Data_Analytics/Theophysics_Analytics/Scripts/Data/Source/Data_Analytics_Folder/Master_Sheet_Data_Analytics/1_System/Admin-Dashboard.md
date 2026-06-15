---
uuid: 4d38f59b-7ffd-5244-9ed2-fb211a474863
title: 🌌 THEOPHYSICS Admin Dashboard
author: David Lowe
type: workflow
created: '2025-11-22'
updated: '2025-11-22'
status: draft
file_path: 00_VAULT_SYSTEM\05_Workflow\Admin-Dashboard.md
uuid_generated_at: '2025-11-22T01:23:02.510872'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

# 🌌 THEOPHYSICS Admin Dashboard

> **Welcome to Your Guided Setup!** This dashboard walks you through organizing, tagging, and navigating your THEOPHYSICS vault. Everything you need is here—no manual slogging through 15k+ files.

---

## 📋 Quick Navigation

- [[#1. Sample Tags & YAML Samples|Sample Tags & YAML]]
- [[#2. Sample Links – Choose Your Type|Link Types Guide]]
- [[#3. Dataview Templates – Search & Control|Dataview Queries]]
- [[#4. Import Headers from External Sources|Import Tools]]
- [[#5. Bulk Operations|Bulk Tagging & Cleanup]]

---

## 1. Sample Tags & YAML Samples

Here's the core taxonomy from our schema. Use these as templates for tagging your notes.

### Core Tag Categories:

**Pillar Tags** (Foundational Domains):
- `#pillar/physics` - Quantifiable physical laws
- `#pillar/theology` - Theological concepts and scripture
- `#pillar/consciousness` - Consciousness studies and observer effects
- `#pillar/mathematics` - Mathematical frameworks and proofs

**Logos Categories** (Conceptual Domains):
- `#logos/field` - The [[Theophysics_Glossary#Logos field|Logos Field]] (χ) and substrate
- `#logos/grace` - Grace function and negentropic forces
- `#logos/decay` - Entropy and decay processes
- `#logos/coherence` - Coherence and order
- `#logos/master` - [[Theophysics_Glossary#Master Equation|Master Equation]] components

**χ Variables** ([[Theophysics_Glossary#Master Equation|Master Equation]] Components):
- `#χ_var/Grace` - G (Grace/Negentropy)
- `#χ_var/MutualInfo` - M (Mutual Information)
- `#χ_var/Entropy` - E (Entropy)
- `#χ_var/SelfReference` - S (Self-Reference/Consciousness)
- `#χ_var/Time` - T (Temporal dynamics)
- `#χ_var/Knowledge` - K (Knowledge/Information)
- `#χ_var/Relationality` - R (Relationality)
- `#χ_var/Quantum` - Q ([[Theophysics_Glossary#Quantum Mechanics|Quantum mechanics]])
- `#χ_var/Force` - F (Force/Faith)
- `#χ_var/Coherence` - C (Coherence)

**Math Roles**:
- `#math_role/operator` - Mathematical operators
- `#math_role/field` - Field equations
- `#math_role/metric` - Metrics and measurements
- `#math_role/transform` - Transformations

### 📝 Sample YAML Templates

**For a Physics Paper:**
```yaml
---
tags: [pillar/physics, logos/field, χ_var/Grace, math_role/field]
paper_id: P1_LOGOS_PRINCIPLE
status: draft
date: 2025-10-17
---
```

**For a Theological Note:**
```yaml
---
tags: [pillar/theology, logos/grace, χ_var/Grace]
scripture_ref: John 1:1-14
topic: Logos Incarnation
---
```

**For a [[Theophysics_Glossary#Master Equation|Master Equation]] Component:**
```yaml
---
tags: [pillar/mathematics, logos/master, χ_var/Entropy, math_role/operator]
equation_id: ME_CHI
component: E (Entropy)
---
```

### 🔧 Quick Actions

- **Apply Tags to Current Note**: Use Templater command `Apply Sample Tags`
- **View All Tags**: Use Dataview query below
- **Bulk Tag Notes**: See [[#5. Bulk Operations]]

---

## 2. Sample Links – Choose Your Type

**Why link?** Connect ideas, reference equations, embed content, and build your knowledge graph.

### Link Type Reference Table

| Type | Syntax | When/Why | Sample |
|------|--------|----------|--------|
| **Internal** | `[[Note]]` | Basic note link; fast navigation | `[[Master-Equation]]` |
| **Embed** | `![[Note]]` | Pull entire note inline | `![[Sample-Tags]]` |
| **Header Embed** | `![[Note#Header]]` | Pull specific section inline | `![[Schema#Terminology-Bridge]]` |
| **Block Reference** | `[[Note#^block-id]]` | Link to specific paragraph | `[[Paper-1#^logos-def]]` |
| **External** | `[Text](url)` | Web/DB links; citations | `[Schema](https://db-url)` |
| **Alias** | `[[Note\|Display Text]]` | Custom display text | `[[P1_LOGOS\|Paper 1]]` |
| **Image** | `![[image.png]]` | Embed images | `![[diagram.png]]` |
| **PDF** | `![[doc.pdf#page=5]]` | Link to PDF page | `![[paper.pdf#page=10]]` |

### 💡 Best Practices

- **Use Internal Links** for navigation between related concepts
- **Use Embeds** when you want to see content without switching notes
- **Use Block References** for precise citations and cross-references
- **Use Aliases** to keep links readable in prose

### Try It Now

Paste a header or paragraph below, then create a block reference:

```
Your content here ^unique-block-id
```

Link to it: `[[Admin-Dashboard#^unique-block-id]]`

---

## 3. Dataview Templates – Search & Control

These are starter queries. Customize them for your needs.

### Query 1: All Tagged Notes

```dataview
TABLE tags, file.mtime AS "Modified"
FROM ""
WHERE tags
SORT file.mtime DESC
LIMIT 50
```

### Query 2: Papers by Status

```dataview
TABLE paper_id, status, date
FROM ""
WHERE paper_id
SORT status ASC, date DESC
```

### Query 3: [[Theophysics_Glossary#Master Equation|Master Equation]] Components

```dataview
TABLE component, equation_id, tags
FROM ""
WHERE contains(tags, "χ_var")
SORT component ASC
```

### Query 4: Recent Theology Notes

```dataview
LIST
FROM ""
WHERE contains(tags, "pillar/theology")
SORT file.mtime DESC
LIMIT 20
```

### Query 5: Untagged Notes (Needs Attention)

```dataview
LIST
FROM ""
WHERE !tags OR length(tags) = 0
SORT file.name ASC
LIMIT 30
```

### Query 6: Notes by Scripture Reference

```dataview
TABLE scripture_ref, topic
FROM ""
WHERE scripture_ref
SORT scripture_ref ASC
```

### 🔍 Search Tips

- **Quick Switcher**: `Ctrl/Cmd + O` - Fast note search
- **Global Search**: `Ctrl/Cmd + Shift + F` - Search all content
- **Tag Search**: Click any tag to see all notes with that tag
- **Dataview**: Modify queries above for custom views

---

## 4. Import Headers from External Sources

### From Database Schema (CSV/JSON)

**Step 1**: Export from D1 database
```bash
# Export papers table
wrangler d1 export theophysics-db --table=the_twelve_papers --output=papers.csv
```

**Step 2**: Use Importer plugin
1. Open Command Palette: `Ctrl/Cmd + P`
2. Type "Importer: Import"
3. Select your CSV file
4. Map columns to YAML fields

**Step 3**: Review and tag imported notes

### From Google Drive / External Docs

**Method 1: Copy-Paste with Templater**
1. Copy headers/content from external source
2. Create new note
3. Run Templater command: `Parse Pasted Headers`
4. Auto-generates YAML and structure

**Method 2: Markdown Import**
1. Export as Markdown from source
2. Drag files into Obsidian vault
3. Run bulk YAML insertion (see below)

---

## 5. Bulk Operations

### Bulk Tag Application

**Using Linter Plugin:**
1. Settings → Linter → YAML
2. Set default tags for folders
3. Run: `Linter: Lint all files in folder`

**Using Templater Script:**
- Run `Apply Tags to Folder` command
- Select folder
- Choose tag template
- Applies to all notes in folder

### Bulk YAML Cleanup

**Find notes missing YAML:**
```dataview
LIST
FROM ""
WHERE !file.frontmatter
```

**Add default YAML to all:**
1. Use Bulk Note Editor plugin
2. Search: notes without frontmatter
3. Prepend template YAML

### Bulk Link Updates

**Find broken links:**
- Use "Broken Links" core plugin
- View all broken links
- Batch fix or remove

---

## 📊 Vault Statistics

```dataview
TABLE 
  length(file.lists) AS "Lists",
  length(file.tags) AS "Tags",
  length(file.outlinks) AS "Links"
FROM ""
SORT file.mtime DESC
LIMIT 10
```

### Current Vault Status

- **Total Notes**: (Use graph view stats)
- **Tagged Notes**: (Run Query 1)
- **Untagged Notes**: (Run Query 5)
- **Papers**: (Run Query 2)

---

## 🚀 Next Steps

1. **Tag Your Core Papers**: Start with the 12 Logos Papers
2. **Create Link Structure**: Connect related concepts
3. **Set Up Templates**: Use Templater for consistent note creation
4. **Run Dataview Queries**: Find gaps and organize
5. **Import External Content**: Bring in schema data and external docs

---

## 🔧 Plugin Setup Checklist

- [ ] Homepage - Set this dashboard as home
- [ ] Dataview - Enable for queries
- [ ] Templater - Configure scripts folder
- [ ] Advanced Tables - For editable tables
- [ ] Linter - For YAML consistency
- [ ] Bulk Note Editor - For mass operations
- [ ] Importer - For CSV/JSON imports
- [ ] Commander - For custom buttons

---

## 📚 Additional Resources

- [[Tags-Samples]] - Detailed tag reference
- [[Dataview-Templates]] - More query examples
- [[Templater-Scripts]] - Custom automation scripts
- [[Import-Guide]] - Step-by-step import instructions

---

**Last Updated**: 2025-10-17
**Vault Version**: THEOPHYSICS v1.0
