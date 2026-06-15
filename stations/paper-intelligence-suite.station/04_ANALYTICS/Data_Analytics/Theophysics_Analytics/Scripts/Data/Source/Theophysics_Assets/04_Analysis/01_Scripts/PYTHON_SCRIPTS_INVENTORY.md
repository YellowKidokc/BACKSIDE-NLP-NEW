# Python Scripts Inventory

## Current Locations

### Vault System Scripts (Organized)
**Location:** `00_VAULT_SYSTEM\04_Analysis\01_Scripts\`

#### Analysis Scripts
- `analysis/analyze_coherence.py` - Coherence analysis
- `analysis/cooccurrence_analyzer.py` - Co-occurrence analysis
- `analysis/extract_metrics.py` - Metrics extraction
- `analysis/matter_analysis.py` - Matter analysis

#### Chart Scripts
- `charts/chart_templates.py` - Highcharts template generator

#### Utilities
- `utilities/auto_linker.py` - Auto-linking functionality
- `utilities/concept_hub_generator.py` - Concept hub generation
- `utilities/duplicate_finder.py` - Duplicate detection
- `utilities/uid_generator.py` - UID generation
- `utilities/validation_scaffold.py` - Validation scaffolding
- `utilities/vault_refresh.py` - Vault refresh

#### Core Scripts
- `api_server.py` - API server
- `grace_vault_manager.py` - Grace vault manager
- `run_theophysics.py` - Main runner script

### Legacy Scripts (To Be Organized)
**Location:** `00_VAULT_SYSTEM\10_Scripts\`

Many scripts in root and `Python/` subfolder. These should be reviewed and either:
1. Moved to appropriate vault system location
2. Archived if obsolete
3. Integrated if still needed

### Paper Chart Scripts
**Location:** `03_PUBLICATIONS\COMPLETE_LOGOS_PAPERS_FINAL\P##-*/charts/`

Each paper has chart generation scripts:
- `P##_chart_##_*.py` - Highcharts generation scripts
- These generate HTML that needs to be rendered to images

### App Scripts
**Location:** `Apps\Obsidian-Definitions-Manager\`

Standalone application scripts (keep separate).

## Action Items

1. **Review `10_Scripts/`** - Determine which scripts are still needed
2. **Move relevant scripts** to `04_Analysis\01_Scripts\` structure
3. **Archive obsolete scripts** to `00_VAULT_SYSTEM\10_Scripts\Archive\`
4. **Document dependencies** for each script category
5. **Create unified runner** that can execute scripts by category

## Notes
- Scripts should be organized by function, not scattered
- Each script should have clear purpose and dependencies
- Chart scripts need rendering pipeline (HTML → PNG/SVG)

