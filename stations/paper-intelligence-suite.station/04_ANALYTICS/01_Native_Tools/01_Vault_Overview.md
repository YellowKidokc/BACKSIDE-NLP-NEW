# Vault Overview
> [!INFO]
> Live view of your vault's health and recent activity. Powered by Dataview.

## 📊 Quick Stats
```dataview
TABLE length(rows) as "Count"
FROM ""
WHERE file.name != this.file.name
GROUP BY file.folder
SORT length(rows) DESC
LIMIT 10
```

## 🕒 Recently Modified
```dataview
TABLE file.mtime as "Last Modified", file.folder as "Location"
FROM ""
SORT file.mtime DESC
LIMIT 10
```

## 📂 Largest Files (Word Count)
```dataview
TABLE file.word-count as "Words"
FROM ""
WHERE file.word-count > 1000
SORT file.word-count DESC
LIMIT 10
```
