# 04_TAGS — Calibration Page Tag Summary

**Source:** `00_DROP/CALIBRATION_pilot-preflight-checklist.md`
**Worker:** claude-code-worker-2
**Run:** 2026-05-22T20:00:00Z
**Provenance:** mocked (upstream 02/03 not yet produced)

## Semantic address

`AVIATION/PILOT_PRE_FLIGHT_CHECKLIST/F/TEAM/I/R4 :: G3M3E0S0T3K3R3Q0F0C0 :: G3-Q0-K3-S0-M3-F0-T3-C0-R3-E0`

Status: **MOCKED** (no lane-02 address to compare against this round). Vector recomputed locally matches the expected calibration vector exactly.

## Dominant chi vars

`chi_G`, `chi_M`, `chi_T`, `chi_K`, `chi_R` — five of ten, all binary 3.

Absent: `chi_E`, `chi_S`, `chi_Q`, `chi_F`, `chi_C`. C is 0 because the article is coherent but not synthesizing — checklist organization ≠ synthesis. If a future run produced C=3 the prompt drifted.

## Dominant Laws

None. Calibration article is not a Theophysics document — no Law_1…Law_10 tags expected or emitted.

## Domain badges

`AVIATION`, `SAFETY`, `PROCEDURE`.

## Workflow tags

`calibration-input` (page), `operational` (sec_02), `kill-condition` (sec_03).

## Drift status

No drift. Recomputed vector matches `configs/CALIBRATION_EXPECTED.md` exactly. No loopback artifact needed.

## Next test

`00_DROP/gtq-03-free-will-two-frames.html`. Different domain (THEOPHYSICS), different expected vector profile, expect rich Law_X coverage and chi_F / chi_C populated.
