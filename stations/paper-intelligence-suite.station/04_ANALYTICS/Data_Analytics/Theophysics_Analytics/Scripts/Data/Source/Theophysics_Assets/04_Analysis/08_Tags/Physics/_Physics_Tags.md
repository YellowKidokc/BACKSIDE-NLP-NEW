---
uid: TAG-physics-index
type: tag-category
category: physics
created: 2025-11-29
---

# Physics Tags

> Tags for physics concepts used in Theophysics research.

---

## Core Physics Concepts

| Tag | Related Atom | Description |
|-----|--------------|-------------|
| [[01_CANONICAL/Glossary/Entropy]] | [[00_SYSTEM/Global_Analytics/ARCHIVE/Gemini_delete/Flat/Entropy (S)]] | Thermodynamic decay, disorder |
| [[99_TAG_NOTES/negentropy]] | [[Grace (G)]] | Negative entropy, ordering |
| [[information]] | [[Information (I)]] | Shannon/quantum information |
| [[01_CANONICAL/Glossary/Coherence]] | [[Coherence (C)]] | Quantum/classical coherence |

---

## Quantum Mechanics

```dataview
LIST
FROM #quantum-mechanics OR #wavefunction OR #superposition OR #entanglement
SORT file.name ASC
```

### Tags in this category:
- `quantum-mechanics` - General QM concepts
- `wavefunction` - Psi function, probability amplitude
- `wavefunction-collapse` - Measurement-induced collapse
- `superposition` - Multiple simultaneous states
- `entanglement` - Non-local correlations
- `decoherence` - Environment-induced classicality
- `measurement` - Quantum measurement problem
- `observer-effect` - Observation influencing outcome
- `uncertainty-principle` - Heisenberg's principle
- `complementarity` - Bohr's complementarity
- `wave-particle-duality` - Dual nature of quanta

---

## Relativity & Spacetime

- `general-relativity` - Einstein's gravity theory
- `special-relativity` - Lorentz invariance
- `spacetime` - 4D manifold
- `curvature` - Riemann geometry
- `geodesics` - Free-fall paths
- `singularity` - Infinite curvature points
- `black-holes` - Event horizons
- `hawking-radiation` - Black hole evaporation

---

## Thermodynamics

- `entropy` - Disorder measure (S)
- `negentropy` - Order measure (-S)
- `thermodynamics` - Heat/energy laws
- `second-law` - Entropy increase
- `conservation-laws` - Conserved quantities

---

## Cosmology

- `cosmology` - Universe structure
- `big-bang` - Origin event
- `inflation` - Exponential expansion
- `dark-matter` - Unseen mass
- `dark-energy` - Cosmic acceleration
- `fine-tuning` - Anthropic constants

---

## Notes Using Physics Tags

```dataview
TABLE file.tags AS Tags, coherence_score AS Coherence
FROM "02_Foundations" OR "04_Integration" OR "05_Doctrine"
WHERE any(file.tags, (t) => contains(t, "physics") OR contains(t, "quantum") OR contains(t, "entropy"))
SORT coherence_score DESC
```
