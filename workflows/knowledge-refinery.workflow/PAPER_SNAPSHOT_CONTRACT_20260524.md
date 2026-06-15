# Paper Snapshot Contract - 7QS / Knowledge Graph

Date: 2026-05-24

Reference snapshot:

- `X:\Backside\workflows\knowledge-refinery.workflow\axioms-closure_PRE_SEVEN_QUESTIONS_20260516-212828.html`
- Recycle mirror: `X:\#recycle\knowledge-refinery.workflow\axioms-closure_PRE_SEVEN_QUESTIONS_20260516-212828.html`

## Core Decision

Every paper should produce one canonical **Paper Snapshot** before downstream export.

The snapshot is the congruent information layer. It is not merely a report. It is the object that tells every later station what the paper is, what it claims, what it does not claim, what tags enter the knowledge graph, what 7QS says, what can kill the claim, and what derivation chain must exist.

HTML, Markdown, Obsidian YAML, Excel, graph nodes, graph edges, paper grades, and critique prompts should all be projections of the same snapshot.

## Snapshot Purpose

The paper snapshot answers:

- What is this paper?
- Where does it live in the canon / series / domain map?
- What tags should enter the knowledge graph?
- What claims are actually being made?
- What claims are explicitly not being made?
- What is true, false, unresolved, or tier-limited?
- What does 7QF classify?
- What does 7QR eliminate or leave alive?
- What does 7QE score?
- What derivation chain supports each major claim?
- What defeat condition would falsify the claim?
- What downstream stations must zoom into before rewriting or judging?

## Required Snapshot Sections

### 1. Identity

Minimum fields:

```yaml
snapshot_id:
source_id:
source_path:
title:
series:
article_number:
author:
created_at:
updated_at:
canonical_status: draft | review | canonical | published | deprecated
input_format: html | markdown | docx | pdf | txt
output_formats:
```

### 2. Graph Tags

Tags must be machine-useful, not only human labels.

```yaml
tags:
  topical:
  series:
  laws:
  axioms:
  methods:
  epistemic:
  entities:
  scripture:
  physics:
  theology:
  math:
```

These become graph node labels, Obsidian tags, search facets, and paper-grade grouping keys.

### 3. 7QS Spine

The reference HTML defines the public spine:

- `Q0` Posture: honest inquiry or advocacy?
- `Q1` Identity: what is it?
- `Q2` Location: where does it live?
- `Q3` Assertion: what is claimed?
- `Q4` Evidence: what supports it?
- `Q5` Dependencies: what must be true?
- `Q6` Consequences: what follows?
- `Q7` Falsification: how does it die?

Snapshot shape:

```yaml
seven_qs:
  q0_posture:
    answer:
    confidence:
    notes:
  q1_identity:
    answer:
    confidence:
    notes:
  q2_location:
    answer:
    confidence:
    notes:
  q3_assertion:
    answer:
    confidence:
    notes:
  q4_evidence:
    answer:
    confidence:
    notes:
  q5_dependencies:
    answer:
    confidence:
    notes:
  q6_consequences:
    answer:
    confidence:
    notes:
  q7_falsification:
    answer:
    confidence:
    notes:
```

### 4. Method Passes

The snapshot must separate method outputs:

```yaml
method_passes:
  seven_q_forward:
    classification:
    claim_type:
    domain:
    law_mapping:
    axiom_mapping:
    output_claim:
  seven_q_reverse:
    eliminated_branches:
    surviving_branches:
    unresolved_branches:
    kill_conditions:
  seven_q_evidence:
    phenomenon_strength:
    explanatory_depth:
    experiential_convergence:
    cross_context_convergence:
    final_evidence_score:
    evidence_notes:
```

### 5. Claim Ledger

Every material claim should have its own object.

```yaml
claims:
  - claim_id:
    text:
    normalized_text:
    claim_type: empirical | mathematical | theological | historical | interpretive | methodological | meta
    status: claimed | not_claimed | supported | refuted | unresolved | tier_limited
    epistemic_tier: 0 | 1 | 2 | 3
    confidence:
    source_span:
    source_section:
    tags:
    supporting_evidence:
    dependencies:
    consequences:
    defeat_conditions:
    derivation_chain:
    graph_nodes:
    graph_edges:
```

Required distinction:

- `claimed`: the paper actually asserts this.
- `not_claimed`: the paper might sound adjacent to this, but does not assert it.
- `tier_limited`: the claim is valid only within a tier, e.g. structural commitment rather than lab prediction.
- `unresolved`: the paper does not give enough evidence to close it.

This prevents later models from attacking a strawman or upgrading a limited claim into a stronger one.

### 6. Epistemic Status

The reference snapshot uses tier disclosure. That needs to become formal output.

```yaml
epistemic_status:
  overall_tier:
  tier_reason:
  test_mode:
  what_can_be_tested:
  what_cannot_be_tested:
  honest_disclosures:
```

Default tier language:

- `Tier 0`: Preconditions of inquiry; self-refuting to deny.
- `Tier 1`: Foundational / structural commitments; tested by consistency, generative power, and parsimony.
- `Tier 2`: Empirical predictions; tested by protocols, replication, thresholds, and external datasets.
- `Tier 3`: Interpretive / narrative / explanatory synthesis; tested by coherence, coverage, and non-contradiction.

### 7. Derivation Chain

Everything important must have a provenance path.

```yaml
derivations:
  - derivation_id:
    conclusion_claim_id:
    starts_from:
    steps:
      - step_id:
        premise:
        operation:
        output:
        support:
    dependencies:
    weakest_link:
    break_if_false:
```

This is the source of graph edges:

- `DERIVES_FROM`
- `DEPENDS_ON`
- `SUPPORTS`
- `CONTRADICTS`
- `LIMITED_BY`
- `FALSIFIED_BY`
- `MAPS_TO_LAW`
- `MAPS_TO_AXIOM`

### 8. Station Marks

Every station that touches the paper must mark the snapshot.

```yaml
station_marks:
  - station_id:
    station_name:
    status: pending | running | complete | failed | skipped
    started_at:
    completed_at:
    input_hash:
    output_hash:
    changed_fields:
    warnings:
```

For the Math Translation Layer specifically:

```yaml
math_translation_layer:
  status:
  translated_spans:
    - span_id:
      original:
      translated:
      source_location:
      dictionary_terms:
      confidence:
      needs_review:
  downstream_zoom_targets:
```

Later graders and rewrite models must zoom into these spans first before changing the paper.

### 9. Output Projections

The snapshot should export to:

- `.paper-snapshot.json` as the canonical machine object.
- `.paper-snapshot.md` as the readable Obsidian / review copy.
- `.paper-snapshot.html` as the public / dashboard view.
- `.paper-snapshot.xlsx` as the audit workbook.
- Obsidian YAML frontmatter.
- Knowledge graph nodes/edges.
- Paper grader summary.

No downstream output should invent fields that are not traceable back to the snapshot.

## Graph Shape

Minimum graph nodes:

- `Paper`
- `Claim`
- `Tag`
- `Law`
- `Axiom`
- `Evidence`
- `Dependency`
- `DefeatCondition`
- `DerivationStep`
- `StationRun`
- `TranslatedSpan`

Minimum graph edges:

- `PAPER_HAS_CLAIM`
- `PAPER_HAS_TAG`
- `CLAIM_MAPS_TO_LAW`
- `CLAIM_MAPS_TO_AXIOM`
- `CLAIM_SUPPORTED_BY`
- `CLAIM_DEPENDS_ON`
- `CLAIM_HAS_DEFEAT_CONDITION`
- `CLAIM_DERIVED_BY`
- `DERIVATION_STEP_NEXT`
- `STATION_PROCESSED_PAPER`
- `STATION_CHANGED_FIELD`
- `TRANSLATED_SPAN_IN_CLAIM`

## Non-Negotiables

- Tags are not decoration. They are graph intake.
- 7QS is not a prose section. It is the inquiry skeleton.
- Claims and not-claims must be separated.
- Every strong claim needs a defeat condition.
- Every derivation needs a weakest-link field.
- Math Translation Layer edits must mark exact spans.
- Paper grader, Obsidian YAML, executive summary, Excel, and graph output must all come from the same snapshot.

## /PROBE

The failure mode is letting each station output its own local truth.

If paper grader has one claim list, Obsidian YAML has another, graphify has another, and Excel has another, then the system will look productive while silently diverging. The snapshot contract prevents that. It makes every station write into one shared object first, then exports the same truth in multiple formats.

## Implementation Order

1. Add `.paper-snapshot.json` generation after intake and extraction.
2. Make paper grader write claims, scores, epistemic tier, and defeat conditions into the snapshot.
3. Make Math Translation Layer write translated spans into the snapshot.
4. Make Obsidian YAML/frontmatter read tags from the snapshot.
5. Make graph export read nodes/edges from the snapshot.
6. Make Excel export read claims, 7QS, station marks, and derivations from the snapshot.
7. Make HTML/Markdown reports render the snapshot instead of recomputing.

