---
title: Tab 6 - Ontology & Concept Graph
version: 1.0
last_updated: 2025-01-15
status: outline
tags: [#tab, #ontology, #specification]
---

# Tab 6: Ontology & Concept Graph

**Purpose**: Structural backbone showing how all concepts relate to each other.

**Group**: Structural Analysis  
**Priority**: Phase 2

---

## Overview

This tab displays the concept graph with nodes (terms, entities) and edges (relationships like is-a, part-of, implies, depends-on).

---

## Core Functions

### 1. Concept Nodes
- All terms and variables as nodes
- Definitions and aliases
- First-seen dates
- Usage tracking

### 2. Relationship Edges
- is-a (taxonomy)
- part-of (composition)
- implies (logical)
- depends-on (dependency)
- causes (causal)
- contradicts (conflict)
- precedes (temporal)

### 3. Graph Visualization
- Interactive network graph
- Filterable by theory, domain, relationship type
- Zoom and pan
- Export capabilities

### 4. Health Metrics
- Node count
- Edge count
- Orphan detection (unconnected nodes)
- Cycle detection
- Structural coherence

---

## Integration
- **Word-ontology** repo for epistemic tagging
- **obsidian-note-definitions** for glossary
- **Obsidian-link-tag-plugin** for relationships

---

## Related Documents
- [[00_VAULT_SYSTEM/Config/12_Plugins/Theophysics_Obsidian_Plugin/01_TABS/00_TAB_INDEX|Tab Index]]
- [[00_VAULT_SYSTEM/Config/12_Plugins/Theophysics_Obsidian_Plugin/02_ARCHITECTURE/Semantic_Editor/Word_Ontology_Extraction|Word-ontology Extraction]]
