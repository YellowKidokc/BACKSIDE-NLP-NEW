---
uid: DASH-graph-analytics-001
type: dashboard
created: 2025-11-29
purpose: Link structure and graph analysis
---

# Graph Analytics Dashboard

> Understand the connection structure of your knowledge system.

---

## Link Density

```dataviewjs
const pages = dv.pages('"02_Foundations" OR "04_Integration" OR "05_Doctrine" OR "05_Hubs"');

let data = [];
for (let p of pages) {
    data.push([
        p.file.link,
        p.file.outlinks.length,
        p.file.inlinks.length,
        p.file.outlinks.length + p.file.inlinks.length
    ]);
}

data.sort((a, b) => b[3] - a[3]);

dv.table(["Note", "Outlinks", "Inlinks", "Total"], data.slice(0, 15));
```

---

## Hub Identification

Notes with the most inbound links (knowledge hubs):

```dataviewjs
const pages = dv.pages('"02_Foundations" OR "04_Integration" OR "05_Doctrine" OR "05_Hubs"');

let hubs = [];
for (let p of pages) {
    if (p.file.inlinks.length >= 2) {
        hubs.push([p.file.link, p.file.inlinks.length]);
    }
}

hubs.sort((a, b) => b[1] - a[1]);
dv.table(["Hub Note", "Inbound Links"], hubs.slice(0, 10));
```

---

## Orphan Notes

Notes with no links (need integration):

```dataview
LIST
FROM "02_Foundations" OR "04_Integration" OR "05_Doctrine" OR "05_Hubs"
WHERE length(file.inlinks) = 0 AND length(file.outlinks) = 0
```

---

## Weakly Connected

Notes with only 1 connection:

```dataview
TABLE file.inlinks.length + file.outlinks.length AS "Total Links"
FROM "02_Foundations" OR "04_Integration" OR "05_Doctrine" OR "05_Hubs"
WHERE (file.inlinks.length + file.outlinks.length) = 1
```

---

## Cross-Folder Links

### Atoms linking to Hubs
```dataview
LIST file.outlinks
FROM "02_Foundations"
WHERE any(file.outlinks, (l) => contains(meta(l).path, "05_Hubs"))
```

### Hubs linking to Atoms
```dataview
LIST file.outlinks
FROM "05_Hubs"
WHERE any(file.outlinks, (l) => contains(meta(l).path, "02_Foundations"))
```

---

## Link Statistics Summary

```dataviewjs
const pages = dv.pages('"02_Foundations" OR "04_Integration" OR "05_Doctrine" OR "05_Hubs"');

let totalOut = 0;
let totalIn = 0;
let maxOut = 0;
let maxIn = 0;

for (let p of pages) {
    totalOut += p.file.outlinks.length;
    totalIn += p.file.inlinks.length;
    maxOut = Math.max(maxOut, p.file.outlinks.length);
    maxIn = Math.max(maxIn, p.file.inlinks.length);
}

dv.table(["Metric", "Value"], [
    ["Total Notes", pages.length],
    ["Total Outlinks", totalOut],
    ["Total Inlinks", totalIn],
    ["Avg Outlinks/Note", (totalOut / pages.length).toFixed(1)],
    ["Max Outlinks", maxOut],
    ["Max Inlinks", maxIn],
    ["Link Density", ((totalOut + totalIn) / (pages.length * pages.length) * 100).toFixed(2) + "%"]
]);
```

---

## Recommended Links

Notes that probably should link to each other based on shared tags:

```dataviewjs
const pages = dv.pages('"02_Foundations"').where(p => p.file.tags);
let suggestions = [];

for (let i = 0; i < pages.length; i++) {
    for (let j = i + 1; j < pages.length; j++) {
        let p1 = pages[i];
        let p2 = pages[j];

        // Check if they share tags but don't link
        let tags1 = new Set(p1.file.tags);
        let tags2 = new Set(p2.file.tags);
        let shared = [...tags1].filter(t => tags2.has(t));

        let linked = p1.file.outlinks.some(l => l.path === p2.file.path) ||
                    p2.file.outlinks.some(l => l.path === p1.file.path);

        if (shared.length > 0 && !linked) {
            suggestions.push([p1.file.link, p2.file.link, shared.join(", ")]);
        }
    }
}

if (suggestions.length > 0) {
    dv.table(["Note 1", "Note 2", "Shared Tags"], suggestions.slice(0, 10));
} else {
    dv.paragraph("No obvious missing links detected.");
}
```
