# 📜 Law Index
```dataview
TABLE file.link AS Law, validation_status, coherence_score, trinity_coherence_index, status
FROM "05_Doctrine"
WHERE type = "law" OR contains(file.name, "LAW_")
SORT coherence_score DESC
```
