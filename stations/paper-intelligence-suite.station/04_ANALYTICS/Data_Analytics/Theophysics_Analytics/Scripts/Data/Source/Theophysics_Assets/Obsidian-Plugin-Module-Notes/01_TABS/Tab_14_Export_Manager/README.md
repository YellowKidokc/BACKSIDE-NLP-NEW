---
title: Tab 14 - Export & Portability Manager
version: 1.0
last_updated: 2025-01-15
status: outline
tags: [#tab, #export, #specification]
---

# Tab 14: Export & Portability Manager

**Purpose**: Ensures all semantics survive export and can be reconstructed elsewhere.

**Group**: Data & Export  
**Priority**: Phase 3

---

## Overview

This tab handles all export functionality, ensuring semantic blocks, relationships, and metadata are preserved and portable.

---

## Core Functions

### 1. Semantic Block Export
- Export notes with embedded `%%semantic%%` blocks intact
- Preserve all UUIDs
- Maintain file structure
- Include metadata

### 2. Project Graph Export
- Generate `semantic-graph.json` containing:
  - All annotations
  - All concepts
  - All events
  - All theories
  - All edges/relationships
  - All metrics

### 3. Database Export
- Optional PostgreSQL dump
- SQL format for reconstruction
- Schema included
- Data integrity verification

### 4. Bundle Creation
- One-click zip of:
  - Vault (with semantic blocks)
  - Graph JSON
  - Optional database dump
  - Manifest file
- Includes reconstruction instructions

### 5. Import Function
- Receive exported bundles
- Reconstruct semantic state
- Verify integrity
- Merge with existing vault

### 6. Format Options
- Embedded blocks (default)
- Sidecar JSON files
- Both (redundant)
- Custom formats

---

## Integration
- **Quartz** repo for web publishing
- **MK-Docs-Obsidian** for documentation export

---

## Related Documents
- [[00_VAULT_SYSTEM/Config/12_Plugins/Theophysics_Obsidian_Plugin/01_TABS/00_TAB_INDEX|Tab Index]]
- [[Semantic_Block_Format|Semantic Block Specification]]
