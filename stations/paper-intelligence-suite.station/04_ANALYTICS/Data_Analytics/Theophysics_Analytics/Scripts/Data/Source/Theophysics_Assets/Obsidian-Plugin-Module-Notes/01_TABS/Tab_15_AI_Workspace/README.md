---
title: Tab 15 - AI Workspace
version: 1.0
last_updated: 2025-01-15
status: outline
tags: [#tab, #ai, #specification]
---

# Tab 15: AI Workspace

**Purpose**: AI's dedicated space for persistent understanding and notes.

**Group**: AI Workspace  
**Priority**: Phase 4

---

## Overview

This tab provides visibility into the AI's "mind"—its understanding, observations, questions, and suggestions. The AI maintains persistent notes that evolve over time.

---

## Core Functions

### 1. Understanding Viewer
- Display AI's current mental model of your framework
- Key variables and their meanings
- Active concerns
- Pending questions
- Confidence levels

### 2. Session Log Browser
- Chronological record of all AI activity
- What was analyzed when
- Actions taken
- Items affected
- Duration and tokens used

### 3. Observations Panel
- Patterns the AI has noticed
- Structural insights
- Potential issues
- Breakthrough candidates
- Circulation patterns (concepts approached repeatedly)

### 4. Questions Panel
- Questions the AI has for you
- Requires human input
- Prioritized by importance
- Answer tracking

### 5. Suggestions Panel
- Improvements the AI recommends
- Prioritized by impact
- Accept/reject tracking
- Learning from decisions

### 6. Claude Workspace
- Strategic notes
- Task queue
- Handoff instructions to GPT
- High-level analysis

### 7. GPT Workspace
- Parsing results
- Extraction logs
- Classification decisions
- Handoff results to Claude

### 8. Handoff Viewer
- Communication between Claude and GPT
- Task assignments
- Results and flags
- Workflow visualization

### 9. AI Status Indicators
- Provider availability (Claude, GPT)
- Current mode (active, idle, processing)
- Queue depth
- Rate limit status

### 10. Manual Triggers
- Force vault scan
- Request strategic review
- Process pending tasks
- Regenerate understanding

---

## AI Architecture

### Multi-Model Orchestration
- **Claude**: Strategic overseer, high-level understanding, breakthrough detection
- **GPT**: Analytical workhorse, document parsing, extraction

### Persistent Understanding
- AI maintains `/ai-workspace/` folder with:
  - `understanding.md` - Current mental model
  - `session-log.md` - Activity history
  - `observations.md` - Noticed patterns
  - `questions.md` - Needs human input
  - `suggestions.md` - Recommendations

---

## Integration
- **Obsidian-AI-Claude** repo
- **Obsidian-AI-Codex** repo
- **AI-Chat-Export** repos for conversation archiving

---

## Related Documents
- [[00_VAULT_SYSTEM/Config/12_Plugins/Theophysics_Obsidian_Plugin/01_TABS/00_TAB_INDEX|Tab Index]]
- [[AI_Integration_Architecture|AI Integration Architecture]]
