---
title: Tab 1 - Research Hub
version: 1.0
last_updated: 2025-01-15
status: draft
tags: [#plugin, #tab, #discovery]
---

# Tab 1: Research Hub

**Purpose**: AI-powered brain that continuously scans and understands your vault. Discovery engine for new concepts, terms, and connections.

---

## Core Functions

### 1. Vault Scanner
- Detects new terms, theories, math expressions, proper names, dates
- Incremental scanning (only changed files)
- Background worker for heavy computation
- Scan history and statistics

### 2. Auto-Discovery Panel
- Concepts needing definitions
- Variables needing naming
- Theories needing linking
- Orphaned items (defined but unused)

### 3. External Link Suggestions
- Proposed connections to Stanford Encyclopedia of Philosophy
- Proposed connections to Wikipedia
- Custom source suggestions
- Relevance scoring for each suggestion

### 4. Gap Analysis
- Missing definitions
- Undefined terms
- Unlinked theories
- Unsupported claims
- Timeline gaps

### 5. Action Queue
- Prioritized list of research tasks
- User can mark items as done or dismiss
- Tracks completion over time
- Suggests next actions

### 6. Sync Function
- Updates all semantic blocks
- Pushes changes to PostgreSQL
- Regenerates Master Sheet
- Manual trigger or auto-sync

---

## UI Notes

```
┌─────────────────────────────────────────────────────────┐
│ Research Hub                          [Scan Now]        │
├─────────────────────────────────────────────────────────┤
│ Last Scan: 2 minutes ago              Status: ● Active  │
│                                                         │
│ Action Queue (12 items)                                 │
│ ┌─────────────────────────────────────────────────┐   │
│ │ ⚠ Define term: "Ω" (used in 3 equations)       │   │
│ │ 💡 Link "quantum decoherence" to SEP            │   │
│ │ ⚠ Resolve axiom contradiction: ax001 ↔ ax017   │   │
│ │ ... (9 more)                                    │   │
│ └─────────────────────────────────────────────────┘   │
│                                                         │
│ Discoveries This Week                                   │
│ • 12 new concepts                                       │
│ • 3 new axioms                                          │
│ • 8 new evidence items                                  │
│ • 2 breakthroughs detected                              │
└─────────────────────────────────────────────────────────┘
```

---

## Implementation Notes

- Incremental indexing to avoid re-scanning entire vault
- Cache vault state between scans
- Performance target: <30 seconds for 10,000 notes
- Graceful handling of parse errors

---

## Related Documents
- [[Architecture_Scanning|Vault Scanning Architecture]]
- [[Implementation_Discovery|Discovery Engine Implementation]]
