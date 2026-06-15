"""
NOVELTY CLASSIFICATION — what is actually new here, at what level?

Fills: snapshot.novelty: NoveltyClassification

Five levels of novelty, weakest to strongest. Most papers oversell at one
level higher than they earn. This prompt detects that and proposes the honest
label.
"""
from ._runner import call_openai_json

SECTION_NAME = "novelty_classification"
SCHEMA_TARGET = "NoveltyClassification"
MODEL = "gpt-4o-mini"
TEMPERATURE = 0.2

SYSTEM_PROMPT = """You are classifying a paper's novelty.

Five levels (weakest to strongest):
  1. new_framing — existing ideas arranged in a new way
  2. new_model — a proposed formal structure
  3. new_prediction — claims something measurable before confirmation
  4. new_derivation — derives something (known or new) from stated axioms
  5. new_empirical_result — produces data not previously available

Most papers fail at one level above what they earn. A paper that is "new
framing + new model" is valuable — calling it "new prediction" without
testable specifics is overselling.

Be honest. Surface overstated novelty as a separate flag list. Propose the
HONEST label the paper should be tagged with."""

USER_PROMPT_TEMPLATE = """Classify this paper's novelty.

Identify which of the 5 novelty levels apply (paper can earn multiple):
- new_framing
- new_model
- new_prediction
- new_derivation
- new_empirical_result

For each level claimed by the paper but not earned (paper SAYS it predicts
but offers no testable specifics, or SAYS it derives but no derivation
appears), add to overstated_novelty_flags as a short sentence.

Then write the honest_label — one phrase describing what kind of paper
this actually is. Examples:
- "framework paper with one proposed formal model"
- "philosophical argument with structural-isomorphism claim"
- "empirical hypothesis paper requiring P3 measurement to confirm"
- "literature review with reframing"

PAPER CONTENT:
{content}

Respond as JSON: {{"novelty_levels": ["new_framing", ...], "primary_novelty": "string", "overstated_novelty_flags": ["string"], "honest_label": "string", "ai_confidence": "low|medium|high"}}"""

EXPECTED_JSON_SHAPE = {
    "novelty_levels": ["new_framing|new_model|new_prediction|new_derivation|new_empirical_result"],
    "primary_novelty": "string",
    "overstated_novelty_flags": ["string"],
    "honest_label": "string",
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
