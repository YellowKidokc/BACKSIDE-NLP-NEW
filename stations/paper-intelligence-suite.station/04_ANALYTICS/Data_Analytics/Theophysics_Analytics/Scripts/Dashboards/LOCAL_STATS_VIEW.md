---
stats_enabled: true
uuid: ff6974c5-eb82-5b71-93c4-ceb4e16a78b5
title: 📈 Local Statistics View
author: David Lowe
type: note
created: null
updated: '2025-11-22'
status: draft
file_path: _DELETE\_STATISTICS\local\LOCAL_STATS_VIEW.md
uuid_generated_at: '2025-11-22T01:23:14.505290'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

# 📈 Local Statistics View

This view shows statistics for individual papers.

```dataview
TABLE
file.mtime as "Last Modified"
FROM "06_Publication/Logos_Papers"
SORT file.mtime DESC
```
