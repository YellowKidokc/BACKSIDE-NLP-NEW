from __future__ import annotations

from enum import Enum
from pathlib import Path
from urllib.parse import urlparse


class Format(str, Enum):
    PDF = "PDF"
    DOCX = "DOCX"
    PPTX = "PPTX"
    XLSX = "XLSX"
    HTML = "HTML"
    IPYNB = "IPYNB"
    MARKDOWN = "MARKDOWN"
    TEXT = "TEXT"
    AUDIO = "AUDIO"
    VIDEO = "VIDEO"
    IMAGE = "IMAGE"
    YOUTUBE_URL = "YOUTUBE_URL"
    WEB_URL = "WEB_URL"
    UNKNOWN = "UNKNOWN"


EXTENSION_FORMATS = {
    ".pdf": Format.PDF,
    ".docx": Format.DOCX,
    ".pptx": Format.PPTX,
    ".xlsx": Format.XLSX,
    ".html": Format.HTML,
    ".htm": Format.HTML,
    ".ipynb": Format.IPYNB,
    ".md": Format.MARKDOWN,
    ".markdown": Format.MARKDOWN,
    ".txt": Format.TEXT,
    ".url": Format.TEXT,
    ".mp3": Format.AUDIO,
    ".wav": Format.AUDIO,
    ".m4a": Format.AUDIO,
    ".mp4": Format.VIDEO,
    ".mov": Format.VIDEO,
    ".png": Format.IMAGE,
    ".jpg": Format.IMAGE,
    ".jpeg": Format.IMAGE,
    ".gif": Format.IMAGE,
    ".tiff": Format.IMAGE,
}


def detect_url(value: str) -> Format:
    parsed = urlparse(value.strip())
    if parsed.scheme not in {"http", "https"}:
        return Format.UNKNOWN
    host = parsed.netloc.lower()
    if "youtube.com" in host or "youtu.be" in host:
        return Format.YOUTUBE_URL
    return Format.WEB_URL


def detect_format(source: str | Path) -> Format:
    source_text = str(source).strip()
    url_format = detect_url(source_text)
    if url_format is not Format.UNKNOWN:
        return url_format

    path = Path(source)
    suffix_format = EXTENSION_FORMATS.get(path.suffix.lower())
    if suffix_format is not None:
        if suffix_format is Format.TEXT and path.exists():
            first_text = path.read_text(encoding="utf-8-sig", errors="replace").strip()[:500]
            url_format = detect_url(first_text)
            if url_format is not Format.UNKNOWN:
                return url_format
        return suffix_format

    if not path.exists() or not path.is_file():
        return Format.UNKNOWN

    magic = path.read_bytes()[:16]
    if magic.startswith(b"%PDF"):
        return Format.PDF
    if magic.startswith(b"PK\x03\x04"):
        return Format.UNKNOWN
    if magic.startswith(b"\x89PNG"):
        return Format.IMAGE
    if magic[:3] == b"\xff\xd8\xff":
        return Format.IMAGE
    if b"<html" in magic.lower() or b"<!doctype html" in magic.lower():
        return Format.HTML
    return Format.UNKNOWN

