# Calibration Test — Expected Outputs

Use this to validate your lane's output before running GTQ-03.
Input: `00_DROP/CALIBRATION_pilot-preflight-checklist.md`

## Expected Semantic Address

```
AVIATION/PILOT_PRE_FLIGHT_CHECKLIST/F/TEAM/I/R4
```

Components:
- D = AVIATION (domain)
- N = PILOT_PRE_FLIGHT_CHECKLIST (named entity)
- V = F (state: final)
- A = TEAM (audience)
- U = I (use: informational/instructional)
- R = R4 (risk: life-critical)

## Expected Semantic Vector

```
G3M3E0S0T3K3R3Q0F0C0
```

- G=3 — operational authority, go/no-go rules
- M=3 — procedural, action-based
- E=0 — clean, ordered, not fragmented
- S=0 — not about selfhood or inner life
- T=3 — must be completed in sequence
- K=3 — structured checklist information
- R=3 — coordinates aircraft, crew, instruments, safety, authorization
- Q=0 — not subjective or felt-experience
- F=0 — not trust/faith/commitment under uncertainty
- C=0 — coherent but synthesis is not dominant function

## Expected Hash

```
[G·Q][K·S][M·F][T·C][R·E]
```

Logic: Dominant = G,K,M,T,R. Absent = E,C,F,S,Q.
Tie-break order: E→C→G→K→M→T→R→F→S→Q.

## Expected Claim Archaeology

```
surface_claim: This checklist ensures aircraft, crew, instruments, fuel, communication systems, and safety controls are ready before flight.
buried_claim: Flight safety depends on completing standardized checks before takeoff.
operational_claim: Each checklist item must have a pass/fail state.
rhetorical_load: low
domain_shift: none
domain_badges: AVIATION, SAFETY, PROCEDURE
```

## Expected Kill Condition

```
stated_kill: checklist fails if pilots cannot determine whether a required safety item passed or failed
implicit_kill: checklist fails if items are ambiguous, unordered, or not actionable
testable_kill: yes
rhetorical_armor: low
```

## Expected Four-Score Dashboard

```
Academic_Readiness: C
Framework_Coherence: A
Public_Communication: A
Risk: R4 / HIGH
```

## Drift Detection

If your lane produces C=3 on the vector, that's drift. A checklist is organized but synthesis is not its dominant function.

If your lane cannot produce an address, vector, or hash from this test article, your lane is not wired to the addressing system yet. Flag it as blocked and say what's missing.

## Per-Lane Expected Outputs

| Lane | Expected Output for Calibration Article |
|------|----------------------------------------|
| 01_LOSSLESS | Clean markdown, no HTML artifacts, preserved structure |
| 02_SECTION_MAP | 4 sections: intro, checklist, kill condition, risk. Stable section_ids |
| 03_YAML_METADATA | domain=AVIATION, state=F, audience=TEAM, risk=R4 |
| 04_TAGS | G3M3E0S0T3K3R3Q0F0C0 vector, semantic address |
| 05_CLAIMS | 1 surface claim, 1 buried claim, 1 operational claim, low rhetorical load |
| 06_CONTRADICTIONS | 0 contradictions (clean document) |
| 07_MATH_TRANSLATION | No equations found (null output is correct) |
| 08_SECTION_VECTORS | 4 section embeddings |
| 09_GRAPH_LINKS | Edges: checklist→kill_condition, checklist→risk |
| 10_RIGOR | High readiness, no kill conditions triggered |
