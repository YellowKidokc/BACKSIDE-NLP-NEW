#!/usr/bin/env python3
"""
combine_html.py — MDA Three-Lane HTML Combiner

Takes Standard + Academic + Easy markdown + two-lane math report
and produces a single production HTML with reader-mode tabs.

Usage:
    python combine_html.py MDA-013-peak-coherence-1940
    python combine_html.py --all
    python combine_html.py MDA-013-peak-coherence-1940 --outdir X:/WORKFLOWS/MDA-PUBLICATION/06_HTML_BUILD

Expects directory layout:
    01_LOSSLESS/articles/{slug}.md          → Standard
    05_READING_LEVELS/{slug}_ACADEMIC.md    → Academic
    05_READING_LEVELS/{slug}_EASY.md        → Easy
    05_READING_LEVELS/{slug}_TERM_INVENTORY.json → Terms
    [optional] two-lane report path via --math-dir
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime
from textwrap import dedent

try:
    import markdown as md_lib
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False

SCRIPT_DIR = Path(__file__).parent
LOSSLESS = SCRIPT_DIR / "01_LOSSLESS" / "articles"
READING_LEVELS = SCRIPT_DIR / "05_READING_LEVELS"
DEFAULT_OUT = SCRIPT_DIR / "06_HTML_BUILD"


# ─────────────────────────────────────────────
#  Markdown → HTML conversion
# ─────────────────────────────────────────────

def md_to_html(text: str) -> str:
    """Convert markdown to HTML. Uses python-markdown if available, else simple regex."""
    # Strip YAML frontmatter
    text = re.sub(r'^---\n.*?\n---\n', '', text, count=1, flags=re.DOTALL)
    # Strip nav lines (← Prev, Next →, etc.)
    text = re.sub(r'^\[←.*?\]\(.*?\)\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\[Next.*?\]\(.*?\)\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\|$', '', text, flags=re.MULTILINE)

    if HAS_MARKDOWN:
        return md_lib.markdown(text, extensions=['tables', 'fenced_code'])

    # Minimal fallback converter
    lines = text.split('\n')
    html_parts = []
    in_table = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_table:
                html_parts.append('</table>')
                in_table = False
            html_parts.append('')
            continue
        # Headings
        if stripped.startswith('######'):
            html_parts.append(f'<h6>{stripped[6:].strip()}</h6>')
        elif stripped.startswith('#####'):
            html_parts.append(f'<h5>{stripped[5:].strip()}</h5>')
        elif stripped.startswith('####'):
            html_parts.append(f'<h4>{stripped[4:].strip()}</h4>')
        elif stripped.startswith('###'):
            html_parts.append(f'<h3>{stripped[3:].strip()}</h3>')
        elif stripped.startswith('##'):
            html_parts.append(f'<h2>{stripped[2:].strip()}</h2>')
        elif stripped.startswith('#'):
            html_parts.append(f'<h1>{stripped[1:].strip()}</h1>')
        # Table rows
        elif '|' in stripped and stripped.startswith('|'):
            cells = [c.strip() for c in stripped.split('|')[1:-1]]
            if all(re.match(r'^[-:]+$', c) for c in cells):
                continue  # separator row
            if not in_table:
                html_parts.append('<table class="mda-table">')
                in_table = True
            row = ''.join(f'<td>{c}</td>' for c in cells)
            html_parts.append(f'<tr>{row}</tr>')
        # Blockquotes
        elif stripped.startswith('>'):
            html_parts.append(f'<blockquote><p>{stripped[1:].strip()}</p></blockquote>')
        # Images
        elif stripped.startswith('!['):
            m = re.match(r'!\[(.*?)\]\((.*?)\)', stripped)
            if m:
                html_parts.append(f'<img src="{m.group(2)}" alt="{m.group(1)}" class="article-img"/>')
        # Regular paragraph
        else:
            # Bold/italic
            s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', stripped)
            s = re.sub(r'\*(.+?)\*', r'<em>\1</em>', s)
            html_parts.append(f'<p>{s}</p>')
    if in_table:
        html_parts.append('</table>')
    return '\n'.join(html_parts)


# ─────────────────────────────────────────────
#  Section splitting for paragraph alignment
# ─────────────────────────────────────────────

def split_sections(html: str) -> list[dict]:
    """Split HTML into sections by h1/h2 headings. Returns [{heading, content}]."""
    parts = re.split(r'(<h[12][^>]*>.*?</h[12]>)', html)
    sections = []
    current = {"heading": "", "content": ""}
    for part in parts:
        if re.match(r'<h[12]', part):
            if current["content"].strip() or current["heading"]:
                sections.append(current)
            current = {"heading": part, "content": ""}
        else:
            current["content"] += part
    if current["content"].strip() or current["heading"]:
        sections.append(current)
    return sections


def extract_title(md_text: str) -> str:
    """Extract title from markdown frontmatter or first h1."""
    m = re.search(r'^title:\s*"?(.+?)"?\s*$', md_text, re.MULTILINE)
    if m:
        title = m.group(1).strip().strip('"')
        # Clean up scrape artifacts like "Title () -- subtitle"
        title = re.sub(r'\s*\(\)\s*', ' ', title)
        title = re.sub(r'\s*--\s*', ' — ', title)
        title = re.sub(r'\s{2,}', ' ', title).strip()
        return title
    m = re.search(r'^#\s+(.+)$', md_text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return "Untitled"


def extract_slug_number(slug: str) -> str:
    """Extract MDA number like '013' from slug."""
    m = re.match(r'MDA-(\d+)', slug)
    return m.group(1) if m else "000"


def load_math_report(math_dir: Path | None, slug: str) -> str:
    """Load two-lane math report if available."""
    if not math_dir:
        return ""
    report = math_dir / f"{slug}_TWO_LANE_REPORT.md"
    if report.exists():
        return report.read_text(encoding="utf-8", errors="replace")
    return ""


def parse_math_for_proof_panel(math_report: str) -> str:
    """Extract math layer content and format as proof panel HTML."""
    if not math_report:
        return '<p class="mda-proof-placeholder">Math translation layer pending.</p>'
    
    # Extract MATH LAYER section
    m = re.search(r'## MATH LAYER ONLY\s*\n(.*?)(?=\n## READER ATTENTION|\Z)',
                  math_report, re.DOTALL)
    math_text = m.group(1).strip() if m else ""
    if not math_text:
        return '<p class="mda-proof-placeholder">Math translation layer pending.</p>'
    
    html_parts = ['<div class="mda-math-layer">']
    html_parts.append('<div class="mda-proof-eyebrow">Math Translation Layer</div>')
    # Convert key sections
    for line in math_text.split('\n'):
        line = line.strip()
        if not line:
            continue
        if line.startswith('- **') and ':**' in line:
            label = re.search(r'\*\*(.+?)\*\*', line)
            val = line.split(':**', 1)[1].strip() if ':**' in line else ""
            if label:
                html_parts.append(
                    f'<div class="math-field">'
                    f'<span class="math-label">{label.group(1)}</span>'
                    f'<span class="math-value">{val}</span></div>')
        elif line.startswith('- '):
            html_parts.append(f'<div class="math-item">{line[2:]}</div>')
        elif line.startswith('|') and not all(c in '-|: ' for c in line):
            cells = [c.strip() for c in line.split('|')[1:-1]]
            row = ''.join(f'<td>{c}</td>' for c in cells)
            html_parts.append(f'<tr>{row}</tr>')
    html_parts.append('</div>')
    return '\n'.join(html_parts)


def load_terms(terms_path: Path) -> list[dict]:
    """Load term inventory JSON."""
    if terms_path.exists():
        try:
            data = json.loads(terms_path.read_text(encoding="utf-8"))
            return data.get("terms", [])
        except (json.JSONDecodeError, KeyError):
            pass
    return []


def build_glossary_html(terms: list[dict]) -> str:
    """Build glossary panel from term inventory."""
    if not terms:
        return '<p class="mda-proof-placeholder">Term inventory pending.</p>'
    parts = ['<div class="mda-glossary">']
    for t in terms:
        parts.append(
            f'<div class="glossary-entry">'
            f'<dt>{t.get("term","")}</dt>'
            f'<dd>{t.get("definition","")}'
            f'<span class="glossary-domain">{t.get("domain","")}</span></dd>'
            f'</div>')
    parts.append('</div>')
    return '\n'.join(parts)


# ─────────────────────────────────────────────
#  HTML Template
# ─────────────────────────────────────────────

TEMPLATE_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{title} — Moral Decline of America</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600;700&family=Oswald:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet"/>
<style>
:root{{
  --bg:#0a0a0a; --surface:#111; --surface2:#1a1a1a;
  --border:#2a2a2a; --border-claim:rgba(212,175,55,.35);
  --text:#e0e0e0; --text2:#a0a0a0; --text3:#707070;
  --mda-red:#dc2626; --mda-red-glow:rgba(220,38,38,.08);
  --claim:#d4af37; --claim-glow:rgba(212,175,55,.08);
  --easy:#22c55e; --easy-glow:rgba(34,197,94,.08);
  --academic:#a78bfa; --academic-glow:rgba(167,139,250,.08);
  --proof:#f59e0b; --proof-glow:rgba(245,158,11,.08);
}}
*{{box-sizing:border-box;}}
body{{
  font-family:'Inter',system-ui,sans-serif;
  background:var(--bg); color:var(--text);
  line-height:1.65; margin:0; padding:0;
}}
</style>
"""
TEMPLATE_CSS = """<style>
/* Reader Mode Bar */
.mda-reader-bar{{
  position:sticky;top:0;z-index:100;
  background:rgba(10,10,10,.95);backdrop-filter:blur(12px);
  border-bottom:1px solid var(--border);
  padding:.5rem 1.5rem;
  display:flex;align-items:center;justify-content:space-between;gap:1rem;
  flex-wrap:wrap;
}}
.mda-reader-bar .series-badge{{
  font-family:'Oswald',sans-serif;font-size:.65rem;letter-spacing:.12em;
  text-transform:uppercase;color:var(--mda-red);font-weight:600;
}}
.mda-reader-bar .meta{{
  font-family:'JetBrains Mono',monospace;font-size:.55rem;
  color:var(--text3);text-transform:uppercase;letter-spacing:.06em;
}}
.tab-group{{display:flex;gap:.4rem;flex-wrap:wrap;}}
.tab-btn{{
  padding:.4rem .7rem;border:1px solid var(--border);border-radius:.35rem;
  background:var(--surface);color:var(--text2);cursor:pointer;
  font-family:'JetBrains Mono',monospace;font-size:.58rem;font-weight:600;
  text-transform:uppercase;letter-spacing:.06em;transition:all .2s;
}}
.tab-btn:hover{{border-color:var(--mda-red);color:var(--text);}}
.tab-btn.active{{border-color:var(--mda-red);background:var(--mda-red-glow);color:var(--mda-red);}}
.tab-btn[data-tab="easy"].active{{border-color:var(--easy);background:var(--easy-glow);color:var(--easy);}}
.tab-btn[data-tab="academic"].active{{border-color:var(--academic);background:var(--academic-glow);color:var(--academic);}}
.tab-btn[data-tab="proof"].active{{border-color:var(--proof);background:var(--proof-glow);color:var(--proof);}}

/* Article */
.article{{max-width:780px;margin:0 auto;padding:2rem 1.5rem 6rem;}}
.article h1{{
  font-family:'Oswald',sans-serif;font-size:clamp(1.8rem,4vw,2.8rem);
  font-weight:600;color:#fff;text-transform:uppercase;letter-spacing:.02em;
  margin:0 0 .5rem;line-height:1.1;
}}
.article .subtitle{{
  font-family:'Crimson Text',serif;font-size:1.15rem;color:var(--text2);
  font-style:italic;margin:0 0 2rem;line-height:1.5;
}}
.article h2{{
  font-family:'Oswald',sans-serif;font-size:1.2rem;font-weight:600;color:#fff;
  text-transform:uppercase;letter-spacing:.04em;margin:2.5rem 0 1rem;
  border-bottom:1px solid var(--border);padding-bottom:.4rem;
}}
.article h3{{font-family:'Crimson Text',serif;font-size:1.15rem;font-weight:600;color:var(--mda-red);margin:1.5rem 0 .5rem;}}
.article p{{font-size:1.02rem;line-height:1.75;margin:0 0 1.25rem;}}
.article blockquote{{
  border-left:3px solid var(--mda-red);background:var(--mda-red-glow);
  padding:1rem 1.25rem;margin:1.5rem 0;border-radius:0 .4rem .4rem 0;
  font-family:'Crimson Text',serif;font-style:italic;color:var(--text2);
}}
.article img{{max-width:100%;border-radius:.4rem;margin:1rem 0;}}
.mda-table{{width:100%;border-collapse:collapse;margin:1rem 0;font-size:.88rem;}}
.mda-table td{{padding:.4rem .6rem;border:1px solid var(--border);color:var(--text2);}}
.mda-table tr:first-child td{{font-weight:600;color:var(--text);background:var(--surface);}}

/* Reading level panels */
.level-panel{{display:none;}}
.level-panel.active{{display:block;}}

/* Proof panel */
.proof-panel{{display:none;max-width:780px;margin:0 auto;padding:1.5rem;}}
.proof-panel.active{{display:block;}}
.mda-proof-eyebrow{{
  font-family:'Inter',sans-serif;font-size:.72rem;letter-spacing:.14em;
  text-transform:uppercase;color:var(--proof);margin-bottom:.6rem;
}}
.math-field{{display:flex;gap:.5rem;margin:.4rem 0;padding:.3rem 0;border-bottom:1px solid rgba(255,255,255,.05);}}
.math-label{{font-family:'JetBrains Mono',monospace;font-size:.7rem;color:var(--proof);font-weight:600;min-width:180px;}}
.math-value{{font-size:.85rem;color:var(--text2);}}
.math-item{{font-size:.85rem;color:var(--text);padding:.2rem 0 .2rem 1rem;border-left:2px solid var(--border);margin:.3rem 0;}}
.mda-proof-placeholder{{color:var(--text3);font-style:italic;font-size:.9rem;}}

/* Glossary */
.mda-glossary{{columns:1;}}
.glossary-entry{{break-inside:avoid;margin-bottom:.8rem;}}
.glossary-entry dt{{font-family:'JetBrains Mono',monospace;font-size:.8rem;color:var(--academic);font-weight:600;}}
.glossary-entry dd{{font-size:.85rem;color:var(--text2);margin:0 0 0 .5rem;}}
.glossary-domain{{font-size:.65rem;color:var(--text3);margin-left:.5rem;font-style:italic;}}

/* Easy level overrides */
body.mode-easy .article p{{font-size:1.15rem;line-height:1.85;}}
body.mode-easy .article h3{{font-size:1.3rem;color:var(--easy);font-family:'Oswald',sans-serif;}}
body.mode-easy .article blockquote{{border-left-color:var(--easy);background:var(--easy-glow);font-style:normal;}}
/* Academic level overrides */
body.mode-academic .article p{{font-size:.95rem;line-height:1.65;color:#d0d0d0;}}
body.mode-academic .article h3{{font-size:1.1rem;color:var(--academic);font-family:'Crimson Text',serif;font-style:italic;}}
body.mode-academic .article blockquote{{border-left-color:var(--academic);background:var(--academic-glow);}}

@media(max-width:640px){{
  .article{{padding:1.5rem 1rem 4rem;}}
  .mda-reader-bar{{padding:.4rem 1rem;}}
}}
</style>
"""
TEMPLATE_JS = """<script>
function setTab(tab) {{
  // Update buttons
  document.querySelectorAll('.tab-btn').forEach(b => {{
    b.classList.toggle('active', b.dataset.tab === tab);
  }});
  // Update body mode class
  document.body.className = 'mode-' + tab;
  // Toggle content panels
  document.querySelectorAll('.level-panel').forEach(p => {{
    p.classList.toggle('active', p.dataset.level === tab);
  }});
  document.querySelectorAll('.proof-panel').forEach(p => {{
    p.classList.toggle('active', tab === 'proof');
  }});
  // Update status text
  const st = document.getElementById('mode-status');
  if (st) st.textContent = tab.charAt(0).toUpperCase() + tab.slice(1) + ' active';
}}
document.addEventListener('DOMContentLoaded', () => setTab('standard'));
</script>
"""

# ─────────────────────────────────────────────
#  Main build function
# ─────────────────────────────────────────────

def build_html(slug: str, math_dir: Path | None = None, outdir: Path = DEFAULT_OUT) -> Path:
    """Build production HTML for one article."""
    std_path = LOSSLESS / f"{slug}.md"
    acad_path = READING_LEVELS / f"{slug}_ACADEMIC.md"
    easy_path = READING_LEVELS / f"{slug}_EASY.md"
    terms_path = READING_LEVELS / f"{slug}_TERM_INVENTORY.json"

    if not std_path.exists():
        print(f"ERROR: Standard article not found: {std_path}")
        return None

    std_md = std_path.read_text(encoding="utf-8", errors="replace")
    title = extract_title(std_md)
    num = extract_slug_number(slug)

    # Convert markdown to HTML
    std_html = md_to_html(std_md)
    acad_html = md_to_html(acad_path.read_text(encoding="utf-8", errors="replace")) if acad_path.exists() else ""
    easy_html = md_to_html(easy_path.read_text(encoding="utf-8", errors="replace")) if easy_path.exists() else ""

    # Load math report
    math_report = load_math_report(math_dir, slug)
    proof_html = parse_math_for_proof_panel(math_report)

    # Load terms
    terms = load_terms(terms_path)
    glossary_html = build_glossary_html(terms)

    # Status flags
    has_easy = bool(easy_html.strip())
    has_acad = bool(acad_html.strip())
    has_proof = bool(math_report.strip())

    # Assemble HTML
    out = []
    out.append(TEMPLATE_HEAD.format(title=title))
    out.append(TEMPLATE_CSS.replace('{{', '{').replace('}}', '}'))
    out.append('</head>\n<body class="mode-standard">\n')

    # Reader mode bar
    easy_state = "" if has_easy else ' style="opacity:.4;pointer-events:none;"'
    acad_state = "" if has_acad else ' style="opacity:.4;pointer-events:none;"'
    proof_state = "" if has_proof else ' style="opacity:.4;pointer-events:none;"'

    out.append(f'''
<!-- BEGIN:COMPONENT:reader-mode:reader-mode-bar -->
<div class="mda-reader-bar">
  <div>
    <span class="series-badge">Moral Decline of America</span>
    <span class="meta">MDA-{num}</span>
    <span class="meta" id="mode-status">Standard active</span>
  </div>
  <div class="tab-group">
    <button class="tab-btn" data-tab="easy" onclick="setTab('easy')"{easy_state}>Easy</button>
    <button class="tab-btn active" data-tab="standard" onclick="setTab('standard')">Standard</button>
    <button class="tab-btn" data-tab="academic" onclick="setTab('academic')"{acad_state}>Academic</button>
    <button class="tab-btn" data-tab="proof" onclick="setTab('proof')"{proof_state}>Proof</button>
  </div>
</div>
<!-- END:COMPONENT:reader-mode:reader-mode-bar -->
''')

    # Standard panel (always present)
    out.append(f'''
<!-- BEGIN:LEVEL:standard -->
<div class="level-panel active" data-level="standard">
  <article class="article">
    <h1>{title}</h1>
    <p class="subtitle">MDA-{num} · David Lowe · Theophysics Institute</p>
    {std_html}
  </article>
</div>
<!-- END:LEVEL:standard -->
''')

    # Easy panel
    if has_easy:
        out.append(f'''
<!-- BEGIN:LEVEL:easy -->
<div class="level-panel" data-level="easy">
  <article class="article">
    <h1>{title}</h1>
    <p class="subtitle">MDA-{num} · Easy Reading Level</p>
    {easy_html}
  </article>
</div>
<!-- END:LEVEL:easy -->
''')

    # Academic panel
    if has_acad:
        out.append(f'''
<!-- BEGIN:LEVEL:academic -->
<div class="level-panel" data-level="academic">
  <article class="article">
    <h1>{title}</h1>
    <p class="subtitle">MDA-{num} · Academic Reading Level</p>
    {acad_html}
  </article>
</div>
<!-- END:LEVEL:academic -->
''')

    # Proof panel (math + glossary)
    out.append(f'''
<!-- BEGIN:LEVEL:proof -->
<div class="proof-panel" data-level="proof">
  <div class="article">
    <div class="mda-proof-eyebrow">Proof Pressure Layer</div>
    <h2 style="font-family:Oswald,sans-serif;color:#fff;text-transform:uppercase;letter-spacing:.04em;">
      {title} — Proof & Math
    </h2>
    
    <h3>Math Translation</h3>
    {proof_html}
    
    <h3 style="margin-top:2rem;">Term Inventory</h3>
    {glossary_html}
    
    <h3 style="margin-top:2rem;">Promoted Claims</h3>
    <p class="mda-proof-placeholder">
      No claim from this article has been promoted through the deterministic Axiom + 7Q gate yet.
      Claims will appear here after the proof-promotion pass.
    </p>
  </div>
</div>
<!-- END:LEVEL:proof -->
''')

    # Footer
    out.append(f'''
<div style="max-width:780px;margin:0 auto;padding:1rem 1.5rem 3rem;">
  <p style="font-family:'JetBrains Mono',monospace;font-size:.55rem;color:var(--text3);
     text-transform:uppercase;letter-spacing:.08em;border-top:1px solid var(--border);
     padding-top:1rem;">
    Generated {datetime.now().strftime("%Y-%m-%d %H:%M")} · 
    Easy: {"✓" if has_easy else "pending"} · 
    Academic: {"✓" if has_acad else "pending"} · 
    Math: {"✓" if has_proof else "pending"} · 
    Claims: pending
  </p>
</div>
''')

    out.append(TEMPLATE_JS.replace('{{', '{').replace('}}', '}'))
    out.append('\n</body>\n</html>')

    # Write output
    outdir.mkdir(parents=True, exist_ok=True)
    out_path = outdir / f"{slug}.html"
    out_path.write_text(''.join(out), encoding="utf-8")
    print(f"Built: {out_path}")
    return out_path


# ─────────────────────────────────────────────
#  CLI
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="MDA Three-Lane HTML Combiner")
    parser.add_argument("slug", nargs="?", help="Article slug e.g. MDA-013-peak-coherence-1940")
    parser.add_argument("--all", action="store_true", help="Process all articles in 01_LOSSLESS")
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUT, help="Output directory")
    parser.add_argument("--math-dir", type=Path, default=None,
                        help="Directory containing TWO_LANE_REPORT.md files")
    args = parser.parse_args()

    if not args.slug and not args.all:
        parser.error("Provide a slug or --all")

    if args.math_dir:
        args.math_dir = Path(str(args.math_dir).strip('"').strip("'"))

    if args.all:
        slugs = sorted(p.stem for p in LOSSLESS.glob("*.md"))
    else:
        slugs = [args.slug]

    built = 0
    skipped = 0
    for slug in slugs:
        result = build_html(slug, math_dir=args.math_dir, outdir=args.outdir)
        if result:
            built += 1
        else:
            skipped += 1

    print(f"\nDone. Built: {built}, Skipped: {skipped}")
    if built:
        print(f"Output: {args.outdir}")


if __name__ == "__main__":
    main()
