---
# CLAIM TEMPLATE
# ==============
# Claims are assertions that require evidence. 
# They are NOT axioms (assumed) or theorems (derived).
# They are empirical or interpretive assertions that can be supported or undermined.

uuid: {{UUID}}
type: claim
id: CL-{{NUMBER}}
status: draft | review | supported | contested | withdrawn

# Epistemic status
confidence: low | medium | high | very_high
evidence_strength: ⬛⬜⬜⬜⬜ | ⬛⬛⬜⬜⬜ | ⬛⬛⬛⬜⬜ | ⬛⬛⬛⬛⬜ | ⬛⬛⬛⬛⬛

# What this claim depends on
supported_by:
  axioms: []
  theorems: []
  evidence: []  # UUIDs of evidence items

# What depends on this claim
enables:
  claims: []
  predictions: []

# Paper linkage
papers: []
primary_role: implication

created: {{DATE}}
last_reviewed: {{DATE}}
---

# CL-{{NUMBER}}: {{CLAIM_TITLE}}

## Claim Statement

> **{{SINGLE_CLEAR_CLAIM_STATEMENT}}**

---

## Claim Type

- [ ] Empirical (testable against data)
- [ ] Interpretive (mapping between domains)
- [ ] Predictive (future-oriented)
- [ ] Historical (past events)

---

## Evidence Bundle

| Evidence ID | Source | Type | Strength | Supports/Undermines |
|-------------|--------|------|----------|---------------------|
| EV-{{X}} | | empirical / theoretical / testimonial | ⬛⬛⬛⬜⬜ | supports |
| | | | | |

### Total Evidence Assessment

- **Supporting evidence:** {{COUNT}}
- **Undermining evidence:** {{COUNT}}
- **Net strength:** {{ASSESSMENT}}

---

## Derivation Chain

How this claim follows from upstream elements:

```
A{{X}}.{{Y}} (axiom) 
    ↓
T{{Z}} (theorem)
    ↓
+ EV-{{W}} (evidence)
    ↓
∴ CL-{{NUMBER}} (this claim)
```

---

## Alternative Interpretations

Could the evidence support a different claim?

| Alternative Claim | Why Less Likely | Why Possible |
|-------------------|-----------------|--------------|
| | | |

---

## Falsification Criteria

This claim would be falsified if:

1. {{SPECIFIC_FALSIFICATION_CONDITION_1}}
2. {{SPECIFIC_FALSIFICATION_CONDITION_2}}

**Strongest potential falsifier:**

> {{WHAT_WOULD_MOST_DIRECTLY_REFUTE_THIS}}

---

## Does NOT Claim

> ⚠️ **Explicit exclusions:**

- This claim does NOT assert...
- This claim does NOT depend on believing...
- This claim is NOT equivalent to saying...

---

## Confidence Assessment

| Factor | Assessment |
|--------|------------|
| Evidence quality | low / medium / high |
| Derivation soundness | weak / moderate / strong |
| Alternative explanations | many / few / none viable |
| Expert consensus | against / divided / supportive / NA |

**Overall confidence:** {{LOW/MEDIUM/HIGH/VERY_HIGH}}

---

## If This Claim Is True

Consequences that follow:

1. 
2. 

---

## If This Claim Is False

What must be revised:

1. 
2. 

---

## Related Claims

| Related Claim | Relationship |
|---------------|--------------|
| CL-{{X}} | prerequisite / consequence / tension / independent |
| | |

---

%%semantic
{
  "uuid": "{{UUID}}",
  "type": "claim",
  "id": "CL-{{NUMBER}}",
  "confidence": "{{CONFIDENCE}}",
  "evidence_strength": "{{STRENGTH}}",
  "classifications": [
    {"content": "{{CLAIM_TITLE}}", "type": "claim"}
  ]
}
%%
