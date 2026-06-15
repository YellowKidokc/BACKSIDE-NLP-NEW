# Research Analytics System - Option B: Python Scripts

## What Was Created

Complete Python engine for generating statistics across three scopes:

1. **Local Stats** - Individual paper analysis
2. **Comparison Stats** - Multi-paper comparisons
3. **Global Stats** - Vault-wide analytics

---

## File Structure

```
00_VAULT_SYSTEM/04_Analysis/01_Scripts/
├── generate_stats.py           # Local stats generator
├── generate_comparisons.py     # Comparison generator
├── generate_global.py          # Global vault stats
├── RUN_ALL_STATS.bat          # Run complete pipeline
└── STATS_README.md            # This file

Output (generated):
Stats/
├── Local/
│   ├── Paper-01.stats.json
│   ├── Paper-02.stats.json
│   └── ...
├── Comparisons/
│   ├── Paper-01-Paper-02.comparison.json
│   ├── Paper-01-Paper-02-Paper-03-plus9.comparison.json
│   └── ...
└── Global/
    ├── vault.stats.json
    ├── tag.stats.json
    ├── math.stats.json
    └── theology.stats.json
```

---

## Usage

### 1. Generate Local Stats

**Single paper:**
```bash
python generate_stats.py Paper-01-The-Logos-Principle-CANONICAL-CURSOR.md
```

**All papers:**
```bash
python generate_stats.py --all
```

**Output:** `Stats/Local/Paper-01.stats.json`

---

### 2. Generate Comparison Stats

**Compare 2 papers:**
```bash
python generate_comparisons.py Paper-01 Paper-02
```

**Compare multiple papers:**
```bash
python generate_comparisons.py Paper-01 Paper-02 Paper-03 Paper-04
```

**Output:** `Stats/Comparisons/Paper-01-Paper-02-Paper-03-plus1.comparison.json`

---

### 3. Generate Global Stats

```bash
python generate_global.py
```

**Output:**
- `Stats/Global/vault.stats.json` (master file)
- `Stats/Global/tag.stats.json` (tag analysis)
- `Stats/Global/math.stats.json` (math analysis)
- `Stats/Global/theology.stats.json` (theology analysis)

---

### 4. Run Complete Pipeline

```bash
RUN_ALL_STATS.bat
```

This runs all three in sequence:
1. Local stats for all papers
2. Comparison of all papers
3. Global vault stats

---

## What Each Script Generates

### Local Stats (per paper)

```json
{
  "metadata": {
    "filename": "Paper-01.md",
    "paper_id": "Paper-01",
    "file_size": 45231
  },
  "text": {
    "total_word_count": 5234,
    "unique_word_count": 1423,
    "reading_time_minutes": 26.17,
    "lexical_density_percent": 27.2
  },
  "links": {
    "internal_link_count": 45,
    "external_url_count": 12
  },
  "entities": {
    "tag_count": 8,
    "tags": ["logos", "trinity", "grace"],
    "uuid_count": 12
  },
  "images": {
    "embedded_image_count": 7,
    "unique_image_uuids": 7
  },
  "math": {
    "math_block_count": 15,
    "inline_math_count": 34,
    "total_math_elements": 49
  },
  "theology": {
    "trinity_father_count": 23,
    "trinity_son_count": 19,
    "trinity_spirit_count": 21,
    "trinity_symmetry_score": 0.923,
    "logos_mentions": 67
  },
  "logic": {
    "has_logic_layer": true,
    "branch_count": 4,
    "bridge_count": 6
  }
}
```

### Comparison Stats

```json
{
  "papers": ["Paper-01", "Paper-02"],
  "comparative_metrics": {
    "text_comparison": {
      "Paper-01": {"word_count": 5234},
      "Paper-02": {"word_count": 6123}
    },
    "math_comparison": {...},
    "theology_comparison": {...}
  },
  "similarity_matrix": {
    "papers": ["Paper-01", "Paper-02"],
    "matrix": [[1.0, 0.73], [0.73, 1.0]]
  },
  "rankings": {
    "by_word_count": [...],
    "by_math_density": [...],
    "by_trinity_symmetry": [...]
  }
}
```

### Global Stats

```json
{
  "metadata": {
    "total_papers": 12
  },
  "aggregates": {
    "total_word_count": 62810,
    "total_images": 84,
    "total_math_elements": 423
  },
  "distributions": {
    "word_count_distribution": {...},
    "math_distribution": {...}
  },
  "tag_analysis": {
    "unique_tags": 67,
    "most_common_tags": [...]
  },
  "math_analysis": {...},
  "theology_analysis": {...},
  "network_analysis": {...}
}
```

---

## Statistics Collected

### Text Metrics
- Word count (total, unique)
- Character count
- Sentence & paragraph count
- Reading time
- Lexical density
- Average sentence length

### Link Metrics
- Internal links (wikilinks)
- External URLs
- Block references
- Link density

### Entity Metrics
- Tags (from frontmatter + inline)
- UUIDs
- Concept mentions

### Image Metrics
- Embedded images
- Unique image UUIDs
- Markdown vs wikilink images

### Math Metrics
- Math blocks (`$$ ... $$`)
- Inline math (`$ ... $`)
- Unique symbols
- Greek letters

### Theology Metrics
- Trinity mentions (Father, Son, Spirit)
- Trinity symmetry score
- Logos mentions
- Grace mentions
- Sin/entropy mentions

### Logic Progression Metrics
- Branch count
- Bridge count
- Skeleton sections
- Condensed statements

### History Metrics
- Created timestamp
- Modified timestamp
- File size

---

## Integration with Obsidian Plugin

These JSON files are designed to be consumed by the Obsidian plugin (Option C).

The plugin will:
1. Watch the `Stats/` folder
2. When JSON changes, refresh dashboards
3. Render HighCharts visualizations
4. Display in Obsidian UI

---

## Next Steps

After running stats generation:

1. **Option C:** Create Obsidian plugin to visualize
2. **Option D:** Define JSON formats (already done above)
3. **Option E:** Create HighCharts templates

---

## Troubleshooting

**"No paper statistics found"**
- Run `generate_stats.py --all` first
- Check `Stats/Local/` folder exists

**"Stats not found for paper"**
- Generate local stats for that paper first
- Check paper ID matches filename

**"Need at least 2 papers to compare"**
- Provide at least 2 paper IDs to comparison script

---

## Requirements

```bash
pip install pyyaml
```

(numpy is optional for similarity calculations)

