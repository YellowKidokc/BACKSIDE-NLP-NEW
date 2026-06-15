#!/usr/bin/env python3
"""
GTQ Article Section Labeler
===========================

Adds canonical GTQ comment markers around recognizable article components
without changing the existing HTML content. By default it writes a labeled copy
beside the source file and emits a JSON inventory.

Examples:
  python label_gtq_sections.py "\\dlowenas\\HPWorkstation\\Desktop\\HERO.html"
  python label_gtq_sections.py "D:\\GTQ-BUILD\\articles" --recursive
  python label_gtq_sections.py "article.html" --in-place

Marker format:
  <!-- BEGIN: SECTION-NAME -->
  ...
  <!-- END: SECTION-NAME -->
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


VOID_TAGS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}


@dataclass(frozen=True)
class LabelRange:
    name: str
    start: int
    end: int
    pattern: str
    text_hint: str = ""


def has_class(start_tag: str, class_name: str) -> bool:
    match = re.search(r"\bclass\s*=\s*(['\"])(.*?)\1", start_tag, re.I | re.S)
    if not match:
        return False
    classes = re.split(r"\s+", match.group(2).strip())
    return class_name in classes


def has_id(start_tag: str, id_value: str) -> bool:
    return re.search(rf"\bid\s*=\s*(['\"]){re.escape(id_value)}\1", start_tag, re.I) is not None


def opening_tag_name(start_tag: str) -> str | None:
    match = re.match(r"<\s*([a-zA-Z][\w:-]*)\b", start_tag)
    return match.group(1).lower() if match else None


def find_matching_element_end(html: str, start: int) -> int | None:
    start_match = re.match(r"<\s*([a-zA-Z][\w:-]*)\b[^>]*>", html[start:], re.S)
    if not start_match:
        return None

    tag = start_match.group(1).lower()
    first_tag = start_match.group(0)
    first_end = start + start_match.end()

    if tag in VOID_TAGS or first_tag.rstrip().endswith("/>"):
        return first_end

    tag_re = re.compile(rf"</?{re.escape(tag)}\b[^>]*>", re.I | re.S)
    depth = 1
    for match in tag_re.finditer(html, first_end):
        token = match.group(0)
        if token.startswith("</"):
            depth -= 1
            if depth == 0:
                return match.end()
        elif not token.rstrip().endswith("/>"):
            depth += 1

    return None


def element_ranges_by_start_tag(html: str, label: str, predicate, pattern_name: str) -> list[LabelRange]:
    ranges: list[LabelRange] = []
    for match in re.finditer(r"<[a-zA-Z][\w:-]*\b[^>]*>", html, re.S):
        start_tag = match.group(0)
        if not predicate(start_tag):
            continue
        end = find_matching_element_end(html, match.start())
        if end is None:
            continue
        ranges.append(LabelRange(label, match.start(), end, pattern_name, start_tag[:140]))
    return ranges


def element_ranges_inside(html: str, parent: LabelRange | None, label: str, predicate, pattern_name: str) -> list[LabelRange]:
    if not parent:
        return []
    return [
        item
        for item in element_ranges_by_start_tag(html, label, predicate, pattern_name)
        if parent.start <= item.start and item.end <= parent.end
    ]


def first_element_by_start_tag(html: str, label: str, predicate, pattern_name: str) -> list[LabelRange]:
    ranges = element_ranges_by_start_tag(html, label, predicate, pattern_name)
    return ranges[:1]


def section_by_id(html: str, section_id: str, label: str, aliases: Iterable[str] = ()) -> list[LabelRange]:
    ids = [section_id, *aliases]

    def predicate(tag: str) -> bool:
        return opening_tag_name(tag) == "section" and any(has_id(tag, item) for item in ids)

    return first_element_by_start_tag(html, label, predicate, f"section id={section_id}")


def classify_kill_card(html: str, range_item: LabelRange) -> str:
    start_tag_match = re.match(r"<[a-zA-Z][\w:-]*\b[^>]*>", html[range_item.start :], re.S)
    start_tag = start_tag_match.group(0) if start_tag_match else ""
    body = html[range_item.start : range_item.end].lower()
    if has_class(start_tag, "destructive") or "destructive" in body:
        return "KILL-CARD-DESTRUCTIVE"
    if has_class(start_tag, "suggestive") or "suggestive" in body:
        return "KILL-CARD-SUGGESTIVE"
    return "KILL-CARD-LOAD-BEARING"


def child_ranges_inside(parent: LabelRange, ranges: Iterable[LabelRange]) -> list[LabelRange]:
    return [item for item in ranges if parent.start <= item.start and item.end <= parent.end]


def find_article_stats(html: str, kill_sidebar: LabelRange | None, kill_cards: list[LabelRange]) -> list[LabelRange]:
    if not kill_sidebar:
        return []
    last_card_end = max((item.end for item in kill_cards if kill_sidebar.start <= item.start <= kill_sidebar.end), default=kill_sidebar.start)
    sidebar_html = html[last_card_end : kill_sidebar.end]
    match = re.search(r"<div\b[^>]*>", sidebar_html, re.I | re.S)
    if not match:
        return []
    start = last_card_end + match.start()
    end = find_matching_element_end(html, start)
    if not end or end > kill_sidebar.end:
        return []
    return [LabelRange("ARTICLE-STATS", start, end, "first div after kill cards")]


def find_equations(html: str) -> list[LabelRange]:
    ranges: list[LabelRange] = []
    protected = []
    for protected_tag in ("script", "style", "head"):
        protected += element_ranges_by_start_tag(
            html,
            "PROTECTED",
            lambda tag, protected_tag=protected_tag: opening_tag_name(tag) == protected_tag,
            protected_tag,
        )

    for item in element_ranges_by_start_tag(
        html,
        "PAPER-EQUATION",
        lambda tag: has_class(tag, "math-box") or has_class(tag, "equation-block"),
        "class math-box/equation-block",
    ):
        ranges.append(item)

    for match in re.finditer(r"\$\$[\s\S]+?\$\$", html):
        if any(item.start <= match.start() and match.end() <= item.end for item in protected):
            continue
        if any(item.start <= match.start() and match.end() <= item.end for item in ranges):
            continue
        ranges.append(LabelRange("PAPER-EQUATION", match.start(), match.end(), "$$...$$", match.group(0)[:120]))

    return ranges


def find_paragraphs_inside(html: str, parent: LabelRange | None, label: str) -> list[LabelRange]:
    if not parent:
        return []
    ranges: list[LabelRange] = []
    segment = html[parent.start : parent.end]
    for match in re.finditer(r"<p\b[^>]*>", segment, re.I | re.S):
        start = parent.start + match.start()
        end = find_matching_element_end(html, start)
        if end and end <= parent.end:
            ranges.append(LabelRange(label, start, end, "<p> inside tab"))
    return ranges


def find_headings_inside(html: str, parent: LabelRange | None, label: str) -> list[LabelRange]:
    if not parent:
        return []
    ranges: list[LabelRange] = []
    segment = html[parent.start : parent.end]
    for match in re.finditer(r"<h[1-6]\b[^>]*>", segment, re.I | re.S):
        start = parent.start + match.start()
        end = find_matching_element_end(html, start)
        if end and end <= parent.end:
            ranges.append(LabelRange(label, start, end, "heading inside tab"))
    return ranges


def find_top_level_ranges(html: str) -> list[LabelRange]:
    ranges: list[LabelRange] = []

    ranges += first_element_by_start_tag(
        html,
        "TOPBAR",
        lambda tag: (
            opening_tag_name(tag) in {"header", "section"}
            and (
                has_class(tag, "site-header")
                or has_class(tag, "gtq-canon-bar")
                or has_class(tag, "gtq-canon-shell")
                or has_class(tag, "canon-bar")
            )
        ),
        "site-header / canon bar",
    )
    ranges += first_element_by_start_tag(
        html,
        "SIDEBAR-NAV",
        lambda tag: opening_tag_name(tag) == "nav" and has_class(tag, "sidebar"),
        "nav.sidebar",
    )
    ranges += first_element_by_start_tag(
        html,
        "HERO",
        lambda tag: has_class(tag, "hero-grid") or has_class(tag, "article-hero-wrap"),
        "hero-grid / article-hero-wrap",
    )
    ranges += first_element_by_start_tag(
        html,
        "TAB-BAR",
        lambda tag: has_class(tag, "tab-shell") or (opening_tag_name(tag) == "nav" and has_class(tag, "tab-nav")),
        "tab-shell / tab-nav",
    )
    ranges += first_element_by_start_tag(
        html,
        "MAIN-LAYOUT",
        lambda tag: opening_tag_name(tag) == "main" and (has_class(tag, "main-layout") or has_class(tag, "container")),
        "main.main-layout / main.container",
    )
    ranges += first_element_by_start_tag(
        html,
        "KILL-SIDEBAR",
        lambda tag: opening_tag_name(tag) == "aside" and has_class(tag, "kill-sidebar"),
        "aside.kill-sidebar",
    )
    ranges += first_element_by_start_tag(
        html,
        "BOTTOM-NAV",
        lambda tag: has_class(tag, "bottom-nav") or has_class(tag, "article-nav"),
        "bottom-nav / article-nav",
    )
    ranges += first_element_by_start_tag(
        html,
        "FOOTER",
        lambda tag: opening_tag_name(tag) == "footer" or has_class(tag, "site-footer"),
        "footer / site-footer",
    )
    ranges += first_element_by_start_tag(
        html,
        "AUDIO-DOCK",
        lambda tag: has_id(tag, "audioDock") or has_class(tag, "audio-dock") or has_class(tag, "player-dock"),
        "audioDock / audio-dock",
    )

    return ranges


def find_tab_ranges(html: str) -> list[LabelRange]:
    ranges: list[LabelRange] = []
    ranges += section_by_id(html, "summary", "TAB-EXECUTIVE-SUMMARY")
    ranges += section_by_id(html, "paper", "TAB-PAPER", aliases=["story"])
    ranges += section_by_id(html, "simple", "TAB-EXPLAIN-IT-SIMPLE", aliases=["eli14"])
    ranges += section_by_id(html, "rigor", "TAB-RIGOR-KILL-CONDITIONS")
    ranges += section_by_id(html, "media", "TAB-WATCH-LISTEN")
    ranges += section_by_id(html, "mathematics", "TAB-MATHEMATICS", aliases=["math"])
    ranges += section_by_id(html, "glossary", "TAB-GLOSSARY")
    ranges += section_by_id(html, "related", "TAB-RELATED-PAPERS")
    ranges += section_by_id(html, "greader", "TAB-GREADER")
    return ranges


def find_component_ranges(html: str, tabs: list[LabelRange], top_level: list[LabelRange]) -> list[LabelRange]:
    ranges: list[LabelRange] = []
    tab_by_name = {item.name: item for item in tabs}
    kill_sidebar = next((item for item in top_level if item.name == "KILL-SIDEBAR"), None)

    hero_cards = element_ranges_by_start_tag(
        html,
        "HERO-SIDE-CARD",
        lambda tag: has_class(tag, "hero-side"),
        "hero-side",
    )
    for index, card in enumerate(hero_cards, start=1):
        name = "HERO-SIDE-KEY-FINDING" if index == 1 else "HERO-SIDE-CRITICAL-INSIGHT" if index == 2 else "HERO-SIDE-CARD"
        ranges.append(LabelRange(name, card.start, card.end, card.pattern, card.text_hint))

    kill_cards_raw = element_ranges_by_start_tag(
        html,
        "KILL-CARD",
        lambda tag: has_class(tag, "kill-card"),
        "kill-card",
    )
    kill_cards = [LabelRange(classify_kill_card(html, item), item.start, item.end, item.pattern, item.text_hint) for item in kill_cards_raw]
    ranges += kill_cards
    ranges += find_article_stats(html, kill_sidebar, kill_cards_raw)

    summary = tab_by_name.get("TAB-EXECUTIVE-SUMMARY")
    if summary:
        ranges += find_headings_inside(html, summary, "EXEC-HEADER")[:1]
        ranges += element_ranges_inside(html, summary, "EXEC-VIDEO", lambda tag: has_class(tag, "summary-video-card"), "summary-video-card")
        ranges += element_ranges_inside(html, summary, "EXEC-ENIGMA", lambda tag: has_class(tag, "enigma") or has_class(tag, "insight"), "enigma / insight")
        ranges += element_ranges_inside(html, summary, "EXEC-KEY-CLAIMS", lambda tag: opening_tag_name(tag) in {"ul", "ol"}, "list in summary")
        ranges += [LabelRange("EXEC-KEY-TERMS", summary.end, summary.end, "placeholder")]

    paper = tab_by_name.get("TAB-PAPER")
    if paper:
        ranges += find_headings_inside(html, paper, "PAPER-HEADING")
        ranges += find_paragraphs_inside(html, paper, "PAPER-PARAGRAPH")
        ranges += element_ranges_inside(html, paper, "PAPER-CALLOUT", lambda tag: has_class(tag, "insight") or has_class(tag, "axiom-box") or has_class(tag, "pull-quote"), "paper callout")
        ranges += element_ranges_inside(html, paper, "PAPER-CHART", lambda tag: opening_tag_name(tag) == "canvas" or has_class(tag, "chart"), "canvas / chart")
        ranges += element_ranges_inside(html, paper, "PAPER-BLOCK-GRID", lambda tag: has_class(tag, "grid") or has_class(tag, "block-grid"), "grid / block-grid")

    simple = tab_by_name.get("TAB-EXPLAIN-IT-SIMPLE")
    if simple:
        ranges += find_headings_inside(html, simple, "SIMPLE-HEADER")[:1]
        ranges += element_ranges_inside(html, simple, "SIMPLE-CARD", lambda tag: has_class(tag, "card"), "card in simple")
        ranges += [LabelRange("SIMPLE-BOTTOM-LINE", simple.end, simple.end, "placeholder")]

    rigor = tab_by_name.get("TAB-RIGOR-KILL-CONDITIONS")
    if rigor:
        ranges += find_headings_inside(html, rigor, "RIGOR-HEADER")[:1]
        ranges += element_ranges_inside(html, rigor, "RIGOR-TABLE", lambda tag: opening_tag_name(tag) == "table", "table in rigor")
        ranges += [LabelRange("RIGOR-WHAT-WE-GOT-RIGHT", rigor.end, rigor.end, "placeholder")]
        ranges += [LabelRange("RIGOR-WHAT-WE-GOT-WRONG", rigor.end, rigor.end, "placeholder")]
        ranges += [LabelRange("RIGOR-WHAT-WE-OVERCLAIMED", rigor.end, rigor.end, "placeholder")]

    media = tab_by_name.get("TAB-WATCH-LISTEN")
    if media:
        media_cards = element_ranges_inside(html, media, "MEDIA-CARD", lambda tag: has_class(tag, "media-card"), "media-card")
        labels = ["MEDIA-READ-ALOUD", "MEDIA-VIDEO", "MEDIA-DEEP-DIVE", "MEDIA-DEBATE", "MEDIA-CRITIQUE"]
        for index, card in enumerate(media_cards):
            name = labels[index] if index < len(labels) else "MEDIA-CARD"
            ranges.append(LabelRange(name, card.start, card.end, card.pattern, card.text_hint))

    math_tab = tab_by_name.get("TAB-MATHEMATICS")
    if math_tab:
        ranges += find_headings_inside(html, math_tab, "MATH-HEADER")[:1]
        math_equations = [item for item in find_equations(html) if math_tab.start <= item.start and item.end <= math_tab.end]
        for item in math_equations:
            ranges.append(LabelRange("MATH-EQUATION-BLOCK", item.start, item.end, item.pattern, item.text_hint))

    glossary = tab_by_name.get("TAB-GLOSSARY")
    if glossary:
        ranges += find_headings_inside(html, glossary, "GLOSSARY-HEADER")[:1]
        ranges += element_ranges_inside(html, glossary, "GLOSSARY-TERM", lambda tag: has_class(tag, "card") or has_class(tag, "glossary-term"), "glossary card/term")

    related = tab_by_name.get("TAB-RELATED-PAPERS")
    if related:
        ranges += find_headings_inside(html, related, "RELATED-HEADER")[:1]
        ranges += element_ranges_inside(html, related, "RELATED-CARD", lambda tag: has_class(tag, "card"), "related card")

    ranges += find_equations(html)
    return ranges


def remove_duplicate_and_existing(html: str, ranges: list[LabelRange]) -> list[LabelRange]:
    existing = set(re.findall(r"<!--\s*BEGIN:\s*([A-Z0-9-& ]+?)\s*-->", html))
    seen: set[tuple[str, int, int]] = set()
    clean: list[LabelRange] = []

    for item in ranges:
        if item.name in existing:
            continue
        key = (item.name, item.start, item.end)
        if key in seen:
            continue
        seen.add(key)
        clean.append(item)

    return sorted(clean, key=lambda item: (item.start, -(item.end - item.start), item.name))


def apply_markers(html: str, ranges: list[LabelRange]) -> str:
    insertions: dict[int, list[str]] = {}
    for item in ranges:
        if item.start == item.end:
            insertions.setdefault(item.start, []).append(
                f"\n<!-- BEGIN: {item.name} -->\n<!-- TODO: {item.name} placeholder -->\n<!-- END: {item.name} -->\n"
            )
            continue
        insertions.setdefault(item.start, []).append(f"<!-- BEGIN: {item.name} -->\n")
        insertions.setdefault(item.end, []).append(f"\n<!-- END: {item.name} -->")

    output: list[str] = []
    cursor = 0
    for position in sorted(insertions):
        output.append(html[cursor:position])
        # End markers before begin markers at the same position keeps nesting sane.
        markers = sorted(insertions[position], key=lambda value: 0 if value.startswith("\n<!-- END") else 1)
        output.extend(markers)
        cursor = position
    output.append(html[cursor:])
    return "".join(output)


def inventory_for(path: Path, ranges: list[LabelRange]) -> dict:
    counts: dict[str, int] = {}
    for item in ranges:
        counts[item.name] = counts.get(item.name, 0) + 1
    return {
        "source": str(path),
        "labeled_at": datetime.now().isoformat(timespec="seconds"),
        "total_markers_added": len(ranges),
        "counts": dict(sorted(counts.items())),
        "items": [
            {
                "name": item.name,
                "start": item.start,
                "end": item.end,
                "pattern": item.pattern,
                "text_hint": item.text_hint,
            }
            for item in ranges
        ],
    }


def label_html_file(path: Path, in_place: bool) -> tuple[Path, Path, int]:
    html = path.read_text(encoding="utf-8", errors="replace")
    top_level = find_top_level_ranges(html)
    tabs = find_tab_ranges(html)
    components = find_component_ranges(html, tabs, top_level)
    ranges = remove_duplicate_and_existing(html, top_level + tabs + components)

    labeled = apply_markers(html, ranges)

    if in_place:
        backup = path.with_suffix(path.suffix + f".bak-{datetime.now().strftime('%Y%m%d-%H%M%S')}")
        shutil.copy2(path, backup)
        output_path = path
    else:
        output_path = path.with_name(path.stem + ".labeled" + path.suffix)

    output_path.write_text(labeled, encoding="utf-8")
    inventory_path = output_path.with_suffix(output_path.suffix + ".inventory.json")
    inventory_path.write_text(json.dumps(inventory_for(path, ranges), indent=2), encoding="utf-8")
    return output_path, inventory_path, len(ranges)


def discover_targets(target: Path, recursive: bool) -> list[Path]:
    if target.is_file():
        return [target] if target.suffix.lower() in {".html", ".htm"} else []
    if not target.is_dir():
        return []
    pattern = "**/*.htm*" if recursive else "*.htm*"
    return sorted(path for path in target.glob(pattern) if path.is_file() and ".labeled" not in path.name)


def main() -> int:
    parser = argparse.ArgumentParser(description="Label canonical GTQ article sections with BEGIN/END comments.")
    parser.add_argument("target", help="HTML file or folder to label")
    parser.add_argument("--recursive", action="store_true", help="Scan folders recursively")
    parser.add_argument("--in-place", action="store_true", help="Modify source file after creating a timestamped backup")
    args = parser.parse_args()

    targets = discover_targets(Path(args.target), args.recursive)
    if not targets:
        print("No HTML files found.")
        return 1

    for path in targets:
        output_path, inventory_path, count = label_html_file(path, args.in_place)
        print(f"[OK] {path}")
        print(f"     Labeled:   {output_path}")
        print(f"     Inventory: {inventory_path}")
        print(f"     Markers:   {count}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
