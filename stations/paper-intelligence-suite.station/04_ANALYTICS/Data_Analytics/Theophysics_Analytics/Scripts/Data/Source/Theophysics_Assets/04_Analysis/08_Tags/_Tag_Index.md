---
uid: TAG-index-001
type: index
created: 2025-11-29
purpose: Master index of all tags in the Theophysics vault
---

# Tag Index

> Master taxonomy for organizing and navigating Theophysics content.

---

## Tag Categories

| Category | Location | Count | Description |
|----------|----------|-------|-------------|
| [[_Physics_Tags\|Physics]] | `08_Tags/Physics/` | 40+ | Quantum mechanics, relativity, thermodynamics |
| [[_Theology_Tags\|Theology]] | `08_Tags/Theology/` | 25+ | Biblical concepts, Trinity, salvation |
| [[_Theophysics_Tags\|Theophysics]] | `08_Tags/Theophysics/` | 15+ | Bridge concepts, Logos Field, Grace Function |
| [[_Information_Tags\|Information]] | `08_Tags/Information/` | 15+ | Information theory, computation, complexity |
| [[_Philosophy_Tags\|Philosophy]] | `08_Tags/Philosophy/` | 15+ | Consciousness, ontology, epistemology |

---

## Tag Usage Statistics

```dataview
TABLE WITHOUT ID
  length(rows) AS "Total Notes",
  sum(rows.file.outlinks.length) AS "Total Links",
  round(average(rows.coherence_score), 2) AS "Avg Coherence"
FROM "02_Foundations" OR "04_Integration" OR "05_Doctrine"
GROUP BY true
```

---

## Most Used Tags

```dataview
TABLE WITHOUT ID
  tag AS "Tag",
  length(rows) AS "Usage Count"
FROM "02_Foundations" OR "04_Integration" OR "05_Doctrine" OR "05_Hubs"
FLATTEN file.tags AS tag
GROUP BY tag
SORT length(rows) DESC
LIMIT 20
```

---

## Tag Co-occurrence Matrix

Tags that frequently appear together indicate conceptual relationships:

```dataviewjs
const pages = dv.pages('"02_Foundations" OR "04_Integration" OR "05_Doctrine"');
let tagPairs = {};

for (let page of pages) {
    if (page.file.tags) {
        let tags = Array.from(page.file.tags);
        for (let i = 0; i < tags.length; i++) {
            for (let j = i + 1; j < tags.length; j++) {
                let pair = [tags[i], tags[j]].sort().join(" + ");
                tagPairs[pair] = (tagPairs[pair] || 0) + 1;
            }
        }
    }
}

let sorted = Object.entries(tagPairs).sort((a, b) => b[1] - a[1]).slice(0, 10);
dv.table(["Tag Pair", "Co-occurrences"], sorted);
```

---

## Untagged Content

Notes that need tagging:

```dataview
LIST
FROM "02_Foundations" OR "04_Integration" OR "05_Doctrine"
WHERE !file.tags OR length(file.tags) = 0
LIMIT 10
```

---

## How to Use Tags

### In Frontmatter
```yaml
tags:
  - entropy
  - grace
  - theophysics
```

### Tag File Structure
Each tag has a dedicated file that:
1. Defines the concept
2. Lists related tags
3. Shows all notes using the tag via Dataview
4. Links to relevant atoms/molecules/hubs

### Tag Naming Conventions
- Use lowercase: `entropy` not `Entropy`
- Use hyphens for multi-word: `quantum-mechanics`
- Prefix domain tags: `physics/entropy`, `theology/grace`
