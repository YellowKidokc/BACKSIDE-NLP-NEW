# System Dashboard

This dashboard provides a live overview of all system scripts located in the `Analytics_Engine/Scripts/System` directory.

```dataview
TABLE
    file.mtime as "Last Modified",
    file.size as "Size (bytes)"
FROM "00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/System"
WHERE contains(file.name, ".py")
SORT file.name ASC
```
