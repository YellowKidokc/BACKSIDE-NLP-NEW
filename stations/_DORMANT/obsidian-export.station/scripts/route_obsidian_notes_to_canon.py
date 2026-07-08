from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


DEFAULT_STAGING_DIR = Path(r"X:\Backside\stations\obsidian-export.station\02_OBSIDIAN_NOTES")
DEFAULT_MANIFEST_PATH = Path(r"X:\Backside\stations\obsidian-export.station\04_REPORTS\canon_routing_manifest.json")
DEFAULT_CANON_ROOT = Path(r"\\dlowenas\z obsidian\_ __THEOPHYSICS_CANON")
DEFAULT_BACKUP_ROOT = DEFAULT_CANON_ROOT / "08_ARCHIVE" / "_router_backups"

REQUIRED_FIELDS = {"id", "type", "source_path", "content_hash", "tags"}
SERIES_CODES = {"GTQ", "MDA", "TRINITY", "JS_SERIES", "APOLOGETICS", "LOGOS_PAPERS"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate staged Obsidian notes and route them into THEOPHYSICS_CANON.")
    parser.add_argument("--note", type=Path, help="Single staged note to route.")
    parser.add_argument("--staging-dir", type=Path, default=DEFAULT_STAGING_DIR)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST_PATH)
    parser.add_argument("--canon-root", type=Path, default=DEFAULT_CANON_ROOT)
    parser.add_argument("--backup-root", type=Path, default=DEFAULT_BACKUP_ROOT)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    lines = text.splitlines()
    end_index = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() in {"---", "..."}:
            end_index = idx
            break
    if end_index is None:
        return {}, text
    frontmatter_raw = "\n".join(lines[1:end_index])
    body = "\n".join(lines[end_index + 1 :]).strip()
    try:
        frontmatter = yaml.safe_load(frontmatter_raw) or {}
    except Exception:
        return {}, text
    return frontmatter if isinstance(frontmatter, dict) else {}, body


def is_raw_json_body(body: str) -> bool:
    stripped = body.strip()
    if not stripped or stripped[0] not in "[{":
        return False
    try:
        json.loads(stripped)
    except Exception:
        return False
    return True


def wikilinks_valid(body: str) -> bool:
    opens = body.count("[[")
    closes = body.count("]]")
    if opens != closes:
        return False
    for match in re.finditer(r"\[\[([^\]]+)\]\]", body):
        inner = match.group(1).strip()
        if not inner or "[[" in inner or "]]" in inner:
            return False
    return True


def detect_series_code(frontmatter: dict[str, Any], path: Path) -> str | None:
    for candidate in (
        frontmatter.get("series_code"),
        frontmatter.get("series"),
        frontmatter.get("series_id"),
    ):
        if not candidate:
            continue
        candidate_text = str(candidate).strip().upper()
        if candidate_text in SERIES_CODES:
            return candidate_text
    stem_upper = path.stem.upper()
    for code in SERIES_CODES:
        if stem_upper.startswith(code.replace("_", "-")) or stem_upper.startswith(code):
            return code
    tags = [str(tag).upper() for tag in frontmatter.get("tags", [])]
    for code in SERIES_CODES:
        if code in tags or code.replace("_", "-") in tags:
            return code
    return None


def route_destination(frontmatter: dict[str, Any], path: Path, canon_root: Path) -> tuple[Path, str]:
    note_type = str(frontmatter.get("type", "")).strip().lower()
    tags = {str(tag).strip().lower() for tag in frontmatter.get("tags", [])}
    source_name = str(frontmatter.get("source_path", "")).lower()

    if note_type in {"series_article", "article", "series_note"} or {"series-article", "gtq", "article"} & tags:
        series_code = detect_series_code(frontmatter, path)
        if series_code:
            return canon_root / "03_SERIES" / series_code / path.name, f"series/article note -> 03_SERIES/{series_code}"
        return canon_root / "10_HOLDING_BAY" / path.name, "series/article note but series code uncertain -> 10_HOLDING_BAY"
    if note_type in {"canonical_theory", "canon"} or "canonical" in tags:
        return canon_root / "01_CANON" / path.name, "canonical theory note -> 01_CANON"
    if note_type in {"framework", "theory"} or {"framework", "theory"} & tags:
        return canon_root / "04_FRAMEWORKS" / path.name, "framework note -> 04_FRAMEWORKS"
    if note_type in {"physics_law", "math_note", "law", "physics"} or {"physics", "math", "law"} & tags:
        return canon_root / "02_PHYSICS_CORE" / path.name, "physics/law/math note -> 02_PHYSICS_CORE"
    if note_type in {"philosophy_of_science", "epistemology"} or {"philosophy-of-science", "epistemology"} & tags:
        return canon_root / "03_PHILOSOPHY_OF_SCIENCE" / path.name, "philosophy of science note -> 03_PHILOSOPHY_OF_SCIENCE"
    if note_type in {"evidence", "experiment"} or {"evidence", "experiment"} & tags:
        return canon_root / "05_EVIDENCE" / path.name, "evidence note -> 05_EVIDENCE"
    if note_type in {"objection", "counterargument", "adversarial"} or {"objection", "counterargument", "adversarial"} & tags:
        return canon_root / "06_ADVERSARIAL_LAYER" / path.name, "objection/counterargument note -> 06_ADVERSARIAL_LAYER"
    if note_type in {"publication", "publish_ready"} or {"publication", "publish-ready"} & tags:
        return canon_root / "07_PUBLICATION_TRACK" / path.name, "publication-ready note -> 07_PUBLICATION_TRACK"
    if note_type in {"media", "transcript_qa"} or {"media", "video", "transcript", "q-and-a"} & tags or "transcript" in source_name:
        return canon_root / "09_MEDIA" / path.name, "media/transcript note -> 09_MEDIA"
    if note_type in {"template", "prompt_template"} or {"template"} & tags:
        return canon_root / "09_TEMPLATE_ENGINE" / path.name, "template note -> 09_TEMPLATE_ENGINE"
    return canon_root / "10_HOLDING_BAY" / path.name, "uncertain note -> 10_HOLDING_BAY"


def backup_existing(target_path: Path, backup_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = backup_root / target_path.parent.name
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_path = backup_dir / f"{target_path.stem}.{timestamp}.bak{target_path.suffix}"
    shutil.copy2(target_path, backup_path)
    return backup_path


def validate_note(note_path: Path, frontmatter: dict[str, Any], body: str, destination: Path) -> tuple[str, list[str]]:
    warnings: list[str] = []
    missing = sorted(field for field in REQUIRED_FIELDS if field not in frontmatter or frontmatter.get(field) in (None, "", []))
    if missing:
        warnings.append(f"Missing required frontmatter fields: {', '.join(missing)}")
    if not frontmatter:
        warnings.append("YAML frontmatter missing or not parseable.")
    if is_raw_json_body(body):
        warnings.append("Body is a raw JSON dump.")
    if not wikilinks_valid(body):
        warnings.append("Wikilinks are not valid Markdown.")
    source_path = Path(str(frontmatter.get("source_path", ""))) if frontmatter.get("source_path") else None
    if not source_path or not source_path.exists():
        warnings.append("Source artifact path does not exist.")
    expected_name = f"{slugify(str(frontmatter.get('id', '')))}.md" if frontmatter.get("id") else None
    if expected_name and note_path.name != expected_name:
        warnings.append(f"Filename is not deterministic. Expected {expected_name}.")
    if not destination.parent.exists():
        warnings.append("Destination folder does not exist.")
    return ("pass" if not warnings else "fail"), warnings


def route_note(note_path: Path, canon_root: Path, backup_root: Path, dry_run: bool) -> dict[str, Any]:
    raw_text = note_path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(raw_text)
    destination, route_reason = route_destination(frontmatter, note_path, canon_root)
    validation_status, warnings = validate_note(note_path, frontmatter, body, destination)
    record: dict[str, Any] = {
        "source_note": str(note_path),
        "destination_note": str(destination),
        "route_reason": route_reason,
        "validation_status": validation_status,
        "backup_path": None,
        "warnings": warnings,
        "copied": False,
        "overwritten": False,
    }
    if validation_status != "pass" or dry_run:
        return record

    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        existing_text = destination.read_text(encoding="utf-8")
        if sha256_text(existing_text) == sha256_text(raw_text):
            record["copied"] = True
            record["warnings"].append("Destination already matched staged note; no content change.")
            return record
        backup_path = backup_existing(destination, backup_root)
        record["backup_path"] = str(backup_path)
        record["overwritten"] = True

    shutil.copy2(note_path, destination)
    record["copied"] = True
    return record


def collect_notes(single_note: Path | None, staging_dir: Path) -> list[Path]:
    if single_note:
        return [single_note]
    return sorted(staging_dir.glob("*.md"))


def main() -> int:
    args = parse_args()
    notes = collect_notes(args.note, args.staging_dir)
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    records = [route_note(note, args.canon_root, args.backup_root, args.dry_run) for note in notes]
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "canon_root": str(args.canon_root),
        "staging_dir": str(args.staging_dir),
        "note_count": len(records),
        "dry_run": args.dry_run,
        "routes": records,
    }
    args.manifest_out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
