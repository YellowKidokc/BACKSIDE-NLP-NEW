from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


WORKFLOW_ROOT = Path(__file__).resolve().parent.parent
LANE_ROOT = Path(__file__).resolve().parent
EXPORTS_ROOT = WORKFLOW_ROOT / "EXPORTS"
LOOPBACK_DIR = EXPORTS_ROOT / "loopback_review"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def token_set(text: str) -> set[str]:
    return set(re.findall(r"[A-Za-z0-9_]+", text.lower()))


def cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def jaccard(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    inter = left & right
    union = left | right
    return len(inter) / len(union)


def edge_id(page_id: str, source_id: str, target_id: str, edge_type: str) -> str:
    raw = f"{page_id}|{source_id}|{target_id}|{edge_type}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def resolve_defaults(article: str) -> dict[str, Path | None]:
    sample_root = WORKFLOW_ROOT
    return {
        "vectors": sample_root / "08_SECTION_VECTORS" / "sample_output" / article / "section-vectors.jsonl",
        "section_map": sample_root / "02_SECTION_MAP" / "sample_output" / article / "section-map.json",
        "metadata": sample_root / "03_YAML_METADATA" / "sample_output" / article / "metadata.json",
        "tags": sample_root / "04_TAGS" / "sample_output" / article / "tags.json",
        "claims": sample_root / "05_CLAIMS" / "sample_output" / article / "claim-packets.json",
        "math": sample_root / "07_MATH_TRANSLATION" / "sample_output" / article / "math-payload.json",
        "output_dir": EXPORTS_ROOT / "graph_links" / article,
    }


def section_role(section: dict) -> str:
    heading_text = (section.get("heading_text") or "").strip().lower()
    text = " ".join([section.get("section_id", ""), heading_text, " ".join(section.get("heading_path", []))]).lower()
    if "kill-condition" in text or "kill condition" in text:
        return "kill_condition"
    if "risk" in text:
        return "risk"
    if heading_text == "checklist":
        return "checklist"
    if "equation" in text:
        return "equation"
    if "summary" in text:
        return "summary"
    return "section"


def build_claim_lookup(claims_payload: dict | None, sections: dict[str, dict]) -> tuple[dict[str, list[str]], bool]:
    lookup: dict[str, list[str]] = {}
    mocked = False
    if claims_payload:
        for section in claims_payload.get("sections", []):
            texts = []
            for claim in section.get("claims", []):
                for key in ("surface_claim", "buried_claim", "operational_claim"):
                    value = claim.get(key)
                    if value:
                        texts.append(value)
            lookup[section["section_id"]] = texts
        return lookup, mocked

    mocked = True
    for section_id, section in sections.items():
        heading = section.get("heading_text") or section_id
        excerpt = (section.get("text_excerpt") or "").strip()
        if not excerpt:
            excerpt = " ".join(section.get("heading_path", []))
        lookup[section_id] = [heading, excerpt[:220]]
    return lookup, mocked


def build_tag_lookup(tags_payload: dict | None, sections: dict[str, dict]) -> tuple[dict[str, dict[str, set[str]]], bool]:
    lookup: dict[str, dict[str, set[str]]] = {}
    mocked = False
    if tags_payload:
        for section in tags_payload.get("sections", []):
            lookup[section["section_id"]] = {
                "chi_vars": set(section.get("chi_vars", [])),
                "laws": set(section.get("laws", [])),
            }
        return lookup, mocked

    mocked = True
    for section_id, section in sections.items():
        heading = " ".join(section.get("heading_path", [])).lower()
        chi_vars: set[str] = set()
        laws: set[str] = set()
        if any(word in heading for word in ("equation", "math", "calculus", "parameter")):
            chi_vars.update({"chi_K", "chi_M"})
        if any(word in heading for word in ("surrender", "salvation", "god", "grace", "faith")):
            chi_vars.update({"chi_F", "chi_C"})
        if any(word in heading for word in ("kill", "risk", "audit", "falsification")):
            chi_vars.update({"chi_G", "chi_R"})
        if any(word in heading for word in ("law", "framework", "coherence")):
            laws.add("Law_10")
        lookup[section_id] = {"chi_vars": chi_vars, "laws": laws}
    return lookup, mocked


def add_edge(edges: dict[str, dict], page_id: str, source_id: str, target_id: str, edge_type: str, weight: float, evidence: str, provenance: dict) -> None:
    if source_id == target_id:
        return
    if source_id > target_id:
        source_id, target_id = target_id, source_id
    eid = edge_id(page_id, source_id, target_id, edge_type)
    rounded = round(max(0.0, min(weight, 1.0)), 4)
    current = edges.get(eid)
    payload = {
        "edge_id": eid,
        "page_id": page_id,
        "source_id": source_id,
        "target_id": target_id,
        "edge_type": edge_type,
        "weight": rounded,
        "evidence": evidence,
        "provenance": provenance,
    }
    if current is None or payload["weight"] > current["weight"]:
        edges[eid] = payload


def write_csv(path: Path, edges: list[dict], paper_uuid: str) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["paper_uuid", "page_id", "edge_id", "source_id", "target_id", "edge_type", "weight", "evidence", "provenance"],
        )
        writer.writeheader()
        for edge in edges:
            writer.writerow(
                {
                    "paper_uuid": paper_uuid,
                    "page_id": edge["page_id"],
                    "edge_id": edge["edge_id"],
                    "source_id": edge["source_id"],
                    "target_id": edge["target_id"],
                    "edge_type": edge["edge_type"],
                    "weight": edge["weight"],
                    "evidence": edge["evidence"],
                    "provenance": edge["provenance"]["label"],
                }
            )


def write_review(path: Path, article: str, edge_rows: list[dict], mocked_claims: bool, mocked_tags: bool, section_count: int) -> None:
    lines = [
        f"# 09_GRAPH_LINKS Review - {article}",
        "",
        f"- generated: {utc_now()}",
        f"- section count: {section_count}",
        f"- edge count: {len(edge_rows)}",
        f"- mocked claims: {'yes' if mocked_claims else 'no'}",
        f"- mocked tags: {'yes' if mocked_tags else 'no'}",
        "",
        "## Top edges",
    ]
    for edge in edge_rows[:12]:
        lines.append(
            f"- `{edge['source_id']}` -> `{edge['target_id']}` | `{edge['edge_type']}` | weight {edge['weight']}: {edge['evidence']}"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_loopback(article: str, reasons: list[str], output_dir: Path) -> None:
    if not reasons:
        return
    ensure_dir(LOOPBACK_DIR)
    write_json(
        LOOPBACK_DIR / "09_graph_links_loopback.json",
        {
            "lane_id": "09",
            "lane_name": "Graph Links",
            "article_slug": article,
            "generated_at_utc": utc_now(),
            "output_dir": output_dir.as_posix(),
            "reasons": reasons,
        },
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Emit graph edge candidates for the HTML article workflow.")
    parser.add_argument("--article", help="Named sample article under sample_output/, e.g. calibration or gtq-03.")
    parser.add_argument("--vectors", help="Explicit path to section-vectors.jsonl.")
    parser.add_argument("--section-map", help="Explicit path to section-map.json.")
    parser.add_argument("--metadata", help="Explicit path to metadata.json.")
    parser.add_argument("--tags", help="Explicit path to tags.json.")
    parser.add_argument("--claims", help="Explicit path to claim-packets.json.")
    parser.add_argument("--math", help="Explicit path to math-payload.json.")
    parser.add_argument("--output-dir", help="Output directory for graph artifacts.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.article:
        defaults = resolve_defaults(args.article)
        article = args.article
    else:
        if not (args.vectors and args.section_map and args.metadata):
            print("Need --article or explicit --vectors/--section-map/--metadata", file=sys.stderr)
            return 2
        defaults = {
            "vectors": Path(args.vectors),
            "section_map": Path(args.section_map),
            "metadata": Path(args.metadata),
            "tags": Path(args.tags) if args.tags else None,
            "claims": Path(args.claims) if args.claims else None,
            "math": Path(args.math) if args.math else None,
            "output_dir": Path(args.output_dir) if args.output_dir else LANE_ROOT,
        }
        article = Path(args.section_map).parent.name

    vectors_path = defaults["vectors"]
    section_map_path = defaults["section_map"]
    metadata_path = defaults["metadata"]
    if not vectors_path or not Path(vectors_path).exists():
        print("Vectors input missing. Run lane 08 first.", file=sys.stderr)
        return 2
    if not section_map_path or not Path(section_map_path).exists():
        print("Section map missing.", file=sys.stderr)
        return 2
    if not metadata_path or not Path(metadata_path).exists():
        print("Metadata missing.", file=sys.stderr)
        return 2

    output_dir = Path(defaults["output_dir"])
    ensure_dir(output_dir)

    vector_rows = load_jsonl(Path(vectors_path))
    section_map = load_json(Path(section_map_path))
    metadata = load_json(Path(metadata_path))
    tags_payload = load_json(Path(defaults["tags"])) if defaults.get("tags") and Path(defaults["tags"]).exists() else None
    claims_payload = load_json(Path(defaults["claims"])) if defaults.get("claims") and Path(defaults["claims"]).exists() else None
    math_payload = load_json(Path(defaults["math"])) if defaults.get("math") and Path(defaults["math"]).exists() else None

    sections = {section["section_id"]: section for section in section_map.get("sections", [])}
    if len(vector_rows) != len(sections):
        loopback_reasons = [f"Vector rows {len(vector_rows)} do not cover section count {len(sections)}."]
    else:
        loopback_reasons = []

    claim_lookup, mocked_claims = build_claim_lookup(claims_payload, sections)
    tag_lookup, mocked_tags = build_tag_lookup(tags_payload, sections)
    math_sections = set()
    if math_payload:
        for entry in math_payload.get("equations", []):
            hint = entry.get("section_hint")
            if hint:
                math_sections.add(hint)

    edges: dict[str, dict] = {}
    page_id = metadata["page_id"]

    vector_by_section = {row["section_id"]: row for row in vector_rows}
    section_ids = list(sections.keys())
    for idx, source_id in enumerate(section_ids):
        left_vec = vector_by_section[source_id]["embedding"]
        left_tokens = token_set(" ".join(claim_lookup.get(source_id, [])) + " " + " ".join(sections[source_id].get("heading_path", [])))
        left_tags = tag_lookup.get(source_id, {"chi_vars": set(), "laws": set()})
        left_role = section_role(sections[source_id])

        for target_id in section_ids[idx + 1 :]:
            right_vec = vector_by_section[target_id]["embedding"]
            right_tokens = token_set(" ".join(claim_lookup.get(target_id, [])) + " " + " ".join(sections[target_id].get("heading_path", [])))
            right_tags = tag_lookup.get(target_id, {"chi_vars": set(), "laws": set()})
            right_role = section_role(sections[target_id])

            similarity = cosine(left_vec, right_vec)
            if similarity >= 0.72:
                add_edge(
                    edges,
                    page_id,
                    source_id,
                    target_id,
                    "THEMATIC_SIMILARITY",
                    similarity,
                    f"Cosine similarity {similarity:.3f} between section vectors.",
                    {"label": "lane09", "mocked": False},
                )

            claim_score = jaccard(left_tokens, right_tokens)
            if claim_score >= 0.18:
                add_edge(
                    edges,
                    page_id,
                    source_id,
                    target_id,
                    "CLAIM_OVERLAP",
                    max(claim_score, 0.35),
                    f"Shared claim/heading vocabulary overlap = {claim_score:.3f}.",
                    {"label": "mocked" if mocked_claims else "lane09", "mocked": bool(mocked_claims)},
                )

            chi_overlap = left_tags["chi_vars"] & right_tags["chi_vars"]
            if chi_overlap:
                add_edge(
                    edges,
                    page_id,
                    source_id,
                    target_id,
                    "VARIABLE_OVERLAP",
                    min(1.0, 0.35 + 0.1 * len(chi_overlap)),
                    f"Shared chi vars: {', '.join(sorted(chi_overlap))}.",
                    {"label": "mocked" if mocked_tags else "lane09", "mocked": bool(mocked_tags)},
                )

            law_overlap = left_tags["laws"] & right_tags["laws"]
            if law_overlap:
                add_edge(
                    edges,
                    page_id,
                    source_id,
                    target_id,
                    "LAW_FAMILY",
                    min(1.0, 0.4 + 0.1 * len(law_overlap)),
                    f"Shared law refs: {', '.join(sorted(law_overlap))}.",
                    {"label": "mocked" if mocked_tags else "lane09", "mocked": bool(mocked_tags)},
                )

            if {left_role, right_role} == {"checklist", "kill_condition"}:
                add_edge(
                    edges,
                    page_id,
                    source_id,
                    target_id,
                    "STRUCTURAL_DEPENDENCY",
                    0.97,
                    "Calibration expectation: checklist must connect to kill_condition via pass/fail dependency.",
                    {"label": "lane09", "mocked": False},
                )

            if {left_role, right_role} == {"checklist", "risk"}:
                add_edge(
                    edges,
                    page_id,
                    source_id,
                    target_id,
                    "STRUCTURAL_DEPENDENCY",
                    0.95,
                    "Calibration expectation: checklist must connect to risk because incomplete checks create unsafe takeoff conditions.",
                    {"label": "lane09", "mocked": False},
                )

            if "THEOPHYSICS" in metadata.get("domain", "") and ("theology" in " ".join(sections[source_id].get("heading_path", [])).lower()) != ("theology" in " ".join(sections[target_id].get("heading_path", [])).lower()):
                if similarity >= 0.6:
                    add_edge(
                        edges,
                        page_id,
                        source_id,
                        target_id,
                        "CROSS_DOMAIN",
                        similarity,
                        "High vector affinity across differently framed sections inside a cross-domain article.",
                        {"label": "lane09", "mocked": False},
                    )

            if source_id in math_sections or target_id in math_sections:
                if similarity >= 0.58:
                    add_edge(
                        edges,
                        page_id,
                        source_id,
                        target_id,
                        "STRUCTURAL_DEPENDENCY",
                        similarity,
                        "Equation-bearing section likely anchors nearby explanatory section.",
                        {"label": "lane09", "mocked": False},
                    )

    edge_rows = sorted(edges.values(), key=lambda edge: (-edge["weight"], edge["edge_type"], edge["source_id"], edge["target_id"]))
    max_edges = max(20, len(sections) * 4)
    trimmed = False
    if len(edge_rows) > max_edges:
        edge_rows = edge_rows[:max_edges]
        trimmed = True
    if len(sections) > 1 and not edge_rows:
        loopback_reasons.append("No edges produced for a multi-section article.")
    if len(edge_rows) != len({edge["edge_id"] for edge in edge_rows}):
        loopback_reasons.append("Duplicate edge ids remained after dedup.")
    if article != "calibration" and claims_payload is None:
        loopback_reasons.append("Claims missing for non-calibration article; local claim signals were used.")

    payload = {
        "lane_id": "09",
        "lane_name": "Graph Links",
        "article_slug": article,
        "paper_uuid": metadata["paper_uuid"],
        "page_id": page_id,
        "title": metadata["title"],
        "generated_at_utc": utc_now(),
        "section_count": len(sections),
        "edge_count": len(edge_rows),
        "trimmed": trimmed,
        "max_edges": max_edges,
        "mocked_claims": mocked_claims,
        "mocked_tags": mocked_tags,
        "edges": edge_rows,
        "loopback": {"triggered": bool(loopback_reasons), "reasons": loopback_reasons},
    }
    write_json(output_dir / "graph-edges.json", payload)
    write_csv(output_dir / "graph-edges.csv", edge_rows, metadata["paper_uuid"])
    write_review(output_dir / "graph-review.md", article, edge_rows, mocked_claims, mocked_tags, len(sections))
    build_loopback(article, loopback_reasons, output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
