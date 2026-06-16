# Two-Lane MDA Report: MDA-004-facts-framework
*Generated: 2026-06-03 08:25*

**Report status:** Codex repair pass. The original two-lane OpenAI batch skipped this manifest article, and the referenced generator path (`X:\apps\paper-intelligence-suite-python\12_HEARTBEAT\openai_mda_two_lane.py`) is not present on this machine. Treat this as station repair guidance, not as an original API batch artifact.

**Total tokens:** not measured

---

## MATH LAYER ONLY

*Model: `codex-repair-pass` | Tokens: `not_measured`*

- MATH_STATUS: NEEDS_REPLICATION_BOUNDARY
- LOAD_BEARING_MATH:
  - The normalized Coherence Index (`chi_i(t) = (X_i(t) - X_i,min) / (X_i,max - X_i,min)`) is the measurement bridge from raw domain data to a 0-1 social coherence scale.
  - The fitted decay form (`chi(t) = chi_0 * e^(-lambda(t - t0)) + A sin(omega t + phi) + C`) carries the central claim that multiple domains share a common mathematical signature.
  - The reported parameter clustering is load-bearing: mean `lambda = 0.045 +/- 0.050`, median `lambda = 0.023`, and mean inflection window around 1958-1968.
  - The statistical rejection of independent decay depends on the K-S tests, t-test, bootstrap intervals, and leave-one-out robustness checks.
  - The Lindbladian comparison is the highest-risk isomorphism claim. It can be useful, but it must stay bounded to functional-form similarity unless a term-by-term mapping is supplied.

- ISOMORPHISM_TABLE:
  | mapping | current status | missing proof step | safe wording |
  |---------|----------------|---------------------|--------------|
  | Normalized domain values as a cross-domain Coherence Index | candidate_measurement_model | Define every domain transform, source range, `X_min`, `X_max`, weighting rule, and exclusion rule | "The Coherence Index is a proposed normalized tracking metric for comparing otherwise incommensurable domains." |
  | Shared exponential/social decay curve as evidence of synchronized coherence loss | pattern_evidence | Independent replication with pre-registered domains, normalization rules, and model comparison | "The analyzed domains exhibit a synchronized decay pattern under the current pipeline." |
  | Social decay equation and quantum decoherence equation | candidate_isomorphism | Provide a term-by-term mapping and show where the analogy stops | "The fitted social decay curve is structurally similar to familiar coherence-decay equations; causal identity is not established here." |
  | Constraint removal as the common coupling mechanism | hypothesis_only | Show causal or intervention evidence that constraint restoration locally improves `chi` | "Constraint removal is a candidate mechanism consistent with the pattern, not a demonstrated cause in this paper." |

- MISSING_EQUATIONS_OR_DEFINITIONS:
  - Exact construction of the composite Coherence Index from individual `chi_i` domain values.
  - Domain inclusion/exclusion rule for 45 surveyed domains, 23 sufficient domains, and 16 domains used in the parameter table.
  - The null distribution used for the K-S tests and whether multiple-comparison adjustments are needed.
  - Full reproducibility reference for `moral_decay_compute.py`, including input files and parameter-fitting method.
  - Term-by-term Lindbladian comparison: Hamiltonian term, dissipative term, coupling/noise term, social analogue, and failure boundary.
  - Sensitivity of `lambda` and `t0` to source selection, normalization range, and outlier removal.

- MINIMAL_PATCHES:
  - "This pattern is far too unlikely to be random" -> "Under the stated normalization and model-selection rules, this pattern is statistically unlikely to be random."
  - "This is not a metaphor. The mathematical structure is identical" -> "The fitted functional form is structurally similar to physical coherence-decay equations; a stronger identity claim requires a term-by-term proof."
  - "With expansion to 45 domains, this significance will increase" -> "Expansion to 45 domains is a prediction; it should remain conditional until the full-domain rerun is complete."
  - "Interventions that increase constraint/structure will locally reverse decay" -> "A falsifiable prediction is that constraint-restoration interventions should produce local `chi` recovery."
  - "No discipline asks..." -> "No single-domain discipline, by itself, explains the cross-domain synchronization shown here."

---

## READER ATTENTION ONLY

*Model: `codex-repair-pass` | Tokens: `not_measured`*

- ATTENTION_STATUS: STRONG_BUT_DENSE

- KEEP_THESE_LINES:
  - "The answer is in the data."
  - "No discipline asks: Why did all of these begin declining simultaneously?"
  - "Forty-five systems. One curve. Same inflection point. Same decay rate."
  - "This is not supposed to happen."
  - "If you can satisfy any kill condition, this paper is falsified. I will publicly acknowledge the refutation."

- ATTENTION_DROPS:
  - The abstract stacks many numbers before the reader has a mental map. Quick fix: add one sentence that says what is being measured before listing p-values and decay constants.
  - The paper moves from `chi` normalization into curve fitting quickly. Quick fix: add a compact variable legend after the first equation.
  - The counts shift between 45 surveyed, 23 sufficient, and 16 fitted domains. Quick fix: add a small "surveyed / analyzed / fitted" count note near Methods.
  - "This is not a metaphor" is rhetorically strong but may trigger resistance. Quick fix: preserve the boldness while adding the proof boundary in the next sentence.

- JARGON_BOTTLENECKS:
  - "Coherence Index" | Reader risk: sounds like a finished accepted metric. | Simpler doorway: "a proposed 0-1 score for how well a social system's parts still hold together."
  - "lambda" | Reader risk: symbol without intuition. | Simpler doorway: "the decay rate, or how fast coherence is falling."
  - "t0" | Reader risk: opaque notation. | Simpler doorway: "the estimated turning-point year."
  - "K-S test" | Reader risk: unexplained statistical authority. | Simpler doorway: "a test of whether the parameter cluster looks random."
  - "Lindbladian master equation" | Reader risk: highest cognitive load. | Simpler doorway: "a standard equation family for coherence loss in open physical systems."
  - "Biaxiosum" and "FACTS Format" | Reader risk: internal method terms can distract from the data. | Simpler doorway: define once and return immediately to the paper's proof burden.

- RHYTHM_FIXES:
  - Add a one-paragraph "what this paper proves / does not prove" bridge before the Methods section.
  - Keep the "What This Paper Does NOT Claim" section close to the Lindbladian comparison so the strongest claim is immediately bounded.
  - Convert the domain-source list into a compact table or bullets with one example each.
  - Move the kill conditions higher in the reader's awareness by previewing them in the introduction.

- OPENING_REWRITE:
  - "America's decline is usually argued one domain at a time: family, religion, trust, economics, language, mental health. This paper asks a different question. If those domains were truly independent, their declines should not share the same curve, timing, and decay form. Here I test whether they do."

---

