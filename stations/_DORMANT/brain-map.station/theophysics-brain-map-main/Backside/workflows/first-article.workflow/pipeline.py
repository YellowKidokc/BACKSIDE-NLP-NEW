from __future__ import annotations

import argparse
import hashlib
import json
import csv
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import unquote

from bs4 import BeautifulSoup
from PIL import Image

def resolve_repo_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "Backside" / "lossless_context_pipeline").exists():
            return parent
    fallback = Path(r"D:\GitHub\theophysics-brain-map")
    if fallback.exists():
        return fallback
    return current.parents[3]


REPO_ROOT = resolve_repo_root()
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from Backside.lossless_context_pipeline.pipeline import build_artifact
from Backside.lossless_context_pipeline.storage import write_outputs
from Backside.station_lab.paper_grader_station_lab import run as run_station_lab


DEFAULT_EXPORT_ROOT = Path(r"X:\EXPORTS\first-article-workflow")
DEFAULT_STATE_ROOT = Path(r"X:\Backside\_state\first-article-workflow")
DEFAULT_DROP = Path(r"X:\Backside\workflows\first-article.workflow\00_DROP")
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff"}
TEXT_EXTS = {".md", ".markdown", ".txt"}
HTML_EXTS = {".html", ".htm"}


def slugify(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return value[:80] or "source"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def timestamped_run_id(source: Path) -> str:
    digest = hashlib.sha256((str(source.resolve()) + str(source.stat().st_mtime_ns)).encode("utf-8")).hexdigest()[:10]
    return f"{datetime.now().strftime('%Y%m%d-%H%M%S')}_{slugify(source.stem)}_{digest}"


def ensure_dirs(*paths: Path) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")
    return path


def convert_to_markdown(source: Path, working_dir: Path, state_dir: Path) -> tuple[Path, dict[str, Any]]:
    """Normalize supported sources to canonical Markdown for downstream stations."""
    suffix = source.suffix.lower()
    out_path = working_dir / "source.canonical.md"

    if suffix in TEXT_EXTS:
        text = read_text(source)
        write_text(out_path, text)
        return out_path, {"method": "direct-text", "source_format": suffix.lstrip(".").upper()}

    if suffix in HTML_EXTS:
        from Backside.conversion_lib.src.theophysics_conversion.convert import convert

        result = convert(source)
        markdown = add_frontmatter_if_missing(
            result.markdown,
            {
                "title": result.metadata.get("title") or source.stem,
                "domain": "THEOPHYSICS",
                "state": "W",
                "audience": "AI_RESEARCH",
                "use": "R",
                "risk": "R1",
            },
        )
        write_text(out_path, markdown)
        write_text(state_dir / "conversion.json", result.model_dump_json(indent=2))
        return out_path, {
            "method": "theophysics_conversion.html",
            "source_format": "HTML",
            "warnings": result.warnings,
            "metadata": result.metadata,
        }

    if suffix in IMAGE_EXTS:
        image_note = describe_standalone_image(source)
        write_text(out_path, image_note["markdown"])
        return out_path, {"method": "image-note-synthesis", "source_format": "IMAGE", "image": image_note["data"]}

    raise ValueError(f"Unsupported first-workflow source type: {source}")


def add_frontmatter_if_missing(markdown: str, fields: dict[str, str]) -> str:
    if markdown.lstrip().startswith("---"):
        return markdown
    lines = ["---"]
    for key, value in fields.items():
        safe = sanitize_yaml_scalar(value)
        lines.append(f'{key}: "{safe}"')
    lines.extend(["---", "", markdown.strip()])
    return "\n".join(lines) + "\n"


def sanitize_yaml_scalar(value: object) -> str:
    text = str(value).replace('"', "'")
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", "", text)
    return text.strip()


def describe_standalone_image(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = {
        "src": str(path),
        "filename": path.name,
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "visual_description_status": "metadata-only; no generative vision captioner is wired in this workflow yet",
    }
    try:
        with Image.open(path) as img:
            data.update({"width": img.width, "height": img.height, "mode": img.mode, "format": img.format})
    except Exception as exc:
        data["image_open_error"] = str(exc)

    quote = f"Image file `{path.name}` is a visual source artifact requiring an explicit vision-caption pass before public use."
    markdown = "\n".join(
        [
            "---",
            f'title: "{path.stem}"',
            'domain: "TECH"',
            'state: "W"',
            'audience: "AI_RESEARCH"',
            'use: "R"',
            'risk: "R1"',
            "---",
            "",
            f"# Image Intake - {path.stem}",
            "",
            "## Image Note",
            "",
            f"- File: `{path}`",
            f"- Size: {data.get('width', 'UNKNOWN')} x {data.get('height', 'UNKNOWN')}",
            f"- SHA-256: `{data['sha256']}`",
            "",
            "## Description",
            "",
            "Visual description is not finalized. This workflow records dimensions, identity, and any nearby caption/alt text. A true caption should be produced by a vision-capable AI partner or a local caption model.",
            "",
            "## Quote",
            "",
            f"> {quote}",
        ]
    )
    return {"data": data, "markdown": markdown}


def extract_image_notes(source: Path, markdown_path: Path, export_dir: Path, state_dir: Path) -> dict[str, Any]:
    notes: list[dict[str, Any]] = []
    suffix = source.suffix.lower()

    if suffix in HTML_EXTS:
        notes.extend(extract_html_images(source))
    elif suffix in TEXT_EXTS:
        notes.extend(extract_markdown_images(markdown_path, base_dir=source.parent))
    elif suffix in IMAGE_EXTS:
        notes.append(describe_standalone_image(source)["data"])

    for note in notes:
        enrich_image_note(note, source.parent)

    write_text(export_dir / "image-notes.md", render_image_notes(notes))
    write_text(state_dir / "image-notes.json", json.dumps(notes, indent=2))
    return {"station": "image-notes", "count": len(notes), "export": str(export_dir / "image-notes.md")}


def extract_html_images(path: Path) -> list[dict[str, Any]]:
    soup = BeautifulSoup(read_text(path), "lxml")
    notes: list[dict[str, Any]] = []
    for index, img in enumerate(soup.find_all("img"), start=1):
        src = img.get("src") or ""
        parent_text = ""
        fig = img.find_parent("figure")
        if fig:
            parent_text = " ".join(fig.get_text(" ", strip=True).split())
        if not parent_text and img.parent:
            parent_text = " ".join(img.parent.get_text(" ", strip=True).split())
        notes.append(
            {
                "ordinal": index,
                "src": src,
                "alt": img.get("alt") or "",
                "title": img.get("title") or "",
                "width_attr": img.get("width") or "",
                "height_attr": img.get("height") or "",
                "nearby_quote": parent_text[:500],
                "source": str(path),
            }
        )
    return notes


def extract_markdown_images(path: Path, base_dir: Path) -> list[dict[str, Any]]:
    text = read_text(path)
    notes: list[dict[str, Any]] = []
    lines = text.splitlines()
    pattern = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<src>[^)]+)\)")
    for line_no, line in enumerate(lines, start=1):
        for match in pattern.finditer(line):
            before = lines[line_no - 2].strip() if line_no > 1 else ""
            after = lines[line_no].strip() if line_no < len(lines) else ""
            quote = before if before else after
            notes.append(
                {
                    "ordinal": len(notes) + 1,
                    "src": match.group("src").strip(),
                    "alt": match.group("alt").strip(),
                    "title": "",
                    "nearby_quote": quote[:500],
                    "source": str(path),
                    "base_dir": str(base_dir),
                }
            )
    return notes


def enrich_image_note(note: dict[str, Any], base_dir: Path) -> None:
    src = unquote(str(note.get("src") or ""))
    candidate = Path(src)
    if not candidate.is_absolute():
        candidate = base_dir / src
    if not candidate.exists() and src:
        fallback = find_by_filename(base_dir, Path(src).name)
        if fallback:
            candidate = fallback
    note["resolved_path"] = str(candidate)
    note["exists"] = candidate.exists()
    if not candidate.exists() or not candidate.is_file():
        note["visual_description_status"] = "referenced image not found locally; using alt/title/nearby quote only"
        return
    note["sha256"] = sha256_file(candidate)
    note["bytes"] = candidate.stat().st_size
    try:
        with Image.open(candidate) as img:
            note.update({"width": img.width, "height": img.height, "mode": img.mode, "format": img.format})
            note["visual_description_status"] = "metadata extracted; caption still requires vision pass"
    except Exception as exc:
        note["image_open_error"] = str(exc)
        note["visual_description_status"] = "image could not be opened by PIL"


def find_by_filename(root: Path, filename: str) -> Path | None:
    if not filename:
        return None
    try:
        matches = list(root.rglob(filename))
    except Exception:
        return None
    files = [path for path in matches if path.is_file()]
    return files[0] if files else None


def render_image_notes(notes: list[dict[str, Any]]) -> str:
    lines = [
        "# Image Notes Station",
        "",
        "This station captures image references, local identity, dimensions when available, alt/title text, and nearby quote/caption context.",
        "",
        f"- Images detected: {len(notes)}",
        "",
    ]
    if not notes:
        lines.append("No image references detected.")
        return "\n".join(lines)

    for note in notes:
        title = note.get("alt") or note.get("title") or Path(str(note.get("src", "image"))).name or "image"
        quote = note.get("nearby_quote") or "No nearby quote/caption found."
        desc_bits = []
        if note.get("width") and note.get("height"):
            desc_bits.append(f"{note['width']}x{note['height']}")
        if note.get("format"):
            desc_bits.append(str(note["format"]))
        if note.get("mode"):
            desc_bits.append(str(note["mode"]))
        descriptor = ", ".join(desc_bits) if desc_bits else str(note.get("visual_description_status", "metadata pending"))
        lines.extend(
            [
                f"## Image {note.get('ordinal', '?')} - {title}",
                "",
                f"- Source: `{note.get('src', '')}`",
                f"- Resolved: `{note.get('resolved_path', '')}`",
                f"- Exists: {note.get('exists', False)}",
                f"- Metadata description: {descriptor}",
                f"- Alt/title: {title}",
                "",
                "### Quote / Caption Context",
                "",
                f"> {quote}",
                "",
                "### Public Caption Draft",
                "",
                f"{title}. {descriptor}.",
                "",
            ]
        )
    return "\n".join(lines)


def copy_source(source: Path, run_dir: Path) -> Path:
    target = run_dir / "SOURCE" / source.name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return target


def run_workflow(source: Path, export_root: Path, state_root: Path, vault_id: str, embeddings: str) -> Path:
    if not source.exists():
        raise FileNotFoundError(source)

    run_id = timestamped_run_id(source)
    export_dir = export_root / run_id
    state_dir = state_root / run_id
    working_dir = state_dir / "WORKING"
    ensure_dirs(export_dir, state_dir, working_dir)
    source_copy = copy_source(source, export_dir)

    markdown_path, conversion_meta = convert_to_markdown(source, working_dir, state_dir)
    shutil.copy2(markdown_path, export_dir / "source.canonical.md")

    station_export_root = export_dir / "stations"
    station_state_root = state_dir / "stations"
    summary_dir = run_station_lab(markdown_path, "all", station_export_root, station_state_root)
    image_result = extract_image_notes(source, markdown_path, export_dir, state_dir)

    artifact = build_artifact(markdown_path, vault_id=vault_id, note_version=run_id, embeddings=embeddings)
    lossless_dir = export_dir / "lossless"
    lossless_json, lossless_html = write_outputs(artifact, lossless_dir)
    semantic_tags_md = lossless_dir / f"{artifact.filename_safe_address}.semantic-tags.md"
    semantic_tags_json = lossless_dir / f"{artifact.filename_safe_address}.semantic-tags.json"

    manifest = {
        "workflow": "first-article.workflow",
        "run_id": run_id,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "source": str(source),
        "source_copy": str(source_copy),
        "canonical_markdown": str(export_dir / "source.canonical.md"),
        "export_dir": str(export_dir),
        "state_dir": str(state_dir),
        "stations": [
            {"station": "conversion", **conversion_meta},
            {"station": "station-lab-all", "export": str(summary_dir)},
            image_result,
            {
                "station": "lossless-context",
                "json": str(lossless_json),
                "html": str(lossless_html),
                "semantic_tags_md": str(semantic_tags_md),
                "semantic_tags_json": str(semantic_tags_json),
                "address": artifact.address,
                "master_equation_uuid": artifact.master_equation_uuid,
            },
        ],
        "master_equation_uuid": artifact.master_equation_uuid,
        "semantic_tag_count": len(artifact.semantic_tags),
        "address": artifact.address,
        "vector": artifact.vector_string,
        "semantic_vector": artifact.semantic_vector,
        "hash": artifact.hash,
    }
    write_text(export_dir / "manifest.json", json.dumps(manifest, indent=2))
    write_text(state_dir / "manifest.json", json.dumps(manifest, indent=2))
    write_readme(export_dir, manifest)
    return export_dir


def write_readme(export_dir: Path, manifest: dict[str, Any]) -> None:
    lines = [
        f"# First Article Workflow Export - {manifest['run_id']}",
        "",
        f"- Source: `{manifest['source']}`",
        f"- Address: `{manifest['address']}`",
        f"- Canonical Markdown: `{manifest['canonical_markdown']}`",
        f"- Manifest: `{export_dir / 'manifest.json'}`",
        "",
        "## Outputs",
        "",
        "- `source.canonical.md` - normalized source for stations",
        "- `stations/` - executive summary, overview, and math layer",
        "- `image-notes.md` - image references, caption/quote context, and metadata",
        "- `lossless/` - JSON and HTML reconstruction artifact",
        "",
        "## Boundary",
        "",
        "Image captions in this pass are metadata/alt/caption based. A true visual caption still needs a vision-capable AI partner or local caption model.",
    ]
    write_text(export_dir / "README.md", "\n".join(lines))


def process_drop_folder(drop: Path, export_root: Path, state_root: Path, vault_id: str, embeddings: str, limit: int | None) -> list[Path]:
    candidates = [p for p in sorted(drop.iterdir()) if p.is_file()]
    outputs: list[Path] = []
    for path in candidates[: limit or None]:
        outputs.append(run_workflow(path, export_root, state_root, vault_id, embeddings))
    return outputs


def process_input_root(
    input_root: Path,
    glob: str,
    export_root: Path,
    state_root: Path,
    vault_id: str,
    embeddings: str,
    limit: int | None,
) -> Path:
    batch_id = f"{datetime.now().strftime('%Y%m%d-%H%M%S')}_{slugify(input_root.name)}"
    batch_export = export_root / batch_id
    batch_state = state_root / batch_id
    batch_export.mkdir(parents=True, exist_ok=True)
    batch_state.mkdir(parents=True, exist_ok=True)
    files = [path for path in sorted(input_root.glob(glob)) if path.is_file()]
    if limit:
        files = files[:limit]

    rows: list[dict[str, Any]] = []
    for index, path in enumerate(files, start=1):
        print(f"[{index}/{len(files)}] {path.name}")
        try:
            out = run_workflow(path, batch_export, batch_state, vault_id, embeddings)
            manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
            image_station = next((row for row in manifest["stations"] if row.get("station") == "image-notes"), {})
            rows.append(
                {
                    "ordinal": index,
                    "name": path.name,
                    "source": str(path),
                    "status": "PASS",
                    "export_path": str(out),
                    "address": manifest.get("address", ""),
                    "vector": manifest.get("vector", ""),
                    "hash": manifest.get("hash", ""),
                    "images": image_station.get("count", ""),
                    "error": "",
                }
            )
        except Exception as exc:
            rows.append(
                {
                    "ordinal": index,
                    "name": path.name,
                    "source": str(path),
                    "status": "FAIL",
                    "export_path": "",
                    "address": "",
                    "vector": "",
                    "hash": "",
                    "images": "",
                    "error": repr(exc),
                }
            )

    write_batch_outputs(batch_export, batch_state, input_root, glob, rows)
    return batch_export


def write_batch_outputs(batch_export: Path, batch_state: Path, input_root: Path, glob: str, rows: list[dict[str, Any]]) -> None:
    json_path = batch_export / "batch-results.json"
    csv_path = batch_export / "batch-results.csv"
    summary_path = batch_export / "BATCH_SUMMARY.md"
    json_path.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()) if rows else ["status"])
        writer.writeheader()
        writer.writerows(rows)

    passed = sum(1 for row in rows if row["status"] == "PASS")
    failed = sum(1 for row in rows if row["status"] == "FAIL")
    lines = [
        "# First Article Workflow Batch",
        "",
        f"- Batch root: `{batch_export}`",
        f"- State root: `{batch_state}`",
        f"- Source root: `{input_root}`",
        f"- Glob: `{glob}`",
        f"- Files: {len(rows)}",
        f"- Passed: {passed}",
        f"- Failed: {failed}",
        f"- Created: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Results",
        "",
    ]
    for row in rows:
        lines.append(f"- [{row['status']}] {row['name']} -> `{row['export_path']}` :: {row['vector']}")
    summary_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    batch_state.mkdir(parents=True, exist_ok=True)
    (batch_state / "batch-results.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the first article workflow: conversion -> summary -> image notes -> lossless artifact.")
    parser.add_argument("--input", type=Path, help="Source Markdown, HTML, text, or image file.")
    parser.add_argument("--input-root", type=Path, help="Batch source folder. Uses --glob.")
    parser.add_argument("--glob", default="*.html", help="Batch glob used with --input-root.")
    parser.add_argument("--drop", type=Path, default=DEFAULT_DROP, help="Drop folder to process when --input is omitted.")
    parser.add_argument("--export-root", type=Path, default=DEFAULT_EXPORT_ROOT)
    parser.add_argument("--state-root", type=Path, default=DEFAULT_STATE_ROOT)
    parser.add_argument("--vault-id", default="theophysics-brain")
    parser.add_argument("--embeddings", choices=["none", "sbert"], default="none")
    parser.add_argument("--limit", type=int)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.input:
        out = run_workflow(args.input, args.export_root, args.state_root, args.vault_id, args.embeddings)
        print(f"Export written: {out}")
        return 0
    if args.input_root:
        out = process_input_root(args.input_root, args.glob, args.export_root, args.state_root, args.vault_id, args.embeddings, args.limit)
        print(f"Batch export written: {out}")
        return 0

    outputs = process_drop_folder(args.drop, args.export_root, args.state_root, args.vault_id, args.embeddings, args.limit)
    print(f"Processed {len(outputs)} files")
    for out in outputs:
        print(f"Export written: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
