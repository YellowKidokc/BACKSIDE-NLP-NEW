# Analysis Dashboard

This dashboard provides a live overview of all analysis scripts located in the `Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Analysis` directory. ::definition::D1::dashboard::purpose=overview::

```dataview
TABLE
    file.mtime as "Last Modified",
    file.size as "Size (bytes)"
FROM "00_VAULT_SYSTEM/Global_Analytics/Data_Analytics/Theophysics_Analytics/Scripts/Analysis"
WHERE contains(file.name, ".py")
SORT file.name ASC
```
