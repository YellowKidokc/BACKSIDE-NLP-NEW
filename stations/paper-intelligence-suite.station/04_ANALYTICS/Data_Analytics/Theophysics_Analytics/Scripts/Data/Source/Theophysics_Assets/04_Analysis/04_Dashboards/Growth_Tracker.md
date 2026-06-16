---
uid: DASH-growth-tracker-001
type: dashboard
created: 2025-11-29
purpose: Track content growth over time
---

# Growth Tracker Dashboard

> Monitor the evolution of your knowledge system.

---

## Content Created by Date

```dataview
TABLE WITHOUT ID
    dateformat(file.ctime, "yyyy-MM-dd") AS Date,
    length(rows) AS "Notes Created"
FROM "02_Foundations" OR "04_Integration" OR "05_Doctrine" OR "05_Hubs"
GROUP BY dateformat(file.ctime, "yyyy-MM-dd")
SORT Date DESC
LIMIT 30
```

---

## Component Growth

### Atoms Over Time
```dataview
TABLE WITHOUT ID
    dateformat(file.ctime, "yyyy-MM-dd") AS Date,
    file.link AS Atom
FROM "02_Foundations"
WHERE type = "atom"
SORT file.ctime ASC
```

### Laws Over Time
```dataview
TABLE WITHOUT ID
    dateformat(file.ctime, "yyyy-MM-dd") AS Date,
    file.link AS Law
FROM "05_Doctrine"
WHERE type = "law"
SORT file.ctime ASC
```

---

## Monthly Summary

```dataviewjs
const pages = dv.pages('"02_Foundations" OR "04_Integration" OR "05_Doctrine" OR "05_Hubs"');

let months = {};
for (let p of pages) {
    let month = p.file.ctime.toFormat("yyyy-MM");
    months[month] = (months[month] || 0) + 1;
}

let sorted = Object.entries(months).sort((a, b) => b[0].localeCompare(a[0]));
dv.table(["Month", "Notes Created"], sorted.slice(0, 12));
```

---

## Coherence Improvement

Track how coherence scores change over time:

```dataviewjs
const pages = dv.pages('"02_Foundations" OR "04_Integration" OR "05_Doctrine"')
    .where(p => p.coherence_score && p.file.ctime);

let data = pages.values.map(p => [
    p.file.link,
    p.file.ctime.toFormat("yyyy-MM-dd"),
    p.coherence_score
]).sort((a, b) => a[1].localeCompare(b[1]));

dv.table(["Note", "Created", "Coherence"], data);
```

---

## Velocity Metrics

```dataviewjs
const pages = dv.pages('"02_Foundations" OR "04_Integration" OR "05_Doctrine" OR "05_Hubs"');

const now = dv.date("today");
const weekAgo = now.minus({days: 7});
const monthAgo = now.minus({days: 30});

const thisWeek = pages.where(p => p.file.ctime >= weekAgo).length;
const thisMonth = pages.where(p => p.file.ctime >= monthAgo).length;

dv.table(["Period", "Notes Created"], [
    ["Last 7 days", thisWeek],
    ["Last 30 days", thisMonth],
    ["All time", pages.length]
]);
```

---

## Milestone Tracking

| Milestone | Target | Current | Status |
|-----------|--------|---------|--------|
| Core Atoms | 8 | 8 | ✓ Complete |
| First Molecule | 1 | 0 | Pending |
| 4 Molecules | 4 | 0 | Pending |
| 3 Laws | 3 | 1 | In Progress |
| 5 Hubs | 5 | 5 | ✓ Complete |
| 100 Notes | 100 | TBD | In Progress |

---

## Activity Heatmap (Last 30 Days)

```dataviewjs
const pages = dv.pages('"02_Foundations" OR "04_Integration" OR "05_Doctrine" OR "05_Hubs"');
const now = dv.date("today");

let days = [];
for (let i = 29; i >= 0; i--) {
    let date = now.minus({days: i});
    let dateStr = date.toFormat("yyyy-MM-dd");
    let count = pages.where(p => p.file.ctime.toFormat("yyyy-MM-dd") === dateStr).length;
    let bar = count > 0 ? "█".repeat(Math.min(count, 10)) : "·";
    days.push([dateStr, count, bar]);
}

dv.table(["Date", "Count", "Activity"], days.filter(d => d[1] > 0 || days.indexOf(d) % 7 === 0));
```
