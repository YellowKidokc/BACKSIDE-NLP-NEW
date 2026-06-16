"""
EVIDENCE MAP — claim → evidence → quality → counterevidence.

Fills: snapshot.evidence_map: list[EvidenceEntry]

Not just citations. A real map of what supports what, how strongly, and
what counterevidence is missing.
"""
from ._runner import call_openai_json

SECTION_NAME = "evidence_map"
SCHEMA_TARGET = "list[EvidenceEntry]"
MODEL = "gpt-4o-mini"
TEMPERATURE = 0.2

SYSTEM_PROMPT = """You are a reviewer building an evidence map for a paper.

For each substantive claim, you trace what evidence the paper offers,
what kind of evidence it is, how strong the support actually is, and
what counterevidence the paper does not address.

Be honest about evidence-claim alignment. Citing a paper that loosely
relates to a claim is not the same as citing one that supports it.
Flag the gap explicitly."""

USER_PROMPT_TEMPLATE = """Build the evidence map for this paper. Cover the 5-12
most substantive claims.

For each:
- claim: the claim being supported (one sentence)
- supporting_evidence: what the paper actually offers — citations, data,
  arguments, experiments, derivations. Quote if possible.
- evidence_type: "primary" (original data/derivation in this paper),
  "secondary" (citation to another paper's evidence),
  "interpretive" (re-reading existing data),
  "speculative" (logical argument without empirical backing)
- evidence_quality: "weak", "moderate", "strong"
- counterevidence_needed: what evidence WOULD strengthen or destroy this claim
  that the paper has not addressed?
- gap: where does the evidence fall short of fully grounding the claim?
  One sentence. Empty string if evidence fully supports.

PAPER CONTENT:
{content}

Respond as JSON: {{"evidence_map": [{{...}}], "ai_confidence": "low|medium|high"}}"""

EXPECTED_JSON_SHAPE = {
    "evidence_map": [
        {
            "claim": "string",
            "supporting_evidence": "string",
            "evidence_type": "primary|secondary|interpretive|speculative",
            "evidence_quality": "weak|moderate|strong",
            "counterevidence_needed": "string",
            "gap": "string",
        }
    ],
    "ai_confidence": "medium",
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
