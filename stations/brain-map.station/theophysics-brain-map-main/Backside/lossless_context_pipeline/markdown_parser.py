from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from .ids import short_hash, slugify


FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def load_markdown(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8-sig")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    frontmatter = yaml.safe_load(match.group(1)) or {}
    return frontmatter, text[match.end() :]


def split_blocks(markdown: str) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    heading_stack: list[tuple[int, str]] = []
    buffer: list[str] = []
    ordinal = 0

    def flush() -> None:
        nonlocal ordinal, buffer
        text = "\n".join(buffer).strip()
        if not text:
            buffer = []
            return
        ordinal += 1
        headings = [item[1] for item in heading_stack]
        section_id = slugify(headings[-1] if headings else "root")
        blocks.append(
            {
                "ordinal": ordinal,
                "section_id": section_id,
                "heading_path": headings,
                "text": text,
                "content_hash": short_hash(text, length=24),
            }
        )
        buffer = []

    for line in markdown.splitlines():
        heading = HEADING_RE.match(line)
        if heading:
            flush()
            level = len(heading.group(1))
            title = heading.group(2).strip()
            heading_stack = [item for item in heading_stack if item[0] < level]
            heading_stack.append((level, title))
            continue
        if not line.strip():
            flush()
            continue
        buffer.append(line)
    flush()
    return blocks
