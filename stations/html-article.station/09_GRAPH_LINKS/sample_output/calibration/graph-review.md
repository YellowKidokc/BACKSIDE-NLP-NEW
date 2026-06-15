# 09_GRAPH_LINKS Review - calibration

- generated: 2026-05-22T22:51:04Z
- section count: 4
- edge count: 8
- mocked claims: no
- mocked tags: no

## Top edges
- `sec-001-pilot-pre-flight-checklist` -> `sec-002-checklist` | `CLAIM_OVERLAP` | weight 1.0: Shared claim/heading vocabulary overlap = 1.000.
- `sec-002-checklist` -> `sec-003-kill-condition` | `STRUCTURAL_DEPENDENCY` | weight 0.97: Calibration expectation: checklist must connect to kill_condition via pass/fail dependency.
- `sec-002-checklist` -> `sec-004-risk` | `STRUCTURAL_DEPENDENCY` | weight 0.95: Calibration expectation: checklist must connect to risk because incomplete checks create unsafe takeoff conditions.
- `sec-001-pilot-pre-flight-checklist` -> `sec-004-risk` | `CLAIM_OVERLAP` | weight 0.8: Shared claim/heading vocabulary overlap = 0.800.
- `sec-002-checklist` -> `sec-004-risk` | `CLAIM_OVERLAP` | weight 0.8: Shared claim/heading vocabulary overlap = 0.800.
- `sec-001-pilot-pre-flight-checklist` -> `sec-003-kill-condition` | `CLAIM_OVERLAP` | weight 0.6667: Shared claim/heading vocabulary overlap = 0.667.
- `sec-002-checklist` -> `sec-003-kill-condition` | `CLAIM_OVERLAP` | weight 0.6667: Shared claim/heading vocabulary overlap = 0.667.
- `sec-003-kill-condition` -> `sec-004-risk` | `CLAIM_OVERLAP` | weight 0.5714: Shared claim/heading vocabulary overlap = 0.571.
