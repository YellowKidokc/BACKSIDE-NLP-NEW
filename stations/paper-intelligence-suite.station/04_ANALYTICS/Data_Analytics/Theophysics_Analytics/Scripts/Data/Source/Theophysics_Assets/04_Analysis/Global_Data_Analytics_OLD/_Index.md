---
uid: GDA-index-001
type: index
created: 2025-11-29
purpose: Master index for Global Data Analytics system
---

# Global Data Analytics

> **The Engine Room** - Centralized analytics system for the entire Theophysics vault.

---

## System Architecture

```
Global_Data_Analytics/
├── Data_Analytics/           # Mechanisms + Output
│   ├── Mechanisms/           # Tools to gather & process data
│   │   ├── Atoms/            # Foundational concepts
│   │   ├── Molecules/        # Synthesized concepts
│   │   ├── Tags/             # Tag taxonomy
│   │   ├── MOCs/             # Navigation hubs
│   │   └── Hubs/             # Concept aggregators
│   │
│   └── Dashboards/           # Analytics output
│       ├── _Analytics_Config.md   # Toggle analytics on/off
│       └── [Dashboard files]      # Generated metrics
│
└── Global_Master_Sheet/      # Source of Truth
    ├── Definitions/          # All definitions (authoritative)
    ├── Links/                # Verified links
    ├── Tags/                 # Tag registry
    ├── Axioms/               # Core axioms
    └── Claims/               # Validated claims
```

---

## Quick Navigation

| Section | Purpose | Link |
|---------|---------|------|
| **Data Analytics** | Mechanisms & Dashboards | [[Global_Data_Analytics/Data_Analytics/_Index\|Data Analytics]] |
| **Global Master Sheet** | Source of Truth | [[Global_Data_Analytics/Global_Master_Sheet/_Index\|Master Sheet]] |
| **Analytics Config** | Toggle analytics on/off | [[Global_Data_Analytics/Data_Analytics/Dashboards/_Analytics_Config\|Config]] |

---

## How It Works

### 1. Data Flow

```
Papers (P01-P12)
      │
      ▼
┌─────────────────────┐
│   MECHANISMS        │  ← Extract & process
│   (Atoms, Tags,     │
│    MOCs, Hubs)      │
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│   DASHBOARDS        │  ← Analyze & visualize
│   (Metrics, Charts, │
│    Reports)         │
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│   MASTER SHEET      │  ← Store truth
│   (Definitions,     │
│    Links, Axioms)   │
└─────────────────────┘
```

### 2. Analytics Modes

| Mode | Scope | Use Case |
|------|-------|----------|
| **Single Paper** | One paper (e.g., P01) | Deep analysis of individual paper |
| **Multi-Paper** | Selected papers (e.g., P01-P05) | Compare/combine subset |
| **Global** | All 12 papers | Full system analysis |

### 3. Toggle System

Use `_Analytics_Config.md` to enable/disable analytics:

```yaml
analytics_enabled: true/false
scope: single/multi/global
target_papers: [P01, P02, ...]
output_to_master_sheet: true/false
```

---

## Integration Points

### Python Integration (Auto's App)
- **Read from:** `Global_Master_Sheet/Definitions/`
- **Write to:** `Global_Master_Sheet/Definitions/`
- **Sync with:** Tag registry, Links, Axioms

### Dataview Integration
- Dashboards use Dataview/DataviewJS queries
- Pull data from Mechanisms folders
- Output to Dashboard files

---

## Getting Started

1. **Configure Analytics** → [[_Analytics_Config]]
2. **Run Mechanisms** → Extract data from papers
3. **View Dashboards** → See aggregated metrics
4. **Check Master Sheet** → Verify source of truth
