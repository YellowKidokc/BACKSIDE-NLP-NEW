# Chi Tagging Workflow Run Report

**Date:** 2026-05-20  
**Workflow:** `chi-tagging.workflow`  
**Purpose:** split canon indexing into separate stations so Postgres chi-variable tagging has a stable reference layer.

## Stations Added

| Station | Canon scope |
|---|---|
| `master-equation-canon.station` | Master Equation, formal layer, test stack, axiom derivation |
| `trinity-canon.station` | Resurrection, Maxwell/Trinity, Lean isomorphism |
| `fruits-spirit-canon.station` | Fruits of Spirit and equations |
| `operators-canon.station` | Grace, Justice/Mercy, Grace-in-data |

All four use the shared deterministic indexer:

```text
Backside\stations\_shared\canon_index.py
```

## Test Run

```powershell
python Backside\workflows\chi-tagging.workflow\pipeline.py --export-root X:\EXPORTS\chi-tagging-test --state-root X:\Backside\_state\chi-tagging-test
```

Output:

```text
X:\EXPORTS\chi-tagging-test\20260520-154907
```

Result:

```text
Tagged blocks: 791
Equations: 360
Sources: 13
Needs review detections: 1243
```

Variable counts:

```text
G: 260
M: 188
E: 131
S: 105
T: 134
K: 238
R: 192
Q: 29
F: 68
C: 167
```

## Boundary

This is not the final Postgres writeback. It is the canon reference index and evidence layer.

Next workflow should use this aggregate to tag:

1. `public.cross_domain`
2. `framework_topology.canonical_axioms`
3. `framework_math.equation_terms`

