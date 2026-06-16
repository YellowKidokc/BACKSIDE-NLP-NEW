"""
PROMOTION PASS — 7 Forward Projection Questions
================================================
NOT kill tests. NOT accountability questions.
The claim survived. Now: build the architecture.

Outputs JSON used to populate:
  - 7Q_INFOBOX_TEMPLATE (the FACTS callout at top)
  - Paper I T.3 evidence table
  - Paper I T.5 cross-domain mapping
  - Paper I [A] ADMIT confidence gradient
  - Paper I FRAMEWORK POSITIONING

7 Questions:
  P1 POSTURE    — which frameworks share this explanatory ambition?
  P2 GRADIENT   — Tier A/B/C confidence per claim layer
  P3 ISOMORPHISM — which mappings are STRUCTURAL vs ANALOGICAL?
  P4 EVIDENCE   — literature supporting the architecture (not full thesis)
  P5 FORMS      — equivalent expressions in physics/info/systems language
  P6 PREDICTIONS — observable consequences if true
  P7 INTEGRATION — cross-domain isomorphism table
"""
import json, os
from pathlib import Path
from datetime import datetime

PROMOTION_SYSTEM = """You are a research architect. A paper's central claim has already survived an adversarial kill test.
Your task is NOT to attack it. Build the strongest support architecture around what survived.

Return ONLY valid JSON. No markdown fences, no explanation, no preamble."""

def build_promotion_prompt(claim, domains, weakest_link, paper_text_excerpt):
    return f"""The following claim has survived adversarial testing. Central claim:

"{claim}"

Primary domains identified: {', '.join(domains)}
Known weakest link: "{weakest_link}"

Paper excerpt (first 1500 chars):
{paper_text_excerpt[:1500]}

Run 7 PROMOTION PASS questions. Return this exact JSON structure:

{{
  "p1_posture_frameworks": [
    {{"name": "...", "type": "STRUCTURAL|ANALOGICAL", "justification": "...", "citation": "..."}}
  ],
  "p2_confidence_gradient": {{
    "tier_a": ["High-confidence claims already grounded..."],
    "tier_b": ["Moderate — plausible and formalizable but contested..."],
    "tier_c": ["Speculative but structured — publishable as hypothesis..."]
  }},
  "p3_domain_isomorphism": [
    {{"domain": "...", "mapping_type": "STRUCTURAL|ANALOGICAL|WEAK", "interpretation": "...", "transfers_equations": true}}
  ],
  "p4_support_literature": [
    {{"citation": "...", "author": "...", "year": "...", "supports_what": "...", "confidence": 0.0}}
  ],
  "p5_equivalent_forms": {{
    "physical_form": "...",
    "informational_form": "...",
    "systems_form": "...",
    "mathematical_form": "..."
  }},
  "p6_forward_predictions": [
    {{"prediction": "...", "testable": true, "decisive": false}}
  ],
  "p7_integration_map": {{
    "core_variable": "...",
    "domain_translations": [
      {{"domain": "...", "translation": "..."}}
    ],
    "iso_status": "FULL|PARTIAL|ANALOGICAL",
    "iso_hint": "..."
  }},
  "infobox_fields": {{
    "confidence_label": "Established|Strong|Provisional|Speculative",
    "structural_count": 0,
    "analogical_count": 0,
    "strongest_q": {{"q_num": "P1", "q_label": "Posture", "score": 0.0, "explanation": "..."}},
    "weakest_q": {{"q_num": "P3", "q_label": "Isomorphism", "score": 0.0, "explanation": "..."}},
    "iso_status": "...",
    "iso_hint": "...",
    "bundled_claims": 0,
    "paper_type": "...",
    "domain_count": 0,
    "effective_n": 0,
    "decisive_test_short": "..."
  }}
}}"""


def run_promotion_pass(paper_path, seven_q_data, output_dir=None):
    """
    Run Promotion Pass on a paper using its 7Q JSON as context.
    Returns dict with all promotion pass results.
    """
    import requests

    api_key = os.environ.get('OPENAI_API_KEY', '')
    if not api_key:
        print("  PROMOTION: No OPENAI_API_KEY — skipping")
        return {}

    paper_path = Path(paper_path)
    paper_text = paper_path.read_text(encoding='utf-8', errors='ignore')

    fwd    = seven_q_data.get('forward_7q', {})
    rev    = seven_q_data.get('reverse_7q', {})
    claim  = str(fwd.get('q2', '')).strip()
    domains_raw = fwd.get('q1', [])
    if isinstance(domains_raw, str):
        domains_raw = [d.strip() for d in domains_raw.split(',')]
    domains = [d.strip().title() for d in domains_raw if d.strip()]
    weakest = str(rev.get('r4', '')).strip()

    prompt = build_promotion_prompt(claim, domains, weakest, paper_text)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    body = {
        "model": "gpt-4o-mini",
        "max_tokens": 2000,
        "messages": [
            {"role": "system", "content": PROMOTION_SYSTEM},
            {"role": "user",   "content": prompt}
        ]
    }

    try:
        resp = requests.post("https://api.openai.com/v1/chat/completions",
                             headers=headers, json=body, timeout=60)
        resp.raise_for_status()
        raw = resp.json()['choices'][0]['message']['content'].strip()
        # Strip any accidental markdown fences
        raw = raw.replace('```json','').replace('```','').strip()
        result = json.loads(raw)

        # Save to output dir
        if output_dir:
            out = Path(output_dir)
            out.mkdir(parents=True, exist_ok=True)
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            stem = paper_path.stem
            out_path = out / f"{stem}_PROMOTION_{ts}.json"
            out_path.write_text(json.dumps(result, indent=2), encoding='utf-8')
            print(f"  Promotion saved: {out_path.name}")

        return result

    except Exception as e:
        print(f"  PROMOTION ERR: {e}")
        return {}
