# Series Flow Auditor Workflow

Purpose: audit whether an ordered article series functions as an argument.

This is **Pass 1: Deterministic NLP Auditor**. More precisely, it is structural-document intelligence: repeatable rules that expose likely sequence failures before a higher-judgment LLM or human editorial pass.

It does not rewrite articles and does not judge whether the thesis is true. It tests sequence coherence:

```text
Could a reader understand and believe this article if they had only read the previous articles in the sequence?
```

## Inputs

Preferred:

```text
python scripts\series_flow_auditor.py --series-dir "PATH_TO_ARTICLES" --out "PATH_TO_OUTPUT"
```

Supported source files:

- `.html`
- `.htm`
- `.md`
- `.txt`
- `.json` with `title`, `body`, `summary`, `claims`, or `evidence`

Optional manifest:

```text
python scripts\series_flow_auditor.py --manifest "series_manifest.json" --out "PATH_TO_OUTPUT"
```

Manifest shape:

```json
[
  {"title": "Article title", "path": "C:\\path\\article.html", "article_number": 1}
]
```

## Outputs

- `series-flow-audit.md`
- `series-flow-audit.json`
- `series-flow-audit.csv`
- `series-flow-audit.xlsx` when `openpyxl` is available

Primary table fields:

- Current Order #
- Title
- Detected Function
- Expected Function
- Concepts Used Before Defined
- Severity Flags
- Dependencies
- Suggested Placement
- Confidence
- Keep / Move / Merge / Appendix

## Function Labels

The auditor classifies each article as one of:

```text
FRAMING
DEFINITION
DOMAIN_OVERVIEW
NARRATIVE_CASE
DATA_EVIDENCE
METHOD
STATISTICAL_SYNTHESIS
CONTROL_CASE
OBJECTION_RESPONSE
PREDICTION
RECOVERY_PATH
APPENDIX
ARCHIVE
```

Default ideal order:

```text
FRAMING -> DEFINITION -> DOMAIN_OVERVIEW -> NARRATIVE_CASE -> DATA_EVIDENCE -> METHOD -> STATISTICAL_SYNTHESIS -> CONTROL_CASE -> OBJECTION_RESPONSE -> PREDICTION -> RECOVERY_PATH -> APPENDIX
```

## MDA Use

For Moral Decline / MDA, do not trust filename order blindly. Prior work found story order and metadata can drift apart. Run the workflow against a clean manifest if David provides a proposed order.

## Boundary

This workflow is not the final authority on ideal order.

Use the system as:

```text
Pass 1 - Deterministic NLP Auditor
Pass 2 - LLM Series Sequence Auditor
Pass 3 - Human Editorial Judgment
```

Pass 1 says: "Here are likely structural violations."

It does not say: "Here is the perfect order."

The perfect order requires judgment because a public series is not just logic. It is also reader formation.
