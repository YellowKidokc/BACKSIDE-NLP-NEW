---
title: Fault Tolerance Architecture
version: 1.0
last_updated: 2025-01-15
status: active
tags: [#architecture, #fault-tolerance, #resilience]
---

# Fault Tolerance Architecture

**Core Principle**: Markdown is always the source of truth. Everything else can fail and be reconstructed.

---

## Design Philosophy

The entire system is built on these principles:

1. **Markdown is truth**: Everything can be reconstructed from the vault
2. **Modules are islands**: Each can function independently
3. **Failures are logged, not fatal**: The system continues and tells you what's wrong
4. **Sync is queued, not blocking**: If a sync target is down, operations wait
5. **Degraded mode is acceptable**: Partial functionality is better than no functionality
6. **Reconstruction is always possible**: One button rebuilds everything from markdown
7. **User is informed, not blocked**: Clear status indicators, not cryptic errors

---

## Isolation Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     MARKDOWN VAULT (Source of Truth)            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ Note.md  │  │ Note.md  │  │ Note.md  │  │ Note.md  │        │
│  │ %%sem%%  │  │ %%sem%%  │  │ %%sem%%  │  │ %%sem%%  │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
└─────────────────────────────────────────────────────────────────┘
         │              │              │              │
         ▼              ▼              ▼              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     SEMANTIC LAYER (In-Memory)                  │
│  Parses semantic blocks → Builds unified graph → Holds in RAM   │
│  CAN FUNCTION WITHOUT POSTGRES                                  │
└─────────────────────────────────────────────────────────────────┘
         │                                           │
         ▼                                           ▼
┌──────────────────────┐                ┌──────────────────────┐
│  POSTGRESQL (Mirror) │                │  DASHBOARDS (Output) │
│  Optional analytics  │                │  /master-truth/      │
│  IF FAILS: Log error │                │  IF FAILS: Log error │
│  System continues    │                │  System continues    │
└──────────────────────┘                └──────────────────────┘
         │                                           │
         ▼                                           ▼
┌──────────────────────┐                ┌──────────────────────┐
│  AI WORKSPACE        │                │  COHERENCE ENGINE    │
│  /ai-workspace/      │                │  Lowe Lagrangian     │
│  IF FAILS: Log error │                │  IF FAILS: Log error │
│  System continues    │                │  System continues    │
└──────────────────────┘                └──────────────────────┘
```

---

## Failure Isolation by Layer

### Layer 1: Semantic Block Parsing
**What it does**: Parses `%%semantic%%` blocks from markdown notes

**If it fails**:
- Log error: "Failed to parse semantic block in Note.md"
- Mark note as "needs-repair" in status
- CONTINUE processing other notes
- DO NOT crash the plugin

**Result**: One malformed note doesn't break the whole vault scan.

---

### Layer 2: PostgreSQL Sync
**What it does**: Syncs semantic data to PostgreSQL for analytics

**If it fails**:
- Log error: "PostgreSQL sync failed for item UUID"
- Queue item for retry (up to 3 attempts)
- Mark item as "sync-pending" in local state
- CONTINUE processing
- Dashboard still generates from in-memory data

**If PostgreSQL completely unavailable**:
- Log warning: "PostgreSQL unavailable, running in local-only mode"
- All features work except advanced SQL queries
- When Postgres comes back, run full reconciliation

**Result**: PostgreSQL going down doesn't stop anything. When it comes back, the system catches up.

---

### Layer 3: Dashboard Generation
**What it does**: Creates markdown dashboards in `/master-truth/`

**If it fails**:
- Log error: "Failed to generate axioms dashboard"
- Mark dashboard as "stale" with timestamp
- CONTINUE generating other dashboards
- Show user notification: "Some dashboards could not be updated"

**Result**: A bug in the timeline dashboard doesn't break the axiom dashboard.

---

### Layer 4: AI Processing
**What it does**: Calls Claude/GPT for analysis and extraction

**If it fails**:
- Log error: "Claude API unavailable"
- TRY: Fall back to GPT
- IF FALLBACK FAILS:
  - Log error: "All AI providers unavailable"
  - CONTINUE without AI processing
  - Mark items as "needs-ai-review"
  - User can manually trigger AI review later

**Result**: API outage doesn't break your ability to write notes or view dashboards.

---

### Layer 5: Coherence Calculation
**What it does**: Computes Lowe Coherence Lagrangian score

**If it fails**:
- Log error: "Coherence calculation failed"
- Display last known coherence score with "(stale)" marker
- CONTINUE all other operations
- Queue coherence recalculation for next cycle

**Result**: A bug in coherence math doesn't break the rest of the system.

---

## Module Independence Matrix

| Module | Required | Optional | If PostgreSQL Fails | If AI Fails | If Other Module Fails |
|--------|----------|----------|---------------------|-------------|-----------------------|
| Research Hub | Markdown + Semantic Blocks | PostgreSQL, AI | Works locally | Works without suggestions | Independent |
| Axiom Manager | Semantic Blocks | PostgreSQL, AI, Coherence | Works locally | Works without analysis | Independent |
| Evidence Manager | Semantic Blocks | PostgreSQL, AI | Works locally | Works without analysis | Independent |
| Claim Manager | Semantic Blocks | PostgreSQL, AI | Works locally | Works without analysis | Independent |
| Timeline Engine | Semantic Blocks | PostgreSQL, AI | Works locally | Works without parsing | Independent |
| Ontology Graph | Semantic Blocks | PostgreSQL, AI | Works locally | Works without suggestions | Independent |
| Math Layer | Semantic Blocks | PostgreSQL, AI | Works locally | Works without translation | Independent |
| External Theories | Semantic Blocks | PostgreSQL, AI, Network | Works locally | Manual linking only | Independent |
| Breakthrough Log | Semantic Blocks | PostgreSQL, AI | Works locally | Manual only | Independent |
| Coherence Dashboard | Semantic Blocks | PostgreSQL, AI | Works locally | Basic scoring only | Independent |
| Tag Analytics | Tags in Notes | PostgreSQL | Works locally | Works fully | Independent |
| Theory Manager | Semantic Blocks | PostgreSQL, AI | Works locally | Works without analysis | Independent |

**Key insight**: Every module can function with just markdown and semantic blocks. Everything else enhances but doesn't require.

---

## Sync Queue Architecture

To handle PostgreSQL failures gracefully, we implement a sync queue that buffers operations and retries them.

### Sync Queue Files
```
/plugin-data/
    sync-queue.json       ← Pending PostgreSQL operations
    sync-errors.json      ← Failed operations for review
    sync-status.json      ← Current sync state
```

### Processing Logic
```
EVERY 30 SECONDS (configurable):
  IF PostgreSQL is available:
    FOR EACH item in sync-queue:
      TRY: Execute operation
      IF SUCCESS: Remove from queue
      IF FAIL: 
        Increment attempts
        IF attempts > 3: Move to sync-errors.json
        ELSE: Leave in queue for retry
```

---

## Reconstruction Protocol

### Full Reconstruction from Markdown
```
1. DROP all PostgreSQL tables (or create fresh database)
2. CREATE tables from schema
3. SCAN entire vault for semantic blocks
4. FOR EACH note with semantic block:
     PARSE the semantic block
     FOR EACH item in block:
       INSERT into appropriate PostgreSQL table
       Preserve original UUIDs
5. REBUILD relationships table from item references
6. RECALCULATE coherence metrics
7. REGENERATE all dashboards
8. UPDATE sync-status to "normal"
```

Triggered via: **Settings → Recovery Tools → Rebuild Database**

### Partial Reconstruction
If only one table is corrupted:
```
1. IDENTIFY corrupted table (e.g., "axioms")
2. TRUNCATE that table only
3. SCAN vault for items of that type
4. REBUILD only that table
5. VERIFY referential integrity
6. LOG reconstruction event
```

---

## Practical Example: PostgreSQL Goes Down

**Minute 0**: You're working normally. PostgreSQL is connected. Everything syncs.

**Minute 5**: PostgreSQL server crashes (network issue, database restart, whatever).

**What happens immediately**:
- Next sync attempt fails
- Plugin logs: "PostgreSQL connection lost"
- Plugin switches to "local-only" mode
- Status bar turns yellow
- Notification: "PostgreSQL unavailable. Working locally."

**What continues working**:
- Writing and editing notes: ✓
- Semantic block updates: ✓
- Dashboard viewing: ✓ (from last generated state)
- AI analysis: ✓
- Right-click annotations: ✓
- Coherence calculation: ✓ (from in-memory data)

**What's degraded**:
- Advanced SQL queries: ✗ (unavailable)
- Dashboard regeneration: ✓ but won't update Postgres
- Changes queue up in sync-queue.json

**Minute 15**: PostgreSQL comes back online.

**What happens**:
- Plugin detects connection restored
- Plugin processes sync-queue.json
- All pending operations execute
- Status bar turns green
- Notification: "PostgreSQL reconnected. Sync complete."

**You never lost any work. You barely noticed the outage.**

---

## Practical Example: AI is Unavailable

**Scenario**: OpenAI and Claude are both rate-limited or down.

**What continues working**:
- Everything except AI-powered features: ✓
- Manual annotations: ✓
- Dashboard viewing: ✓
- PostgreSQL sync: ✓
- Coherence calculation: ✓

**What's degraded**:
- Auto-extraction: ✗
- Math translation: ✗
- Strategic suggestions: ✗
- AI observations/questions: ✗

**What the user sees**:
- Items marked as "needs-ai-review" in semantic blocks
- AI workspace shows "AI unavailable" in session log
- Settings show which providers are down

**When AI comes back**:
- User can click "Process Pending AI Tasks"
- Or enable "Auto-process when AI available"
- Queued items get processed

---

## Settings for Fault Tolerance

In **Tab 0: General Settings → Fault Tolerance**:

**Database Resilience**
- PostgreSQL Required: `[toggle: OFF by default]`
- Sync Retry Attempts: `[number: 3]`
- Sync Retry Interval: `[dropdown: 30s, 1min, 5min]`
- Auto-Rebuild on Corruption: `[toggle: ON]`

**Failure Notifications**
- Show notification on sync failure: `[toggle: ON]`
- Show notification on AI failure: `[toggle: ON]`
- Show notification on dashboard failure: `[toggle: ON]`
- Aggregate notifications (don't spam): `[toggle: ON]`

**Recovery Options**
- `[Button: Rebuild PostgreSQL from Vault]`
- `[Button: Regenerate All Dashboards]`
- `[Button: Clear Sync Queue]`
- `[Button: View Error Log]`

---

## Error Logging System

Every failure gets logged to a structured error log:

```
/plugin-data/
    error-log.json
```

Example entries:
```json
{
  "errors": [
    {
      "id": "err-001",
      "timestamp": "2025-01-15T14:22:10Z",
      "module": "postgresql-sync",
      "severity": "warning",
      "message": "Connection refused to PostgreSQL",
      "context": { "operation": "INSERT", "table": "axioms" },
      "resolved": false,
      "resolution": null
    },
    {
      "id": "err-002",
      "timestamp": "2025-01-15T14:23:00Z",
      "module": "ai-claude",
      "severity": "info",
      "message": "Rate limit reached, falling back to GPT",
      "context": { "task": "strategic-review" },
      "resolved": true,
      "resolution": "Fallback successful"
    }
  ]
}
```

---

## Status Bar Indicators

The plugin shows a small indicator in the status bar:
- **Green**: All systems normal
- **Yellow**: Some warnings (click to see)
- **Red**: Critical errors need attention

Click for details showing:
- PostgreSQL status
- AI provider status
- Sync queue depth
- Recent errors
- Quick actions

---

## Module Startup Independence

When the plugin starts, each module initializes independently:

```
PLUGIN STARTUP:
  
  1. CORE INIT (Required)
     - Load settings
     - Initialize file watchers
     - Build in-memory semantic index from vault
     
  2. POSTGRESQL INIT (Optional)
     TRY: Connect to PostgreSQL
     IF FAILS: 
       - Set mode = "local-only"
       - Log warning
       - CONTINUE startup
       
  3. AI INIT (Optional)
     TRY: Validate API keys
     IF FAILS:
       - Set ai_available = false
       - Log warning
       - CONTINUE startup
       
  4. MODULE INIT (Each independent)
     FOR EACH module in [research-hub, axioms, timeline, ...]:
       TRY: Initialize module
       IF FAILS:
         - Log error for that module
         - Disable that module's UI tab
         - CONTINUE to next module
         
  5. DASHBOARD INIT (Optional)
     TRY: Load existing dashboards
     IF FAILS:
       - Mark dashboards as "needs-regeneration"
       - CONTINUE
       
  RESULT: Plugin is running, possibly in degraded mode
```

**Degraded Mode UI**:
```
⚠️ Running in limited mode:
  - PostgreSQL: Unavailable (using local storage)
  - AI: Claude unavailable, using GPT only
  - Timeline Module: Initialization failed (click to retry)
  
[Retry All] [View Details] [Dismiss]
```

---

## Related Documents
- [[Architecture_Overview|System Architecture]]
- [[Implementation_Error_Handling|Error Handling Implementation]]
- [[User_Guide_Troubleshooting|Troubleshooting Guide]]
