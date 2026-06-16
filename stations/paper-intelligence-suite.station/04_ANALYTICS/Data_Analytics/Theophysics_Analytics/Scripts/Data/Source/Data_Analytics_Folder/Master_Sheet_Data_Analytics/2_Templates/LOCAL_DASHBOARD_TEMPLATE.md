---
cssclass: dashboard-local
tags:
- meta
- system
- local-stats
zone: '{{ZONE_NAME}}'
uuid: e5c95215-197a-5dc7-b7d6-ca1c7ce4a1b6
title: '📁 LOCAL DASHBOARD: {{ZONE_NAME}}'
author: David Lowe
type: template
created: null
updated: '2025-11-22'
status: draft
file_path: 00_VAULT_SYSTEM\LOCAL_DASHBOARD_TEMPLATE.md
uuid_generated_at: '2025-11-22T01:23:04.191275'
uuid_version: '1.0'
pillars: []
category: theophysics-general
---

# 📁 LOCAL DASHBOARD: {{ZONE_NAME}}

*Folder-aware analytics for spatially bounded content*  
*Last Updated: `= date(now)`*

---

## 📊 ZONE STATISTICS

### Content Overview
```dataview
TABLE WITHOUT ID
    "Total Files" as "Metric",
    length(rows) as "Count"
FROM "{{FOLDER_PATH}}"
WHERE scan_zone = "{{ZONE_NAME}}"
FLATTEN "summary" as row

UNION

TABLE WITHOUT ID
    "Total Words" as "Metric",
    sum(rows.word_count) as "Count"
FROM "{{FOLDER_PATH}}"
WHERE scan_zone = "{{ZONE_NAME}}"
FLATTEN "summary" as row

UNION

TABLE WITHOUT ID
    "Avg Words/File" as "Metric",
    round(sum(rows.word_count) / length(rows), 0) as "Count"
FROM "{{FOLDER_PATH}}"
WHERE scan_zone = "{{ZONE_NAME}}"
FLATTEN "summary" as row
```

### Files in This Zone
```dataview
TABLE WITHOUT ID
    file.link as "File",
    content_type as "Type",
    word_count as "Words",
    length(file.outlinks) as "Links Out",
    length(file.inlinks) as "Backlinks",
    file.mtime as "Modified"
FROM "{{FOLDER_PATH}}"
WHERE scan_zone = "{{ZONE_NAME}}"
SORT file.mtime DESC
```

---

## 🔗 CONNECTIVITY ANALYSIS

### Most Connected Files (Within Zone)
```dataview
TABLE WITHOUT ID
    file.link as "File",
    length(file.outlinks) as "→ Outbound",
    length(file.inlinks) as "← Inbound",
    (length(file.outlinks) + length(file.inlinks)) as "Total"
FROM "{{FOLDER_PATH}}"
WHERE scan_zone = "{{ZONE_NAME}}"
SORT (length(file.outlinks) + length(file.inlinks)) DESC
LIMIT 10
```

### Cross-Zone References (Linking Outside)
```dataview
TABLE WITHOUT ID
    file.link as "File",
    length(file.outlinks) as "External Links",
    file.outlinks[0] as "Example Link"
FROM "{{FOLDER_PATH}}"
WHERE scan_zone = "{{ZONE_NAME}}" AND length(file.outlinks) > 0
SORT length(file.outlinks) DESC
LIMIT 10
```

### Backlinks FROM Other Zones
```dataview
TABLE WITHOUT ID
    file.link as "File",
    length(file.inlinks) as "External References",
    file.inlinks[0] as "Example Backlink"
FROM "{{FOLDER_PATH}}"
WHERE scan_zone = "{{ZONE_NAME}}" AND length(file.inlinks) > 0
SORT length(file.inlinks) DESC
LIMIT 10
```

---

## 🧠 CONCEPT DISTRIBUTION

### Top Concepts (Zone-Local)
```dataviewjs
// Query concepts specific to this zone
const zoneName = "{{ZONE_NAME}}";
const concepts = await dv.query(`
    SELECT concept, mentions 
    FROM concepts 
    WHERE zones LIKE '%${zoneName}%'
    ORDER BY mentions DESC 
    LIMIT 15
`);

if (concepts && concepts.values) {
    dv.table(
        ["Concept", "Mentions in Zone"],
        concepts.values.map(c => [c[0], c[1]])
    );
} else {
    dv.paragraph("*Run vault_refresh_v2.py to populate concept data*");
}
```

### Unique Concepts (Zone-Exclusive)
```dataviewjs
// Concepts that ONLY appear in this zone
const zoneName = "{{ZONE_NAME}}";
const unique = await dv.query(`
    SELECT concept, mentions 
    FROM concepts 
    WHERE zones = '${zoneName}'
    ORDER BY mentions DESC 
    LIMIT 10
`);

if (unique && unique.values) {
    dv.table(
        ["Concept", "Mentions"],
        unique.values.map(c => [c[0], c[1]])
    );
} else {
    dv.paragraph("*No zone-exclusive concepts detected*");
}
```

---

## 📈 TEMPORAL PATTERNS

### Recent Activity (Last 14 Days)
```dataview
TABLE WITHOUT ID
    file.link as "File",
    word_count as "Words",
    file.mtime as "Modified"
FROM "{{FOLDER_PATH}}"
WHERE scan_zone = "{{ZONE_NAME}}" AND file.mtime >= date(now) - dur(14 days)
SORT file.mtime DESC
```

### Creation Timeline
```dataview
TABLE WITHOUT ID
    dateformat(file.ctime, "yyyy-MM") as "Month",
    length(rows) as "Files Created"
FROM "{{FOLDER_PATH}}"
WHERE scan_zone = "{{ZONE_NAME}}"
GROUP BY dateformat(file.ctime, "yyyy-MM")
SORT dateformat(file.ctime, "yyyy-MM") DESC
LIMIT 12
```

---

## 🎯 QUALITY METRICS

### Completion Status
```dataview
TABLE WITHOUT ID
    "Complete (>500 words)" as "Status",
    length(rows) as "Count",
    round(100 * length(rows) / {{TOTAL_FILES}}, 1) + "%" as "Percentage"
FROM "{{FOLDER_PATH}}"
WHERE scan_zone = "{{ZONE_NAME}}" AND word_count >= 500
FLATTEN "complete" as row

UNION

TABLE WITHOUT ID
    "In Progress (200-500)" as "Status",
    length(rows) as "Count",
    round(100 * length(rows) / {{TOTAL_FILES}}, 1) + "%" as "Percentage"
FROM "{{FOLDER_PATH}}"
WHERE scan_zone = "{{ZONE_NAME}}" AND word_count >= 200 AND word_count < 500
FLATTEN "progress" as row

UNION

TABLE WITHOUT ID
    "Stub (<200 words)" as "Status",
    length(rows) as "Count",
    round(100 * length(rows) / {{TOTAL_FILES}}, 1) + "%" as "Percentage"
FROM "{{FOLDER_PATH}}"
WHERE scan_zone = "{{ZONE_NAME}}" AND word_count < 200
FLATTEN "stub" as row
```

### Isolated Files (No Connections)
```dataview
TABLE WITHOUT ID
    file.link as "File",
    word_count as "Words",
    "⚠️ No links" as "Status"
FROM "{{FOLDER_PATH}}"
WHERE scan_zone = "{{ZONE_NAME}}" 
  AND length(file.inlinks) = 0 
  AND length(file.outlinks) = 0
SORT file.name
```

---

## 🔍 SUGGESTED ACTIONS

```dataview
LIST
- "Review isolated files and add relevant links"
- "Expand stub files (<200 words)"
- "Cross-reference with other zones"
- "Update concept tags for better discoverability"
WHERE file.name = "FAKE"
```

---

## 📖 NAVIGATION

- [[GLOBAL_VAULT_STATS]] - Return to global view
- [[BREAKTHROUGH_MAP]] - Conceptual breakthrough tracking
- [[🚀 START_HERE]] - Vault guide

---

*This LOCAL dashboard tracks content within the {{ZONE_NAME}} zone. For cross-zone analysis, see GLOBAL_VAULT_STATS.*

---

## 📝 USAGE INSTRUCTIONS

**To create a zone-specific dashboard:**

1. Copy this template to the target folder (e.g., `03_PUBLICATIONS/LOGOS_DASHBOARD.md`)
2. Replace `{{ZONE_NAME}}` with the zone name (e.g., "Logos Papers")
3. Replace `{{FOLDER_PATH}}` with the folder path (e.g., "03_PUBLICATIONS/Logos_Papers")
4. Replace `{{TOTAL_FILES}}` with the total file count (or use a DataView calculation)
5. Save and open in Obsidian

**Example for Logos Papers:**
```markdown
---
zone: "Logos Papers"
---

# 📁 LOCAL DASHBOARD: Logos Papers

### Files in This Zone
```dataview
FROM "03_PUBLICATIONS/Logos_Papers"
WHERE scan_zone = "Logos Papers"
...
```
