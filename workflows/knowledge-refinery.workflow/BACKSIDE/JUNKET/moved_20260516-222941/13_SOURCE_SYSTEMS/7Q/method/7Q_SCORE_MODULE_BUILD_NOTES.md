# 7Q Score Module — Build Notes for Developer

## What You're Building
A drop-in Python module (`7q_score_module.py`) that adds 7 epistemic dimension scores to the existing Truth Engine pipeline.

## Architecture Match
Follow the EXACT pattern of `truth_coherence_scanner.py` at:
`O:\_Theophysics_v4\00_SYSTEM\01_ENGINE\truth_coherence_scanner.py`

That file already has: CLAIM_TERMS, EVIDENCE_TERMS, FALSIFY_TERMS, DEPENDENCY_TERMS, HEDGE_TERMS, BRIDGE_TERMS, FRUITS_LEXICON, ANTI_FRUITS_LEXICON. Same pattern — keyword sets, density scoring, dataclass output.

## The Gap Analysis (what's missing)

| 7Q Dimension | Current Coverage | Gap |
|---|---|---|
| Q7 Kill Conditions | Grace Layer (boolean only) | Needs density scoring |
| Q6 Consequences | Partial in Grounding | No forced prediction detection |
| Q5 Foundations | Grounding score | No depth-tracing (axiom vs assertion vs circular) |
| Q4 Evidence (PS×ED×EC) | Grounding = PS only | ED and EC channels completely missing |
| Q3 Claim Precision | Not scored | No hedging-vs-precision metric |
| Q2 Cross-Domain | Not scored | No isomorphism/generalization detection |
| Q1 Identity Clarity | Not scored | No claim-type classification |

## The Critical Formula (Why-Penalty)

```
CF = (0.5 + 0.5 × ED) × (0.5 + 0.5 × EC)
E_final = PS × CF
```

If ED = 0, evidence capped at 50%. This is the key addition.

## Integration

```
T_enhanced = T_v3 × (0.6 + 0.4 × 7Q_score)
```

Zero 7Q markers = 60% of truth score. Full 7Q = 100%.

## Fruits Mapping

- Q7 (falsifiability) → Faithfulness booster
- Q4 (evidence discipline) → Self-control booster  
- Q6 (consequences) → Goodness booster
- Q5 (foundations) → Patience booster

## Full Spec
Read: `C:\Users\lowes\Desktop\Opus Web Building Kit\7Q_ENGINE_SPEC.md`
Read: `O:\_Theophysics_v4\05_EVIDENCE_ENGINE\EVIDENCE_CLASSIFICATION_PROTOCOL.md`

## Note on ED Channel
Keyword matching will catch explanation vocabulary but not actual explanations. Consider a semantic layer (sentence-level NLI or embedding similarity to known mechanistic patterns) for ED if you want depth beyond surface markers. Start with keywords, upgrade later.
