from __future__ import annotations

import re
from pathlib import Path

import html2text
from bs4 import BeautifulSoup

from ..models import ConvertResult


DROP_SELECTORS = [
    "script",
    "style",
    "nav",
    "footer",
    "header",
    "aside",
    ".navigation",
    ".nav",
    ".sidebar",
]


def convert_html(path: Path) -> ConvertResult:
    raw = path.read_text(encoding="utf-8-sig", errors="replace")
    soup = BeautifulSoup(raw, "lxml")
    warnings: list[str] = []

    for selector in DROP_SELECTORS:
        for node in soup.select(selector):
            node.decompose()

    title = ""
    if soup.title and soup.title.string:
        title = " ".join(soup.title.string.split())

    body = soup.body or soup
    converter = html2text.HTML2Text()
    converter.body_width = 0
    converter.ignore_images = False
    converter.ignore_links = False
    converter.ignore_emphasis = False
    converter.unicode_snob = True
    markdown = converter.handle(str(body))
    markdown = normalize_markdown(markdown)

    if not markdown.strip():
        warnings.append("HTML conversion produced empty markdown.")

    metadata = {
        "title": title,
        "source_format": "HTML",
        "source_bytes": len(raw.encode("utf-8", errors="replace")),
        "markdown_words": len(re.findall(r"\b\w+\b", markdown)),
    }
    return ConvertResult(markdown=markdown, metadata=metadata, warnings=warnings)


def normalize_markdown(markdown: str) -> str:
    markdown = markdown.replace("\r\n", "\n").replace("\r", "\n")
    markdown = re.sub(r"\n{4,}", "\n\n\n", markdown)
    markdown = re.sub(r"[ \t]+\n", "\n", markdown)
    return markdown.strip() + "\n"

