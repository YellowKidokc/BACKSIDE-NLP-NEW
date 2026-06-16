from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from bs4 import BeautifulSoup, Comment, NavigableString, Tag


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "CODEX_BUILD" / "tts_markdown"
SOURCE_MD = ROOT / "CODEX_BUILD" / "markdown"


@dataclass(frozen=True)
class Article:
    label: str
    filename: str
    title: str


ARTICLES = [
    Article("01", "gtq-01-measurement-collapsed-reality.html", "The Measurement That Collapsed Reality"),
    Article("01A", "gtq-01a-collapse-threshold.html", "The Collapse Threshold"),
    Article("02", "gtq-02-the-first-quantum-state.html", "The First Quantum State"),
    Article("03", "gtq-03-free-will-two-frames.html", "Free Will in Two Frames"),
    Article("03A", "gtq-03a-macarthur-and-the-equation.html", "MacArthur and the Equation"),
    Article("03B", "gtq-03b-the-three-pathways.html", "The Three Pathways"),
    Article("03C", "gtq-03c-why-god-drowned-everybody.html", "Why God Drowned Everybody"),
    Article("04", "gtq-04-the-day-time-began.html", "The Day Time Began"),
    Article("04A", "gtq-04a-the-decoherence-curve.html", "The Decoherence Curve"),
    Article("04B", "gtq-04b-how-lies-kill.html", "How Lies Kill"),
    Article("05", "gtq-05-the-substrate-fractured.html", "The Substrate Fractured"),
    Article("05A", "gtq-05a-trinity-mechanism.html", "The Trinity Mechanism"),
    Article("05B", "gtq-05b-trinity-timeline.html", "The Trinity Timeline"),
    Article("05C", "gtq-05c-why-physics-is-broken-in-two.html", "Why Physics Is Broken in Two"),
    Article("06", "gtq-06-why-reality-needs-three.html", "Why Reality Needs Three"),
    Article("07", "gtq-07-the-photon-isnt-watching.html", "The Photon Isn't Watching You Back"),
    Article("07A", "gtq-07a-empirical-testing.html", "We Actually Ran the Numbers"),
    Article("08", "gtq-08-god-doesnt-need-a-clock.html", "God Doesn't Need a Clock"),
    Article("08A", "gtq-08a-the-temporal-trap.html", "The Temporal Trap"),
    Article("08B", "gtq-08b-how-god-restores.html", "How God Restores"),
    Article("08C", "gtq-08c-science-behind-restoration.html", "The Science Behind Restoration"),
    Article("09", "gtq-09-same-god-both-testaments.html", "The Same God in Both Testaments"),
    Article("09A", "gtq-09a-regime-dependent-theology.html", "Regime-Dependent Theology"),
    Article("09B", "gtq-09b-civilizational-decay.html", "Civilizational Decay"),
    Article("10", "gtq-10-the-counter-move.html", "The Counter-Move"),
    Article("10A", "gtq-10a-why-the-pattern-is-the-signal.html", "Why the Pattern Is the Signal"),
]

FALLBACK_MARKDOWN = {
    "gtq-07-the-photon-isnt-watching.html": SOURCE_MD / "OBS" / "06_Why the Photon Isn't Watching You Back.md",
}


REMOVE_SELECTORS = [
    "script",
    "style",
    "noscript",
    "svg",
    "canvas",
    "video",
    "audio",
    "iframe",
    "button",
    "nav",
    "footer",
    ".sidebar",
    ".sidebar-overlay",
    ".sidebar-toggle",
    ".gtq-unified-player",
    ".audio-dock",
    ".sticky-player",
    ".floating-player",
    ".bottom-nav",
    ".topbar-gold-edge",
    ".tp-ribbon",
    ".prog",
    ".progress-track",
    ".progress-fill",
    ".tab-buttons",
    ".tab-nav",
    ".tabs",
    ".share-section",
    ".ring-nav",
    ".hero-banner",
    ".hero-main",
    ".hero-side",
    ".audio-deck",
    ".ps-deck-card",
    ".paper-audio",
    ".threshold-widget",
    ".top-threshold",
    ".bb-canvas",
]

SIDE_SELECTORS = [
    ".kill-sidebar",
    ".gtq-system-audit",
    ".cw-audit",
    ".audit",
]


def clean_text(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = text.replace("\u200b", "")
    replacements = {
        "\u00e2\u20ac\u201d": "—",
        "\u00e2\u20ac\u201c": "–",
        "\u00e2\u20ac\u02dc": "'",
        "\u00e2\u20ac\u2122": "'",
        "\u00e2\u20ac\u0153": '"',
        "\u00e2\u20ac\u009d": '"',
        "\u00e2\u2020\u2019": "->",
        "\u00e2\u2020\u201d": "<->",
        "\u00c2\u00b7": "·",
        "\u00c2": "",
        "\u00cf\u0087": "χ",
        "\u00cf\u0083": "σ",
        "\u00cf\u0080": "π",
        "\u00ce\u00a9": "Ω",
        "\u00e2\u2030\u00a5": ">=",
        "\u00e2\u2030\u00a4": "<=",
        "\u00f0\u0178\u201c\u2039": "",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n[ \t]+", "\n", text)
    return text.strip()


def normalize_math(text: str) -> str:
    def block_repl(match: re.Match[str]) -> str:
        body = match.group(1).strip()
        return f"\n\n$$\n{body}\n$$\n\n"

    text = re.sub(r"\\\[(.*?)\\\]", block_repl, text, flags=re.S)
    text = re.sub(r"\$\$\s*(.*?)\s*\$\$", block_repl, text, flags=re.S)
    return text


def inline_md(node: Tag | NavigableString) -> str:
    if isinstance(node, Comment):
        return ""
    if isinstance(node, NavigableString):
        return clean_text(str(node))
    if not isinstance(node, Tag):
        return ""
    name = node.name.lower()
    text = " ".join(inline_md(child) for child in node.children)
    text = clean_text(text)
    if not text:
        return ""
    if name in {"strong", "b"}:
        return f"**{text}**"
    if name in {"em", "i"}:
        return f"*{text}*"
    if name == "code":
        return f"`{text}`"
    if name == "br":
        return "\n"
    if name == "a":
        href = node.get("href", "")
        if href and not href.startswith("#"):
            return f"{text} ({href})"
    return text


def table_md(table: Tag) -> str:
    rows: list[list[str]] = []
    for tr in table.find_all("tr"):
        row = [clean_text(cell.get_text(" ", strip=True)) for cell in tr.find_all(["th", "td"])]
        if row:
            rows.append(row)
    if not rows:
        return ""
    width = max(len(row) for row in rows)
    rows = [row + [""] * (width - len(row)) for row in rows]
    out = ["| " + " | ".join(rows[0]) + " |"]
    out.append("| " + " | ".join(["---"] * width) + " |")
    for row in rows[1:]:
        out.append("| " + " | ".join(row) + " |")
    return "\n".join(out)


def block_md(node: Tag, depth: int = 0) -> list[str]:
    if isinstance(node, Comment):
        return []
    if not isinstance(node, Tag):
        return []
    name = node.name.lower()
    if name in {"script", "style", "noscript", "svg", "canvas", "video", "audio", "button"}:
        return []
    if name in {"h1", "h2", "h3", "h4", "h5", "h6"}:
        level = int(name[1])
        text = inline_md(node)
        return [f"{'#' * min(level, 6)} {text}"] if text else []
    if name == "p":
        text = normalize_math(clean_text(node.get_text(" ", strip=True)))
        return [text] if text else []
    if name == "blockquote":
        lines = []
        for part in children_md(node):
            for line in part.splitlines():
                lines.append("> " + line)
        return ["\n".join(lines)] if lines else []
    if name in {"ul", "ol"}:
        ordered = name == "ol"
        out = []
        for idx, li in enumerate(node.find_all("li", recursive=False), 1):
            text = clean_text(li.get_text(" ", strip=True))
            if not text:
                continue
            prefix = f"{idx}. " if ordered else "- "
            lines = text.splitlines()
            out.append(prefix + lines[0])
            out.extend("  " + line for line in lines[1:])
        return out
    if name == "li":
        text = clean_text(node.get_text(" ", strip=True))
        return [text] if text else []
    if name == "table":
        rendered = table_md(node)
        return [rendered] if rendered else []
    if name in {"pre"}:
        text = node.get_text("\n", strip=True)
        return [f"```\n{text}\n```"] if text else []
    if name in {"img", "picture", "source"}:
        return []
    return children_md(node)


def children_md(node: Tag) -> list[str]:
    chunks: list[str] = []
    for child in node.children:
        if isinstance(child, Comment):
            continue
        if isinstance(child, NavigableString):
            text = clean_text(str(child))
            if text:
                chunks.append(text)
        elif isinstance(child, Tag):
            chunks.extend(block_md(child))
    return [chunk for chunk in chunks if chunk.strip()]


def extract_sections(soup: BeautifulSoup) -> tuple[list[Tag], list[Tag], Tag]:
    for comment in soup.find_all(string=lambda item: isinstance(item, Comment)):
        comment.extract()
    for selector in REMOVE_SELECTORS:
        for tag in soup.select(selector):
            tag.decompose()

    for tag in soup.find_all(True):
        if tag.attrs is None:
            continue
        classes = " ".join(tag.get("class", [])).lower()
        if any(token in classes for token in ["player", "dock", "deck", "ribbon", "topbar", "canvas", "widget"]):
            tag.decompose()

    side_sections: list[Tag] = []
    for selector in SIDE_SELECTORS:
        for tag in soup.select(selector):
            side_sections.append(tag.extract())

    main = soup.find("main") or soup.body or soup

    exec_sections: list[Tag] = []
    for selector in [
        "#summary",
        ".exec-summary",
        ".executive-summary",
        ".hero-side",
        ".summary-card",
    ]:
        for tag in main.select(selector):
            if tag in exec_sections:
                continue
            if "Executive Summary" in tag.get_text(" ", strip=True) or selector == "#summary":
                exec_sections.append(tag.extract())

    # Fallback: pull the first section containing an Executive Summary heading.
    if not exec_sections:
        for tag in main.find_all(["section", "div", "article"], recursive=True):
            if "Executive Summary" in tag.get_text(" ", strip=True)[:500]:
                exec_sections.append(tag.extract())
                break

    # Remove any remaining duplicated executive-summary cards from the body.
    for tag in list(main.find_all(["section", "div", "article"], recursive=True)):
        preview = tag.get_text(" ", strip=True)[:700]
        if "Executive Summary" in preview and tag not in exec_sections:
            tag.decompose()

    return exec_sections, side_sections, main


def clean_existing_markdown(text: str) -> str:
    text = clean_text(text)
    text = re.sub(r"(?s)^---.*?---\s*", "", text, count=1)
    text = re.sub(r"(?s)<!-- MEDIA_CALLOUT_START -->.*?<!-- MEDIA_CALLOUT_END -->", "", text)
    text = re.sub(r"(?s)`<style>.*?</style>`\{=html\}", "", text)
    text = re.sub(r"(?s)<style>.*?</style>", "", text)
    text = re.sub(r"(?s)<!--.*?-->", "", text)
    text = re.sub(r"(?m)^:{3,}.*$", "", text)
    text = re.sub(r"(?m)^:::.*$", "", text)
    text = re.sub(r"(?m)^::::.*$", "", text)
    text = re.sub(r"(?m)^> \[!.*$", "", text)
    text = re.sub(r"(?m)^<label>.*$", "", text)
    text = re.sub(r"(?m)^.*<input [^>]+>.*$", "", text)
    text = re.sub(r"(?m)^> - .*$", "", text)
    text = re.sub(r"(?im)^.*Series Navigation:.*$", "", text)
    text = re.sub(r"(?s)\*\*Primary Operation:\*\* TBD.*?\*\*Honest Blank:\*\* Structural map pending verification\.", "", text)
    for _ in range(5):
        text = re.sub(r"\[\[[^\n\]]*?\|([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", text)
    text = re.sub(r"\{#[^}]+\}", "", text)
    text = re.sub(r"\{\.[^}]+\}", "", text)
    text = re.sub(r"\{=[^}]+\}", "", text)
    text = re.sub(r"(?m)^> ?", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def fallback_markdown(article: Article) -> str | None:
    source = FALLBACK_MARKDOWN.get(article.filename)
    if not source or not source.exists():
        return None
    body = clean_existing_markdown(source.read_text(encoding="utf-8", errors="replace"))
    first_heading = re.search(r"(?m)^# .+$", body)
    if first_heading:
        body = body[first_heading.start() :]
    body = re.sub(r"^# .*$", "", body, count=1).strip()
    text = "\n\n".join(
        [
            f"# GTQ-{article.label}: {article.title}",
            "",
            f"Source HTML: `{article.filename}`",
            f"Fallback source: `{source.relative_to(ROOT)}`",
            "",
            "## Executive Summary",
            "_Executive summary not found in the live HTML. Kimi/content pass should add one._",
            "",
            "## Main Article",
            body,
        ]
    ).strip() + "\n"
    text = re.sub(r"(?m)^> - .*$", "", text)
    text = re.sub(r"(?m)^.*\[\[.*$", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def render_article(article: Article) -> str:
    html = (ROOT / article.filename).read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(html, "html.parser")
    exec_sections, side_sections, main = extract_sections(soup)

    title = article.title
    h1 = main.find("h1")
    if h1:
        candidate = clean_text(h1.get_text(" ", strip=True))
        if candidate:
            title = candidate

    parts = [
        f"# GTQ-{article.label}: {title}",
        "",
        f"Source HTML: `{article.filename}`",
        "",
        "## Executive Summary",
    ]

    exec_md: list[str] = []
    for tag in exec_sections:
        exec_md.extend(block_md(tag))
    if exec_md:
        seen_exec = set()
        deduped_exec = []
        for item in exec_md:
            key = re.sub(r"\W+", "", item).lower()
            if key and key not in seen_exec:
                seen_exec.add(key)
                deduped_exec.append(item)
        parts.extend(deduped_exec)
    else:
        parts.append("_Executive summary not found in the HTML. Kimi/content pass should add one._")

    parts.extend(["", "## Main Article"])
    body_md = children_md(main)
    # Drop repeated title at the start when it mirrors the file title.
    if body_md and body_md[0].lstrip("# ").strip().lower() == title.lower():
        body_md = body_md[1:]
    parts.extend(body_md)

    if side_sections:
        parts.extend(["", "## Supplemental Material"])
        for tag in side_sections:
            rendered = block_md(tag)
            if rendered:
                parts.extend(rendered)

    text = "\n\n".join(part for part in parts if part is not None)
    text = normalize_math(clean_text(text))
    drop_patterns = [
        r"(?im)^.*Continue to\s*The Paper.*$",
        r"(?im)^.*Series Navigation:.*$",
        r"(?im)^.*Tab bar.*$",
        r"(?im)^.*Tab \d+:.*$",
        r"(?im)^.*HERO IMAGE.*$",
        r"(?im)^.*END HERO IMAGE.*$",
        r"(?im)^.*LEFT COLUMN.*$",
        r"(?im)^.*RIGHT COLUMN.*$",
        r"(?im)^.*AUDIO DOCK.*$",
        r"(?im)^.*END AUDIO DOCK.*$",
        r"(?im)^.*slide \d+.*$",
    ]
    for pattern in drop_patterns:
        text = re.sub(pattern, "", text)
    text = re.sub(r"(?m)^> - .*$", "", text)
    text = re.sub(r"(?m)^.*\[\[.*$", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    words = len(re.findall(r"\b[\w'-]+\b", text))
    if words < 1000:
        fallback = fallback_markdown(article)
        if fallback:
            return fallback
    return text.strip() + "\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = ["# GTQ TTS Markdown Manifest", "", "Generated from the 26 canonical live HTML files.", ""]
    qa_rows = ["filename,words,html_fragments,has_exec_summary,source_type"]
    for article in ARTICLES:
        md = render_article(article)
        out_name = article.filename.replace(".html", ".md")
        (OUT / out_name).write_text(md, encoding="utf-8", newline="\n")
        html_fragments = len(re.findall(r"</?[a-zA-Z][^>]*>", md))
        words = len(re.findall(r"\b[\w'-]+\b", md))
        has_exec = "_Executive summary not found" not in md
        manifest.append(f"- GTQ-{article.label}: [{article.title}]({out_name})")
        source_type = "fallback-md" if "Fallback source:" in md else "html"
        qa_rows.append(f"{out_name},{words},{html_fragments},{has_exec},{source_type}")
    (OUT / "README.md").write_text("\n".join(manifest) + "\n", encoding="utf-8", newline="\n")
    (OUT / "_qa.csv").write_text("\n".join(qa_rows) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {len(ARTICLES)} markdown files to {OUT}")
    print(OUT / "_qa.csv")


if __name__ == "__main__":
    main()
