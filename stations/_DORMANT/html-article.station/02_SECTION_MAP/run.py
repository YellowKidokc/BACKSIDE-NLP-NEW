#!/usr/bin/env python3
"""02_SECTION_MAP — deterministic section splitter for HTML and Markdown.

Stdlib only. Reads from 00_DROP (or 01_LOSSLESS when present), writes the
section ledger that every downstream lane joins against.

Usage:
    python run.py --in <source_path> --out <output_dir> [--paper-uuid <uuid>]

Output files (in --out):
    section-map.json
    section-map.md
    section_packets/{section_id}.md  (one per section)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import uuid
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

NAMESPACE = uuid.UUID("28282828-0000-0000-0000-000000000001")
HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
SKIP_TAGS = {"script", "style", "noscript", "template"}
STOPWORDS = {"the", "a", "an", "of", "to", "in", "for", "on", "and", "or", "is", "are", "be", "was", "were", "by", "with", "this", "that", "it", "as", "at", "from"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def slugify(value: str, fallback: str = "x") -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or fallback


def stable_uuid(kind: str, *parts: str) -> str:
    raw = "::".join([kind, *[str(part) for part in parts]])
    return str(uuid.uuid5(NAMESPACE, raw))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def count_equations(text: str) -> int:
    inline = len(re.findall(r"(?<!\$)\$[^\$\n]+\$(?!\$)", text))
    display = len(re.findall(r"\$\$[^\$]+\$\$", text, flags=re.S))
    paren = len(re.findall(r"\\\(.+?\\\)", text, flags=re.S))
    bracket = len(re.findall(r"\\\[.+?\\\]", text, flags=re.S))
    mathtag = len(re.findall(r"<math\b", text, flags=re.I))
    return inline + display + paren + bracket + mathtag


def count_citations(text: str) -> int:
    sup = len(re.findall(r"<sup\b[^>]*>.*?</sup>", text, flags=re.I | re.S))
    cite = len(re.findall(r"<cite\b", text, flags=re.I))
    bracket = len(re.findall(r"(?<!\w)\[\d+(?:,\s*\d+)*\](?!\w)", text))
    return sup + cite + bracket


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def first_excerpt(text: str, limit: int = 200) -> str:
    flat = re.sub(r"\s+", " ", text).strip()
    return flat[:limit]


def inferred_heading_from(text: str) -> str:
    tokens = [t for t in re.findall(r"\b[a-zA-Z][a-zA-Z\-]+\b", text or "") if t.lower() not in STOPWORDS]
    return " ".join(tokens[:5]) or "intro"


# --- HTML walker --------------------------------------------------------------

class HtmlSectionWalker(HTMLParser):
    """Streams (event, payload, offset) tuples from an HTML source.

    Events emitted:
      ("section_open", id, offset)
      ("section_close", _, offset)
      ("heading_open", level, offset)
      ("heading_text", text, offset)   # accumulated under any open heading
      ("heading_close", level, offset)
      ("body_text", text, offset)      # text outside headings
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.events: list[tuple] = []
        self._section_id_stack: list[str | None] = []
        self._skip_depth = 0
        self._heading_level: int | None = None
        self._char_offset = 0

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attrs_d = dict(attrs)
        if tag in SKIP_TAGS:
            self._skip_depth += 1
            return
        if tag == "section":
            sid = attrs_d.get("id")
            self._section_id_stack.append(sid)
            self.events.append(("section_open", sid, self._char_offset))
            return
        if tag in HEADING_TAGS:
            self._heading_level = int(tag[1])
            self.events.append(("heading_open", self._heading_level, self._char_offset))
            return

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in SKIP_TAGS:
            if self._skip_depth > 0:
                self._skip_depth -= 1
            return
        if tag == "section":
            if self._section_id_stack:
                self._section_id_stack.pop()
            self.events.append(("section_close", None, self._char_offset))
            return
        if tag in HEADING_TAGS:
            level = int(tag[1])
            self.events.append(("heading_close", level, self._char_offset))
            self._heading_level = None

    def handle_data(self, data):
        if self._skip_depth > 0:
            return
        if not data:
            return
        if self._heading_level is not None:
            self.events.append(("heading_text", data, self._char_offset))
        else:
            self.events.append(("body_text", data, self._char_offset))
        self._char_offset += len(data)


def parse_html(source: str) -> tuple[list[dict], int, int]:
    """Walk HTML and emit section dicts (with raw text spans not yet finalized).

    Returns: (sections, eq_total, cite_total)
    """
    walker = HtmlSectionWalker()
    walker.feed(source)
    walker.close()

    sections: list[dict] = []
    open_stack: list[dict] = []          # stack of open section nodes by heading_level
    section_anchor_stack: list[str | None] = []
    current_heading_text: list[str] = []
    current_heading_level: int | None = None
    pending_body: list[str] = []
    ordinal = 0

    def close_to(level: int):
        while open_stack and open_stack[-1]["heading_level"] >= level:
            sections.append(open_stack.pop())

    for ev in walker.events:
        kind = ev[0]
        if kind == "section_open":
            section_anchor_stack.append(ev[1])
        elif kind == "section_close":
            # close any sections opened solely inside this container; safest is to leave them
            if section_anchor_stack:
                section_anchor_stack.pop()
        elif kind == "heading_open":
            # flush pending body to the most recent open section
            if pending_body and open_stack:
                open_stack[-1].setdefault("_text", []).append("".join(pending_body))
            pending_body = []
            current_heading_text = []
            current_heading_level = ev[1]
        elif kind == "heading_text":
            current_heading_text.append(ev[1])
        elif kind == "heading_close":
            heading_text = "".join(current_heading_text).strip()
            level = current_heading_level or ev[1]
            close_to(level)
            ordinal += 1
            parent = open_stack[-1] if open_stack else None
            node = {
                "ordinal": ordinal,
                "heading_level": level,
                "heading_text": heading_text or "(untitled)",
                "heading_path": (parent["heading_path"] + [heading_text]) if parent else [heading_text],
                "parent_section_id": parent["section_id"] if parent else None,
                "source_anchor": section_anchor_stack[-1] if section_anchor_stack else None,
                "inferred": False,
                "inferred_reason": None,
                "_text": [],
            }
            node["section_id"] = f"sec-{ordinal:03d}-{slugify(heading_text or 'untitled')}"
            open_stack.append(node)
            current_heading_text = []
            current_heading_level = None
        elif kind == "body_text":
            pending_body.append(ev[1])

    if pending_body and open_stack:
        open_stack[-1].setdefault("_text", []).append("".join(pending_body))
    while open_stack:
        sections.append(open_stack.pop())

    # If we never opened a section, the whole document is an inferred intro.
    if not sections:
        body = "".join(pending_body).strip()
        sections.append({
            "ordinal": 1,
            "heading_level": 1,
            "heading_text": inferred_heading_from(body),
            "heading_path": [inferred_heading_from(body)],
            "parent_section_id": None,
            "source_anchor": None,
            "inferred": True,
            "inferred_reason": "No <h1>..<h6> headings detected in source.",
            "_text": [body],
            "section_id": f"sec-001-{slugify(inferred_heading_from(body))}",
        })

    sections.sort(key=lambda s: s["ordinal"])
    eq_total = 0
    cite_total = 0
    for s in sections:
        body = "".join(s.pop("_text", [])).strip()
        s["text"] = body
        s["equation_count"] = count_equations(body)
        s["citation_count"] = count_citations(body)
        s["word_count"] = word_count(body)
        eq_total += s["equation_count"]
        cite_total += s["citation_count"]
    return sections, eq_total, cite_total


# --- Markdown walker ----------------------------------------------------------

def parse_markdown(source: str) -> tuple[list[dict], int, int]:
    # Strip YAML frontmatter.
    if source.lstrip().startswith("---"):
        m = re.match(r"^\s*---\s*\n(.*?)\n---\s*\n", source, flags=re.S)
        if m:
            source = source[m.end():]

    sections: list[dict] = []
    open_stack: list[dict] = []
    pending_body: list[str] = []
    ordinal = 0

    def close_to(level: int):
        while open_stack and open_stack[-1]["heading_level"] >= level:
            sections.append(open_stack.pop())

    def attach_intro_if_needed():
        nonlocal ordinal
        if open_stack:
            return
        if not pending_body:
            return
        body = "".join(pending_body).strip()
        if not body:
            return
        ordinal += 1
        node = {
            "ordinal": ordinal,
            "heading_level": 1,
            "heading_text": "intro",
            "heading_path": ["intro"],
            "parent_section_id": None,
            "source_anchor": None,
            "inferred": True,
            "inferred_reason": "Leading content before first ATX heading.",
            "_text": [body],
            "section_id": f"sec-{ordinal:03d}-intro",
        }
        open_stack.append(node)
        pending_body.clear()

    for line in source.splitlines(keepends=True):
        m = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line.rstrip("\n"))
        if m:
            attach_intro_if_needed()
            if pending_body and open_stack:
                open_stack[-1].setdefault("_text", []).append("".join(pending_body))
            pending_body = []

            level = len(m.group(1))
            heading_text = m.group(2).strip()
            close_to(level)
            ordinal += 1
            parent = open_stack[-1] if open_stack else None
            node = {
                "ordinal": ordinal,
                "heading_level": level,
                "heading_text": heading_text,
                "heading_path": (parent["heading_path"] + [heading_text]) if parent else [heading_text],
                "parent_section_id": parent["section_id"] if parent else None,
                "source_anchor": None,
                "inferred": False,
                "inferred_reason": None,
                "_text": [],
            }
            node["section_id"] = f"sec-{ordinal:03d}-{slugify(heading_text)}"
            open_stack.append(node)
        else:
            pending_body.append(line)

    if pending_body and open_stack:
        open_stack[-1].setdefault("_text", []).append("".join(pending_body))
    elif pending_body and not open_stack:
        attach_intro_if_needed()

    while open_stack:
        sections.append(open_stack.pop())
    sections.sort(key=lambda s: s["ordinal"])

    eq_total = 0
    cite_total = 0
    for s in sections:
        body = "".join(s.pop("_text", [])).strip()
        s["text"] = body
        s["equation_count"] = count_equations(body)
        s["citation_count"] = count_citations(body)
        s["word_count"] = word_count(body)
        eq_total += s["equation_count"]
        cite_total += s["citation_count"]
    return sections, eq_total, cite_total


# --- Finalize and serialize ---------------------------------------------------

def finalize(sections: list[dict], paper_uuid: str, worker: str, source_kind: str) -> list[dict]:
    seen_paths: dict[str, int] = {}
    finalized: list[dict] = []
    for s in sections:
        path_key = "/".join(slugify(p) for p in s["heading_path"])
        n = seen_paths.get(path_key, 0)
        if n > 0:
            s["section_id"] = f"{s['section_id']}-{n + 1}"
        seen_paths[path_key] = n + 1

        body = s.pop("text", "")
        s_id = s["section_id"]
        s["stable_uuid"] = stable_uuid("section", paper_uuid, path_key, str(s["ordinal"]))
        s["text_excerpt"] = first_excerpt(body)
        s["packet_path"] = f"section_packets/{s_id}.md"
        s["source_offset_start"] = s.get("source_offset_start")
        s["source_offset_end"] = s.get("source_offset_end")
        s["passes"] = {
            "section_map":      {"status": "passed",  "timestamp_utc": utc_now(), "worker": worker},
            "math_translation": {"status": "pending"},
            "claims":           {"status": "pending"},
            "vectors":          {"status": "pending"},
            "rigor":            {"status": "pending"},
        }
        s["_body_for_packet"] = body
        finalized.append(s)
    return finalized


def emit(sections: list[dict], src: Path, out_dir: Path, paper_uuid: str, source_kind: str, worker: str, eq_total: int, cite_total: int) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    packets_dir = out_dir / "section_packets"
    packets_dir.mkdir(exist_ok=True)

    sections_for_json: list[dict] = []
    inferred_count = 0
    for s in sections:
        body = s.pop("_body_for_packet", "")
        packet_path = out_dir / s["packet_path"]
        packet_path.parent.mkdir(parents=True, exist_ok=True)
        packet_path.write_text(
            f"# {s['heading_text']}\n\n"
            f"<!-- section_id: {s['section_id']} -->\n"
            f"<!-- heading_path: {' > '.join(s['heading_path'])} -->\n\n"
            f"{body}\n",
            encoding="utf-8",
        )
        if s["inferred"]:
            inferred_count += 1
        sections_for_json.append(s)

    inferred_pct = (inferred_count / max(len(sections), 1))
    loopback_reasons: list[str] = []
    if inferred_pct > 0.10:
        loopback_reasons.append(f"Inferred sections {inferred_count}/{len(sections)} exceed 10% threshold.")

    out_json = {
        "lane_id": "02",
        "lane_name": "Section Map",
        "article_slug": out_dir.name,
        "paper_uuid": paper_uuid,
        "source_file": str(src).replace("\\", "/"),
        "source_kind": source_kind,
        "generated_at_utc": utc_now(),
        "worker": worker,
        "section_count": len(sections),
        "equation_count_total": eq_total,
        "citation_count_total": cite_total,
        "inferred_section_count": inferred_count,
        "sections": sections_for_json,
        "loopback": {"triggered": bool(loopback_reasons), "reasons": loopback_reasons},
    }
    (out_dir / "section-map.json").write_text(json.dumps(out_json, indent=2, ensure_ascii=False), encoding="utf-8")

    md_lines = [
        f"# Section Map — {out_dir.name}",
        "",
        f"- source: `{src}`",
        f"- sections: {len(sections)}",
        f"- equations (total): {eq_total}",
        f"- citations (total): {cite_total}",
        f"- inferred sections: {inferred_count}",
        f"- generated: {out_json['generated_at_utc']}",
        "",
        "## Heading tree",
        "",
    ]
    for s in sections:
        indent = "  " * (s["heading_level"] - 1)
        flag = "  *(inferred)*" if s["inferred"] else ""
        md_lines.append(f"{indent}- `{s['section_id']}` h{s['heading_level']}: {s['heading_text']}{flag}")
    (out_dir / "section-map.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", required=True)
    ap.add_argument("--out", dest="out", required=True)
    ap.add_argument("--paper-uuid", dest="paper_uuid", default=None)
    ap.add_argument("--worker", dest="worker", default="worker-1")
    args = ap.parse_args(argv)

    src = Path(args.src)
    out_dir = Path(args.out)
    text = src.read_text(encoding="utf-8", errors="replace")

    if src.suffix.lower() in {".html", ".htm"}:
        sections, eq_total, cite_total = parse_html(text)
        source_kind = "html"
    else:
        sections, eq_total, cite_total = parse_markdown(text)
        source_kind = "markdown"

    paper_uuid = args.paper_uuid or stable_uuid("paper", str(src).lower(), sha256_text(text)[:16])
    sections = finalize(sections, paper_uuid, args.worker, source_kind)
    emit(sections, src, out_dir, paper_uuid, source_kind, args.worker, eq_total, cite_total)

    print(f"OK lane=02 sections={len(sections)} eq={eq_total} cite={cite_total} out={out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
