from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


DEFAULT_EXPORT_ROOT = Path(r"X:\EXPORTS\paper-grader-station-lab")
DEFAULT_STATE_ROOT = Path(r"X:\Backside\_state\station-lab")

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
HTML_TAG_RE = re.compile(r"<[^>]+>")
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")
YAML_FRONTMATTER_RE = re.compile(r"\A---\s*\n.*?\n---\s*", re.DOTALL)
MEDIA_CALLOUT_RE = re.compile(r"<!--\s*MEDIA_CALLOUT_START\s*-->.*?<!--\s*MEDIA_CALLOUT_END\s*-->", re.DOTALL)
MATH_SIGNAL_RE = re.compile(
    r"("
    r"\b(?:chi|χ|sigma|σ|delta|δ|alpha|β|beta|gamma|λ|lambda|entropy|coherence|gradient|tensor|lagrangian|noether)\b"
    r"|[A-Za-z0-9_χδσβλ]+\s*(?:=|≈|≃|∝|->|→|>=|<=|>|<)\s*[^.\n;]+"
    r"|(?:\d+(?:\.\d+)?\s*(?:σ|sigma|%|x|×))"
    r"|(?:R\^2|p\s*[<=>]\s*0?\.\d+)"
    r")",
    re.IGNORECASE,
)
CLAIM_SIGNAL_RE = re.compile(
    r"\b(claim|therefore|thus|shows|demonstrates|proves|predicts|requires|implies|"
    r"evidence|model|equation|axiom|testable|falsif|measure|correlat)\b",
    re.IGNORECASE,
)


@dataclass
class Section:
    title: str
    level: int
    text: str


def slugify(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return value[:80] or "paper"


def read_text(path: Path) -> str:
    raw = path.read_text(encoding="utf-8-sig", errors="replace")
    if path.suffix.lower() in {".html", ".htm"}:
        raw = HTML_TAG_RE.sub(" ", raw)
        raw = html.unescape(raw)
    raw = YAML_FRONTMATTER_RE.sub("", raw)
    raw = MEDIA_CALLOUT_RE.sub("", raw)
    return re.sub(r"\n{3,}", "\n\n", raw).strip()


def split_sections(text: str) -> list[Section]:
    matches = list(HEADING_RE.finditer(text))
    if not matches:
        return [Section(title="Document", level=1, text=text)]

    sections: list[Section] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append(
            Section(
                title=match.group(2).strip(),
                level=len(match.group(1)),
                text=text[start:end].strip(),
            )
        )
    return sections


def sentences(text: str) -> list[str]:
    compact = re.sub(r"\s+", " ", text).strip()
    if not compact:
        return []
    return [s.strip() for s in SENTENCE_RE.split(compact) if len(s.strip()) > 35]


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def extract_math_items(sections: Iterable[Section]) -> list[dict]:
    items: list[dict] = []
    for section in sections:
        lines = [line.strip() for line in section.text.splitlines() if line.strip()]
        for line in lines:
            if MATH_SIGNAL_RE.search(line):
                items.append(
                    {
                        "section": section.title,
                        "raw": line[:1000],
                        "kind": classify_math_line(line),
                        "translation_stub": translate_math_stub(line),
                    }
                )
    return items


def classify_math_line(line: str) -> str:
    if "=" in line or "≈" in line or "∝" in line:
        return "equation-or-relation"
    if re.search(r"\d", line) and re.search(r"σ|sigma|%|R\^2|p\s*[<=>]", line, re.I):
        return "statistical-claim"
    return "math-language"


def translate_math_stub(line: str) -> str:
    lower = line.lower()
    if "chi" in lower or "χ" in lower:
        return "Likely coherence / master-equation term. Translate by naming what changes, what resists change, and what would falsify the relation."
    if "entropy" in lower:
        return "Likely disorder/noise term. Translate by identifying the direction of drift and whether recovery is modeled."
    if "sigma" in lower or "σ" in lower:
        return "Statistical strength marker. Translate by stating effect size, comparison baseline, and whether the source data is named."
    if "=" in line:
        return "Formal relation. Translate each variable, then state what the equation claims cannot vary independently."
    return "Math-adjacent claim. Translate only after the variables and evidence source are explicit."


def extract_claimish_sentences(text: str, limit: int = 16) -> list[str]:
    scored: list[tuple[int, str]] = []
    for sentence in sentences(text):
        score = 0
        score += 3 if CLAIM_SIGNAL_RE.search(sentence) else 0
        score += 2 if MATH_SIGNAL_RE.search(sentence) else 0
        score += 1 if any(token in sentence.lower() for token in ("because", "therefore", "if ", "then")) else 0
        if score:
            scored.append((score, sentence))
    scored.sort(key=lambda item: (-item[0], len(item[1])))
    return [sentence for _, sentence in scored[:limit]]


def write_markdown(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def station_executive_summary(input_path: Path, text: str, sections: list[Section], export_dir: Path) -> dict:
    claimish = extract_claimish_sentences(text, 8)
    math_items = extract_math_items(sections)
    section_titles = [s.title for s in sections[:8]]
    opening = first_body_opening(text)
    strongest = claimish[0] if claimish else ""
    key_math = next((item["raw"] for item in math_items if item["kind"] == "equation-or-relation"), "")

    lines = [
        f"# Executive Summary - {input_path.stem}",
        "",
        "## Accessible Layer",
        "",
        accessible_summary(input_path, opening, strongest),
        "",
        "## Medium Layer",
        "",
        medium_summary(input_path, opening, strongest, key_math, len(math_items)),
        "",
        "## Academic Layer",
        "",
        academic_summary(input_path, text, sections, math_items, claimish),
        "",
        "## Source Throughline",
        "",
        opening or "No clear throughline detected yet.",
        "",
        "## Load-Bearing Signals",
        "",
    ]
    lines.extend([f"- {item}" for item in claimish[:5]] or ["- No strong claim signals detected."])
    lines.extend(
        [
            "",
            "## Section Map",
            "",
        ]
    )
    lines.extend([f"- {title}" for title in section_titles] or ["- Document"])

    out = export_dir / "executive-summary.md"
    write_markdown(out, lines)
    return {"station": "executive-summary", "export": str(out), "claim_signals": len(claimish)}


def station_overview(input_path: Path, text: str, sections: list[Section], export_dir: Path) -> dict:
    math_items = extract_math_items(sections)
    claimish = extract_claimish_sentences(text, 12)
    lines = [
        f"# Overview - {input_path.stem}",
        "",
        "## Reader Orientation",
        "",
        f"- Word count: {word_count(text):,}",
        f"- Sections detected: {len(sections)}",
        f"- Math candidates: {len(math_items)}",
        f"- Claim-like sentences: {len(claimish)}",
        "",
        "## What This Piece Appears To Be Doing",
        "",
        first_nonempty_sentence(text) or "No opening sentence detected.",
        "",
        "## Structural Outline",
        "",
    ]
    for section in sections:
        lines.append(f"- {'  ' * max(section.level - 1, 0)}{section.title} ({word_count(section.text):,} words)")
    lines.extend(["", "## Strongest Current Signals", ""])
    lines.extend([f"- {item}" for item in claimish[:8]] or ["- No claim signals detected."])
    lines.extend(
        [
            "",
            "## Tuning Questions",
            "",
            "- Does the first paragraph say the actual thesis, or only set mood?",
            "- Which claim would embarrass us most under adversarial review?",
            "- Which equation or statistic is doing real work rather than decoration?",
            "- What should become the final human export, and what should stay internal?",
        ]
    )

    out = export_dir / "overview.md"
    write_markdown(out, lines)
    return {"station": "overview", "export": str(out), "sections": len(sections)}


def station_math_layer(input_path: Path, sections: list[Section], export_dir: Path) -> dict:
    items = extract_math_items(sections)
    lines = [
        f"# Math Layer - {input_path.stem}",
        "",
        "## Purpose",
        "",
        "This file is the digestible math layer: equations, statistics, and math-adjacent claims extracted for translation and review.",
        "",
        f"- Math candidates: {len(items)}",
        "",
    ]
    by_section: dict[str, list[dict]] = {}
    for item in items:
        by_section.setdefault(item["section"], []).append(item)

    if not items:
        lines.append("No math candidates detected.")
    for section, section_items in by_section.items():
        lines.extend(["", f"## {section}", ""])
        for index, item in enumerate(section_items, 1):
            lines.extend(
                [
                    f"### M{index:03d} - {item['kind']}",
                    "",
                    "```text",
                    item["raw"],
                    "```",
                    "",
                    f"Translation note: {item['translation_stub']}",
                    "",
                ]
            )

    out = export_dir / "math-layer.md"
    write_markdown(out, lines)
    return {"station": "math-layer", "export": str(out), "math_candidates": len(items)}


def first_nonempty_sentence(text: str) -> str:
    opening = first_body_opening(text)
    return sentences(opening)[0] if sentences(opening) else opening


def first_body_opening(text: str) -> str:
    fragments: list[str] = []
    for paragraph in re.split(r"\n\s*\n", text):
        paragraph = re.sub(r"^#+\s*", "", paragraph.strip())
        paragraph = re.sub(r"[*_`]", "", paragraph)
        paragraph = paragraph.strip(" -\n\t")
        if not paragraph:
            continue
        lower = paragraph.lower()
        if lower.startswith(("title:", "uuid:", "date_created:", "status:", "series:", "article_number:", "paper_id:", "tags:")):
            continue
        if lower.startswith(("genesis as quantum event:", "a theophysics treatment of")):
            continue
        if "david lowe" in lower and "theophysics framework" in lower:
            continue
        if paragraph.startswith(">"):
            continue
        if len(paragraph) < 20:
            continue
        fragments.append(re.sub(r"\s+", " ", paragraph))
        if sum(len(fragment) for fragment in fragments) > 220:
            break
    return " ".join(fragments).strip()


def accessible_summary(input_path: Path, opening: str, strongest: str) -> str:
    if strongest:
        return (
            f"This piece is trying to make one big idea readable: Genesis is being framed as a real collapse event, "
            f"not just a moral story. Its opening hook is simple: {opening} The strongest current claim is that "
            f"{strip_claim_label(strongest)}"
        )
    return (
        f"This piece is trying to make a Theophysics argument readable from the article `{input_path.name}`. "
        f"The current opening signal is: {opening or 'not yet clearly detected.'}"
    )


def medium_summary(input_path: Path, opening: str, strongest: str, key_math: str, math_count: int) -> str:
    parts = [
        f"`{input_path.name}` argues from a narrative-theological event toward a physics-shaped model.",
        f"The reader-facing entry point is: {opening or 'not yet clearly detected.'}",
    ]
    if strongest:
        parts.append(f"The load-bearing claim to tune first is: {strip_claim_label(strongest)}")
    if key_math:
        parts.append(f"The first formal anchor detected is `{key_math}`.")
    parts.append(
        f"The station found {math_count} math-layer candidates, so the next pass should separate real formal anchors from math-flavored explanatory language."
    )
    return " ".join(parts)


def academic_summary(
    input_path: Path,
    text: str,
    sections: list[Section],
    math_items: list[dict],
    claimish: list[str],
) -> str:
    falsification = [claim for claim in claimish if re.search(r"\bif\b|\btest|falsif|measure|evidence", claim, re.I)]
    return (
        f"`{input_path.name}` contains {word_count(text):,} words across {len(sections)} detected sections. "
        f"The current deterministic pass surfaces {len(math_items)} math candidates and {len(claimish)} prioritized claim signals. "
        f"The academic review layer should focus on three questions: whether the Genesis-as-collapse mapping is structural rather than analogical, "
        f"whether each equation constrains a claim rather than decorating it, and whether falsification language is operational. "
        f"Detected falsification/evidence signals: {len(falsification)}."
    )


def strip_claim_label(value: str) -> str:
    value = re.sub(r"^\*\*Claim\s+\d+:\*\*\s*", "", value).strip()
    value = re.sub(r"^If\b", "if", value)
    return value[:650].rstrip()


def run(input_path: Path, station: str, export_root: Path, state_root: Path) -> Path:
    text = read_text(input_path)
    sections = split_sections(text)
    digest = hashlib.sha256(str(input_path).encode("utf-8") + text[:5000].encode("utf-8")).hexdigest()[:10]
    run_id = f"{datetime.now().strftime('%Y%m%d-%H%M%S')}_{slugify(input_path.stem)}_{digest}"
    export_dir = export_root / run_id
    state_dir = state_root / run_id
    export_dir.mkdir(parents=True, exist_ok=True)
    state_dir.mkdir(parents=True, exist_ok=True)

    results: list[dict] = []
    if station in {"executive-summary", "all"}:
        results.append(station_executive_summary(input_path, text, sections, export_dir))
    if station in {"overview", "all"}:
        results.append(station_overview(input_path, text, sections, export_dir))
    if station in {"math-layer", "all"}:
        results.append(station_math_layer(input_path, sections, export_dir))

    manifest = {
        "run_id": run_id,
        "input": str(input_path),
        "station": station,
        "export_dir": str(export_dir),
        "state_dir": str(state_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "metrics": {
            "word_count": word_count(text),
            "sections": len(sections),
            "math_candidates": len(extract_math_items(sections)),
            "claim_signals": len(extract_claimish_sentences(text, 250)),
        },
        "results": results,
    }
    (state_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_markdown(
        export_dir / "README.md",
        [
            f"# Station Lab Export - {input_path.stem}",
            "",
            f"- Input: `{input_path}`",
            f"- Station: `{station}`",
            f"- Internal state: `{state_dir}`",
            "",
            "## Files",
            "",
            *[f"- `{Path(result['export']).name}` - {result['station']}" for result in results],
        ],
    )
    return export_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Tune paper-grader stations one at a time.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument(
        "--station",
        choices=["executive-summary", "overview", "math-layer", "all"],
        default="all",
    )
    parser.add_argument("--export-root", type=Path, default=DEFAULT_EXPORT_ROOT)
    parser.add_argument("--state-root", type=Path, default=DEFAULT_STATE_ROOT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.input.exists():
        raise SystemExit(f"Input not found: {args.input}")
    export_dir = run(args.input, args.station, args.export_root, args.state_root)
    print(f"Export written: {export_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
