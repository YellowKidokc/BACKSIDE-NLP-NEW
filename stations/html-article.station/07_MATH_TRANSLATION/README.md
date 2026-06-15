# 07_MATH_TRANSLATION

Purpose: extract every article equation, preserve the raw math, generate a provisional plain-English translation, and surface loopback conditions instead of hiding them in chat.

## Inputs

- `00_DROP/*.html` or `00_DROP/*.md`
- optional upstream preview artifact such as `*-MATH-PREVIEW-report.json`
- optional later semantic address/routing output from the categorization lane

## Outputs

- `math-payload.json`
- `math-translation.md`
- `math-snippets.html`
- loopback sidecars in `../14_LOOPBACK_REVIEW/` when structural gaps are detected

## Wrapper Strategy

- prefer existing preview/report artifacts if they exist for the same page
- do not block if preview support files are stale or missing
- regenerate structural math extraction directly from the source article
- keep confidence explicit because math translation is revisitable, not final authority

## Current Round Notes

- calibration expectation for `CALIBRATION_pilot-preflight-checklist.md`: no equations found
- GTQ-03 currently has a desktop preview report but the CSV/table path in that report is stale
- stale preview dependencies are recorded as loopback, not treated as hard blockers

## Run

```powershell
python .\run.py --input ..\00_DROP\gtq-03-free-will-two-frames.html --output-dir . --loopback-dir ..\14_LOOPBACK_REVIEW
python .\run.py --input ..\00_DROP\CALIBRATION_pilot-preflight-checklist.md --output-dir .\sample_output\calibration --loopback-dir ..\14_LOOPBACK_REVIEW\sample_output\calibration
```
