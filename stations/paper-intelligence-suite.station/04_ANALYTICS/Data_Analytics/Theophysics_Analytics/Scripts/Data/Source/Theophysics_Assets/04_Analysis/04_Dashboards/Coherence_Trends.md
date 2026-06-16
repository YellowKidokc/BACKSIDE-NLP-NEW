---
uid: DASH-coherence-trends-001
type: dashboard
created: 2025-11-29
purpose: Track coherence quality evolution
---

# Coherence Trends Dashboard

> Monitor the quality and consistency of your knowledge system.

---

## Overall Coherence Status

```dataviewjs
const pages = dv.pages('"02_Foundations" OR "04_Integration" OR "05_Doctrine"')
    .where(p => p.coherence_score);

if (pages.length > 0) {
    const scores = pages.values.map(p => p.coherence_score);
    const avg = scores.reduce((a, b) => a + b, 0) / scores.length;

    let status = "⚠ Needs Work";
    if (avg >= 0.9) status = "✓ Excellent";
    else if (avg >= 0.8) status = "✓ Good";
    else if (avg >= 0.7) status = "○ Acceptable";

    dv.paragraph(`## System Coherence: ${avg.toFixed(3)} ${status}`);
}
```

---

## Coherence Distribution

```dataviewjs
const pages = dv.pages('"02_Foundations" OR "04_Integration" OR "05_Doctrine"')
    .where(p => p.coherence_score);

if (pages.length > 0) {
    const scores = pages.values.map(p => p.coherence_score);

    const excellent = scores.filter(s => s >= 0.9).length;
    const good = scores.filter(s => s >= 0.8 && s < 0.9).length;
    const acceptable = scores.filter(s => s >= 0.7 && s < 0.8).length;
    const needsWork = scores.filter(s => s < 0.7).length;

    dv.table(["Range", "Count", "Bar", "Percentage"], [
        ["Excellent (≥0.9)", excellent, "🟢".repeat(excellent), (excellent/scores.length*100).toFixed(0) + "%"],
        ["Good (0.8-0.9)", good, "🟡".repeat(good), (good/scores.length*100).toFixed(0) + "%"],
        ["Acceptable (0.7-0.8)", acceptable, "🟠".repeat(acceptable), (acceptable/scores.length*100).toFixed(0) + "%"],
        ["Needs Work (<0.7)", needsWork, "🔴".repeat(needsWork), (needsWork/scores.length*100).toFixed(0) + "%"]
    ]);
}
```

---

## Coherence by Component Type

```dataviewjs
const atoms = dv.pages('"02_Foundations"').where(p => p.coherence_score);
const molecules = dv.pages('"04_Integration"').where(p => p.coherence_score);
const laws = dv.pages('"05_Doctrine"').where(p => p.coherence_score);

function avg(arr) {
    if (arr.length === 0) return "N/A";
    return (arr.values.map(p => p.coherence_score).reduce((a,b) => a+b, 0) / arr.length).toFixed(3);
}

dv.table(["Component", "Count", "Avg Coherence"], [
    ["Atoms", atoms.length, avg(atoms)],
    ["Molecules", molecules.length, avg(molecules)],
    ["Laws", laws.length, avg(laws)]
]);
```

---

## Individual Coherence Scores

### Highest Coherence
```dataview
TABLE coherence_score AS Coherence, type AS Type
FROM "02_Foundations" OR "04_Integration" OR "05_Doctrine"
WHERE coherence_score
SORT coherence_score DESC
LIMIT 10
```

### Needs Improvement
```dataview
TABLE coherence_score AS Coherence, type AS Type
FROM "02_Foundations" OR "04_Integration" OR "05_Doctrine"
WHERE coherence_score AND coherence_score < 0.8
SORT coherence_score ASC
LIMIT 10
```

---

## Trinity Coherence Analysis

```dataviewjs
const pages = dv.pages('"02_Foundations"').where(p => p.divine_field);

let imbalanced = [];
for (let p of pages) {
    if (p.divine_field) {
        let f = p.divine_field.Father || 0;
        let s = p.divine_field.Son || 0;
        let sp = p.divine_field.Spirit || 0;

        let max = Math.max(f, s, sp);
        let min = Math.min(f, s, sp);

        if (max - min > 0.5) {
            imbalanced.push([
                p.file.link,
                f.toFixed(2),
                s.toFixed(2),
                sp.toFixed(2),
                (max - min).toFixed(2)
            ]);
        }
    }
}

if (imbalanced.length > 0) {
    dv.paragraph("### Imbalanced Trinity Aspects");
    dv.paragraph("Notes where one aspect dominates (spread > 0.5):");
    dv.table(["Note", "Father", "Son", "Spirit", "Spread"], imbalanced);
} else {
    dv.paragraph("### ✓ Trinity aspects are well-balanced across all notes.");
}
```

---

## Coherence Improvement Actions

### Priority 1: Low Coherence Notes
```dataview
LIST
FROM "02_Foundations" OR "04_Integration" OR "05_Doctrine"
WHERE coherence_score AND coherence_score < 0.7
SORT coherence_score ASC
```

### Priority 2: Missing Coherence Scores
```dataview
LIST
FROM "02_Foundations" OR "04_Integration" OR "05_Doctrine"
WHERE !coherence_score
```

---

## Coherence Metrics Definitions

| Metric | Range | Meaning |
|--------|-------|---------|
| **Coherence Score** | 0-1 | Overall internal consistency |
| **Trinity Balance** | -1 to 1 | Aspect alignment |
| **SIS** | 0-1 | Semantic Integrity Score |
| **LCS** | 0-1 | Logical Consistency Score |
| **SRI** | 0-1 | Scar Resolution Index |

---

## Run Coherence Analysis

To recalculate coherence scores, run:
```bash
python 01_Scripts/analysis/analyze_coherence.py
```

This will update:
- Individual note coherence scores
- Cross-reference density
- Notation consistency
- Overall system coherence
