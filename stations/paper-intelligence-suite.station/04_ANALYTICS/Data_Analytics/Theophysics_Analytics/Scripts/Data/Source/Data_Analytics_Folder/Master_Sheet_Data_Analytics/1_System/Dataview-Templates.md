---
uuid: ac234d1a-259a-5156-9ac9-70de1715cdf3
title: 📊 Dataview Query Templates
author: David Lowe
type: template
created: '2025-11-22'
updated: '2025-11-22'
status: draft
file_path: 00_VAULT_SYSTEM\05_Workflow\Dataview-Templates.md
uuid_generated_at: '2025-11-22T01:23:02.523098'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

# 📊 Dataview Query Templates

> Powerful queries for searching, filtering, and organizing your THEOPHYSICS vault. Copy and customize these for your needs.

---

## 🔍 Basic Queries

### All Notes with Tags
```dataview
TABLE tags, file.mtime AS "Modified"
FROM ""
WHERE tags
SORT file.mtime DESC
```

### Recent Notes (Last 7 Days)
```dataview
TABLE file.mtime AS "Modified", tags
FROM ""
WHERE file.mtime >= date(today) - dur(7 days)
SORT file.mtime DESC
```

### Notes by Folder
```dataview
TABLE file.folder, tags, file.mtime AS "Modified"
FROM ""
SORT file.folder ASC, file.name ASC
```

---

## 📚 Paper & Research Queries

### All Papers by Status
```dataview
TABLE paper_id, status, date, tags
FROM ""
WHERE paper_id
SORT status ASC, date DESC
```

### Draft Papers Needing Work
```dataview
LIST
FROM ""
WHERE status = "draft" AND paper_id
SORT file.name ASC
```

### Papers by Topic
```dataview
TABLE paper_id, topic, date
FROM ""
WHERE paper_id AND topic
SORT topic ASC
```

### Papers Referencing Specific Equation
```dataview
LIST
FROM ""
WHERE contains(file.content, "Master Equation") OR contains(tags, "logos/master")
SORT file.name ASC
```

---

## 🏷️ Tag-Based Queries

### Notes by Pillar
```dataview
TABLE tags, file.mtime AS "Modified"
FROM [[pillar/physics]] OR [[pillar/theology]] OR [[pillar/consciousness]] OR [[pillar/mathematics]]
SORT file.name ASC
```

### [[Theophysics_Glossary#Master Equation|Master Equation]] Components (χ Variables)
```dataview
TABLE component, equation_id, tags
FROM ""
WHERE contains(tags, "χ_var")
SORT component ASC
```

### Grace-Related Notes
```dataview
LIST
FROM [[χ_var/Grace]] OR [[logos/grace]]
SORT file.name ASC
```

### Entropy & Decay Notes
```dataview
TABLE tags, file.mtime AS "Modified"
FROM [[χ_var/Entropy]] OR [[logos/decay]]
SORT file.mtime DESC
```

### All 10 Deep Laws
```dataview
TABLE law_number, law_name, tags
FROM ""
WHERE contains(tags, "law/")
SORT law_number ASC
```

---

## ⚡ Miracle Analysis Queries

### All Miracle Notes
```dataview
TABLE miracle_type, scripture_ref, tags
FROM ""
WHERE contains(tags, "miracle/")
SORT scripture_ref ASC
```

### Healing Miracles
```dataview
LIST scripture_ref
FROM [[miracle/healing]]
SORT scripture_ref ASC
```

### Matter Multiplication Events
```dataview
TABLE scripture_ref, physics_mechanism
FROM [[miracle/matter]]
SORT scripture_ref ASC
```

### Resurrection Events
```dataview
TABLE scripture_ref, key_insight
FROM [[miracle/resurrection]]
SORT scripture_ref ASC
```

---

## 🔬 Experimental Protocol Queries

### All Experiments
```dataview
TABLE experiment_id, status, priority, expected_impact
FROM ""
WHERE contains(tags, "experiment/")
SORT priority DESC, status ASC
```

### High Priority Experiments
```dataview
LIST
FROM ""
WHERE priority = "CRITICAL" OR priority = "High"
SORT experiment_id ASC
```

### Experiments by Status
```dataview
TABLE experiment_id, status, difficulty
FROM ""
WHERE experiment_id
GROUP BY status
```

---

## 📖 Scripture & Theology Queries

### Notes by Scripture Reference
```dataview
TABLE scripture_ref, topic, tags
FROM ""
WHERE scripture_ref
SORT scripture_ref ASC
```

### Theological Concepts
```dataview
LIST topic
FROM [[pillar/theology]]
WHERE topic
SORT topic ASC
```

### Trinity-Related Notes
```dataview
TABLE tags, file.mtime AS "Modified"
FROM ""
WHERE contains(file.content, "Trinity") OR contains(file.content, "Father") AND contains(file.content, "Son")
SORT file.mtime DESC
```

---

## 🧮 Mathematical Framework Queries

### All Equations
```dataview
TABLE equation_id, equation_type, tags
FROM ""
WHERE equation_id
SORT equation_id ASC
```

### Operators (Λ, Ψ, Γ, Ω)
```dataview
TABLE operator_name, description, tags
FROM [[math_role/operator]]
SORT operator_name ASC
```

### Field Equations
```dataview
LIST equation_id
FROM [[math_role/field]]
SORT equation_id ASC
```

### Metrics & Measurements
```dataview
TABLE metric_name, formula, tags
FROM [[math_role/metric]]
SORT metric_name ASC
```

---

## 🔗 Link Analysis Queries

### Most Connected Notes (High Outlinks)
```dataview
TABLE length(file.outlinks) AS "Links Out", length(file.inlinks) AS "Links In", tags
FROM ""
SORT length(file.outlinks) DESC
LIMIT 20
```

### Orphan Notes (No Links)
```dataview
LIST
FROM ""
WHERE length(file.outlinks) = 0 AND length(file.inlinks) = 0
SORT file.name ASC
```

### Notes Linking to Specific Note
```dataview
LIST
FROM [[Master-Equation]]
SORT file.name ASC
```

---

## ⚠️ Maintenance Queries

### Untagged Notes (Needs Attention)
```dataview
LIST file.mtime AS "Modified"
FROM ""
WHERE !tags OR length(tags) = 0
SORT file.mtime DESC
LIMIT 50
```

### Notes Missing YAML Frontmatter
```dataview
LIST
FROM ""
WHERE !file.frontmatter
SORT file.name ASC
```

### Notes with Broken Links
```dataview
TABLE file.outlinks AS "Outlinks"
FROM ""
WHERE length(file.outlinks) > 0
SORT file.name ASC
```

### Large Notes (>5000 words)
```dataview
TABLE length(file.content) AS "Characters", tags
FROM ""
WHERE length(file.content) > 20000
SORT length(file.content) DESC
```

### Recently Modified Notes
```dataview
TABLE file.mtime AS "Modified", tags
FROM ""
SORT file.mtime DESC
LIMIT 30
```

---

## 📈 Statistics & Analytics

### Tag Usage Statistics
```dataview
TABLE length(tags) AS "Tag Count", tags
FROM ""
WHERE tags
SORT length(tags) DESC
LIMIT 30
```

### Notes by Creation Date
```dataview
TABLE file.ctime AS "Created", tags
FROM ""
SORT file.ctime DESC
LIMIT 20
```

### Folder Statistics
```dataview
TABLE length(rows) AS "Note Count"
FROM ""
GROUP BY file.folder
SORT length(rows) DESC
```

### Word Count by Tag
```dataview
TABLE length(file.content) AS "Characters", file.name
FROM [[pillar/physics]]
SORT length(file.content) DESC
LIMIT 10
```

---

## 🎯 Advanced Custom Queries

### Papers Needing Scripture References
```dataview
LIST
FROM ""
WHERE paper_id AND !scripture_ref
SORT paper_id ASC
```

### Experiments Without Protocols
```dataview
TABLE experiment_id, status
FROM ""
WHERE experiment_id AND !methodology_keywords
SORT experiment_id ASC
```

### Laws Without Examples
```dataview
LIST
FROM ""
WHERE law_number AND !example
SORT law_number ASC
```

### Cross-Domain Notes (Multi-Pillar)
```dataview
TABLE tags, file.name
FROM ""
WHERE contains(tags, "pillar/physics") AND contains(tags, "pillar/theology")
SORT file.name ASC
```

---

## 🔄 Dynamic Queries (Update Automatically)

### Today's Work
```dataview
TABLE file.mtime AS "Modified", tags
FROM ""
WHERE file.mtime >= date(today)
SORT file.mtime DESC
```

### This Week's Progress
```dataview
TABLE file.ctime AS "Created", tags
FROM ""
WHERE file.ctime >= date(today) - dur(7 days)
SORT file.ctime DESC
```

### This Month's Papers
```dataview
TABLE paper_id, status, date
FROM ""
WHERE paper_id AND date >= date(today) - dur(30 days)
SORT date DESC
```

---

## 💡 Query Customization Tips

### Filter by Multiple Tags
```dataview
FROM [[tag1]] AND [[tag2]]
```

### Exclude Specific Tags
```dataview
FROM "" WHERE !contains(tags, "exclude-tag")
```

### Search File Content
```dataview
WHERE contains(file.content, "search term")
```

### Combine Conditions
```dataview
WHERE (condition1 OR condition2) AND condition3
```

### Group Results
```dataview
GROUP BY field_name
```

### Limit Results
```dataview
LIMIT 20
```

---

## 🚀 Quick Reference

**Common Fields:**
- `file.name` - Note name
- `file.mtime` - Modified time
- `file.ctime` - Created time
- `file.folder` - Folder path
- `file.tags` - All tags
- `file.outlinks` - Outgoing links
- `file.inlinks` - Incoming links
- `file.content` - Full note content

**Common Operators:**
- `=` - Equals
- `!=` - Not equals
- `>` / `<` - Greater/less than
- `>=` / `<=` - Greater/less or equal
- `AND` / `OR` - Logical operators
- `contains()` - Contains text/tag
- `length()` - Count items

---

**Last Updated**: 2025-10-17
**Total Queries**: 50+
**Categories**: Basic, Papers, Tags, Miracles, Experiments, Scripture, Math, Links, Maintenance, Statistics, Advanced
