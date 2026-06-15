# GTQ Series Stress Run Report

**Date:** 2026-05-20  
**Workflow:** `first-article.workflow`  
**Corpus:** root Genesis-to-Quantum production HTML files

## Source

```text
\\dlowenas\HPWorkstation\Desktop\Master HTMl\K-Production-Ready\02-genesis-to-quantum
```

Filtered to clean root files:

```text
gtq-*.html matching ^gtq-\d{2}-.+\.html$
```

This excludes `OLD`, `New Folder`, backup files, index pages, and tangent pages.

## Batch Output

```text
X:\EXPORTS\first-article-workflow-series\20260520-155258-gtq-root-series
```

## Result

```text
Files: 26
Passed: 26
Failed: 0
```

GTQ-01 initially failed because the HTML title/frontmatter path carried a control character that YAML rejected. The workflow now sanitizes generated YAML frontmatter scalars before lossless parsing. GTQ-01 passed after rerun.

## Vector Distribution

```text
14 x G3M3E0S0T3K3R3Q0F3C3
11 x G3M3E3S0T3K3R3Q0F3C3
 1 x G3M0E0S0T3K3R3Q0F0C0
```

The `E3` cluster should be reviewed as calibration pressure. Some may be legitimate artifact disorder/collapse emphasis, but some may still be topic drift from dark/broken subject language.

## Semantic Space

Generated:

```text
X:\EXPORTS\first-article-workflow-series\20260520-155258-gtq-root-series\semantic-space\semantic-space.csv
X:\EXPORTS\first-article-workflow-series\20260520-155258-gtq-root-series\semantic-space\semantic-space.json
```

## Series Stack

Generated:

```text
X:\EXPORTS\first-article-workflow-series\20260520-155258-gtq-root-series\STACK
```

Files:

```text
simple-summary.md
cumulative-executive-summary.md
lossless-series-index.md
cumulative-math-translation.md
contradiction-scan.md
series-paper-draft.md
stack-manifest.json
```

Stack result:

```text
Articles: 26
Math candidates: 1215
Contradiction flags: 15
```

Boundary: contradiction scan is heuristic and expected to overflag. Math candidates are broad and include math-flavored prose; next refinement should split equations from formal claims and prose signals.

## Durable Runner

Added:

```text
Backside\workflows\first-article.workflow\RUN_GTQ_ROOT_SERIES.bat
Backside\workflows\first-article.workflow\RUN_STACK_GTQ_SERIES.bat
```
