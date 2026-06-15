# 🧱 Atom Index
```dataview
TABLE file.link AS Atom, series, phase, coherence_score, trinity_coherence_index, length(file.content) AS chars
FROM "02_Foundations"
SORT coherence_score DESC
```
