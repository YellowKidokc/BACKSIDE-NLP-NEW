from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "lossless_context_compression.semantic_address.v1"
TIE_BREAK = ["E", "C", "G", "K", "M", "T", "R", "F", "S", "Q"]
VECTOR_ORDER = ["G", "M", "E", "S", "T", "K", "R", "Q", "F", "C"]

VARIABLES = {
    "G": {
        "label": "Authority/Ground",
        "keywords": ["axiom", "ground", "authority", "source", "law", "foundation", "canon", "proof boundary"],
    },
    "M": {
        "label": "Mechanism/Action",
        "keywords": ["procedure", "workflow", "mechanism", "algorithm", "pipeline", "method", "operation", "step"],
    },
    "E": {
        "label": "Entropy/Disorder",
        "keywords": ["mojibake", "encoding broken", "�", "Ã", "[redacted]", "[illegible]", "parse error"],
    },
    "S": {
        "label": "Identity/Self",
        "keywords": ["i ", "my ", "me ", "myself", "personhood", "inner life", "who i am"],
    },
    "T": {
        "label": "Time/Sequence",
        "keywords": ["timeline", "sequence", "version", "before", "after", "phase", "history", "dated"],
    },
    "K": {
        "label": "Knowledge/Info",
        "keywords": ["claim", "definition", "data", "equation", "evidence", "fact", "schema", "table"],
    },
    "R": {
        "label": "Relation/Bond",
        "keywords": ["depends", "supports", "connects", "maps to", "relation", "link", "edge", "covenant"],
    },
    "Q": {
        "label": "Experience/Felt",
        "keywords": ["felt", "emotion", "pain", "joy", "fear", "grief", "delight", "perception"],
    },
    "F": {
        "label": "Faith/Trust",
        "keywords": ["trust", "belief", "reliance", "uncertainty", "commitment under uncertainty", "epistemic risk"],
    },
    "C": {
        "label": "Coherence/Unity",
        "keywords": ["coherence", "integrate", "unify", "synthesis", "reconcile", "one whole", "cross-domain"],
    },
}

DOMAIN_KEYWORDS = {
    "THEOPHYSICS": ["theophysics", "chi", "logos", "grace", "gtq", "master equation", "axiom"],
    "SCIENCE": ["experiment", "physics", "biology", "data", "hypothesis", "empirical"],
    "TECH": ["python", "api", "postgres", "json", "pipeline", "script", "database"],
    "LAW": ["contract", "legal", "court", "statute", "liability"],
    "MEDICINE": ["clinical", "patient", "diagnosis", "treatment", "medical"],
    "BUSINESS": ["revenue", "client", "market", "sales", "business"],
    "PERSONAL": ["journal", "diary", "personal", "family"],
}

BLOCK_TYPES = {
    "CLAIM": ["claim", "argues", "therefore", "shows", "means", "proves", "asserts"],
    "EVIDENCE": ["evidence", "source", "citation", "data", "observed", "measured"],
    "EQUATION": ["=", "\\frac", "\\chi", "$$", "\\(", "\\["],
    "DEFINITION": ["definition", "means", "is defined as", "::"],
    "KILL_CONDITION": ["kill condition", "falsify", "breaks", "refute", "contradict"],
    "DOMAIN_SHIFT": ["maps to", "across", "bridge", "physics", "theology", "metaphysics"],
}

OVERSTATEMENT_HIGH = ["proves", "mathematically proven", "undeniable", "impossible", "refuted", "destroyed", "only", "definitive", "settled"]
LOAD_BEARING_WORDS = {"not", "because", "unless", "except", "before", "after", "therefore", "however", "if", "then", "only", "must", "may", "should", "never"}


@dataclass
class VariableScore:
    score: int
    confidence: float
    evidence: list[str]


def normalize_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def strip_html(raw: str) -> str:
    raw = re.sub(r"(?is)<script.*?</script>", " ", raw)
    raw = re.sub(r"(?is)<style.*?</style>", " ", raw)
    raw = re.sub(r"(?is)<br\s*/?>", "\n", raw)
    raw = re.sub(r"(?is)</(p|div|section|article|li|h[1-6])>", "\n", raw)
    raw = re.sub(r"(?is)<[^>]+>", " ", raw)
    return html.unescape(raw)


def read_document(path: Path) -> tuple[str, dict[str, Any]]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    metadata: dict[str, Any] = {"source_path": str(path), "input_format": path.suffix.lower().lstrip(".") or "txt"}
    if raw.startswith("---"):
        match = re.match(r"(?s)^---\s*\n(.*?)\n---\s*\n(.*)$", raw)
        if match:
            metadata["frontmatter_raw"] = match.group(1)
            raw = match.group(2)
    if path.suffix.lower() in {".html", ".htm"}:
        title = re.search(r"(?is)<title[^>]*>(.*?)</title>", raw)
        if title:
            metadata["title"] = normalize_ws(strip_html(title.group(1)))
        raw = strip_html(raw)
    return raw, metadata


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "x"


def evidence_snippets(text: str, keywords: list[str], limit: int = 3) -> list[str]:
    snippets: list[str] = []
    lower = text.lower()
    for keyword in keywords:
        index = lower.find(keyword)
        if index >= 0:
            start = max(0, index - 80)
            end = min(len(text), index + len(keyword) + 120)
            snippets.append(normalize_ws(text[start:end]))
        if len(snippets) >= limit:
            break
    return snippets


def score_variables(text: str) -> dict[str, VariableScore]:
    lower = text.lower()
    length = max(len(text), 1)
    result: dict[str, VariableScore] = {}
    for symbol, config in VARIABLES.items():
        hits = [kw for kw in config["keywords"] if kw in lower]
        count = sum(lower.count(kw) for kw in hits)
        threshold = _dominance_threshold(symbol)
        score = 3 if count >= threshold and _passes_special_rule(symbol, lower) else 0
        density = min(1.0, count / max(2, length / 3500))
        confidence = round(0.55 + (0.4 * density), 3) if count else 0.5
        result[symbol] = VariableScore(score=score, confidence=confidence, evidence=evidence_snippets(text, hits))
    return result


def _passes_special_rule(symbol: str, lower: str) -> bool:
    if symbol == "E":
        return any(word in lower for word in ["mojibake", "encoding broken", "�", "ã", "[redacted]", "[illegible]", "parse error"])
    if symbol == "C":
        return any(word in lower for word in ["integrate", "unify", "synthesis", "reconcile", "cross-domain", "one whole"])
    if symbol == "S":
        return bool(re.search(r"\b(i|my|me|myself)\b", lower)) and any(
            word in lower for word in ["identity", "personhood", "inner life", "who i am", "selfhood"]
        )
    if symbol == "Q":
        return any(word in lower for word in ["felt", "emotion", "pain", "joy", "fear", "grief", "delight"])
    if symbol == "F":
        return any(word in lower for word in ["trust", "belief", "reliance", "commitment under uncertainty", "epistemic risk"])
    return True


def _dominance_threshold(symbol: str) -> int:
    if symbol in {"E", "S", "Q"}:
        return 3
    if symbol == "F":
        return 2
    if symbol == "C":
        return 1
    return 2


def vector_string(scores: dict[str, VariableScore]) -> str:
    return "".join(f"{symbol}{scores[symbol].score}" for symbol in VECTOR_ORDER)


def semantic_hash(scores: dict[str, VariableScore]) -> dict[str, Any]:
    ranked = sorted(VECTOR_ORDER, key=lambda symbol: (-scores[symbol].score, TIE_BREAK.index(symbol)))
    pairs = [f"{ranked[i]}.{ranked[-(i + 1)]}" for i in range(5)]
    return {"ranked": ranked, "pairs": pairs, "hash": "-".join(pair.replace(".", "") for pair in pairs)}


def infer_domain(text: str) -> str:
    lower = text.lower()
    counts = {domain: sum(lower.count(kw) for kw in keywords) for domain, keywords in DOMAIN_KEYWORDS.items()}
    domain, count = max(counts.items(), key=lambda item: item[1])
    return domain if count else "UNKNOWN"


def infer_named_entity(path: Path, metadata: dict[str, Any]) -> str:
    title = metadata.get("title")
    if title:
        return slugify(str(title))[:80].upper()
    return slugify(path.stem)[:80].upper()


def infer_state(path: Path, text: str) -> str:
    lower = f"{path.name} {text[:2000]}".lower()
    if "deprecated" in lower:
        return "X"
    if "archived" in lower or "archive" in lower:
        return "A"
    if "published" in lower or "production-ready" in lower:
        return "P"
    if "final" in lower:
        return "F"
    if "draft" in lower:
        return "D"
    return "W"


def infer_audience(text: str) -> str:
    lower = text.lower()
    if "public" in lower or "seo" in lower or "reader" in lower:
        return "PUBLIC"
    if "legal" in lower:
        return "LEGAL"
    if "academic" in lower or "paper" in lower:
        return "ACADEMIC"
    if "internal" in lower:
        return "INTERNAL"
    if "ai" in lower or "llm" in lower:
        return "AI_RESEARCH"
    return "UNKNOWN"


def infer_use(text: str) -> str:
    lower = text.lower()
    if any(word in lower for word in ["must", "required", "binding", "contract"]):
        return "B"
    if any(word in lower for word in ["convert", "repair", "rewrite", "transform"]):
        return "T"
    if any(word in lower for word in ["log", "record", "archive", "snapshot"]):
        return "R"
    return "I"


def infer_risk(text: str) -> str:
    lower = text.lower()
    if any(word in lower for word in ["medical", "life-critical", "safety-critical"]):
        return "R4"
    if any(word in lower for word in ["legal", "financial", "contract", "formal consequence"]):
        return "R3"
    if any(word in lower for word in ["private", "pii", "password", "credential"]):
        return "R2"
    if any(word in lower for word in ["internal", "research", "draft"]):
        return "R1"
    return "R0"


def build_address(path: Path, text: str, metadata: dict[str, Any], scores: dict[str, VariableScore]) -> dict[str, Any]:
    domain = infer_domain(text)
    named_entity = infer_named_entity(path, metadata)
    version_state = infer_state(path, text)
    audience = infer_audience(text)
    use_direction = infer_use(text)
    risk = infer_risk(text)
    vector = vector_string(scores)
    hash_payload = semantic_hash(scores)
    address = f"{domain}/{named_entity}/{version_state}/{audience}/{use_direction}/{risk} :: {vector} :: {hash_payload['hash']}"
    return {
        "address": address,
        "filename_safe": f"{domain}__{named_entity}__{version_state}__{audience}__{use_direction}__{risk}__{vector}__{hash_payload['hash']}",
        "domain": domain,
        "named_entity": named_entity,
        "version_state": version_state,
        "audience": audience,
        "use_direction": use_direction,
        "risk": risk,
        "vector": vector,
        "semantic_hash": hash_payload,
    }


def split_blocks(text: str) -> list[dict[str, Any]]:
    chunks = [normalize_ws(chunk) for chunk in re.split(r"\n\s*\n+", text) if normalize_ws(chunk)]
    blocks = []
    for index, chunk in enumerate(chunks, start=1):
        block_type = classify_block(chunk)
        blocks.append(
            {
                "block_id": f"block-{index:05d}",
                "block_type": block_type,
                "text": chunk,
                "content_hash": hashlib.sha1(chunk.encode("utf-8", errors="replace")).hexdigest(),
            }
        )
    return blocks


def classify_block(chunk: str) -> str:
    lower = chunk.lower()
    for block_type, keywords in BLOCK_TYPES.items():
        if any(keyword in lower for keyword in keywords):
            return block_type
    return "OTHER"


def extract_equations(text: str) -> list[dict[str, Any]]:
    patterns = [
        r"\$\$(.+?)\$\$",
        r"\\\[(.+?)\\\]",
        r"\\\((.+?)\\\)",
    ]
    equations = []
    seen = set()
    for pattern in patterns:
        for match in re.finditer(pattern, text, re.DOTALL):
            equation = normalize_ws(match.group(1))
            if equation and equation not in seen:
                seen.add(equation)
                equations.append(
                    {
                        "equation_id": f"eq-{len(equations) + 1:04d}",
                        "equation": equation,
                        "role": "EXPAND_REQUIRED",
                        "status": "PRESENTATIONAL",
                        "undefined_vars": [],
                        "dimensional_status": "UNKNOWN",
                        "derivation_present": "UNKNOWN",
                        "computable": "UNKNOWN",
                        "known_theory_comparison": "EXPAND_REQUIRED",
                    }
                )
    return equations


def extract_claims(blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    claims = []
    for block in blocks:
        if block["block_type"] in {"CLAIM", "DOMAIN_SHIFT"}:
            claims.append(
                {
                    "claim_id": f"claim-{len(claims) + 1:04d}",
                    "block_id": block["block_id"],
                    "surface_claim": block["text"][:600],
                    "buried_claim": "EXPAND_REQUIRED",
                    "operational_claim": "EXPAND_REQUIRED",
                    "rhetorical_load": "UNKNOWN",
                    "domain_shift": block["block_type"] == "DOMAIN_SHIFT",
                    "domain_badges": infer_domain_badges(block["text"]),
                }
            )
    return claims


def infer_domain_badges(text: str) -> list[str]:
    lower = text.lower()
    badges = []
    mapping = {
        "PHYSICS": ["physics", "quantum", "entropy", "field"],
        "THEOLOGY": ["god", "grace", "christ", "theology", "scripture"],
        "FORMAL": ["formal", "proof", "lean", "axiom", "equation"],
        "EMPIRICAL": ["data", "experiment", "observed", "measurement"],
        "ANALOGY": ["analogy", "maps to", "correspondence"],
        "INFORMATION": ["information", "signal", "entropy", "shannon"],
        "TECH": ["python", "api", "postgres", "json"],
    }
    for badge, keywords in mapping.items():
        if any(keyword in lower for keyword in keywords):
            badges.append(badge)
    return badges or ["UNKNOWN"]


def build_artifact(path: Path) -> dict[str, Any]:
    text, metadata = read_document(path)
    scores = score_variables(text)
    address = build_address(path, text, metadata, scores)
    blocks = split_blocks(text)
    claims = extract_claims(blocks)
    equations = extract_equations(text)
    overstatements = [word for word in OVERSTATEMENT_HIGH if word in text.lower()]
    return {
        "schema_version": SCHEMA_VERSION,
        "source": metadata,
        "content_hash": content_hash(text),
        "compression_declaration": {
            "scope": "single document",
            "goal": "dense reconstruction seed with deterministic semantic address",
            "known_limits": ["LLM-required fields marked EXPAND_REQUIRED", "rule-based first pass only"],
            "reconstruction_confidence": "MEDIUM_RULE_BASED",
        },
        "semantic_address": address,
        "semantic_vector": {
            "vector": address["vector"],
            "scores": {symbol: scores[symbol].score for symbol in VECTOR_ORDER},
            "confidence": {symbol: scores[symbol].confidence for symbol in VECTOR_ORDER},
            "evidence": {symbol: scores[symbol].evidence for symbol in VECTOR_ORDER},
        },
        "semantic_hash": address["semantic_hash"],
        "blocks": blocks,
        "claim_arch": claims,
        "eq_sem": equations,
        "overstate_pattern": {
            "high_risk_words": sorted(set(overstatements)),
            "safe_rewrite": "EXPAND_REQUIRED",
            "detection_rule": "literal high-risk lexeme match; context requires review",
        },
        "eight_gaps": [
            {"gap": "Score separation gap", "status": "PARTIAL", "repair_action": "append score ledger module"},
            {"gap": "Hostile reviewer gap", "status": "EXPAND_REQUIRED", "repair_action": "LLM hostile review pass"},
            {"gap": "Evidence bridge gap", "status": "EXPAND_REQUIRED", "repair_action": "LLM bridge extraction"},
            {"gap": "Domain badge gap", "status": "PARTIAL", "repair_action": "review inferred badges"},
            {"gap": "Score ledger gap", "status": "MISSING", "repair_action": "build score event writer"},
            {"gap": "Equation semantics gap", "status": "PARTIAL", "repair_action": "run math translation/equation audit"},
            {"gap": "Overstatement gap", "status": "PARTIAL", "repair_action": "contextual rewrite pass"},
            {"gap": "Benchmark/risk-context gap", "status": "EXPAND_REQUIRED", "repair_action": "compare against benchmark corpus"},
        ],
        "decompress": [
            "Decode ADDRESS.",
            "Expand VECTOR and HASH.",
            "Read blocks and claim_arch.",
            "Preserve EXPAND_REQUIRED fields.",
            "Separate formal proof, structural support, empirical evidence, and interpretation.",
            "Do not replace the user's framework with generic interpretation.",
        ],
        "check": {
            "included_threads": len(blocks),
            "missing_threads": [],
            "ambiguity_flags": ["rule_based_first_pass"],
            "compression_loss_risk": "MEDIUM",
            "reconstruction_confidence": "MEDIUM_RULE_BASED",
            "decision_count": 0,
            "entity_count": 0,
            "claim_count": len(claims),
            "equation_count": len(equations),
            "open_thread_count": 0,
        },
        "recovery_key": f"{address['domain']}-{address['named_entity'][:16]}-{content_hash(text)[:10]}",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a lossless compression + semantic address artifact.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    artifact = build_artifact(args.input)
    output = args.output or args.input.with_suffix(args.input.suffix + ".semantic-address.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(artifact, indent=2, ensure_ascii=True), encoding="utf-8")
    print(json.dumps({"output": str(output), "address": artifact["semantic_address"]["address"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
