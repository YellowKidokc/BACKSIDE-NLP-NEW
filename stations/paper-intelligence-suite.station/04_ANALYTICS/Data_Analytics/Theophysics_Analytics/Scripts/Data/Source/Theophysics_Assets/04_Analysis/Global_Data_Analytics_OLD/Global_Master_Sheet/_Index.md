---
uid: GMS-index-001
type: index
created: 2025-11-29
purpose: Global Master Sheet - 100% source of truth
---

# Global Master Sheet

> **Source of Truth** - The authoritative record for all extracted data.

---

## Purpose

This folder contains the **definitive, verified** data extracted from all 12 Logos Papers. When analytics run, they:

1. Extract data from papers
2. Process through Mechanisms
3. Display in Dashboards
4. **Store final results HERE**

If there's ever a conflict, **this folder is correct**.

---

## Structure

```
Global_Master_Sheet/
├── Definitions/     # All definitions (phrase + meaning)
├── Links/           # Verified external links
├── Tags/            # Authoritative tag assignments
├── Axioms/          # Core axioms from papers
└── Claims/          # Validated claims
```

---

## Data Categories

### Definitions
| Field | Type | Description |
|-------|------|-------------|
| `phrase` | string | The term being defined |
| `aliases` | array | Alternative names |
| `definition` | string | The meaning |
| `source_paper` | string | Which paper (P01-P12) |
| `source_location` | string | Section/paragraph |
| `tags` | array | Associated tags |

### Links
| Field | Type | Description |
|-------|------|-------------|
| `url` | string | The link |
| `title` | string | Link title |
| `domain` | string | physics/theology/etc. |
| `source_paper` | string | Which paper |
| `verified` | boolean | Link checked? |

### Tags
| Field | Type | Description |
|-------|------|-------------|
| `tag` | string | Tag name |
| `category` | string | Physics/Theology/etc. |
| `usage_count` | number | How many times used |
| `papers` | array | Papers using this tag |

### Axioms
| Field | Type | Description |
|-------|------|-------------|
| `axiom_id` | string | Unique ID |
| `statement` | string | The axiom |
| `source_paper` | string | Origin paper |
| `dependencies` | array | Related axioms |

### Claims
| Field | Type | Description |
|-------|------|-------------|
| `claim_id` | string | Unique ID |
| `statement` | string | The claim |
| `evidence` | array | Supporting evidence |
| `validation_status` | string | pending/validated/rejected |

---

## File Formats

### Option 1: Markdown with YAML Frontmatter
```markdown
---
phrase: "Logos Field"
aliases: ["Chi Field", "χ"]
definition: "The divine ordering principle..."
source_paper: P01
tags: [logos, theophysics, physics]
---

# Logos Field

The divine ordering principle that sustains coherence...
```

### Option 2: JSON (for Python integration)
```json
{
  "phrase": "Logos Field",
  "aliases": ["Chi Field", "χ"],
  "definition": "The divine ordering principle...",
  "source_paper": "P01",
  "tags": ["logos", "theophysics", "physics"]
}
```

### Option 3: Both (Markdown as primary, JSON as export)
- Primary storage: Markdown files
- Python reads: JSON exports
- Sync: Script converts between formats

---

## Integration with Python

Auto's Obsidian Definitions Manager can:
- **READ** from `Definitions/` folder
- **WRITE** new definitions here
- **SYNC** with the Obsidian Note Definitions plugin
- **EXPORT** to JSON for other tools

### Recommended Workflow
1. Analytics extract definitions → store as Markdown
2. Python exports to JSON for app
3. App edits → writes back to Markdown
4. Both systems stay in sync

---

## Aggregation Rules

When combining data from multiple papers:

1. **Duplicates**: Same definition in multiple papers
   - Keep one authoritative version
   - Track all source papers in `source_papers` array

2. **Conflicts**: Different definitions for same term
   - Flag for manual review
   - Store both with conflict marker

3. **Merging**: Similar definitions
   - Combine and note all sources
   - Create comprehensive definition

---

## Queries

### All Definitions
```dataview
TABLE phrase, source_paper, tags
FROM "Global_Data_Analytics/Global_Master_Sheet/Definitions"
SORT phrase ASC
```

### Definitions by Paper
```dataview
TABLE phrase, definition
FROM "Global_Data_Analytics/Global_Master_Sheet/Definitions"
WHERE source_paper = "P01"
```

### Cross-Paper Definitions
```dataview
TABLE phrase, length(source_papers) AS "Papers Using"
FROM "Global_Data_Analytics/Global_Master_Sheet/Definitions"
WHERE length(source_papers) > 1
SORT length(source_papers) DESC
```
