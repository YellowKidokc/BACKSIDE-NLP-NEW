---
title: Tab 0 - General Settings
version: 1.0
last_updated: 2025-01-15
status: draft
tags: [#plugin, #tab, #configuration]
---

# Tab 0: General Settings

**Purpose**: Control center for the entire plugin. All configuration, API keys, database connections, and system-wide settings.

---

## Sections

### 1. API Key Management
- OpenAI API Key input field
- Claude API Key input field
- Provider selection dropdowns (which model handles which tasks)
- Test connection buttons
- Cost tracking display (optional)

**Notes to implement**:
- Secure storage of API keys
- Validation on input
- Clear error messages if keys invalid

---

### 2. Database Connection
- PostgreSQL DSN input field
- Connection test button
- Sync frequency settings (immediate, 5min, 15min, manual)
- Auto-sync toggle
- Rebuild database button

**Notes to implement**:
- Handle connection failures gracefully
- Show connection status indicator
- Queue operations if database unavailable

---

### 3. Semantic Block Format
- Choose format: inline comments `%%semantic%%`, sidecar JSON, or both
- Block versioning settings
- Migration tools for format changes

**Notes to implement**:
- Backward compatibility essential
- Clear documentation of format

---

### 4. AI Behavior Mode
- Context request mode: explicit, silent, or hybrid
- Auto-scan on file save toggle
- AI provider assignment per task type
- Max context size slider (4k-128k tokens)

**Notes to implement**:
- Clear explanation of each mode
- User control over AI automation level

---

### 5. External Linking
- Enable/disable auto-linking to Stanford Encyclopedia of Philosophy
- Enable/disable auto-linking to Wikipedia
- Custom source configuration (add URLs, patterns)
- Link validation frequency

**Notes to implement**:
- Respect user preference for automation
- Allow manual override of auto-links

---

### 6. Coherence Settings
- Toggle Lowe Coherence Lagrangian calculations
- Set entropy weighting parameters
- Configure violation thresholds
- Coherence calculation frequency

**Notes to implement**:
- Provide sensible defaults
- Allow advanced users to tune parameters
- Explain what each parameter does

---

### 7. Fault Tolerance
- PostgreSQL required toggle (default: OFF)
- Sync retry attempts (default: 3)
- Sync retry interval (default: 30s)
- Auto-rebuild on corruption toggle
- Failure notification settings

**Notes to implement**:
- System should work without PostgreSQL by default
- Clear status indicators for degraded mode

---

### 8. Export Preferences
- Default export format
- Include/exclude history in exports
- Compression options
- Selective export settings

**Notes to implement**:
- Make exports portable
- Include reconstruction instructions

---

### 9. Prompt Management
- List of all 15+ prompts with edit buttons
- Regenerate prompt with AI button
- Reset to default button
- Prompt versioning

**Notes to implement**:
- Allow users to customize prompts
- Preserve custom prompts across updates
- Easy rollback to defaults

---

### 10. Recovery Tools
- **Rebuild PostgreSQL from Vault** button
- **Regenerate All Dashboards** button
- **Clear Sync Queue** button
- **View Error Log** button
- **Export Diagnostic Report** button

**Notes to implement**:
- Confirm before destructive operations
- Show progress during rebuild
- Log all recovery actions

---

### 11. Status Indicators
- PostgreSQL connection status (green/yellow/red)
- AI provider availability (OpenAI, Claude)
- Sync queue depth (pending operations)
- Last successful sync timestamp
- Current mode (normal, local-only, degraded)

**Notes to implement**:
- Always visible
- Click for details
- Clear visual hierarchy

---

## UI Mockup Notes

```
┌─────────────────────────────────────────────────────────┐
│ General Settings                                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ API Configuration                                       │
│ ┌─────────────────────────────────────────────────┐   │
│ │ OpenAI API Key: [••••••••••••••••] [Test]      │   │
│ │ Claude API Key: [••••••••••••••••] [Test]      │   │
│ │ Default Parser: [GPT-4 ▼]                      │   │
│ │ Default Strategy: [Claude-3-Opus ▼]            │   │
│ └─────────────────────────────────────────────────┘   │
│                                                         │
│ Database Connection                                     │
│ ┌─────────────────────────────────────────────────┐   │
│ │ PostgreSQL DSN: [postgresql://...] [Test]      │   │
│ │ Status: ● Connected                             │   │
│ │ Sync: [Auto ▼] every [5 min ▼]                │   │
│ │ [Rebuild Database]                              │   │
│ └─────────────────────────────────────────────────┘   │
│                                                         │
│ ... (other sections)                                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Implementation Priority

1. **Phase 1 (MVP)**: API keys, basic settings, semantic block format
2. **Phase 2**: Database connection, sync settings
3. **Phase 3**: AI behavior, prompt management
4. **Phase 4**: Advanced settings, recovery tools

---

## Related Documents
- [[Architecture_Overview|System Architecture]]
- [[Implementation_Settings|Settings Implementation Guide]]
- [[User_Guide_Settings|User Guide for Settings]]
