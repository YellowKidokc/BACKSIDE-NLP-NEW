# Semantic Address And Routing

Purpose: connect the file naming system / semantic filing idea to the HTML article workflow.

## Core Principle

The semantic address identifies what the artifact is.

The audit grade, defensibility score, or readiness score attach as metadata and should not become the permanent filename.

## Address Shape

Working shape from the prior naming conversation:

`D/N/V/A/U/R :: VECTOR :: HASH`

Where:

- `D` = Domain
- `N` = Named Entity
- `V` = Version / State
- `A` = Audience / Access
- `U` = Use / Direction
- `R` = Risk

And the vector layer uses the ranked artifact variables.

## Workflow Use

The categorization/routing lane should produce:

- structural classification
- semantic address candidate
- YAML fields
- naming recommendation
- destination bucket

## Canon Routing Fields

At minimum:

```json
{
  "primary_bucket": "01_CANON|02_THEORIES|03_SERIES|04_FRAMEWORKS|05_EVIDENCE|06_DRAFTS|07_PUBLISH|08_ARCHIVE|09_MEDIA",
  "secondary_bucket": "",
  "type": "paper|note|axiom|claim|evidence|dashboard|story",
  "story_flag": true,
  "series": "",
  "website_layers": [
    "reader",
    "academic",
    "accessible",
    "lossless_ai"
  ]
}
```

## Important Call

`story` should remain explicit. If it is not explicit, the system will confuse narrative or series-facing content with generic papers or notes.
