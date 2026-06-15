#!/usr/bin/env python3
"""Scan HTML/Markdown documents for math anchors.

This is the placement layer, not the translator. It finds math-like blocks,
classifies them, assigns stable IDs, captures context, and optionally writes an
annotated copy that later translation/weaving passes can target.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from bs4 import BeautifulSoup, Comment, Tag


SUPPORTED_EXTENSIONS = {".html", ".htm", ".md", ".markdown"}
MATH_SYMBOL_RE = re.compile(
    r"(\\[a-zA-Z]+|[=≈~∫∑∂√∞≤≥±×÷→←↔χκλφψρσθπΩΔΓ]|\\frac|\\sum|\\int|\\partial|\^|_)",
    re.IGNORECASE,
)
DISPLAY_PATTERNS = [
    re.compile(r"\$\$(.+?)\$\$", re.DOTALL),
    re.compile(r"\\\[(.+?)\\\]", re.DOTALL),
]
INLINE_PATTERNS = [
    re.compile(r"\\\((.+?)\\\)", re.DOTALL),
]
MATH_SELECTORS = [
    ".equation-main",
    ".equation-showpiece",
    ".equation-block",
    ".equation",
    ".math-display",
    ".math",
    ".MathJax",
    ".MathJax_Display",
    "[data-tex]",
    "script[type='math/tex']",
    "script[type='math/tex; mode=display']",
    "math",
    "mjx-container",
]


UNICODE_LATEX_MAP = {
    "χ": r"\chi",
    "κ": r"\kappa",
    "λ": r"\lambda",
    "φ": r"\phi",
    "ψ": r"\psi",
    "ρ": r"\rho",
    "σ": r"\sigma",
    "θ": r"\theta",
    "π": r"\pi",
    "Ω": r"\Omega",
    "Δ": r"\Delta",
    "Γ": r"\Gamma",
    "∫": r"\int",
    "∑": r"\sum",
    "∂": r"\partial",
    "√": r"\sqrt",
    "∞": r"\infty",
    "≈": r"\approx",
    "→": r"\to",
    "←": r"\leftarrow",
    "↔": r"\leftrightarrow",
    "≤": r"\le",
    "≥": r"\ge",
    "±": r"\pm",
    "×": r"\times",
    "÷": r"\div",
}


@dataclass
class MathAnchor:
    id: str
    sourceFile: str
    documentId: str
    position: int
    raw: str
    normalized: str
    block_type: str
    detection_method: str
    needs_translation: bool
    confidence: float
    location: dict
    surrounding_context: dict
    content_hash: str


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return slug or "document"


def clean_text(value: str) -> str:
    text = html.unescape(value or "")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalize_math(value: str) -> str:
    text = clean_text(value)
    text = re.sub(r"^\$+", "", text)
    text = re.sub(r"\$+$", "", text)
    text = re.sub(r"^\\\[", "", text)
    text = re.sub(r"\\\]$", "", text)
    text = re.sub(r"^\\\(", "", text)
    text = re.sub(r"\\\)$", "", text)
    for unicode_char, latex in UNICODE_LATEX_MAP.items():
        text = text.replace(unicode_char, latex)
    while "\\\\" in text:
        text = text.replace("\\\\", "\\")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def canonical_for_hash(value: str) -> str:
    return re.sub(r"\s+", "", normalize_math(value)).lower()


def content_hash(value: str) -> str:
    return hashlib.sha256(canonical_for_hash(value).encode("utf-8")).hexdigest()[:16]


def text_has_math(value: str) -> bool:
    text = clean_text(value)
    if len(text) < 3:
        return False
    return bool(MATH_SYMBOL_RE.search(text))


def classify_math(raw: str, element: Tag | None = None, method: str = "") -> tuple[str, bool, float]:
    text = normalize_math(raw)
    compact = re.sub(r"\s+", "", text)
    class_values = " ".join(element.get("class", [])) if element else ""
    class_values = class_values.lower()
    if "showpiece" in class_values or "equation-main" in class_values:
        return "equation_showpiece", True, 0.98
    if "equation" in class_values or method == "display_delimiter":
        return "display_equation", True, 0.92
    if re.search(r"\\int|\\sum|\\partial|\\frac", text):
        return "derivation_step" if len(compact) < 80 else "equation_showpiece", True, 0.88
    if re.search(r"(?:^|[^a-zA-Z])(?:m|H|G|c|k|r|t|T|S|V|C|R|A)_?\\?[a-zA-Z]*\s*(?:~|=|≈)", text):
        return "parameter_value", True, 0.82
    if "=" in text or "\\approx" in text or "~" in text:
        return "display_equation" if len(compact) >= 20 else "parameter_value", True, 0.78
    if method == "inline_delimiter":
        return "inline_math", False, 0.60
    return "math_candidate", True, 0.55


def nearest_heading(element: Tag | None) -> dict:
    if element is None:
        return {"level": "", "text": ""}
    heading = element.find_previous(["h1", "h2", "h3", "h4", "h5", "h6"])
    if not heading:
        return {"level": "", "text": ""}
    return {"level": heading.name, "text": clean_text(heading.get_text(" ", strip=True))}


def nearest_paragraph(element: Tag | None) -> str:
    if element is None:
        return ""
    candidates = list(element.find_all_previous("p", limit=1)) + list(element.find_all_next("p", limit=1))
    for paragraph in candidates:
        text = clean_text(paragraph.get_text(" ", strip=True))
        if text:
            return text[:320]
    return ""


def css_location(element: Tag | None) -> dict:
    if element is None:
        return {"tag": "", "classes": [], "id": ""}
    return {
        "tag": element.name or "",
        "classes": list(element.get("class", [])),
        "id": element.get("id") or "",
    }


def make_anchor(
    *,
    document_id: str,
    source_file: str,
    raw: str,
    position: int,
    method: str,
    element: Tag | None = None,
) -> MathAnchor:
    normalized = normalize_math(raw)
    block_type, needs_translation, confidence = classify_math(raw, element, method)
    anchor_id = f"{document_id}-eq-{position:03d}"
    return MathAnchor(
        id=anchor_id,
        sourceFile=source_file,
        documentId=document_id,
        position=position,
        raw=clean_text(raw),
        normalized=normalized,
        block_type=block_type,
        detection_method=method,
        needs_translation=needs_translation,
        confidence=confidence,
        location={**css_location(element), "heading": nearest_heading(element)},
        surrounding_context={
            "nearest_heading": nearest_heading(element),
            "nearest_paragraph": nearest_paragraph(element),
        },
        content_hash=content_hash(raw),
    )


def should_keep(anchor: MathAnchor) -> bool:
    if not text_has_math(anchor.normalized):
        return False
    if anchor.block_type == "inline_math" and len(anchor.normalized) < 14:
        return False
    return True


def scan_html(path: Path, annotate: bool = False) -> tuple[list[MathAnchor], str | None]:
    raw_html = path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(raw_html, "lxml")
    document_id = slugify(path.stem)
    anchors: list[MathAnchor] = []
    seen: set[str] = set()
    position = 1

    for element in soup.select(",".join(MATH_SELECTORS)):
        tex = element.get("data-tex") or element.string or element.get_text(" ", strip=True)
        normalized = normalize_math(tex)
        if not normalized:
            continue
        key = content_hash(normalized)
        if key in seen:
            continue
        anchor = make_anchor(
            document_id=document_id,
            source_file=str(path),
            raw=tex,
            position=position,
            method="html_container",
            element=element,
        )
        if should_keep(anchor):
            seen.add(key)
            anchors.append(anchor)
            if annotate:
                element["data-math-id"] = anchor.id
                element["data-math-kind"] = anchor.block_type
                element.insert_before(Comment(f'MATH_ANCHOR_START id="{anchor.id}" kind="{anchor.block_type}"'))
                element.insert_after(Comment(f'MATH_ANCHOR_END id="{anchor.id}"'))
            position += 1

    for pattern in DISPLAY_PATTERNS:
        for match in pattern.finditer(raw_html):
            raw = match.group(1)
            key = content_hash(raw)
            if key in seen:
                continue
            anchor = make_anchor(
                document_id=document_id,
                source_file=str(path),
                raw=raw,
                position=position,
                method="display_delimiter",
            )
            if should_keep(anchor):
                seen.add(key)
                anchors.append(anchor)
                position += 1

    for pattern in INLINE_PATTERNS:
        for match in pattern.finditer(raw_html):
            raw = match.group(1)
            key = content_hash(raw)
            if key in seen:
                continue
            anchor = make_anchor(
                document_id=document_id,
                source_file=str(path),
                raw=raw,
                position=position,
                method="inline_delimiter",
            )
            if should_keep(anchor):
                seen.add(key)
                anchors.append(anchor)
                position += 1

    return anchors, str(soup) if annotate else None


def scan_markdown(path: Path) -> list[MathAnchor]:
    text = path.read_text(encoding="utf-8", errors="replace")
    document_id = slugify(path.stem)
    anchors: list[MathAnchor] = []
    seen: set[str] = set()
    position = 1
    for pattern, method in [(p, "display_delimiter") for p in DISPLAY_PATTERNS] + [(p, "inline_delimiter") for p in INLINE_PATTERNS]:
        for match in pattern.finditer(text):
            raw = match.group(1)
            key = content_hash(raw)
            if key in seen:
                continue
            anchor = make_anchor(
                document_id=document_id,
                source_file=str(path),
                raw=raw,
                position=position,
                method=method,
            )
            if should_keep(anchor):
                seen.add(key)
                anchors.append(anchor)
                position += 1
    return anchors


def collect_inputs(input_path: Path | None, scan_path: Path | None, recursive: bool) -> list[Path]:
    paths: list[Path] = []
    if input_path:
        paths.append(input_path.resolve())
    if scan_path:
        folder = scan_path.resolve()
        iterator = folder.rglob("*") if recursive else folder.glob("*")
        paths.extend(sorted(path for path in iterator if path.suffix.lower() in SUPPORTED_EXTENSIONS))
    return [path for path in paths if path.exists() and path.is_file()]


def write_outputs(path: Path, output_dir: Path, annotate: bool) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    article_out = output_dir / slugify(path.stem)
    article_out.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() in {".html", ".htm"}:
        anchors, annotated_html = scan_html(path, annotate=annotate)
        if annotate and annotated_html is not None:
            (article_out / f"{path.stem}.math-anchored.html").write_text(annotated_html, encoding="utf-8")
    else:
        anchors = scan_markdown(path)
    anchor_dicts = [asdict(anchor) for anchor in anchors]
    anchors_path = article_out / f"{path.stem}.math-anchors.json"
    anchors_path.write_text(json.dumps(anchor_dicts, ensure_ascii=False, indent=2), encoding="utf-8")
    return {
        "sourceFile": str(path),
        "documentId": slugify(path.stem),
        "anchorCount": len(anchors),
        "needsTranslationCount": sum(1 for anchor in anchors if anchor.needs_translation),
        "outputs": [str(anchors_path)],
    }


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Detect and anchor math blocks before translation.")
    parser.add_argument("--input", type=Path)
    parser.add_argument("--scan", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--annotate", action="store_true", help="Write annotated HTML copies with data-math-id markers.")
    parser.add_argument("--recursive", action="store_true", help="Scan subfolders too. Default scans only the folder root.")
    args = parser.parse_args(list(argv) if argv is not None else None)

    inputs = collect_inputs(args.input, args.scan, recursive=args.recursive)
    if not inputs:
        raise SystemExit("No input files found.")

    results = [write_outputs(path, args.output_dir.resolve(), args.annotate) for path in inputs]
    manifest = {
        "generated_at": utc_now(),
        "mode": "math_anchor_scan",
        "input_count": len(inputs),
        "anchor_count": sum(result["anchorCount"] for result in results),
        "needs_translation_count": sum(result["needsTranslationCount"] for result in results),
        "documents": results,
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "MATH_ANCHOR_SCAN_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
