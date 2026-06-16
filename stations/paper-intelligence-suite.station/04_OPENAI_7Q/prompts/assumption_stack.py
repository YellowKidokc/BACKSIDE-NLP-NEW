"""
ASSUMPTION STACK — every assumption, surfaced and categorized.

Fills: snapshot.assumptions: AssumptionStack

Hidden assumptions are where most quiet failures live. Imported assumptions
are especially dangerous — papers inherit a theory's commitments silently.
"""
from ._runner import call_openai_json

SECTION_NAME = "assumption_stack"
SCHEMA_TARGET = "AssumptionStack"
MODEL = "gpt-4o-mini"
TEMPERATURE = 0.2

SYSTEM_PROMPT = """You are a structural peer reviewer extracting the full
assumption stack of a paper.

An assumption is anything the paper takes for granted that a hostile reviewer
could legitimately question. Some are stated outright. Most are not. Imported
assumptions — inherited silently from existing theories — are the most
dangerous because they hide.

Surface them all. Categorize them. Don't be charitable about hidden ones —
if the argument requires it but the paper doesn't say it, it's implicit."""

USER_PROMPT_TEMPLATE = """Extract every assumption this paper rests on, categorized.

Categories (an assumption may belong in only ONE):
- explicit: stated in the paper directly
- implicit: required for the argument but never stated
- imported: inherited from another theory (Standard Model, GR, QM, info theory, etc.)
- theological: requires a theological commitment (God, soul, scripture, etc.)
- scientific: a contested or non-trivial scientific claim taken as given
- philosophical: a metaphysical position taken as given (realism, naturalism, etc.)
- measurement: assumes a measurement is possible, valid, or invariant
- causal: assumes a causal relationship that isn't argued

Write each assumption as a short complete sentence. Aim for 1-8 entries per
category, only filling categories that actually apply.

PAPER CONTENT:
{content}

Respond as JSON: {{"explicit": [], "implicit": [], "imported": [], "theological": [], "scientific": [], "philosophical": [], "measurement": [], "causal": [], "ai_confidence": "low|medium|high"}}"""

EXPECTED_JSON_SHAPE = {
    "explicit": ["string"],
    "implicit": ["string"],
    "imported": ["string"],
    "theological": ["string"],
    "scientific": ["string"],
    "philosophical": ["string"],
    "measurement": ["string"],
    "causal": ["string"],
    "ai_confidence": "medium",
}


def run(content: str, client) -> dict:
    return call_openai_json(
        client,
        model=MODEL,
        system=SYSTEM_PROMPT,
        user=USER_PROMPT_TEMPLATE.format(content=content),
        temperature=TEMPERATURE,
        max_tokens=2000,
    )
