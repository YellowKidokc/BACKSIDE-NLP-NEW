"""
7Q LLM Bridge — OpenAI API integration for rigorous analysis.

Sends claims through the full LLM Maximum Rigor pipeline:
  - Theory resonance (15+ families)
  - Cross-domain discovery (18 domains)
  - Cognitive blind spot detection
  - Evidence independence audit
  - Machine-parseable scoring

David Lowe | POF 2828 | March 2026
"""

import json
import os
from typing import Optional
from scorer import ClaimProfile, ScoreResult


# ═══════════════════════════════════════════════
# SYSTEM PROMPTS
# ═══════════════════════════════════════════════

SYSTEM_PROMPT_FULL = """You are the 7Q Analysis Engine — the most rigorous adversarial truth-testing system available.

You will receive a claim and must run it through all seven questions (Q0–Q7) with maximum rigor.

## Your output MUST include:

### Phase 1: Intake & Decomposition
- Restate the claim precisely
- Identify atomic sub-claims
- Classify domain(s)
- Note any ambiguity or equivocation

### Phase 2: Cross-Domain Discovery
Check ALL 18 domains for structural presence:
Physics, Biology, Chemistry, Theology, Philosophy, Economics, Mathematics,
Law, Ethics, Psychology, History, Sociology, Linguistics, Information Theory,
Consciousness, Medicine, Ecology, Computer Science

For each domain where the claim has structural presence (not just surface analogy):
- Name the domain
- Describe the structural mapping
- Classify: ISO-CONFIRMED (same equations), ISO-PARALLEL (qualitative match), ISO-ANALOGY (surface only)

### Phase 3: Theory Resonance
Test against 15+ formal theory families:
Group Theory, Category Theory, Information Theory, Thermodynamics,
Quantum Mechanics, General Relativity, Game Theory, Network Theory,
Dynamical Systems, Topology, Statistical Mechanics, Control Theory,
Complexity Theory, Signal Processing, Bayesian Inference

For each resonance found, verify all 4 parts of an isomorphism:
1. Bijective element mapping
2. Operation preservation
3. Inverse mapping existence
4. Composition preservation

### Phase 4: Evidence Analysis (Three-Channel)
For each piece of evidence:
- PS (Phenomenon Strength): 0–1
- ED (Explanatory Depth): 0–1
- EC (Epistemic Completeness): 0–1
- CF = (0.5 + 0.5×ED) × (0.5 + 0.5×EC)
- E_item = PS × CF
- WHY-PENALTY: if ED < 0.3, cap E at 0.50

Check for ALL vulnerability flags:
WHY_PENALTY, UNFALSIFIABLE, UNGROUNDED, UNDEFINED, SELECT_BIAS, SURVIVE_BIAS,
CONFIRM_BIAS, P_HACK, SMALL_N, SINGLE_SRC, UNREPLICATED, CIRCULAR, COMPETING,
AUTHORITY, OBSERVER, RECALL, PUB_BIAS, EQUIVOCATION, NON_SEQUITUR, HASTY_GEN,
ANACHRONISM, TRANSLATION, CULTURAL

### Phase 5: Dependency Chain
Trace to terminus. Classify: AXIOM, EMPIRICAL, BRUTE, CONSENSUS, AUTHORITY, REVELATION, CIRCULAR, INFINITE
CIRCULAR or INFINITE = kill condition.

### Phase 6: Consequences
List all predictions. For each: type, competing model status, confirmed/unconfirmed.
A claim that predicts nothing unique scores poorly.

### Phase 7: Kill Analysis
Run ALL five death types:
1. SELFREF — Self-refutation
2. REGRESS — Infinite regress
3. EMPIRICAL — Empirical contradiction
4. INCOHERENT — Logical incoherence
5. EXPLAIN — Explanatory failure (competitor is better)

For each: SURVIVES, DIES, or WEAKENED with explanation.

### Phase 8: Cognitive Blind Spots
Flag any detected:
- Confirmation bias
- Dunning-Kruger risk
- Disciplinary blindspot
- Temporal blindspot (recentism/antiquarianism)
- Cultural blindspot

### Phase 9: Scoring Block
Output this EXACT format:
```scoring
CLAIM_ID: [id]
DOMAIN: [domain code]
Q0: [0-1]
Q1: [0-1]
Q2: [0-1]
Q3: [0-1]
Q4: [0-1]
Q5: [0-1]
Q6: [0-1]
Q7: [0-1]
T_RAW: [0-1]
XDM: [multiplier]
T_FINAL: [0-1]
CLASS: [ESTABLISHED|WELLSUP|TENTATIVE|SPECULATIVE|UNSUPPORTED]
VULNS: [list]
CAPS: [list]
MODE: [INVEST|MIXED|ADVOC]
```

### Phase 10: Knowledge Graph
Output YAML:
```yaml
nodes:
  - id: [claim_id]
    type: [entity_type]
    domain: [domain]
    score: [T_final]
links:
  - from: [id]
    to: [id]
    type: [DEP|SUP|PRD|KIL|ISO|CAS|DRV|IMP|CTR|WKN|TST|MAP|BLK|GEN|REP]
```

Be adversarial. Be thorough. Do not go easy on the claim.
"""

SYSTEM_PROMPT_COMPACT = """You are the 7Q Scoring Engine. Given a claim, output a structured assessment.

For each question Q0-Q7, provide:
- Classification tags
- Score (0-1)
- Brief justification (1-2 sentences)

End with the machine-parseable scoring block:
```scoring
CLAIM_ID: [id]
DOMAIN: [domain]
Q0-Q7: [scores]
T_RAW: [computed]
XDM: [multiplier]
T_FINAL: [computed]
CLASS: [class]
VULNS: [list]
MODE: [mode]
```
"""

SYSTEM_PROMPT_JUDGE = """You are the 7Q Judge. You receive a previously scored 7Q assessment and verify it.

Your job:
1. Check every score for consistency with the evidence cited
2. Check for missed vulnerabilities
3. Check for inflated/deflated scores
4. Verify the math (T_RAW, XDM, T_FINAL)
5. Issue a PASS/ADJUST/FAIL verdict

If ADJUST, provide corrected scores with explanation.
If FAIL, explain what was fundamentally wrong.

Output your verdict in this format:
```judge
VERDICT: [PASS|ADJUST|FAIL]
ORIGINAL_T: [original T_final]
CORRECTED_T: [your T_final, if different]
ADJUSTMENTS: [list of changed scores with reasons]
MISSED_VULNS: [any vulnerabilities not flagged]
NOTES: [additional observations]
```
"""


# ═══════════════════════════════════════════════
# API INTERFACE
# ═══════════════════════════════════════════════

def call_openai(messages: list, model: str = "gpt-4o",
                api_key: str = None, temperature: float = 0.2) -> Optional[str]:
    """
    Call OpenAI API. Returns the response text or None on failure.

    Requires: pip install openai
    API key from: OPENAI_API_KEY env var or api_key parameter.
    """
    try:
        import openai
    except ImportError:
        print("  ERROR: openai package not installed. Run: pip install openai")
        return None

    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        print("  ERROR: No API key. Set OPENAI_API_KEY or pass api_key parameter.")
        return None

    client = openai.OpenAI(api_key=key)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=8000,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"  ERROR: API call failed: {e}")
        return None


def run_full_analysis(claim_text: str, claim_id: str = "CL-UNV-0001",
                      domain: str = "UNV", model: str = "gpt-4o",
                      api_key: str = None) -> Optional[str]:
    """Run the full LLM Maximum Rigor analysis on a claim."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_FULL},
        {"role": "user", "content": f"Analyze this claim with maximum rigor.\n\nCLAIM_ID: {claim_id}\nDOMAIN: {domain}\nCLAIM: {claim_text}"},
    ]
    print(f"  Sending to {model} for full 7Q analysis...")
    return call_openai(messages, model=model, api_key=api_key)


def run_compact_analysis(claim_text: str, claim_id: str = "CL-UNV-0001",
                         domain: str = "UNV", model: str = "gpt-4o",
                         api_key: str = None) -> Optional[str]:
    """Run compact scoring (faster, less thorough)."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_COMPACT},
        {"role": "user", "content": f"Score this claim.\n\nCLAIM_ID: {claim_id}\nDOMAIN: {domain}\nCLAIM: {claim_text}"},
    ]
    print(f"  Sending to {model} for compact scoring...")
    return call_openai(messages, model=model, api_key=api_key)


def run_judge(prior_assessment: str, model: str = "gpt-4o",
              api_key: str = None) -> Optional[str]:
    """Run the judge prompt to verify a prior assessment."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_JUDGE},
        {"role": "user", "content": f"Judge this 7Q assessment:\n\n{prior_assessment}"},
    ]
    print(f"  Sending to {model} for judge review...")
    return call_openai(messages, model=model, api_key=api_key)


def parse_scoring_block(text: str) -> dict:
    """
    Extract the machine-parseable scoring block from LLM output.
    Returns dict of field → value.
    """
    result = {}
    in_block = False
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped == "```scoring":
            in_block = True
            continue
        if stripped == "```" and in_block:
            break
        if in_block and ":" in stripped:
            key, _, val = stripped.partition(":")
            result[key.strip()] = val.strip()
    return result


def parse_knowledge_graph(text: str) -> dict:
    """Extract the knowledge graph YAML from LLM output."""
    try:
        import yaml
    except ImportError:
        print("  WARNING: PyYAML not installed. Cannot parse knowledge graph.")
        return {}

    in_block = False
    yaml_lines = []
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped == "```yaml":
            in_block = True
            continue
        if stripped == "```" and in_block:
            break
        if in_block:
            yaml_lines.append(line)

    if yaml_lines:
        try:
            return yaml.safe_load("\n".join(yaml_lines))
        except Exception:
            return {}
    return {}


# ═══════════════════════════════════════════════
# BATCH MODE
# ═══════════════════════════════════════════════

def batch_analyze(claims: list, model: str = "gpt-4o",
                  api_key: str = None) -> list:
    """
    Analyze multiple claims sequentially.
    Each claim should be a dict with: text, id, domain.
    Returns list of (claim_dict, response_text) tuples.
    """
    results = []
    for i, claim in enumerate(claims, 1):
        print(f"\n  ─── Claim {i}/{len(claims)}: {claim.get('id', '?')} ───")
        response = run_full_analysis(
            claim_text=claim["text"],
            claim_id=claim.get("id", f"CL-UNV-{i:04d}"),
            domain=claim.get("domain", "UNV"),
            model=model,
            api_key=api_key,
        )
        results.append((claim, response))
    return results


# ═══════════════════════════════════════════════
# QUICK TEST
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    # Test parsing (doesn't require API key)
    test_output = """
Some analysis text here...

```scoring
CLAIM_ID: CL-PHY-0001
DOMAIN: PHY
Q0: 1.0000
Q1: 0.9500
Q2: 0.5000
Q3: 0.8500
Q4: 0.7800
Q5: 0.8500
Q6: 0.9000
Q7: 0.9500
T_RAW: 0.8475
XDM: 1.30
T_FINAL: 0.8700
CLASS: ESTABLISHED
VULNS: []
CAPS: []
MODE: INVEST
```

```yaml
nodes:
  - id: CL-PHY-0001
    type: LAW
    domain: PHY
    score: 0.87
links:
  - from: CL-PHY-0001
    to: AX-MTH-0001
    type: DEP
```
"""
    scores = parse_scoring_block(test_output)
    print("Parsed scores:", json.dumps(scores, indent=2))

    kg = parse_knowledge_graph(test_output)
    print("Knowledge graph:", json.dumps(kg, indent=2))
