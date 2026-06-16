# Peer-Review Prompt Library

Each `*.py` file here is one focused, single-purpose OpenAI prompt that fills exactly one section of the master `ProofExplorerSnapshot` schema (`lib/snapshot_schema.py`).

## Why one prompt per section

Monolithic prompts produce shallow generic work. One-purpose prompts produce focused, comparable, debuggable output. If a section's quality drops, you fix one prompt â€” not unscramble a 2000-token mega-response.

## House style (every prompt file follows this shape)

```python
SECTION_NAME = "claim_inventory"              # matches schema field
SCHEMA_TARGET = "list[Claim]"                 # what this fills
MODEL = "gpt-4o-mini"                         # cheap default; bump per-prompt if needed
TEMPERATURE = 0.2                             # low; we want stable structured output

SYSTEM_PROMPT = """..."""                     # role + posture, ~100 words

USER_PROMPT_TEMPLATE = """...
PAPER CONTENT:
{content}

Respond as JSON with shape: {expected_shape}
"""

EXPECTED_JSON_SHAPE = {...}                   # the literal dict shape we expect

def run(content: str, client) -> dict:
    """Call OpenAI, return the parsed JSON dict.
    Errors become {"error": str, "section": SECTION_NAME}.
    """
    ...
```

## Running

```python
from prompts._runner import run_all
from openai import OpenAI

client = OpenAI()
snapshot_sections = run_all(paper_text, client)   # dict keyed by SECTION_NAME
```

Or run a single section:

```python
from prompts.claim_inventory import run as run_claims
result = run_claims(paper_text, client)
```

## The sections

| File                          | Section in schema           | Status |
|-------------------------------|------------------------------|--------|
| `claim_inventory.py`          | `claim_inventory: list[Claim]` |        |
| `equation_audit.py`           | `equations: list[EquationEntry]` |    |
| `assumption_stack.py`         | `assumptions: AssumptionStack` |      |
| `kill_conditions.py`          | `kill_conditions: list[KillCondition]` | |
| `evidence_map.py`             | `evidence_map: list[EvidenceEntry]` |  |
| `physics_comparison.py`       | `physics_comparison: list[PhysicsComparison]` | |
| `novelty_classification.py`   | `novelty: NoveltyClassification` |    |
| `coherence_score.py`          | `coherence: CoherenceScore` |          |
| `overstatement_detector.py`   | `overstatement: OverstatementDetector` | |
| `revision_plan.py`            | `revision: RevisionPlan` |             |
| `spine_analysis.py`            | `spine_analysis: dict` | GTQ question-answer spine |

## Style rules

1. **No "great question" / "fascinating insight" language** in system prompts. Posture is rigorous-analyst, not flatterer.
2. **Every prompt MUST end with the literal expected JSON shape**. `response_format={"type": "json_object"}` enforces JSON but not shape â€” the shape spec is what makes outputs comparable.
3. **Fields use the schema's enum literals exactly**. If schema says `"core" | "support" | "rhetorical"`, the prompt must list those exact strings.
4. **Truncate content at 8000 chars** if longer (keep first 6000 + last 2000). Most signal is at start/end.
5. **`ai_confidence` field on every section that has one** â€” `low | medium | high`. Default `medium`. If the paper is too short or too vague to extract reliably, return `low`.

## Adding a new prompt

1. Create `<section_name>.py` matching the house style above.
2. Add the field to `lib/snapshot_schema.py`.
3. Register it in `_runner.py`'s `ALL_PROMPTS` list.
4. The orchestrator and Excel/HTML writers pick it up automatically once the schema knows about it.

