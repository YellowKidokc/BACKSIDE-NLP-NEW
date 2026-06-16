"""
EQUATION AUDIT — is the math doing work or decorative?

Fills: snapshot.equations: list[EquationEntry]

The key question: does each equation produce outputs, constrain something,
or sit there for visual authority?
"""
from ._runner import call_openai_json

SECTION_NAME = "equation_audit"
SCHEMA_TARGET = "list[EquationEntry]"
MODEL = "gpt-4o-mini"
TEMPERATURE = 0.2

SYSTEM_PROMPT = """You are a mathematical physicist auditing a paper's equations.

For every equation, you must answer one structural question: is this math
doing actual work — producing outputs, constraining predictions, deriving
results — or is it decorative, symbolic flourish, or analogical scaffolding?

This is not an insult. Decorative equations have a place. But the reader
should know which is which. Be precise. If variables are undefined, name
that. If a variable does double duty (means two things in different places),
flag it. If units are absent, flag it."""

USER_PROMPT_TEMPLATE = """Audit every equation in this paper.

For each equation found:
- equation: the equation as written (use plain text approximation if Unicode/LaTeX)
- purpose: one sentence — what is this equation FOR?
- variables_defined: true if all variables are defined somewhere in the paper
- variable_definitions: dict of "symbol": "definition" for each variable
- dimensional_status: "defined" (units stated), "undefined" (no units),
  "symbolic" (intentionally dimensionless/abstract), "not_applicable"
- operational_status: "computable" (you could plug in numbers and get a result),
  "symbolic" (formal but not numerical), "metaphorical" (visually equation-shaped
  but not mathematical)
- role: "doing_work" (produces predictions/derivations),
  "decorative" (visual authority only),
  "structural" (organizes the framework),
  "predictive" (forecasts something measurable)
- issues: array of flags. Examples: "variable G undefined", "double use of S",
  "no units given", "dimensionally inconsistent"

PAPER CONTENT:
{content}

Respond as JSON: {{"equations": [{{...}}], "summary": "string", "ai_confidence": "low|medium|high"}}

If the paper has no equations, return {{"equations": [], "summary": "no equations found", "ai_confidence": "high"}}"""

EXPECTED_JSON_SHAPE = {
    "equations": [
        {
            "equation": "string",
            "purpose": "string",
            "variables_defined": True,
            "variable_definitions": {"symbol": "definition"},
            "dimensional_status": "defined|undefined|symbolic|not_applicable",
            "operational_status": "computable|symbolic|metaphorical",
            "role": "doing_work|decorative|structural|predictive",
            "issues": ["string"],
        }
    ],
    "summary": "string",
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
