# First Workflow Station Map

**Workflow:** `first-article.workflow`  
**Purpose:** make the first X-drive packet path operational without copying station logic into every workflow.

## Working Chain

```text
Markdown / HTML / image
-> conversion
-> executive-summary
-> overview
-> math-layer
-> image-notes
-> lossless-context
-> manifest
```

## Station Status

| Station | Current implementation | Status | Notes |
|---|---|---|---|
| conversion | `Backside/conversion_lib` | wired | HTML and text work; PDF/DOCX depend on MarkItDown availability. |
| executive-summary | `Backside/station_lab/paper_grader_station_lab.py` | wrapped | Produces accessible, medium, and academic layers. |
| overview | `Backside/station_lab/paper_grader_station_lab.py` | wrapped | Produces section map, signals, tuning questions. |
| math-layer | `Backside/station_lab/paper_grader_station_lab.py` | wrapped | Extracts equations/statistics/math language. |
| image-notes | `first-article.workflow/pipeline.py` | first pass | Metadata, dimensions, alt/title, nearby quote. No true vision model yet. |
| lossless-context | `Backside/lossless_context_pipeline` | wired | Produces permanent address, vector, hash, JSON, HTML. |
| semantic-space | `Backside/lossless_context_pipeline/vector_space.py` | separate batch pass | Best after multiple artifacts exist. |

## Honest Boundary

The image station can describe **known context** around a picture. It cannot yet see the picture semantically. That means it can say:

```text
alt/title/caption + dimensions + file identity + quote context
```

It should not claim:

```text
actual scene understanding
```

until a vision-caption model is added.

## Next Stations To Promote

1. `image-caption.station` - true local or API vision captioning.
2. `claim-extract.station` - split from lossless/context into reusable claim-only output.
3. `evidence-bridge.station` - citation/tested thing/claim bridge.
4. `contradiction-scan.station` - DeBERTa/NLI pass over extracted claims.
5. `semantic-space.station` - batch projection and neighborhood output.

