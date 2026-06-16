---
title: Theophysics Semantic Research Engine - Overview
version: 1.0
last_updated: 2025-01-15
status: active
tags: [#plugin, #overview, #theophysics]
---

# Theophysics Semantic Research Engine
## Complete Plugin Overview

**Purpose**: Transform an Obsidian vault into a coherent, testable, self-auditing knowledge system for academic research.

**Core Innovation**: Users write naturally in Markdown. AI parses everything—math, axioms, timelines, theories, evidence—and stores structured semantic meaning in hidden blocks within each note. All knowledge is portable, exportable, and reconstructable without any proprietary database.

---

## Executive Summary

This is not a simple Obsidian plugin. It is a **semantic research operating system** that transforms a vault of notes into a coherent, testable, self-auditing knowledge system.

### What It Does
- Detects and classifies axioms, claims, evidence, definitions, events, and theories
- Builds a unified knowledge graph connecting all concepts
- Computes coherence using the [[Lowe Coherence Lagrangian]]
- Identifies contradictions, gaps, and breakthrough insights
- Syncs to PostgreSQL for advanced analytics
- Maintains AI workspace with persistent understanding

### Who It's For
- **Researchers**: Building complex theoretical frameworks
- **Theologians**: Integrating faith and reason systematically
- **Physicists**: Developing new theories with mathematical rigor
- **Philosophers**: Constructing logically consistent arguments
- **Anyone**: Creating multi-theory knowledge systems

---

## Architecture Overview

### Four Fundamental Layers

**Layer 0: Obsidian + Vault**  
Raw markdown notes, images, files. This is what the user sees and edits.

**Layer 1: Extraction & Annotation**  
AI-powered parsing that detects axioms, claims, evidence, math, timelines, terms, and theories. Each piece gets a UUID and is stored in hidden semantic blocks within the markdown.

**Layer 2: Normalization & Graph**  
Unifies tags, links, ontology nodes, definitions, events, and math into a single knowledge graph. PostgreSQL mirrors this for analytics but is not the source of truth.

**Layer 3: Analytics, Coherence & Visualization**  
Dashboards, coherence scoring (via the Lowe Coherence Lagrangian), breakthrough detection, cross-theory conflict identification, and exportable reports.

---

## Complete Tab Structure

The plugin has **15 primary tabs** organized into 6 functional groups:

### Group A: Configuration
- **Tab 0**: [[00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Data/Source/Theophysics_Assets/Obsidian-Plugin-Module-Notes/01_TABS/Tab_00_General_Settings|General Settings]] - Control center for entire plugin

### Group B: Discovery & Analysis
- **Tab 1**: [[00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Data/Source/Theophysics_Assets/Obsidian-Plugin-Module-Notes/01_TABS/Tab_01_Research_Hub|Research Hub]] - AI-powered vault scanner and discovery engine
- **Tab 2**: [[Tab_02_Axiom_Manager|Axiom Manager]] - Foundational assumptions and rules
- **Tab 3**: [[Tab_03_Evidence_Manager|Evidence Manager]] - Supporting evidence and relationships
- **Tab 4**: [[Tab_04_Claim_Manager|Claim Manager]] - Assertions and verification status

### Group C: Structural Analysis
- **Tab 5**: [[Tab_05_Timeline_Engine|Timeline & Chronology Engine]] - Time-based reasoning
- **Tab 6**: [[Tab_06_Ontology_Graph|Ontology & Concept Graph]] - Structural backbone
- **Tab 7**: [[Tab_07_Math_Layer|Math Interpretation Layer]] - Mathematical formalism bridge
- **Tab 8**: [[Tab_08_External_Theories|External Theory Integration]] - Outside frameworks

### Group D: Progress & Diagnostics
- **Tab 9**: [[Tab_09_Breakthrough_Log|Breakthrough Log]] - Evolution of understanding
- **Tab 10**: [[00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Data/Source/Theophysics_Assets/Obsidian-Plugin-Module-Notes/01_TABS/Tab_10_Coherence_Dashboard|Coherence Dashboard]] - Primary diagnostic interface
- **Tab 11**: [[Tab_11_Tag_Analytics|Tag Analytics]] - Tagging patterns and clustering
- **Tab 12**: [[Tab_12_Theory_Manager|Theory Manager]] - Theories as first-class objects

### Group E: Data & Export
- **Tab 13**: [[Tab_13_Master_Truth_Manager|Master Truth Manager]] - Central knowledge repository
- **Tab 14**: [[Tab_14_Export_Manager|Export & Portability Manager]] - Semantic export system

### Group F: AI Workspace
- **Tab 15**: [[Tab_15_AI_Workspace|AI Workspace]] - AI's persistent understanding and notes

### Persistent UI Elements
- [[Semantic_Editor|Semantic Editor / Annotation Layer]] - Right-click annotation throughout Obsidian
- [[Status_Bar|Status Bar Indicator]] - System health at a glance

---

## Key Differentiators

### 1. Unified Semantic Model
Not point solutions—a single graph connecting tags, links, definitions, math, ontology, axioms, evidence across the entire vault.

### 2. Epistemic Typing
Not just "text"—every statement can be classified as axiom, claim, evidence, definition, giving the system logical structure.

### 3. Coherence Checking
Not just search—the system tells you whether your ideas hang together, using the [[Lowe Coherence Lagrangian]] as a principled variational foundation.

### 4. Portable by Design
All semantics live in markdown. No proprietary lock-in. Export your vault and everything travels with it.

### 5. AI-Native
Built for AI collaboration from the ground up, with structured prompts, provider flexibility, and continuous learning.

### 6. Theory-Building Focus
Designed for researchers constructing complex multi-theory frameworks—not just note-taking.

---

## Data Flow Summary

```
USER WRITES IN OBSIDIAN
         ↓
PLUGIN DETECTS CHANGE
         ↓
    ┌────┴────┐
    ↓         ↓
SEMANTIC    TRIGGER
BLOCK       AI SCAN
UPDATE         ↓
    ↓     CLAUDE REVIEWS
    ↓     (uses understanding.md)
    ↓         ↓
    ↓     CLAUDE TASKS GPT
    ↓     (via handoff)
    ↓         ↓
    ↓     GPT PARSES
    ↓     (extraction)
    ↓         ↓
    ↓     GPT RETURNS TO CLAUDE
    ↓     (results)
    ↓         ↓
    ↓     CLAUDE SYNTHESIZES
    ↓     (updates understanding)
    ↓         ↓
    └────┬────┘
         ↓
SYNC TO POSTGRESQL
(all items with UUIDs)
         ↓
REGENERATE DASHBOARDS
(/master-truth/ folder)
         ↓
UPDATE MASTER SHEET
         ↓
LOG TO AI SESSION
         ↓
READY FOR NEXT CHANGE
```

---

## Fault Tolerance Philosophy

**Core Principle**: Markdown is always the source of truth.

- PostgreSQL is a mirror/index, not the canonical store
- Each module can run independently
- Failures are isolated, logged, but don't cascade
- System continues in degraded mode if components fail
- One-button reconstruction from vault

See: [[00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Data/Source/Theophysics_Assets/Obsidian-Plugin-Module-Notes/02_ARCHITECTURE/Architecture_Fault_Tolerance|Fault Tolerance Architecture]]

---

## Master Truth Folder

The `/master-truth/` folder contains:
- **master-sheet.md** - Unified overview of all knowledge
- Sub-dashboards for each metric (concepts, math, axioms, evidence, claims, timeline, theories, coherence, breakthroughs)
- Historical snapshots with timestamps
- Progression analytics showing research velocity

See: [[00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Data/Source/Theophysics_Assets/Obsidian-Plugin-Module-Notes/03_MASTER_TRUTH/Master_Truth_Architecture|Master Truth Folder Architecture]]

---

## AI Integration

**Multi-Model Orchestration**:
- **Claude**: Strategic overseer, high-level understanding, breakthrough detection
- **GPT**: Analytical workhorse, document parsing, extraction

**Persistent Understanding**:
- AI maintains its own notes in `/ai-workspace/`
- Tracks understanding, observations, questions, suggestions
- Session logs for full transparency
- Handoff protocol between models

See: [[AI_Integration_Architecture|AI Integration Architecture]]

---

## PostgreSQL Schema

Complete database schema with tables for:
- Items (universal UUID system)
- Concepts, Axioms, Claims, Evidence
- Math objects, Variables, Timeline events
- Theories, External links, Relationships
- Coherence history, Breakthroughs
- AI sessions, AI understanding snapshots

See: [[PostgreSQL_Schema|PostgreSQL Schema Documentation]]

---

## Development Roadmap

### Phase 1: Core (MVP)
- Semantic block parser
- Right-click annotation menu
- Basic vault scanner
- In-memory semantic index

### Phase 2: Dashboards
- Dashboard generation from semantic index
- `/master-truth/` folder structure
- Master sheet generation

### Phase 3: PostgreSQL
- PostgreSQL sync layer
- Sync queue
- Rebuild capability

### Phase 4: AI Integration
- AI workspace
- Claude/GPT integration
- Prompt management

### Phase 5: Polish
- Iterate on individual modules
- Performance optimization
- User experience refinement

---

## Related Documents

### Architecture
- [[Architecture_Overview|System Architecture]]
- [[00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Data/Source/Theophysics_Assets/Obsidian-Plugin-Module-Notes/02_ARCHITECTURE/Architecture_Fault_Tolerance|Fault Tolerance Design]]
- [[Architecture_Data_Flow|Data Flow Diagrams]]

### Features
- [[Features_By_Tab|Complete Feature List by Tab]]
- [[Features_Semantic_Blocks|Semantic Block Format]]
- [[Features_Coherence_Scoring|Coherence Scoring System]]

### Implementation
- [[Implementation_PostgreSQL|PostgreSQL Integration]]
- [[Implementation_AI|AI Integration]]
- [[Implementation_Prompts|AI Prompt Specifications]]

### Design Decisions
- [[Decision_Markdown_Source_of_Truth|Why Markdown is Source of Truth]]
- [[Decision_Multi_Model_AI|Why Multi-Model AI Architecture]]
- [[Decision_Lowe_Lagrangian|Why Lowe Coherence Lagrangian]]

---

## Quick Start for Team Members

**For Developers**:
1. Read [[Architecture_Overview|System Architecture]]
2. Review [[PostgreSQL_Schema|Database Schema]]
3. Check [[Implementation_Guide|Implementation Guide]]

**For Researchers**:
1. Read this overview
2. Explore [[00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Data/Source/Theophysics_Assets/Obsidian-Plugin-Module-Notes/01_TABS/Tab_10_Coherence_Dashboard|Coherence Dashboard]]
3. Review [[02_LIBRARY/Glossary/Lowe_Coherence_Lagrangian|Coherence Theory]]

**For Marketers**:
1. Read [[Key_Differentiators|What Makes This Different]]
2. Review [[Use_Cases|Use Cases and Examples]]
3. Check [[Value_Proposition|Value Proposition]]

**For Third-Party Integrators**:
1. Read [[API_Documentation|API Documentation]]
2. Review [[Export_Formats|Export Formats]]
3. Check [[PostgreSQL_Schema|Database Schema]]

---

**Status**: Active development  
**Version**: 1.0  
**Last Updated**: 2025-01-15  
**Contact**: David Lowe
