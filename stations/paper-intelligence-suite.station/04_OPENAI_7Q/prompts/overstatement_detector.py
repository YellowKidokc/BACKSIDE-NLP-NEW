"""
OVERSTATEMENT DETECTOR — rhetorical strength vs evidence strength.

Fills: snapshot.overstatement: OverstatementDetector

When prose intensity outruns evidence backing, the paper is oversold.
This isn't a moral failure — it's a calibration problem the author should
know about before publication.
"""
from ._runner import call_openai_json

SECTION_NAME = "overstatement_detector"
SCHEMA_TARGET = "OverstatementDetector"
MODEL = "gpt-4o-mini"
TEMPERATURE = 0.2

SYSTEM_PROMPT = """You measure the gap between how strongly a paper TALKS
about its claims and how strongly its evidence actually supports them.

Look for: superlatives, certainty markers ("proves", "demonstrates", "definitively"),
sigma claims that don't survive scrutiny, "obviously" / "clearly" used when the
point isn't obvious, claims of universality from local results, language that
treats analogy as identity.

A paper can be confident and well-calibrated. The issue is only when the
language outruns the backing. Quote the worst examples directly."""

USER_PROMPT_TEMPLATE = """Detect overstatement in this paper.

Procedure:
1. Identify passages where the rhetoric is notably stronger than the
   evidence backs. Quote them. List up to 8.
2. Score rhetorical_strength_index 0-1: how forceful is the prose overall?
   (Conservative academic = 0.2; aggressive certainty = 0.9)
3. Score evidence_strength_index 0-1: how strong is the actual evidence
   for the central claims?
4. delta = rhetorical_strength_index - evidence_strength_index.
   Positive delta means oversold; negative means undersold.
5. severity:
   - "none" if delta < 0.1
   - "mild" if 0.1 <= delta < 0.25
   - "moderate" if 0.25 <= delta < 0.45
   - "severe" if delta >= 0.45

PAPER CONTENT:
{content}

Respond as JSON: {{"overstated_passages": ["quoted passage", ...], "rhetorical_strength_index": 0.0, "evidence_strength_index": 0.0, "delta": 0.0, "severity": "none|mild|moderate|severe", "ai_confidence": "low|medium|high"}}"""

EXPECTED_JSON_SHAPE = {
    "overstated_passages": ["string"],
    "rhetorical_strength_index": 0.0,
    "evidence_strength_index": 0.0,
    "delta": 0.0,
    "severity": "none|mild|moderate|severe",
    "ai_confidence": "medium",
}


def run(content: str, client) -> dict:
    return call_openai_json(
        client,
        model=MODEL,
        system=SYSTEM_PROMPT,
        user=USER_PROMPT_TEMPLATE.format(content=content),
        temperature=TEMPERATURE,
        max_tokens=1500,
    )
