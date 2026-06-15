"""
OPENAI SENTENCE-LEVEL SCORER
==============================
Fills the voids that NLP/SBERT cannot reach:
  O. Sentence Type (claim/evidence/definition/derivation/question/narrative)
  P. Axiom Trace (which Codex axioms this sentence depends on)
  Q. Theory Match (established theories from literature)
  R. Isomorphic Bridge (0-1: physics-theology mapping quality)
  S. Logical Strength (0-1: does conclusion follow from premises?)
  T. Falsifiability (0-1: could this claim be empirically tested?)
  U. Missing Citations (specific authors/papers to reference)
  V. Strongest Objection (best counter-argument)

Batches ~10 sentences per API call to minimize cost.
Uses gpt-4o-mini for speed/cost, structured JSON output.
"""

import os
import json
import re
import time
from pathlib import Path
from typing import Optional

try:
    from openai import OpenAI
    _client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    HAS_OPENAI = True
except Exception:
    _client = None
    HAS_OPENAI = False

MODEL = "gpt-4o-mini"
BATCH_SIZE = 10  # sentences per API call

# ═══════════════════════════════════════════════════════════════
# SYSTEM PROMPT — teaches the model the Theophysics framework
# ═══════════════════════════════════════════════════════════════

SYSTEM_PROMPT = """You are analyzing sentences from a Theophysics research paper.

Theophysics is a framework that maps theology to physics via a formal axiom system:
- 193 axioms deriving from 3 primitives: Existence, Distinction, Information
- Master Equation: χ = ∭ (G·M·E·S·T·K·R·Q·F·C) dx dy dt
- 10 Laws mapping to physics: Gravitation/Grace, Motion/Grace-Force, EM/Truth, Strong/Love,
  Thermo/Harvest, Information/Logos, QM/Faith, Relativity/Eternal-Frame, Cosmo/Omega, Coherence/Christ
- 24 Properties establishing God ↔ Math isomorphism
- 9 Fruits of the Spirit mapped to physics equations (V(r) minima, resonance, equilibrium, etc.)

For each sentence, provide ALL of these fields:

1. "type": one of ["claim", "evidence", "definition", "derivation", "question", "narrative", "transition", "equation"]
2. "axiom_deps": list of axiom numbers (1-193) this sentence logically depends on, or [] if none apparent
3. "axiom_notes": brief note on WHY those axioms apply (max 30 words)
4. "theories": list of established scientific theories/frameworks this relates to (use real names: "Noether's theorem", "Shannon information theory", etc.)
5. "bridge_score": float 0.0-1.0 — how strong is the physics-theology mapping in this sentence? 0=no mapping, 1=rigorous isomorphism
6. "bridge_note": why this score (max 20 words)
7. "logic_score": float 0.0-1.0 — does the conclusion follow from stated premises? 0=non-sequitur, 1=valid deduction
8. "falsifiable": float 0.0-1.0 — could this specific claim be empirically/formally tested? 0=unfalsifiable, 1=directly testable
9. "missing_citations": list of specific authors/papers that should be cited (real ones only, max 3)
10. "strongest_objection": the single best counter-argument to this sentence (max 40 words, or "" if not a claim)

Be honest and rigorous. This is for STRENGTHENING the paper, not validating it.
Return valid JSON array matching the input sentence order."""


def _build_batch_prompt(sentences: list[dict], batch_idx: int) -> str:
    """Build the user prompt for a batch of sentences."""
    lines = [f"Analyze these {len(sentences)} sentences (batch {batch_idx + 1}):\n"]
    for i, s in enumerate(sentences):
        lines.append(f"[{i}] \"{s['text']}\"")
    lines.append("\nReturn a JSON array of objects, one per sentence, in order.")
    return "\n".join(lines)


def score_sentences(sentences: list[str], paper_name: str = "",
                    cache_dir: Optional[str] = None) -> list[dict]:
    """
    Score sentences using OpenAI. Returns list of score dicts aligned to input.

    Args:
        sentences: list of sentence strings
        paper_name: for cache key
        cache_dir: directory to cache results (avoids re-calling)
    """
    if not HAS_OPENAI:
        print("  ERROR: OpenAI not configured")
        return [{}] * len(sentences)

    # Check cache
    if cache_dir and paper_name:
        cache_path = Path(cache_dir) / f"{paper_name}_openai_scores.json"
        if cache_path.exists():
            print(f"  Using cached OpenAI scores: {cache_path.name}")
            cached = json.loads(cache_path.read_text(encoding='utf-8'))
            if len(cached) == len(sentences):
                return cached
            print(f"  Cache size mismatch ({len(cached)} vs {len(sentences)}), re-scoring...")

    # Prepare sentence dicts
    sent_dicts = [{"text": s, "idx": i} for i, s in enumerate(sentences)]

    # Batch and call
    all_results = [None] * len(sentences)
    n_batches = (len(sent_dicts) + BATCH_SIZE - 1) // BATCH_SIZE
    total_tokens = 0

    print(f"  OpenAI scoring: {len(sentences)} sentences in {n_batches} batches (model: {MODEL})")

    for batch_idx in range(n_batches):
        start = batch_idx * BATCH_SIZE
        end = min(start + BATCH_SIZE, len(sent_dicts))
        batch = sent_dicts[start:end]

        prompt = _build_batch_prompt(batch, batch_idx)

        try:
            response = _client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=3000,
                temperature=0.2,
                response_format={"type": "json_object"}
            )

            text = response.choices[0].message.content
            usage = response.usage
            total_tokens += usage.total_tokens if usage else 0

            # Parse — expect {"results": [...]} or just [...]
            parsed = json.loads(text)
            if isinstance(parsed, dict):
                # Try common wrapper keys
                for key in ('results', 'sentences', 'analysis', 'data'):
                    if key in parsed:
                        parsed = parsed[key]
                        break
                else:
                    # If it's a dict with numeric keys
                    if all(k.isdigit() for k in parsed.keys()):
                        parsed = [parsed[str(i)] for i in range(len(batch))]
                    else:
                        parsed = [parsed]  # single result

            if isinstance(parsed, list):
                for i, result in enumerate(parsed):
                    if start + i < len(sentences):
                        all_results[start + i] = _normalize_result(result)

            print(f"    Batch {batch_idx + 1}/{n_batches} — {usage.total_tokens if usage else '?'} tokens")

        except Exception as e:
            print(f"    Batch {batch_idx + 1} ERROR: {e}")
            for i in range(start, end):
                all_results[i] = _empty_result()

        # Rate limit courtesy
        if batch_idx < n_batches - 1:
            time.sleep(0.5)

    # Fill any None gaps
    for i in range(len(all_results)):
        if all_results[i] is None:
            all_results[i] = _empty_result()

    print(f"  OpenAI complete: {total_tokens:,} total tokens")

    # Cache
    if cache_dir and paper_name:
        cache_path = Path(cache_dir) / f"{paper_name}_openai_scores.json"
        Path(cache_dir).mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(all_results, indent=2, ensure_ascii=False),
                              encoding='utf-8')
        print(f"  Cached: {cache_path.name}")

    return all_results


def _normalize_result(raw: dict) -> dict:
    """Normalize a single result dict to expected schema."""
    TYPE_MAP = {
        'claim': 'claim', 'claims': 'claim',
        'evidence': 'evidence', 'support': 'evidence',
        'definition': 'definition', 'def': 'definition',
        'derivation': 'derivation', 'derive': 'derivation',
        'question': 'question', 'inquiry': 'question',
        'narrative': 'narrative', 'exposition': 'narrative',
        'transition': 'transition', 'connector': 'transition',
        'equation': 'equation', 'formula': 'equation',
    }

    return {
        'type': TYPE_MAP.get(str(raw.get('type', 'narrative')).lower(), 'narrative'),
        'axiom_deps': _safe_list(raw.get('axiom_deps', [])),
        'axiom_notes': str(raw.get('axiom_notes', ''))[:200],
        'theories': _safe_list(raw.get('theories', [])),
        'bridge_score': _safe_float(raw.get('bridge_score', 0)),
        'bridge_note': str(raw.get('bridge_note', ''))[:100],
        'logic_score': _safe_float(raw.get('logic_score', 0)),
        'falsifiable': _safe_float(raw.get('falsifiable', 0)),
        'missing_citations': _safe_list(raw.get('missing_citations', [])),
        'strongest_objection': str(raw.get('strongest_objection', ''))[:300],
    }


def _empty_result() -> dict:
    return {
        'type': 'narrative',
        'axiom_deps': [],
        'axiom_notes': '',
        'theories': [],
        'bridge_score': 0.0,
        'bridge_note': '',
        'logic_score': 0.0,
        'falsifiable': 0.0,
        'missing_citations': [],
        'strongest_objection': '',
    }


def _safe_float(v) -> float:
    try:
        return max(0.0, min(1.0, float(v)))
    except (ValueError, TypeError):
        return 0.0


def _safe_list(v) -> list:
    if isinstance(v, list):
        return [str(x) for x in v]
    if isinstance(v, str):
        return [x.strip() for x in v.split(',') if x.strip()]
    return []


# ═══════════════════════════════════════════════════════════════
# SENTENCE TYPE → NUMERIC ENCODING (for Excel heat coloring)
# ═══════════════════════════════════════════════════════════════

SENTENCE_TYPE_ENCODING = {
    'claim': 1.0,
    'evidence': 0.8,
    'derivation': 0.9,
    'definition': 0.7,
    'equation': 0.85,
    'question': 0.5,
    'narrative': 0.3,
    'transition': 0.1,
}


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        paper = Path(sys.argv[1])
        text = paper.read_text(encoding='utf-8', errors='replace')
        text = re.sub(r'^---.*?---', '', text, flags=re.DOTALL)
        text = re.sub(r'#+\s+', '', text)
        sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if len(s.strip()) > 20]
        print(f"Scoring {len(sents)} sentences from {paper.name}")
        results = score_sentences(sents, paper.stem,
                                  cache_dir=str(paper.parent / '_openai_cache'))
        for i, r in enumerate(results[:5]):
            print(f"\n[{i}] {sents[i][:80]}...")
            print(f"    type={r['type']}  bridge={r['bridge_score']:.2f}  logic={r['logic_score']:.2f}  falsifiable={r['falsifiable']:.2f}")
            print(f"    theories={r['theories']}")
            print(f"    objection={r['strongest_objection'][:80]}")
    else:
        print("Usage: python openai_sentence_scorer.py <paper.md>")
