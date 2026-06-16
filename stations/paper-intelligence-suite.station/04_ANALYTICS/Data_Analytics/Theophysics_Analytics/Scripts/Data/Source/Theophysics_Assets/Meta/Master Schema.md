---
uuid: c1b2992a-0634-54a4-81df-9864eb395db6
title: 🧭 Master Schema (Dashboard)
author: David Lowe
type: note
created: '2025-11-22'
updated: '2025-11-22'
status: draft
file_path: Logos zright\Meta\Master Schema.md
uuid_generated_at: '2025-11-22T01:23:48.985290'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

# 🧭 Master Schema (Dashboard)

This is the quiet hub for navigation, conventions, and live indexes.

## Folders
- [[Research/TH]] (Theophysics)
- [[Research/JS]] (Jesus Series)
- [[Research/TR]] (Trinity)
- [[Research/HP]] (Hypothesis)
- [[Research/QW]] (Quantum Warfare)
- [[Research/DD]] (Deep Dives)
- [[Research/EX]] (Experimental)
- [[MOCs/Characters]] · [[MOCs/Topics]]

---

## Series Overview (live)
```dataview
TABLE WITHOUT ID file.link AS Paper, series, paper_number, characters, topics
FROM "Research"
WHERE series
GROUP BY series
```

## Characters (MOCs)
[[MOCs/Characters/GF]] · [[MOCs/Characters/JC]] · [[MOCs/Characters/HS]] · [[MOCs/Characters/ADV]]

## Top Topics (live)
```dataviewjs
const files = dv.pages().where(p => Array.isArray(p.topics));
const freq = new Map();
for (const p of files) for (const t of p.topics) freq.set(t, (freq.get(t)||0)+1);
const top = [...freq.entries()].sort((a,b)=> b[1]-a[1]).slice(0,20);
top.forEach(([t,c]) => dv.paragraph(`[[MOCs/Topics/${t}|${t}]] (${c})`));
```

---

## Conventions (short)
- **File name:** `[SERIES]-[Title-Kebab]-[NN].md` e.g. `TH-Master-Equation-Framework-01.md`
- **Properties (frontmatter) drive automation** (no visible #tags required)
- **Prev/Next/Home** links render at the bottom of each paper note
