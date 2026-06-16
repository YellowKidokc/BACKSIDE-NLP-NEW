"""
KILL CONDITIONS — what would destroy each major claim.

Fills: snapshot.kill_conditions: list[KillCondition]

A claim without a kill condition is unfalsifiable, which means it isn't
a scientific claim. A paper may still be valuable without one — but the
distinction must be visible.
"""
from ._runner import call_openai_json

SECTION_NAME = "kill_conditions"
SCHEMA_TARGET = "list[KillCondition]"
MODEL = "gpt-4o-mini"
TEMPERATURE = 0.2

SYSTEM_PROMPT = """You are a hostile but fair reviewer. For each major claim
in a paper, your job is to identify what observation, calculation,
contradiction, or experimental result would weaken or destroy it.

Do not invent kill conditions the paper rules out. Do not strawman. The kill
condition must be a genuine vulnerability the claim genuinely has.

If a claim is in principle unfalsifiable (a metaphysical or analytical claim),
say so explicitly with severity "unfalsifiable" — this is data, not a fault.
But mark it clearly so readers know what kind of claim they're dealing with."""

USER_PROMPT_TEMPLATE = """For each major claim in this paper, specify a kill condition.

Cover the 5-10 most load-bearing claims. For each:
- claim: the claim being tested (one sentence, near-quote)
- kill_condition: the specific observation/calculation/result that would
  destroy or significantly weaken this claim
- test_method: how would you actually run that test? Be concrete.
  Examples: "QFT calculation in infinite-volume limit", "philological review
  of post-hoc reading", "energy conservation audit across full sequence"
- severity: "fatal" (claim cannot survive), "wounding" (claim survives but weakened),
  "minor" (claim adjusts but holds)
- current_status: "open" (test hasn't been run), "weak" (some evidence against),
  "strong" (claim has survived attempts), "unresolved" (test is ambiguous),
  "satisfied" (kill condition has been met — claim is dead)

If the claim is unfalsifiable in principle, set severity to "fatal" and
test_method to "unfalsifiable in principle — note as metaphysical".

PAPER CONTENT:
{content}

Respond as JSON: {{"kill_conditions": [{{...}}], "ai_confidence": "low|medium|high", "notes": "string"}}"""

EXPECTED_JSON_SHAPE = {
    "kill_conditions": [
        {
            "claim": "string",
            "kill_condition": "string",
            "test_method": "string",
            "severity": "fatal|wounding|minor",
            "current_status": "open|weak|strong|unresolved|satisfied",
        }
    ],
    "ai_confidence": "medium",
    "notes": "string",
}


def run(content: str, client) -> dict:
    return call_openai_json(
        client,
        model=MODEL,
        system=SYSTEM_PROMPT,
        user=USER_PROMPT_TEMPLATE.format(content=content),
        temperature=TEMPERATURE,
        max_tokens=2500,
    )
