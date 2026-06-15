---
title: Dashboard Generation Specification
version: 1.0
last_updated: 2025-01-15
status: active
tags: [#implementation, #dashboards, #generation]
---

# Dashboard Generation Specification v1.0

**Purpose**: Dashboards are auto-generated markdown files that visualize and summarize the semantic data stored across all notes in the vault. They provide human-readable views into the state of the research framework, its coherence, its components, and its evolution over time.

---

## Core Principles

### 1. Dashboards are Output, Not Input
Users never edit dashboards directly. All changes flow from the semantic blocks in individual notes. If a user wants to change something they see in a dashboard, they edit the source note, and the dashboard regenerates.

### 2. Dashboards are Portable
They are plain markdown files with embedded tables, lists, and optionally JSON data blocks. They render properly in any markdown viewer, not just Obsidian.

### 3. Dashboards are Scoped
Every dashboard can be generated at four different scopes:
- **Note level**: Single file
- **Paper level**: Single folder
- **Multi-paper level**: Selected folders
- **Global level**: Entire vault

The scope is indicated in the dashboard filename and header.

### 4. Dashboards are Timestamped
Every dashboard includes a generation timestamp and optionally a history of previous states for trend analysis.

---

## Folder Structure

All dashboards live in the `/master-truth/` folder at the root of the vault:

```
/master-truth/
    master-sheet.md
    master-sheet.json
    
    /history/
        2025-01-15-14-22-10.md
        2025-01-14-10-00-00.md
        
    /concepts/
        glossary-dashboard.md
        glossary-data.json
        new-terms-log.md
        undefined-terms.md
        
    /axioms/
        axioms-dashboard.md
        axioms-data.json
        axiom-registry.md
        contradictions-log.md
        
    /evidence/
        evidence-dashboard.md
        evidence-data.json
        evidence-registry.md
        support-chains.md
        
    /claims/
        claims-dashboard.md
        claims-data.json
        claims-registry.md
        unsupported-claims.md
        
    /timeline/
        timeline-dashboard.md
        timeline-data.json
        events-registry.md
        chronological-conflicts.md
        
    /ontology/
        ontology-dashboard.md
        ontology-data.json
        concepts-graph.md
        relationships.md
        
    /math/
        math-dashboard.md
        math-data.json
        equations-registry.md
        variables-registry.md
        lowe-lagrangian.md
        
    /theories/
        theories-dashboard.md
        theories-data.json
        internal-theories.md
        external-theories.md
        cross-theory-conflicts.md
        
    /coherence/
        coherence-dashboard.md
        coherence-data.json
        score-progression.md
        violations-log.md
        strengths-log.md
        lowe-lagrangian-history.md
        
    /breakthroughs/
        breakthroughs-dashboard.md
        breakthroughs-data.json
        breakthrough-registry.md
        breakthrough-timeline.md
        
    /external-links/
        links-dashboard.md
        links-data.json
        links-registry.md
        
    /tags/
        tags-dashboard.md
        tags-data.json
        tag-clusters.md
        
    /progression/
        research-velocity.md
        concept-growth.md
        coherence-trend.md
        weekly-summary.md
```

Each subfolder contains:
- Primary dashboard file (`*-dashboard.md`)
- Data file (`*-data.json`)
- Supporting detail files

---

## Dashboard File Format

Every dashboard follows a consistent format:

### 1. Header Block

```markdown
# Axioms Dashboard

**Scope:** Global  
**Generated:** 2025-01-15 14:22:10 UTC  
**Source Notes:** 47  
**Plugin Version:** 1.0.0

---
```

### 2. Coherence Pulse Section

Every dashboard includes the Coherence Pulse as its first content section:

```markdown
## Coherence Pulse

| Metric | Value | Trend |
|--------|-------|-------|
| Global Coherence | 0.847 | ↑ +0.026 |
| Propagation Term | 0.923 | ↑ +0.014 |
| Entropy Term | 0.153 | ↓ -0.012 |

**Status:** Healthy — propagation exceeds entropy  
**Action:** Resolve axiom conflict ax001/ax017 to improve coherence by ~0.03

---
```

### 3. Summary Statistics Section

```markdown
## Summary

| Statistic | Count |
|-----------|-------|
| Total Axioms | 47 |
| Well-Supported | 41 |
| Contradictions | 2 |
| Needs Evidence | 4 |
| Added This Week | 3 |

---
```

### 4. Main Content Section

The main content varies by dashboard type. It may include tables, lists, or prose depending on what is being displayed.

### 5. Data Block

At the bottom of each dashboard, a hidden JSON block contains the raw data:

```markdown
%%dashboard-data
{
  "generatedAt": "2025-01-15T14:22:10Z",
  "scope": "global",
  "metrics": {...},
  "items": [...],
  "version": "1.0"
}
%%
```

---

## The Master Sheet

**File**: `/master-truth/master-sheet.md`

The master sheet is the unified overview of everything in the vault. It aggregates data from all other dashboards into one comprehensive document.

### Sections

1. **Header and Coherence Pulse**
2. **Framework Overview** - High-level summary
3. **Concepts Summary** - Glossary health
4. **Axioms Summary** - Foundation status
5. **Evidence Summary** - Support coverage
6. **Claims Summary** - Verification status
7. **Timeline Summary** - Chronological data
8. **Math Summary** - Mathematical framework
9. **Theories Summary** - Internal and external theories
10. **Coherence Summary** - Lowe Lagrangian analysis
11. **Breakthroughs Summary** - Major insights
12. **New Items Section** - Recent additions

### Example Framework Overview

```markdown
## Framework Overview

The Theophysics framework currently contains 47 axioms, 89 claims, 62 evidence items, 
142 defined concepts, 23 mathematical equations, and 34 timeline events spanning from 
4004 BC to 2025 AD. The framework integrates 3 internal theories and references 12 
external theories including General Relativity, Quantum Mechanics, and entries from 
the Stanford Encyclopedia of Philosophy.

Current global coherence score is 0.847, indicating a healthy and well-integrated 
framework with minor issues requiring attention.
```

---

## Individual Dashboard Specifications

### Concepts Dashboard

**File**: `/master-truth/concepts/glossary-dashboard.md`

**Purpose**: Displays all defined concepts, their definitions, and glossary health metrics.

**Data Sources**: All annotations with `kind` = "definition" or "term"

**Sections**:
- Summary (total concepts, defined vs undefined, new additions, completeness %)
- Glossary table (alphabetical list with definitions, domains, sources, status)
- Undefined terms section (terms used but lacking definitions)
- New terms log (chronological additions)

**Example Glossary Table**:

```markdown
## Glossary

| Term | Definition | Domain | Source | Status |
|------|------------|--------|--------|--------|
| Causal Manifold | A mathematical structure representing... | ontology | Definitions.md | ✓ Defined |
| Coherence Potential | The active coherence state χ(t)... | coherence | Core.md | ✓ Defined |
| Dual Entropy | ... | physics | Paper12.md | ⚠ Needs Review |
| Epistemic Time | Not yet defined | methodology | — | ✗ Undefined |
```

**Generation Logic**:
1. Query all semantic blocks for annotations where `kind` = "definition" or "term"
2. Group definitions by their `term` field
3. Identify canonical definition for each term
4. Flag terms that appear but have no definition
5. Calculate usage counts by scanning all text
6. Sort alphabetically and render to markdown

**PostgreSQL Query**:
```sql
SELECT 
    a.uuid,
    a.text,
    a.properties->>'term' as term,
    a.properties->>'domain' as domain,
    a.properties->>'isCanonical' as is_canonical,
    a.properties->>'needsDefinition' as needs_definition,
    n.file_path as source,
    a.created_at
FROM annotations a
JOIN notes n ON a.note_uuid = n.uuid
WHERE a.kind IN ('definition', 'term')
ORDER BY COALESCE(a.properties->>'term', a.text) ASC;
```

---

### Axioms Dashboard

**File**: `/master-truth/axioms/axioms-dashboard.md`

**Purpose**: Displays all axioms, their supporting evidence, contradictions, and coherence scores.

**Data Sources**: All annotations with `kind` = "axiom" and their relationships

**Sections**:
- Summary (total, well-supported, contradictions, avg coherence, new this week)
- Axiom registry table
- Contradictions section (detailed analysis of each conflict)
- Unsupported axioms section

**Example Axiom Registry**:

```markdown
## Axiom Registry

| ID | Axiom | Theory | Coherence | Evidence | Status |
|----|-------|--------|-----------|----------|--------|
| ax001 | Causality must be directional in physical systems | Core | 0.94 | 3 | ⚠ Conflict |
| ax002 | Information propagation is monotonic | Core | 0.91 | 2 | ✓ Healthy |
| ax003 | Grace acts as negentropic correction | Core | 0.89 | 4 | ✓ Healthy |
| ax017 | Influence propagates bidirectionally in epistemic space | Dual-Time | 0.72 | 1 | ⚠ Conflict |
```

**Example Contradiction Analysis**:

```markdown
## Active Contradictions

### ax001 ↔ ax017

**Axiom 1:** Causality must be directional in physical systems  
**Axiom 17:** Influence propagates bidirectionally in epistemic space

**Analysis:** These axioms may not be in direct contradiction if ax001 is scoped 
specifically to physical causality while ax017 applies to epistemic influence. 
Consider clarifying the scope of ax001.

**Suggested Resolution:** Add scope qualifier to ax001: "Causality must be 
directional in physical systems, while epistemic influence may be bidirectional."

**Impact on Coherence:** Resolving this conflict would improve global coherence 
by approximately 0.03.
```

---

### Evidence Dashboard

**File**: `/master-truth/evidence/evidence-dashboard.md`

**Purpose**: Displays all evidence, what it supports, its strength, and coverage metrics.

**Sections**:
- Summary (total, strength distribution, coverage percentages)
- Evidence registry table
- Support chains (what supports what)
- Coverage analysis

**Example Support Chain**:

```markdown
## Support Chains

### Axiom: ax001 — Causality must be directional

Supported by:
- ev001: Thermodynamic arrow of time (Strong, Empirical)
- ev002: Biblical chronology pattern (Moderate, Textual)
- ev007: Causation literature review (Moderate, Textual)

**Support Assessment:** Well-supported with 3 evidence items including 1 strong empirical source.
```

---

### Claims Dashboard

**File**: `/master-truth/claims/claims-dashboard.md`

**Purpose**: Displays all claims, their verification status, and relationships.

**Sections**:
- Summary (total, verified/unverified, conflicting)
- Claims registry table
- Unsupported claims list (prioritized)
- Claims promoted to axioms log

---

### Timeline Dashboard

**File**: `/master-truth/timeline/timeline-dashboard.md`

**Purpose**: Displays all timeline events, chronological order, and conflicts.

**Sections**:
- Summary (total events, date range, conflicts, gaps)
- Timeline visualization (table sorted by year)
- Conflicts section (detailed analysis)
- Gaps section (missing periods)

**Example Timeline**:

```markdown
## Timeline

| Year | Event | Duration | Source | Status |
|------|-------|----------|--------|--------|
| -4004 | Creation (traditional) | Point | Genesis.md | ✓ |
| -2348 | Great Flood (traditional) | Point | Genesis.md | ✓ |
| -1446 | Exodus from Egypt | Point | Exodus.md | ⚠ Disputed |
| -931 | Divided Kingdom begins | Point | Kings.md | ✓ |
| -931 to -587 | Divided Kingdom period | 344 years | Kings.md | ✓ |
| -586 to -516 | Babylonian Captivity | 70 years | Timeline.xlsx | ✓ |
| 33 | Crucifixion | Point | Gospels.md | ✓ |
```

---

### Ontology Dashboard

**File**: `/master-truth/ontology/ontology-dashboard.md`

**Purpose**: Displays the conceptual structure showing how concepts relate to each other.

**Sections**:
- Summary (nodes, edges, orphans, cycles)
- Concept hierarchy (nested lists)
- Relationships table
- Orphan concepts section

**Example Concept Hierarchy**:

```markdown
## Concept Hierarchy

- **Coherence Theory**
  - Coherence Potential (χ)
    - Propagation Term
    - Entropy Term
  - Lowe Coherence Lagrangian
  - Grace Function (G)

- **Temporal Framework**
  - Physical Time
    - Chronological Events
  - Epistemic Time
    - Knowledge Acquisition
    - Revelation Sequence

- **Theological Mapping**
  - Trinity Structure
    - Father → Information Substrate
    - Son → Grace Function
    - Spirit → Witness Field
```

---

### Math Dashboard

**File**: `/master-truth/math/math-dashboard.md`

**Purpose**: Displays all mathematical objects, their translations, and variables.

**Sections**:
- Summary (equations, variables, undefined, translation completeness)
- Equations registry (with LaTeX and English)
- Variables registry
- Lowe Lagrangian analysis (current computation)

**Example Equation Entry**:

```markdown
### Core Equations

**Lowe Coherence Lagrangian**

$$\mathcal{L}_{LC} = \chi(t)\Big(\frac{d}{dt}(G+M+E+S+T+K+R+Q+F+C)\Big)^2 - S \cdot \chi(t)$$

*English:* Coherence equals the squared rate of collective phase alignment across all domain variables, minus entropy interference.

*Variables:* χ (coherence potential), G (grace), M (mercy), E (faith energy), S (sin/entropy), T (truth), K (knowledge), R (repentance), Q (quantum state), F (faith), C (consciousness)

*Status:* ✓ Fully translated, all variables defined
```

**Lowe Lagrangian Analysis**:

```markdown
## Lowe Coherence Lagrangian Analysis

**Current Computation:**

| Component | Formula | Current Value |
|-----------|---------|---------------|
| χ(t) | Coherence potential | 0.891 |
| Σ | Sum of all variables | (computed) |
| dΣ/dt | Rate of change | 0.961 |
| (dΣ/dt)² | Propagation squared | 0.923 |
| S·χ(t) | Entropy interference | 0.153 |
| **L_LC** | **χ(dΣ/dt)² - Sχ** | **0.847** |

**Interpretation:**

The positive L_LC value indicates the system is generating more coherence than 
entropy is destroying. The equilibrium condition (dL/dt = 0) would occur when 
χ̇ ∝ S, meaning coherence evolution is proportional to entropy — this is the 
mathematical expression of grace as negentropic correction.
```

---

### Theories Dashboard

**File**: `/master-truth/theories/theories-dashboard.md`

**Purpose**: Displays all theories (internal and external), their components, and interactions.

**Sections**:
- Summary (internal, external, conflicts)
- Internal theories table
- External theories table
- Cross-theory conflicts
- Theory dependency graph

---

### Coherence Dashboard

**File**: `/master-truth/coherence/coherence-dashboard.md`

**Purpose**: The primary diagnostic interface showing coherence scores, violations, and strengths.

**Sections**:
- Expanded Coherence Pulse
- Score progression table (historical)
- Violations log (detailed explanations)
- Strengths log (what's working well)
- Recommendations (ordered by impact)

---

### Breakthroughs Dashboard

**File**: `/master-truth/breakthroughs/breakthroughs-dashboard.md`

**Purpose**: Tracks major insights and their evolution over time.

**Sections**:
- Summary (total, this month, AI vs user)
- Breakthrough registry
- Detailed breakthrough entries
- Breakthrough timeline

---

### External Links Dashboard

**File**: `/master-truth/external-links/links-dashboard.md`

**Purpose**: Tracks all external references to SEP, Wikipedia, and other authoritative sources.

**Sections**:
- Summary (total, by source, auto vs manual)
- Links registry
- Suggested links
- Broken links

---

### Tags Dashboard

**File**: `/master-truth/tags/tags-dashboard.md`

**Purpose**: Analyzes tagging patterns and semantic clustering.

**Sections**:
- Summary (unique tags, total usages, clusters)
- Tag frequency table
- Tag clusters (co-occurrence patterns)
- Tag inconsistencies

---

### Progression Dashboard

**File**: `/master-truth/progression/weekly-summary.md`

**Purpose**: Provides meta-analytics on research velocity and progress over time.

**Sections**:
- Research velocity table
- Concept growth chart
- Coherence trend
- Weekly narrative summary

**Example Weekly Summary**:

```markdown
## Weekly Summary: January 13-19, 2025

This week saw significant progress on Paper 12, adding 12 new concepts and 3 
foundational axioms. The Lowe Coherence Lagrangian improved from 0.798 to 0.847, 
primarily due to:

1. Resolution of the timeline conflict between events ev003 and ev007
2. Addition of strong evidence for core causality axioms
3. Formalization of grace as negentropic correction (major breakthrough)

**Areas of Focus:**
- Mathematical formalism (6 new equations)
- Temporal framework (8 timeline events verified)
- External theory integration (2 new SEP links)

**Remaining Work:**
- 6 terms still need definitions
- 2 axiom contradictions need resolution
- 4 claims lack supporting evidence

**Projected Next Week:**
If current velocity continues, expect coherence to reach 0.87-0.89 by end of 
next week, assuming contradiction resolution proceeds.
```

---

## Generation Triggers

Dashboards regenerate based on these triggers:

### 1. On Semantic Block Change
When any semantic block in any note is modified, the affected dashboards regenerate. The system tracks which dashboards depend on which data types and only regenerates what's necessary.

### 2. On Manual Request
User clicks "Regenerate Dashboards" button in the plugin.

### 3. On Schedule
Optionally, dashboards can regenerate on a timer (hourly, daily) for users who want regular snapshots.

### 4. On Scope Change
When user changes the analysis scope, dashboards regenerate for the new scope.

---

## Dependency Map

This table shows which dashboards depend on which annotation types:

| Dashboard | Depends On |
|-----------|------------|
| Concepts | definition, term |
| Axioms | axiom, evidence (via relationships) |
| Evidence | evidence, axiom, claim (via relationships) |
| Claims | claim, evidence (via relationships) |
| Timeline | event |
| Ontology | definition, term, relationships |
| Math | equation |
| Theories | all (grouped by theory field) |
| Coherence | all (computed) |
| Breakthroughs | breakthrough |
| External Links | external-reference |
| Tags | all (via tags arrays) |
| Progression | historical snapshots |
| Master Sheet | all |

**Example**: When an axiom annotation changes, the system regenerates:
- Axioms Dashboard
- Evidence Dashboard (support chains may change)
- Theories Dashboard (if theory field changed)
- Coherence Dashboard (score recalculation)
- Master Sheet

---

## Performance Considerations

For large vaults, full regeneration of all dashboards could be slow. The system uses these optimizations:

### 1. Incremental Updates
Track which notes changed since last generation. Only re-query those notes and merge with cached data from unchanged notes.

### 2. Lazy Generation
Don't regenerate dashboards that haven't been viewed recently. Mark them as "stale" and regenerate on demand.

### 3. Background Processing
Run dashboard generation in a background worker so it doesn't block the UI.

### 4. Caching
Cache intermediate computations (coherence scores, relationship graphs) and invalidate only affected portions on change.

---

## Export Format

When exporting the `/master-truth/` folder, all dashboards are included as markdown files. The JSON data blocks at the bottom of each dashboard ensure that the data can be reimported and the dashboards can be regenerated in a new environment.

### Manifest File

**File**: `/master-truth/manifest.json`

```json
{
  "exportedAt": "2025-01-15T14:22:10Z",
  "pluginVersion": "1.0.0",
  "schemaVersion": "1.0",
  "scope": "global",
  "statistics": {
    "notes": 47,
    "annotations": 342,
    "relationships": 156,
    "concepts": 142,
    "axioms": 47,
    "evidence": 62,
    "claims": 89,
    "events": 34,
    "equations": 23,
    "theories": 15,
    "breakthroughs": 12
  },
  "coherence": {
    "global": 0.847,
    "lastUpdated": "2025-01-15T14:22:10Z"
  }
}
```

---

## Related Documents
- [[Semantic_Block_Format|Semantic Block Specification]]
- [[00_VAULT_SYSTEM/Config/12_Plugins/Theophysics_Obsidian_Plugin/03_MASTER_TRUTH/Master_Truth_Architecture|Master Truth Folder Architecture]]
- [[PostgreSQL_Schema|PostgreSQL Schema]]
- [[Coherence_Calculation|Coherence Engine Implementation]]
