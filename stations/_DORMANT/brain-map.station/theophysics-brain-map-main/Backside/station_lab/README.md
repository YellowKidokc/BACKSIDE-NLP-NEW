# Paper Grader Station Lab

**What this is:** A safe tuning bench for individual paper-grader stations before they are chained into a full workflow.
**Owner:** shared
**Status:** experimental
**Last updated:** 2026-05-16

This lab keeps final human-readable exports separate from internal state.

Final readable outputs go to:

```text
X:\EXPORTS\paper-grader-station-lab\<run_id>\
```

Intermediate JSON/state goes to:

```text
X:\Backside\_state\station-lab\<run_id>\
```

## Current stations

- `executive-summary` - concise decision-grade summary of one paper or article.
- `overview` - structured reader orientation with sections, strengths, gaps, and next edits.
- `math-layer` - extracts equations/math-like statements into a structured Markdown layer.
- `all` - runs the current three stations together.

## Run

```powershell
python .\Backside\station_lab\paper_grader_station_lab.py --input "X:\paper-proof-grader\INPUT\GTQ_01_Why_Time_Is_Grace.md" --station all
```

No source files are modified.
