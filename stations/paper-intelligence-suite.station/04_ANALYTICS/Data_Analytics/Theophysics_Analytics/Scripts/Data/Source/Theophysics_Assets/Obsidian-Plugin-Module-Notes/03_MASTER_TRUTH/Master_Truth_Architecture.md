---
title: Master Truth Folder Architecture
version: 1.0
last_updated: 2025-01-15
status: active
tags: [#architecture, #master-truth, #dashboards]
---

# Master Truth Folder Architecture

**Purpose**: Central repository tracking all knowledge, metrics, and progression over time.

**Location**: `/master-truth/` at vault root

---

## Core Principle

The Master Truth folder is your **global snapshot** of everything the system knows. Each category within it has its own dedicated dashboard that tracks progression, accumulation, and historical trends.

---

## Folder Structure

```
/master-truth/
    master-sheet.md                    ← Unified overview (regenerated on each scan)
    master-sheet.json                  ← Machine-readable version for tooling
    
    /history/                          ← Timestamped snapshots of master sheet
        2025-01-14-14-00.md
        2025-01-15-10-00.md
        ...
    
    /concepts/                         ← Glossary progression
        glossary-dashboard.md
        glossary-history.json
        new-terms-log.md
        undefined-terms.md
    
    /math/                             ← Mathematical objects accumulation
        math-dashboard.md
        equations-registry.md
        variables-registry.md
        lowe-lagrangian-scores.md
        math-history.json
    
    /axioms/                           ← Axiom accumulation and health
        axioms-dashboard.md
        axiom-registry.md
        contradictions-log.md
        axiom-history.json
    
    /evidence/                         ← Evidence accumulation
        evidence-dashboard.md
        evidence-registry.md
        support-chains.md
        evidence-history.json
    
    /claims/                           ← Claims progression
        claims-dashboard.md
        claims-registry.md
        unsupported-claims.md
        claims-history.json
    
    /timeline/                         ← Chronological data
        timeline-dashboard.md
        events-registry.md
        chronological-conflicts.md
        timeline-history.json
    
    /theories/                         ← Theory integration
        theories-dashboard.md
        internal-theories.md
        external-theories.md
        cross-theory-conflicts.md
        theories-history.json
    
    /coherence/                        ← Coherence metrics over time
        coherence-dashboard.md
        score-progression.md
        violations-log.md
        strengths-log.md
        lowe-lagrangian-history.md
        coherence-history.json
    
    /breakthroughs/                    ← Breakthrough accumulation
        breakthroughs-dashboard.md
        breakthrough-registry.md
        breakthrough-timeline.md
        breakthroughs-history.json
    
    /external-links/                   ← SEP, Wikipedia, etc.
        links-dashboard.md
        links-registry.md
        auto-linked.md
        links-history.json
    
    /progression/                      ← Meta-analytics on research journey
        research-velocity.md
        concept-growth-rate.md
        coherence-trend.md
        weekly-summary.md
```

---

## Master Sheet

**File**: `master-sheet.md`

**Purpose**: Single auto-generated markdown file that serves as the global index of everything the system knows.

**Contents**:
1. **Concepts (Glossary)**: All terms with definitions, first-seen dates, source notes
2. **Mathematical Objects**: All equations with LaTeX, English summary, creator, UUID
3. **Axioms**: All axioms with theory assignment, coherence score, contradiction status
4. **Evidence**: All evidence with support chains and confidence ratings
5. **Claims**: All claims with verification status
6. **Theories Combined**: Internal and external theories with conflict counts
7. **Timeline Events**: All events with dates, sources, conflict flags
8. **External Links**: All SEP/Wikipedia links with relevance mapping
9. **Breakthroughs**: Chronological log of major insights
10. **NEW Items Section**: What's been added since last update

**Regeneration**: On every vault scan, with history preserved in `/history/`

---

## Sub-Dashboard Details

### /concepts/ — Glossary Progression

**glossary-dashboard.md** contains:
- Total concept count (current)
- New concepts added this week/month
- Concepts still needing definitions
- Most-referenced concepts
- Orphaned concepts (defined but never used)
- Trend chart: concept count over time

**glossary-history.json** stores:
```json
{
  "snapshots": [
    { "date": "2025-01-14", "totalConcepts": 142, "undefined": 8, "newThisWeek": 5 },
    { "date": "2025-01-15", "totalConcepts": 147, "undefined": 6, "newThisWeek": 7 }
  ]
}
```

**new-terms-log.md** is chronological:
```markdown
## New Terms Log

### 2025-01-15
- **Dual Entropy Gradient** — Added in Paper12.md
- **Chrono-Epistemic Derivative** — Added in Math Notes.md

### 2025-01-14
- **Causal Manifold** — Added in Ontology.md
```

**undefined-terms.md** lists terms used but not yet defined.

---

### /math/ — Mathematical Objects Accumulation

**math-dashboard.md** contains:
- Total equations count
- Total variables count
- Equations added this week
- Variables with missing concept links
- Mathematical contradictions detected
- Lowe Coherence Lagrangian current score

**equations-registry.md**:
```markdown
## Equations Registry

| UUID | Name | LaTeX | English Summary | Source | Date Added |
|------|------|-------|-----------------|--------|------------|
| eq001 | ΔE Transform | ΔE = Σ{∂𝒇(⊘⟶Ω)} | Energy change equals sum of partial derivatives | Paper12.md | 2025-01-10 |
| eq002 | Lowe Coherence Lagrangian | L_LC = χ(t)(d/dt(Σvars))² - S·χ(t) | Coherence propagation minus entropy | Core.md | 2025-01-08 |
```

**variables-registry.md**:
```markdown
## Variables Registry

| Variable | Concept | Definition Note | First Used |
|----------|---------|-----------------|------------|
| G | Grace | Definitions/Grace.md | 2024-12-01 |
| S | Sin/Entropy | Definitions/Entropy.md | 2024-12-01 |
| χ(t) | Coherence Potential | Definitions/Coherence.md | 2025-01-05 |
```

**lowe-lagrangian-scores.md**:
```markdown
## Lowe Coherence Lagrangian Scores

| Date | Global Score | Entropy Term | Propagation Term | Notes |
|------|--------------|--------------|------------------|-------|
| 2025-01-15 | 0.847 | 0.153 | 0.912 | Added Paper12 axioms |
| 2025-01-14 | 0.821 | 0.179 | 0.889 | Resolved timeline conflict |
```

---

### /coherence/ — Coherence Metrics Over Time

**coherence-dashboard.md** contains:
- Current global coherence score
- Per-theory coherence scores
- Violation count by type
- Strength count by type
- Week-over-week change
- Trend direction (improving/stable/degrading)

**score-progression.md**:
```markdown
## Coherence Score Progression

| Date | Global | Core Theory | Dual-Time | Violations | Notes |
|------|--------|-------------|-----------|------------|-------|
| 2025-01-15 | 0.847 | 0.891 | 0.842 | 3 | Added Paper12 |
| 2025-01-14 | 0.821 | 0.865 | 0.838 | 5 | Before resolution |
| 2025-01-13 | 0.798 | 0.842 | 0.831 | 7 | Timeline conflict |
```

**lowe-lagrangian-history.md**:
```markdown
## Lowe Coherence Lagrangian History

The Lagrangian: L_LC = χ(t)(d/dt(ΣVars))² - S·χ(t)

| Date | χ(t) | Propagation² | S·χ(t) | L_LC | Interpretation |
|------|------|--------------|--------|------|----------------|
| 2025-01-15 | 0.891 | 0.923 | 0.076 | 0.847 | Near equilibrium |
| 2025-01-14 | 0.865 | 0.898 | 0.077 | 0.821 | Entropy elevated |
```

---

### /progression/ — Meta-Analytics

**research-velocity.md**:
```markdown
## Research Velocity

| Week | New Concepts | New Axioms | New Evidence | Breakthroughs | Coherence Δ |
|------|--------------|------------|--------------|---------------|-------------|
| Jan 8-14 | 12 | 3 | 8 | 2 | +0.049 |
| Jan 1-7 | 8 | 2 | 5 | 1 | +0.023 |
```

**weekly-summary.md** (auto-generated narrative):
```markdown
## Weekly Summary: Jan 8-14, 2025

This week you added 12 new concepts and 3 axioms. The Lowe Coherence Lagrangian improved from 0.798 to 0.847, primarily due to resolving the timeline conflict between events ev003 and ev007.

Key breakthrough: Formalization of grace as negentropic correction (brk001).

Action items for next week:
- Define 6 terms still marked as undefined
- Address 2 remaining axiom contradictions
- Add evidence for 4 unsupported claims
```

---

## Integration with Plugin

The plugin generates and maintains this entire folder structure automatically:

**On Every Scan**:
- `master-sheet.md` is regenerated
- Timestamped copy goes to `/history/`

**On Every Change**:
- Relevant sub-dashboard is updated
- Add a new axiom? `/axioms/axiom-registry.md` and `/axioms/axioms-dashboard.md` update

**Daily/Weekly**:
- `/progression/` folder generates summary reports

**JSON Files**:
- Store raw data that markdown dashboards visualize
- These are what PostgreSQL mirrors for advanced analytics

---

## Why This Structure Matters

**For Researchers**:
- See exactly how your thinking has evolved
- Every axiom, term, breakthrough has a timestamp and trail

**For Collaboration**:
- Share `/master-truth/` folder and collaborators instantly understand your framework's current state and history

**For Export**:
- This folder is self-contained
- Zip it and the recipient has everything—no database needed

**For Debugging**:
- When coherence drops, trace back through history to find what changed

**For Motivation**:
- Watch your concept count grow, coherence score improve, breakthroughs accumulate

---

## Related Documents
- [[00_VAULT_SYSTEM/Config/12_Plugins/Theophysics_Obsidian_Plugin/00_OVERVIEW|Plugin Overview]]
- [[Tab_13_Master_Truth_Manager|Master Truth Manager Tab]]
- [[Implementation_Dashboards|Dashboard Generation Implementation]]
