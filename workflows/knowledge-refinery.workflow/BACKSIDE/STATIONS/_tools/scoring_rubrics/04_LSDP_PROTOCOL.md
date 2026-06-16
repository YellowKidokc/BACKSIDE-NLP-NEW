---
publish: false
---
# LOWE SERIES DISCLOSURE PROTOCOL (LSDP) v0.1

> **Purpose:** A standardized framework for independent researchers publishing multi-document series to clearly communicate scope, provide traceable evidence paths, and meet journal requirements proactively.

---

## PART I: SERIES ARCHITECTURE

### 1.1 Series Manifest (Required — Lives in Paper 1 or Standalone)

```yaml
series_manifest:
  title: "Cross-Domain Coherence Project"
  author: "David Lowe"
  version: 1.0
  total_papers: 12
  status: "In Progress | Complete | Under Review"
  
  papers:
    - paper_id: P1
      title: "Introduction to Cross-Domain Moral Decay"
      type: "Overview | FREE"
      scope: "Framework introduction, claims summary, roadmap"
      excludes: "Statistical derivations, raw data, domain-specific analyses"
      
    - paper_id: P2
      title: "The Quantum Bridge"
      type: "Technical | PAID"
      scope: "Lindbladian formalism, decoherence mathematics"
      depends_on: [P1]
      required_for: [P3, P4, P5]
```

### 1.2 Dependency Graph

Every series needs a visual or structured dependency map:

```
P1 (Overview)
 ├── P2 (Quantum Bridge) ──────┐
 ├── P3 (Statistical Methods) ─┤
 │    └── P4 (Domain Analysis) │
 ├── P5 (Historical Data)      │
 │    └── P6 (Timeline Sync)   │
 └── P7-P10 (Domain Papers) ───┤
      └── P11 (Synthesis) ─────┘
           └── P12 (Implications)
```

---

## PART II: INDIVIDUAL PAPER DISCLOSURE BLOCK

Every paper in the series includes this block (frontmatter or appendix):

### 2.1 Scope Declaration Block

```yaml
paper_scope:
  paper_id: P1
  uuid: a217dd34-e3df-4787-b077-21387a5057c1
  series: "Cross-Domain Coherence Project"
  position: "1 of 12"
  
  this_paper_covers:
    - "Introduction to the coherence decay framework"
    - "Summary of 45-domain analysis (list provided)"
    - "Central claims with citation pointers"
    - "Roadmap to supporting papers"
    
  this_paper_excludes:
    - item: "Statistical derivation of λ≈0.031"
      location: "{P3, Section 4.2, Eq. 17-23}"
    - item: "Raw dataset (69GB)"
      location: "{P3, Appendix B, DOI: 10.xxxxx}"
    - item: "Lindbladian equivalence proof"
      location: "{P2, Section 3, Theorem 2.1}"
    - item: "Individual domain analyses"
      location: "{P7-P10, domain-specific papers}"
      
  claims_register:
    - claim_id: C1
      statement: "45 domains show synchronized decay"
      evidence_location: "{P3, Table 1; P7-P10}"
      confidence: "High"
      falsifiable_by: "Independent replication with different domain selection"
      
    - claim_id: C2
      statement: "Inflection point 1965±8"
      evidence_location: "{P3, Section 5.1, Figure 3}"
      confidence: "High"
      falsifiable_by: "Alternative change-point detection methods"
```

### 2.2 The Curly Bracket Citation System (Adapted from IPCC)

**Format:**
```
{Paper#, Section/Chapter, Element}
```

**Examples:**
```
{P3, §4.2, Eq.17}     → Paper 3, Section 4.2, Equation 17
{P2, Thm.2.1}          → Paper 2, Theorem 2.1
{P7, Table 3}          → Paper 7, Table 3
{P3, App.B, DOI:xxx}   → Paper 3, Appendix B, with DOI
```

**In-text usage:**
> "The decay rate λ≈0.031 {P3, §4.2} emerges from Lindbladian dynamics {P2, Thm.2.1} applied across 45 domains {P7-P10}."

---

## PART III: COVER LETTER TEMPLATE (For Journal Submission)

```
Dear Editor,

RE: Submission of "[Paper Title]" — Part [X] of [Y] in the 
    Cross-Domain Coherence Project

SERIES CONTEXT:
This manuscript is Paper [X] of a [Y]-paper series investigating 
[brief description]. The complete series architecture is provided 
in Supplementary Document S1.

THIS PAPER'S SCOPE:
This paper specifically addresses:
• [Bullet 1]
• [Bullet 2]
• [Bullet 3]

THIS PAPER DELIBERATELY EXCLUDES:
The following elements are addressed in companion papers 
(see Series Manifest):
• [Element 1] → Paper [#], Section [X]
• [Element 2] → Paper [#], Section [Y]

STANDALONE VALIDITY:
While part of a series, this paper:
□ Contains all methods necessary for replication of its specific claims
□ Includes complete data availability statement
□ Can be evaluated independently of companion papers
□ Provides traceable citations to supporting materials

RELATED SUBMISSIONS:
• Paper [#] currently under review at [Journal]
• Paper [#] published at [Journal, DOI]
• Paper [#] in preparation

DATA AVAILABILITY:
[Statement per journal requirements]

Thank you for your consideration.

[Signature]
```

---

## PART IV: SERIES INDEX DOCUMENT (Standalone Reference)

A master document (published or hosted) containing:

### 4.1 Complete Paper Registry

| Paper | Title | Status | UUID | DOI/Link |
|-------|-------|--------|------|----------|
| P1 | Introduction | Published | abc123 | doi:xxx |
| P2 | Quantum Bridge | Under Review | def456 | — |
| P3 | Statistical Methods | Draft | ghi789 | — |

### 4.2 Claims-to-Evidence Map

| Claim ID | Statement | Primary Paper | Supporting Papers | Data Location |
|----------|-----------|---------------|-------------------|---------------|
| C1 | 45 domains decay | P1 | P3, P7-P10 | DOI:xxx |
| C2 | λ≈0.031 | P3 | P2 | P3 Appendix B |
| C3 | 1965±8 inflection | P3 | P5, P6 | P3 Fig.3 |

### 4.3 Domain Registry (For Domain-Heavy Projects)

| Domain # | Domain Name | Paper | Section | Dataset |
|----------|-------------|-------|---------|---------|
| D1 | Marriage rates | P7 | §2.1 | DS-001 |
| D2 | Church attendance | P7 | §2.2 | DS-002 |
| ... | ... | ... | ... | ... |
| D45 | [Name] | P10 | §4.3 | DS-045 |

---

## PART V: DATA AVAILABILITY ARCHITECTURE

### 5.1 Dataset Registry

```yaml
datasets:
  - dataset_id: DS-MASTER
    description: "Complete 69GB analysis dataset"
    location: "Zenodo DOI: 10.xxxx"
    access: "Open"
    format: "PostgreSQL dump + CSV"
    
  - dataset_id: DS-001
    description: "Marriage rate time series 1900-2024"
    parent: DS-MASTER
    location: "{DS-MASTER}/domains/marriage/"
    papers_using: [P1, P7]
```

### 5.2 Code Repository

```yaml
code:
  repository: "github.com/user/project"
  languages: ["Python", "R", "SQL"]
  
  scripts:
    - script_id: S-001
      name: "decay_rate_calculation.py"
      produces: "λ estimate"
      used_in: [P3, §4.2]
```

---

## PART VI: JOURNAL COMPATIBILITY CHECKLIST

Before submission, verify:

### Universal Requirements (All Journals)
- [ ] Data Availability Statement present
- [ ] Methods reproducible without series access
- [ ] All claims have traceable evidence paths
- [ ] Author contributions specified
- [ ] Competing interests declared
- [ ] LLM usage disclosed (if applicable)

### Series-Specific Requirements
- [ ] Series Manifest included (Supplementary)
- [ ] Scope Declaration Block in paper
- [ ] Curly bracket citations resolve correctly
- [ ] Dependency graph accurate
- [ ] Cross-paper references use stable identifiers (UUID/DOI)

### High-Prestige Journals (Nature, PRL)
- [ ] Standalone novelty argument in cover letter
- [ ] "Why this journal" explanation
- [ ] Length within limits
- [ ] Supplementary material organized per journal spec

### Standard Journals (Phys Rev A-E, etc.)
- [ ] Joint submission considered if appropriate
- [ ] Supplemental material properly cited
- [ ] REVTeX/LaTeX formatting

---

## PART VII: ERROR PROTOCOL (Adapted from IPCC)

### 7.1 Error Types

| Type | Definition | Response |
|------|------------|----------|
| Typographical | Spelling, formatting | Errata notice |
| Citation | Wrong reference | Correction + notification |
| Calculation | Math error | Full correction + impact assessment |
| Methodological | Flawed approach | Retraction consideration |

### 7.2 Correction Propagation

When error found in Paper X:
1. Assess impact on dependent papers
2. Issue correction in Paper X
3. Issue notices in affected papers
4. Update Series Index
5. Update Claims-to-Evidence Map

---

## ORIGIN

This protocol was developed to address a gap in academic publishing: no standardized format exists for independent researchers publishing multi-document series to disclose scope across papers. The IPCC model (Summary for Policymakers → Technical Summary → Full Chapters) was adapted for individual use.

**Key innovations:**
- YAML-structured manifests for machine readability
- Curly bracket citation system for cross-paper references
- Claims-to-Evidence mapping for traceability
- Journal-agnostic checklist for submission readiness

---

*"The first step toward truth is admitting what you wanted to find."*
