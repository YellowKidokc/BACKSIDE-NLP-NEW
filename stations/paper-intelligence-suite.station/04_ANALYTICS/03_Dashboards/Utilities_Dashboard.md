# Utilities Dashboard

This dashboard provides a live overview of all utility scripts located in the `Analytics_Engine/Scripts/Utilities` directory.

```dataview
TABLE
    file.mtime as "Last Modified",
    file.size as "Size (bytes)"
FROM "00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Utilities"
WHERE contains(file.name, ".py")
SORT file.name ASC
```
