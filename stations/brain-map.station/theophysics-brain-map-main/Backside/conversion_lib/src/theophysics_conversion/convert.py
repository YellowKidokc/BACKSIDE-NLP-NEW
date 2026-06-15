from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

import yaml

from .converters.html_adapter import convert_html
from .converters.markitdown_adapter import convert_with_markitdown
from .converters.youtube_adapter import convert_youtube
from .detect import Format, detect_format
from .models import ConversionConfig, ConvertResult


TEXT_FORMATS = {Format.MARKDOWN, Format.TEXT}
MARKITDOWN_FORMATS = {Format.PDF, Format.DOCX, Format.PPTX, Format.XLSX, Format.IPYNB, Format.WEB_URL, Format.IMAGE}


def slugify(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return value[:80] or "source"


def load_config(path: Path | None) -> ConversionConfig:
    if path is None:
        return ConversionConfig()
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    flattened = {
        "markitdown_enabled": data.get("markitdown", {}).get("enabled", True),
        "youtube_prefer_transcript": data.get("youtube", {}).get("prefer_transcript", True),
        "metadata": {"deployment_name": data.get("deployment_name", "custom")},
    }
    if "export_root" in data:
        flattened["export_root"] = Path(data["export_root"])
    if "state_root" in data:
        flattened["state_root"] = Path(data["state_root"])
    return ConversionConfig(**flattened)


def read_text_source(path: Path) -> ConvertResult:
    raw = path.read_text(encoding="utf-8-sig", errors="replace")
    source = raw.strip()
    fmt = detect_format(source)
    if fmt is Format.YOUTUBE_URL:
        return convert_youtube(source)
    if fmt is Format.WEB_URL:
        return convert_with_markitdown(source)
    normalized = raw.replace("\r\n", "\n").replace("\r", "\n")
    normalized = re.sub(r"\n{3,}", "\n\n", normalized).strip() + "\n"
    return ConvertResult(
        markdown=normalized,
        metadata={"source_format": "TEXT", "markdown_words": len(re.findall(r"\b\w+\b", raw))},
    )


def convert(source: str | Path, *, config: ConversionConfig | None = None) -> ConvertResult:
    config = config or ConversionConfig()
    fmt = detect_format(source)
    path = Path(source)

    if fmt is Format.HTML:
        result = convert_html(path)
    elif fmt in TEXT_FORMATS:
        result = read_text_source(path)
    elif fmt is Format.YOUTUBE_URL:
        result = convert_youtube(str(source))
    elif fmt in MARKITDOWN_FORMATS and config.markitdown_enabled:
        result = convert_with_markitdown(source)
    elif fmt in {Format.AUDIO, Format.VIDEO}:
        result = ConvertResult(
            markdown="",
            metadata={"source_format": fmt.value},
            warnings=["Audio/video conversion requires the Whisper adapter; not enabled in this first pass."],
        )
    else:
        detail = ""
        if path.exists() and path.is_file():
            detail = f" first16={path.read_bytes()[:16]!r}"
        result = ConvertResult(markdown="", warnings=[f"Unsupported or unknown format: {fmt.value}.{detail}"])

    result.metadata.update({"detected_format": fmt.value, "source": str(source)})
    return result


def write_export(source: str | Path, result: ConvertResult, config: ConversionConfig) -> Path:
    source_name = Path(str(source)).stem if Path(str(source)).suffix else slugify(str(source))
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    digest = hashlib.sha256(str(source).encode("utf-8", errors="replace")).hexdigest()[:10]
    run_id = f"{stamp}_{slugify(source_name)}_{digest}"
    export_dir = config.export_root / run_id
    state_dir = config.state_root / run_id
    export_dir.mkdir(parents=True, exist_ok=True)
    state_dir.mkdir(parents=True, exist_ok=True)

    md_path = export_dir / f"{slugify(source_name)}.canonical.md"
    md_path.write_text(result.markdown, encoding="utf-8")
    (state_dir / "conversion.json").write_text(result.model_dump_json(indent=2), encoding="utf-8")
    (export_dir / "README.md").write_text(
        "\n".join(
            [
                "# Conversion Export",
                "",
                f"- Source: `{source}`",
                f"- Markdown: `{md_path}`",
                f"- Detected format: `{result.metadata.get('detected_format', 'UNKNOWN')}`",
                f"- Warnings: {len(result.warnings)}",
                "",
                "Internal state is stored separately under the configured state root.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return export_dir


def cli() -> int:
    parser = argparse.ArgumentParser(description="Convert source files or URLs to canonical markdown.")
    parser.add_argument("source", nargs="?", help="Source path or URL.")
    parser.add_argument("--config", type=Path, help="Optional YAML config.")
    parser.add_argument("--out", type=Path, help="Write markdown to this path instead of an export folder.")
    parser.add_argument("--export-root", type=Path, help="Override export root.")
    parser.add_argument("--state-root", type=Path, help="Override state root.")
    parser.add_argument("--detect", action="store_true", help="Only print detected format.")
    parser.add_argument("--version", action="store_true", help="Print version.")
    args = parser.parse_args()

    if args.version:
        print("theophysics-conversion 0.1.0")
        return 0
    if not args.source:
        parser.error("source is required unless --version is used")

    if args.detect:
        print(detect_format(args.source).value)
        return 0

    config = load_config(args.config)
    if args.export_root:
        config.export_root = args.export_root
    if args.state_root:
        config.state_root = args.state_root

    result = convert(args.source, config=config)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(result.markdown, encoding="utf-8")
        print(f"Wrote markdown: {args.out}")
        if result.warnings:
            print(json.dumps({"warnings": result.warnings}, indent=2))
        return 0 if result.markdown else 2

    export_dir = write_export(args.source, result, config)
    print(f"Export written: {export_dir}")
    if result.warnings:
        print(json.dumps({"warnings": result.warnings}, indent=2))
    return 0 if result.markdown else 2


def main() -> int:
    return cli()


if __name__ == "__main__":
    raise SystemExit(main())
