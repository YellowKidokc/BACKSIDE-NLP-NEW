from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_REGISTRY = Path(__file__).resolve().parent / "registry" / "site_feature_registry.json"


BIBLE_RE = re.compile(
    r"\b(?:Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth|"
    r"Matthew|Mark|Luke|John|Acts|Romans|Ephesians|Revelation)\s+\d{1,3}:\d{1,3}",
    re.I,
)
CLAIM_RE = re.compile(r"\b(claim|therefore|implies|requires|proves|evidence|control group|if .+ then)\b", re.I)
EQUATION_RE = re.compile(r"(\\chi|χ|\\\[|\\\(|\$\$|[A-Za-z_][A-Za-z0-9_{}]*\s*=)")
TABLE_RE = re.compile(r"(^\s*\|.+\|\s*$|<table\b)", re.I | re.M)
PULL_QUOTE_RE = re.compile(r"(^>\s+|\bpull quote\b|class=[\"']pull-quote)", re.I | re.M)
CITATION_RE = re.compile(r"\b(doi:|DOI|et al\.|Journal|citation_needed|\[CITATION NEEDED\])\b", re.I)
SATURDAY_RE = re.compile(r"\b(Saturday|Sabbath|weekend edition)\b", re.I)
PROOF_RE = re.compile(r"\b(proof|theorem|lemma|formal verification|Lean|Alloy)\b", re.I)
GLOSSARY_RE = re.compile(r"\b(glossary|term inventory|defined as|definition)\b", re.I)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace").replace("\r\n", "\n").replace("\r", "\n")


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def paragraph_count(text: str) -> int:
    blocks = [block.strip() for block in re.split(r"\n\s*\n", text) if block.strip()]
    return len(blocks)


def rough_flesch_kincaid_grade(text: str) -> float:
    words = re.findall(r"\b[a-zA-Z]+\b", text)
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    if not words or not sentences:
        return 0.0
    syllables = sum(max(1, len(re.findall(r"[aeiouyAEIOUY]+", word))) for word in words)
    return round(0.39 * (len(words) / len(sentences)) + 11.8 * (syllables / len(words)) - 15.59, 2)


def sidecar_candidates(path: Path) -> dict[str, str]:
    stem = path.with_suffix("")
    candidates = {
        "easy": f"{stem}.easy.md",
        "academic": f"{stem}.academic.md",
        "claims": f"{stem}.claims.json",
        "math": f"{stem}.math.json",
    }
    return {key: value for key, value in candidates.items() if Path(value).exists()}


def detect_series(path: Path, text: str) -> str:
    match = re.search(r"\b(MDA|GTQ)-\d{3}\b", path.name + "\n" + text)
    return match.group(1) if match else "unknown"


def load_registry(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def scan(path: Path, registry_path: Path) -> dict[str, Any]:
    text = read_text(path)
    sidecars = sidecar_candidates(path)
    grade = rough_flesch_kincaid_grade(text)
    series = detect_series(path, text)
    features = {
        "title": bool(re.search(r"^#\s+|<h1\b|<title\b", text, re.I | re.M)),
        "series": series,
        "paragraph_count": paragraph_count(text),
        "word_count": word_count(text),
        "has_equations": bool(EQUATION_RE.search(text)),
        "equation_count_estimate": len(EQUATION_RE.findall(text)),
        "has_claims": bool(CLAIM_RE.search(text) or "claims" in sidecars),
        "claim_marker_count_estimate": len(CLAIM_RE.findall(text)),
        "has_bible_references": bool(BIBLE_RE.search(text)),
        "bible_reference_count": len(BIBLE_RE.findall(text)),
        "has_academic_citations": bool(CITATION_RE.search(text)),
        "has_glossary_terms": bool(GLOSSARY_RE.search(text)),
        "has_pull_quotes": bool(PULL_QUOTE_RE.search(text)),
        "has_tables": bool(TABLE_RE.search(text)),
        "has_saturday_section": bool(SATURDAY_RE.search(text)),
        "has_proof_blocks": bool(PROOF_RE.search(text)),
        "reading_level_grade": grade,
        "reading_level": "easy" if grade <= 8 else "standard" if grade <= 12 else "academic",
        "has_easy_sidecar": "easy" in sidecars,
        "has_academic_sidecar": "academic" in sidecars,
        "has_claims_sidecar": "claims" in sidecars,
        "has_math_sidecar": "math" in sidecars,
    }

    missing_optional = []
    if not features["has_easy_sidecar"]:
        missing_optional.append("easy_version")
    if not features["has_academic_sidecar"]:
        missing_optional.append("academic_version")
    if features["has_claims"] and not features["has_claims_sidecar"]:
        missing_optional.append("claims_sidecar")
    if features["has_equations"] and not features["has_math_sidecar"]:
        missing_optional.append("math_layer")

    unknown_patterns = []
    for idx, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if re.match(r"^[-=*_]{5,}$", stripped):
            unknown_patterns.append(f"custom divider at line {idx}")
        if stripped.startswith("<!--") and "feature:" not in stripped and "level:" not in stripped and len(unknown_patterns) < 20:
            unknown_patterns.append(f"unrecognized html comment at line {idx}")

    return {
        "schema": "theophysics.feature_manifest.v1",
        "source_file": str(path),
        "scanned_at": datetime.now(timezone.utc).isoformat(),
        "registry": str(registry_path),
        "detected_features": features,
        "missing_optional_features": missing_optional,
        "unknown_patterns": unknown_patterns[:50],
        "sidecar_candidates": sidecars,
        "builder_gates": {
            "can_render_standard": True,
            "can_render_easy": features["has_easy_sidecar"],
            "can_render_academic": features["has_academic_sidecar"],
            "can_render_claims": features["has_claims_sidecar"],
            "can_render_math": features["has_math_sidecar"],
            "requires_review": bool(unknown_patterns),
        },
        "known_features": sorted(load_registry(registry_path).get("features", {}).keys()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan an article for known page compiler features.")
    parser.add_argument("article", type=Path)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    manifest = scan(args.article, args.registry)
    out = args.out or args.article.with_suffix(".feature_manifest.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "out": str(out),
        "series": manifest["detected_features"]["series"],
        "paragraphs": manifest["detected_features"]["paragraph_count"],
        "claims_estimate": manifest["detected_features"]["claim_marker_count_estimate"],
        "equations_estimate": manifest["detected_features"]["equation_count_estimate"],
        "missing_optional_features": manifest["missing_optional_features"],
        "requires_review": manifest["builder_gates"]["requires_review"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
