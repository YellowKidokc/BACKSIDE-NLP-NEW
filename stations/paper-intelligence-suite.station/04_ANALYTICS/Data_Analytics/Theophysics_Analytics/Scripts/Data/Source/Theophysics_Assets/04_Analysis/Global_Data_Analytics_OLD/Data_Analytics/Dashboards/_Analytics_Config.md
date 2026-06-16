---
uid: CONFIG-analytics-001
type: config
created: 2025-11-29
purpose: Toggle analytics on/off and configure scope
---

# Analytics Configuration

> **Control Panel** - Enable/disable analytics and set scope.

---

## Current Settings

```yaml
# ═══════════════════════════════════════════════════════════
# ANALYTICS TOGGLE
# ═══════════════════════════════════════════════════════════

analytics_enabled: true

# ═══════════════════════════════════════════════════════════
# SCOPE SETTINGS
# ═══════════════════════════════════════════════════════════

# Options: single | multi | global
scope: global

# For single/multi mode, specify papers
target_papers:
  - P01
  - P02
  - P03
  - P04
  - P05
  - P06
  - P07
  - P08
  - P09
  - P10
  - P11
  - P12

# ═══════════════════════════════════════════════════════════
# OUTPUT SETTINGS
# ═══════════════════════════════════════════════════════════

# Write results to Global Master Sheet?
output_to_master_sheet: true

# Generate dashboard reports?
generate_dashboards: true

# ═══════════════════════════════════════════════════════════
# FEATURE TOGGLES
# ═══════════════════════════════════════════════════════════

features:
  definitions_extraction: true
  links_extraction: true
  tags_analysis: true
  coherence_scoring: true
  breakthrough_tracking: true
  axiom_extraction: true
  claims_tracking: true

# ═══════════════════════════════════════════════════════════
# PYTHON INTEGRATION
# ═══════════════════════════════════════════════════════════

python_integration:
  enabled: true
  auto_sync: false
  definitions_manager_path: "THEOPHYSICS_MASTER/Apps/Obsidian-Definitions-Manager/"
```

---

## How to Use

### Enable/Disable All Analytics
```yaml
analytics_enabled: true   # Run analytics
analytics_enabled: false  # Skip analytics
```

### Set Scope

**Single Paper:**
```yaml
scope: single
target_papers:
  - P01
```

**Multiple Papers:**
```yaml
scope: multi
target_papers:
  - P01
  - P02
  - P05
```

**Global (All Papers):**
```yaml
scope: global
```

### Toggle Features

Enable only what you need:
```yaml
features:
  definitions_extraction: true   # Extract definitions
  links_extraction: false        # Skip links
  tags_analysis: true            # Analyze tags
  coherence_scoring: false       # Skip coherence
```

---

## Python Script Integration

When Python scripts read this config:

```python
import yaml

def load_analytics_config():
    with open('_Analytics_Config.md', 'r') as f:
        content = f.read()
        # Extract YAML from markdown
        yaml_block = content.split('```yaml')[1].split('```')[0]
        return yaml.safe_load(yaml_block)

config = load_analytics_config()
if config['analytics_enabled']:
    if config['scope'] == 'global':
        # Run global analytics
        pass
    elif config['scope'] == 'single':
        # Run single paper analytics
        paper = config['target_papers'][0]
        pass
```

---

## Dataview Integration

Check if analytics are enabled:

```dataviewjs
const config = dv.page("Global_Data_Analytics/Data_Analytics/Dashboards/_Analytics_Config");
if (config) {
    dv.paragraph("Analytics: " + (config.analytics_enabled ? "✓ Enabled" : "✗ Disabled"));
    dv.paragraph("Scope: " + config.scope);
}
```

---

## Run Analytics

### Via Python
```bash
python run_analytics.py --config "_Analytics_Config.md"
```

### Via Dataview
Dashboards automatically read this config and adjust queries.

### Manual
1. Set `analytics_enabled: true`
2. Set desired `scope`
3. Enable needed `features`
4. Open dashboards to see results
