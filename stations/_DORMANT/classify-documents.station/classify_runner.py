from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DOC_TYPES = {
    "foundational_paper",
    "empirical_study",
    "story",
    "apologetics",
    "technical_analysis",
    "meta_analysis",
    "devotional",
    "infrastructure",
}

TAG_KEYWORDS: dict[str, tuple[str, ...]] = {
    "pillar/philosophy": ("philosophy", "metaphysics", "epistemology", "ontology", "meaning"),
    "pillar/theology": ("theology", "god", "christ", "logos", "trinity", "scripture", "resurrection"),
    "pillar/physics": ("physics", "field", "entropy", "quantum", "relativity", "particle", "energy"),
    "pillar/mathematics": ("mathematics", "equation", "theorem", "proof", "axiom", "category", "function"),
    "pillar/consciousness": ("consciousness", "mind", "qualia", "awareness", "agency", "free will"),
    "pillar/information-theory": ("information", "signal", "entropy", "code", "encoding", "channel"),
    "master_equation": ("master equation", "χ", "chi", "nabla", "equation"),
    "logos/method": ("logos", "method", "rational", "word", "structure"),
    "structural-isomorphism": ("isomorphism", "isomorphic", "mapping", "homology", "structure preserving"),
    "entropy": ("entropy", "thermodynamic", "disorder"),
    "free_will": ("free will", "agency", "choice", "volition"),
    "trinity": ("trinity", "triune", "father", "son", "spirit"),
    "moral-conservation": ("moral conservation", "justice", "mercy", "moral law", "grace"),
    "boundary-proof": ("boundary proof", "boundary condition", "limit condition", "edge case"),
    "fruits-of-spirit": ("fruit of the spirit", "fruits of the spirit", "love", "joy", "peace", "patience"),
    "seven-q": ("7q", "seven q", "q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7"),
    "lean4-verified": ("lean4", "lean 4", "lake", "theorem", "formal verification"),
    "series/mda": ("mda", "moral decay", "america", "statistical spine"),
    "series/gtq": ("gtq", "grand theory", "theophysics"),
    "series/convergence": ("convergence", "alignment", "integrated", "cross-domain"),
    "series/logos-papers": ("logos papers", "logos", "formal theory"),
    "series/bible-study": ("bible study", "scripture", "biblical", "verse"),
    "method/lean4": ("lean4", "lean 4", "formal verification"),
    "method/jax": ("jax", "numpy", "gradient", "simulation"),
    "method/statistical": ("statistics", "statistical", "regression", "sigma", "dataset", "p-value"),
    "method/formal-proof": ("proof", "theorem", "lemma", "axiom", "derive", "qed"),
}

DOMAIN_KEYWORDS: dict[str, tuple[str, ...]] = {
    "physics": ("physics", "quantum", "entropy", "field", "relativity", "energy", "particle"),
    "theology": ("theology", "god", "christ", "logos", "trinity", "scripture", "resurrection"),
    "consciousness": ("consciousness", "mind", "qualia", "awareness", "agency", "free will"),
    "category_theory": ("category theory", "category", "functor", "morphism", "isomorphism", "mapping"),
    "evidence": ("evidence", "data", "empirical", "statistical", "sigma", "observed", "dataset"),
    "isomorphism": ("isomorphism", "isomorphic", "structural", "mapping", "correspondence"),
}

STATUS_BY_DOMAIN = {
    "physics": "Grounded",
    "theology": "Canonical",
    "consciousness": "Suggested",
    "category_theory": "Framework",
    "evidence": "Theoretical",
    "isomorphism": "Verified",
}

HARD_WORD_ALLOWLIST = {
    "isomorphism", "substrate", "spontaneous symmetry breaking", "thermodynamics",
    "epistemology", "eschatology", "consciousness", "canonical", "axiomatic",
    "homomorphism", "phenomenology", "soteriology", "pneumatology",
}

@dataclass(frozen=True)
class MappingSignal:
    domain: str
    keyword: str
    weight: int = 1


def read_text(path: str | Path) -> str:
    p = Path(path)
    if p.suffix.lower() == ".json":
        data = json.loads(p.read_text(encoding="utf-8-sig"))
        if isinstance(data, str):
            return data
        if isinstance(data, dict):
            for key in ("text", "content", "body", "markdown"):
                if isinstance(data.get(key), str):
                    return data[key]
        return json.dumps(data, ensure_ascii=False)
    return p.read_text(encoding="utf-8", errors="replace")


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z'\-]*", text)


def count_syllables(word: str) -> int:
    cleaned = re.sub(r"[^a-z]", "", word.lower())
    if not cleaned:
        return 0
    groups = re.findall(r"[aeiouy]+", cleaned)
    count = len(groups)
    if cleaned.endswith("e") and count > 1:
        count -= 1
    return max(count, 1)


def reading_level(text: str) -> dict[str, Any]:
    word_list = words(text)
    sentence_count = max(len(re.findall(r"[.!?]+", text)), 1)
    syllables = sum(count_syllables(word) for word in word_list)
    word_count = max(len(word_list), 1)
    grade = 0.39 * (word_count / sentence_count) + 11.8 * (syllables / word_count) - 15.59
    hard = sorted({
        w.lower().strip("-'") for w in word_list
        if len(w) >= 11 or count_syllables(w) >= 4
    } | {phrase for phrase in HARD_WORD_ALLOWLIST if phrase in text.lower()})
    return {
        "flesch_kincaid_grade": round(max(0.0, grade), 1),
        "hard_words": hard[:100],
        "hard_word_count": len(hard),
    }


def keyword_score(lower_text: str, terms: tuple[str, ...]) -> int:
    return sum(lower_text.count(term.lower()) for term in terms)


def load_mapping_signals(mapping_path: Path | None) -> list[MappingSignal]:
    if not mapping_path or not mapping_path.exists():
        return []
    if mapping_path.suffix.lower() == ".csv":
        with mapping_path.open(newline="", encoding="utf-8-sig") as handle:
            return _signals_from_rows(csv.DictReader(handle))
    if mapping_path.suffix.lower() in {".xlsx", ".xlsm"}:
        if importlib.util.find_spec("openpyxl") is None:
            return []
        import openpyxl
        wb = openpyxl.load_workbook(mapping_path, read_only=True, data_only=True)
        rows = []
        for ws in wb.worksheets:
            iterator = ws.iter_rows(values_only=True)
            headers = [str(v or "").strip().lower() for v in next(iterator, [])]
            for values in iterator:
                rows.append({headers[i]: values[i] for i in range(min(len(headers), len(values)))})
        return _signals_from_rows(rows)
    return []


def _signals_from_rows(rows: Any) -> list[MappingSignal]:
    signals: list[MappingSignal] = []
    known_domains = set(DOMAIN_KEYWORDS) | {"theology", "physics", "consciousness", "evidence", "isomorphism"}
    for row in rows:
        values = {str(k or "").lower(): str(v or "").strip() for k, v in dict(row).items()}
        joined = " ".join(v for v in values.values() if v)
        domain = next((d for d in known_domains if d.replace("_", " ") in joined.lower()), "")
        keyword = values.get("keyword") or values.get("term") or values.get("concept") or values.get("source") or joined[:80]
        if domain and keyword:
            signals.append(MappingSignal(domain=domain, keyword=keyword.lower()))
    return signals[:500]


def infer_doc_type(lower_text: str, word_count: int) -> str:
    scores = {
        "foundational_paper": keyword_score(lower_text, ("axiom", "foundation", "formal theory", "master equation", "framework")),
        "empirical_study": keyword_score(lower_text, ("dataset", "regression", "statistical", "survey", "sample", "p-value", "sigma")),
        "story": keyword_score(lower_text, ("story", "narrative", "chapter", "character", "parable")),
        "apologetics": keyword_score(lower_text, ("apologetic", "defense", "resurrection", "scripture", "gospel")),
        "technical_analysis": keyword_score(lower_text, ("analysis", "technical", "implementation", "architecture", "algorithm")),
        "meta_analysis": keyword_score(lower_text, ("meta-analysis", "literature review", "review of", "systematic review")),
        "devotional": keyword_score(lower_text, ("devotional", "prayer", "meditation", "worship")),
        "infrastructure": keyword_score(lower_text, ("pipeline", "station", "orchestrator", "infrastructure", "workflow", "tracker")),
    }
    if word_count < 500 and scores["infrastructure"]:
        return "infrastructure"
    return max(scores.items(), key=lambda item: item[1])[0] if any(scores.values()) else "technical_analysis"


def human_classification(doc_type: str, tags: list[str]) -> str:
    doc_label = doc_type.replace("_", " ").title()
    if "series/mda" in tags:
        return "Empirical / MDA" if doc_type == "empirical_study" else f"{doc_label} / MDA"
    if "pillar/physics" in tags:
        return "Technical / Physics" if doc_type in {"technical_analysis", "foundational_paper"} else f"{doc_label} / Physics"
    if "story" == doc_type or "series/bible-study" in tags:
        return "Story / Foundational" if doc_type == "story" else f"{doc_label} / Bible Study"
    if "pillar/theology" in tags:
        return f"{doc_label} / Theology"
    return doc_label


def infer_tags(lower_text: str) -> list[str]:
    tags = [tag for tag, terms in TAG_KEYWORDS.items() if keyword_score(lower_text, terms) > 0]
    if not any(tag.startswith("pillar/") for tag in tags):
        tags.append("pillar/philosophy")
    return sorted(dict.fromkeys(tags))


def infer_spine_mappings(lower_text: str, mapping_signals: list[MappingSignal]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    mapping_hits = {domain: 0 for domain in DOMAIN_KEYWORDS}
    for signal in mapping_signals:
        normalized = signal.domain if signal.domain in mapping_hits else signal.domain.replace(" ", "_")
        if normalized in mapping_hits and signal.keyword and signal.keyword in lower_text:
            mapping_hits[normalized] += signal.weight
    for domain, terms in DOMAIN_KEYWORDS.items():
        hits = keyword_score(lower_text, terms) + mapping_hits.get(domain, 0)
        score = max(0, min(100, hits * 15))
        status = STATUS_BY_DOMAIN[domain] if score else "None"
        if domain == "evidence" and score:
            sigma = re.search(r"(\d+(?:\.\d+)?)\s*(?:σ|sigma)", lower_text)
            status = f"{sigma.group(1)}σ" if sigma else "Theoretical"
        result[domain] = {"score": score, "status": status}
    return result


def infer_dependencies(text: str) -> dict[str, list[str]]:
    refs = sorted(set(re.findall(r"\b(?:A\d+\.\d+|FP-\d+|MDA-\d+|GTQ-\d+|OP\d+|PRED-\d+)\b", text)))
    upstream = [r for r in refs if r.startswith(("A", "FP-", "MDA-", "GTQ-"))]
    downstream = [r for r in refs if r.startswith(("PRED-", "OP"))]
    return {"upstream": upstream, "downstream": downstream}


def fallback_embedding(text: str, dim: int = 384) -> list[float]:
    vector = [0.0] * dim
    for token in words(text.lower())[:5000]:
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        vector[int.from_bytes(digest[:4], "little") % dim] += 1.0
    norm = math.sqrt(sum(v * v for v in vector))
    return [round(v / norm, 8) for v in vector] if norm else vector


def classify_text(text: str, source_name: str = "", cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    cfg = cfg or {}
    lower = text.lower()
    word_count = len(words(text))
    mapping_path_value = cfg.get("domain_mapping") or cfg.get("templates", {}).get("domain_mapping")
    mapping_path = Path(mapping_path_value) if mapping_path_value else None
    if mapping_path and not mapping_path.is_absolute():
        repo_root = Path(__file__).resolve().parents[2]
        mapping_path = repo_root / mapping_path.as_posix().replace("15_TEMPLATES/", "templates/")
    signals = load_mapping_signals(mapping_path)
    doc_type = infer_doc_type(lower, word_count)
    tags = infer_tags(lower)
    spine_mappings = infer_spine_mappings(lower, signals)
    classification = human_classification(doc_type, tags)
    reading = reading_level(text)
    return {
        "doc_type": doc_type,
        "classification": classification,
        "tags": tags,
        "spine_mappings": spine_mappings,
        "dependency_chain": infer_dependencies(text),
        "word_count": word_count,
        "reading_level": reading,
        "source_name": source_name,
        "embedding": {
            "model": "deterministic-keyword-fallback",
            "dim": 384,
            "vector": fallback_embedding(text) if cfg.get("include_embedding", False) else [],
        },
    }


def classify_file(path: str | Path, cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    p = Path(path)
    return classify_text(read_text(p), source_name=p.name, cfg=cfg)


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Classify documents into the BACKSIDE passport schema.")
    parser.add_argument("paths", nargs="*", type=Path, help="Files to classify; defaults to station _inbox")
    parser.add_argument("--out-dir", type=Path, default=Path(__file__).resolve().parent / "_outbox")
    parser.add_argument("--config", type=Path, default=Path(__file__).resolve().parent / "config.json")
    args = parser.parse_args()
    cfg = json.loads(args.config.read_text(encoding="utf-8-sig")) if args.config.exists() else {}
    paths = args.paths or sorted((Path(__file__).resolve().parent / "_inbox").glob("*"))
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for path in paths:
        if not path.is_file() or path.name.startswith("."):
            continue
        data = classify_file(path, cfg)
        out = args.out_dir / f"{path.stem}.classification.json"
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
