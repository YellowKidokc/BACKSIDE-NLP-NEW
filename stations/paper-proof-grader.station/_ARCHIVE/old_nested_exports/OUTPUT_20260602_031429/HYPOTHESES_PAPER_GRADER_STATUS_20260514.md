# Hypotheses Paper Grader Status

Run time: 2026-05-14 04:46 Central

## Input Copies

Working copies were dropped into:

```text
\\dlowenas\brain\paper-proof-grader\DROP_PAPERS_HERE
```

The grader archived those working copies after processing:

```text
\\dlowenas\brain\paper-proof-grader\ARCHIVE
```

Original source remains untouched:

```text
X:\knowledge-refinery\13_SOURCE_SYSTEMS\HYPOTHESES\01_Core_Hypotheses
```

## Run Manifest

```text
\\dlowenas\brain\paper-proof-grader\OUTPUT\paper-proof-grader-run-20260514_044630.json
```

## Papers Processed

| Paper | Words | Sections | Equations | Claim Candidates |
|---|---:|---:|---:|---:|
| 01-RESONANT-COUPLING-HYPOTHESIS-RCH | 2202 | 45 | 61 | 21 |
| 02-REGISTERED-REPORT-MVE-QRNG | 2679 | 56 | 72 | 21 |
| 03-THE-FOURFOLD-NATURE-OF-TRUTH | 931 | 10 | 2 | 3 |
| 04-TURTLES-TERMINAL-NODE-HYPOTHESES | 748 | 8 | 0 | 9 |

## Output Pattern

Each paper now has:

```text
<paper-id>.paper-grade.json
<paper-id>.paper-grade.md
<paper-id>.paper-grade.html
<paper-id>.claim-audit.csv
<paper-id>.paper-grade.xlsx
```

Output folder:

```text
\\dlowenas\brain\paper-proof-grader\OUTPUT
```

Readable report mirror:

```text
O:\Vault\AI Chats\Paper Proof Grader Reports
```

## /PROBE Result

The grader ran successfully, but this is a deterministic claim-audit grader, not a final truth-score engine.

It is useful for:

- finding claim candidates
- counting equations
- identifying missing evidence markers
- surfacing missing kill conditions
- producing reviewable HTML/MD/JSON/XLSX reports

It does not yet:

- produce a single robust final paper score
- run the in-house 7Q scorer per claim
- verify math
- verify external citations
- run independent empirical/statistical checks

## Next Integration Step

Wire this output into:

```text
paper-proof-grader -> 7Q per-claim scoring -> axiom/math map -> Treaties/proof-explorer HTML
```

Best next target:

```text
02-REGISTERED-REPORT-MVE-QRNG
```

Reason: it is already closest to an empirical registered-report format.
