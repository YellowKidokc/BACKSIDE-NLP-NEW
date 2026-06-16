# Theophysics Analysis System

A comprehensive analysis toolkit for the Theophysics vault, including AI-powered note analysis, coherence metrics, and automated linking.

## Quick Start

1. **Start the API server:**
   ```bash
   python 01_Scripts/api_server.py
   ```

2. **Enable the Obsidian plugin:**
   - Settings -> Community Plugins -> Enable "Theophysics AI Engine"
   - Set endpoint: `http://localhost:8001/analyze`

3. **Run full vault analysis:**
   ```bash
   python 01_Scripts/grace_vault_manager.py --cli --vault /path/to/vault --auto
   ```

## Folder Structure

```
04_Analysis/
├── 01_Scripts/           # Python scripts and automation
│   ├── analysis/         # Coherence and co-occurrence analyzers
│   ├── utilities/        # Vault refresh, linking, validation
│   └── docker/           # Docker configuration
│
├── 02_System/            # System documentation and prompts
│
├── 03_Templates/         # Obsidian note templates (6 phases)
│
├── 04_Dashboards/        # Dataview-powered dashboards
│
├── 05_Hubs/              # Auto-generated concept hubs
│
├── 06_Wizards/           # Templater wizards for vault management
│
├── 07_Data/              # Analysis output, databases, JSON
│   ├── profiles/         # Individual note profiles
│   ├── correlations/     # Correlation analysis
│   └── master_sheets/    # Glossaries and axiom sheets
│
└── _Archive/             # Superseded files
```

## Key Features

### Analysis Scripts
- **Coherence Analysis** - Cross-reference density, notation consistency
- **Co-occurrence Mapping** - Statistical concept co-mentions
- **Duplicate Detection** - Exact and near-duplicate finding
- **Auto-Linking** - Relationship inference from tags

### Validation Metrics
- **SIS** - Semantic Integrity Score
- **LCS** - Logical Consistency Score
- **SRI** - Scar Resolution Index

### Templates (6-Phase System)
1. Assets - Raw source intake
2. Foundations - Atomic concepts (Atoms)
3. Analysis - Exploration and experimentation
4. Integration - Synthesis (Molecules)
5. Doctrine - Laws and principles
6. Publication - Papers and articles

## Dependencies

- Python 3.8+
- Obsidian with Dataview plugin
- Optional: Templater, Buttons plugins

### Python packages:
```bash
pip install fastapi uvicorn requests matplotlib numpy
```

## API Providers

Set environment variables for live AI:
```bash
# OpenAI
export AI_PROVIDER=openai
export OPENAI_API_KEY=sk-...

# Anthropic
export AI_PROVIDER=anthropic
export ANTHROPIC_API_KEY=sk-ant-...
```

Default is `stub` mode (no API key needed).

---

**Version:** 2.0 (Reorganized November 2025)
**Author:** David Lowe + AI Collaborators
