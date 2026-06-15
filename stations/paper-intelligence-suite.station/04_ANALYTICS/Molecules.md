# 🧬 Molecule Index
```dataview
TABLE file.link AS Molecule, phase, internal_consistency, predictive_power, coherence_score
FROM "04_Integration"
WHERE type = "molecule" OR contains(file.name, "MOL_")
SORT coherence_score DESC
```
