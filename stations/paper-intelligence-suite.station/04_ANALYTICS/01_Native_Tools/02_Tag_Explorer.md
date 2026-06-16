# Tag Explorer
> [!TIP]
> Visualize how your tags are being used.

## 🏷️ Most Used Tags
```dataview
TABLE length(rows) as "Count"
FROM ""
FLATTEN file.tags as tag
GROUP BY tag
SORT length(rows) DESC
LIMIT 20
```

## 🔗 Tag Connections
*Files that share tags often suggest a connection.*

```dataview
TABLE file.tags as "Tags"
FROM ""
WHERE length(file.tags) > 0
SORT file.mtime DESC
LIMIT 20
```
