"""
CLAIM INVENTORY — every claim, typed and scored.

Fills: snapshot.claim_inventory: list[Claim]

Why it matters: most papers fail when rhetorical claims and technical claims
get mixed together. This separates them.
"""
from ._runner import call_openai_json

SECTION_NAME = "claim_inventory"
SCHEMA_TARGET = "list[Claim]"
MODEL = "gpt-4o-mini"
TEMPERATURE = 0.2

SYSTEM_PROMPT = """You are a structural peer reviewer. Your job is to inventory
every distinct claim a paper makes and tag each one rigorously.

Do not summarize. Do not paraphrase loosely. Quote or near-quote each claim,
then categorize. If a sentence makes two claims, split them. If a claim is
implied but never stated, flag it as implicit in `notes`.

Be honest about which claims are rhetorical (assertion without argument).
Calling something rhetorical is not an insult — it's a precise category."""

USER_PROMPT_TEMPLATE = """Inventory every distinct claim in this paper. Aim for 8-20 claims.

For each claim:
- claim: the actual statement, quoted or near-quoted (one sentence)
- claim_type: one of "mathematical", "physical", "information_theoretic",
  "metaphysical", "historical", "empirical", "analogy"
- importance: "core" (load-bearing), "support" (used to justify a core claim),
  or "rhetorical" (asserted without argument)
- evidence_present: true if the paper provides evidence; false if it asserts
- testability: "yes" (clear test exists), "partial" (test conceivable but not specified),
  "no" (in principle untestable)
- risk_level: "low", "medium", "high" — risk that the claim is wrong or unfounded
- needs_citation: true if a factual claim is uncited
- notes: brief annotation if anything is unusual (implicit, ambiguous, contested)

PAPER CONTENT:
{content}

Respond as JSON: {{"claims": [{{...}}, {{...}}, ...], "ai_confidence": "low|medium|high", "notes": "any global observation"}}"""

EXPECTED_JSON_SHAPE = {
    "claims": [
        {
            "claim": "string",
            "claim_type": "mathematical|physical|information_theoretic|metaphysical|historical|empirical|analogy",
            "importance": "core|support|rhetorical",
            "evidence_present": True,
            "testability": "yes|partial|no",
            "risk_level": "low|medium|high",
            "needs_citation": False,
            "notes": "string",
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
