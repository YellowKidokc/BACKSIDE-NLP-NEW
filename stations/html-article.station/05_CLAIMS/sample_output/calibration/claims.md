# 05_CLAIMS — Calibration Claims Rollup

**Source:** `00_DROP/CALIBRATION_pilot-preflight-checklist.md`
**Worker:** claude-code-worker-2
**Run:** 2026-05-22T20:00:00Z
**Provenance:** mocked upstream (02_SECTION_MAP pending), station pass-1 skipped in sample, LLM pass-2 only

## Calibration match

| Field | Expected (from CALIBRATION_EXPECTED.md) | Emitted | Match |
|---|---|---|---|
| surface_claim | This checklist ensures aircraft, crew, instruments, fuel, communication systems, and safety controls are ready before flight. | exact | ✓ |
| buried_claim | Flight safety depends on completing standardized checks before takeoff. | exact | ✓ |
| operational_claim | Each checklist item must have a pass/fail state. | exact | ✓ |
| rhetorical_load | low | low | ✓ |
| domain_shift | none | false | ✓ |
| domain_badges | AVIATION, SAFETY, PROCEDURE | AVIATION, SAFETY, PROCEDURE | ✓ |

## Per-section rollup

### sec_01 — Intro

- **Surface:** This checklist ensures aircraft, crew, instruments, fuel, communication systems, and safety controls are ready before flight.
- **Buried:** Flight safety depends on completing standardized checks before takeoff.
- **Operational:** Each checklist item must have a pass/fail state.

### sec_02 — Checklist

- **Surface 1:** The checklist must be completed in order. If any required item fails, takeoff must stop until the issue is corrected.
- **Buried 1:** A checklist is an ordered sequence whose validity depends on every prior step having passed.
- **Operational 1:** On any failed item, takeoff is blocked until the failed item is re-verified as passing.
- **Surface 2:** Authorize takeoff only after all checks pass.
- **Buried 2:** Takeoff authorization is conditional on full checklist completion.
- **Operational 2:** Takeoff authorization is a terminal step that gates on every preceding item.

### sec_03 — Kill Condition

- **Surface:** This checklist fails if pilots cannot determine whether a required safety item passed or failed.
- **Buried:** Checklist validity requires every required item to be decidable as pass or fail.
- **Operational:** Every required item must have an explicit pass/fail state before the checklist can be marked complete.

### sec_04 — Risk

- **Surface:** Failure to complete this checklist could lead to aircraft malfunction, communication failure, or unsafe takeoff.
- **Buried:** Incomplete pre-flight verification raises operational risk in flight-critical systems.
- **Operational:** Risk is mitigated by completing every checklist item; risk pressure is measurable as the count of unverified items at takeoff.

## Distribution

- Total ClaimArchs: 5
- rhetorical_load: low=5, medium=0, high=0
- domain_shift: 0
- support_needed: 0
- station_classification: DEFINITION=4, PREDICTION=1

## Notes

Calibration article — no Theophysics claims, no Master Equation invocation, no Law_X claims, no scripture refs. Sample output structurally matches expected ClaimArch shape; downstream lanes (06_CONTRADICTIONS, 10_RIGOR) can consume as-is for shape validation. When `02_SECTION_MAP` lands, swap mocked section_ids for canonical ones and re-emit.
