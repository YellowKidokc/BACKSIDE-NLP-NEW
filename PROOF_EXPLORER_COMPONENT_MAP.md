# PROOF EXPLORER: Component-to-Station Mapping
# POF 2828 | 2026-06-17
#
# Every component in the proof explorer is produced by a station.
# This document maps them so the template can auto-generate.

---

## THE 7 FRAMEWORK TABS

| Tab | What It Shows | Station That Produces It | Data Shape |
|-----|---------------|--------------------------|------------|
| **Axioms** | Which axioms ground this paper, orphaned claims | `axioms.station` | axiom IDs, grounding status, orphan count |
| **7Q Framework** | Q0-Q7 grid filled/empty status, inheritance check | `7q-classifier.station` | 8 cells (FILLED/EMPTY), inheritance PASS/FAIL |
| **Decision Tree** | Worldview pre-filter Q0-Q12 | `7q-engine.station` | 13 nodes, status per node |
| **Swap Test** | Isomorphism validation: forward + reverse prediction | `operators-canon.station` | domains, forward HOLDS/FAILS, reverse HOLDS/FAILS, confidence |
| **CKG Evaluator** | 5-tier quality: foundations/propositions/constraints/evidence/integration | `paper-proof-grader.station` | 5 tier scores (x/10), raw total, final score |
| **Fruits Scorer** | Structural invariant detection: F4/F7/F8/F9/F12 | `fruits-spirit-canon.station` | 5 fruit scores (+/-), total, COHERENT/INCOHERENT |
| **Iron Chain** | Lean 4 formal verification: theorem, mode, compile status | External (Lean 4) | mode (A/B/C), theorem name, VERIFIED/PENDING, axioms used |

---

## THE MAIN BODY CARDS

| Card | What It Shows | Station That Produces It |
|------|---------------|--------------------------|
| **LOWE FACTS** | F=Falsifiable, A=Axiomatic, C=Coherent, T=Testable, S=Systematic | Composite: ST_006 (falsification) + axioms + fruits + ST_006 + 7q |
| **Rigor Grid** (6 cells) | Rubric score, Chi score, CKG grade, Claims count, Layers OK, Status | `paper-proof-grader.station` |
| **Kill Conditions Table** | K1-K7 with condition, test, severity (fatal/wounding) | `ST_006 falsification.station` |
| **Promoted Claims** | Load-bearing claims that survived triage | `ST_005 load-bearing-claims.station` |
| **Evidence Spine** | Bars showing evidence coverage per claim/section | `ST_007 evidence-map.station` |
| **Dependency Graph** | Visual: which papers/axioms this paper depends on | `graph-linker.station` |
| **Tags** | Domain tags, law tags, framework tags | `ST_004 claim-classification.station` |
| **Metadata** | Word count, read time, author, date, status, Lean file | Intake parser + metadata |

---

## THINGS THAT NEED NEW STATIONS OR NEW CAPABILITY

| Need | Currently | Station/Capability |
|------|-----------|-------------------|
| **Auto-glossary** (>8th grade terms) | Manual glossary_data.json | NEW: `glossary-builder.station` using reading-level analysis + NER |
| **Reading level classifier** (per-word/term) | Not automated | Add to ST_002: flag every word above grade 8, output term list |
| **FACTS card generator** | Manual | NEW: `facts-card.station` — composite of multiple upstream outputs |
| **Series aggregation** | Not built | NEW: `series-aggregator.station` — rolls up all per-paper scores into series dashboard |
| **Proof explorer template builder** | Manual HTML | Enhance `html-article.station` — generate from JSON station outputs |

---

## AUTO-GLOSSARY SPECIFICATION

**Rule:** Any term in the article above 8th-grade reading level gets:
1. Added to glossary_data.json with definition
2. Auto-linked in the HTML (`<a href="/glossary/?term=...">`)
3. Flagged for the Easy reading version (ST_002 replaces with simpler word or adds explanation)

**How it works:**
```
ST_002 plain-language runs →
  For each section:
    1. Tokenize into words/phrases
    2. Check reading level per term (syllable count, frequency list, domain-specific)
    3. Terms above grade 8 → glossary_candidates list
    4. For each candidate:
       - Generate definition (LLM or existing glossary lookup)
       - Generate easy-version replacement (analogy or simpler word)
       - Add to glossary_data.json if not already present
    5. In Easy version: replace term with "simpler word (technical term)"
    6. In Academic version: keep term, add footnote link to glossary
```

**Output addition to ST_002:**
```json
{
  "glossary_candidates": [
    {
      "term": "coherence factor",
      "grade_level": 12,
      "definition": "A metric measuring how well a civilization's subsystems align and reinforce each other",
      "easy_replacement": "alignment score",
      "frequency_in_article": 14,
      "first_occurrence": {"paragraph": 3, "sentence": 1}
    },
    {
      "term": "phase transition",
      "grade_level": 11,
      "definition": "A sudden shift from one state to another, like water freezing to ice",
      "easy_replacement": "sudden shift",
      "frequency_in_article": 7,
      "first_occurrence": {"paragraph": 8, "sentence": 2}
    }
  ]
}
```

---

## CLASSIFICATION TAGS (what ST_004 should tag)

Every claim gets classified across these dimensions:

| Dimension | Labels | Station |
|-----------|--------|---------|
| **Maturity** | Formal Model, Structural Correspondence, Empirical Support, Analogy, Metaphor, Assertion | ST_004 |
| **Domain** | physics, theology, mathematics, consciousness, information_theory, ethics, empirical_data, historical | ST_004 |
| **Law** | Law1-Gravitation, Law2-Motion, Law3-EM, Law4-Strong, Law5-Thermo, Law6-Info, Law7-Quantum, Law8-Relativity, Law9-Weak, Law10-Coherence | ST_004 (new label set) |
| **7Q Position** | Q0-Posture, Q1-Identity, Q2-Domain, Q3-Claim, Q4-Support, Q5-Dependencies, Q6-Consequences, Q7-Kill | 7q-classifier |
| **CKG Tier** | Tier1-Foundations, Tier2-Propositions, Tier3-Constraints, Tier4-Evidence, Tier5-Integration | paper-proof-grader |
| **Fruits** | love, joy, peace, patience, kindness, goodness, faithfulness, gentleness, self-control | fruits-spirit-canon |
| **Load-Bearing** | PAPER_CLAIM / CITATION_FACT / REVIEW / PARK | ST_005 |
| **Evidence Status** | SUPPORTED / PARTIAL / UNSUPPORTED / GAP | ST_007 |
| **Falsifiability** | HIGH / MEDIUM / LOW | ST_006 |

---

## SERIES AGGREGATION (how to roll up)

For a series of N papers, the aggregated view shows:

```json
{
  "series": "MDA",
  "total_papers": 61,
  "total_claims": 2847,
  "load_bearing_claims": 892,
  "average_ckg": 5.8,
  "average_fruits": "+6.2",
  "grade_distribution": {"A": 3, "B": 12, "C": 28, "D": 14, "F": 4},
  "evidence_coverage": {"SUPPORTED": 0.68, "PARTIAL": 0.18, "GAP": 0.14},
  "contradictions_found": 7,
  "cross_article_tensions": 23,
  "lean_verified": 8,
  "glossary_terms_generated": 340,
  "total_word_count": 182000,
  "chi_mean": 4.2,
  "chi_status": "MODERATE"
}
```

This becomes the series-level proof explorer — one page that summarizes the entire MDA corpus.

---

## TEMPLATE GENERATION ORDER

To auto-build a proof explorer from station outputs:

```
1. Collect all station artifacts for article X
2. Extract:
   - Rigor grid values from paper-proof-grader
   - FACTS card from facts-card composite
   - Kill conditions from ST_006
   - Claims from ST_005
   - 7Q grid from 7q-classifier
   - CKG scores from paper-proof-grader
   - Fruits scores from fruits-spirit-canon
   - Swap test from operators-canon
   - Axioms from axioms.station
   - Lean status from iron chain data
   - Evidence spine from ST_007
   - Tags from ST_004
   - Dependencies from graph-linker
3. Inject into proof-explorer template HTML
4. Write to proof-explorer/{article-id}.html
```
