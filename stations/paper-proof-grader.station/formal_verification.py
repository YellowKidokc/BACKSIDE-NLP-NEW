from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


STATUS_PROVEN = "proven"
STATUS_COUNTERMODEL = "counterexample_found"
STATUS_CANDIDATE = "formalizable"
STATUS_BRIDGE = "bridge_only"
STATUS_SPECULATIVE = "speculative"
STATUS_NOT_ATTEMPTED = "not_attempted"


LEAN_DEPENDENCIES = {
    "closure": ["lean/ClosureTheorem.lean", "lean/T1SpineClosure.lean"],
    "sign_invariance": ["lean/SignInvariance.lean"],
    "targeted_openness": ["lean/TargetedOpenness.lean", "lean/OpennessGrace.lean"],
    "external_grace": ["lean/ExternalGraceRequired.lean", "lean/OpennessGrace.lean"],
    "necessary_conditions": ["lean/NecessaryConditions.lean"],
    "justice_mercy_transform": ["lean/JusticeMercyTransform.lean"],
}


THEOREM_PATTERNS = [
    (
        "closure",
        re.compile(
            r"\b(closure|self[- ]repair|self[- ]generated|broken.+fix|error[- ]closed|reference state)\b",
            re.I,
        ),
    ),
    (
        "sign_invariance",
        re.compile(r"\b(sign invariance|orientation|toward|away|cannot.+reverse|goldstone)\b", re.I),
    ),
    (
        "targeted_openness",
        re.compile(r"\b(open(ness)? to|false target|counterfeit|lord lord|false vacuum|o[_ -]?[rf])\b", re.I),
    ),
    (
        "external_grace",
        re.compile(r"\b(external grace|external operator|grace required|outside.+system|g\s*=|o\s*[·*]\s*g)\b", re.I),
    ),
    (
        "necessary_conditions",
        re.compile(r"\b(product|χ|chi|necessary condition|zero.+coherence|one zero|integrated coherence)\b", re.I),
    ),
    (
        "justice_mercy_transform",
        re.compile(r"\b(justice|mercy|transformation|j\s*∧\s*m|cost[- ]bear|cross)\b", re.I),
    ),
]


def verification_for_claim(claim: dict) -> dict:
    text = " ".join(
        str(claim.get(key, ""))
        for key in ("one_sentence_claim", "section", "nearby_equation", "proof_boundary")
    )
    dependencies = [
        theorem_id
        for theorem_id, pattern in THEOREM_PATTERNS
        if pattern.search(text)
    ]
    lower = text.lower()
    has_formal_language = bool(re.search(r"\b(theorem|proof|proves|machine[- ]checked|lean|formal)\b", lower))
    has_bridge_language = bool(re.search(r"\b(bridge|analogy|isomorphism|maps? to|corresponds|physics)\b", lower))
    has_empirical_language = bool(re.search(r"\b(data|measurement|experiment|empirical|correlation|p[- ]?value|sigma)\b", lower))

    if "counterexample" in lower or "countermodel" in lower:
        status = STATUS_COUNTERMODEL
    elif dependencies and has_formal_language:
        status = STATUS_CANDIDATE
    elif dependencies:
        status = STATUS_CANDIDATE
    elif has_bridge_language:
        status = STATUS_BRIDGE
    elif has_empirical_language:
        status = STATUS_NOT_ATTEMPTED
    else:
        status = STATUS_SPECULATIVE

    if status == STATUS_CANDIDATE and not dependencies:
        status = STATUS_NOT_ATTEMPTED

    return {
        "lean": status if dependencies else STATUS_NOT_ATTEMPTED,
        "alloy": "not_configured",
        "state_model": "not_applicable",
        "bridge_status": "formal_candidate" if dependencies else ("bridge" if has_bridge_language else "unclassified"),
        "theorem_dependencies": dependencies,
        "lean_files": sorted({path for dep in dependencies for path in LEAN_DEPENDENCIES.get(dep, [])}),
        "formalization_note": formalization_note(status, dependencies, has_bridge_language),
    }


def formalization_note(status: str, dependencies: list[str], has_bridge_language: bool) -> str:
    if status == STATUS_CANDIDATE:
        return (
            "Candidate for formal attachment; verify exact Lean theorem exists before labeling as proven."
            if dependencies
            else "Formal language present, but no known theorem dependency was detected."
        )
    if status == STATUS_BRIDGE or has_bridge_language:
        return "Bridge/isomorphism language detected; keep category boundary explicit."
    if status == STATUS_NOT_ATTEMPTED:
        return "Measurable or empirical claim; route to data/statistical validation, not Lean first."
    return "No formal dependency detected by deterministic pass."


def attach_verification(claims: list[dict]) -> dict:
    counts: Counter[str] = Counter()
    dependencies: Counter[str] = Counter()
    for claim in claims:
        layer = verification_for_claim(claim)
        claim["formal_verification"] = layer
        counts[layer["lean"]] += 1
        for dep in layer["theorem_dependencies"]:
            dependencies[dep] += 1
    return {
        "schema_version": "formal-verification-layer/v0.1",
        "lean": {
            "proven": counts[STATUS_PROVEN],
            "formalizable": counts[STATUS_CANDIDATE],
            "counterexample_found": counts[STATUS_COUNTERMODEL],
            "not_attempted": counts[STATUS_NOT_ATTEMPTED],
            "speculative": counts[STATUS_SPECULATIVE],
        },
        "alloy": {
            "status": "not_configured",
            "note": "Counterexample search lane reserved; install Alloy specs after the station contract settles.",
        },
        "state_model": {
            "status": "not_configured",
            "note": "Use TLA+/Maude only for claims with explicit state-transition dynamics.",
        },
        "bridge_status": {
            "formal_candidate_dependencies": dict(sorted(dependencies.items())),
        },
    }


def write_dependency_map(path: Path) -> None:
    lines = [
        "# Formal Verification Dependency Map",
        "",
        "This file is generated/maintained for the paper-proof-grader verification layer.",
        "It maps detected claim families to the intended Lean attachment files.",
        "",
    ]
    for theorem_id, files in LEAN_DEPENDENCIES.items():
        lines.append(f"## {theorem_id}")
        lines.append("")
        for file in files:
            lines.append(f"- `{file}`")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
