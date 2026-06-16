from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


ARTICLES = [
    ("01", "gtq-01-measurement-collapsed-reality.html", "The Measurement That Collapsed Reality", "main"),
    ("01A", "gtq-01a-collapse-threshold.html", "The Collapse Threshold", "deep"),
    ("02", "gtq-02-the-first-quantum-state.html", "The First Quantum State", "main"),
    ("03", "gtq-03-free-will-two-frames.html", "Free Will in Two Frames", "main"),
    ("03A", "gtq-03a-macarthur-and-the-equation.html", "MacArthur and the Equation", "deep"),
    ("03B", "gtq-03b-the-three-pathways.html", "The Three Pathways", "deep"),
    ("03C", "gtq-03c-why-god-drowned-everybody.html", "Why God Drowned Everybody", "deep"),
    ("04", "gtq-04-the-day-time-began.html", "The Day Time Began", "main"),
    ("04A", "gtq-04a-the-decoherence-curve.html", "The Decoherence Curve", "deep"),
    ("04B", "gtq-04b-how-lies-kill.html", "How Lies Kill", "deep"),
    ("05", "gtq-05-the-substrate-fractured.html", "The Substrate Fractured", "main"),
    ("05A", "gtq-05a-trinity-mechanism.html", "The Trinity Mechanism", "deep"),
    ("05B", "gtq-05b-trinity-timeline.html", "The Trinity Timeline", "deep"),
    ("05C", "gtq-05c-why-physics-is-broken-in-two.html", "Why Physics Is Broken in Two", "deep"),
    ("06", "gtq-06-why-reality-needs-three.html", "Why Reality Needs Three", "main"),
    ("07", "gtq-07-the-photon-isnt-watching.html", "The Photon Isn't Watching You Back", "main"),
    ("07A", "gtq-07a-empirical-testing.html", "We Actually Ran the Numbers", "deep"),
    ("08", "gtq-08-god-doesnt-need-a-clock.html", "God Doesn't Need a Clock", "main"),
    ("08A", "gtq-08a-the-temporal-trap.html", "The Temporal Trap", "deep"),
    ("08B", "gtq-08b-how-god-restores.html", "How God Restores", "deep"),
    ("08C", "gtq-08c-science-behind-restoration.html", "The Science Behind Restoration", "deep"),
    ("09", "gtq-09-same-god-both-testaments.html", "The Same God in Both Testaments", "main"),
    ("09A", "gtq-09a-regime-dependent-theology.html", "Regime-Dependent Theology", "deep"),
    ("09B", "gtq-09b-civilizational-decay.html", "Civilizational Decay", "deep"),
    ("10", "gtq-10-the-counter-move.html", "The Counter-Move", "main"),
    ("10A", "gtq-10a-why-the-pattern-is-the-signal.html", "Why the Pattern Is the Signal", "deep"),
]


LINK_MAP = {
    "gtq-02-collapse-threshold.html": "gtq-01a-collapse-threshold.html",
    "gtq-03-first-quantum-state.html": "gtq-02-the-first-quantum-state.html",
    "gtq-04-free-will-two-frames.html": "gtq-03-free-will-two-frames.html",
    "gtq-05-macarthur-equation.html": "gtq-03a-macarthur-and-the-equation.html",
    "gtq-05-macarthur-and-the-equation.html": "gtq-03a-macarthur-and-the-equation.html",
    "gtq-06-three-pathways.html": "gtq-03b-the-three-pathways.html",
    "gtq-07-why-god-drowned-everybody.html": "gtq-03c-why-god-drowned-everybody.html",
    "gtq-08-day-time-began.html": "gtq-04-the-day-time-began.html",
    "gtq-09-decoherence-curve.html": "gtq-04a-the-decoherence-curve.html",
    "gtq-10-how-lies-kill.html": "gtq-04b-how-lies-kill.html",
    "gtq-11-substrate-fractured.html": "gtq-05-the-substrate-fractured.html",
    "gtq-12-trinity-mechanism.html": "gtq-05a-trinity-mechanism.html",
    "gtq-13-trinity-timeline.html": "gtq-05b-trinity-timeline.html",
    "gtq-14-physics-broken-in-two.html": "gtq-05c-why-physics-is-broken-in-two.html",
    "gtq-15-reality-needs-three.html": "gtq-06-why-reality-needs-three.html",
    "gtq-15-why-reality-needs-three.html": "gtq-06-why-reality-needs-three.html",
    "gtq-16-photon-isnt-watching.html": "gtq-07-the-photon-isnt-watching.html",
    "gtq-17-ran-the-numbers.html": "gtq-07a-empirical-testing.html",
    "gtq-18-eraser-and-cross.html": "gtq-08-god-doesnt-need-a-clock.html",
    "gtq-18-eraser-and-the-cross.html": "gtq-08-god-doesnt-need-a-clock.html",
    "gtq-19-temporal-trap.html": "gtq-08a-the-temporal-trap.html",
    "gtq-20-how-god-restores.html": "gtq-08b-how-god-restores.html",
    "gtq-21-science-behind-restoration.html": "gtq-08c-science-behind-restoration.html",
    "gtq-22-same-god-both-testaments.html": "gtq-09-same-god-both-testaments.html",
    "gtq-23-regime-dependent-theology.html": "gtq-09a-regime-dependent-theology.html",
    "gtq-24-societies-die.html": "gtq-09b-civilizational-decay.html",
    "gtq-24-societies-die-same-way.html": "gtq-09b-civilizational-decay.html",
    "gtq-25-counter-move.html": "gtq-10-the-counter-move.html",
    "gtq-26-pattern-is-the-signal.html": "gtq-10a-why-the-pattern-is-the-signal.html",
}

ABSOLUTE_GTQ_PREFIX = "/genesis-to-quantum/"

POSTER_MAP = {
    "images/gtq-05c.webp": "images/gtq-05.webp",
    "images/gtq-08c.webp": "images/gtq-08.webp",
    "images/gtq-09a.webp": "images/gtq-09.webp",
    "images/gtq-09b.webp": "images/gtq-09.webp",
    "images/gtq-10a.webp": "images/gtq-10.webp",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="")


def sidebar_for(current_file: str, tag: str = "nav") -> str:
    end_tag = f"</{tag}>"
    lines = [
        f'<{tag} class="sidebar" id="sidebar">',
        '  <div class="series-title"><i class="fas fa-atom" style="margin-right:.4rem;"></i> Genesis to Quantum</div>',
        '  <a href="index.html"><i class="fas fa-home" style="width:1.2rem;"></i> Series Home</a>',
        "",
        '  <div class="nav-section">Main Articles</div>',
    ]
    for label, filename, title, kind in ARTICLES:
        if kind != "main":
            continue
        current = " current active" if filename == current_file else ""
        lines.append(f'  <a href="{filename}" class="main-article{current}">{label} {title}</a>')

    lines.extend(["", '  <div class="nav-section">Deep Dives</div>'])
    for label, filename, title, kind in ARTICLES:
        if kind != "deep":
            continue
        current = " current active" if filename == current_file else ""
        lines.append(f'  <a href="{filename}" class="deep-dive{current}">{label} {title}</a>')

    lines.extend(
        [
            "",
            '  <div class="nav-section">Formal Proofs</div>',
            '  <a href="iso/iso-001-gravity-sin.html" class="deep-dive">ISO-001: Gravity - Sin</a>',
            '  <a href="iso/iso-003-collapse-fall.html" class="deep-dive">ISO-003: Collapse - The Fall</a>',
            '  <a href="iso/iso-009-entropy-wages-sin.html" class="deep-dive">ISO-009: Entropy - Wages of Sin</a>',
            end_tag,
        ]
    )
    return "\n".join(lines)


def bottom_nav_for(index: int) -> str:
    label, _filename, _title, _kind = ARTICLES[index]
    prev = ARTICLES[index - 1] if index > 0 else None
    nxt = ARTICLES[index + 1] if index < len(ARTICLES) - 1 else None

    prev_html = (
        f'<a href="{prev[1]}"><i class="fas fa-arrow-left"></i>Previous: {prev[2]}</a>'
        if prev
        else '<span class="nav-disabled"><i class="fas fa-arrow-left"></i>Series opener - no previous</span>'
    )
    next_html = (
        f'<a href="{nxt[1]}" class="primary">Next: {nxt[2]}<i class="fas fa-arrow-right"></i></a>'
        if nxt
        else '<span class="nav-disabled">Series complete<i class="fas fa-arrow-right"></i></span>'
    )
    return "\n".join(
        [
            '<div class="bottom-nav">',
            f"    {prev_html}",
            f'    <div class="nav-center">Article {index + 1} of {len(ARTICLES)} &middot; GTQ-{label}</div>',
            f"    {next_html}",
            "  </div>",
        ]
    )


def bottom_section_for(index: int) -> str:
    return "\n".join(
        [
            "<!-- BOTTOM NAVIGATION -->",
            '<div class="container mx-auto px-6" style="padding-left:4.5rem;">',
            f"  {bottom_nav_for(index)}",
            "</div>",
            "",
        ]
    )


def replace_first_div_block(text: str, class_name: str, replacement: str) -> str:
    match = re.search(rf'<div class="{re.escape(class_name)}"[^>]*>', text)
    if not match:
        return text
    depth = 1
    token_re = re.compile(r"</?div\b[^>]*>", re.I)
    for token in token_re.finditer(text, match.end()):
        if token.group(0).lower().startswith("</div"):
            depth -= 1
        else:
            depth += 1
        if depth == 0:
            return text[: match.start()] + replacement + text[token.end() :]
    return text


def update_article(path: Path, index: int) -> bool:
    text = read(path)
    original = text
    for old, new in LINK_MAP.items():
        text = text.replace(old, new)
    for old, new in POSTER_MAP.items():
        text = text.replace(old, new)
    text = text.replace(ABSOLUTE_GTQ_PREFIX, "")
    text = text.replace('href="/index.html"', 'href="index.html"')

    if '<nav class="sidebar" id="sidebar">' in text:
        text = re.sub(
            r'<nav class="sidebar" id="sidebar">.*?</nav>',
            sidebar_for(path.name, "nav"),
            text,
            count=1,
            flags=re.S,
        )
    elif '<aside class="sidebar" id="sidebar">' in text:
        text = re.sub(
            r'<aside class="sidebar" id="sidebar">.*?</aside>',
            sidebar_for(path.name, "aside"),
            text,
            count=1,
            flags=re.S,
        )
    elif 'class="sidebar"' not in text and '<body' in text:
        injected = "\n".join(
            [
                '<button class="sidebar-toggle" onclick="document.querySelector(\'.sidebar\').classList.toggle(\'open\')" aria-label="Toggle series navigation"><i class="fas fa-bars"></i></button>',
                sidebar_for(path.name, "aside"),
                "",
            ]
        )
        text = re.sub(r"(<body[^>]*>)", r"\1\n" + injected, text, count=1, flags=re.S)

    if "<!-- BOTTOM NAVIGATION -->" in text and "<!-- FOOTER -->" in text:
        text = re.sub(
            r"<!-- BOTTOM NAVIGATION -->.*?(?=<!-- FOOTER -->)",
            bottom_section_for(index),
            text,
            count=1,
            flags=re.S,
        )
    elif '<nav class="bottom-nav">' in text:
        text = re.sub(
            r'<nav class="bottom-nav">.*?</nav>',
            bottom_nav_for(index),
            text,
            count=1,
            flags=re.S,
        )
    else:
        text = replace_first_div_block(text, "bottom-nav", bottom_nav_for(index))

    text = re.sub(
        r'(<div class="bottom-nav">.*?</div>)</div>(\s*<script>)',
        r"\1\2",
        text,
        count=1,
        flags=re.S,
    )
    if 'class="bottom-nav"' not in text:
        block = bottom_nav_for(index) + "\n\n"
        if "<footer" in text:
            text = text.replace("<footer", block + "<footer", 1)
        elif "</body>" in text:
            text = text.replace("</body>", block + "</body>", 1)
    text = re.sub(
        r"David Lowe &middot; Genesis to Quantum &middot; Article [^<]+",
        f"David Lowe &middot; Genesis to Quantum &middot; Article {index + 1} of {len(ARTICLES)}",
        text,
        count=1,
    )
    if text != original:
        write(path, text)
        return True
    return False


def remove_variants_from_index() -> bool:
    path = ROOT / "index.html"
    text = read(path)
    original = text
    for old, new in LINK_MAP.items():
        text = text.replace(old, new)
    text = re.sub(
        r'\n<section style="max-width:760px;margin:0 auto;padding:1rem 2rem 0;">\s*<a href="bridges\.html".*?</section>\s*',
        "\n",
        text,
        count=1,
        flags=re.S,
    )
    text = re.sub(
        r"\n<hr class=\"divider\"/>\s*<!--\s+.*?VARIANTS / IN PROGRESS.*?</section>\s*",
        "\n",
        text,
        count=1,
        flags=re.S,
    )
    if text != original:
        write(path, text)
        return True
    return False


def update_index_gtq() -> bool:
    path = ROOT / "index-gtq.html"
    if not path.exists():
        return False
    text = read(path)
    original = text
    for old, new in LINK_MAP.items():
        text = text.replace(old, new)
    text = text.replace("../index.html", "index.html")
    if text != original:
        write(path, text)
        return True
    return False


def main() -> None:
    changed = []
    for index, (_label, filename, _title, _kind) in enumerate(ARTICLES):
        path = ROOT / filename
        if not path.exists():
            raise FileNotFoundError(path)
        if update_article(path, index):
            changed.append(filename)
    if remove_variants_from_index():
        changed.append("index.html")
    if update_index_gtq():
        changed.append("index-gtq.html")
    print(f"updated {len(changed)} files")
    for name in changed:
        print(f"  {name}")


if __name__ == "__main__":
    main()
