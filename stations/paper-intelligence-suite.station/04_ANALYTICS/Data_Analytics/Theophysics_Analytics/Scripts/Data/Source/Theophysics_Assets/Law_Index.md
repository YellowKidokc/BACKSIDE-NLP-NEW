---
type: index
role: laws
aliases:
- Laws Index
uuid: d6bfd4da-a80a-5d9a-aa85-2578bdf86578
title: Law Index
author: David Lowe
created: null
updated: '2025-11-22'
status: draft
file_path: [[Theophysics_Glossary#Logos|Logos]] zright\Meta\Law_Index.md
uuid_generated_at: '2025-11-22T01:23:48.906365'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

# Law Index

This page provides a master index of all Laws defined in the TheoPhysics framework. All laws are projections of the [[00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Data/Source/Theophysics_Assets/Master_Equation/Master-Equation]].

---

## The 12 Laws of TheoPhysics

```dataview
TABLE WITHOUT ID
  file.link AS "Law",
  L.trinity_aspects AS "Trinity Aspect",
  L.component_atoms AS "Core Atoms"
FROM "Library/Laws"
WHERE file.name != "LAW-00-Carrier-Principle" AND file.name != "Law_Index" AND contains(file.name, "LAW")
SORT L.law ASC
FLATTEN file.frontmatter as L
```

## The Meta-Law

```dataview
TABLE WITHOUT ID
  file.link AS "Law",
  L.trinity_aspects AS "Trinity Aspect",
  L.component_atoms AS "Core Atoms"
FROM "Library/Laws"
WHERE file.name = "LAW-00-Carrier-Principle"
FLATTEN file.frontmatter as L
```




