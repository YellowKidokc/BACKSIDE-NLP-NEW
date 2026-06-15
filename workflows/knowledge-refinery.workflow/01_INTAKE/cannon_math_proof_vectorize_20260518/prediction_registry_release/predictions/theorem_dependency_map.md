# Theorem Dependency Map

Registry: `PREDICTION_REGISTRY_2026-05-18.md`  
Initialized UTC: 2026-05-19T00:31:00Z

## Compiled Lean Dependency

| Lean file | Theorem | Status | Supports |
| --- | --- | --- | --- |
| `lean/ClosureTheorem.lean` | `PreservesError` | compiled | T1 closure definitions |
| `lean/ClosureTheorem.lean` | `applyOps` | compiled | finite composition |
| `lean/ClosureTheorem.lean` | `applyOps_preserves_error` | compiled | preservation under finite operation list |
| `lean/ClosureTheorem.lean` | `no_error_closed_path_to_reference` | compiled | TP-PRED-0001 directly; indirect support for T1-based predictions |

## Prediction Dependency Levels

| Prediction ID | Dependency level | Direct dependency |
| --- | --- | --- |
| TP-PRED-0001 | Lean-backed | `no_error_closed_path_to_reference` |
| TP-PRED-0002 | bridge / Shannon | T1 closure + signal/noise layer |
| TP-PRED-0003 | bridge / institutional | T1 closure + Pharisee Function |
| TP-PRED-0004 | planned Lean extension | future `TargetedOpenness.lean` |
| TP-PRED-0005 | planned Lean extension | future `RepetitionProvisionality.lean` |
| TP-PRED-0006 | bridge / coupling dynamics | future community coupling model |
| TP-PRED-0007 | bridge / openness dynamics | future hardening/openness model |
| TP-PRED-0008 | planned Lean extension | future `JusticeMercyTransform.lean` |
| TP-PRED-0009 | planned Lean extension | future `JusticeMercyTransform.lean` |
| TP-PRED-0010 | boundary / governance | no theorem dependency |
| TP-PRED-0011 | physics-adjacent bridge | `O*G(1-C)` coupling-quality interpretation; no direct Lean theorem |
| TP-PRED-0012 | human-domain / phase bridge | T1/SSB process-isomorphism; no direct Lean theorem |
| TP-PRED-0013 | biology / information bridge | coherence-preservation and Shannon layer; no direct Lean theorem |

## Rule

Do not cite planned Lean extensions as compiled proofs. Mark them as planned until they build.
