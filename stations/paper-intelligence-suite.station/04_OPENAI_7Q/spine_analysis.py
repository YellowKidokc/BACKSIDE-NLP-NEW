SECTION_NAME = "spine_analysis"
SCHEMA_TARGET = "SpineAnalysis"
MODEL = "gpt-4o"
TEMPERATURE = 0.3

SYSTEM_PROMPT = """You are a structural editor analyzing articles in a 26-part series called Genesis to Quantum. Your job is to extract the question-answer architecture of each article — not summarize content, but identify the logical skeleton.

You extract three layers:
1. Movement Chain — every section or major paragraph shift is answering a sub-question. Find each one in order.
2. Page Question — the ONE question this entire article exists to answer.
3. Bridge — what question this article opens that the next article must answer.

You also inventory every technical term and flag where terms pile up before the reader has reason to care.

State all questions the way a curious non-expert would ask them. State all answers the way you would explain to a smart friend over coffee. No jargon in questions or answers. If you cannot state it without jargon, flag it as a clarity problem.

Do not editorialize about whether claims are true. Analyze whether they are CLEAR.

Respond ONLY as JSON with the shape provided. No preamble. No markdown fences."""

USER_PROMPT_TEMPLATE = """Analyze the following article and extract its question-answer spine.

PAPER CONTENT:
{content}

Respond as JSON with shape:
{expected_shape}
"""

EXPECTED_JSON_SHAPE = {
    "article_title": "string — title as written",
    "proposed_reader_title": "string — rewritten as question or statement a non-physicist would click on",
    "movement_chain": [
        {
            "number": "int",
            "question_asked": "string — plain English, no jargon",
            "answer_given": "string — one sentence, plain English",
            "terms_introduced": ["string — each new technical term introduced"],
            "clarity_flag": "OK | JARGON_HEAVY | UNCLEAR | REDUNDANT"
        }
    ],
    "page_question": "string — the ONE question this article answers, plain English",
    "page_answer": "string — one sentence answer",
    "is_single_question": "ONE | MULTIPLE",
    "multiple_questions_if_any": ["string — list if MULTIPLE"],
    "bridge_question": "string — what question this article opens for the next",
    "bridge_strength": "STRONG | WEAK | NONE",
    "term_inventory": [
        {
            "term": "string",
            "first_section": "int — section number where first used",
            "defined_before_use": "YES | NO",
            "plain_definition_given": "YES | NO"
        }
    ],
    "jargon_pileup_sections": ["int — section numbers where 4+ undefined terms appear within 3 paragraphs"],
    "strongest_section": {"number": "int", "reason": "string"},
    "weakest_section": {"number": "int", "reason": "string"},
    "biggest_clarity_problem": "string — one sentence",
    "reader_dropoff_risk": "string — where and why a non-expert would stop reading",
    "recommended_fix_priority": "string — the single change that would improve this article most",
    "clarity_grade": "A | B | C | D | F"
}


def run(content: str, client) -> dict:
    """Call OpenAI, return the parsed JSON dict."""
    import json
    try:
        response = client.chat.completions.create(
            model=MODEL,
            temperature=TEMPERATURE,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": USER_PROMPT_TEMPLATE.format(
                    content=content[:6000] + "\n...\n" + content[-2000:] if len(content) > 8000 else content,
                    expected_shape=json.dumps(EXPECTED_JSON_SHAPE, indent=2)
                )}
            ]
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e), "section": SECTION_NAME}
