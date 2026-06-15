---
title: "Evidence Classification Protocol"
type: system-spec
version: 1.0
created: 2026-03-21
author: David Lowe | POF 2828
purpose: Companion to 7Q Engine Spec — how evidence enters, gets classified, scored, and connected
principle: "Not all evidence is the same kind of evidence — but all evidence must declare what kind it is."
---

# Evidence Classification Protocol

> A claim is only as strong as its evidence — and evidence is only as strong as its explanation.

This document completes the 7Q system. The 7Q Engine tells you to ask "what supports it?" (Q4). This protocol tells you how to answer that question rigorously.

---

## Core Principle

No raw evidence enters the system unstructured.

Every piece of evidence becomes an atomic unit with:
- an identity
- a type
- a strength score across three independent channels
- declared limits on what it can and cannot prove

If it can't be classified, compared, and scored, it's storage — not knowledge.

---

## The Three Channels

Modern science scores evidence on one axis: "is it repeatable?" That's not enough. Repeatable phenomena without explanation are incomplete. Lived experience without measurement is unverifiable. You need three independent channels, and they multiply — not add.

### Channel 1: Phenomenon Strength (PS)

**"What do we reliably observe?"**

This is what science already does well. Measurement. Replication. Signal detection.

| Component | Weight | What It Measures |
|-----------|--------|-----------------|
| reproducibility | 0.4 | Has it been replicated? By independent teams? |
| effect_size | 0.3 | How large is the measured effect? |
| measurement_quality | 0.3 | Direct measurement, proxy, or inferred? |

```
PS = (reproducibility × 0.4) + (effect_size × 0.3) + (measurement_quality × 0.3)
```

Scale: 0–1

### Channel 2: Explanatory Depth (ED)

**"Do we understand WHY?"**

This is what science systematically avoids. Repeatable without explained is incomplete. Every major breakthrough in physics came from someone who asked why. Every dead framework refused to.

| Component | Weight | What It Measures |
|-----------|--------|-----------------|
| mechanism_clarity | 0.4 | Is there a causal pathway? Can you trace it? |
| constraint_consistency | 0.3 | Does the explanation survive known physics/logic? |
| scope | 0.3 | Does it explain adjacent cases or just this one? |

```
ED = (mechanism_clarity × 0.4) + (constraint_consistency × 0.3) + (scope × 0.3)
```

Scale: 0–1

**The Why-Penalty:** If ED = 0 (no explanation at all), evidence strength is capped at 50% no matter how repeatable it is. This is the mechanism that enforces the principle: observed ≠ explained, repeatable ≠ understood.

### Channel 3: Experiential Coherence (EC)

**"Does it produce stable, structured patterns across time, behavior, and agents?"**

This is not "I feel strongly about it." This is: does the evidence produce consistent downstream effects in lived systems? This channel exists because there are forms of evidence that are experientially undeniable but not directly transferable — faith, moral conviction, consciousness itself. They are real. They must be handled rigorously, not dismissed and not inflated.

| Component | Weight | What It Measures |
|-----------|--------|-----------------|
| internal_consistency | 0.25 | Does the experience contradict itself, or form stable structure? |
| longitudinal_stability | 0.25 | Does it persist over time, or fluctuate randomly? |
| behavioral_transformation | 0.25 | Does it produce measurable change in habits, decisions, outcomes? |
| intersubjective_pattern | 0.25 | Do independent individuals report structurally similar experiences? |

```
EC = (internal_consistency × 0.25) + (longitudinal_stability × 0.25) +
     (behavioral_transformation × 0.25) + (intersubjective_pattern × 0.25)
```

Scale: 0–1

**Critical constraint:** Experiential evidence must ALWAYS route through consequences (Q6) to affect claims. You never say "this is true because I experienced it." You say "this produces stable, repeatable structure across time, behavior, and agents — even if mechanism is incomplete."

---

## The Completeness Formula

The three channels don't add. They multiply through completeness gates.

```
Completeness Factor (CF) = (0.5 + 0.5 × ED) × (0.5 + 0.5 × EC)

E_final = PS × CF
```

### What This Does

| Scenario | PS | ED | EC | CF | E_final | Meaning |
|----------|----|----|----|----|---------|---------|
| Strong + explained + lived | 0.9 | 0.8 | 0.9 | 0.86 | 0.77 | Full weight earned |
| Strong + unexplained | 0.9 | 0.1 | 0.5 | 0.41 | 0.37 | Capped — repeatable but blind |
| Weak + well-explained | 0.3 | 0.9 | 0.5 | 0.71 | 0.21 | Explanation can't save weak data |
| Personal + stable + unexplained | 0.2 | 0.3 | 0.85 | 0.60 | 0.12 | Modest but not dismissed |
| Personal + stable + explained | 0.2 | 0.7 | 0.85 | 0.78 | 0.16 | Stronger — mechanism helps |
| Strong + explained + no lived | 0.9 | 0.8 | 0.0 | 0.45 | 0.41 | Lab-only — untested in life |
| Noise | 0.1 | 0.1 | 0.1 | 0.28 | 0.03 | Collapses as it should |

Key insight: You can't cheat the system. High PS alone gets capped. High EC alone can't compensate for no data. High ED alone can't compensate for no signal. You need at least two channels strong and the third not absent to score well.

---

## Evidence Classification (Five Gates)

Every evidence unit passes through five gates before entering the system.

### Gate 1: Evidence Identity (E1)

**"What IS this piece of evidence?"**

Not the claim — the evidence itself.

```yaml
e1_identity:
  id: "e_<uuid>"
  label: "<short name, max 8 words>"
  evidence_format: dataset | paper | observation | proof | protocol | prediction_result | isomorphism | testimony | synthesis
```

### Gate 2: Evidence Type (E2)

**"What kind of knowing is this?"**

Two layers:

**Epistemic Class** (what channel of knowledge):
```yaml
epistemic_class: empirical | logical | structural | experiential
```

**Evidence Type** (how it was obtained):
```yaml
evidence_type: experimental | observational | statistical | mathematical | logical | historical | scriptural | testimonial | inferential | isomorphic
```

**Reliability Class** (how solid is the source):
```yaml
reliability: replicated | single_study | anecdotal | simulated | inferred
```

### Gate 3: Strength Scoring (E3)

**"How strong is each channel?"**

User inputs (guided, not free-form):

```yaml
phenomenon_strength:
  reproducibility: 0.0-1.0    # dropdown: none(0) | single(0.3) | partial(0.6) | replicated(0.8) | massively_replicated(1.0)
  effect_size: 0.0-1.0        # dropdown: noise(0) | weak(0.3) | moderate(0.6) | strong(0.8) | overwhelming(1.0)
  measurement_quality: 0.0-1.0 # dropdown: inferred(0.2) | proxy(0.5) | direct(0.8) | precision(1.0)

explanatory_depth:
  mechanism_clarity: 0.0-1.0   # dropdown: unknown(0) | speculative(0.2) | partial(0.5) | clear(0.8) | mechanistic(1.0)
  constraint_consistency: 0.0-1.0 # dropdown: contradicts_known(0) | untested(0.3) | compatible(0.6) | derived_from(0.9)
  scope: 0.0-1.0              # dropdown: this_case_only(0.2) | domain(0.5) | cross_domain(0.8) | universal(1.0)

experiential_coherence:
  internal_consistency: 0.0-1.0   # dropdown: contradictory(0) | partial(0.4) | stable(0.7) | maximally_coherent(1.0)
  longitudinal_stability: 0.0-1.0 # dropdown: fluctuates(0.1) | recent(0.3) | years(0.6) | lifetime(0.9)
  behavioral_transformation: 0.0-1.0 # dropdown: none(0) | minor(0.3) | significant(0.6) | total(0.9)
  intersubjective_pattern: 0.0-1.0   # dropdown: unique(0.1) | small_group(0.3) | widespread(0.6) | cross_cultural(0.9)
```

**Computed outputs (auto-calculated):**

```yaml
scores:
  PS: <computed>
  ED: <computed>
  EC: <computed>
  CF: <computed>
  E_final: <computed>
```

### Gate 4: Linkage (E4)

**"What does this connect to?"**

```yaml
linkage:
  supports_claims: ["c_<uuid>"]     # which claims this evidence supports
  contradicts_claims: ["c_<uuid>"]  # which claims this evidence weakens
  connection_type: direct | inferential | contextual
  competing_support: false          # could this equally support a different claim?
  competing_model: ""               # if yes, name it
```

### Gate 5: Evidence Kill Conditions (E5)

**"What could invalidate THIS EVIDENCE?"**

Not the claim — the evidence itself.

```yaml
evidence_vulnerabilities:
  - type: selection_bias | confounding | unreproducible | measurement_error | sample_size | cherry_picking
    description: ""
    severity: minor | moderate | fatal
  adversarial_tested: true | false
  attacked_by: ""                   # who has tried to invalidate this evidence?
```

---

## Complete YAML Template (One Evidence Unit)

```yaml
---
# === EVIDENCE UNIT ===
e1_identity:
  id: "e_<uuid>"
  label: ""
  evidence_format: ""

e2_type:
  epistemic_class: ""
  evidence_type: ""
  reliability: ""

e3_strength:
  phenomenon_strength:
    reproducibility: 0.0
    effect_size: 0.0
    measurement_quality: 0.0
  explanatory_depth:
    mechanism_clarity: 0.0
    constraint_consistency: 0.0
    scope: 0.0
  experiential_coherence:
    internal_consistency: 0.0
    longitudinal_stability: 0.0
    behavioral_transformation: 0.0
    intersubjective_pattern: 0.0
  scores:
    PS: 0.0
    ED: 0.0
    EC: 0.0
    CF: 0.0
    E_final: 0.0

e4_linkage:
  supports_claims: []
  contradicts_claims: []
  connection_type: ""
  competing_support: false

e5_vulnerabilities:
  conditions: []
  adversarial_tested: false

limits:
  non_transferable: false
  requires_translation: ""
  notes: ""
---

# <Evidence Label>

<Brief description of what this evidence is, where it came from, and what it shows.>
```

---

## AI Prompts (Per Gate)

### E1 — Identity

```
Classify this evidence: is it a dataset, paper, observation, proof, protocol, prediction result, isomorphism detection, testimony, or synthesis? Return the format and a label (max 8 words).
```

### E2 — Type

```
For this evidence, determine:
1. Epistemic class: empirical (measured), logical (proven), structural (coherence-based), or experiential (lived/internal)?
2. Evidence type: experimental, observational, statistical, mathematical, logical, historical, scriptural, testimonial, inferential, or isomorphic?
3. Reliability: replicated, single_study, anecdotal, simulated, or inferred?
Return all three.
```

### E3 — Strength

```
Score this evidence across three channels (each component 0-1):

Phenomenon Strength:
- Reproducibility (none=0, single=0.3, partial=0.6, replicated=0.8, massive=1.0)
- Effect size (noise=0, weak=0.3, moderate=0.6, strong=0.8, overwhelming=1.0)
- Measurement quality (inferred=0.2, proxy=0.5, direct=0.8, precision=1.0)

Explanatory Depth:
- Mechanism clarity (unknown=0, speculative=0.2, partial=0.5, clear=0.8, mechanistic=1.0)
- Constraint consistency (contradicts=0, untested=0.3, compatible=0.6, derived=0.9)
- Scope (single case=0.2, domain=0.5, cross-domain=0.8, universal=1.0)

Experiential Coherence:
- Internal consistency (contradictory=0, partial=0.4, stable=0.7, maximal=1.0)
- Longitudinal stability (fluctuates=0.1, recent=0.3, years=0.6, lifetime=0.9)
- Behavioral transformation (none=0, minor=0.3, significant=0.6, total=0.9)
- Intersubjective pattern (unique=0.1, small group=0.3, widespread=0.6, cross-cultural=0.9)

Score honestly. Separate "unsupported" from "false." Separate "coherent" from "proven."
```

### E4 — Linkage

```
Which claims does this evidence connect to? For each:
1. Does it support, contradict, or provide context?
2. Is the connection direct or inferential?
3. Could this same evidence equally support a competing explanation? If yes, name it.
```

### E5 — Vulnerabilities

```
How could this evidence itself be wrong? Check for: selection bias, confounding variables, unreproducible conditions, measurement error, insufficient sample size, cherry-picking. For each vulnerability found, rate severity: minor, moderate, or fatal. Has anyone attempted to invalidate this evidence? If so, who and what happened?
```

---

## How Evidence Feeds Back Into 7Q

The evidence protocol is not separate from 7Q. It IS Q4, fully specified.

When the 7Q Engine reaches Q4 ("What supports it?"), the user creates evidence units using this protocol. Each evidence unit's `E_final` score feeds directly into the Truth Score:

```
7Q Truth Score variable "E" = mean(E_final) across all linked evidence units
```

The three channels also feed the scoring layer's cap system:

- If mean(ED) < 0.3 across all evidence → cap total Truth Score at 70
  "Repeatable but nobody knows why — incomplete."

- If mean(EC) = 0 and epistemic_class = experiential → evidence unit flagged
  "Claims experiential but shows no coherence pattern."

- If competing_support = true on majority of evidence → flag claim
  "Evidence doesn't distinguish this claim from alternatives."

---

## Epistemic Honesty Rules

These are non-negotiable and enforced by the system:

1. **"Observed" ≠ "Explained."** High PS with low ED gets capped. Always.

2. **"Repeatable" ≠ "Understood."** The system will not let you score high without answering why.

3. **"Evidence" ≠ "Complete evidence."** Every evidence unit declares its limits.

4. **"Personal" ≠ "Transferable."** Experiential evidence must always route through Q6 consequences. You measure the downstream effects, not the private experience.

5. **"Strong evidence" ≠ "Correct claim."** Evidence strength and claim validity are computed separately and never collapsed into one number.

6. **"Coherent" ≠ "True."** A system can be internally coherent and still false. Coherence is necessary but not sufficient.

7. **"Unsupported" ≠ "False."** Absence of evidence is not evidence of absence. The system marks unsupported claims as unknown, not dead.

---

## The Historical Thesis (Why This Matters)

Pre-1927, the scientists who moved the needle — Newton, Maxwell, Faraday, Einstein, Planck, Lemaître — all pursued explanatory closure. They asked why. Post-1927, instrumentalism correlated with proliferating interpretations, fragmentation, and unresolved foundational disputes.

This is not nostalgia. It's a testable claim:

> Science can produce reliable local predictions while remaining explanatorily underdetermined and structurally fragmented. Therefore, predictive success alone is an insufficient metric of theoretical maturity.

The Evidence Classification Protocol operationalizes this by making explanatory depth a first-class scoring channel alongside phenomenon strength. If you only measure "does it repeat?" you get modern physics: 20+ interpretations of quantum mechanics, no unification in 100 years. If you also measure "do we understand why?" you get a filter that rewards the kind of work that actually closes gaps.

| Dimension | What current science rewards | What this protocol adds |
|-----------|---------------------------|----------------------|
| Predictive adequacy | repeatability, fit, significance | Still required (PS channel) |
| Explanatory adequacy | Often optional | Mechanism, why, chain completion (ED channel) |
| Integrative adequacy | Weakly measured | Cross-domain unification, lived coherence (EC channel) |

A theory can be predictively competent and still be explanatorily immature. This protocol catches that.

---

## Folder Structure (Obsidian)

```
05_EVIDENCE_ENGINE/
  01_REGISTRIES/
    CLAIMS_REGISTER.md          ← existing
    EVIDENCE_REGISTER.md        ← existing, add E1-E5 fields
  02_LINKBOARD/
    CLAIM_EVIDENCE_SWITCHBOARD.md ← existing, add E_final scores
  03_EVIDENCE_UNITS/            ← NEW: one .md per evidence unit
    e_<uuid>.md
    e_<uuid>.md
  04_REPORTS/                   ← existing
  05_PIPELINE/                  ← existing
  EVIDENCE_CLASSIFICATION_PROTOCOL.md ← THIS DOCUMENT
```

---

## System Summary

```
EVIDENCE ENTERS
      ↓
E1: Identity (what is it?)
      ↓
E2: Type (what kind of knowing?)
      ↓
E3: Score (PS × ED × EC → E_final)
      ↓
E4: Link (which claims does it connect to?)
      ↓
E5: Kill (what could invalidate the evidence itself?)
      ↓
EVIDENCE UNIT STORED → feeds Q4 → feeds Truth Score
```

Five gates. Three channels. One formula. No raw evidence enters unstructured. No repeatable phenomenon gets full credit without explaining why. No lived experience gets dismissed, but none gets inflated either.

---

## One Line to Anchor It

> A claim is only as strong as its evidence — and evidence is only as strong as its explanation.

---

*David Lowe | POF 2828 | Theophysics*
*Companion to: 7Q Engine Specification v1.0*
