# Linking Dashboard

This dashboard provides a live overview of all linking scripts located in the `Analytics_Engine/Scripts/Linking` directory.

```dataview
TABLE
    file.mtime as "Last Modified",
    file.size as "Size (bytes)"
FROM "00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Linking"
WHERE contains(file.name, ".py")
SORT file.name ASC
```
