from __future__ import annotations

import argparse
import csv
import html
import json
import re
import unicodedata
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


STATION_DIR = Path(__file__).resolve().parent
CONFIG_PATH = STATION_DIR / "config.json"

KEEP_LABELS = {"Formal Model", "Structural Correspondence", "Public Proof Claim", "Empirical Support"}
REVIEW_LABELS = {"Analogy"}
METADATA_SECTIONS = {
    "related work",
    "previous",
    "next",
    "read aloud",
    "deep dive",
    "podcast",
    "document start",
    "no promoted claim",
}
PIPELINE_METADATA_PHRASES = {
    "easy and academic are reserved surfaces",
    "proof opens the evidence and derivation layer",
    "no claim from this article survived",
}
AUTHOR_POSTURE_SECTION_WORDS = {
    "author posture",
    "biaxiosum",
}
NARRATIVE_SECTION_WORDS = {
    "the drive",
    "the options",
    "the world",
    "the world of",
    "march ",
    "1900:",
    "1920:",
    "1940:",
    "1950:",
    "1960:",
    "1970:",
    "1980:",
    "1990:",
    "2000:",
    "2010:",
    "2020:",
    "samuel lowe",
    "henry",
    "william",
    "jacob",
}
LOAD_BEARING_SECTION_WORDS = {
    "thesis",
    "lesson",
    "claim",
    "proof",
    "evidence",
    "data",
    "metric",
    "mechanism",
    "control",
    "baseline",
    "result",
    "method",
    "model",
}
MODEL_CLAIM_TERMS = {
    "axiom",
    "causal",
    "causality",
    "coherence",
    "constraint",
    "control group",
    "correlation",
    "decline",
    "entropy",
    "equation",
    "falsifiable",
    "falsification",
    "framework",
    "mechanism",
    "metric",
    "model",
    "prediction",
    "proof",
    "theorem",
    "threshold",
}
SUPPORTING_FACT_TERMS = {
    "census",
    "data",
    "dataset",
    "gallup",
    "gss",
    "percent",
    "percentage",
    "rate",
    "study",
    "survey",
}
AUTHOR_VOICE_TERMS = {
    "i argue",
    "i believe",
    "i came",
    "i claim",
    "i hold",
    "i present",
    "i think",
    "i walked",
    "i would",
    "my claim",
    "my view",
    "we argue",
    "we believe",
    "we should",
}
ANALYTIC_SECTION_WORDS = {
    "analyst",
    "commentary",
    "claim",
    "conclusion",
    "data",
    "equation",
    "evidence",
    "mechanism",
    "method",
    "model",
    "proof",
    "result",
    "statistical",
    "synthesis",
    "threshold",
}


def load_config() -> dict[str, Any]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inventory and triage MDA claim-audit rows before 7Q.")
    parser.add_argument("--claim-audits-dir", default=None, help="Folder containing *.claim-audit.csv.")
    parser.add_argument("--articles-dir", default=None, help="Folder containing source MDA markdown articles.")
    parser.add_argument("--output", default=None, help="Output run directory.")
    return parser.parse_args()


def article_id(path: Path) -> str:
    return path.name.replace(".claim-audit.csv", "")


def claim_id_for(article: str, row_index: int) -> str:
    return f"{article}:claim-{row_index:03d}"


def normalize_for_match(text: str) -> str:
    text = html.unescape(text or "")
    text = unicodedata.normalize("NFKD", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("\\_", "_")
    text = re.sub(r"[`*_#>$~|{}()\[\]\"'“”‘’]", " ", text)
    text = re.sub(r"[^a-zA-Z0-9]+", " ", text).lower()
    return re.sub(r"\s+", " ", text).strip()


def token_set(text: str) -> set[str]:
    return {token for token in normalize_for_match(text).split() if len(token) >= 4}


def overlap_score(query: str, target: str) -> float:
    query_tokens = token_set(query)
    if not query_tokens:
        return 0.0
    target_tokens = token_set(target)
    return len(query_tokens & target_tokens) / len(query_tokens)


def strip_frontmatter(text: str) -> tuple[str, dict[str, str]]:
    if not text.startswith("---"):
        return text, {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return text, {}
    meta: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"')
    return parts[2].lstrip(), meta


def split_sentences(text: str) -> list[str]:
    pieces: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        line = re.sub(r"^[*\-\d.]+\s*", "", line)
        pieces.extend(part.strip() for part in re.split(r"(?<=[.!?])\s+", line) if part.strip())
    return pieces or [text.strip()]


def load_article_locations(article_path: Path) -> dict[str, Any]:
    raw = article_path.read_text(encoding="utf-8", errors="replace")
    body, meta = strip_frontmatter(raw)
    blocks = [block.strip() for block in re.split(r"\n\s*\n", body) if block.strip()]
    paragraphs: list[dict[str, Any]] = []
    heading = ""
    paragraph_index = 0
    for block in blocks:
        heading_match = re.match(r"^(#{1,6})\s+(.+)$", block)
        if heading_match:
            heading = heading_match.group(2).strip()
        paragraph_index += 1
        paragraphs.append(
            {
                "paragraph_index": paragraph_index,
                "heading": heading,
                "text": block,
                "normalized": normalize_for_match(block),
                "sentences": split_sentences(block),
            }
        )
    return {"path": article_path, "frontmatter": meta, "paragraphs": paragraphs}


def build_article_cache(articles_dir: Path) -> dict[str, dict[str, Any]]:
    cache: dict[str, dict[str, Any]] = {}
    if not articles_dir.exists():
        return cache
    for path in sorted(articles_dir.glob("MDA-*.md")):
        cache[path.stem] = load_article_locations(path)
    return cache


def best_sentence_index(claim: str, sentences: list[str]) -> tuple[int, str, float]:
    best_index = 0
    best_sentence = ""
    best_score = 0.0
    claim_norm = normalize_for_match(claim)
    for index, sentence in enumerate(sentences, start=1):
        sentence_norm = normalize_for_match(sentence)
        if claim_norm and claim_norm in sentence_norm:
            return index, sentence, 1.0
        score = overlap_score(claim, sentence)
        if score > best_score:
            best_index = index
            best_sentence = sentence
            best_score = score
    return best_index, best_sentence, best_score


def locate_claim(article_cache: dict[str, dict[str, Any]], article: str, row_index: int, section: str, claim: str) -> dict[str, str]:
    claim_anchor = f"claim-{article}-r{row_index:03d}"
    base = {
        "source_article_path": "",
        "canonical_html_hint": "",
        "proof_anchor": claim_anchor,
        "locator_status": "ARTICLE_NOT_FOUND",
        "paragraph_index": "",
        "sentence_index": "",
        "matched_heading": "",
        "matched_excerpt": "",
        "locator_confidence": "0.00",
    }
    article_record = article_cache.get(article)
    if not article_record:
        return base

    base["source_article_path"] = str(article_record["path"])
    base["canonical_html_hint"] = article_record.get("frontmatter", {}).get("source_path", "")
    paragraphs = article_record["paragraphs"]
    claim_norm = normalize_for_match(claim)
    section_norm = normalize_for_match(section)

    for paragraph in paragraphs:
        if claim_norm and claim_norm in paragraph["normalized"]:
            sentence_index, sentence, sentence_score = best_sentence_index(claim, paragraph["sentences"])
            base.update(
                {
                    "locator_status": "EXACT_SENTENCE" if sentence_score >= 1.0 else "EXACT_PARAGRAPH",
                    "paragraph_index": str(paragraph["paragraph_index"]),
                    "sentence_index": str(sentence_index) if sentence_index else "",
                    "matched_heading": paragraph["heading"],
                    "matched_excerpt": (sentence or paragraph["text"])[:500],
                    "locator_confidence": "1.00" if sentence_score >= 1.0 else "0.92",
                }
            )
            return base

    for offset in range(len(paragraphs)):
        window = paragraphs[offset : offset + 4]
        combined = normalize_for_match(" ".join(paragraph["text"] for paragraph in window))
        if claim_norm and claim_norm in combined:
            paragraph = window[0]
            base.update(
                {
                    "locator_status": "EXACT_PARAGRAPH",
                    "paragraph_index": str(paragraph["paragraph_index"]),
                    "sentence_index": "",
                    "matched_heading": paragraph["heading"],
                    "matched_excerpt": " ".join(item["text"] for item in window)[:500],
                    "locator_confidence": "0.92",
                }
            )
            return base

    candidates = paragraphs
    if section_norm:
        section_candidates = [
            paragraph
            for paragraph in paragraphs
            if section_norm in normalize_for_match(paragraph["heading"])
            or normalize_for_match(paragraph["heading"]) in section_norm
        ]
        if section_candidates:
            candidates = section_candidates

    best_paragraph: dict[str, Any] | None = None
    best_score = 0.0
    for paragraph in candidates:
        score = overlap_score(claim, paragraph["text"])
        if score > best_score:
            best_score = score
            best_paragraph = paragraph

    if best_paragraph and best_score >= 0.35:
        sentence_index, sentence, sentence_score = best_sentence_index(claim, best_paragraph["sentences"])
        base.update(
            {
                "locator_status": "SECTION_FUZZY" if candidates is not paragraphs else "ARTICLE_FUZZY",
                "paragraph_index": str(best_paragraph["paragraph_index"]),
                "sentence_index": str(sentence_index) if sentence_index else "",
                "matched_heading": best_paragraph["heading"],
                "matched_excerpt": (sentence or best_paragraph["text"])[:500],
                "locator_confidence": f"{max(best_score, sentence_score):.2f}",
            }
        )
        return base

    base["locator_status"] = "NOT_FOUND"
    return base


def has_real_evidence(row: dict[str, str]) -> bool:
    evidence = (row.get("evidence_bar") or "").strip()
    if not evidence:
        return False
    return "No explicit evidence marker" not in evidence


def has_kill_condition(row: dict[str, str]) -> bool:
    kill = (row.get("kill_conditions") or "").strip()
    if not kill:
        return False
    return "Needs an explicit failure case" not in kill


def is_markdown_table(text: str) -> bool:
    return text.count("|") >= 6 or "| --- |" in text


def is_author_posture_section(section: str) -> bool:
    text = section.lower()
    return any(term in text for term in AUTHOR_POSTURE_SECTION_WORDS)


def is_narrative_or_example_section(section: str) -> bool:
    text = section.lower().strip()
    return any(text == term or text.startswith(term) or term in text for term in NARRATIVE_SECTION_WORDS)


def is_analytic_section(section: str) -> bool:
    text = section.lower()
    return any(term in text for term in ANALYTIC_SECTION_WORDS)


def has_model_claim_terms(section: str, claim: str) -> bool:
    text = f"{section} {claim}".lower()
    strong_terms = MODEL_CLAIM_TERMS - {"model", "equation", "framework"}
    if any(term in text for term in strong_terms):
        return True
    model_patterns = [
        r"\b(the|our|mda|coherence|decline|decay|formal)\s+model\b",
        r"\bmodel\s+(predicts|requires|survived|fails|would|explains|claims|says)\b",
        r"\bmodel would be falsified\b",
    ]
    equation_patterns = [
        r"\bequation\s+(predicts|requires|reads|says|shows|claims)\b",
        r"\brun the equation\b",
    ]
    if any(re.search(pattern, text) for pattern in model_patterns + equation_patterns):
        return True
    if "framework" in text and any(term in text for term in {"claim", "proof", "evidence", "prediction"}):
        return True
    return False


def has_supporting_fact_shape(section: str, claim: str) -> bool:
    text = f"{section} {claim}".lower()
    has_number_or_date = bool(re.search(r"\b(1[5-9]\d{2}|20\d{2}|\d+(\.\d+)?\s?%|\d+(\.\d+)?)\b", text))
    has_fact_term = any(term in text for term in SUPPORTING_FACT_TERMS)
    has_named_source = bool(re.search(r"\b(pew|gss|gallup|census|fred|seshat|barna)\b", text))
    return has_number_or_date or has_fact_term or has_named_source


def has_author_voice(claim: str) -> bool:
    text = claim.lower()
    return any(term in text for term in AUTHOR_VOICE_TERMS)


def classify(row: dict[str, str]) -> tuple[str, int, str]:
    section = (row.get("section") or "").strip()
    section_l = section.lower()
    claim = (row.get("one_sentence_claim") or "").strip()
    claim_l = claim.lower()
    label = (row.get("claim_maturity_label") or "").strip()

    score = 0
    reasons: list[str] = []

    if not claim:
        return "EXCLUDE_EMPTY", -5, "empty claim text"

    if any(section_l == item or section_l.startswith(item) for item in METADATA_SECTIONS):
        return "EXCLUDE_METADATA", -4, f"metadata/navigation section: {section}"

    if any(phrase in claim_l for phrase in PIPELINE_METADATA_PHRASES):
        return "EXCLUDE_METADATA", -4, "website shell or pipeline placeholder text"

    composite_claim = is_markdown_table(claim) or len(claim) > 650 or "![" in claim
    model_shaped = has_model_claim_terms(section, claim)
    fact_shaped = has_supporting_fact_shape(section, claim)
    narrative_section = is_narrative_or_example_section(section)
    analytic_section = is_analytic_section(section)

    if is_author_posture_section(section):
        return "PARK_AUTHOR_VOICE_OR_RHETORIC", 0, "author posture/context, not a paper claim"

    if composite_claim:
        return "NEEDS_SPLIT", 2, "composite/table claim needs splitting before 7Q"

    if has_author_voice(claim) and "supporting claims" not in section_l and "primary claim" not in section_l:
        return "PARK_AUTHOR_VOICE_OR_RHETORIC", 0, "author voice or personal/theological aside, not paper claim"

    if narrative_section and not analytic_section:
        if fact_shaped:
            return "CITATION_FACT_QUEUE", 2, "narrative/supporting fact needs source check, not 7Q"
        return "PARK_AUTHOR_VOICE_OR_RHETORIC", 0, "narrative/example row, not load-bearing paper claim"

    if re.search(r"\bmodel t\b", claim_l):
        return "CITATION_FACT_QUEUE", 2, "Model T/supporting historical fact, not model claim"

    if len(claim.split()) < 8 and model_shaped and not re.search(r"[=<>]|\\frac|\\sum|\\chi|χ|dC/dt", claim):
        return "REVIEW_QUEUE", 2, "short rhetorical model/equation fragment needs human triage"

    if label in KEEP_LABELS:
        score += 4
        reasons.append(f"maturity={label}")
    elif label in REVIEW_LABELS:
        score += 2
        reasons.append(f"review maturity={label}")
    elif label == "Metaphor":
        reasons.append("maturity=Metaphor")
    elif not label:
        reasons.append("missing maturity label")
    else:
        score += 1
        reasons.append(f"other maturity={label}")

    if any(word in section_l for word in LOAD_BEARING_SECTION_WORDS):
        score += 1
        reasons.append(f"load-bearing section={section}")

    if model_shaped:
        score += 1
        reasons.append("model/framework term present")
    elif fact_shaped:
        reasons.append("supporting factual/citation-shaped claim")

    if has_real_evidence(row):
        score += 1
        reasons.append("nearby evidence marker")
    else:
        reasons.append("no explicit evidence marker")

    if has_kill_condition(row):
        score += 1
        reasons.append("has kill condition")
    else:
        reasons.append("missing kill condition")

    if len(claim.split()) < 5:
        score -= 1
        reasons.append("short fragment")

    if score >= 5 and model_shaped:
        return "PAPER_CLAIM_QUEUE", score, "; ".join(reasons)
    if score >= 4 and fact_shaped:
        return "CITATION_FACT_QUEUE", score, "; ".join(reasons)
    if score >= 4 and not model_shaped:
        return "REVIEW_QUEUE", score, "; ".join(reasons)
    if score >= 2:
        return "REVIEW_QUEUE", score, "; ".join(reasons)
    return "PARK_AUTHOR_VOICE_OR_RHETORIC", score, "; ".join(reasons)


def read_claims(claim_dir: Path, article_cache: dict[str, dict[str, Any]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for file_path in sorted(claim_dir.glob("*.claim-audit.csv")):
        aid = article_id(file_path)
        with file_path.open(newline="", encoding="utf-8-sig", errors="replace") as handle:
            reader = csv.DictReader(handle)
            for index, row in enumerate(reader, start=1):
                status, score, reason = classify(row)
                section = row.get("section") or ""
                claim = row.get("one_sentence_claim") or ""
                locator = locate_claim(article_cache, aid, index, section, claim)
                rows.append(
                    {
                        "claim_id": claim_id_for(aid, index),
                        "article_id": aid,
                        "source_csv": str(file_path),
                        "row_index": str(index),
                        "section": section,
                        "claim_text": claim,
                        "claim_maturity_label": row.get("claim_maturity_label") or "",
                        "triage_status": status,
                        "triage_score": str(score),
                        "triage_reason": reason,
                        **locator,
                        "evidence_bar": row.get("evidence_bar") or "",
                        "kill_conditions": row.get("kill_conditions") or "",
                        "Q1_identity": row.get("Q1_identity") or "",
                        "Q2_scope": row.get("Q2_scope") or "",
                        "Q3_mechanism": row.get("Q3_mechanism") or "",
                        "Q4_evidence": row.get("Q4_evidence") or "",
                        "Q5_falsifiability": row.get("Q5_falsifiability") or "",
                        "Q6_boundary": row.get("Q6_boundary") or "",
                        "Q7_listener_risk": row.get("Q7_listener_risk") or "",
                    }
                )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else [
        "claim_id",
        "article_id",
        "source_csv",
        "row_index",
        "section",
        "claim_text",
        "claim_maturity_label",
        "triage_status",
        "triage_score",
        "triage_reason",
        "source_article_path",
        "canonical_html_hint",
        "proof_anchor",
        "locator_status",
        "paragraph_index",
        "sentence_index",
        "matched_heading",
        "matched_excerpt",
        "locator_confidence",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def proof_layer_seed(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    seed: list[dict[str, Any]] = []
    for row in rows:
        seed.append(
            {
                "claim_id": row["claim_id"],
                "article_id": row["article_id"],
                "statement": row["claim_text"],
                "status": "PENDING_7Q",
                "source_stage": "claim_inventory",
                "triage": {
                    "status": row["triage_status"],
                    "score": row["triage_score"],
                    "reason": row["triage_reason"],
                    "maturity_label": row["claim_maturity_label"],
                },
                "location": {
                    "source_article_path": row["source_article_path"],
                    "canonical_html_hint": row["canonical_html_hint"],
                    "proof_anchor": row["proof_anchor"],
                    "section": row["section"],
                    "paragraph_index": row["paragraph_index"],
                    "sentence_index": row["sentence_index"],
                    "matched_heading": row["matched_heading"],
                    "matched_excerpt": row["matched_excerpt"],
                    "locator_status": row["locator_status"],
                    "locator_confidence": row["locator_confidence"],
                },
                "evidence_bar": row["evidence_bar"],
                "kill_condition": row["kill_conditions"],
                "seven_q": {
                    "Q1_identity": row["Q1_identity"],
                    "Q2_scope": row["Q2_scope"],
                    "Q3_mechanism": row["Q3_mechanism"],
                    "Q4_evidence": row["Q4_evidence"],
                    "Q5_falsifiability": row["Q5_falsifiability"],
                    "Q6_boundary": row["Q6_boundary"],
                    "Q7_listener_risk": row["Q7_listener_risk"],
                },
            }
        )
    return seed


def write_report(output_dir: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    lines = [
        "# MDA Claim Inventory",
        "",
        f"- Generated: {summary['generated_at']}",
        f"- Source files: {summary['source_files']}",
        f"- Total claim candidates: {summary['total_claim_candidates']}",
        f"- 7Q queue: {summary['status_counts'].get('PAPER_CLAIM_QUEUE', 0)}",
        f"- Citation fact queue: {summary['status_counts'].get('CITATION_FACT_QUEUE', 0)}",
        f"- Review queue: {summary['status_counts'].get('REVIEW_QUEUE', 0)}",
        f"- Needs split: {summary['status_counts'].get('NEEDS_SPLIT', 0)}",
        f"- Parked/excluded: {summary['parked_or_excluded']}",
        f"- Located exactly: {summary['exact_locations']}",
        f"- Needs locator review: {summary['locator_review_needed']}",
        "",
        "## Status Counts",
        "",
        "| Status | Count |",
        "|---|---:|",
    ]
    for key, count in summary["status_counts"].items():
        lines.append(f"| {key} | {count} |")
    lines.extend(
        [
            "",
            "## Locator Counts",
            "",
            "| Locator Status | Count |",
            "|---|---:|",
        ]
    )
    for key, count in summary["locator_counts"].items():
        lines.append(f"| {key} | {count} |")
    lines.extend(
        [
            "",
            "## Label Counts",
            "",
            "| Maturity Label | Count |",
            "|---|---:|",
        ]
    )
    for key, count in summary["label_counts"].items():
        lines.append(f"| {key or '(blank)'} | {count} |")
    lines.extend(
        [
            "",
            "## First 25 7Q Queue Items",
            "",
            "| Article | Section | Claim |",
            "|---|---|---|",
        ]
    )
    for row in [item for item in rows if item["triage_status"] == "PAPER_CLAIM_QUEUE"][:25]:
        claim = row["claim_text"].replace("|", "\\|")
        if len(claim) > 180:
            claim = claim[:177] + "..."
        lines.append(f"| {row['article_id']} | {row['section']} | {claim} |")
    lines.extend(
        [
            "",
            "## First 25 Citation Fact Queue Items",
            "",
            "| Article | Section | Claim |",
            "|---|---|---|",
        ]
    )
    for row in [item for item in rows if item["triage_status"] == "CITATION_FACT_QUEUE"][:25]:
        claim = row["claim_text"].replace("|", "\\|")
        if len(claim) > 180:
            claim = claim[:177] + "..."
        lines.append(f"| {row['article_id']} | {row['section']} | {claim} |")
    (output_dir / "CLAIM_INVENTORY_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    config = load_config()
    claim_dir = Path(args.claim_audits_dir or config["inputs"]["existing_claim_audits_dir"])
    articles_dir = Path(args.articles_dir or config["inputs"]["articles_dir"])
    if args.output:
        output_dir = Path(args.output)
    else:
        output_dir = Path(config["outputs"]["exports_dir"]) / "claim_inventory" / datetime.now().strftime("run_%Y%m%d_%H%M%S")
    output_dir.mkdir(parents=True, exist_ok=True)

    article_cache = build_article_cache(articles_dir)
    rows = read_claims(claim_dir, article_cache)
    source_files = len({row["source_csv"] for row in rows})
    status_counts = Counter(row["triage_status"] for row in rows)
    label_counts = Counter(row["claim_maturity_label"] for row in rows)
    locator_counts = Counter(row["locator_status"] for row in rows)

    queue = [row for row in rows if row["triage_status"] == "PAPER_CLAIM_QUEUE"]
    citation_facts = [row for row in rows if row["triage_status"] == "CITATION_FACT_QUEUE"]
    review = [row for row in rows if row["triage_status"] in {"REVIEW_QUEUE", "NEEDS_SPLIT"}]
    parked = [
        row
        for row in rows
        if row["triage_status"] not in {"PAPER_CLAIM_QUEUE", "CITATION_FACT_QUEUE", "REVIEW_QUEUE", "NEEDS_SPLIT"}
    ]

    write_csv(output_dir / "all_claim_candidates.csv", rows)
    write_csv(output_dir / "7q_queue.csv", queue)
    write_csv(output_dir / "citation_fact_queue.csv", citation_facts)
    write_csv(output_dir / "review_queue.csv", review)
    write_csv(output_dir / "parked_or_excluded.csv", parked)
    (output_dir / "proof_layer_claims.seed.json").write_text(
        json.dumps(proof_layer_seed(queue), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "claim_audits_dir": str(claim_dir),
        "articles_dir": str(articles_dir),
        "source_files": source_files,
        "source_articles_loaded": len(article_cache),
        "total_claim_candidates": len(rows),
        "status_counts": dict(status_counts),
        "label_counts": dict(label_counts),
        "locator_counts": dict(locator_counts),
        "exact_locations": locator_counts.get("EXACT_SENTENCE", 0) + locator_counts.get("EXACT_PARAGRAPH", 0),
        "locator_review_needed": len(rows)
        - locator_counts.get("EXACT_SENTENCE", 0)
        - locator_counts.get("EXACT_PARAGRAPH", 0),
        "parked_or_excluded": len(parked),
        "outputs": {
            "all": str(output_dir / "all_claim_candidates.csv"),
            "7q_queue": str(output_dir / "7q_queue.csv"),
            "proof_layer_claims_seed": str(output_dir / "proof_layer_claims.seed.json"),
            "citation_fact_queue": str(output_dir / "citation_fact_queue.csv"),
            "review_queue": str(output_dir / "review_queue.csv"),
            "parked_or_excluded": str(output_dir / "parked_or_excluded.csv"),
        },
    }
    (output_dir / "claim_inventory_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_report(output_dir, rows, summary)

    print(f"Wrote claim inventory: {output_dir}")
    print(f"Total candidates: {len(rows)}")
    print(f"7Q queue: {len(queue)}")
    print(f"Citation fact queue: {len(citation_facts)}")
    print(f"Review queue: {len(review)}")
    print(f"Parked/excluded: {len(parked)}")
    print(f"Exact locations: {summary['exact_locations']}")
    print(f"Locator review needed: {summary['locator_review_needed']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
