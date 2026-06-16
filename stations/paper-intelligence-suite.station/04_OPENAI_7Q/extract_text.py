from __future__ import annotations

import re
from html import unescape
from pathlib import Path


BLOCK_BREAK_TAGS = ("p", "div", "section", "article", "li", "tr", "td", "th", "h1", "h2", "h3", "h4", "h5", "h6", "br")


def strip_html(raw: str) -> str:
    """Convert HTML into analysis-friendly text.

    The paper grader should see document content, not page chrome. We strip
    head/script/style/svg blocks first, then collapse block tags into newlines.
    """
    text = raw
    text = re.sub(r"(?is)<!--.*?-->", " ", text)
    text = re.sub(r"(?is)<head\b.*?>.*?</head>", " ", text)
    text = re.sub(r"(?is)<script\b.*?>.*?</script>", " ", text)
    text = re.sub(r"(?is)<style\b.*?>.*?</style>", " ", text)
    text = re.sub(r"(?is)<svg\b.*?>.*?</svg>", " ", text)
    text = re.sub(r"(?is)<noscript\b.*?>.*?</noscript>", " ", text)
    text = re.sub(r"(?is)<(nav|aside|footer|form)\b.*?>.*?</\1>", " ", text)

    body_match = re.search(r"(?is)<body\b[^>]*>(.*?)</body>", text)
    if body_match:
        text = body_match.group(1)

    for tag in BLOCK_BREAK_TAGS:
        text = re.sub(rf"(?is)</{tag}\s*>", "\n", text)
        text = re.sub(rf"(?is)<{tag}\b[^>]*?/?>", "\n", text)

    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = unescape(text)

    lines: list[str] = []
    for raw_line in text.splitlines():
        line = re.sub(r"[ \t]+", " ", raw_line).strip()
        if not line:
            continue
        if _looks_like_css_or_chrome(line):
            continue
        lines.append(line)

    return "\n\n".join(lines).strip()


def read_paper(path: Path) -> str:
    raw = path.read_text(encoding="utf-8", errors="ignore")
    if path.suffix.lower() in {".html", ".htm"}:
        return strip_html(raw)
    return raw


def _looks_like_css_or_chrome(line: str) -> bool:
    lowered = line.lower()
    if lowered.startswith(("http://", "https://")) and " " not in lowered:
        return True
    css_signals = (
        "font-family:",
        "background:",
        "display:",
        "grid-template",
        "border-radius:",
        "letter-spacing:",
        "text-transform:",
        "scroll-behavior:",
        "box-sizing:",
        "viewport",
        "charset=",
        "doctype html",
    )
    if any(signal in lowered for signal in css_signals):
        return True
    punctuation = sum(1 for ch in line if ch in "{}[];<>:=#")
    alpha = sum(1 for ch in line if ch.isalpha())
    return punctuation > alpha and punctuation >= 6
