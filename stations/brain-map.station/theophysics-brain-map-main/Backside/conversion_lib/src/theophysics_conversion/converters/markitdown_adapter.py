from __future__ import annotations

from pathlib import Path

from ..models import ConvertResult


def convert_with_markitdown(source: str | Path) -> ConvertResult:
    try:
        from markitdown import MarkItDown
    except Exception as exc:  # pragma: no cover - environment-dependent
        return ConvertResult(
            markdown="",
            metadata={"source_format": "MARKITDOWN"},
            warnings=[f"MarkItDown is not available: {exc}"],
        )

    result = MarkItDown().convert(str(source))
    text = getattr(result, "text_content", "") or ""
    return ConvertResult(
        markdown=text.strip() + "\n" if text.strip() else "",
        metadata={"source_format": "MARKITDOWN"},
        warnings=[] if text.strip() else ["MarkItDown returned empty text."],
    )

