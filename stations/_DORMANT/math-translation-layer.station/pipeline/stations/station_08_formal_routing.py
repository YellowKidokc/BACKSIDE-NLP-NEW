from __future__ import annotations

from pathlib import Path
from typing import Any

from pipeline.stations.common import paper_output_dir, read_json, utc_now, write_json


TARGET_LEAN = "Lean"
TARGET_PYTHON = "Python/state-model"
TARGET_SPEC = "Alloy/TLA-style spec"
TARGET_BRIDGE = "Bridge-only / not formal yet"

LEAN_HINTS = {
    "no-drift": "no-drift topology",
    "topology": "no-drift topology",
    "canonical law order": "canonical law order",
    "law order": "canonical law order",
    "law 9": "terminal asymmetry of Law 9 and Law 10",
    "law 10": "terminal asymmetry of Law 9 and Law 10",
    "signature": "physical equation signature",
    "physical equation": "physical equation signature",
    "spiritual side": "spiritual side signature",
    "alias": "approved alias normalization",
    "closure": "closure theorem",
    "theorem": "formal theorem skeleton",
    "necessary condition": "necessary-condition lemma",
    "sign invariance": "sign-invariance lemma",
}


def _typing_by_claim(output_dir: Path) -> dict[str, dict[str, Any]]:
    path = output_dir / "04_claim_typing.json"
    if not path.exists():
        raise FileNotFoundError("Station 08 requires 04_claim_typing.json from Partner B.")
    payload = read_json(path)
    items = payload.get("claim_typing") or payload.get("claims") or payload.get("typed_claims") or []
    return {item["claim_uuid"]: item for item in items if "claim_uuid" in item}


def _domain_badges(typing: dict[str, Any]) -> list[str]:
    badges = typing.get("domain_badges") or []
    return [str(badge) for badge in badges]


def _lean_hints(text: str) -> list[str]:
    lower = text.lower()
    hints = [hint for key, hint in LEAN_HINTS.items() if key in lower]
    return sorted(set(hints))


def _route_claim(claim: dict[str, Any], typing: dict[str, Any]) -> dict[str, Any]:
    text = str(claim.get("claim_text", ""))
    lower = text.lower()
    badges = _domain_badges(typing)
    equation_needed = bool(typing.get("equation_semantics_needed"))
    claim_type = str(typing.get("claim_type") or claim.get("claim_type") or "untyped")
    overstatement_flags = typing.get("overstatement_flags") or []

    if "master equation" in lower:
        primary = TARGET_BRIDGE
        reason = "Master Equation claim is routed as framework bridge/audit context, not as a law-level physical equation."
        candidates = [TARGET_BRIDGE]
        hints: list[str] = []
    elif any(term in lower for term in ["law order", "canonical law", "no-drift", "topology", "signature", "law 9", "law 10"]):
        primary = TARGET_LEAN
        reason = "Law-order, topology, signature, or terminal-asymmetry language is suitable for Lean dependency checks."
        candidates = [TARGET_LEAN]
        hints = _lean_hints(lower)
    elif any(term in lower for term in ["closure", "theorem", "necessary condition", "sign invariance", "cannot", "impossible"]):
        primary = TARGET_LEAN
        reason = "Formal necessity or theorem-style language needs proof-target routing before public use."
        candidates = [TARGET_LEAN, TARGET_SPEC]
        hints = _lean_hints(lower) or ["formal theorem skeleton"]
    elif any(term in lower for term in ["state", "operation", "restore", "trapped", "only", "self-repair", "dependency"]):
        primary = TARGET_SPEC
        reason = "State transition or allowed-operation language fits an Alloy/TLA-style model."
        candidates = [TARGET_SPEC, TARGET_LEAN]
        hints = _lean_hints(lower)
    elif equation_needed or any(term in lower for term in ["equation", "model", "phase", "signal", "capacity", "predicts", "operator"]):
        primary = TARGET_PYTHON
        reason = "Equation or dynamical-model language should be tested as a computable state model first."
        candidates = [TARGET_PYTHON]
        hints = _lean_hints(lower)
    elif "bridge" in claim_type or "bridge" in lower or "ANALOGY" in badges or ("PHYSICS" in badges and "THEOLOGY" in badges):
        primary = TARGET_BRIDGE
        reason = "Cross-domain bridge language needs domain-boundary review before formalization."
        candidates = [TARGET_BRIDGE]
        hints = []
    else:
        primary = TARGET_BRIDGE
        reason = "No stable formal target detected from deterministic heuristics."
        candidates = [TARGET_BRIDGE]
        hints = []

    if overstatement_flags and primary == TARGET_BRIDGE:
        candidates = sorted(set(candidates + [TARGET_LEAN]))

    return {
        "claim_uuid": claim["claim_uuid"],
        "claim_text": text,
        "primary_target": primary,
        "target_candidates": candidates,
        "likely_lean_dependencies": hints,
        "master_equation_guardrail": "master equation" in lower,
        "reason": reason,
        "source": f"section:{claim.get('section_heading') or 'Untitled'}",
    }


def run(paper_uuid: str) -> dict[str, Any]:
    output_dir = paper_output_dir(paper_uuid)
    claims = read_json(output_dir / "03_claims.json")["claims"]
    typing = _typing_by_claim(output_dir)

    targets = [_route_claim(claim, typing.get(claim["claim_uuid"], {})) for claim in claims]
    target_counts: dict[str, int] = {}
    for target in targets:
        target_counts[target["primary_target"]] = target_counts.get(target["primary_target"], 0) + 1

    payload = {
        "paper_uuid": paper_uuid,
        "station": "08_formal_routing",
        "timestamp": utc_now(),
        "targets": targets,
        "target_counts": target_counts,
        "guardrails": [
            "Master Equation is not routed as a law-level physical equation.",
            "Bridge-only means not formal yet, not rejected.",
        ],
    }
    write_json(output_dir / "08_formal_targets.json", payload)
    write_human(output_dir / "08_formal_targets_human.md", payload)
    return payload


def write_human(path: Path, payload: dict[str, Any]) -> None:
    lines = [f"# Formal Routing - {payload['paper_uuid']}", ""]
    lines += ["## Target Counts", ""]
    for target, count in sorted(payload["target_counts"].items()):
        lines.append(f"- {target}: {count}")
    lines += ["", "## Claim Targets", ""]
    for item in payload["targets"]:
        lines += [
            f"### Claim {item['claim_uuid'][:8]}",
            f"- Primary target: {item['primary_target']}",
            f"- Candidates: {', '.join(item['target_candidates'])}",
            f"- Lean hints: {', '.join(item['likely_lean_dependencies']) or 'none'}",
            f"- Reason: {item['reason']}",
            "",
        ]
    path.write_text("\n".join(lines), encoding="utf-8")
