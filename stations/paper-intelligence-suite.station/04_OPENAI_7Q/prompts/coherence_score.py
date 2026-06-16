"""
COHERENCE / REVIEW-READINESS — 8-metric structural rubric.

Fills: snapshot.coherence: CoherenceScore

This is NOT an objective truth score. It is a review-readiness score:
how well-built is this paper as a piece of structured argument?
"""
from ._runner import call_openai_json

SECTION_NAME = "coherence_score"
SCHEMA_TARGET = "CoherenceScore"
MODEL = "gpt-4o-mini"
TEMPERATURE = 0.2

SYSTEM_PROMPT = """You are scoring a paper's review-readiness across 8
structural metrics. Each is 0-10. This is NOT a verdict on whether the
paper's claims are TRUE. It is an audit of whether the paper is BUILT WELL.

A brilliant paper can score low if it's poorly structured. A boring paper
can score high if it's tight. Both outcomes are useful.

Be specific in your justifications. Vague rubric scores are worse than no
scores at all."""

USER_PROMPT_TEMPLATE = """Score this paper across 8 review-readiness metrics (0-10 each).

1. definition_clarity — are key terms defined consistently?
2. equation_coherence — do equations match prose claims, or contradict them?
3. claim_discipline — are claims kept inside the evidence offered?
4. scope_control — does the paper stay within its stated scope, or overreach?
5. falsifiability — are kill conditions present and concrete?
6. citation_adequacy — are factual claims supported with citations?
7. domain_separation — are physics, theology, metaphor, and math kept distinct?
   (A paper that conflates them silently scores low.)
8. reader_burden — could a smart outsider follow the argument?
   (10 = clear; 0 = requires inside knowledge to parse.)

Then compute review_readiness as a weighted aggregate (0-100). The aggregate
should be your overall judgment, not a mechanical mean.

Provide a one-sentence justification per metric in `justifications`.

PAPER CONTENT:
{content}

Respond as JSON: {{"definition_clarity": 0, "equation_coherence": 0, "claim_discipline": 0, "scope_control": 0, "falsifiability": 0, "citation_adequacy": 0, "domain_separation": 0, "reader_burden": 0, "review_readiness": 0, "justifications": {{"definition_clarity": "string", ...}}, "ai_confidence": "low|medium|high"}}"""

EXPECTED_JSON_SHAPE = {
    "definition_clarity": 0,
    "equation_coherence": 0,
    "claim_discipline": 0,
    "scope_control": 0,
    "falsifiability": 0,
    "citation_adequacy": 0,
    "domain_separation": 0,
    "reader_burden": 0,
    "review_readiness": 0,
    "justifications": {"metric_name": "one-sentence justification"},
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
