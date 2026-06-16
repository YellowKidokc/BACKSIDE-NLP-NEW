"""
REVISION PLAN — actionable guidance for the author.

Fills: snapshot.revision: RevisionPlan

The output the author actually wants. What's strongest, what's weakest,
what to fix before publication, what test would settle the most uncertainty.
"""
from ._runner import call_openai_json

SECTION_NAME = "revision_plan"
SCHEMA_TARGET = "RevisionPlan"
MODEL = "gpt-4o-mini"
TEMPERATURE = 0.2

SYSTEM_PROMPT = """You are writing the revision plan for a paper's author.

This is the section that has to be useful. Vague advice ("clarify your terms",
"add citations") helps no one. Specific advice ("define χ in section 2 — it's
used three different ways", "the τ_lock = 33 derivation is the single most
load-bearing claim, prioritize that calculation") is worth the whole rest
of the review.

Be direct. Name passages. Name what test, citation, or derivation would do
the most work."""

USER_PROMPT_TEMPLATE = """Write the revision plan for this paper.

Fields:
- strongest_part: name the single most defensible component. Be specific —
  section name, claim, or argument. One paragraph.
- weakest_part: name the single most vulnerable component. Same specificity.
- must_fix_before_publication: 3-7 concrete edits. Each one should be actionable
  in a sentence the author could put on a TODO list. Not "improve the math",
  but "define G in equation 2 — it's used as both gravitational coupling and
  Grace function".
- best_next_test: the single experiment, calculation, citation review, or
  derivation that would do the MOST to strengthen or kill the paper.
- needs_expert_review: which specific expert domains should review before
  publication? Examples: "philology", "QFT", "statistics", "history of
  early Christianity", "category theory". Up to 4.

PAPER CONTENT:
{content}

Respond as JSON: {{"strongest_part": "string", "weakest_part": "string", "must_fix_before_publication": ["string"], "best_next_test": "string", "needs_expert_review": ["string"], "ai_confidence": "low|medium|high"}}"""

EXPECTED_JSON_SHAPE = {
    "strongest_part": "string",
    "weakest_part": "string",
    "must_fix_before_publication": ["string"],
    "best_next_test": "string",
    "needs_expert_review": ["string"],
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
