"""
ST-CONV-001 — Document Converter.

Read routing.yml (from ST-ROUTE-001), dispatch to the right converter
(MarkItDown / Docling / Marker / pass-through), produce clean source.md
+ conversion_report.yml.

Dispatch table:
    pdf       -> Marker (if installed) else Docling -> MarkItDown -> stub
    docx/html/rtf/epub/text -> MarkItDown
    markdown  -> pass-through (copy)
    transcript-> pass-through (clean whitespace)

Usage:
    python run.py --in <routing.yml> --out <source.md>
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

STATION_ID = "ST-CONV-001"


def parse_routing_yml(text: str) -> dict:
    """Same flat scalar parser as ROUTE-001 writes."""
    out = {}
    for line in text.splitlines():
        m = re.match(r'^(\w+):\s*"(.*)"\s*$', line)
        if m:
            out[m.group(1)] = m.group(2)
            continue
        m = re.match(r"^(\w+):\s*([^\s].*?)\s*$", line)
        if m:
            v = m.group(2).strip('"')
            if v == "~":
                v = None
            out[m.group(1)] = v
    return out


def convert_via_markitdown(src: Path) -> str | None:
    try:
        from markitdown import MarkItDown  # type: ignore
    except ImportError:
        return None
    md = MarkItDown()
    return md.convert(str(src)).text_content


def convert_via_marker(src: Path) -> str | None:
    """Marker for PDFs — heavy dep, best for academic papers."""
    try:
        from marker.convert import convert_single_pdf  # type: ignore
        from marker.models import load_all_models  # type: ignore
    except ImportError:
        return None
    models = load_all_models()
    text, _, _ = convert_single_pdf(str(src), models)
    return text


def convert_via_docling(src: Path) -> str | None:
    try:
        from docling.document_converter import DocumentConverter  # type: ignore
    except ImportError:
        return None
    conv = DocumentConverter()
    result = conv.convert(str(src))
    return result.document.export_to_markdown()


def passthrough_markdown(src: Path) -> str:
    return src.read_text(encoding="utf-8", errors="ignore")


def clean_transcript(src: Path) -> str:
    text = src.read_text(encoding="utf-8", errors="ignore")
    # Collapse runs of whitespace to single space, preserve paragraph breaks
    paragraphs = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", text)]
    return "\n\n".join(p for p in paragraphs if p)


def dispatch(file_type: str, src: Path) -> tuple[str, str]:
    """Returns (markdown_text, converter_used)."""
    if file_type == "markdown":
        return passthrough_markdown(src), "passthrough"
    if file_type == "transcript":
        return clean_transcript(src), "clean_transcript"
    if file_type == "pdf":
        for fn, name in [(convert_via_marker, "marker"),
                         (convert_via_docling, "docling"),
                         (convert_via_markitdown, "markitdown")]:
            out = fn(src)
            if out is not None:
                return out, name
    if file_type in {"docx", "doc", "html", "htm", "rtf", "epub", "text"}:
        out = convert_via_markitdown(src)
        if out is not None:
            return out, "markitdown"
        out = convert_via_docling(src)
        if out is not None:
            return out, "docling"
    return f"# {src.name}\n\n[Conversion stub — no converter available for type `{file_type}`. Install markitdown/docling/marker.]\n", "stub"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="inp", required=True)
    parser.add_argument("--out", dest="out", required=True)
    args = parser.parse_args()

    routing = parse_routing_yml(Path(args.inp).read_text(encoding="utf-8"))
    src_path = Path(routing.get("normalized_path") or routing.get("input_path", ""))
    file_type = routing.get("file_type", "unknown")

    if not src_path.exists():
        print(json.dumps({"status": "error", "reason": f"source not found: {src_path}"}),
              file=sys.stderr)
        return 3

    markdown, converter_used = dispatch(file_type, src_path)
    out_path = Path(args.out)
    if out_path.suffix.lower() not in {".md", ".markdown"}:
        out_path = out_path.with_suffix(".md")
    out_path.write_text(markdown, encoding="utf-8")

    report = {
        "station":        STATION_ID,
        "source":         str(src_path),
        "file_type":      file_type,
        "converter_used": converter_used,
        "output_path":    str(out_path),
        "output_chars":   len(markdown),
        "converted_at":   datetime.now().isoformat(timespec="seconds"),
        "next_station":   "ST-CLAIM-001",
    }
    report_path = out_path.with_name("conversion_report.yml")
    report_path.write_text(
        "\n".join(f'{k}: "{v}"' if not isinstance(v, int) else f"{k}: {v}"
                  for k, v in report.items()) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": "ok", "converter": converter_used, "chars": len(markdown)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
