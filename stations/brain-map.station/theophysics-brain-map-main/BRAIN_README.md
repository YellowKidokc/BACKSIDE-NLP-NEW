# X Drive Front Door

Use this root as the Brain front door, not the runtime shelf.

## Target Visible Root

```text
X:\
  David\
  GUI\
  Conversions\
  EXPORTS\
  Backside\
  README.md
  ARCHITECTURE.md
  THEOPHYSICS_PRIMER.md
  RUN_*.bat
```

## Human Front Door

```text
X:\David
```

Human-facing maps, notes, session entrypoints, and material David opens directly.

## GUI

```text
X:\GUI
```

User-facing dashboards and control panels. The first promoted app is the Brain Dashboard currently represented in the repo at:

```text
theophysics-brain-map\Backside\brain_dashboard
```

Runtime target:

```text
X:\GUI\brain-dashboard
```

## Conversions

```text
X:\Conversions
```

The front door for format conversion: HTML, Markdown, text, URL text, audio/video when Whisper is available, OCR when installed, and future "convert it to anything" lanes.

The current implementation lives in the repo at:

```text
theophysics-brain-map\Backside\conversion_lib
```

Runtime target:

```text
X:\Conversions\conversion-layer
```

Finished conversion outputs still go to:

```text
X:\EXPORTS\conversion-layer
```

## Finished Outputs

```text
X:\EXPORTS
```

Finished human-readable outputs stay here: Markdown, HTML, Excel, PDFs, prompt packs, reports, galleries, and other deliverables that should be easy to find.

## Backside

```text
X:\Backside
```

The workhorse layer: workflows, models, services, apps, stations, control-plane repos, archives, logs, machine state, and data folders that David does not need to open constantly.

Target runtime lanes:

```text
X:\Backside\workflows
X:\Backside\_models
X:\Backside\_state
X:\Backside\control-plane
X:\Backside\corpus
X:\Backside\services
```

## One-Click Workflow

```text
X:\RUN_PUBLIC_ARTICLE_REFINERY.bat
X:\RUN_FAP_ARTICLE_PIPELINE.bat
```

Root-level click buttons may remain while they call into Backside/Conversions/GUI paths.

## Root Cleanup Contract

Old root workflow paths are transitional compatibility paths only. They should not be treated as the target architecture.

Root cleanup contract:

```text
ROOT_REORG_TARGET_2026-05-20.md
Backside\ROOT_REORG_MOVE_MAP_2026-05-20.csv
```
