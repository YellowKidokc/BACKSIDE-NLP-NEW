from __future__ import annotations

import argparse
import html
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
CANON_TERMS = ROOT / "CONFIG" / "canon_terms.json"


BLOCK_TAGS = {"p", "li", "blockquote", "figcaption"}
HEADING_TAGS = {"h1", "h2", "h3", "h4"}
SKIP_TAGS = {"script", "style", "noscript", "svg"}
MATH_SPAN_RE = re.compile(r"(\$\$.*?\$\$|\$[^$\n]{2,160}\$|\\\([^)]+\\\)|\\\[[^\]]+\\\])", re.DOTALL)
EQUATION_RE = re.compile(r"([A-Za-zχΧ][\wχΧ_{}()\[\]\^\\]*\s*=\s*[^.;<>\n]{1,160})")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z\-]{5,}")


@dataclass
class TextBlock:
    id: str
    tag: str
    text: str


class ArticleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.meta: dict[str, str] = {}
        self.blocks: list[TextBlock] = []
        self._stack: list[str] = []
        self._current_tag: str | None = None
        self._current_text: list[str] = []
        self._skip_depth = 0
        self._in_title = False
        self._title_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        self._stack.append(tag)
        if tag in SKIP_TAGS:
            self._skip_depth += 1
        if tag == "title":
            self._in_title = True
        attrs_dict = {key.lower(): value or "" for key, value in attrs}
        if tag == "meta":
            name = attrs_dict.get("name") or attrs_dict.get("property")
            content = attrs_dict.get("content")
            if name and content:
                self.meta[name] = content
        if self._skip_depth:
            return
        if tag in BLOCK_TAGS or tag in HEADING_TAGS:
            self._flush()
            self._current_tag = tag
            self._current_text = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self._in_title = False
            self.title = " ".join("".join(self._title_parts).split())
        if self._skip_depth and tag in SKIP_TAGS:
            self._skip_depth -= 1
        if self._current_tag == tag:
            self._flush()
        if self._stack:
            self._stack.pop()

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._title_parts.append(data)
        if self._skip_depth or not self._current_tag:
            return
        self._current_text.append(data)

    def _flush(self) -> None:
        if not self._current_tag:
            return
        text = html.unescape(" ".join("".join(self._current_text).split()))
        if len(text) >= 24:
            block_id = f"p{len(self.blocks) + 1:04d}"
            self.blocks.append(TextBlock(block_id, self._current_tag, text))
        self._current_tag = None
        self._current_text = []


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def slug_for(path: Path) -> str:
    stem = re.sub(r"[^A-Za-z0-9]+", "-", path.stem).strip("-").lower()
    return stem or "article"


def html_files(path: Path) -> Iterable[Path]:
    if path.is_file() and path.suffix.lower() in {".html", ".htm"}:
        yield path
        return
    for item in path.rglob("*"):
        if item.is_file() and item.suffix.lower() in {".html", ".htm"}:
            yield item


def parse_article(path: Path) -> ArticleParser:
    parser = ArticleParser()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    parser._flush()
    return parser


def find_equations(text: str) -> list[str]:
    seen: list[str] = []
    candidates = [match.group(1) for match in MATH_SPAN_RE.finditer(text)]
    text_without_math_spans = MATH_SPAN_RE.sub(" ", text)
    candidates.extend(match.group(1) for match in EQUATION_RE.finditer(text_without_math_spans))
    for candidate in candidates:
        value = " ".join(candidate.split()).strip()
        value = value.strip("$")
        if value not in seen:
            seen.append(value)
    return seen


def canon_hits(blocks: list[TextBlock], canon_terms: dict) -> list[dict]:
    hits: list[dict] = []
    for block in blocks:
        lowered = block.text.lower()
        for family, entries in canon_terms.items():
            if not isinstance(entries, dict):
                continue
            for anchor, terms in entries.items():
                matched = [term for term in terms if term.lower() in lowered]
                if matched:
                    hits.append(
                        {
                            "paragraph_id": block.id,
                            "family": family,
                            "anchor": anchor,
                            "matched_terms": matched,
                            "text_preview": block.text[:260],
                        }
                    )
    return hits


def glossary_candidates(blocks: list[TextBlock], canon_terms: dict) -> list[dict]:
    forced = set(canon_terms.get("reader_glossary_force_terms", []))
    counts: dict[str, int] = {}
    for block in blocks:
        for word in WORD_RE.findall(block.text):
            clean = word.strip("-").lower()
            if len(clean) >= 9 or clean in forced:
                counts[clean] = counts.get(clean, 0) + 1
    for term in forced:
        key = term.lower()
        if any(key in block.text.lower() for block in blocks):
            counts[key] = max(counts.get(key, 0), 1)
    common = {"because", "through", "between", "without", "something", "everything", "article"}
    rows = [
        {"term": term, "count": count}
        for term, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
        if term not in common
    ]
    return rows[:80]


def build_review_markdown(slug: str, source: Path, title: str, blocks: list[TextBlock], hits: list[dict], equations: list[str], glossary: list[dict]) -> str:
    lines = [
        f"# Article Refinery Review - {slug}",
        "",
        f"Source: `{source}`",
        f"Title: {title or source.stem}",
        "",
        "## Pipeline Status",
        "",
        "TODO: AI review of generated prompt packet",
        "IN_PROGRESS: deterministic extraction complete",
        "REVIEW: canon candidates, glossary candidates, math candidates",
        "BLOCKED: human/AI judgment layers not filled yet",
        "DONE: article text extracted and mapped by first-pass terms",
        "",
        "## Extracted Shape",
        "",
        f"- Text blocks: {len(blocks)}",
        f"- Canon candidate hits: {len(hits)}",
        f"- Equation candidates: {len(equations)}",
        f"- Glossary candidates: {len(glossary)}",
        "",
        "## Strongest Canon Candidate Hits",
        "",
    ]
    for hit in hits[:40]:
        lines.append(f"- `{hit['paragraph_id']}` {hit['family']} / {hit['anchor']} via {', '.join(hit['matched_terms'])}")
    if not hits:
        lines.append("- No deterministic canon hits found.")
    lines.extend(["", "## Equation Candidates", ""])
    for equation in equations[:30]:
        lines.append(f"- `{equation}`")
    if not equations:
        lines.append("- No equation candidates found.")
    lines.extend(["", "## Glossary Candidates", ""])
    for row in glossary[:50]:
        lines.append(f"- {row['term']} ({row['count']})")
    return "\n".join(lines) + "\n"


def build_prompt_packet(slug: str, title: str) -> str:
    return f"""# AI Prompt Packet - {slug}

Article title: {title}

Use these local artifacts:

- `OUTPUT/{slug}/article_extract.json`
- `OUTPUT/{slug}/canon_candidates.json`
- `OUTPUT/{slug}/math_candidates.json`
- `OUTPUT/{slug}/glossary_candidates.json`
- `REVIEW/{slug}/canon_mapping_first_pass.md`

Run the prompts:

1. `PROMPTS/article_public_refinery.md`
2. `PROMPTS/canon_mapping_review.md`
3. `PROMPTS/math_translation_coherence.md` if math candidates exist

Return final review output as:

- `REVIEW/{slug}/executive_summary.md`
- `REVIEW/{slug}/explain_it_simply.md`
- `REVIEW/{slug}/master_equation_map.md`
- `REVIEW/{slug}/rigor_kill_conditions.md`
- `REVIEW/{slug}/math_in_plain_english.md`
- `REVIEW/{slug}/glossary.md`
- `REVIEW/{slug}/post_summary.md`

Do not rewrite the source HTML yet. This is review packet generation.
"""


def process_file(path: Path, output_root: Path, review_root: Path, canon_terms: dict) -> dict:
    parser = parse_article(path)
    slug = slug_for(path)
    output_dir = output_root / slug
    review_dir = review_root / slug
    full_text = "\n\n".join(block.text for block in parser.blocks)
    equations = find_equations(full_text)
    hits = canon_hits(parser.blocks, canon_terms)
    glossary = glossary_candidates(parser.blocks, canon_terms)

    extract = {
        "schema_version": "1.0",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source": str(path),
        "slug": slug,
        "title": parser.title,
        "meta": parser.meta,
        "blocks": [asdict(block) for block in parser.blocks],
    }
    write_json(output_dir / "article_extract.json", extract)
    write_json(output_dir / "canon_candidates.json", hits)
    write_json(output_dir / "math_candidates.json", {"equations": equations})
    write_json(output_dir / "glossary_candidates.json", glossary)
    write_text(review_dir / "canon_mapping_first_pass.md", build_review_markdown(slug, path, parser.title, parser.blocks, hits, equations, glossary))
    write_text(review_dir / "ai_prompt_packet.md", build_prompt_packet(slug, parser.title or path.stem))
    write_text(
        review_dir / "publish_checklist.md",
        f"""# Publish Checklist - {slug}

- [ ] Executive summary reviewed
- [ ] Explain-it-simply reviewed
- [ ] Master Equation / canon map reviewed
- [ ] Axiom/formal proof map reviewed
- [ ] Math translation checked if equations exist
- [ ] Rigor and kill conditions reviewed
- [ ] Glossary definitions written
- [ ] Post summary approved
- [ ] HTML update applied
- [ ] Final browser check complete
""",
    )
    return {
        "slug": slug,
        "source": str(path),
        "title": parser.title,
        "text_blocks": len(parser.blocks),
        "canon_hits": len(hits),
        "equations": len(equations),
        "glossary_candidates": len(glossary),
        "output": str(output_dir),
        "review": str(review_dir),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run public GTQ/Theophysics article refinery extraction.")
    parser.add_argument("--input", default=str(ROOT / "INPUT"), help="HTML file or directory.")
    parser.add_argument("--output", default=str(ROOT / "OUTPUT"))
    parser.add_argument("--review", default=str(ROOT / "REVIEW"))
    args = parser.parse_args()

    input_path = Path(args.input)
    output_root = Path(args.output)
    review_root = Path(args.review)
    canon_terms = read_json(CANON_TERMS)

    files = list(html_files(input_path))
    results = [process_file(path, output_root, review_root, canon_terms) for path in files]
    summary = {
        "schema_version": "1.0",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "input": str(input_path),
        "file_count": len(results),
        "results": results,
    }
    write_json(output_root / "last_run_summary.json", summary)
    print(f"Processed {len(results)} HTML file(s). Summary: {output_root / 'last_run_summary.json'}")
    return 0 if results else 2


if __name__ == "__main__":
    raise SystemExit(main())
