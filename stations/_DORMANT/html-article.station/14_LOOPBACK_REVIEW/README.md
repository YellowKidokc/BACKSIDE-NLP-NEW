# 14_LOOPBACK_REVIEW

Purpose: convert structural breakage, stale upstream artifacts, and low-confidence lane outputs into explicit machine-readable returns.

## Inputs

- lane-owned evidence from upstream folders
- trigger conditions and recommended fixes

## Outputs

- `loopback-review.json`
- `loopback-review.md`

## Current Wiring

- `07_MATH_TRANSLATION/run.py` writes here automatically
- downstream lanes may continue when the loopback packet explicitly says continuation is safe for the current build round
- loopback is not a dead stop by default; it is a formal return channel

## This Round

- GTQ-03 math loopback is expected because the preview report references a stale CSV path and shows fallback-only translation history
