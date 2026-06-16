---
uid: TAG-information-index
type: tag-category
category: information
created: 2025-11-29
---

# Information Tags

> Tags for information theory, computation, and complexity concepts.

---

## Core Information Concepts

| Tag | Related Atom | Description |
|-----|--------------|-------------|
| `information` | [[Information (I)]] | Pattern distinction |
| `entropy` | [[00_VAULT_SYSTEM/Global_Analytics/ARCHIVE/Gemini_delete/Flat/Entropy (S)]] | Information uncertainty |
| `coherence` | [[Coherence (C)]] | Information integration |

---

## Information Theory

- `information` - General information concept
- `information-theory` - Shannon's framework
- `shannon-entropy` - H = -Σ p log p
- `kolmogorov-complexity` - Algorithmic complexity
- `mutual-information` - Shared information
- `information-conservation` - Information preservation

---

## Quantum Information

- `qubits` - Quantum bits
- `quantum-information` - QM information theory
- `entanglement` - Non-local correlations
- `quantum-error-correction` - Protecting quantum states

---

## Computation & Complexity

- `computation` - Information processing
- `algorithm` - Computational procedure
- `complexity` - Computational difficulty
- `emergence` - Higher-order patterns
- `self-organization` - Spontaneous order

---

## Notes Using Information Tags

```dataview
TABLE file.tags AS Tags, coherence_score AS Coherence
FROM "02_Foundations" OR "04_Integration" OR "05_Doctrine"
WHERE any(file.tags, (t) => contains(t, "information") OR contains(t, "entropy") OR contains(t, "complexity"))
SORT coherence_score DESC
```

---

## Information Flow in Theophysics

```
SOURCE (Father)          CHANNEL (Son)           RECEIVER (Spirit)
────────────────────────────────────────────────────────────────
Information (I)    →     Form (F)          →     Dynamics (D)
Pattern            →     Structure         →     Relationship
Potential          →     Actual            →     Process
```
