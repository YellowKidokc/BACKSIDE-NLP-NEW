# Paper Management Dashboard

This dashboard provides a live overview of all paper management scripts located in the `Analytics_Engine/Scripts/Paper_Management` directory.

```dataview
TABLE
    file.mtime as "Last Modified",
    file.size as "Size (bytes)"
FROM "00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Paper_Management"
WHERE contains(file.name, ".py")
SORT file.name ASC
```
