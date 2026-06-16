# **System Architecture Map: Dashboard & Filter Specification**

This document provides the structural overview of how all dashboards interconnect, what filters they accept, and how data flows through the entire system.

---

## **Visual System Map**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              COHERENCE PULSE                                     │
│                    (Persistent header on ALL views)                              │
│         Global Coherence: 0.847 │ Propagation: 0.923 │ Entropy: 0.153           │
│                         Scope: [Note▼] Action: [Resolve ax001↔ax017]            │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                  │
│                           ┌─────────────────────┐                               │
│                           │    MASTER SHEET     │                               │
│                           │   (Tab 13 Output)   │                               │
│                           │   Unified Overview  │                               │
│                           └──────────┬──────────┘                               │
│                                      │                                          │
│           ┌──────────────────────────┼──────────────────────────┐               │
│           │                          │                          │               │
│           ▼                          ▼                          ▼               │
│   ┌───────────────┐          ┌───────────────┐          ┌───────────────┐       │
│   │   COHERENCE   │          │   THEORIES    │          │ BREAKTHROUGHS │       │
│   │   Dashboard   │          │   Dashboard   │          │   Dashboard   │       │
│   │   (Tab 10)    │◄────────►│   (Tab 12)    │◄────────►│   (Tab 9)     │       │
│   └───────┬───────┘          └───────┬───────┘          └───────┬───────┘       │
│           │                          │                          │               │
│           │    ┌─────────────────────┼─────────────────────┐    │               │
│           │    │                     │                     │    │               │
│           ▼    ▼                     ▼                     ▼    ▼               │
│   ┌─────────────────┐        ┌─────────────────┐        ┌─────────────────┐     │
│   │     AXIOMS      │        │     CLAIMS      │        │    EVIDENCE     │     │
│   │    Dashboard    │◄──────►│    Dashboard    │◄──────►│    Dashboard    │     │
│   │    (Tab 2)      │        │    (Tab 4)      │        │    (Tab 3)      │     │
│   └────────┬────────┘        └────────┬────────┘        └────────┬────────┘     │
│            │                          │                          │              │
│            └──────────────────────────┼──────────────────────────┘              │
│                                       │                                         │
│                                       ▼                                         │
│                          ┌────────────────────────┐                             │
│                          │   SUPPORT CHAINS       │                             │
│                          │   (Relationship Layer) │                             │
│                          └────────────┬───────────┘                             │
│                                       │                                         │
│       ┌───────────────────────────────┼───────────────────────────────┐         │
│       │                               │                               │         │
│       ▼                               ▼                               ▼         │
│ ┌───────────────┐             ┌───────────────┐             ┌───────────────┐   │
│ │   CONCEPTS    │             │     MATH      │             │   TIMELINE    │   │
│ │   Dashboard   │◄───────────►│   Dashboard   │◄───────────►│   Dashboard   │   │
│ │   (Tab 6)     │             │   (Tab 7)     │             │   (Tab 5)     │   │
│ └───────┬───────┘             └───────┬───────┘             └───────┬───────┘   │
│         │                             │                             │           │
│         └─────────────────────────────┼─────────────────────────────┘           │
│                                       │                                         │
│                                       ▼                                         │
│                          ┌────────────────────────┐                             │
│                          │      ONTOLOGY          │                             │
│                          │      Dashboard         │                             │
│                          │      (Tab 6)           │                             │
│                          └────────────────────────┘                             │
│                                       │                                         │
│       ┌───────────────────────────────┼───────────────────────────────┐         │
│       │                               │                               │         │
│       ▼                               ▼                               ▼         │
│ ┌───────────────┐             ┌───────────────┐             ┌───────────────┐   │
│ │   EXTERNAL    │             │     TAGS      │             │  PROGRESSION  │   │
│ │    LINKS      │             │   Dashboard   │             │   Dashboard   │   │
│ │   (Tab 8)     │             │   (Tab 11)    │             │   (Tab 13)    │   │
│ └───────────────┘             └───────────────┘             └───────────────┘   │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            SEMANTIC BLOCKS                                       │
│                         (Source of All Truth)                                    │
│                                                                                  │
│    %%semantic                                                                    │
│    { "version": "1.0", "annotations": [...], "relationships": [...] }           │
│    %%                                                                            │
│                                                                                  │
│    Every markdown note contains embedded semantic data                           │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         OPTIONAL: PostgreSQL Mirror                              │
│                                                                                  │
│   ┌──────────┐  ┌─────────────┐  ┌───────────────┐  ┌──────────────┐            │
│   │  notes   │  │ annotations │  │ relationships │  │   theories   │            │
│   └──────────┘  └─────────────┘  └───────────────┘  └──────────────┘            │
│                                                                                  │
│   ┌────────────────────┐  ┌─────────────┐  ┌─────────────┐                       │
│   │  coherence_history │  │ ai_sessions │  │ sync_queue  │                       │
│   └────────────────────┘  └─────────────┘  └─────────────┘                       │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## **Data Flow Diagram**

```
USER WRITES MARKDOWN
         │
         ▼
┌─────────────────────┐
│   Raw Markdown      │
│   with natural      │
│   annotations       │
│   (AXIOM:, etc.)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐         ┌─────────────────────┐
│   AI PARSING        │◄───────►│   AI WORKSPACE      │
│   (GPT Primary)     │         │   /ai-workspace/    │
│                     │         │   understanding.md  │
│   • Extract axioms  │         │   observations.md   │
│   • Extract claims  │         │   questions.md      │
│   • Extract events  │         │   suggestions.md    │
│   • Extract math    │         └─────────────────────┘
│   • Extract terms   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   SEMANTIC BLOCKS   │
│   Generated &       │
│   Embedded in       │
│   each note         │
│                     │
│   %%semantic...%%   │
└──────────┬──────────┘
           │
           ├─────────────────────────────────────┐
           │                                     │
           ▼                                     ▼
┌─────────────────────┐               ┌─────────────────────┐
│   VAULT INDEX       │               │   PostgreSQL        │
│   (In-Memory)       │               │   (Optional Mirror) │
│                     │               │                     │
│   Quick lookups     │               │   Complex queries   │
│   Local-first       │               │   Historical data   │
│   Always available  │               │   Analytics         │
└──────────┬──────────┘               └──────────┬──────────┘
           │                                     │
           └──────────────┬──────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│                    DASHBOARD GENERATOR                        │
│                                                               │
│   For each dashboard type:                                    │
│   1. Query relevant annotations by kind                       │
│   2. Query relevant relationships                             │
│   3. Apply scope filter (note/paper/multi/global)            │
│   4. Apply additional filters (theory, date range, etc.)     │
│   5. Compute derived metrics (coherence, coverage, etc.)     │
│   6. Render to markdown with embedded JSON data block        │
└──────────────────────────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────────────┐
│                    /master-truth/                             │
│                                                               │
│   master-sheet.md    ◄── Aggregates all dashboards           │
│   /concepts/         ◄── Glossary, terms, definitions        │
│   /axioms/           ◄── Axiom registry, contradictions      │
│   /evidence/         ◄── Evidence registry, support chains   │
│   /claims/           ◄── Claims registry, verification       │
│   /timeline/         ◄── Events, chronology, conflicts       │
│   /ontology/         ◄── Concept graph, relationships        │
│   /math/             ◄── Equations, variables, Lagrangian    │
│   /theories/         ◄── Internal & external theories        │
│   /coherence/        ◄── Scores, violations, strengths       │
│   /breakthroughs/    ◄── Discovery log, reasoning chains     │
│   /external-links/   ◄── SEP, Wikipedia, references          │
│   /tags/             ◄── Tag analytics, clusters             │
│   /progression/      ◄── Research velocity, trends           │
│   /history/          ◄── Timestamped snapshots               │
└──────────────────────────────────────────────────────────────┘
```

---

## **Filter Specification Matrix**

This table defines every filter available for each dashboard:

|Dashboard|Scope Filter|Theory Filter|Date Range|Status Filter|Strength Filter|Domain Filter|Tag Filter|Custom Filters|
|---|---|---|---|---|---|---|---|---|
|**Master Sheet**|✓ Note/Paper/Multi/Global|✓|✓|—|—|—|—|—|
|**Concepts**|✓|—|✓ Created/Modified|✓ Defined/Undefined/Needs-Review|—|✓|✓|First letter (A-Z)|
|**Axioms**|✓|✓|✓|✓ Healthy/Conflict/Needs-Evidence|—|—|✓|Scope (Universal/Local/Conditional)|
|**Evidence**|✓|✓|✓|—|✓ Strong/Moderate/Weak|—|✓|Source type (Empirical/Textual/Logical/Testimonial/Computational)|
|**Claims**|✓|✓|✓|✓ Verified/Unverified/Conflicting|✓|—|✓|Promotable (Yes/No)|
|**Timeline**|✓|—|✓ Event date range|✓ Valid/Conflict/Disputed|—|—|✓|Era (BC/AD), Participants|
|**Ontology**|✓|—|—|✓ Has-relationships/Orphan|—|✓|—|Relationship type (is-a/part-of/implies/etc.)|
|**Math**|✓|✓|✓|✓ Translated/Untranslated/Undefined-vars|—|✓|✓|Axiomatic (Yes/No)|
|**Theories**|✓|—|✓|✓ Active/Archived/Tension|—|—|—|Type (Internal/External), Coherence threshold|
|**Coherence**|✓|✓|✓ Historical range|—|—|—|—|Violation type, Severity threshold|
|**Breakthroughs**|✓|✓|✓|—|—|—|✓|Detected by (User/Claude/GPT), Significance (Major/Moderate/Minor)|
|**External Links**|✓|—|✓ Added/Accessed|✓ Valid/Broken|—|—|—|Source (SEP/Wikipedia/arXiv/DOI/Book/Journal/Other)|
|**Tags**|✓|—|✓|—|—|—|—|Frequency threshold, Cluster membership|
|**Progression**|✓|✓|✓|—|—|—|—|Metric type (Velocity/Growth/Trend)|

---

## **Scope Filter Detail**

The scope filter is the most important filter, determining what subset of the vault the dashboard analyzes:

### **Scope Levels**

**Note Level**

- Analyzes a single markdown file
- Used for: Quick check of a specific note's semantic health
- Filter input: Note path or selection
- Example: "Show coherence for Paper12-Grace-Dynamics.md"

**Paper Level**

- Analyzes all notes within a single folder
- Used for: Checking health of one paper/chapter in your research
- Filter input: Folder path
- Example: "Show all axioms in /Papers/Paper12/"

**Multi-Paper Level**

- Analyzes selected folders
- Used for: Comparing or aggregating across specific papers
- Filter input: Array of folder paths
- Example: "Show timeline events from Papers 1, 5, and 12"

**Global Level**

- Analyzes entire vault
- Used for: Overall framework health, master metrics
- Filter input: None (default root)
- Example: "Show global coherence score"

### **Scope Implementation**

```
User selects scope in UI
         │
         ▼
┌─────────────────────────────────────────┐
│   SCOPE RESOLVER                        │
│                                         │
│   Input: scope_type + scope_value       │
│                                         │
│   if scope_type == "note":              │
│       return [note_path]                │
│   elif scope_type == "paper":           │
│       return list_files_in_folder()     │
│   elif scope_type == "multi":           │
│       return flatten(folder_paths)      │
│   elif scope_type == "global":          │
│       return list_all_vault_files()     │
│                                         │
│   Output: List of note paths to analyze │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│   SEMANTIC BLOCK COLLECTOR              │
│                                         │
│   For each note in resolved paths:      │
│       Parse %%semantic...%% block       │
│       Add to working dataset            │
│                                         │
│   Output: Unified annotation set        │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│   DASHBOARD GENERATOR                   │
│                                         │
│   Apply additional filters              │
│   Compute metrics                       │
│   Render dashboard                      │
└─────────────────────────────────────────┘
```

---

## **Filter Parameter Specifications**

### **Theory Filter**

```json
{
  "filterType": "theory",
  "operator": "include" | "exclude" | "only",
  "values": ["Theophysics Core", "Dual-Time Model", "Grace Dynamics"],
  "includeUnassigned": true | false
}
```

**Operators:**

- `include`: Show items from these theories AND unassigned items
- `exclude`: Show everything EXCEPT items from these theories
- `only`: Show ONLY items from these theories (excludes unassigned)

---

### **Date Range Filter**

```json
{
  "filterType": "dateRange",
  "field": "created" | "modified" | "eventDate",
  "start": "2025-01-01T00:00:00Z",
  "end": "2025-01-31T23:59:59Z",
  "includeNull": true | false
}
```

**Fields:**

- `created`: When the annotation was first added
- `modified`: When the annotation was last changed
- `eventDate`: For timeline events, the historical date (BC/AD)

---

### **Status Filter**

Different dashboards have different status values:

**Concepts Status:**

```json
{
  "filterType": "status",
  "values": ["defined", "undefined", "needs-review"]
}
```

**Axioms Status:**

```json
{
  "filterType": "status",
  "values": ["healthy", "conflict", "needs-evidence", "deprecated"]
}
```

**Claims Status:**

```json
{
  "filterType": "status",
  "values": ["verified", "unverified", "conflicting", "promoted", "refuted"]
}
```

**Timeline Status:**

```json
{
  "filterType": "status",
  "values": ["valid", "conflict", "disputed", "uncertain"]
}
```

---

### **Strength Filter**

```json
{
  "filterType": "strength",
  "operator": "gte" | "lte" | "eq" | "between",
  "value": "strong" | "moderate" | "weak" | "unsupported",
  "numericThreshold": 0.7
}
```

For evidence and claims, strength can be categorical (strong/moderate/weak) or numeric (0.0-1.0 confidence score). The filter supports both.

---

### **Domain Filter**

```json
{
  "filterType": "domain",
  "values": ["physics", "theology", "mathematics", "philosophy", "history", "consciousness", "information"]
}
```

Domain values are standardized vocabulary from the ontology.

---

### **Tag Filter**

```json
{
  "filterType": "tag",
  "operator": "any" | "all" | "none",
  "values": ["causality", "coherence", "trinity"]
}
```

**Operators:**

- `any`: Item has at least one of these tags
- `all`: Item has all of these tags
- `none`: Item has none of these tags

---

### **Combined Filter Example**

A complex query might combine multiple filters:

```json
{
  "scope": {
    "type": "paper",
    "value": "/Papers/Paper12/"
  },
  "filters": [
    {
      "filterType": "theory",
      "operator": "include",
      "values": ["Grace Dynamics"]
    },
    {
      "filterType": "status",
      "values": ["needs-evidence"]
    },
    {
      "filterType": "dateRange",
      "field": "created",
      "start": "2025-01-01",
      "end": "2025-01-31"
    }
  ],
  "sort": {
    "field": "coherenceScore",
    "direction": "desc"
  },
  "limit": 50
}
```

This query would return: All axioms in Paper 12 that belong to Grace Dynamics theory, need evidence, were created in January 2025, sorted by coherence score descending, limited to 50 results.

---

## **Dashboard Dependency Graph**

This shows which dashboards feed into which other dashboards:

```
                    ┌──────────────────┐
                    │   MASTER SHEET   │
                    │                  │
                    │   Aggregates:    │
                    │   • Summary from │
                    │     each dash    │
                    │   • Global stats │
                    │   • Coherence    │
                    └────────┬─────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   COHERENCE     │ │    THEORIES     │ │  PROGRESSION    │
│                 │ │                 │ │                 │
│   Computes:     │ │   Groups:       │ │   Tracks:       │
│   • L_LC score  │ │   • All items   │ │   • Velocity    │
│   • Violations  │ │     by theory   │ │   • Growth      │
│   • Strengths   │ │   • External    │ │   • Trends      │
│                 │ │     mappings    │ │                 │
│   Depends on:   │ │                 │ │   Depends on:   │
│   ALL dashboards│ │   Depends on:   │ │   Historical    │
│                 │ │   Axioms,Claims │ │   snapshots of  │
│                 │ │   Evidence      │ │   ALL dashboards│
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                   │
         │    ┌──────────────┼──────────────┐    │
         │    │              │              │    │
         ▼    ▼              ▼              ▼    ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│     AXIOMS      │ │     CLAIMS      │ │    EVIDENCE     │
│                 │ │                 │ │                 │
│   Lists all     │ │   Lists all     │ │   Lists all     │
│   axioms with:  │ │   claims with:  │ │   evidence with:│
│   • Coherence   │ │   • Verification│ │   • Strength    │
│   • Conflicts   │ │   • Support     │ │   • Source type │
│                 │ │                 │ │                 │
│   Depends on:   │ │   Depends on:   │ │   Depends on:   │
│   Evidence      │ │   Evidence      │ │   (base data)   │
│   (support)     │ │   Axioms (→)    │ │                 │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  RELATIONSHIPS  │
                    │                 │
                    │  Stored as:     │
                    │  supports       │
                    │  contradicts    │
                    │  implies        │
                    │  depends-on     │
                    │  etc.           │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│    CONCEPTS     │ │      MATH       │ │    TIMELINE     │
│                 │ │                 │ │                 │
│   Glossary of   │ │   Equations &   │ │   Events in     │
│   all terms &   │ │   variables     │ │   chronological │
│   definitions   │ │   with English  │ │   order         │
│                 │ │   translations  │ │                 │
│   Depends on:   │ │                 │ │   Depends on:   │
│   (base data)   │ │   Depends on:   │ │   (base data)   │
│                 │ │   Concepts      │ │                 │
│                 │ │   (var→concept) │ │                 │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    ONTOLOGY     │
                    │                 │
                    │   Concept graph │
                    │   showing how   │
                    │   everything    │
                    │   relates       │
                    │                 │
                    │   Depends on:   │
                    │   Concepts      │
                    │   Relationships │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ EXTERNAL LINKS  │ │      TAGS       │ │  BREAKTHROUGHS  │
│                 │ │                 │ │                 │
│   References to │ │   Tag analysis  │ │   Major insight │
│   SEP, Wiki,    │ │   & clustering  │ │   discoveries   │
│   etc.          │ │                 │ │                 │
│                 │ │   Depends on:   │ │   Depends on:   │
│   Depends on:   │ │   All items     │ │   Axioms,Claims │
│   (base data)   │ │   (tags arrays) │ │   Evidence,Math │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

---

## **Regeneration Cascade Logic**

When data changes, this determines which dashboards need regeneration:

```
┌─────────────────────────────────────────────────────────────────┐
│                    CHANGE DETECTION                             │
│                                                                 │
│   When semantic block in note X changes:                        │
│                                                                 │
│   1. Identify what annotation types changed                     │
│   2. Look up dependency graph                                   │
│   3. Mark affected dashboards as stale                          │
│   4. Regenerate in dependency order (leaves → roots)            │
└─────────────────────────────────────────────────────────────────┘

CHANGE TYPE                    DASHBOARDS TO REGENERATE
───────────────────────────────────────────────────────────────────
Axiom added/modified      →    Axioms, Theories, Coherence, Master
Claim added/modified      →    Claims, Theories, Coherence, Master
Evidence added/modified   →    Evidence, Axioms, Claims, Coherence, Master
Definition added/modified →    Concepts, Ontology, Master
Term added/modified       →    Concepts, Ontology, Master
Event added/modified      →    Timeline, Coherence, Master
Equation added/modified   →    Math, Coherence, Master
External ref added        →    External Links, Master
Breakthrough added        →    Breakthroughs, Coherence, Master
Relationship added        →    Ontology, Axioms, Evidence, Claims, Coherence, Master
Tag changed              →    Tags, Master
Any change               →    Progression (if historical tracking enabled)
```

---

## **Query Interface Specification**

The UI provides these query capabilities for each dashboard:

### **Quick Filters (Toggles)**

```
┌─────────────────────────────────────────────────────────────────┐
│   AXIOMS DASHBOARD                                              │
│                                                                 │
│   Scope: [Note ▼] [Paper 12 ▼]                                 │
│                                                                 │
│   Quick Filters:                                                │
│   [✓] Show Healthy  [✓] Show Conflicts  [ ] Show Deprecated    │
│   [✓] Has Evidence  [ ] Needs Evidence                         │
│                                                                 │
│   Theory: [All ▼]    Domain: [All ▼]    Tags: [+Add Tag]       │
│                                                                 │
│   Sort: [Coherence ▼] [↓ Desc]          Show: [50 ▼] results   │
└─────────────────────────────────────────────────────────────────┘
```

### **Advanced Query Builder**

For complex queries, an advanced mode allows building filter chains:

```
┌─────────────────────────────────────────────────────────────────┐
│   ADVANCED QUERY                                                │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ WHERE theory IN ["Grace Dynamics", "Dual-Time Model"]   │   │
│   │ AND status = "needs-evidence"                           │   │
│   │ AND created > "2025-01-01"                              │   │
│   │ AND coherenceScore < 0.8                                │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   [+ Add Condition]  [Run Query]  [Save as Preset ▼]           │
└─────────────────────────────────────────────────────────────────┘
```

### **Saved Query Presets**

Users can save common queries:

```json
{
  "presets": [
    {
      "name": "Weak Points",
      "description": "All items needing attention",
      "query": {
        "scope": { "type": "global" },
        "filters": [
          { "filterType": "status", "values": ["conflict", "needs-evidence", "unverified", "undefined"] }
        ]
      }
    },
    {
      "name": "Recent Work",
      "description": "Everything added this week",
      "query": {
        "scope": { "type": "global" },
        "filters": [
          { "filterType": "dateRange", "field": "created", "start": "{{weekStart}}", "end": "{{now}}" }
        ]
      }
    },
    {
      "name": "Paper 12 Health",
      "description": "Status check for current paper",
      "query": {
        "scope": { "type": "paper", "value": "/Papers/Paper12/" },
        "filters": []
      }
    }
  ]
}
```

---

## **Cross-Dashboard Navigation**

Every item in every dashboard can link to related views in other dashboards:

```
┌─────────────────────────────────────────────────────────────────┐
│   AXIOM: ax003 - Grace acts as negentropic correction          │
│                                                                 │
│   Theory: Grace Dynamics                                        │
│   Coherence: 0.89                                               │
│   Status: ✓ Healthy                                             │
│                                                                 │
│   NAVIGATION:                                                   │
│   ├── [View in Theories Dashboard]     → Shows this axiom's    │
│   │                                       place in Grace        │
│   │                                       Dynamics theory       │
│   ├── [View Supporting Evidence]       → Evidence Dashboard     │
│   │                                       filtered to ev items  │
│   │                                       that support ax003    │
│   ├── [View in Ontology]               → Ontology Dashboard     │
│   │                                       centered on ax003     │
│   │                                       showing relationships │
│   ├── [View Related Math]              → Math Dashboard         │
│   │                                       showing equations     │
│   │                                       that use grace (G)    │
│   ├── [View in Coherence Analysis]     → Coherence Dashboard    │
│   │                                       showing this axiom's  │
│   │                                       contribution          │
│   └── [Go to Source Note]              → Opens Paper12.md at    │
│                                           the axiom location    │
└─────────────────────────────────────────────────────────────────┘
```

This navigation is implemented as pre-built filter links:

```markdown
[View Supporting Evidence](obsidian://plugin-command?dashboard=evidence&filter=supports:ax003)
```

---

## **Master Truth Folder Manifest**

The complete folder structure with file purposes:

```
/master-truth/
│
├── manifest.json                    ← Export metadata, statistics, version
├── master-sheet.md                  ← Unified overview (human-readable)
├── master-sheet.json                ← Unified overview (machine-readable)
│
├── /history/                        ← Timestamped snapshots
│   ├── 2025-01-15-14-22-10.md
│   ├── 2025-01-14-10-00-00.md
│   └── ...
│
├── /concepts/
│   ├── glossary-dashboard.md        ← Main concept view
│   ├── glossary-data.json           ← Raw concept data
│   ├── new-terms-log.md             ← Recently added terms
│   └── undefined-terms.md           ← Terms needing definitions
│
├── /axioms/
│   ├── axioms-dashboard.md          ← Main axiom view
│   ├── axioms-data.json             ← Raw axiom data
│   ├── axiom-registry.md            ← Full axiom list
│   └── contradictions-log.md        ← Active conflicts
│
├── /evidence/
│   ├── evidence-dashboard.md        ← Main evidence view
│   ├── evidence-data.json           ← Raw evidence data
│   ├── evidence-registry.md         ← Full evidence list
│   └── support-chains.md            ← What supports what
│
├── /claims/
│   ├── claims-dashboard.md          ← Main claims view
│   ├── claims-data.json             ← Raw claims data
│   ├── claims-registry.md           ← Full claims list
│   └── unsupported-claims.md        ← Claims needing evidence
│
├── /timeline/
│   ├── timeline-dashboard.md        ← Main timeline view
│   ├── timeline-data.json           ← Raw event data
│   ├── events-registry.md           ← Full event list
│   └── chronological-conflicts.md   ← Dating conflicts
│
├── /ontology/
│   ├── ontology-dashboard.md        ← Main concept graph view
│   ├── ontology-data.json           ← Raw graph data
│   ├── concepts-graph.md            ← Visual hierarchy
│   └── relationships.md             ← All relationship types
│
├── /math/
│   ├── math-dashboard.md            ← Main math view
│   ├── math-data.json               ← Raw equation data
│   ├── equations-registry.md        ← Full equation list
│   ├── variables-registry.md        ← Variable→concept mappings
│   └── lowe-lagrangian.md           ← L_LC analysis
│
├── /theories/
│   ├── theories-dashboard.md        ← Main theories view
│   ├── theories-data.json           ← Raw theory data
│   ├── internal-theories.md         ← Your frameworks
│   ├── external-theories.md         ← Referenced frameworks
│   └── cross-theory-conflicts.md    ← Inter-theory tensions
│
├── /coherence/
│   ├── coherence-dashboard.md       ← Main coherence view
│   ├── coherence-data.json          ← Raw coherence data
│   ├── score-progression.md         ← Historical scores
│   ├── violations-log.md            ← Current issues
│   ├── strengths-log.md             ← What's working well
│   └── lowe-lagrangian-history.md   ← L_LC over time
│
├── /breakthroughs/
│   ├── breakthroughs-dashboard.md   ← Main breakthroughs view
│   ├── breakthroughs-data.json      ← Raw breakthrough data
│   ├── breakthrough-registry.md     ← Full breakthrough list
│   └── breakthrough-timeline.md     ← Chronological insights
│
├── /external-links/
│   ├── links-dashboard.md           ← Main links view
│   ├── links-data.json              ← Raw links data
│   └── links-registry.md            ← All external references
│
├── /tags/
│   ├── tags-dashboard.md            ← Main tags view
│   ├── tags-data.json               ← Raw tag data
│   └── tag-clusters.md              ← Co-occurrence patterns
│
└── /progression/
    ├── research-velocity.md         ← Items added over time
    ├── concept-growth.md            ← Concept accumulation
    ├── coherence-trend.md           ← L_LC trajectory
    └── weekly-summary.md            ← Narrative summaries
```

---

## **Summary: The Complete Filter System**

To summarize what filters exist and where they apply:

**Universal Filters (Available on ALL dashboards):**

1. **Scope** — Note / Paper / Multi-Paper / Global
2. **Date Range** — Created / Modified timeframe
3. **Theory** — Include / Exclude specific theories

**Domain-Specific Filters:**

|Dashboard|Unique Filters|
|---|---|
|Concepts|Definition status, Domain, First letter|
|Axioms|Coherence threshold, Contradiction status, Evidence count|
|Evidence|Strength, Source type|
|Claims|Verification status, Promotable flag|
|Timeline|Era (BC/AD), Date range (historical), Conflict status|
|Ontology|Relationship type, Orphan status|
|Math|Translation status, Undefined variables, Axiomatic flag|
|Theories|Internal/External type, Coherence threshold|
|Coherence|Violation type, Severity threshold|
|Breakthroughs|Detected by (User/AI), Significance level|
|External Links|Source type, Link validity|
|Tags|Frequency threshold, Cluster membership|
|Progression|Metric type, Time granularity|

---

This architecture map provides the complete structural specification for how all dashboards connect, what data flows where, and what filters are available at each level. The system is designed so that everything traces back to the semantic blocks embedded in individual notes, making the entire framework portable and reconstructible.

What would you like me to specify next? The AI Prompt Specifications would define exactly what instructions Claude and GPT receive when analyzing notes. Or we could go into the PostgreSQL Query Library showing the exact SQL for each dashboard computation.