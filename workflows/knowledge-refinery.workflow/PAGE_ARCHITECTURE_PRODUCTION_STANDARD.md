# Theophysics Vault Page Architecture

Status: locked production standard
Purpose: define what every finished production vault page looks like.

This is not folder structure. This is page anatomy.

Every production page has seven layers plus a visible Facts Header. Some layers can say `[pending]`, but the layer must exist.

## Required Epistemic State

Every page must declare:

```yaml
epistemic_state: hypothesis
```

Allowed values:

- `hypothesis`
- `partially_supported`
- `mathematically_derived`
- `empirically_supported`
- `unresolved`
- `speculative`
- `contradicted`

Without this field, the page is not production-ready.

## Required Link Types

The vault must distinguish link meaning:

- `depends_on` - load-bearing prerequisite
- `supports` - evidential support
- `relates_to` - associative connection
- `contradicts` - tension or conflict requiring review
- `supersedes` - version replacement

## Layer 0 - Frontmatter

The machine layer. Dataview, the pipeline, HTML generation, and graph tools read this.

Required starter fields:

```yaml
---
title: ""
paper_id: ""
series: ""
status: stub
type: paper
epistemic_state: hypothesis
laws: []
axioms: []
seven_q: ""
rubric_score: 0.0
verdict: HOLD
fact_check_score: 0.0
math_score: 0.0
contradiction_score: 0.0
timeline_score: 0.0
voice_score: 0.0
cross_domain_score: 0.0
word_count: 0
reading_level: 0.0
created: ""
updated: ""
author: POF 2828
ai_partners: []
tags: []
provenance: mixed
depends_on: []
supports: []
relates_to: []
contradicts: []
supersedes: []
related: []
---
```

## Layer 0A - Facts Header

The visible epistemic card at the top of every paper.

This is the reader-facing version of the frontmatter. It prevents a reader, AI partner, or future David from confusing a hypothesis with a supported theorem.

```markdown
> [!metadata] Facts
> **Paper ID:** GTQ-009
> **Status:** published
> **Epistemic State:** partially_supported
> **Verdict:** PUBLISH
> **Composite Score:** 0.84
> **Provenance:** mixed
> **Primary Links:** depends_on: [[Law 5]]; supports: [[Axiom A-012]]; contradicts: [pending]
```

## Layer 1 - Executive Summary

One paragraph. Three sentences max. Busy reader version.

```markdown
> [!abstract] Executive Summary
> [pending]
```

## Layer 2 - Plain English

The everyday-person explanation. No jargon, no citations, no equations. 200-400 words.

## Layer 3 - Article

The actual paper. David's argument, cleaned by the lossless station but not replaced.

Must include:

- equations where needed
- equation presentation: equation, plain English, isomorphism proof
- Honest Audit
- disclaimer

## Layer 4 - Academic Summary

The scholar-facing version.

Must include:

- Abstract
- Key Claims
- Methodology
- Evidence Summary
- Limitations
- Falsification Criteria

## Layer 5 - Cross-Reference And Wiki Layer

The connective tissue.

Must include:

- related laws
- related axioms
- related papers
- related concepts
- upstream dependencies
- downstream dependents
- external references
- contradictions or tensions

## Layer 6 - Data And Evidence Layer

The receipts.

Must include:

- rubric scores
- fact check results
- math check results
- contradiction results
- timeline results
- bibliography
- raw data links when available

## Layer 7A - Framework Impact

What the paper changes in the framework.

## Layer 7B - Open Obligations

What the paper does not prove, and what must be tested next.

This is the honesty layer. It keeps the vault epistemically stable.

## Pipeline Mapping

```text
raw input
  -> classifier
  -> lossless prep
  -> claim extractor
  -> fact checker
  -> math checker
  -> contradiction detector
  -> timeline verifier
  -> paper grader
  -> axiom mapper
  -> Excel rubric
  -> HTML report card
  -> Obsidian page compiler
  -> production vault page
```

The pipeline fills the layers. David writes or approves Layer 3.
