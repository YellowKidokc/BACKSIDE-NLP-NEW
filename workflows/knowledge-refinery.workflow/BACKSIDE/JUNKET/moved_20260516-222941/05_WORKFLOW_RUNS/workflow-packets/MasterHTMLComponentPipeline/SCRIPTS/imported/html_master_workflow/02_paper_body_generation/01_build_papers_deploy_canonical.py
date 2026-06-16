#!/usr/bin/env python3
"""
Build Theophysics Formal Papers — "Illuminated Codex" design.
Each paper: dramatic numeral watermark, unique accent color, pull-quote scripture,
glowing equation panels, floating TOC, reading progress bar.
"""

import re, os, html as htmlmod

PAPERS_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(PAPERS_DIR, "html")

PAPERS = [
    ("Paper_01_Gravitation_Grace_Sin.md",          "Gravitation & Grace"),
    ("Paper_02_Mass_Energy_Holy_Spirit.md",         "Mass-Energy & Holy Spirit"),
    ("Paper_03_Electromagnetism_Truth_Deception.md","Electromagnetism & Truth"),
    ("Paper_04_Strong_Force_Love_Addiction.md",     "Strong Force & Love"),
    ("Paper_05_Quantum_Faith_Doubt.md",             "Quantum & Faith"),
    ("Paper_06_Thermodynamics_Justice_Mercy.md",    "Thermodynamics & Justice"),
    ("Paper_07_Weak_Force_Redemption.md",           "Weak Force & Redemption"),
    ("Paper_08_Conservation_Laws_Righteousness.md", "Conservation & Righteousness"),
    ("Paper_09_Entropy_The_Adversary.md",           "Entropy & the Adversary"),
    ("Paper_10_Master_Integral_Christ_Coherence.md","Master Integral & Christ"),
]

# Each paper gets a unique accent from a curated spectrum
ACCENTS = [
    "#d4af37",  # 01 - classic gold (gravity/grace)
    "#e8c547",  # 02 - warm gold (energy/spirit)
    "#4a9eff",  # 03 - electric blue (electromagnetism/truth)
    "#ff6b6b",  # 04 - warm red (strong force/love)
    "#a78bfa",  # 05 - violet (quantum/faith)
    "#f59e0b",  # 06 - amber (thermodynamics/justice)
    "#2dd4a8",  # 07 - teal (weak force/redemption)
    "#60a5fa",  # 08 - sky blue (conservation/righteousness)
    "#ef4444",  # 09 - crimson (entropy/adversary)
    "#fbbf24",  # 10 - radiant gold (master integral/christ)
]

# Physics symbols for each paper's watermark
GLYPHS = ["G", "E", "c", "S", "ψ", "S", "W", "∮", "Ω", "χ"]

# Short taglines for each paper
TAGLINES = [
    "The curvature that guides home — or crushes into darkness.",
    "Spirit and Matter: two states of the same substance.",
    "Truth propagates at the speed of Christ.",
    "The paradox of freedom within commitment.",
    "The measurement operator that collapses divine potential.",
    "The inescapable accounting of every expenditure.",
    "Identity-level transformation — not repair, but transmutation.",
    "The universe keeps perfect books.",
    "Evil possesses no creative power — only the mathematics of disintegration.",
    "The one solution that remains stable across all parameters.",
]


def extract_metadata(md):
    lines = md.strip().split("\n")
    title = subtitle = abstract = ""
    body_start = 0
    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith("# ") and not s.startswith("## "):
            title = s[2:].strip()
        elif s.startswith("## ") and not subtitle:
            subtitle = s[3:].strip()
        elif s.startswith("**Abstract:**"):
            abstract = s.replace("**Abstract:**", "").strip()
            body_start = i + 1
            break
    body = "\n".join(lines[body_start:])
    body = re.sub(r"^\s*---\s*", "", body)
    return title, subtitle, abstract, body


def process_inline(text):
    # Display math
    text = re.sub(r"\$\$(.+?)\$\$", r'<span class="eq-display">\1</span>', text)
    # Inline math
    text = re.sub(r"\$([^$]+?)\$", r'<span class="eq">\1</span>', text)
    # Bold+italic
    text = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", text)
    # Bold
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # Italic
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)
    return text


def extract_scripture_refs(text):
    """Find scripture references like *John 6:44* or *Genesis 1:2* for pull-quote treatment."""
    pattern = r'\*([A-Z]\w+\s+\d+:\d+(?:-\d+)?)\*'
    return re.findall(pattern, text)


def md_to_sections(body_text):
    """Parse body into sections, each starting with ### header."""
    sections = []
    current_title = ""
    current_lines = []

    for line in body_text.strip().split("\n"):
        s = line.strip()
        if s.startswith("### "):
            if current_title or current_lines:
                sections.append((current_title, "\n".join(current_lines)))
            current_title = s[4:].strip()
            current_lines = []
        elif s == "---":
            continue
        elif s.startswith("*This is the") and s.endswith("*"):
            continue  # skip series footer
        else:
            current_lines.append(line)

    if current_title or current_lines:
        sections.append((current_title, "\n".join(current_lines)))

    return sections


def render_section_body(text):
    """Convert section body text to HTML paragraphs and lists."""
    lines = text.strip().split("\n")
    parts = []
    in_list = False
    list_type = "ul"

    for line in lines:
        s = line.strip()
        if not s:
            if in_list:
                parts.append(f"</{list_type}>")
                in_list = False
            continue

        if s.startswith("* ") or s.startswith("- "):
            if not in_list:
                list_type = "ul"
                parts.append("<ul>")
                in_list = True
            parts.append(f"<li>{process_inline(s[2:].strip())}</li>")
        elif re.match(r"^\d+\.\s+", s):
            if not in_list:
                list_type = "ol"
                parts.append("<ol>")
                in_list = True
            parts.append(f"<li>{process_inline(re.sub(r'^\\d+\\.\\s+', '', s))}</li>")
        else:
            if in_list:
                parts.append(f"</{list_type}>")
                in_list = False
            # Check if this paragraph contains a scripture quote — make it a pull-quote
            if re.search(r'\*"[^"]+"\*', s) or (re.search(r'\*[A-Z]\w+\s+\d+:\d+', s) and '"' in s):
                parts.append(f'<blockquote class="scripture">{process_inline(s)}</blockquote>')
            else:
                parts.append(f"<p>{process_inline(s)}</p>")

    if in_list:
        parts.append(f"</{list_type}>")

    return "\n                ".join(parts)


def generate_toc_items(sections):
    items = []
    for i, (title, _) in enumerate(sections):
        # Extract section number from title like "1. Introduction"
        num_match = re.match(r"(\d+)\.\s+(.*)", title)
        if num_match:
            num, name = num_match.groups()
            slug = f"section-{num}"
            items.append(f'<a href="#{slug}" class="toc-link"><span class="toc-num">{num}</span>{name}</a>')
    return "\n                ".join(items)


def generate_sections_html(sections, accent):
    parts = []
    for i, (title, body) in enumerate(sections):
        num_match = re.match(r"(\d+)\.\s+(.*)", title)
        if num_match:
            num, name = num_match.groups()
            slug = f"section-{num}"
        else:
            num = str(i + 1)
            name = title
            slug = f"section-{num}"

        body_html = render_section_body(body)
        parts.append(f'''
            <section class="paper-section" id="{slug}">
                <div class="section-marker">
                    <span class="marker-num" style="color: {accent}">{num}</span>
                    <span class="marker-line" style="background: {accent}"></span>
                </div>
                <h2 class="section-title">{name}</h2>
                <div class="section-body">
                {body_html}
                </div>
            </section>''')

    return "\n".join(parts)


def generate_paper_html(idx, md_text):
    num = f"{idx + 1:02d}"
    _, subtitle, abstract, body = extract_metadata(md_text)
    accent = ACCENTS[idx]
    glyph = GLYPHS[idx]
    tagline = TAGLINES[idx]
    nav_title = PAPERS[idx][1]

    sections = md_to_sections(body)
    toc_html = generate_toc_items(sections)
    sections_html = generate_sections_html(sections, accent)

    # Prev/next
    prev_link = ""
    next_link = ""
    if idx > 0:
        prev_link = f'<a href="paper_{idx:02d}.html" class="nav-arrow prev"><span class="arrow-icon">&larr;</span><span class="arrow-label">Paper {idx:02d}</span><span class="arrow-title">{PAPERS[idx-1][1]}</span></a>'
    if idx < 9:
        next_link = f'<a href="paper_{idx+2:02d}.html" class="nav-arrow next"><span class="arrow-icon">&rarr;</span><span class="arrow-label">Paper {idx+2:02d}</span><span class="arrow-title">{PAPERS[idx+1][1]}</span></a>'

    # Accent with transparency for backgrounds
    # Parse hex to rgb
    r_val = int(accent[1:3], 16)
    g_val = int(accent[3:5], 16)
    b_val = int(accent[5:7], 16)
    accent_rgb = f"{r_val}, {g_val}, {b_val}"

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Paper {num}: {subtitle} — Theophysics</title>
    <meta name="description" content="{htmlmod.escape(abstract[:160])}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
    <style>
        :root {{
            --accent: {accent};
            --accent-rgb: {accent_rgb};
            --bg: #0b1120;
            --bg-elevated: #0f1628;
            --bg-card: rgba(255, 255, 255, 0.025);
            --surface: #141d30;
            --text: #c8cdd8;
            --text-bright: #eef0f5;
            --text-dim: #6878a0;
            --border: rgba(255, 255, 255, 0.07);
            --border-accent: rgba(var(--accent-rgb), 0.2);
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        html {{ scroll-behavior: smooth; }}

        body {{
            font-family: 'Cormorant Garamond', Georgia, serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.85;
            font-size: 18px;
            overflow-x: hidden;
        }}

        /* === READING PROGRESS BAR === */
        .progress-bar {{
            position: fixed;
            top: 0;
            left: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--accent), rgba(var(--accent-rgb), 0.4));
            z-index: 1000;
            transition: width 0.1s linear;
            box-shadow: 0 0 12px rgba(var(--accent-rgb), 0.5);
        }}

        /* === TOP NAV === */
        .top-bar {{
            position: fixed;
            top: 3px;
            left: 0;
            right: 0;
            z-index: 900;
            padding: 0.75rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-family: 'Inter', sans-serif;
            font-size: 0.78rem;
            background: rgba(6, 8, 15, 0.85);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--border);
        }}

        .top-bar a {{
            color: var(--text-dim);
            text-decoration: none;
            transition: color 0.2s;
        }}
        .top-bar a:hover {{ color: var(--accent); }}

        .top-bar .brand {{ color: var(--accent); font-weight: 600; letter-spacing: 0.15em; text-transform: uppercase; font-size: 0.72rem; }}

        .paper-dots {{
            display: flex;
            gap: 0.5rem;
            align-items: center;
        }}

        .paper-dots a {{
            width: 28px;
            height: 28px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.7rem;
            font-weight: 500;
            border: 1px solid var(--border);
            transition: all 0.2s;
        }}

        .paper-dots a:hover {{
            border-color: var(--accent);
            color: var(--accent);
        }}

        .paper-dots a.current {{
            background: rgba(var(--accent-rgb), 0.15);
            border-color: var(--accent);
            color: var(--accent);
            font-weight: 600;
        }}

        /* === HERO === */
        .hero {{
            position: relative;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 8rem 4rem 4rem;
            overflow: hidden;
        }}

        .hero::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background:
                radial-gradient(ellipse 80% 60% at 70% 40%, rgba(var(--accent-rgb), 0.06), transparent),
                radial-gradient(ellipse 60% 50% at 20% 80%, rgba(var(--accent-rgb), 0.03), transparent);
            pointer-events: none;
        }}

        .hero-watermark {{
            position: absolute;
            right: -2%;
            top: 50%;
            transform: translateY(-50%);
            font-family: 'Cormorant Garamond', serif;
            font-size: clamp(18rem, 30vw, 28rem);
            font-weight: 300;
            color: rgba(var(--accent-rgb), 0.04);
            line-height: 1;
            pointer-events: none;
            user-select: none;
        }}

        .hero-content {{
            position: relative;
            max-width: 720px;
        }}

        .hero-eyebrow {{
            font-family: 'Inter', sans-serif;
            font-size: 0.72rem;
            letter-spacing: 0.3em;
            text-transform: uppercase;
            color: var(--accent);
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        }}

        .hero-eyebrow::before {{
            content: '';
            width: 40px;
            height: 1px;
            background: var(--accent);
        }}

        .hero-number {{
            font-family: 'Cormorant Garamond', serif;
            font-size: clamp(4rem, 8vw, 7rem);
            font-weight: 300;
            color: var(--text-bright);
            line-height: 0.9;
            margin-bottom: 0.5rem;
        }}

        .hero-title {{
            font-size: clamp(1.8rem, 3.5vw, 2.6rem);
            font-weight: 400;
            color: var(--text-bright);
            line-height: 1.2;
            margin-bottom: 1.5rem;
        }}

        .hero-tagline {{
            font-size: 1.15rem;
            font-style: italic;
            color: var(--text-dim);
            max-width: 560px;
            margin-bottom: 2.5rem;
        }}

        .hero-meta {{
            font-family: 'Inter', sans-serif;
            font-size: 0.78rem;
            color: var(--text-dim);
            display: flex;
            gap: 2rem;
            flex-wrap: wrap;
        }}

        .hero-meta span {{ display: flex; align-items: center; gap: 0.4rem; }}
        .meta-dot {{ width: 4px; height: 4px; border-radius: 50%; background: var(--accent); }}

        /* === ABSTRACT === */
        .abstract-band {{
            border-top: 1px solid var(--border);
            border-bottom: 1px solid var(--border);
            background: var(--bg-elevated);
        }}

        .abstract-inner {{
            max-width: 780px;
            margin: 0 auto;
            padding: 3rem 2rem;
        }}

        .abstract-label {{
            font-family: 'Inter', sans-serif;
            font-size: 0.68rem;
            letter-spacing: 0.3em;
            text-transform: uppercase;
            color: var(--accent);
            margin-bottom: 1rem;
        }}

        .abstract-text {{
            font-size: 1.05rem;
            line-height: 2;
            color: var(--text);
        }}

        /* === MAIN LAYOUT === */
        .main-layout {{
            display: grid;
            grid-template-columns: 200px 1fr;
            max-width: 1100px;
            margin: 0 auto;
            gap: 3rem;
            padding: 3rem 2rem;
        }}

        /* === FLOATING TOC === */
        .toc {{
            position: sticky;
            top: 5rem;
            height: fit-content;
            padding-top: 1rem;
        }}

        .toc-label {{
            font-family: 'Inter', sans-serif;
            font-size: 0.65rem;
            letter-spacing: 0.25em;
            text-transform: uppercase;
            color: var(--text-dim);
            margin-bottom: 1.25rem;
        }}

        .toc-link {{
            display: flex;
            align-items: baseline;
            gap: 0.65rem;
            padding: 0.45rem 0;
            color: var(--text-dim);
            text-decoration: none;
            font-family: 'Inter', sans-serif;
            font-size: 0.78rem;
            transition: all 0.2s;
            border-left: 2px solid transparent;
            padding-left: 0.75rem;
            margin-left: -0.75rem;
        }}

        .toc-link:hover {{
            color: var(--text-bright);
            border-left-color: rgba(var(--accent-rgb), 0.3);
        }}

        .toc-link.active {{
            color: var(--accent);
            border-left-color: var(--accent);
        }}

        .toc-num {{
            font-weight: 600;
            color: var(--accent);
            font-size: 0.7rem;
            min-width: 1rem;
        }}

        /* === PAPER SECTIONS === */
        .paper-content {{
            max-width: 720px;
        }}

        .paper-section {{
            margin-bottom: 4rem;
            scroll-margin-top: 5rem;
        }}

        .section-marker {{
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 0.75rem;
        }}

        .marker-num {{
            font-family: 'Inter', sans-serif;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.1em;
        }}

        .marker-line {{
            flex: 1;
            height: 1px;
            opacity: 0.3;
        }}

        .section-title {{
            font-size: 1.6rem;
            font-weight: 400;
            color: var(--text-bright);
            margin-bottom: 1.5rem;
        }}

        .section-body p {{
            margin-bottom: 1.4rem;
        }}

        .section-body strong {{
            color: var(--text-bright);
            font-weight: 600;
        }}

        .section-body em {{
            font-style: italic;
        }}

        .section-body ul, .section-body ol {{
            margin: 1rem 0 1.4rem 1.5rem;
        }}

        .section-body li {{
            margin-bottom: 0.6rem;
        }}

        /* === EQUATIONS === */
        .section-body .eq {{
            font-family: 'KaTeX_Math', 'Cormorant Garamond', serif;
            color: var(--accent);
            font-style: italic;
            padding: 0 0.1em;
        }}

        .section-body .eq-display {{
            display: block;
            text-align: center;
            margin: 2rem 0;
            padding: 1.75rem 2rem;
            font-family: 'JetBrains Mono', 'KaTeX_Math', monospace;
            color: var(--accent);
            font-style: normal;
            font-size: 1.05rem;
            background: linear-gradient(135deg, rgba(var(--accent-rgb), 0.06), rgba(var(--accent-rgb), 0.02));
            border: 1px solid rgba(var(--accent-rgb), 0.15);
            border-radius: 12px;
            position: relative;
            letter-spacing: 0.02em;
        }}

        .section-body .eq-display::before {{
            content: 'EQUATION';
            position: absolute;
            top: -0.55rem;
            left: 1.5rem;
            font-family: 'Inter', sans-serif;
            font-size: 0.6rem;
            letter-spacing: 0.2em;
            color: var(--accent);
            background: var(--bg);
            padding: 0 0.6rem;
            font-style: normal;
            font-weight: 500;
        }}

        /* === SCRIPTURE PULL-QUOTES === */
        .scripture {{
            position: relative;
            margin: 2.5rem 0;
            padding: 2rem 2rem 2rem 2.5rem;
            background: linear-gradient(135deg, rgba(var(--accent-rgb), 0.04), rgba(var(--accent-rgb), 0.01));
            border-left: 3px solid rgba(var(--accent-rgb), 0.5);
            border-radius: 0 16px 16px 0;
            font-style: italic;
            font-size: 1.05rem;
            color: var(--text);
            line-height: 2;
        }}

        .scripture::before {{
            content: '\\201C';
            position: absolute;
            top: 0.25rem;
            left: 0.75rem;
            font-size: 3rem;
            color: rgba(var(--accent-rgb), 0.2);
            font-family: 'Cormorant Garamond', serif;
            line-height: 1;
        }}

        .scripture em {{
            color: var(--text-bright);
        }}

        /* === BOTTOM NAV === */
        .paper-nav {{
            display: flex;
            justify-content: space-between;
            align-items: stretch;
            max-width: 1100px;
            margin: 0 auto;
            padding: 0 2rem 4rem;
            gap: 1.5rem;
        }}

        .nav-arrow {{
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
            padding: 1.5rem 2rem;
            border: 1px solid var(--border);
            border-radius: 16px;
            text-decoration: none;
            color: var(--text-dim);
            transition: all 0.3s;
            flex: 1;
            max-width: 45%;
            background: var(--bg-card);
        }}

        .nav-arrow:hover {{
            border-color: rgba(var(--accent-rgb), 0.3);
            background: rgba(var(--accent-rgb), 0.03);
        }}

        .nav-arrow .arrow-icon {{
            font-size: 1.5rem;
            color: var(--accent);
            font-family: 'Inter', sans-serif;
        }}

        .nav-arrow .arrow-label {{
            font-family: 'Inter', sans-serif;
            font-size: 0.7rem;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            color: var(--text-dim);
        }}

        .nav-arrow .arrow-title {{
            font-size: 1rem;
            color: var(--text-bright);
        }}

        .nav-arrow.next {{
            text-align: right;
            margin-left: auto;
        }}

        /* === FOOTER === */
        .site-footer {{
            text-align: center;
            padding: 3rem 2rem;
            border-top: 1px solid var(--border);
            font-family: 'Inter', sans-serif;
            font-size: 0.78rem;
            color: var(--text-dim);
        }}

        .site-footer a {{
            color: var(--accent);
            text-decoration: none;
        }}

        .footer-dots {{
            display: flex;
            justify-content: center;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }}

        .footer-dot {{
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: var(--border);
        }}

        .footer-dot.active {{
            background: var(--accent);
            box-shadow: 0 0 8px rgba(var(--accent-rgb), 0.4);
        }}

        /* === RESPONSIVE === */
        @media (max-width: 900px) {{
            .main-layout {{
                grid-template-columns: 1fr;
            }}
            .toc {{
                display: none;
            }}
            .hero {{
                padding: 7rem 1.5rem 3rem;
            }}
            .paper-nav {{
                flex-direction: column;
            }}
            .nav-arrow {{
                max-width: 100%;
            }}
            .paper-dots {{
                display: none;
            }}
        }}

        @media (max-width: 600px) {{
            body {{ font-size: 16px; }}
            .hero-number {{ font-size: 4rem; }}
            .hero-watermark {{ font-size: 14rem; }}
            .abstract-inner {{ padding: 2rem 1.25rem; }}
        }}
    </style>
</head>
<body>

<div class="progress-bar" id="progress"></div>

<nav class="top-bar">
    <a href="index.html" class="brand">Theophysics</a>
    <div class="paper-dots">
        {"".join(f'<a href="paper_{i+1:02d}.html" class="{"current" if i == idx else ""}">{i+1}</a>' for i in range(10))}
    </div>
</nav>

<header class="hero">
    <div class="hero-watermark">{glyph}</div>
    <div class="hero-content">
        <div class="hero-eyebrow">Algorithmic Foundations of Reality</div>
        <div class="hero-number">{num}.</div>
        <h1 class="hero-title">{process_inline(subtitle)}</h1>
        <p class="hero-tagline">{tagline}</p>
        <div class="hero-meta">
            <span><span class="meta-dot"></span> David Lowe (POF 2828)</span>
            <span><span class="meta-dot"></span> Paper {num} of 10</span>
            <span><span class="meta-dot"></span> faiththruphysics.com</span>
        </div>
    </div>
</header>

<section class="abstract-band">
    <div class="abstract-inner">
        <div class="abstract-label">Abstract</div>
        <p class="abstract-text">{process_inline(abstract)}</p>
    </div>
</section>

<div class="main-layout">
    <aside class="toc">
        <div class="toc-label">Contents</div>
        {toc_html}
    </aside>

    <article class="paper-content">
        {sections_html}
    </article>
</div>

<nav class="paper-nav">
    {prev_link}
    {next_link}
</nav>

<footer class="site-footer">
    <div class="footer-dots">
        {"".join(f'<span class="footer-dot {"active" if i == idx else ""}"></span>' for i in range(10))}
    </div>
    <p>&#10013; <a href="https://faiththruphysics.com">Theophysics</a> — David Lowe (POF 2828)</p>
    <p style="margin-top: 0.35rem; opacity: 0.6;">The Algorithmic Foundations of Reality</p>
</footer>

<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
    onload="initKatex()"></script>
<script>
// Reading progress bar
window.addEventListener('scroll', () => {{
    const h = document.documentElement;
    const pct = (h.scrollTop / (h.scrollHeight - h.clientHeight)) * 100;
    document.getElementById('progress').style.width = pct + '%';
}});

// TOC active state
const sections = document.querySelectorAll('.paper-section');
const tocLinks = document.querySelectorAll('.toc-link');
const observer = new IntersectionObserver(entries => {{
    entries.forEach(entry => {{
        if (entry.isIntersecting) {{
            tocLinks.forEach(l => l.classList.remove('active'));
            const id = entry.target.id;
            const active = document.querySelector(`.toc-link[href="#${{id}}"]`);
            if (active) active.classList.add('active');
        }}
    }});
}}, {{ rootMargin: '-20% 0px -70% 0px' }});
sections.forEach(s => observer.observe(s));

// KaTeX rendering
function initKatex() {{
    document.querySelectorAll('.eq').forEach(el => {{
        try {{ katex.render(el.textContent, el, {{ throwOnError: false }}); }} catch(e) {{}}
    }});
    document.querySelectorAll('.eq-display').forEach(el => {{
        try {{ katex.render(el.textContent, el, {{ displayMode: true, throwOnError: false }}); }} catch(e) {{}}
    }});
}}
</script>

</body>
</html>'''


def generate_index_html():
    cards = []
    for i, (filename, nav_title) in enumerate(PAPERS):
        num = f"{i+1:02d}"
        accent = ACCENTS[i]
        glyph = GLYPHS[i]
        tagline = TAGLINES[i]

        filepath = os.path.join(PAPERS_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            md = f.read()
        _, subtitle, abstract, _ = extract_metadata(md)

        r_val = int(accent[1:3], 16)
        g_val = int(accent[3:5], 16)
        b_val = int(accent[5:7], 16)

        cards.append(f'''
            <a href="paper_{num}.html" class="index-card" style="--card-accent: {accent}; --card-rgb: {r_val}, {g_val}, {b_val};">
                <div class="card-watermark">{glyph}</div>
                <div class="card-number">{num}</div>
                <h2 class="card-title">{subtitle}</h2>
                <p class="card-tagline">{tagline}</p>
                <div class="card-footer">
                    <span class="card-type">{nav_title}</span>
                    <span class="card-arrow">&rarr;</span>
                </div>
            </a>''')

    cards_html = "\n".join(cards)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Algorithmic Foundations of Reality — Theophysics</title>
    <meta name="description" content="A 10-paper series mapping the fundamental forces of physics to the structural invariants of theological reality.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #0b1120;
            --bg-elevated: #0f1628;
            --text: #c8cdd8;
            --text-bright: #eef0f5;
            --text-dim: #6878a0;
            --border: rgba(255, 255, 255, 0.07);
            --gold: #d4af37;
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html {{ scroll-behavior: smooth; }}

        body {{
            font-family: 'Cormorant Garamond', Georgia, serif;
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
            line-height: 1.7;
        }}

        .top-bar {{
            padding: 1.25rem 2rem;
            display: flex;
            justify-content: center;
            border-bottom: 1px solid var(--border);
            font-family: 'Inter', sans-serif;
        }}

        .top-bar a {{
            color: var(--gold);
            text-decoration: none;
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 0.25em;
            text-transform: uppercase;
        }}

        .index-hero {{
            max-width: 800px;
            margin: 0 auto;
            padding: 6rem 2rem 2rem;
            text-align: center;
        }}

        .index-hero .series-line {{
            font-family: 'Inter', sans-serif;
            font-size: 0.68rem;
            letter-spacing: 0.35em;
            text-transform: uppercase;
            color: var(--text-dim);
            margin-bottom: 2rem;
        }}

        .index-hero h1 {{
            font-size: clamp(2.2rem, 5vw, 3.6rem);
            font-weight: 300;
            color: var(--text-bright);
            line-height: 1.15;
            margin-bottom: 1.25rem;
        }}

        .index-hero .subtitle {{
            font-size: 1.15rem;
            font-style: italic;
            color: var(--text-dim);
            max-width: 580px;
            margin: 0 auto 1.5rem;
        }}

        .index-hero .author {{
            font-family: 'Inter', sans-serif;
            font-size: 0.78rem;
            color: var(--gold);
            letter-spacing: 0.1em;
        }}

        .divider {{
            max-width: 200px;
            margin: 3rem auto;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--gold), transparent);
            opacity: 0.3;
        }}

        .index-grid {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 0 2rem 4rem;
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1.25rem;
        }}

        .index-card {{
            position: relative;
            display: flex;
            flex-direction: column;
            padding: 2rem;
            border: 1px solid var(--border);
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.015);
            text-decoration: none;
            color: inherit;
            overflow: hidden;
            transition: all 0.35s ease;
        }}

        .index-card:hover {{
            border-color: rgba(var(--card-rgb), 0.25);
            background: rgba(var(--card-rgb), 0.03);
            transform: translateY(-2px);
        }}

        .card-watermark {{
            position: absolute;
            right: -0.5rem;
            top: -1rem;
            font-size: 8rem;
            font-weight: 300;
            color: rgba(var(--card-rgb), 0.05);
            pointer-events: none;
            line-height: 1;
        }}

        .card-number {{
            font-family: 'Inter', sans-serif;
            font-size: 0.7rem;
            font-weight: 600;
            color: var(--card-accent);
            letter-spacing: 0.15em;
            margin-bottom: 0.75rem;
        }}

        .card-title {{
            font-size: 1.3rem;
            font-weight: 400;
            color: var(--text-bright);
            margin-bottom: 0.65rem;
            line-height: 1.3;
            position: relative;
        }}

        .card-tagline {{
            font-size: 0.92rem;
            color: var(--text-dim);
            font-style: italic;
            flex: 1;
            margin-bottom: 1.25rem;
        }}

        .card-footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-top: 1rem;
            border-top: 1px solid var(--border);
            font-family: 'Inter', sans-serif;
            font-size: 0.75rem;
        }}

        .card-type {{ color: var(--text-dim); }}
        .card-arrow {{
            color: var(--card-accent);
            font-size: 1.1rem;
            transition: transform 0.2s;
        }}
        .index-card:hover .card-arrow {{ transform: translateX(4px); }}

        /* Special treatment for Paper 10 — full width */
        .index-card:last-child {{
            grid-column: 1 / -1;
        }}

        .site-footer {{
            text-align: center;
            padding: 3rem 2rem;
            border-top: 1px solid var(--border);
            font-family: 'Inter', sans-serif;
            font-size: 0.78rem;
            color: var(--text-dim);
        }}

        .site-footer a {{
            color: var(--gold);
            text-decoration: none;
        }}

        @media (max-width: 700px) {{
            .index-grid {{
                grid-template-columns: 1fr;
                padding: 0 1.25rem 3rem;
            }}
            .index-hero {{ padding: 4rem 1.25rem 1.5rem; }}
        }}
    </style>
</head>
<body>

<nav class="top-bar">
    <a href="https://faiththruphysics.com">Theophysics</a>
</nav>

<header class="index-hero">
    <div class="series-line">A 10-Paper Series</div>
    <h1>The Algorithmic Foundations of Reality</h1>
    <p class="subtitle">A rigorous mapping between the fundamental forces of physics and the structural invariants of theological reality.</p>
    <p class="author">David Lowe (POF 2828)</p>
</header>

<div class="divider"></div>

<section class="index-grid">
    {cards_html}
</section>

<footer class="site-footer">
    <p>&#10013; <a href="https://faiththruphysics.com">Theophysics</a> — David Lowe (POF 2828)</p>
</footer>

</body>
</html>'''


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    for i, (filename, nav_title) in enumerate(PAPERS):
        filepath = os.path.join(PAPERS_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            md_text = f.read()
        html = generate_paper_html(i, md_text)
        out_name = f"paper_{i+1:02d}.html"
        with open(os.path.join(OUT_DIR, out_name), "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  {out_name}: {nav_title}")

    index = generate_index_html()
    with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index)
    print("  index.html")

    print(f"\nAll files -> {OUT_DIR}")


if __name__ == "__main__":
    main()
