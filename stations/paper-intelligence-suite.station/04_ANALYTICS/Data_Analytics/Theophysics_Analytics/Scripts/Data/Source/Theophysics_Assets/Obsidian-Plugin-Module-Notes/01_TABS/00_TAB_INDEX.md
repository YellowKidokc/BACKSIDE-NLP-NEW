---
title: Complete Tab Index
version: 1.0
last_updated: 2025-01-15
status: active
tags: [#plugin, #index, #tabs]
---

# Complete Tab Index

This document provides the canonical list of all 15 tabs in the Theophysics Semantic Research Engine plugin.

---

## Tab Organization

### Group A: Configuration
| Tab | Name | Status | Priority |
|-----|------|--------|----------|
| 0 | [[00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Data/Source/Theophysics_Assets/Obsidian-Plugin-Module-Notes/01_TABS/Tab_00_General_Settings\|General Settings]] | Draft | Phase 1 |

### Group B: Discovery & Analysis
| Tab | Name | Status | Priority |
|-----|------|--------|----------|
| 1 | [[00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Data/Source/Theophysics_Assets/Obsidian-Plugin-Module-Notes/01_TABS/Tab_01_Research_Hub\|Research Hub]] | Draft | Phase 1 |
| 2 | [[Tab_02_Axiom_Manager\|Axiom Manager]] | Outline | Phase 2 |
| 3 | [[Tab_03_Evidence_Manager\|Evidence Manager]] | Outline | Phase 2 |
| 4 | [[Tab_04_Claim_Manager\|Claim Manager]] | Outline | Phase 2 |

### Group C: Structural Analysis
| Tab | Name | Status | Priority |
|-----|------|--------|----------|
| 5 | [[Tab_05_Timeline_Engine\|Timeline & Chronology Engine]] | Outline | Phase 3 |
| 6 | [[Tab_06_Ontology_Graph\|Ontology & Concept Graph]] | Outline | Phase 2 |
| 7 | [[Tab_07_Math_Layer\|Math Interpretation Layer]] | Outline | Phase 3 |
| 8 | [[Tab_08_External_Theories\|External Theory Integration]] | Outline | Phase 4 |

### Group D: Progress & Diagnostics
| Tab | Name | Status | Priority |
|-----|------|--------|----------|
| 9 | [[Tab_09_Breakthrough_Log\|Breakthrough Log]] | Outline | Phase 4 |
| 10 | [[00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Data/Source/Theophysics_Assets/Obsidian-Plugin-Module-Notes/01_TABS/Tab_10_Coherence_Dashboard\|Coherence Dashboard]] | Draft | Phase 2 |
| 11 | [[Tab_11_Tag_Analytics\|Tag Analytics]] | Outline | Phase 4 |
| 12 | [[Tab_12_Theory_Manager\|Theory Manager]] | Outline | Phase 3 |

### Group E: Data & Export
| Tab | Name | Status | Priority |
|-----|------|--------|----------|
| 13 | [[Tab_13_Master_Truth_Manager\|Master Truth Manager]] | Outline | Phase 2 |
| 14 | [[Tab_14_Export_Manager\|Export & Portability Manager]] | Outline | Phase 3 |

### Group F: AI Workspace
| Tab | Name | Status | Priority |
|-----|------|--------|----------|
| 15 | [[Tab_15_AI_Workspace\|AI Workspace]] | Outline | Phase 4 |

---

## Persistent UI Elements (Not Tabs)

| Element | Description | Status | Priority |
|---------|-------------|--------|----------|
| [[Semantic_Editor\|Semantic Editor]] | Right-click annotation throughout Obsidian | Outline | Phase 1 |
| [[Status_Bar\|Status Bar Indicator]] | System health at a glance | Outline | Phase 1 |

---

## Development Phases

### Phase 1: Core (MVP)
**Goal**: Basic annotation and semantic block system
- Tab 0: General Settings (basic)
- Tab 1: Research Hub (basic scanning)
- Semantic Editor (right-click menu)
- Status Bar (basic indicators)

### Phase 2: Dashboards & Core Analysis
**Goal**: Visualization and basic analytics
- Tab 2: Axiom Manager
- Tab 3: Evidence Manager
- Tab 4: Claim Manager
- Tab 6: Ontology Graph
- Tab 10: Coherence Dashboard
- Tab 13: Master Truth Manager

### Phase 3: Advanced Analysis
**Goal**: Timeline, math, theories
- Tab 5: Timeline Engine
- Tab 7: Math Layer
- Tab 12: Theory Manager
- Tab 14: Export Manager

### Phase 4: AI & Polish
**Goal**: Full AI integration and refinement
- Tab 8: External Theories
- Tab 9: Breakthrough Log
- Tab 11: Tag Analytics
- Tab 15: AI Workspace
- Polish all existing tabs

---

## Quick Reference by Function

### For Writing & Annotation
- [[Semantic_Editor|Semantic Editor]] - Mark text as axiom, claim, evidence, etc.
- [[00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Data/Source/Theophysics_Assets/Obsidian-Plugin-Module-Notes/01_TABS/Tab_01_Research_Hub|Research Hub]] - Discover what needs attention

### For Analysis
- [[00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Data/Source/Theophysics_Assets/Obsidian-Plugin-Module-Notes/01_TABS/Tab_10_Coherence_Dashboard|Coherence Dashboard]] - Overall framework health
- [[Tab_02_Axiom_Manager|Axiom Manager]] - Foundational assumptions
- [[Tab_03_Evidence_Manager|Evidence Manager]] - Supporting evidence
- [[Tab_04_Claim_Manager|Claim Manager]] - Assertions and verification

### For Structure
- [[Tab_06_Ontology_Graph|Ontology Graph]] - Concept relationships
- [[Tab_05_Timeline_Engine|Timeline Engine]] - Chronological data
- [[Tab_07_Math_Layer|Math Layer]] - Mathematical formalism

### For Integration
- [[Tab_08_External_Theories|External Theories]] - Outside frameworks
- [[Tab_12_Theory_Manager|Theory Manager]] - Theory management

### For Progress Tracking
- [[Tab_09_Breakthrough_Log|Breakthrough Log]] - Major insights
- [[Tab_11_Tag_Analytics|Tag Analytics]] - Tagging patterns
- [[Tab_13_Master_Truth_Manager|Master Truth Manager]] - Central repository

### For Export & AI
- [[Tab_14_Export_Manager|Export Manager]] - Portability
- [[Tab_15_AI_Workspace|AI Workspace]] - AI understanding

### For Configuration
- [[00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Data/Source/Theophysics_Assets/Obsidian-Plugin-Module-Notes/01_TABS/Tab_00_General_Settings|General Settings]] - All configuration
- [[Status_Bar|Status Bar]] - System status

---

## Documentation Status Legend

- **Draft**: Detailed outline with implementation notes
- **Outline**: Basic structure defined, needs details
- **Planned**: Identified but not yet documented
- **Complete**: Fully documented and ready for implementation

---

## Notes for Development

### Dependencies Between Tabs
- Most tabs depend on **Tab 0** (settings) and **Semantic Editor**
- **Tab 10** (Coherence) depends on Tabs 2, 3, 4 (Axiom, Evidence, Claim)
- **Tab 13** (Master Truth) aggregates data from all other tabs
- **Tab 15** (AI Workspace) integrates with all tabs

### Shared Components
All tabs share:
- Semantic block parser
- UUID system
- PostgreSQL sync layer
- In-memory semantic index
- Dashboard generation engine

### UI Consistency
All tabs should follow:
- Consistent header with tab name and actions
- Status indicators where relevant
- Scope selector (note/folder/vault) where applicable
- Export button for tab-specific data
- Help/documentation link

---

## Related Documents
- [[00_VAULT_SYSTEM/Config/12_Plugins/Theophysics_Obsidian_Plugin/00_OVERVIEW|Plugin Overview]]
- [[Architecture_Overview|System Architecture]]
- [[Implementation_Guide|Implementation Guide]]
- [[User_Guide|User Guide]]
