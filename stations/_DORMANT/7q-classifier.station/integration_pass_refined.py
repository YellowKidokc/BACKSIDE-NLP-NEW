"""
Seven Questions Integration Pass — Refined
=========================================
Formerly: Promotion Pass.

Purpose:
After a claim survives reversal testing, this pass builds the support architecture:
- comparable frameworks
- confidence gradient
- structural vs analogical mappings
- evidence/literature targets
- equivalent expressions
- predictions
- integration map

This is not a hype pass. It is a convergence architecture pass.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from seven_q_core import DEFAULT_MODEL, call_openai_json, ensure_list, read_text, safe_str, slugify, today, write_json

SYSTEM_PROMPT = """You are a research architect and epistemic auditor.
A claim has already undergone adversarial reversal testing.
Your job is not to praise it. Your job is to build the cleanest possible integration architecture around whatever survived.

Rules:
- Distinguish structural isomorphism from analogy.
- Distinguish support from resonance.
- Do not invent citations. Mark citation_needed where needed.
- Name real fields, theories, authors, and journals only when you have reasonable confidence.
- Return ONLY valid JSON.
"""

INTEGRATION_PROMPT = """Build an Integration Pass for the following paper and Seven Questions analysis.

Central claim:
{claim}

Known domains:
{domains}

Weakest link:
{weakest_link}

Paper excerpt:
{paper_excerpt}

7QS excerpt:
{seven_q_excerpt}

Return this exact JSON object:
{
  "i1_framework_posture": [
    {"name":"...", "field":"...", "relation":"structural|analogical|historical|oppositional", "why_it_matters":"...", "citation":"citation_needed|..."}
  ],
  "i2_confidence_gradient": {
    "tier_a_high_confidence": ["claims already strongly grounded"],
    "tier_b_plausible": ["claims plausible but requiring more support"],
    "tier_c_speculative": ["claims publishable only as hypothesis"]
  },
  "i3_isomorphism_map": [
    {"domain_a":"...", "domain_b":"...", "mapping":"...", "quality":"structural|analogical|weak|contested", "equations_transfer":false, "failure_mode":"..."}
  ],
  "i4_literature_targets": [
    {"topic":"...", "likely_authors_or_fields":["..."], "search_query":"...", "why_needed":"..."}
  ],
  "i5_equivalent_forms": {
    "plain_language":"...",
    "physical_form":"...",
    "informational_form":"...",
    "systems_form":"...",
    "mathematical_form":"...",
    "theological_form":"..."
  },
  "i6_predictions": [
    {"prediction":"...", "test_type":"empirical|formal|historical|conceptual", "decisive":false, "what_result_would_hurt":"..."}
  ],
  "i7_integration_verdict": {
    "core_variable":"...",
    "iso_status":"full|partial|analogical|weak|unclear",
    "best_use":"canon|research|hypothesis|archive|rewrite",
    "one_sentence_verdict":"..."
  },
  "infobox_fields": {
    "confidence_label":"Established|Strong|Provisional|Speculative|Weak",
    "structural_count":0,
    "analogical_count":0,
    "strongest_q":{"q_num":"I1", "q_label":"Framework Posture", "score":0.0, "explanation":"..."},
    "weakest_q":{"q_num":"I3", "q_label":"Isomorphism", "score":0.0, "explanation":"..."},
    "iso_status":"...",
    "iso_hint":"...",
    "bundled_claims":0,
    "paper_type":"...",
    "domain_count":0,
    "effective_n":0,
    "decisive_test_short":"..."
  }
}
"""


def _extract_claim(seven_q: Dict[str, Any]) -> str:
    return safe_str(
        seven_q.get("foundations_7q", {}).get("central_claim")
        or seven_q.get("forward_7q", {}).get("q2")
        or "[claim not found]"
    )


def _extract_domains(seven_q: Dict[str, Any]) -> str:
    domains = (
        seven_q.get("foundations_7q", {}).get("domains")
        or seven_q.get("forward_7q", {}).get("q1")
        or []
    )
    return ", ".join(safe_str(d) for d in ensure_list(domains)) or "[domains not found]"


def _extract_weakest(seven_q: Dict[str, Any]) -> str:
    return safe_str(
        seven_q.get("reversals_7q", {}).get("weakest_link")
        or seven_q.get("reverse_7q", {}).get("r4")
        or "[weakest link not found]"
    )


def run_integration_pass(paper_path: str | Path, seven_q_json: str | Path, output_dir: Optional[str | Path] = None, model: str = DEFAULT_MODEL) -> Dict[str, Any]:
    paper_path = Path(paper_path)
    seven_q_path = Path(seven_q_json)
    paper_excerpt = read_text(paper_path, max_chars=5000)
    seven_q = json.loads(seven_q_path.read_text(encoding="utf-8"))
    seven_q_excerpt = json.dumps(seven_q, ensure_ascii=False)[:6000]

    prompt = INTEGRATION_PROMPT.format(
        claim=_extract_claim(seven_q),
        domains=_extract_domains(seven_q),
        weakest_link=_extract_weakest(seven_q),
        paper_excerpt=paper_excerpt,
        seven_q_excerpt=seven_q_excerpt,
    )

    print(f"  Integration Pass: {paper_path.name}")
    integration = call_openai_json(prompt, SYSTEM_PROMPT, model=model, max_tokens=4000)

    result = {
        "schema": "seven_questions.integration.v1",
        "paper": paper_path.name,
        "source_path": str(paper_path),
        "seven_q_source": str(seven_q_path),
        "analyzed_at": datetime.now().isoformat(),
        "model": model,
        "integration_pass": integration,
        # compatibility alias for older scripts
        "promotion_pass": integration,
        "infobox_fields": integration.get("infobox_fields", {}) if isinstance(integration, dict) else {},
    }

    out_dir = Path(output_dir) if output_dir else seven_q_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{slugify(paper_path.stem)}_INTEGRATION_{today()}.json"
    write_json(out_path, result)
    print(f"  Saved: {out_path.name}")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run refined Integration Pass using a paper and a 7QS JSON file.")
    parser.add_argument("--paper", required=True, help="Source markdown paper")
    parser.add_argument("--seven-q", required=True, help="7QS JSON result")
    parser.add_argument("--output", help="Output directory")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    args = parser.parse_args()
    run_integration_pass(args.paper, args.seven_q, args.output, args.model)
