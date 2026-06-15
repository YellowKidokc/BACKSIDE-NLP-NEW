---
# ============== AI PROCESSING DIRECTIVE ==============
ai_analysis_prompt: |
  Please analyze this publication draft and:
  1. Generate 200-300 word abstract (academic style)
  2. Extract 3-5 key findings
  3. Verify all claims are sourced to atoms/molecules/laws
  4. Check citation completeness
  5. Identify target journals/venues
  6. Generate SEO keywords for Substack
  7. Flag any unsupported claims
  8. Format all equations in LaTeX

  Content to analyze: {See full document below}

# ============== CORE METADATA ==============
title: "{{title}}"
subtitle: ""
author: "David Lowe"
co_authors:
  -
created: "{{date}}"
updated: "{{date}}"

# ============== STATUS & PUBLICATION ==============
status: draft | review | final | published
phase: 06_Publication
paper_number:
series: "The Logos Papers" | "Theophysics Foundations" | "Applied Logos" | "Standalone"

# ============== CLASSIFICATION ==============
type: paper | essay | article | book-chapter | presentation
publication_type: academic | substack | blog | book | conference

domains:
  - theophysics | physics | theology | philosophy | mathematics | information-theory

topics:
  -

tags:
  -

# ============== PUBLICATION ROUTING ==============
visibility: public | academia | premium | free
security: low | medium

publish_to:
  production: true
  research: false
  template: false
  substack: true
  arxiv: false
  journal: false

target_venues:
  - "Substack (Theophysics)"
  - "arXiv (physics.gen-ph)"
  - "Journal of Consciousness Studies"

# ============== CONTENT STRUCTURE ==============
abstract: AI-will-generate
key_findings:
  - AI-will-extract

word_count: 0
estimated_reading_time: ""

# ============== VALIDATION & GROUNDING ==============
claims_sourced_to:
  atoms: []
  molecules: []
  laws: []

analyses_cited: []
experiments_cited: []

# ============== PEER REVIEW ==============
review_status: not-submitted | submitted | under-review | accepted | rejected | published
peer_reviewed: false
submitted_to: ""
submission_date: ""
reviewer_feedback: []

# ============== SEO & DISCOVERABILITY ==============
seo_keywords:
  -

related_papers: []
citation_ready: false

# ============== DISPLAY OPTIONS ==============
math: true
mermaid: false
toc: true
citations: true

# ============== VERSIONING ==============
version: "1.0"
doi: ""
permalink: ""

# ============== REVIEW TRACKING ==============
next_review: ""
priority: 1-10
premium_content: false

---

# {{title}}
*{{subtitle}}*

**Author:** {{author}}
**Series:** {{series}}
**Paper #{{paper_number}}**

---

## Abstract
(200-300 words, formal academic style)

---

## Key Findings
1.
2.
3.

---

## Table of Contents
```toc
```

---

## 1. Introduction
(Context, motivation, research question)

---

## 2. Theoretical Foundation
(What atoms/molecules/laws ground this work?)

**Core Concepts:**
- [[Atom 1]]
- [[Molecule 1]]
- [[Law 1]]

---

## 3. Framework Development
(The meat of the argument)

### 3.1 Subsection

### 3.2 Subsection

---

## 4. Mathematical Formulation
$$

$$

---

## 5. Experimental Predictions
**This framework predicts:**
1.
2.
3.

**Falsification criteria:**
-

---

## 6. Evidence & Validation
**Physical Evidence:**

**Theological Evidence:**

**Mathematical Consistency:**

---

## 7. Implications
**For Physics:**

**For Theology:**

**For Consciousness Studies:**

---

## 8. Discussion
(Limitations, open questions, future work)

---

## 9. Conclusion
(Summary of key contributions)

---

## Acknowledgments
(Co-authors, reviewers, AI assistants)

---

## References
### Academic Citations
1.

### Internal Framework
- [[Law 1]]
- [[Molecule 1]]
- [[Analysis 1]]

---

## Appendices
### Appendix A: Mathematical Derivations

### Appendix B: Experimental Protocols

---

## Metadata for Publication
**Keywords:**
**DOI:**
**License:** CC BY 4.0
**Citation:** Lowe, D. (2025). {{title}}. *The Logos Papers*, Paper {{paper_number}}.
