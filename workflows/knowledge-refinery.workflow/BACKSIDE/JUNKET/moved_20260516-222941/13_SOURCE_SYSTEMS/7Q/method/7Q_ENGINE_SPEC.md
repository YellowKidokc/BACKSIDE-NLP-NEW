---
title: "7Q Engine — Complete Specification"
type: system-spec
version: 1.0
created: 2026-03-21
author: David Lowe | POF 2828
purpose: Obsidian plugin spec for the 7Q research methodology engine
target: Obsidian Forge publication + GitHub repo
---

# 7Q Engine — Plugin Specification

> Seven questions forward: classify anything.
> Seven questions reversed: prove anything.
> Q0: arrive humble or don't arrive at all.

---

## Design Principles

1. **Minimum input, maximum structure.** User fills 3-5 fields per question. System derives the rest.
2. **Machine-readable output.** Every field maps to YAML frontmatter, Postgres column, or graph edge.
3. **AI-injectable.** Every field has a one-purpose prompt. Any LLM can assist.
4. **9th grader can use it. Scientist can trust it.**
5. **Forward and reverse use the same fields.** Direction changes the order, not the structure.

---

## Q0 — Posture Before Inquiry

Not a question. A precondition. Displayed once at note creation. Cannot be skipped.

**Display:** A single statement the user acknowledges before proceeding.

> "The inquirer cannot be the ground of inquiry. You do not arrive already decided."

**Field:**

```yaml
q0_acknowledged: true  # Boolean. Checkbox. Required to proceed.
```

**AI Prompt:** None. This is human-only.

---

## Q1 — What Is It? (Identity)

**Function:** Create the object. Name it. Classify it. Prevent category confusion.

**Transformation:** undefined → defined

### Fields

| Field | Type | Required | UX |
|-------|------|----------|-----|
| `id` | UUID v4 | Auto | Hidden, auto-generated |
| `label` | String (max 8 words) | Yes | Text box |
| `claim_type` | Enum | Yes | Dropdown |
| `tier` | Enum | No | Dropdown |
| `statement` | Structured sentence | Yes | Guided builder |
| `tags` | String[] | Auto-suggest | Tag input with autocomplete |
| `relations` | Object[] | Optional | Link picker |

### Dropdown: `claim_type`

- descriptive
- causal
- ontological
- mathematical
- mechanistic
- predictive
- normative

### Dropdown: `tier`

- foundational (axiom, postulate, definition)
- derived (theorem, corollary, hypothesis)
- constraint (boundary condition)
- support (evidence bundle)
- connection (bridge, relationship)

### Guided Sentence Builder

Instead of blank text box:

```
[ SUBJECT ] → [ RELATIONSHIP ] → [ OBJECT ] → under [ CONDITIONS ]
```

User fills blanks. System composes: `"Observer consciousness influences random physical systems under controlled experimental conditions."`

### AI Prompts (Q1)

**Label:** `Generate a short clear label (max 8 words) summarizing this claim.`

**Type Classifier:** `Classify this statement into exactly one of: descriptive, causal, ontological, mathematical, mechanistic, predictive, normative. Return only the word.`

**Statement Refiner:** `Rewrite into a single precise sentence using: [subject] → [relationship] → [object] (under conditions). Remove all ambiguity. One sentence only.`

**Tag Generator:** `Generate 3-6 concise tags capturing core concepts. Return as comma-separated list.`

**Relation Suggester:** `Given this claim and the existing claims in the vault, suggest relationships (supports, contradicts, depends_on, equivalent_to). Return only high-confidence matches.`

### YAML Output

```yaml
q1_identity:
  id: "c_8f3a2e91-7b2c-4d1a-9c77-2f1e8c9a12ab"
  label: "Consciousness affects physical systems"
  claim_type: causal
  tier: derived
  statement: "Observer consciousness influences random physical systems under controlled experimental conditions."
  tags: [observer-effect, consciousness, randomness, PEAR]
  relations:
    - type: depends_on
      target: "c_xxxxx"
```

---

## Q2 — Where Does It Live? (Domain)

**Function:** Place the object in reality. Anchor it. Set boundaries.

**Transformation:** defined → located

### Fields

| Field | Type | Required | UX |
|-------|------|----------|-----|
| `primary_domain` | Enum | Yes | Dropdown |
| `additional_domains` | Enum[] | No | Multi-select dropdown |
| `scale` | Enum | Yes | Dropdown |
| `isomorphism_status` | Enum | No | Dropdown (appears if 2+ domains) |

### Dropdown: `primary_domain`

- physics
- biology
- psychology
- mathematics
- philosophy
- theology
- information
- social
- computational
- moral
- consciousness

### Dropdown: `scale`

- quantum
- molecular
- neural
- individual
- social
- civilizational
- cosmic
- universal

### Dropdown: `isomorphism_status`

- none (single domain)
- ISO-analogy (surface similarity)
- ISO-parallel (structural similarity, untested)
- ISO-confirmed (structural identity, tested)

### Sub-questions (displayed as helper text)

- Does it appear in more than one domain?
- If cross-domain: is it analogy or isomorphism? (Can you swap labels and the structure survives?)
- At what scale does it operate?

### AI Prompts (Q2)

**Domain Classifier:** `Identify the primary domain this claim belongs to. Choose from: physics, biology, psychology, mathematics, philosophy, theology, information, social, computational, moral, consciousness. Then identify any additional domains. Return primary first, then additional.`

**Scale Detector:** `At what scale does this claim operate? Choose from: quantum, molecular, neural, individual, social, civilizational, cosmic, universal. Return one.`

**Isomorphism Scanner:** `Does this claim appear structurally in more than one domain? If yes, is the cross-domain mapping an analogy (surface similarity) or isomorphism (structural identity that survives variable substitution)? Return: none, analogy, parallel, or confirmed.`

### YAML Output

```yaml
q2_domain:
  primary: physics
  additional: [consciousness, theology]
  scale: quantum
  isomorphism_status: ISO-confirmed
```

---

## Q3 — What Does It Say? (Assertion)

**Function:** Force precision. No hedging. The claim commits.

**Transformation:** located → stated

### Fields

| Field | Type | Required | UX |
|-------|------|----------|-----|
| `assertion` | String | Yes | Single sentence text box |
| `precision` | Enum | Auto | Auto-classified |
| `certainty` | Enum | Yes | Dropdown |
| `scope` | Enum | Yes | Dropdown |
| `negation` | String | Yes | Auto-generated, user confirms |

### Dropdown: `certainty`

- proven
- derived
- well_supported
- tentative
- speculative
- unknown

### Dropdown: `scope`

- universal
- domain_specific
- local
- specialized

### Key Sub-question

**"Can a serious opponent restate this claim accurately?"** If the opponent can't restate it, it isn't precise enough. Displayed as helper text.

### The Negation Field

System auto-generates the negation of the assertion. User confirms it's correct. This becomes the seed for Q7 (kill conditions).

Example:
- Assertion: "Observer consciousness influences random physical systems."
- Negation: "Observer consciousness has no influence on random physical systems."

### AI Prompts (Q3)

**Precision Assessor:** `Rate the precision of this statement: vague, basic, detailed, mathematical, precise. Return one word.`

**Negation Generator:** `Generate the exact logical negation of this claim in one sentence. The negation must be testable.`

**Opponent Restatement:** `You are a skeptical opponent of this claim. Restate it in your own words as accurately and charitably as possible. If you cannot restate it clearly, respond: "UNCLEAR — needs refinement."`

### YAML Output

```yaml
q3_claim:
  assertion: "Observer consciousness influences random physical systems under controlled experimental conditions."
  precision: detailed
  certainty: well_supported
  scope: universal
  negation: "Observer consciousness has no measurable influence on random physical systems."
```

---

## Q4 — What Supports It? (Evidence)

**Function:** Attach justification. Show it's not arbitrary.

**Transformation:** stated → supported

### Fields

| Field | Type | Required | UX |
|-------|------|----------|-----|
| `evidence_type` | Enum[] | Yes | Multi-select dropdown |
| `evidence_tier` | Enum | Yes | Dropdown |
| `sources` | Object[] | Yes | Source entry form |
| `replication` | Enum | Yes | Dropdown |
| `competing_support` | Boolean | No | Checkbox |

### Dropdown: `evidence_type`

- empirical
- experimental
- observational
- mathematical
- logical
- scriptural
- historical
- inferential

### Dropdown: `evidence_tier`

- tier_1 (direct experimental, replicated)
- tier_2 (observational, partially replicated)
- tier_3 (inferential, unreplicated, historical)

### Dropdown: `replication`

- replicated
- partial
- unreplicated
- not_applicable

### Sub-question (Critical)

**"Could this same evidence support a competing model equally well?"**

If yes → checkbox `competing_support: true` → flag for Q7.

### Source Entry (Repeatable)

```
[ Author/Lab ] | [ Year ] | [ Finding summary, 1 line ] | [ Sigma / p-value if applicable ]
```

### AI Prompts (Q4)

**Evidence Finder:** `Search for published empirical evidence that either supports or contradicts this claim. Return author, year, finding, and significance level for each.`

**Tier Classifier:** `Given this evidence, classify it as tier_1 (direct experimental, replicated), tier_2 (observational, partially replicated), or tier_3 (inferential, unreplicated). Return one.`

**Competing Model Check:** `Could this same evidence equally support a different explanation? If yes, name the competing model.`

### YAML Output

```yaml
q4_evidence:
  evidence_type: [experimental, observational]
  evidence_tier: tier_1
  sources:
    - author: "PEAR Lab"
      year: 1979-2007
      finding: "2.5M trials show consciousness correlates with RNG outputs"
      significance: "6.35σ"
    - author: "Global Consciousness Project"
      year: 1998-2010
      finding: "325+ events show collective coherence spikes"
      significance: "6σ"
  replication: replicated
  competing_support: false
```

---

## Q5 — What Does It Depend On? (Dependencies)

**Function:** Expose the foundation. Reveal hidden assumptions.

**Transformation:** supported → grounded

### Fields

| Field | Type | Required | UX |
|-------|------|----------|-----|
| `depends_on` | Link[] | Yes | Note link picker from vault |
| `axiom_deps` | String[] | No | Tag-select from axiom list |
| `assumptions` | String[] | Yes | List input |
| `chain_terminus` | Enum | Yes | Dropdown |
| `fragility` | Enum | Yes | Dropdown |

### Dropdown: `chain_terminus`

Where does the dependency chain end?

- axiom (self-evident foundation)
- brute_fact (accepted without proof)
- circularity (loops back — **flag this**)
- open (chain doesn't terminate — **flag this**)

### Dropdown: `fragility`

If a dependency fails, does this claim:

- collapse_immediately
- degrade_gracefully
- survive_independently

### Sub-questions

- What must already be true for this to stand?
- Trace the chain all the way down. Where does it end?
- Are any of the dependencies themselves unverified?

### AI Prompts (Q5)

**Dependency Extractor:** `List every assumption and prior truth this claim requires. Be exhaustive. Include hidden assumptions the author may not have stated.`

**Chain Tracer:** `Trace the dependency chain of this claim downward. For each dependency, ask: what does THAT depend on? Continue until you reach axiom, brute fact, or circularity. Return the chain.`

**Fragility Assessor:** `If [dependency X] fails, does this claim collapse immediately, degrade gracefully, or survive independently? Assess each dependency.`

### YAML Output

```yaml
q5_dependencies:
  depends_on:
    - "[[Quantum measurement problem]]"
    - "[[Shannon information theory]]"
  axiom_deps: [A1.1, A1.3]
  assumptions:
    - "Consciousness is not reducible to computation"
    - "RNG outputs are genuinely random before observation"
  chain_terminus: axiom
  fragility: degrade_gracefully
```

---

## Q6 — What Does It Force? (Consequences)

**Function:** Generate downstream constraints. If true, what else must be true?

**Transformation:** grounded → generative

### Fields

| Field | Type | Required | UX |
|-------|------|----------|-----|
| `enables` | Link[] | No | Note link picker |
| `implies` | String[] | Yes | List input |
| `predicts` | String[] | Yes | List input |
| `cross_domain_force` | Boolean | No | Checkbox |
| `untested_predictions` | String[] | No | List input |

### Sub-questions

- If this is true, what else MUST be true that nobody has checked?
- Does it generate a testable prediction?
- Does it force a consequence in a DIFFERENT domain? → **That's where isomorphisms live.**

### The Cross-Domain Trigger

If `cross_domain_force: true` → system prompts: "You said this forces something in another domain. Does the structure survive variable substitution? If yes, this may be an isomorphism. Flag for Q2 review."

This is where the ontological tree, propagation map, and structural isomorphism pages COME FROM. They're Q6 output.

### AI Prompts (Q6)

**Consequence Generator:** `If this claim is true, what else must necessarily be true? List downstream consequences. Include consequences the author has not stated.`

**Prediction Extractor:** `What testable predictions does this claim generate? List predictions that have NOT yet been tested separately from those already confirmed.`

**Cross-Domain Scanner:** `Does this claim force consequences in a domain other than its primary domain? If yes, name the domain and the forced consequence. Assess whether the cross-domain mapping is analogy or structural isomorphism.`

### YAML Output

```yaml
q6_consequences:
  enables:
    - "[[Prayer effects should be measurable]]"
    - "[[Community coherence amplification]]"
  implies:
    - "Focused intentionality produces stronger effects than diffuse attention"
    - "Consciousness is not epiphenomenal"
  predicts:
    - "PEAR-type effects should replicate in any properly controlled setting"
  cross_domain_force: true
  untested_predictions:
    - "Coherence field should show measurable gradient around sustained prayer communities"
```

---

## Q7 — What Kills It? (Falsification)

**Function:** Attach termination conditions. Make failure explicit. Every object carries its own death warrant.

**Transformation:** generative → testable

### Fields

| Field | Type | Required | UX |
|-------|------|----------|-----|
| `death_conditions` | Object[] | Yes | Structured entry |
| `branch_status` | Enum | Yes | Dropdown |
| `collapse_cascade` | Link[] | No | Note link picker |
| `proof_status` | Enum | Yes | Dropdown |
| `adversarial_tested` | Boolean | Yes | Checkbox |

### Death Condition Entry (Repeatable)

```
[ Condition statement ] | [ Death type ] | [ Severity ]
```

### Dropdown: `death_type`

- self_refutation (claim destroys itself when stated)
- infinite_regress (pushes question back without resolution)
- empirical_contradiction (data kills it)
- logical_incoherence (contradicts established chain)
- explanatory_failure (runs out of road at forced questions)

### Dropdown: `branch_status`

- alive (survives all known tests)
- dead (killed by specific condition)
- problematic (carries unresolved cost)
- terminal (stops generating — not dead, but done)
- untested (no one has tried to kill it)

### Dropdown: `proof_status`

- open
- argued
- derived
- tested
- survived_adversary

### Sub-questions (Critical)

- Name the death condition. Which of the five types?
- What breaks DOWNSTREAM if this fails? (Link to Q6 consequences)
- **Has anyone actually tried to kill it? Or has it only survived friendly examination?**

### AI Prompts (Q7)

**Death Condition Generator:** `Generate specific, testable conditions that would falsify this claim. For each, classify as: self_refutation, infinite_regress, empirical_contradiction, logical_incoherence, or explanatory_failure.`

**Cascade Analyzer:** `If this claim is falsified, what other claims in the system collapse? Trace the downstream damage.`

**Adversarial Attacker:** `You are an expert opponent of this claim. Mount the strongest possible attack. Use the claim's own dependencies and assumptions against it. Identify the single weakest point.`

**Survival Assessor:** `Has this claim been tested adversarially by someone who genuinely wanted it to fail? Or has it only been examined by sympathetic parties? Rate: untested, friendly_only, light_adversarial, serious_adversarial, survived_expert_attack.`

### YAML Output

```yaml
q7_falsification:
  death_conditions:
    - condition: "If RNG outcomes show zero correlation with observer presence across 10K+ trials"
      death_type: empirical_contradiction
      severity: fatal
    - condition: "If consciousness is proven to be purely computational with no observer effect"
      death_type: logical_incoherence
      severity: fatal
  branch_status: alive
  collapse_cascade:
    - "[[Prayer effects claim]]"
    - "[[Church as quantum error correction]]"
  proof_status: survived_adversary
  adversarial_tested: true
```

---

## Completion Tracking

Auto-calculated from field presence:

```yaml
q_complete:
  q0: true   # acknowledged
  q1: true   # label + type + statement filled
  q2: true   # domain + scale filled
  q3: true   # assertion + certainty filled
  q4: false  # sources empty
  q5: false  # dependencies empty
  q6: true   # at least one consequence listed
  q7: false  # no death conditions entered
q_score: 4   # count of true values (0-7)
```

**Dataview query for incomplete notes:** `WHERE q_score < 7 SORT q_score ASC`

---

## Output Pipeline

What the engine produces → three possible outputs:

| Output | Trigger | Display |
|--------|---------|---------|
| **Isomorphism** | Q2 has 2+ domains AND Q6 has cross_domain_force=true AND isomorphism_status=ISO-confirmed | Structural isomorphism page |
| **Evidence** | Q4 has tier_1 or tier_2 sources with significance levels | Evidence convergence strip |
| **Kill Condition** | Q7 death_conditions populated | Falsification court |

The ontological tree = running the engine on "does anything exist?"
The propagation map = running the engine on "what is a distinction?"
The structural isomorphism = Q6 output across all five symmetry pairs
The evidence page = Q4 output aggregated
The kill conditions page = Q7 output aggregated

**Everything is engine output. The engine is the product.**

---

## Truth Score (Emergent Evaluation)

The user does not fill out a scoring rubric. They answer seven questions. The score falls out of the answers. Not imposed — emergent from structure.

### Six Variables (All Derived From 7Q Fields)

| Variable | Name | Source | What It Measures |
|----------|------|--------|-----------------|
| **S** | Survivability | Q7 `death_conditions` + `branch_status` | How many kill conditions it survived. Alive vs dead vs problematic. |
| **E** | Evidence | Q4 `evidence_tier` + `replication` + `sources` | Source quality, replication status, significance levels. |
| **L** | Logic | Q4 `evidence_type` (mathematical/logical) + Q3 `precision` | Internal consistency, proof strength, formal validity. |
| **D** | Dependencies | Q5 `chain_terminus` + `fragility` | Foundation stability. Axiom terminus = strong. Circular = weak. |
| **P** | Predictions | Q6 `predicts` + `untested_predictions` | Does it generate correct predictions? Confirmed vs untested ratio. |
| **C** | Coherence | Q2 `isomorphism_status` + Q6 `cross_domain_force` | Cross-domain survival. ISO-confirmed = maximum. Single-domain = neutral. |

### Formula

```
T = w₁·S + w₂·E + w₃·L + w₄·D + w₅·P + w₆·C
```

- Normalized to 0–1
- Weights adjustable (default: equal)
- Each variable computed from fields the user already filled

### Variable Computation (How Each Score Is Derived)

**S (Survivability):**
- `branch_status = alive` AND `adversarial_tested = true` → S = 1.0
- `branch_status = alive` AND `adversarial_tested = false` → S = 0.6
- `branch_status = problematic` → S = 0.3
- `branch_status = dead` → S = 0.0

**E (Evidence):**
- tier_1 + replicated → E = 1.0
- tier_1 + partial → E = 0.8
- tier_2 + replicated → E = 0.7
- tier_2 + unreplicated → E = 0.4
- tier_3 → E = 0.2
- no sources → E = 0.0

**L (Logic):**
- Has mathematical proof → L = 1.0
- Has logical proof → L = 0.8
- Precision = mathematical or precise → L += 0.2 bonus
- No formal proof → L = 0.3 (if internally consistent), 0.0 (if incoherent)

**D (Dependencies):**
- chain_terminus = axiom + fragility = survive_independently → D = 1.0
- chain_terminus = axiom + fragility = degrade_gracefully → D = 0.8
- chain_terminus = brute_fact → D = 0.5
- chain_terminus = circularity → D = 0.1
- chain_terminus = open → D = 0.0

**P (Predictions):**
- Confirmed predictions / total predictions ratio
- 0 predictions → P = 0.0 (claim is inert)
- All confirmed → P = 1.0
- Untested predictions count as neutral (0.5 each)

**C (Coherence):**
- ISO-confirmed across 2+ domains → C = 1.0
- ISO-parallel → C = 0.6
- ISO-analogy → C = 0.3
- Single domain, no cross-domain force → C = 0.0 (not penalized, just neutral)

### YAML Output (Per Claim)

```yaml
truth_score:
  S: 0.6    # survived but not adversarially tested
  E: 0.8    # tier_1, partially replicated
  L: 0.8    # logical proof, precise statement
  D: 1.0    # axiom terminus, survives independently
  P: 0.75   # 3/4 predictions confirmed
  C: 1.0    # ISO-confirmed cross-domain
  T: 0.825  # weighted composite
  confidence: high  # auto-classified from T range
```

### Confidence Classification

| T Range | Label | Meaning |
|---------|-------|---------|
| 0.85–1.0 | **established** | Survived adversarial testing, replicated evidence, strong logic, stable foundations |
| 0.65–0.84 | **well_supported** | Strong but gaps remain (untested predictions, partial replication) |
| 0.40–0.64 | **tentative** | Some support but significant unknowns |
| 0.15–0.39 | **speculative** | More unknown than known |
| 0.0–0.14 | **unsupported** | No evidence, no proof, or actively falsified |

### Cluster Truth (Aggregation Across Claims)

When multiple claims are related (via `relations` links):

```yaml
cluster:
  name: "Observer-dependent collapse"
  claims: [c_001, c_002, c_003, c_004]
  mean_T: 0.78
  variance: 0.04
  classification: stable_region
```

**Interpretation:**
- **High T + Low variance** → Stable truth region. Multiple claims converge.
- **High T + High variance** → Contested frontier. Strong claims disagree.
- **Low T + Low variance** → Consistently weak. Probably false.
- **Low T + High variance** → Noise. No signal.

### Mapping to Existing Scorer

This truth score IS the Unified Coherence Scorer (`unified_scorer.py`) in new clothes:

| 7Q Truth Score | Unified Scorer |
|----------------|----------------|
| T (composite) | χ (coherence) |
| confidence range | κ (confidence) |
| variance across cluster | ρ (robustness) |

The 7Q Engine is the front door. The scorer is the back end. Same math, different interface.

### Dataview Queries (Truth Score)

```dataview
// Highest truth claims
TABLE truth_score.T AS "Truth", truth_score.confidence AS "Confidence",
  q1_identity.label AS "Claim"
FROM "" WHERE truth_score.T != null
SORT truth_score.T DESC LIMIT 20
```

```dataview
// Claims that need adversarial testing (high T but untested)
TABLE truth_score.T AS "Truth", q7_falsification.adversarial_tested AS "Tested"
FROM "" WHERE truth_score.T > 0.5 AND q7_falsification.adversarial_tested = false
SORT truth_score.T DESC
```

```dataview
// Weakest links (lowest D score = fragile foundations)
TABLE truth_score.D AS "Dependency", q5_dependencies.chain_terminus AS "Terminus"
FROM "" WHERE truth_score.D < 0.5
SORT truth_score.D ASC
```

---

## Plugin Architecture (Obsidian Forge)

### Core Features

1. **New Note Wizard** — Walks user through Q1-Q7 with guided fields
2. **Template Insertion** — Generates YAML frontmatter from wizard answers
3. **AI Assist Button** — Per-field AI prompts (works with any LLM API)
4. **Completion Sidebar** — Shows q_score, highlights missing questions
5. **Direction Toggle** — Forward (Q1→Q7) or Reverse (Q7→Q1) mode
6. **Truth Score Dashboard** — Auto-computed T score with S/E/L/D/P/C breakdown
7. **Cluster View** — Aggregated truth across linked claims, shows stable regions vs frontiers
8. **Dataview Integration** — Pre-built queries for score, domain, status, dependencies, truth
9. **Graph View Enhancement** — Color nodes by q_score, branch_status, truth_score, domain

### File Output

Every note created by the plugin produces:
- Valid Obsidian markdown with YAML frontmatter
- Exportable to JSON / CSV / PostgreSQL
- Graph-edge-ready via `relations` and `depends_on` fields

---

## The Acronym (TBD)

Seven letters. One word. Each letter IS a question.
Must be memorable, pronounceable, and carry meaning.
Q0 sits outside the word — the silence before the first letter.

Candidates under consideration. Lock when it's right, not when it's fast.

---

## System Summary (Three Layers)

```
LAYER 1: THE METHOD
  Q0 (posture) → Q1-Q7 (seven questions, each with sub-questions, fields, AI prompts)
  Forward: classify anything. Reverse: prove anything.

LAYER 2: THE OUTPUT
  Isomorphism ← Q2 + Q6 cross-domain survival
  Evidence    ← Q4 aggregated sources
  Kill        ← Q7 death conditions

LAYER 3: THE SCORE
  T = w₁·S + w₂·E + w₃·L + w₄·D + w₅·P + w₆·C
  All variables derived from fields user already filled.
  Cluster aggregation → truth landscape across many claims.
```

The user fills seven questions. The system produces three outputs and one score. Nothing else is required. Everything else is visualization.

---

*David Lowe | POF 2828 | Theophysics*
*"Define → Ground → Propagate → Test → Score. Everything else is metadata."*
