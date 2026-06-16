from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from semantic_addressing import build_artifact as build_semantic_artifact


SCHEMA_VERSION = "paper_snapshot.contract.v0.draft"

TITLE_RE = re.compile(r"(?is)<title[^>]*>(.*?)</title>")
EQUATION_INLINE_RE = re.compile(r"\$(.+?)\$", re.DOTALL)
JS_STRING_FIELD_TEMPLATE = r"{field}\s*:\s*'((?:\\.|[^'])*)'"
JS_ARRAY_FIELD_TEMPLATE = r"{field}\s*:\s*(\[[\s\S]*?\])\s*,\s*{next_field}\s*:"

TOPICAL_TERMS = {
    "coherence": ["coherence", "chi", "logos"],
    "thermodynamics": ["entropy", "decay", "heat death"],
    "consciousness": ["consciousness", "observer", "measurement"],
    "biblical_data": ["biblical", "scripture", "prophetic", "gospel"],
    "empirical_testing": ["test", "data", "prediction", "experiment", "significance"],
    "math_translation": ["equation", "wavefunction", "rho", "r^2", "spearman"],
}

CLAIM_TYPE_RULES = {
    "empirical": ["data", "measurement", "significant", "prediction", "observed", "experiment"],
    "mathematical": ["equation", "theorem", "derive", "formal", "operator", "model"],
    "theological": ["god", "grace", "christ", "biblical", "theology", "scripture"],
    "historical": ["history", "timeline", "era", "kingdom", "century", "bce", "ce"],
    "methodological": ["method", "protocol", "scoring", "analysis", "test design"],
    "interpretive": ["suggests", "appears", "framework", "maps to", "correspondence"],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Emit a draft .paper-snapshot.json from paper-grader outputs.")
    parser.add_argument("--paper-grade-json", type=Path, required=True)
    parser.add_argument("--claim-audit-csv", type=Path, required=True)
    parser.add_argument("--lossless-summary-md", type=Path)
    parser.add_argument("--source-html", type=Path)
    parser.add_argument("--math-translation-json", type=Path)
    parser.add_argument("--proof-explorer-audit-html", type=Path)
    parser.add_argument("--proof-explorer-audit-fallback-html", type=Path)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def find_live_source(paper_id: str, preferred: Path | None, grader_source: str | None) -> Path | None:
    candidates: list[Path] = []
    if preferred is not None:
        candidates.append(preferred)
    if grader_source:
        candidates.append(Path(grader_source))
    live_roots = [
        Path(r"\\dlowenas\HPWorkstation\Desktop\Master HTMl\K-Production-Ready\02-genesis-to-quantum"),
        Path(r"D:\GTQ-BUILD\articles"),
    ]
    html_name = f"{paper_id}.html"
    for root in live_roots:
        candidates.append(root / html_name)
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def title_from_html(path: Path | None, fallback: str) -> str:
    if path is None or not path.exists():
        return fallback
    raw = path.read_text(encoding="utf-8", errors="replace")
    match = TITLE_RE.search(raw)
    if match:
        return re.sub(r"\s+", " ", match.group(1)).strip()
    return fallback


def article_number_from_paper_id(paper_id: str) -> str | None:
    match = re.match(r"gtq-(\d+[a-z]?)", paper_id, re.IGNORECASE)
    return match.group(1) if match else None


def infer_claim_type(text: str) -> str:
    lower = text.lower()
    for claim_type, keywords in CLAIM_TYPE_RULES.items():
        if any(keyword in lower for keyword in keywords):
            return claim_type
    return "meta"


def infer_epistemic_tier(maturity_label: str, text: str) -> int:
    lower = maturity_label.lower()
    if "empirical" in lower:
        return 2
    if "formal" in lower or "structural" in lower:
        return 1
    if "proof" in lower:
        return 1
    if "histor" in text.lower() or "interpret" in text.lower():
        return 3
    return 1


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def normalize_lookup(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", normalize_text(value).lower()).strip()


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def parse_js_quoted_string(raw: str) -> str:
    return bytes(raw, "utf-8").decode("unicode_escape")


def extract_js_string_field(text: str, field: str) -> str | None:
    pattern = re.compile(JS_STRING_FIELD_TEMPLATE.format(field=re.escape(field)), re.DOTALL)
    match = pattern.search(text)
    if not match:
        return None
    return parse_js_quoted_string(match.group(1))


def extract_js_number_field(text: str, field: str) -> int | None:
    match = re.search(rf"{re.escape(field)}\s*:\s*(\d+)", text)
    return int(match.group(1)) if match else None


def extract_js_array_field(text: str, field: str, next_field: str) -> str | None:
    pattern = re.compile(
        JS_ARRAY_FIELD_TEMPLATE.format(field=re.escape(field), next_field=re.escape(next_field)),
        re.DOTALL,
    )
    match = pattern.search(text)
    return match.group(1) if match else None


def parse_js_literal_array(raw: str) -> Any:
    normalized = raw.replace("true", "True").replace("false", "False").replace("null", "None")
    return ast.literal_eval(normalized)


def normalize_equations(raw_equations: list[str]) -> list[str]:
    cleaned: list[str] = []
    seen: set[str] = set()
    for item in raw_equations:
        value = normalize_text(item)
        if len(value) < 6:
            continue
        if value in {"O_{eff}", "G(t)", "(1-C)", "[0, 1]", "(0, \\infty)", "[0, \\infty)"}:
            continue
        if not any(token in value for token in ("=", "\\frac", "\\chi", "\\rho", "R^2", "\\times", "\\cdot", "\\iiint", "\\alpha", "\\beta", "\\gamma")):
            continue
        key = value.lower()
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(value)
    return cleaned


def read_proof_explorer_audit(primary: Path | None, fallback: Path | None) -> dict[str, Any]:
    for candidate in [primary, fallback]:
        if candidate is None or not candidate.exists():
            continue
        text = candidate.read_text(encoding="utf-8", errors="replace")
        q7_raw = extract_js_array_field(text, "q7", "forward_reverse")
        if not q7_raw:
            continue
        facts_raw = extract_js_array_field(text, "facts", "q7")
        evidence_raw = extract_js_array_field(text, "evidence_bar", "not_claimed")
        not_claimed_raw = re.search(r"not_claimed\s*:\s*(\[[\s\S]*?\])\s*\n\s*};", text, re.DOTALL)
        return {
            "source_path": str(candidate),
            "one_sentence_claim": extract_js_string_field(text, "one_sentence_claim"),
            "maturity_level": extract_js_number_field(text, "maturity_level"),
            "maturity_note": extract_js_string_field(text, "maturity_note"),
            "proof_boundary": extract_js_string_field(text, "proof_boundary"),
            "facts": parse_js_literal_array(facts_raw) if facts_raw else [],
            "q7": parse_js_literal_array(q7_raw),
            "forward_reverse": extract_js_string_field(text, "forward_reverse"),
            "evidence_bar": parse_js_literal_array(evidence_raw) if evidence_raw else [],
            "not_claimed": parse_js_literal_array(not_claimed_raw.group(1)) if not_claimed_raw else [],
        }
    return {}


def proof_audit_matches_paper(audit_payload: dict[str, Any], paper_id: str, title: str) -> bool:
    if not audit_payload:
        return False
    source_path = str(audit_payload.get("source_path", ""))
    lowered_source = source_path.lower()
    if paper_id.lower() in lowered_source:
        return True
    paper_number = article_number_from_paper_id(paper_id)
    if paper_number and f"gtq-{paper_number}".lower() in lowered_source:
        return True
    normalized_title = normalize_lookup(title)
    normalized_claim = normalize_lookup(audit_payload.get("one_sentence_claim", ""))
    if normalized_title and normalized_claim:
        title_tokens = [token for token in normalized_title.split() if len(token) > 4]
        overlap = sum(1 for token in title_tokens if token in normalized_claim)
        if overlap >= 3:
            return True
    return False


def find_rigor_report_json(paper_grade_json: Path) -> Path | None:
    candidates = [
        paper_grade_json.parent.parent / "RIGOR_GATE" / "rigor-report.json",
        paper_grade_json.with_name("rigor-report.json"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def read_rigor_report(path: Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {}
    return read_json(path)


def extract_topical_tags(title: str, claims: list[dict[str, Any]], equations: list[str]) -> dict[str, list[str]]:
    text = " ".join([title] + [claim["text"] for claim in claims] + equations).lower()
    topical = [tag for tag, keywords in TOPICAL_TERMS.items() if any(keyword in text for keyword in keywords)]
    entities: list[str] = []
    for marker in ["PEAR-LAB", "Global Consciousness Project", "PROP-COSMOS", "Master Equation", "P(t)"]:
        if marker.lower() in text:
            entities.append(marker)
    return {
        "topical": sorted(topical),
        "series": ["Genesis-to-Quantum"],
        "laws": [],
        "axioms": [],
        "methods": ["paper_grader", "claim_audit"],
        "epistemic": ["draft_snapshot", "canary"],
        "entities": entities,
        "scripture": [],
        "physics": ["coherence_equation"] if equations else [],
        "theology": ["theophysics"] if "theophysics" in text else [],
        "math": ["equation_extraction"] if equations else [],
    }


def load_claim_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        return list(csv.DictReader(handle))


def build_claims(claim_rows: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    claims: list[dict[str, Any]] = []
    evidence: list[dict[str, Any]] = []
    contradictions: list[dict[str, Any]] = []
    not_claimed_values: list[str] = []
    for index, row in enumerate(claim_rows, start=1):
        text = normalize_text(row.get("one_sentence_claim", ""))
        if not text:
            continue
        claim_id = f"claim-{index:03d}"
        evidence_bar = normalize_text(row.get("evidence_bar", ""))
        kill_conditions = normalize_text(row.get("kill_conditions", ""))
        not_claimed = normalize_text(row.get("not_claimed", ""))
        if not_claimed:
            not_claimed_values.append(not_claimed)
        claim = {
            "claim_id": claim_id,
            "text": text,
            "normalized_text": text.lower(),
            "claim_type": infer_claim_type(text),
            "status": "claimed",
            "epistemic_tier": infer_epistemic_tier(row.get("claim_maturity_label", ""), text),
            "confidence": row.get("Q4_evidence", "") == "present" and 0.75 or 0.5,
            "source_span": "",
            "source_section": row.get("section", ""),
            "tags": [slugify(row.get("section", "")), slugify(row.get("claim_maturity_label", ""))],
            "supporting_evidence": [evidence_bar] if evidence_bar else [],
            "dependencies": [],
            "consequences": [],
            "defeat_conditions": [kill_conditions] if kill_conditions else [],
            "derivation_chain": [],
            "graph_nodes": [slugify(row.get("section", ""))] if row.get("section") else [],
            "graph_edges": [],
            "paper_grader": {
                "claim_maturity_level": row.get("claim_maturity_level", ""),
                "claim_maturity_label": row.get("claim_maturity_label", ""),
                "facts_snapshot": row.get("facts_snapshot", ""),
                "forward_test": row.get("forward_test", ""),
                "reverse_test": row.get("reverse_test", ""),
                "proof_boundary": row.get("proof_boundary", ""),
                "q_markers": {
                    "Q1_identity": row.get("Q1_identity", ""),
                    "Q2_scope": row.get("Q2_scope", ""),
                    "Q3_mechanism": row.get("Q3_mechanism", ""),
                    "Q4_evidence": row.get("Q4_evidence", ""),
                    "Q5_falsifiability": row.get("Q5_falsifiability", ""),
                    "Q6_boundary": row.get("Q6_boundary", ""),
                    "Q7_listener_risk": row.get("Q7_listener_risk", ""),
                },
            },
        }
        claims.append(claim)
        if evidence_bar:
            evidence.append(
                {
                    "evidence_id": f"evidence-{index:03d}",
                    "claim_id": claim_id,
                    "text": evidence_bar,
                    "type": "paper_grader_evidence_bar",
                    "section": row.get("section", ""),
                }
            )
        if "failed" in text.lower() or "not significant" in text.lower() or "contradict" in kill_conditions.lower():
            contradictions.append(
                {
                    "contradiction_id": f"contradiction-{index:03d}",
                    "claim_id": claim_id,
                    "summary": text,
                    "notes": kill_conditions,
                }
            )
    unique_not_claimed = sorted({value for value in not_claimed_values if value})
    return claims, evidence, contradictions, unique_not_claimed


def load_math_dictionary(dictionary_path: Path) -> dict[str, Any]:
    payload = read_json(dictionary_path)
    equation_summaries = payload.get("summaries", {})
    compiled_equations = []
    for entry in payload.get("equations", []):
        patterns = [re.compile(pattern, re.IGNORECASE) for pattern in entry.get("patterns", [])]
        compiled_equations.append(
            {
                "equationId": entry.get("equationId"),
                "title": entry.get("title"),
                "patterns": patterns,
                "summary": entry.get("summary") or equation_summaries.get(entry.get("equationId")),
                "narrative": entry.get("narrative"),
            }
        )
    aliases = payload.get("aliases", [])
    symbols = payload.get("symbols", [])
    return {"aliases": aliases, "equations": compiled_equations, "symbols": symbols}


def apply_aliases(text: str, aliases: list[dict[str, str]]) -> str:
    result = text
    for alias in aliases:
        result = re.sub(alias["pattern"], alias["replacement"], result)
    return result


def normalize_equation_for_match(text: str, aliases: list[dict[str, str]]) -> str:
    value = apply_aliases(text, aliases)
    value = value.replace("\\text{eff}", "eff").replace("{", "").replace("}", "")
    return normalize_text(value)


def resolve_claim_for_equation(equation_text: str, claims: list[dict[str, Any]]) -> str | None:
    normalized_equation = normalize_lookup(equation_text)
    best_claim_id = None
    best_score = 0
    for claim in claims:
        claim_text = claim.get("text", "")
        normalized_claim = normalize_lookup(claim_text)
        score = 0
        if equation_text and equation_text in claim_text:
            score += 10
        if normalized_equation and normalized_equation in normalized_claim:
            score += 8
        for token in [token for token in normalized_equation.split() if len(token) > 2]:
            if token in normalized_claim:
                score += 1
        if score > best_score:
            best_score = score
            best_claim_id = claim.get("claim_id")
    return str(best_claim_id) if best_claim_id else None


def build_math_translation_fallback(extracted_equations: list[str], claims: list[dict[str, Any]]) -> dict[str, Any]:
    dictionary_path = Path(r"X:\Backside\stations\math-layer.station\src\dictionaries\theophysics.json")
    if not dictionary_path.exists():
        return {
            "status": "not_found",
            "source_path": None,
            "translated_spans": [],
            "notes": "No math translation result or dictionary fallback was found.",
        }

    dictionary = load_math_dictionary(dictionary_path)
    spans = []
    for index, equation_text in enumerate(extracted_equations, start=1):
        normalized_equation = normalize_equation_for_match(equation_text, dictionary["aliases"])
        matched_entry = None
        for entry in dictionary["equations"]:
            if any(pattern.search(normalized_equation) for pattern in entry["patterns"]):
                matched_entry = entry
                break
        if not matched_entry or not matched_entry.get("summary"):
            continue
        claim_id = resolve_claim_for_equation(equation_text, claims)
        spans.append(
            {
                "span_id": f"dict-span-{index:03d}",
                "original": equation_text,
                "translated": matched_entry["summary"],
                "source_location": f"extracted_equations:eq-{index:03d}",
                "dictionary_terms": [matched_entry["equationId"]],
                "confidence": 0.95,
                "needs_review": False,
                "claim_id": claim_id,
                "translation_source": "dictionary_summary_fallback",
            }
        )

    if not spans:
        return {
            "status": "not_found",
            "source_path": str(dictionary_path),
            "translated_spans": [],
            "notes": "Dictionary fallback loaded, but no extracted equations matched canonical translation patterns.",
        }

    return {
        "status": "dictionary_fallback",
        "source_path": str(dictionary_path),
        "translated_spans": spans,
        "notes": "Translated spans backfilled from the canonical math-layer dictionary because no external translation JSON was present.",
    }


def build_math_translation(
    math_translation_path: Path | None,
    extracted_equations: list[str],
    claims: list[dict[str, Any]],
) -> dict[str, Any]:
    if math_translation_path is None or not math_translation_path.exists():
        return build_math_translation_fallback(extracted_equations, claims)
    payload = read_json(math_translation_path)
    result = payload.get("result", {})
    spans = []
    for index, item in enumerate(result.get("evidence", []), start=1):
        quote = item.get("quote", "")
        equations = [normalize_text(match.group(1)) for match in EQUATION_INLINE_RE.finditer(quote)]
        spans.append(
            {
                "span_id": item.get("paragraph_id", f"span-{index:03d}"),
                "source_quote": quote,
                "translated_text": result.get("output", ""),
                "equations": equations,
            }
        )
    return {
        "status": result.get("status", "unknown").lower(),
        "source_path": str(math_translation_path),
        "translated_spans": spans,
        "notes": result.get("notes", ""),
        "blockers": result.get("blockers", []),
    }


def build_local_seven_qs(title: str, paper_id: str, claims: list[dict[str, Any]], rigor_report: dict[str, Any]) -> dict[str, Any]:
    def first_matching(fragment: str) -> str | None:
        for claim in claims:
            if fragment in claim.get("normalized_text", ""):
                return claim.get("text")
        return None

    strongest_empirical = first_matching("specific quantitative predictions") or (claims[0]["text"] if claims else None)
    evidence_claim = first_matching("statistically significant results") or first_matching("strongest results are")
    dependency_claim = first_matching("three non-negotiable constraints") or first_matching("requires revision or rejection")
    falsification_claim = next(
        (claim.get("text") for claim in claims if claim.get("text", "").lower().startswith("falsification:")),
        None,
    ) or first_matching("requires revision or rejection")

    result = {
        "q0_posture": {
            "answer": "Treat GTQ-17 as a testable paper and keep evidence, kill conditions, and boundary claims separate.",
            "confidence": 0.7,
            "notes": "Seeded from GTQ-17 rigor-gate rejection-first requirements.",
        },
        "q1_identity": {
            "answer": title or paper_id,
            "confidence": 0.7,
            "notes": "Seeded from GTQ-17 title and paper identity.",
        },
        "q2_location": {
            "answer": "Genesis-to-Quantum empirical testing lane inside the axioms workflow.",
            "confidence": 0.7,
            "notes": "Seeded from file location and series metadata.",
        },
        "q3_assertion": {
            "answer": strongest_empirical,
            "confidence": 0.7 if strongest_empirical else None,
            "notes": "Seeded from the highest-salience GTQ-17 claim audit row.",
        },
        "q4_evidence": {
            "answer": evidence_claim,
            "confidence": 0.65 if evidence_claim else None,
            "notes": "Seeded from GTQ-17 empirical-results claim rows.",
        },
        "q5_dependencies": {
            "answer": dependency_claim,
            "confidence": 0.65 if dependency_claim else None,
            "notes": "Seeded from GTQ-17 dependency/constraint claims.",
        },
        "q6_consequences": {
            "answer": "If strengthened, GTQ-17 supports the claim that framework predictions can survive contact with measured biblical and historical data.",
            "confidence": 0.55,
            "notes": "Seeded from GTQ-17 claim audit plus rigor verdict context.",
        },
        "q7_falsification": {
            "answer": falsification_claim,
            "confidence": 0.7 if falsification_claim else None,
            "notes": "Seeded from GTQ-17 falsification and revision-language claims.",
        },
    }
    if rigor_report.get("verdict"):
        result["q7_falsification"]["rigor_verdict"] = rigor_report["verdict"]
    return result


def build_seven_qs(title: str, paper_id: str, claims: list[dict[str, Any]], audit_payload: dict[str, Any], rigor_report: dict[str, Any]) -> dict[str, Any]:
    if audit_payload.get("q7"):
        q7_map = {
            "Q0 Posture": "q0_posture",
            "Q1 Identity": "q1_identity",
            "Q2 Domain": "q2_location",
            "Q3 Claim": "q3_assertion",
            "Q4 Support": "q4_evidence",
            "Q5 Dependencies": "q5_dependencies",
            "Q6 Consequences": "q6_consequences",
            "Q7 Kill Conditions": "q7_falsification",
        }
        result = {
            "q0_posture": {"answer": None, "confidence": None, "notes": "Placeholder for 7QS station."},
            "q1_identity": {"answer": None, "confidence": None, "notes": "Placeholder for 7QS station."},
            "q2_location": {"answer": None, "confidence": None, "notes": "Placeholder for 7QS station."},
            "q3_assertion": {"answer": None, "confidence": None, "notes": "Placeholder for 7QS station."},
            "q4_evidence": {"answer": None, "confidence": None, "notes": "Placeholder for 7QS station."},
            "q5_dependencies": {"answer": None, "confidence": None, "notes": "Placeholder for 7QS station."},
            "q6_consequences": {"answer": None, "confidence": None, "notes": "Placeholder for 7QS station."},
            "q7_falsification": {"answer": None, "confidence": None, "notes": "Placeholder for 7QS station."},
        }
        maturity_level = audit_payload.get("maturity_level")
        confidence = min(0.95, 0.45 + 0.1 * maturity_level) if maturity_level is not None else 0.75
        for label, body in audit_payload["q7"]:
            target_key = q7_map.get(label)
            if not target_key:
                continue
            result[target_key] = {
                "answer": normalize_text(body),
                "confidence": confidence,
                "notes": f"Loaded from proof explorer audit HTML: {audit_payload['source_path']}",
            }
        if audit_payload.get("proof_boundary"):
            result["q7_falsification"]["proof_boundary"] = audit_payload["proof_boundary"]
        audit_payload["seven_qs_seed"] = result
        return result
    result = build_local_seven_qs(title, paper_id, claims, rigor_report)
    audit_payload["seven_qs_seed"] = result
    return result


def build_station_marks(
    paper_grade_json: Path,
    claim_audit_csv: Path,
    math_translation: dict[str, Any],
    proof_explorer_audit: dict[str, Any],
    output_path: Path,
) -> list[dict[str, Any]]:
    marks = [
        {
            "station_id": "paper_grader",
            "station_name": "Axiom Paper Grader",
            "status": "complete",
            "started_at": None,
            "completed_at": datetime.fromtimestamp(paper_grade_json.stat().st_mtime).isoformat(timespec="seconds"),
            "input_hash": sha256_file(paper_grade_json),
            "output_hash": sha256_file(paper_grade_json),
            "changed_fields": ["metrics", "sections", "equations"],
            "warnings": [],
        },
        {
            "station_id": "claim_audit",
            "station_name": "Claim Audit CSV",
            "status": "complete",
            "started_at": None,
            "completed_at": datetime.fromtimestamp(claim_audit_csv.stat().st_mtime).isoformat(timespec="seconds"),
            "input_hash": sha256_file(claim_audit_csv),
            "output_hash": sha256_file(claim_audit_csv),
            "changed_fields": ["claims", "evidence", "proof_boundary"],
            "warnings": [],
        },
        {
            "station_id": "math_translation",
            "station_name": "Math Translation Layer",
            "status": "complete" if math_translation["status"] not in {"not_found", "unknown"} else "skipped",
            "started_at": None,
            "completed_at": None,
            "input_hash": None,
            "output_hash": None,
            "changed_fields": ["math_translation_layer"] if math_translation["translated_spans"] else [],
            "warnings": [] if math_translation["translated_spans"] else ["No math translation result found for canary."],
        },
        {
            "station_id": "proof_explorer_audit",
            "station_name": "Proof Explorer 7Q Audit",
            "status": "complete" if proof_explorer_audit.get("q7") else "skipped",
            "started_at": None,
            "completed_at": None,
            "input_hash": sha256_file(Path(proof_explorer_audit["source_path"])) if proof_explorer_audit.get("source_path") else None,
            "output_hash": sha256_file(Path(proof_explorer_audit["source_path"])) if proof_explorer_audit.get("source_path") else None,
            "changed_fields": ["seven_qs"] if proof_explorer_audit.get("q7") else [],
            "warnings": [] if proof_explorer_audit.get("q7") else ["No proof explorer audit HTML found for seven_qs population."],
        },
        {
            "station_id": "paper_snapshot_writer",
            "station_name": "Paper Snapshot Writer",
            "status": "complete",
            "started_at": None,
            "completed_at": datetime.now().isoformat(timespec="seconds"),
            "input_hash": None,
            "output_hash": None,
            "changed_fields": ["identity", "source", "claims", "station_marks", "output_path_references"],
            "warnings": [] if output_path else [],
        },
    ]
    return marks


def build_epistemic_status(
    claims: list[dict[str, Any]],
    proof_explorer_audit: dict[str, Any],
    rigor_report: dict[str, Any],
    not_claimed: list[str],
) -> dict[str, Any]:
    maturity_level = proof_explorer_audit.get("maturity_level")
    if maturity_level is not None:
        overall_tier = 1 if maturity_level <= 5 else 2
    elif rigor_report.get("verdict") == "NEEDS_RIGOR":
        overall_tier = 1
    else:
        overall_tier = 2 if any(claim.get("epistemic_tier") == 2 for claim in claims) else 1

    failure_counts = rigor_report.get("failure_counts", {})
    what_can_be_tested = []
    for claim in claims[:5]:
        if claim.get("paper_grader", {}).get("forward_test"):
            what_can_be_tested.append(claim["paper_grader"]["forward_test"])
    what_can_be_tested = list(dict.fromkeys(what_can_be_tested))

    return {
        "overall_tier": overall_tier,
        "tier_reason": proof_explorer_audit.get("maturity_note")
        or f"Rigor verdict: {rigor_report.get('verdict', 'unknown')}",
        "test_mode": "artifact_boundaries_plus_claim_audit",
        "what_can_be_tested": what_can_be_tested,
        "what_cannot_be_tested": [proof_explorer_audit.get("proof_boundary")] if proof_explorer_audit.get("proof_boundary") else [],
        "honest_disclosures": [item for item in [proof_explorer_audit.get("maturity_note"), proof_explorer_audit.get("proof_boundary"), *not_claimed] if item],
        "rigor_verdict": rigor_report.get("verdict"),
        "rigor_failure_counts": failure_counts,
    }


def build_derivations(
    claims: list[dict[str, Any]],
    proof_explorer_audit: dict[str, Any],
    rigor_report: dict[str, Any],
) -> list[dict[str, Any]]:
    if not claims:
        return []
    anchor_claim = next(
        (claim for claim in claims if "master equation" in claim.get("normalized_text", "")),
        claims[0],
    )
    q7_map = {
        "q1_identity": "identity_scope",
        "q4_evidence": "support_aggregation",
        "q5_dependencies": "dependency_constraint",
        "q6_consequences": "consequence_projection",
    }
    steps = []
    seven_qs = proof_explorer_audit.get("seven_qs_seed", {})
    for order, (key, operation) in enumerate(q7_map.items(), start=1):
        payload = seven_qs.get(key)
        if not payload or not payload.get("answer"):
            continue
        steps.append(
            {
                "step_id": f"{anchor_claim['claim_id']}-step-{order:02d}",
                "premise": payload["answer"],
                "operation": operation,
                "output": anchor_claim["text"] if key != "q6_consequences" else payload["answer"],
                "support": payload.get("notes"),
            }
        )
    if rigor_report.get("failure_counts"):
        steps.append(
            {
                "step_id": f"{anchor_claim['claim_id']}-step-rigor",
                "premise": "Rigor gate failure counts constrain which parts of the paper remain structural versus closed.",
                "operation": "boundary_audit",
                "output": f"Verdict {rigor_report.get('verdict')}",
                "support": json.dumps(rigor_report.get("failure_counts", {}), ensure_ascii=False),
            }
        )
    if not steps:
        return []
    return [
        {
            "derivation_id": f"{anchor_claim['claim_id']}-derivation-001",
            "conclusion_claim_id": anchor_claim["claim_id"],
            "starts_from": proof_explorer_audit.get("facts", []),
            "steps": steps,
            "dependencies": [proof_explorer_audit.get("forward_reverse")] if proof_explorer_audit.get("forward_reverse") else [],
            "weakest_link": "Boundary/mechanism closure remains the weakest live link until Q3/Q5 rigor gaps are repaired.",
            "break_if_false": proof_explorer_audit.get("seven_qs_seed", {}).get("q7_falsification", {}).get("answer")
            or "If the stated falsification conditions survive contradictory data, the derivation chain needs revision.",
            "notes": "Grounded from GTQ-17 local rigor report plus deterministic 7Q seed extraction.",
        }
    ]


def build_semantic_fields(source_path: Path | None) -> dict[str, Any]:
    if source_path is None or not source_path.exists():
        return {
            "semantic_address": None,
            "semantic_vector": None,
            "semantic_hash": None,
            "classifier_tags": {
                "domain": [],
                "subject": [],
                "artifact_function": [],
                "canon_folder_route": None,
                "route_confidence": 0.0,
            },
            "lossless_compression": {
                "status": "skipped",
                "reason": "No live source file found for semantic addressing.",
            },
        }
    artifact = build_semantic_artifact(source_path)
    address = artifact["semantic_address"]
    return {
        "semantic_address": {
            "address": address["address"],
            "filename_safe": address["filename_safe"],
            "domain": address["domain"],
            "named_entity": address["named_entity"],
            "version_state": address["version_state"],
            "audience": address["audience"],
            "use_direction": address["use_direction"],
            "risk": address["risk"],
        },
        "semantic_vector": artifact["semantic_vector"],
        "semantic_hash": artifact["semantic_hash"],
        "classifier_tags": {
            "domain": [address["domain"]],
            "subject": [address["named_entity"]],
            "artifact_function": [
                symbol
                for symbol, value in artifact["semantic_vector"]["scores"].items()
                if value == 3
            ],
            "canon_folder_route": None,
            "route_confidence": 0.0,
        },
        "lossless_compression": {
            "status": "rule_based_first_pass",
            "schema_version": artifact["schema_version"],
            "content_hash": artifact["content_hash"],
            "recovery_key": artifact["recovery_key"],
            "claim_count": artifact["check"]["claim_count"],
            "equation_count": artifact["check"]["equation_count"],
            "compression_loss_risk": artifact["check"]["compression_loss_risk"],
            "reconstruction_confidence": artifact["check"]["reconstruction_confidence"],
        },
    }


def build_output_refs(
    paper_grade_json: Path,
    claim_audit_csv: Path,
    lossless_summary_md: Path | None,
    source_html: Path | None,
    math_translation_path: Path | None,
    proof_explorer_audit: dict[str, Any],
    output_path: Path,
) -> dict[str, Any]:
    refs = {
        "paper_grade_json": str(paper_grade_json),
        "claim_audit_csv": str(claim_audit_csv),
        "paper_snapshot_json": str(output_path),
    }
    if lossless_summary_md and lossless_summary_md.exists():
        refs["lossless_summary_md"] = str(lossless_summary_md)
    if source_html and source_html.exists():
        refs["source_html"] = str(source_html)
    if math_translation_path and math_translation_path.exists():
        refs["math_translation_json"] = str(math_translation_path)
    if proof_explorer_audit.get("source_path"):
        refs["proof_explorer_audit_html"] = proof_explorer_audit["source_path"]
    sibling_dir = paper_grade_json.parent
    for suffix in [".paper-grade.html", ".paper-grade.md", ".paper-grade.xlsx"]:
        candidate = sibling_dir / paper_grade_json.name.replace(".paper-grade.json", suffix)
        if candidate.exists():
            refs[candidate.suffix.lower().lstrip(".")] = str(candidate)
    return refs


def build_coverage(snapshot: dict[str, Any]) -> dict[str, Any]:
    required_keys = [
        "identity",
        "source",
        "graph_tags",
        "extracted_equations",
        "math_translation_layer",
        "claims",
        "claimed_placeholders",
        "not_claimed_placeholders",
        "seven_qs",
        "station_marks",
        "output_path_references",
    ]
    present = [key for key in required_keys if key in snapshot]
    placeholder_sections = []
    if snapshot["math_translation_layer"]["status"] == "not_found":
        placeholder_sections.append("math_translation_layer")
    for key, value in snapshot["seven_qs"].items():
        if value.get("notes", "").startswith("Placeholder") or not value.get("answer"):
            placeholder_sections.append(f"seven_qs.{key}")
    return {
        "required_keys_total": len(required_keys),
        "required_keys_present": len(present),
        "required_keys_missing": [key for key in required_keys if key not in snapshot],
        "claim_count": len(snapshot["claims"]),
        "equation_count": len(snapshot["extracted_equations"]),
        "translated_span_count": len(snapshot["math_translation_layer"]["translated_spans"]),
        "placeholder_sections": placeholder_sections,
    }


def main() -> int:
    args = parse_args()
    paper_grade = read_json(args.paper_grade_json)
    claim_rows = load_claim_rows(args.claim_audit_csv)
    paper_id = paper_grade.get("paper_id", args.paper_grade_json.stem.replace(".paper-grade", ""))
    live_source = find_live_source(paper_id, args.source_html, paper_grade.get("source_file"))
    title = title_from_html(live_source, paper_id)
    article_number = article_number_from_paper_id(paper_id)
    claims, evidence, contradictions, not_claimed = build_claims(claim_rows)
    equations = normalize_equations(paper_grade.get("equations", []))
    math_translation = build_math_translation(args.math_translation_json, equations, claims)
    proof_explorer_audit = read_proof_explorer_audit(args.proof_explorer_audit_html, args.proof_explorer_audit_fallback_html)
    if proof_explorer_audit and not proof_audit_matches_paper(proof_explorer_audit, paper_id, title):
        proof_explorer_audit = {}
    rigor_report = read_rigor_report(find_rigor_report_json(args.paper_grade_json))
    semantic_fields = build_semantic_fields(live_source)
    if proof_explorer_audit.get("not_claimed"):
        not_claimed = sorted({*not_claimed, *[normalize_text(item) for item in proof_explorer_audit["not_claimed"]]})
    output_path = args.output or args.paper_grade_json.with_name(f"{paper_id}.paper-snapshot.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    graph_tags = extract_topical_tags(title, claims, equations)
    seven_qs = build_seven_qs(title, paper_id, claims, proof_explorer_audit, rigor_report)
    epistemic_status = build_epistemic_status(claims, proof_explorer_audit, rigor_report, not_claimed)
    derivations = build_derivations(claims, proof_explorer_audit, rigor_report)

    snapshot = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "snapshot_id": f"{paper_id}.paper-snapshot",
        "snapshot_status": "draft",
        "source_id": paper_id,
        "source_path": str(live_source) if live_source else paper_grade.get("source_file", ""),
        "title": title,
        "tags": graph_tags,
        "identity": {
            "snapshot_id": f"{paper_id}.paper-snapshot",
            "source_id": paper_id,
            "source_path": str(live_source) if live_source else paper_grade.get("source_file", ""),
            "title": title,
            "series": "Genesis-to-Quantum",
            "article_number": article_number,
            "author": "David Lowe",
            "created_at": paper_grade.get("generated_at"),
            "updated_at": datetime.now().isoformat(timespec="seconds"),
            "canonical_status": "draft",
            "input_format": "html",
            "output_formats": ["json"],
        },
        "source": {
            "selected_source_path": str(live_source) if live_source else None,
            "selected_source_hash_sha256": sha256_file(live_source) if live_source and live_source.exists() else None,
            "paper_grader_source_path": paper_grade.get("source_file"),
            "paper_grader_source_hash_sha256": None,
        },
        **semantic_fields,
        "graph_tags": graph_tags,
        "extracted_equations": [
            {"equation_id": f"eq-{index:03d}", "text": equation, "source": "paper_grade_json"}
            for index, equation in enumerate(equations, start=1)
        ],
        "math_translation_layer": math_translation,
        "claims": claims,
        "claimed_placeholders": [
            {"claim_id": claim["claim_id"], "status": "claimed", "notes": "Seeded from claim audit row."}
            for claim in claims
        ],
        "not_claimed_placeholders": not_claimed,
        "seven_qs": seven_qs,
        "epistemic_status": epistemic_status,
        "station_marks": build_station_marks(args.paper_grade_json, args.claim_audit_csv, math_translation, proof_explorer_audit, output_path),
        "output_path_references": build_output_refs(
            args.paper_grade_json,
            args.claim_audit_csv,
            args.lossless_summary_md,
            live_source,
            args.math_translation_json,
            proof_explorer_audit,
            output_path,
        ),
        "derivations": derivations,
        "evidence": evidence,
        "contradictions": contradictions,
        "method_passes": {
            "paper_grader_metrics": paper_grade.get("metrics", {}),
            "claim_audit_rows": len(claim_rows),
            "math_translation_status": math_translation["status"],
            "rigor_verdict": rigor_report.get("verdict"),
        },
    }
    snapshot["field_coverage"] = build_coverage(snapshot)

    output_path.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"output_path": str(output_path), "field_coverage": snapshot["field_coverage"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
