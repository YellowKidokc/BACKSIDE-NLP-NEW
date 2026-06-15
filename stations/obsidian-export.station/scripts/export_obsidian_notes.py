from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ftfy import fix_text


REQUIRED_FRONTMATTER_KEYS = {
    "uuid",
    "title",
    "type",
    "series",
    "status",
    "maturity",
    "created",
    "updated",
    "tags",
    "source_path",
    "content_hash",
    "target_path",
}
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
PAPER_NUMBER_RE = re.compile(r"gtq-(\d+[a-z]?)", re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export snapshot and YouTube Q/A artifacts to validated Obsidian notes.")
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path(r"X:\Backside\stations\obsidian-export.station\routing_manifest.json"),
        help="Routing manifest with explicit test routes.",
    )
    parser.add_argument("--route-id", action="append", help="Optional specific route_id(s) to process.")
    return parser.parse_args()


def iso_today() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", fix_text(text)).strip()


def dump_yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value).replace('"', '\\"')
    return f'"{text}"'


def build_frontmatter(data: dict[str, Any]) -> str:
    lines = ["---"]
    ordered_keys = [
        "uuid",
        "title",
        "type",
        "series",
        "paper_number",
        "status",
        "maturity",
        "created",
        "updated",
        "source_path",
        "upstream_source_path",
        "content_hash",
        "target_path",
        "route_id",
        "tags",
        "wikilinks",
    ]
    for key in ordered_keys:
        if key not in data:
            continue
        value = data[key]
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {dump_yaml_scalar(item)}")
        else:
            lines.append(f"{key}: {dump_yaml_scalar(value)}")
    lines.append("---")
    return "\n".join(lines)


def parse_frontmatter(note_text: str) -> dict[str, Any]:
    if not note_text.startswith("---\n"):
        raise ValueError("Note is missing opening YAML frontmatter delimiter.")
    parts = note_text.split("\n---\n", 1)
    if len(parts) != 2:
        raise ValueError("Note is missing closing YAML frontmatter delimiter.")
    raw_yaml = parts[0][4:]
    parsed: dict[str, Any] = {}
    current_list_key: str | None = None
    for line in raw_yaml.splitlines():
        if not line.strip():
            continue
        if line.startswith("  - ") and current_list_key:
            parsed.setdefault(current_list_key, []).append(line[4:].strip().strip('"'))
            continue
        current_list_key = None
        if ":" not in line:
            raise ValueError(f"Invalid YAML line: {line}")
        key, raw_value = line.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        if raw_value == "":
            parsed[key] = []
            current_list_key = key
        elif raw_value == "null":
            parsed[key] = None
        elif raw_value.startswith('"') and raw_value.endswith('"'):
            parsed[key] = raw_value[1:-1].replace('\\"', '"')
        else:
            parsed[key] = raw_value
    return parsed


def validate_wikilinks(note_text: str) -> list[str]:
    body = note_text.split("\n---\n", 1)[1]
    warnings: list[str] = []
    if body.count("[[") != body.count("]]"):
        raise ValueError("Unbalanced wikilink delimiters.")
    for match in WIKILINK_RE.finditer(body):
        inner = match.group(1).strip()
        if not inner:
            raise ValueError("Empty wikilink detected.")
        if "\n" in inner:
            raise ValueError("Multiline wikilink detected.")
        if "|" in inner:
            warnings.append(f"Alias wikilink used: {inner}")
    return warnings


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if not value:
            continue
        key = value.lower()
        if key not in seen:
            seen.add(key)
            ordered.append(value)
    return ordered


def validate_note(note_text: str, source_artifact_path: Path) -> dict[str, Any]:
    frontmatter = parse_frontmatter(note_text)
    missing = sorted(REQUIRED_FRONTMATTER_KEYS - set(frontmatter))
    if missing:
        raise ValueError(f"Missing required frontmatter keys: {missing}")
    source_path = Path(frontmatter["source_path"])
    if source_path != source_artifact_path:
        raise ValueError(f"Frontmatter source_path does not match route source: {source_path} != {source_artifact_path}")
    if not source_path.exists():
        raise ValueError(f"Frontmatter source_path does not exist: {source_path}")
    actual_hash = sha256_file(source_path)
    if frontmatter["content_hash"] != actual_hash:
        raise ValueError("Frontmatter content_hash does not match source artifact hash.")
    wikilink_warnings = validate_wikilinks(note_text)
    return {
        "frontmatter": frontmatter,
        "wikilink_warnings": wikilink_warnings,
    }


def render_snapshot_note(route: dict[str, Any], artifact: dict[str, Any], source_artifact_path: Path, target_path: Path) -> str:
    title = artifact.get("title") or route["note_title"]
    source_id = artifact.get("source_id", slugify(title))
    tags = [
        "type/note",
        "pipeline/paper-snapshot",
        "series/genesis-to-quantum",
        "status/review",
        "lane/paper-grader-pds1",
    ]
    graph_tags = artifact.get("graph_tags") or {}
    topical_tags = graph_tags.get("topical") or []
    classifier_domain = ((artifact.get("classifier_tags") or {}).get("domain")) or []
    wikilinks = [
        "Paper Grader PDS1",
        "Genesis to Quantum",
        "Master Equation",
        "Theophysics",
        "Empirical Testing",
        "gtq-17-ran-the-numbers",
    ]
    claims = artifact.get("claims") or []
    translated_spans = ((artifact.get("math_translation_layer") or {}).get("translated_spans")) or []
    seven_qs = artifact.get("seven_qs") or {}
    paper_number_match = PAPER_NUMBER_RE.search(source_id)
    paper_number = paper_number_match.group(1).upper() if paper_number_match else None
    frontmatter = build_frontmatter(
        {
            "uuid": source_id,
            "title": route["note_title"],
            "type": "note",
            "series": "Genesis-to-Quantum",
            "paper_number": paper_number,
            "status": "review",
            "maturity": "developing",
            "created": iso_today(),
            "updated": iso_today(),
            "source_path": str(source_artifact_path),
            "upstream_source_path": artifact.get("source_path", ""),
            "content_hash": sha256_file(source_artifact_path),
            "target_path": str(target_path),
            "route_id": route["route_id"],
            "tags": tags + [f"topic/{slugify(tag)}" for tag in topical_tags] + [f"domain/{slugify(tag)}" for tag in classifier_domain],
            "wikilinks": wikilinks,
        }
    )
    lines = [
        frontmatter,
        "",
        f"# {route['note_title']}",
        "",
        f"Canonical route target: `06_ADVERSARIAL_LAYER/Paper_Grader_PDS1`",
        "",
        f"Source artifact: `{source_artifact_path}`",
        f"Upstream source path: `{artifact.get('source_path', '')}`",
        "",
        "Related anchors: [[Paper Grader PDS1]] | [[Genesis to Quantum]] | [[Master Equation]] | [[Theophysics]] | [[Empirical Testing]] | [[gtq-17-ran-the-numbers]]",
        "",
        "## Snapshot Summary",
        "",
        f"- Source ID: `{source_id}`",
        f"- Title: {title}",
        f"- Claim count: {len(claims)}",
        f"- Seven Q fields: {', '.join(seven_qs.keys()) if seven_qs else 'none'}",
        f"- Math translation status: `{(artifact.get('math_translation_layer') or {}).get('status', 'missing')}`",
        f"- Translated spans: {len(translated_spans)}",
        f"- Epistemic tier: `{(artifact.get('epistemic_status') or {}).get('overall_tier', 'missing')}`",
        "",
        "## Routing Reason",
        "",
        "This note is routed into the PDS-1 adversarial layer because it is a paper-snapshot artifact with claim, evidence, seven-question, and math-translation structure that still needs canon-facing review rather than direct canonization.",
        "",
        "Twin series note: [[gtq-17-ran-the-numbers]]",
        "",
        "## Topic Tags",
        "",
        ", ".join(topical_tags) if topical_tags else "_none_",
        "",
        "## Key Claims",
        "",
    ]
    for claim in claims[:10]:
        lines.append(f"- `{claim.get('claim_id', '')}` {normalize_text(claim.get('text', ''))}")
    if len(claims) > 10:
        lines.append(f"- ... {len(claims) - 10} additional claims omitted in note body")
    lines.extend(["", "## Math Translation Highlights", ""])
    if translated_spans:
        for span in translated_spans[:5]:
            lines.append(f"- `{span.get('equation', span.get('original', ''))}` -> {normalize_text(span.get('translation', span.get('translated', '')))}")
    else:
        lines.append("- No translated spans were present.")
    lines.extend(["", "## Seven Questions", ""])
    for key, value in seven_qs.items():
        summary = ""
        if isinstance(value, dict):
            summary = value.get("summary") or value.get("notes") or value.get("answer") or ""
        lines.append(f"### {key}")
        lines.append("")
        lines.append(summary if summary else "_No summary text in snapshot._")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def render_series_note(route: dict[str, Any], artifact: dict[str, Any], source_artifact_path: Path, target_path: Path) -> str:
    title = artifact.get("title") or route["note_title"]
    source_id = artifact.get("source_id", slugify(title))
    graph_tags = artifact.get("graph_tags") or {}
    topical_tags = graph_tags.get("topical") or []
    claims = artifact.get("claims") or []
    translated_spans = ((artifact.get("math_translation_layer") or {}).get("translated_spans")) or []
    seven_qs = artifact.get("seven_qs") or {}
    paper_number_match = PAPER_NUMBER_RE.search(source_id)
    paper_number = paper_number_match.group(1).upper() if paper_number_match else None
    frontmatter = build_frontmatter(
        {
            "uuid": source_id,
            "title": route["note_title"],
            "type": "note",
            "series": "Genesis-to-Quantum",
            "paper_number": paper_number,
            "status": "review",
            "maturity": "developing",
            "created": iso_today(),
            "updated": iso_today(),
            "source_path": str(source_artifact_path),
            "upstream_source_path": artifact.get("source_path", ""),
            "content_hash": sha256_file(source_artifact_path),
            "target_path": str(target_path),
            "route_id": route["route_id"],
            "tags": [
                "type/note",
                "pipeline/paper-snapshot",
                "series/genesis-to-quantum",
                "status/review",
                "audience/human-series",
            ] + [f"topic/{slugify(tag)}" for tag in topical_tags],
            "wikilinks": [
                "GTQ",
                "Genesis to Quantum",
                "Master Equation",
                "GTQ-17-Ran-the-Numbers-Paper-Snapshot",
            ],
        }
    )
    lines = [
        frontmatter,
        "",
        f"# {title}",
        "",
        "This is the human article or series-facing GTQ note derived from the current paper snapshot.",
        "",
        "Twin audit note: [[GTQ-17-Ran-the-Numbers-Paper-Snapshot]]",
        "",
        f"Source artifact: `{source_artifact_path}`",
        f"Upstream source path: `{artifact.get('source_path', '')}`",
        "",
        "## Routing Rule",
        "",
        "This note belongs in `03_SERIES/GTQ` because it is the human article or series-facing note. The audit and proof-grader companion note for the same source artifact belongs in `06_ADVERSARIAL_LAYER/Paper_Grader_PDS1`.",
        "",
        "## Summary",
        "",
        f"- Claim count: {len(claims)}",
        f"- Topic tags: {', '.join(topical_tags) if topical_tags else 'none'}",
        f"- Math translation spans: {len(translated_spans)}",
        f"- Seven Q fields: {', '.join(seven_qs.keys()) if seven_qs else 'none'}",
        "",
        "## Primary Claim",
        "",
        normalize_text(claims[0].get("text", "")) if claims else "_No primary claim extracted._",
        "",
        "## Human-Facing Framing",
        "",
        "GTQ-17 presents the empirical-testing side of the Master Equation argument: a paper claiming that the framework makes quantitative predictions and that the biblical and historical record fits those predictions in multiple completed tests.",
        "",
        "## Canon Cross-Link",
        "",
        "For audit, rigor, seven-question, and math-translation detail, use [[GTQ-17-Ran-the-Numbers-Paper-Snapshot]].",
        "",
    ]
    return "\n".join(lines).strip() + "\n"


def render_youtube_qa_note(route: dict[str, Any], artifact: dict[str, Any], source_artifact_path: Path, target_path: Path) -> str:
    source = artifact["source"]
    tags = [
        "type/note",
        "pipeline/youtube-qa",
        "status/review",
        "holding-bay/ai-output",
        "series/apologetics",
    ]
    topic_tags = artifact.get("topic_tags") or []
    wikilinks = [
        "Case for Christ",
        "Apologetics",
        "YouTube Q&A",
        "Holding Bay",
    ]
    frontmatter = build_frontmatter(
        {
            "uuid": slugify(source["video_title"]),
            "title": route["note_title"],
            "type": "note",
            "series": "Apologetics",
            "paper_number": None,
            "status": "review",
            "maturity": "seed",
            "created": iso_today(),
            "updated": iso_today(),
            "source_path": str(source_artifact_path),
            "upstream_source_path": source.get("transcript_path", ""),
            "content_hash": sha256_file(source_artifact_path),
            "target_path": str(target_path),
            "route_id": route["route_id"],
            "tags": tags + [f"topic/{slugify(tag)}" for tag in topic_tags],
            "wikilinks": wikilinks,
        }
    )
    lines = [
        frontmatter,
        "",
        f"# {route['note_title']}",
        "",
        f"Canonical route target: `10_HOLDING_BAY/AI_OUTPUTS_NEEDS_REVIEW`",
        "",
        f"Source artifact: `{source_artifact_path}`",
        f"Upstream transcript path: `{source.get('transcript_path', '')}`",
        "",
        "Related anchors: [[Case for Christ]] | [[Apologetics]] | [[YouTube Q&A]] | [[Holding Bay]]",
        "",
        "## Routing Reason",
        "",
        "This note is intentionally routed to the holding bay because it is a generated Q/A extraction artifact that is useful, but not ready for direct production canon placement.",
        "",
        "## Source Summary",
        "",
        f"- Video title: {source.get('video_title', '')}",
        f"- Channel: {source.get('channel', '') or 'unknown'}",
        f"- YouTube URL: {source.get('youtube_url', '') or 'n/a'}",
        f"- Q/A pair count: {len(artifact.get('qa_pairs') or [])}",
        f"- Claim count: {len(artifact.get('claims') or [])}",
        "",
        "## Topic Tags",
        "",
        ", ".join(topic_tags) if topic_tags else "_none_",
        "",
        "## Scripture References",
        "",
    ]
    scripture_refs = artifact.get("scripture_refs") or []
    if scripture_refs:
        for ref in scripture_refs:
            lines.append(f"- {ref}")
    else:
        lines.append("- None detected.")
    lines.extend(["", "## Reusable Q/A Cards", ""])
    for qa in (artifact.get("qa_pairs") or [])[:10]:
        lines.extend(
            [
                f"### {qa.get('qa_id', '')}",
                "",
                f"**Question:** {qa.get('question', '')}",
                "",
                f"**Answer:** {qa.get('answer', '') or '_No explicit answer found._'}",
                "",
                f"- Speakers: Q=`{qa.get('speaker_question', '') or 'unknown'}` A=`{qa.get('speaker_answer', '') or 'unknown'}`",
                f"- Objection type: `{qa.get('objection_type', '') or 'none'}`",
                f"- Answer type: `{qa.get('answer_type', '') or 'unknown'}`",
                f"- Confidence: `{qa.get('confidence', '')}`",
                f"- Evidence refs: {json.dumps(qa.get('evidence_refs') or [], ensure_ascii=False)}",
                f"- Scripture refs: {json.dumps(qa.get('scripture_refs') or [], ensure_ascii=False)}",
                "",
            ]
        )
    return "\n".join(lines).strip() + "\n"


def render_note(route: dict[str, Any], artifact: dict[str, Any], source_artifact_path: Path, target_path: Path) -> str:
    if route["source_kind"] == "paper_snapshot_series":
        return render_series_note(route, artifact, source_artifact_path, target_path)
    if route["source_kind"] == "paper_snapshot":
        return render_snapshot_note(route, artifact, source_artifact_path, target_path)
    if route["source_kind"] == "youtube_qa":
        return render_youtube_qa_note(route, artifact, source_artifact_path, target_path)
    raise ValueError(f"Unsupported source_kind: {route['source_kind']}")


def load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def process_route(route: dict[str, Any], canon_root: Path, workflow_root: Path) -> dict[str, Any]:
    source_path = Path(route["source_path"])
    if not source_path.exists():
        raise FileNotFoundError(f"Source artifact not found: {source_path}")
    artifact = json.loads(source_path.read_text(encoding="utf-8"))
    target_path = canon_root / route["target_relative_path"]
    note_text = render_note(route, artifact, source_path, target_path)
    validation = validate_note(note_text, source_path)

    export_root = workflow_root / "EXPORTS" / "reports"
    staging_dir = export_root / "01_STAGING_NOTES"
    routed_dir = export_root / "03_ROUTED_NOTES"
    staging_dir.mkdir(parents=True, exist_ok=True)
    routed_dir.mkdir(parents=True, exist_ok=True)

    staged_note_path = staging_dir / route["note_filename"]
    routed_note_path = routed_dir / route["note_filename"]
    staged_note_path.write_text(note_text, encoding="utf-8")
    routed_note_path.write_text(note_text, encoding="utf-8")

    copy_status = "root_export_only_not_copied_to_target"
    return {
        "route_id": route["route_id"],
        "source_kind": route["source_kind"],
        "source_path": str(source_path),
        "staged_note_path": str(staged_note_path),
        "routed_note_path": str(routed_note_path),
        "target_path": str(target_path),
        "copy_status": copy_status,
        "wikilink_warnings": validation["wikilink_warnings"],
        "frontmatter_title": validation["frontmatter"]["title"],
    }


def main() -> int:
    args = parse_args()
    manifest = load_manifest(args.manifest)
    workflow_root = args.manifest.parent
    canon_root = Path(manifest["canon_root"])
    selected_ids = set(args.route_id or [])
    routes = manifest["routes"]
    if selected_ids:
        routes = [route for route in routes if route["route_id"] in selected_ids]
    results: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    for route in routes:
        try:
            results.append(process_route(route, canon_root, workflow_root))
        except Exception as exc:
            errors.append({"route_id": route.get("route_id"), "error": str(exc)})
    report = {
        "manifest": str(args.manifest),
        "processed_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "requested_route_ids": sorted(selected_ids),
        "results": results,
        "errors": errors,
    }
    report_name = f"obsidian_export_report_{datetime.now():%Y%m%d_%H%M%S}.json"
    report_path = workflow_root / "EXPORTS" / "reports" / "02_VALIDATION_REPORTS" / report_name
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"report_path": str(report_path), "results": results, "errors": errors}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
