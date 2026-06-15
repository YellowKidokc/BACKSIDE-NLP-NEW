---
stats_enabled: true
uuid: 1338863e-71a7-56d3-ad25-bf69478acf29
title: 🌎 Global Statistics View
author: David Lowe
type: note
created: null
updated: '2025-11-22'
status: draft
file_path: _DELETE\_STATISTICS\global\GLOBAL_STATS_VIEW.md
uuid_generated_at: '2025-11-22T01:23:14.493271'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

# 🌎 Global Statistics View

This view shows statistics across the entire project.

## Top 10 Most Recently Modified Files
```dataview
TABLE
file.mtime as "Last Modified"
WHERE file.name != "LOGOS_PROJECT_STATS.md"
SORT file.mtime DESC
LIMIT 10
```
