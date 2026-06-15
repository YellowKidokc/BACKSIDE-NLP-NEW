---
uid: DASH-vault-stats-001
type: dashboard
created: 2025-11-29
purpose: Overall vault health and statistics
---

# Vault Statistics Dashboard

> Real-time overview of your Theophysics knowledge system.

---

## Component Summary

```dataviewjs
const atoms = dv.pages('"02_Foundations"').where(p => p.type == "atom").length;
const molecules = dv.pages('"04_Integration"').where(p => p.type == "molecule").length;
const laws = dv.pages('"05_Doctrine"').where(p => p.type == "law").length;
const hubs = dv.pages('"05_Hubs"').where(p => p.type == "hub").length;
const dashboards = dv.pages('"04_Dashboards"').length;
const templates = dv.pages('"03_Templates"').length;

dv.table(["Component", "Count", "Target", "Status"], [
    ["Atoms", atoms, "8+", atoms >= 8 ? "✓" : "⚠"],
    ["Molecules", molecules, "4+", molecules >= 4 ? "✓" : "○"],
    ["Laws", laws, "3+", laws >= 3 ? "✓" : "○"],
    ["Hubs", hubs, "5+", hubs >= 5 ? "✓" : "⚠"],
    ["Dashboards", dashboards, "--", "✓"],
    ["Templates", templates, "8", templates >= 8 ? "✓" : "⚠"]
]);
```

---

## Coherence Overview

```dataviewjs
const pages = dv.pages('"02_Foundations" OR "04_Integration" OR "05_Doctrine"')
    .where(p => p.coherence_score);

if (pages.length > 0) {
    const scores = pages.values.map(p => p.coherence_score);
    const avg = scores.reduce((a, b) => a + b, 0) / scores.length;
    const max = Math.max(...scores);
    const min = Math.min(...scores);

    // Distribution
    const high = scores.filter(s => s >= 0.9).length;
    const medium = scores.filter(s => s >= 0.7 && s < 0.9).length;
    const low = scores.filter(s => s < 0.7).length;

    dv.table(["Metric", "Value"], [
        ["Average Coherence", avg.toFixed(3)],
        ["Highest", max.toFixed(3)],
        ["Lowest", min.toFixed(3)],
        ["High (≥0.9)", high],
        ["Medium (0.7-0.9)", medium],
        ["Low (<0.7)", low]
    ]);
} else {
    dv.paragraph("No coherence scores found.");
}
```

---

## Trinity Balance

```dataviewjs
const pages = dv.pages('"02_Foundations"').where(p => p.divine_field);

if (pages.length > 0) {
    let fatherSum = 0, sonSum = 0, spiritSum = 0;
    let count = 0;

    for (let p of pages) {
        if (p.divine_field) {
            fatherSum += p.divine_field.Father || 0;
            sonSum += p.divine_field.Son || 0;
            spiritSum += p.divine_field.Spirit || 0;
            count++;
        }
    }

    dv.table(["Aspect", "Average Score", "Bar"], [
        ["Father", (fatherSum/count).toFixed(2), "█".repeat(Math.round(fatherSum/count * 10))],
        ["Son", (sonSum/count).toFixed(2), "█".repeat(Math.round(sonSum/count * 10))],
        ["Spirit", (spiritSum/count).toFixed(2), "█".repeat(Math.round(Math.abs(spiritSum/count) * 10))]
    ]);
}
```

---

## Content by Phase

```dataview
TABLE WITHOUT ID
    phase AS Phase,
    length(rows) AS "Note Count"
FROM "02_Foundations" OR "04_Integration" OR "05_Doctrine" OR "05_Hubs"
WHERE phase
GROUP BY phase
SORT phase ASC
```

---

## Recent Activity

### Recently Modified
```dataview
TABLE file.mtime AS "Modified"
FROM "02_Foundations" OR "04_Integration" OR "05_Doctrine" OR "05_Hubs"
SORT file.mtime DESC
LIMIT 10
```

### Recently Created
```dataview
TABLE file.ctime AS "Created"
FROM "02_Foundations" OR "04_Integration" OR "05_Doctrine" OR "05_Hubs"
SORT file.ctime DESC
LIMIT 10
```

---

## Link Health

```dataviewjs
const pages = dv.pages('"02_Foundations" OR "04_Integration" OR "05_Doctrine" OR "05_Hubs"');

let totalLinks = 0;
let orphans = [];

for (let p of pages) {
    totalLinks += p.file.outlinks.length;
    if (p.file.inlinks.length === 0 && p.file.outlinks.length === 0) {
        orphans.push(p.file.name);
    }
}

dv.paragraph(`**Total Outlinks:** ${totalLinks}`);
dv.paragraph(`**Average Links per Note:** ${(totalLinks / pages.length).toFixed(1)}`);
dv.paragraph(`**Orphan Notes:** ${orphans.length}`);

if (orphans.length > 0) {
    dv.paragraph("Orphans: " + orphans.slice(0, 5).join(", ") + (orphans.length > 5 ? "..." : ""));
}
```

---

## System Health Checklist

- [x] Core atoms created (8/8)
- [ ] First molecules synthesized (0/4)
- [ ] Core laws formalized (1/3)
- [x] Concept hubs established (5/5)
- [x] Tag system in place
- [x] MOC navigation ready
- [x] Analytics dashboards active
