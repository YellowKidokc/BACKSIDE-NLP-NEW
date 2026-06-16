"""
PHYSICS COMPARISON — what known theory is this closest to, and does it outperform?

Fills: snapshot.physics_comparison: list[PhysicsComparison]

Prevents category confusion: a metaphysical framework should not be judged
as failed empirical physics, and vice versa.
"""
from ._runner import call_openai_json

SECTION_NAME = "physics_comparison"
SCHEMA_TARGET = "list[PhysicsComparison]"
MODEL = "gpt-4o-mini"
TEMPERATURE = 0.2

SYSTEM_PROMPT = """You are placing a paper on the map of existing physics
and theory. For each substantive comparison, you name the nearest known theory,
the structural similarity, the structural difference, and whether the paper
actually outperforms its nearest neighbor on any axis.

Be specific. "Quantum mechanics" is a category, not a theory. "Copenhagen
interpretation" is a theory. "Bohmian mechanics" is a theory. Pick the
specific one.

Flag category-confusion risk: when a paper LOOKS like one kind of theory
(empirical physics) but is actually another (metaphysical framework, formal model,
philosophical argument), readers misjudge it. Surface that risk."""

USER_PROMPT_TEMPLATE = """Place this paper on the map of existing theories.

Compare against the nearest 2-5 known theories from this list (or others
if appropriate): Standard Model, General Relativity, Quantum Mechanics
(specify interpretation), Thermodynamics, Information Theory (Shannon /
Kolmogorov / algorithmic), Cybernetics, Integrated Information Theory,
Process Philosophy, Theological Metaphysics (specify tradition),
Mathematical Platonism, Simulation Theory, Systems Theory,
Quantum Cognition, Free Energy Principle.

For each comparison:
- nearest_theory: specific theory name
- similarity: where the paper aligns structurally with this theory
- difference: where it diverges, and what the divergence buys
- does_paper_outperform: "yes" (clearly better on some axis), "no", "unclear"
- category_confusion_risk: a sentence on what KIND of paper this should be
  judged as. E.g., "This is a formal model, not an empirical claim — judging
  it on empirical predictions would miscategorize it."

PAPER CONTENT:
{content}

Respond as JSON: {{"comparisons": [{{...}}], "honest_label": "string", "ai_confidence": "low|medium|high"}}

`honest_label` is what KIND of paper this is — e.g., "framework paper", "formal
model", "empirical hypothesis", "philosophical argument", "structural isomorphism
proposal"."""

EXPECTED_JSON_SHAPE = {
    "comparisons": [
        {
            "nearest_theory": "string",
            "similarity": "string",
            "difference": "string",
            "does_paper_outperform": "yes|no|unclear",
            "category_confusion_risk": "string",
        }
    ],
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
        max_tokens=2500,
    )
