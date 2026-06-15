---
publish: false
---
# META-SYNTHESIS CONSENSUS LAYER v1.0
## Supreme Court Style Multi-Model Alignment Report

---

## Purpose

This layer **never re-reads the paper**. It only reads the structured outputs from multiple AI models and produces:

1. **Alignment Summary** — Where models agree
2. **Variance Report** — Where models disagree
3. **Consensus Ruling** — Supreme Court style majority/dissent breakdown
4. **One-Page Executive Summary** — Human-readable synthesis

**This is the synthesis layer between claim-indexing and human review.**

---

## INPUTS

```
- Structured Output from Model A (Claim-Indexer JSON)
- Structured Output from Model B (Claim-Indexer JSON)
- Structured Output from Model C (Claim-Indexer JSON)

OR

- Sectional Coherence Scorecard from Model A
- Sectional Coherence Scorecard from Model B
- Sectional Coherence Scorecard from Model C
```

---

## ALIGNMENT RULES (EXPLICIT)

### Rating Alignment
- Scores within **±2 points** → **Aligned**
- Scores **>2 points apart** → **Flagged Variance**

### Claim Presence
- Same claim extracted by **all 3** → **Stable**
- Missing in **1 model** → **Weak Signal**
- Missing in **2 models** → **Unstable / Underspecified**

### Topology Agreement
- Same dependency edges → **Aligned**
- One disagreement → **Partial**
- Structural disagreement → **Dissent**

---

## PROMPT (COPY/PASTE)

```
ACT AS: Multi-Model Consensus Synthesizer.

YOU ARE NOT re-reading the original paper.
YOU ARE synthesizing THREE structured outputs from different AI models.

Your task is to:
1) Identify where all models align
2) Identify where models diverge
3) Produce a Supreme Court-style ruling (majority, concurrence, dissent)
4) Create a one-page human-readable summary

---

## INPUTS PROVIDED

MODEL_A_OUTPUT: [JSON or Scorecard]
MODEL_B_OUTPUT: [JSON or Scorecard]
MODEL_C_OUTPUT: [JSON or Scorecard]

---

## PHASE 1 — ALIGNMENT CALCULATION

For each claim or dimension:
- Calculate variance across models
- Mark as: Aligned (±2) | Partial (2-3) | Divergent (>3)
- Calculate overall alignment percentage

---

## PHASE 2 — CONSENSUS SUMMARY (ONE PAGE)

Produce a summary in this exact format:

### Document: [ID]
### Overall Alignment Score: [X%]
### Models Aligned: [Yes/No]
### Tolerance Threshold: ±2 points

**Claims/Dimensions Fully Aligned (All 3 Models):**
- [List with scores from each model]

**Claims/Dimensions Partially Aligned (2 of 3 Models):**
- [List with variance notes]

**Claims/Dimensions Not Aligned:**
- [List with specific disagreements]

---

## PHASE 3 — SUPREME COURT BREAKDOWN

### Majority Interpretation (3/3 or 2/3)
[What the models agree on regarding the paper's structure, claims, or section effectiveness]

### Concurring Variations
[Where models agree on outcome but differ on reasoning or classification]

### Dissents
[Where one model fundamentally disagrees with the others]

---

## PHASE 4 — VARIANCE HOTSPOTS

Produce a table showing exactly where human attention is needed:

| Item | Variance Type | Description | Human Action Required |
|------|--------------|-------------|----------------------|
| | | | |

---

## PHASE 5 — NUMERIC ALIGNMENT INDEX

Produce a compact JSON summary:

{
  "document_id": "",
  "alignment_index": 0.00,
  "claim_agreement": 0.00,
  "topology_agreement": 0.00,
  "scope_agreement": 0.00,
  "modal_agreement": 0.00,
  "clarity_std_dev": 0.00,
  "models_used": ["A", "B", "C"],
  "consensus_status": "Aligned | Partial | Divergent"
}

---

## OUTPUT CONSTRAINTS

- Do NOT re-evaluate the paper
- Do NOT introduce new claims or judgments
- Do NOT favor any single model
- Present disagreements neutrally
- Make variance actionable for human review
```

---

## OUTPUT FORMAT: One-Page Executive Summary

```markdown
# CONSENSUS REPORT — [Document ID]

## Alignment Status: [ALIGNED / PARTIAL / DIVERGENT]
## Overall Agreement: [X%]
## Models: A (OpenAI) | B (Anthropic) | C (Grok/Other)

---

### AGREED (All Models)
- Point 1
- Point 2
- Point 3

### PARTIAL AGREEMENT (2/3 Models)
- Point with variance note

### DISSENT (Structural Disagreement)
- Point with explanation

---

### VARIANCE HOTSPOTS (Human Review Required)
| Item | Issue | Recommendation |
|------|-------|----------------|
| | | |

---

### NUMERIC SUMMARY
- Alignment Index: X.XX
- Claim Agreement: X%
- Topology Agreement: X%
- Confidence: High/Medium/Low

---

**Ruling:** [One-sentence synthesis of what the models collectively determined]

**Next Action:** [What human reviewer should do]
```

---

## WHY THIS ARCHITECTURE WORKS

1. **Layer Separation is Strict**
   - Models do extraction (Claim-Indexer)
   - Models do section evaluation (Sectional Coherence)
   - Meta layer does synthesis (this prompt)
   - Humans read one page

2. **Disagreements are Explicit**
   - No hidden averaging
   - No model dominance
   - Variance becomes signal, not noise

3. **Scales Across Thousands of Papers**
   - Same format every time
   - Comparable across corpus
   - Automatable later

---

## CHECKSUM / AUDIT PROTOCOL

For each run, record:

```
Prompt Hash: SHA-256 of prompt text
Model A Output Hash: SHA-256 of JSON
Model B Output Hash: SHA-256 of JSON
Model C Output Hash: SHA-256 of JSON
Consensus Output Hash: SHA-256 of final synthesis
Date: YYYY-MM-DD
```

This creates a tamper-evident audit trail without hiding anything.

---

## AUDIT BLOCK

```
Prompt Version: Meta-Synthesis Consensus v1.0
Date Created: 2026-01-14
Purpose: Multi-model alignment and Supreme Court-style consensus
Constraint: Never re-reads paper, only synthesizes structured outputs
```

---

*This is how serious consensus reports work: alignment, variance, ruling, next action.*
