"""
ST-PUB-001 — Publication Gate.

Read all upstream artifacts and decide where the paper goes:
    website / substack / zenodo / proof_explorer / obsidian_canon / review / archive

Decision is rule-based, transparent, and overridable.

Usage:
    python run.py --in <input_dir> --out <publication_status.yml>
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

STATION_ID = "ST-PUB-001"


def load_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def has_file(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0


def check_readiness(input_dir: Path) -> dict:
    """Return a checklist dict — each key is a readiness criterion."""
    claims = load_json(input_dir / "claims.json") or {}
    forward = load_json(input_dir / "forward_7q.json") or {}
    reverse = load_json(input_dir / "reverse_7q.json") or {}
    evidence = load_json(input_dir / "evidence_7q.json") or {}
    graph = load_json(input_dir / "graph.json") or {}

    claim_count = len(claims.get("claims", [])) if isinstance(claims, dict) else 0
    verdict = str(reverse.get("verdict", "")).lower()
    confidence = reverse.get("confidence_score", 0)
    try:
        confidence = float(confidence)
    except (TypeError, ValueError):
        confidence = 0.0

    ev_items = evidence.get("evidence", []) if isinstance(evidence, dict) else []
    ev_gaps = evidence.get("gaps", []) if isinstance(evidence, dict) else []
    conflicting = sum(1 for e in ev_items if e.get("class") == "conflicting")

    checks = {
        "claims_extracted":       claim_count > 0,
        "lossless_summary_exists": has_file(input_dir / "summary.lossless.md"),
        "reverse_pass_survived":  "surviv" in verdict or "passes" in verdict,
        "confidence_above_0_5":   confidence >= 0.5,
        "evidence_classified":    len(ev_items) > 0,
        "evidence_gaps_acceptable": len(ev_gaps) <= 3,
        "graph_built":            graph.get("node_count", 0) > 0,
        "no_unresolved_contradictions": conflicting == 0,
    }
    return {
        "checks": checks,
        "passed": sum(1 for v in checks.values() if v),
        "total":  len(checks),
        "metrics": {
            "claim_count":         claim_count,
            "verdict":             verdict,
            "confidence_score":    confidence,
            "evidence_items":      len(ev_items),
            "evidence_gaps":       len(ev_gaps),
            "conflicting_evidence": conflicting,
            "graph_node_count":    graph.get("node_count", 0),
        },
    }


def recommend(checks: dict, metrics: dict) -> tuple[str, str]:
    passed = sum(1 for v in checks.values() if v)
    total = len(checks)
    ratio = passed / total if total else 0

    if not checks["claims_extracted"]:
        return ("archive", "No claims extracted. Paper went through pipeline but produced nothing actionable.")
    if not checks["reverse_pass_survived"]:
        return ("review", "Reverse pass did NOT mark the claim as surviving. Human review needed before any publication step.")
    if metrics["conflicting_evidence"] > 2:
        return ("review", f"{metrics['conflicting_evidence']} conflicting evidence items — resolve before publication.")
    if ratio >= 0.9 and metrics["confidence_score"] >= 0.8:
        return ("proof_explorer", "All gates green and confidence high — promote to Proof Explorer / Obsidian Canon.")
    if ratio >= 0.75:
        return ("website", "Most gates green — publish to website (faiththruphysics.com / theophysics.pro).")
    if ratio >= 0.6:
        return ("substack", "Solid but provisional — publish to Substack as a working draft.")
    if checks["claims_extracted"] and checks["lossless_summary_exists"]:
        return ("zenodo", "Has structure but gates incomplete — deposit on Zenodo for record while addressing gaps.")
    return ("review", f"{passed}/{total} gates passed — needs work before any publication step.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="inp", required=True)
    parser.add_argument("--out", dest="out", required=True)
    args = parser.parse_args()

    inp_path = Path(args.inp)
    if inp_path.is_file():
        inp_path = inp_path.parent
    readiness = check_readiness(inp_path)
    destination, rationale = recommend(readiness["checks"], readiness["metrics"])

    status = {
        "station":     STATION_ID,
        "input_dir":   str(inp_path),
        "passed":      readiness["passed"],
        "total":       readiness["total"],
        "destination": destination,
        "rationale":   rationale,
        "checks":      readiness["checks"],
        "metrics":     readiness["metrics"],
        "decided_at":  datetime.now().isoformat(timespec="seconds"),
    }

    # YAML-ish output (flat for the top, nested for checks/metrics).
    out_path = Path(args.out)
    lines = []
    for k in ("station", "input_dir", "passed", "total", "destination", "rationale", "decided_at"):
        v = status[k]
        if isinstance(v, str):
            v_str = '"' + v.replace('"', '\\"') + '"'
        else:
            v_str = str(v)
        lines.append(f"{k}: {v_str}")
    lines.append("checks:")
    for ck, cv in status["checks"].items():
        lines.append(f"  {ck}: {str(cv).lower()}")
    lines.append("metrics:")
    for mk, mv in status["metrics"].items():
        lines.append(f"  {mk}: {json.dumps(mv)}")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Companion human-readable recommendation
    md = [
        f"# {STATION_ID} — Publication Recommendation",
        "",
        f"**Destination:** `{destination}`",
        "",
        f"**Rationale:** {rationale}",
        "",
        f"**Gates passed:** {readiness['passed']}/{readiness['total']}",
        "",
        "## Checklist",
        "",
    ]
    for ck, cv in status["checks"].items():
        md.append(f"- [{'x' if cv else ' '}] {ck.replace('_', ' ')}")
    md += ["", "## Metrics", ""]
    for mk, mv in status["metrics"].items():
        md.append(f"- **{mk}**: {mv}")
    out_path.with_name("release_recommendation.md").write_text("\n".join(md), encoding="utf-8")

    print(json.dumps({"status": "ok", "destination": destination,
                      "passed": readiness["passed"], "total": readiness["total"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
