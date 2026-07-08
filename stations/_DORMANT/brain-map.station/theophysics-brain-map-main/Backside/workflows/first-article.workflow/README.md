# First Article Workflow

**What this is:** the first practical X-drive workflow for an article/file packet.

It chains the reusable pieces that already exist:

```text
source
-> conversion / canonical Markdown
-> executive summary + overview + math layer
-> image notes / quote context
-> lossless context JSON + HTML + semantic tags
-> manifest
```

## Front Door

```text
X:\Backside\workflows\first-article.workflow\00_DROP
```

Drop a Markdown, text, HTML, or image file there, then run:

```text
X:\Backside\workflows\first-article.workflow\RUN.bat
```

Or run one explicit file:

```powershell
python X:\Backside\workflows\first-article.workflow\pipeline.py --input "path\to\file.html"
```

Batch a folder:

```powershell
python X:\Backside\workflows\first-article.workflow\pipeline.py --input-root "path\to\folder" --glob "gtq-*.html"
```

GTQ root-series runner:

```text
X:\Backside\workflows\first-article.workflow\RUN_GTQ_ROOT_SERIES.bat
```

Stack an already-generated batch into cumulative series outputs:

```powershell
python X:\Backside\workflows\first-article.workflow\series_stack.py --batch-root "X:\EXPORTS\first-article-workflow-series\<batch_id>"
```

Current GTQ stack runner:

```text
X:\Backside\workflows\first-article.workflow\RUN_STACK_GTQ_SERIES.bat
```

## Outputs

Final reproducible exports go to:

```text
X:\EXPORTS\first-article-workflow\<run_id>\
```

Internal state goes to:

```text
X:\Backside\_state\first-article-workflow\<run_id>\
```

## Stations

| Station | Status | Output |
|---|---|---|
| conversion | wired | `source.canonical.md` |
| executive-summary | wrapped from station lab | `stations/<run>/executive-summary.md` |
| overview | wrapped from station lab | `stations/<run>/overview.md` |
| math-layer | wrapped from station lab | `stations/<run>/math-layer.md` |
| image-notes | first deterministic pass | `image-notes.md` |
| lossless-context | wired | `lossless/*.json`, `lossless/*.html`, `lossless/*.semantic-tags.md`, `lossless/*.semantic-tags.json` |

Each lossless packet now carries a deterministic `master_equation_uuid`, the Nabla address/vector/hash, and an Obsidian-style semantic tag block. Tag rows point back to stable block IDs so the HTML snapshot, Markdown comments, and Postgres records can all reference the same claim, evidence bundle, equation, kill condition, or relationship.

## Boundary

Image notes use file metadata, dimensions, alt/title text, and nearby caption/quote context. They do not yet use a true image-caption model. That is intentional: the workflow should not pretend metadata is vision.

The cumulative math stack is a staging layer. It intentionally catches broad math-like prose and must be refined before being treated as formal equation extraction.
