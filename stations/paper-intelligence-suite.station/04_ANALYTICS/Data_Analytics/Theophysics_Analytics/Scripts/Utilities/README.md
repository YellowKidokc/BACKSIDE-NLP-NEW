---
uuid: cab71062-e98c-58c0-83b3-19502ad48e57
title: Word Ontology Validation Scripts
author: David Lowe
type: documentation
created: '2025-11-22'
updated: '2025-11-22'
status: draft
file_path: _DELETE\Word-ontology\Scripts\README.md
uuid_generated_at: '2025-11-22T01:23:47.818751'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

# Word Ontology Validation Scripts

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

This will install:
- `sentence-transformers` (for semantic embeddings)
- `numpy` (for vector math)

2. **First run** will download the embedding model (~80MB)

---

## Usage

### Validate a New Term

```bash
python validate_term.py \
  --definition "Your term definition here" \
  --sources "source_word1,source_word2,source_word3"
```

### Example: Validating "Decoherence"

```bash
python validate_term.py \
  --definition "The universal process of information loss and order degradation" \
  --sources "entropy,disorder,sin,moral failing"
```

**Output:**
```
========================================================================
THEOPHYSICS TERM VALIDATION REPORT
========================================================================

Similarity Score:  0.8512 (85.1%)
Status:            ✅ APPROVED
Zone:              Valid Birth Zone (70-90%)

Inheritance:       0.85 (preserved meaning from source)
Novelty:           0.15 (new meaning introduced)

========================================================================
RECOMMENDATIONS:
========================================================================
1. Excellent balance of inheritance and novelty
2. This term successfully bridges concepts

✅ VALIDATION PASSED - Term ready for ontology
```

---

## Interpreting Results

### Similarity Scores

- **< 0.70 (< 70%)**: ❌ REJECTED - Too disconnected from source
- **0.70-0.90 (70-90%)**: ✅ APPROVED - Valid conceptual birth
- **> 0.90 (> 90%)**: ❌ REJECTED - Too redundant with source

### Inheritance vs. Novelty

- **Inheritance**: How much meaning is preserved from source words
- **Novelty**: How much new meaning is introduced

**Ideal balance:** ~0.70-0.85 inheritance, 0.15-0.30 novelty

---

## Workflow

### Creating a New Term

1. **Identify source concepts:**
   ```
   Old term: "Sin"
   Source words: sin, moral failing, spiritual death, separation from God
   ```

2. **Write definition:**
   ```
   "An act of conscious choice that opposes the ordering principle of the Logos,
   thereby increasing the net Decoherence (S) of the system."
   ```

3. **Run validator:**
   ```bash
   python validate_term.py \
     --definition "An act of conscious choice that opposes the ordering principle..." \
     --sources "sin,moral failing,spiritual death,separation from God"
   ```

4. **Check results:**
   - If APPROVED → proceed to create term file
   - If REJECTED → revise definition and retry

5. **Document in term file:**
   - Copy similarity score to YAML frontmatter
   - Include validation results in "Semantic Validation" section

---

## Future Scripts

### Planned additions:
- `scan_papers.py` - Find old terminology across all papers
- `consistency_check.py` - Verify term usage matches definitions
- `ontology_map.py` - Generate visual concept map
- `usage_tracker.py` - Track term frequency across papers

---

## Troubleshooting

### "Model not found" error
The first run downloads the model. Ensure internet connection and ~500MB free space.

### "ImportError: sentence_transformers"
Run: `pip install -r requirements.txt`

### Slow validation
First validation is slow (model loading). Subsequent validations are fast (~1 second).

---

## Model Details

**Model:** all-MiniLM-L6-v2  
**Size:** ~80MB  
**Speed:** ~1000 sentences/second  
**Quality:** 384-dimensional embeddings

This model balances speed and accuracy for semantic similarity tasks.

---

**Questions?** See `QUICK-START.md` in parent directory.
