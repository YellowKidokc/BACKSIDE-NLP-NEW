# Axiom + 7Q Station Status

Run time: 2026-05-14 04:49 Central

Station root:

```text
\\dlowenas\brain\paper-proof-grader\OUTPUT\station-runs\axiom-7q-20260514_044911
```

Batch index:

```text
\\dlowenas\brain\paper-proof-grader\OUTPUT\station-runs\axiom-7q-20260514_044911\batch-index.md
```

## Stations Tried

```text
axiom_map
7q_forward
7q_reverse
```

## Results

| Paper | Claims | Avg 7Q Forward | Reverse Summary |
|---|---:|---:|---|
| 01-RESONANT-COUPLING-HYPOTHESIS-RCH | 21 | 3.24/7 | 12 FAIL_REVIEW, 5 WEAKENED, 4 SURVIVES_WITH_REPAIRS |
| 02-REGISTERED-REPORT-MVE-QRNG | 21 | 2.90/7 | 12 FAIL_REVIEW, 5 WEAKENED, 4 SURVIVES_WITH_REPAIRS |
| 03-THE-FOURFOLD-NATURE-OF-TRUTH | 3 | 3.33/7 | 2 FAIL_REVIEW, 1 SURVIVES_WITH_REPAIRS |
| 04-TURTLES-TERMINAL-NODE-HYPOTHESES | 9 | 2.22/7 | 8 FAIL_REVIEW, 1 WEAKENED |

## /PROBE Read

This was a deterministic smoke test, not final reasoning.

It proves the three station lanes can now read paper-grader claim audits and produce review artifacts.

It also exposes the next fixes:

- claim splitting is still too rough
- equations are sometimes treated as claims without enough context
- many failures are caused by missing explicit mechanism/evidence/kill-condition markers
- some text has encoding damage from older source files
- axiom matching is keyword/concept matching, not yet canonical Postgres/Lean-backed mapping

## Next Step

Use `02-REGISTERED-REPORT-MVE-QRNG` as the first serious repair target. It has the best empirical shape, but the station says its claims need clearer per-claim mechanisms and explicit failure cases.
