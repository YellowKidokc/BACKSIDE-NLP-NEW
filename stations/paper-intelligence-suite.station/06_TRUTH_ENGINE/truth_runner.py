"""
L6 Truth Engine — RICH MODE
============================
Wraps truth_coherence_scanner.analyze_document() and flattens its output into
~50 L6_* columns including the full Galatians fruits/anti-fruits pair, character
attributes, integrity profiles, and per-document truth/coherence metrics.

Replaces the old MiniLM-based 9-column scorer.

Public API (unchanged for orchestrator compatibility):
    score_paper(path_or_text, is_path=True) -> dict
"""
from __future__ import annotations
import sys
from pathlib import Path

# Make the scanner importable when called from the orchestrator (which sys.path-injects this folder)
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import truth_coherence_scanner as TCS  # noqa: E402


def _flatten_record(rec: TCS.DocumentRecord) -> dict:
    """DocumentRecord → flat dict of L6_* keys, Excel-safe (no nested dicts)."""
    out: dict = {
        # Core scores
        "truth_score":          rec.truth_score,
        "coherence_score":      rec.coherence_score,
        "combined_score":       rec.combined_score,

        # Density / pressure
        "evidence_density":     rec.evidence_density,
        "falsifiability_density": rec.falsifiability_density,
        "hedge_density":        rec.hedge_density,
        "contradiction_flags":  rec.contradiction_flags,
        "absolute_pressure":    rec.absolute_pressure,
        "rhetorical_force":     rec.rhetorical_force,

        # Spiritual posture
        "warmth_score":         rec.warmth_score,
        "discipline_score":     rec.discipline_score,
        "fruit_integrity_score": rec.fruit_integrity_score,
        "anti_fruit_pressure":  rec.anti_fruit_pressure,

        # Counts
        "sentence_count":       rec.sentence_count,
        "paragraph_count":      rec.paragraph_count,
        "section_count":        rec.section_count,

        # Claim breakdown
        "claim_count":              rec.claim_count,
        "anchored_claims":          rec.anchored_claims,
        "under_supported_claims":   rec.under_supported_claims,
        "overstated_claims":        rec.overstated_claims,
        "speculative_claims":       rec.speculative_claims,
        "contradictory_claims":     rec.contradictory_claims,
        "falsifiable_claims":       rec.falsifiable_claims,
    }

    # Per-fruit and per-anti-fruit columns (9 + 9 = 18)
    for key, val in rec.fruits_vector.items():
        out[f"fruit_{key}"] = val
    for key, val in rec.anti_fruits_vector.items():
        out[f"anti_{key}"] = val
        out[f"anti_fruit_{key}"] = val

    # Character attributes (8 attributes × 5 scalars = 40 columns)
    for name, attrs in rec.character_attributes.items():
        out[f"attr_{name}_kind"]             = attrs.get("kind", "")
        out[f"attr_{name}_pos_hits"]         = attrs.get("positive_hits", 0)
        out[f"attr_{name}_neg_hits"]         = attrs.get("negative_hits", 0)
        out[f"attr_{name}_strength"]         = attrs.get("strength", 0)
        out[f"attr_{name}_counter_pressure"] = attrs.get("counter_pressure", 0)
        out[f"attr_{name}_net_score"]        = attrs.get("net_score", 0)

    # Character profile rollup
    cp = rec.character_profile or {}
    out["threat_score"]        = cp.get("threat_score", 0)
    out["protection_score"]    = cp.get("protection_score", 0)
    out["balance_score"]       = cp.get("balance_score", 0)
    out["primary_threats"]     = "; ".join(cp.get("primary_threats", []) or [])
    out["primary_protections"] = "; ".join(cp.get("primary_protections", []) or [])

    # Label lists → semicolon-joined strings
    out["character_posture"]   = "; ".join(rec.character_posture or [])
    out["integrity_profiles"]  = "; ".join(rec.integrity_profiles or [])

    # Evidence excerpts (top supported / risky sentences)
    out["top_supported_1"] = (rec.top_supported_sentences[:1] or [""])[0]
    out["top_supported_2"] = (rec.top_supported_sentences[1:2] or [""])[0]
    out["top_risky_1"]     = (rec.top_risky_sentences[:1] or [""])[0]
    out["top_risky_2"]     = (rec.top_risky_sentences[1:2] or [""])[0]

    return out


def score_paper(path_or_text, is_path: bool = True) -> dict:
    """Score one paper. Returns flat L6_* dict, or {'L6_error': ...} on failure."""
    try:
        if is_path:
            p = Path(path_or_text)
            text = TCS.read_text_from_path(p)
            source = str(p)
            stype = "file"
        else:
            text = str(path_or_text)
            source = "inline"
            stype = "text"

        if not text or not text.strip():
            return {"error": "empty text"}

        rec, _sentences, _claims = TCS.analyze_document(source, text, stype)
        flat = _flatten_record(rec)
        return flat
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


if __name__ == "__main__":
    import json
    if len(sys.argv) < 2:
        print("usage: python truth_runner.py <paper.md>")
        sys.exit(1)
    result = score_paper(sys.argv[1])
    print(json.dumps(result, indent=2, default=str))
