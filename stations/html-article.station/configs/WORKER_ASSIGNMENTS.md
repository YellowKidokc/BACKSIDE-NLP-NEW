# Worker Assignments — Wave 1

These are the per-worker comms messages to post. Each worker gets ONE lane.
David posts each to the appropriate worker channel on comms.
Worker reads dispatch prompt + their assignment + goes.

## How to Deploy

1. Drop a copy of GTQ-03 HTML into `X:\Backside\workflows\html-article.workflow\00_DROP\`
2. Post the master dispatch prompt to workflow-4 (or link to the file)
3. Post each worker assignment below to the worker's channel
4. Worker reads their channel, reads WORKER_DISPATCH.md, starts

## Wave 1 — Parallelizable Lanes (6 workers)

These can all start simultaneously. Each mocks its upstream input from the raw GTQ-03 drop.

### Worker 1 → Lane 01 + 02 (Lossless + Section Map)
```
ASSIGNMENT: Lanes 01_LOSSLESS and 02_SECTION_MAP (bundled — 02 needs 01 output)

Station: section-splitter.station (X:\Backside\stations\section-splitter.station)
Also check: brain-map.station lossless_context_pipeline (has calibration data for GTQ-03)

Your job:
- Take raw HTML from 00_DROP
- Extract clean canonical text (lossless — no interpretation)
- Detect headings, hierarchy, equations, citations
- Assign stable section_id values
- Emit: lossless.md, section_map.json

Read WORKER_DISPATCH.md at X:\Backside\workflows\html-article.workflow\prompts\WORKER_DISPATCH.md
Produce deliverables in both 01_LOSSLESS/ and 02_SECTION_MAP/
```

### Worker 2 → Lane 03 (YAML Metadata)
```
ASSIGNMENT: Lane 03_YAML_METADATA

Station: metadata-extractor.station (X:\Backside\stations\metadata-extractor.station)

Your job:
- Read section_map.json from 02 (mock from raw HTML if 02 not ready)
- Extract page-level metadata (title, author, series, date, law references, chi variables)
- Extract section-level metadata
- Emit: page_metadata.yaml, section_metadata.json

Read WORKER_DISPATCH.md at X:\Backside\workflows\html-article.workflow\prompts\WORKER_DISPATCH.md
```

### Worker 3 → Lane 04 (Tags)
```
ASSIGNMENT: Lane 04_TAGS

Station: 7q-classifier.station (X:\Backside\stations\7q-classifier.station)
Also check: chi-tagging.workflow

Your job:
- Read section_map from 02 (mock if needed)
- Attach semantic tags: which of the 10 Laws, which chi variables, which axioms
- Attach workflow tags: needs-math, needs-rigor, needs-citation
- Emit: tags.json (page-level + section-level)

Read WORKER_DISPATCH.md at X:\Backside\workflows\html-article.workflow\prompts\WORKER_DISPATCH.md
```

### Worker 4 → Lane 05 (Claims)
```
ASSIGNMENT: Lane 05_CLAIMS

Station: claim-extractor.station (X:\Backside\stations\claim-extractor.station)

Your job:
- Read section_map from 02 (mock if needed)
- Extract explicit claims per section
- Extract implied claims per section
- Flag claims that need evidence support
- Emit: claims.json

The station has extract.py and config.json already. Use them.

Read WORKER_DISPATCH.md at X:\Backside\workflows\html-article.workflow\prompts\WORKER_DISPATCH.md
```

### Worker 5 → Lane 07 (Math Translation)
```
ASSIGNMENT: Lane 07_MATH_TRANSLATION

Station: math-layer.station (X:\Backside\stations\math-layer.station)

SPECIAL RULE: This lane is REVISITABLE, not final authority. Tag everything with confidence.

Your job:
- Find all equations in the article
- Parse raw math (LaTeX, MathJax, inline)
- Translate each equation to plain English
- Preserve raw math alongside translation
- Tag confidence per translation
- If translation seems structurally wrong, write to 14_LOOPBACK_REVIEW
- Emit: math_translations.json

The station is app-shaped (TypeScript + Python). Read its docs before rebuilding anything.
Templates exist: college-prompt.txt, doctorate-prompt.txt, summary-prompt.txt

Read WORKER_DISPATCH.md at X:\Backside\workflows\html-article.workflow\prompts\WORKER_DISPATCH.md
```

### Worker 6 → Lane 08 (Section Vectors)
```
ASSIGNMENT: Lane 08_SECTION_VECTORS

Station: sbert-embedder.station (X:\Backside\stations\sbert-embedder.station)

Your job:
- Read section_map from 02 (mock if needed)
- Embed every section using SBERT
- Emit: vectors.json (section_id + vector payload + metadata)

The station has sbert_runner.py and config.json. Use them.

Read WORKER_DISPATCH.md at X:\Backside\workflows\html-article.workflow\prompts\WORKER_DISPATCH.md
```

## Wave 2 — After Wave 1 Outputs Land (2-3 workers)

### Worker 7 → Lane 06 (Contradictions)
Needs: claims.json from Lane 05
Station: deberta-runner.station

### Worker 8 → Lane 10 (Rigor)
Needs: claims + contradictions + math translations
Station: 7q-classifier.station + paper-proof-grader

### Worker 9 → Lane 09 (Graph Links)
Needs: tags + claims + vectors
Station: graph-linker.station

## Lanes That Are Assembly (Not Station Work)

These don't need dedicated workers until Wave 1+2 outputs exist:
- 11_HTML_RENDER — Kimi authority
- 12_EXPORTS — postgres-sync + brain-map
- 13_LAYER_LEDGER — orchestration script
- 14_LOOPBACK_REVIEW — receives from others
- 15_SECTION_PACKETS — bundler
- 16_FINAL_PAGE_ASSEMBLY — combines everything
- 17_PUBLISH_READY — terminal

## The Goal

One end-to-end GTQ-03 run. Wave 1 workers produce their outputs.
Wave 2 workers consume those outputs.
Assembly lanes stitch it together.
David reviews the final page.
