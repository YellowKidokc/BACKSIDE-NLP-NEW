---
uid: MOC-atoms-001
type: moc
created: 2025-11-29
purpose: Navigation hub for all atomic concepts
---

# Atoms MOC

> **Foundational Concepts** - The irreducible building blocks of Theophysics.

---

## What is an Atom?

An **Atom** is a single, irreducible concept that:
- Contains ONE core idea (no mixing)
- Is context-free (understandable alone)
- Serves as a building block for Molecules
- Maps to a specific Trinity aspect

---

## Current Atoms

### By Trinity Aspect

#### Father Aspect (Source/Information)
```dataview
TABLE coherence_score AS Coherence, file.tags AS Tags
FROM "02_Foundations"
WHERE trinity_aspect = "Father" OR contains(divine_field.Father, 0.7)
SORT coherence_score DESC
```

#### Son Aspect (Form/Manifestation)
```dataview
TABLE coherence_score AS Coherence, file.tags AS Tags
FROM "02_Foundations"
WHERE trinity_aspect = "Son" OR contains(divine_field.Son, 0.7)
SORT coherence_score DESC
```

#### Spirit Aspect (Dynamics/Relationship)
```dataview
TABLE coherence_score AS Coherence, file.tags AS Tags
FROM "02_Foundations"
WHERE trinity_aspect = "Spirit" OR contains(divine_field.Spirit, 0.7)
SORT coherence_score DESC
```

---

## All Atoms Table

```dataview
TABLE
  coherence_score AS Coherence,
  trinity_aspect AS Trinity,
  translation_up AS "Translates Up",
  translation_down AS "Translates Down"
FROM "02_Foundations"
WHERE type = "atom"
SORT coherence_score DESC
```

---

## Atom Relationship Map

```
                    LOGOS (L)
                   /    |    \
                  /     |     \
         INFORMATION   FORM   DYNAMICS
              (I)      (F)      (D)
               |        |        |
            Father    Son     Spirit
               \       |       /
                \      |      /
                 COHERENCE (C)
                      |
              ┌───────┴───────┐
              |               |
           GRACE (G)     ENTROPY (S)
              |               |
              └───────┬───────┘
                      |
               RESURRECTION (R)
```

---

## Creating New Atoms

Use template: `[[03_Templates/02_Foundation_Template]]`

### Checklist
- [ ] Single concept only
- [ ] Clear definition
- [ ] Trinity aspect identified
- [ ] Physics bridge defined
- [ ] Theology bridge defined
- [ ] Mathematical expression (if applicable)
- [ ] Related atoms linked

---

## Atom Statistics

```dataviewjs
const atoms = dv.pages('"02_Foundations"').where(p => p.type == "atom");
const avgCoherence = atoms.values.reduce((sum, p) => sum + (p.coherence_score || 0), 0) / atoms.length;

dv.paragraph(`**Total Atoms:** ${atoms.length}`);
dv.paragraph(`**Average Coherence:** ${avgCoherence.toFixed(2)}`);
```
