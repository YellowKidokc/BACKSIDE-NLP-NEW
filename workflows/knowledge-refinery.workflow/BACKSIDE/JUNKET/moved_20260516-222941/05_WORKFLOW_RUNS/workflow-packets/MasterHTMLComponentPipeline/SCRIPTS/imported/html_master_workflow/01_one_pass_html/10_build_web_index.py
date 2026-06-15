#!/usr/bin/env python3
"""
build_web_index.py — Auto-scanning Web Page Index Generator
Scans all subdirectories of faiththruphysics.com, extracts HTML titles,
and generates a self-tracking WEB_PAGE_INDEX.html.

Usage:
  python build_web_index.py
  python build_web_index.py --dir "C:/path/to/site"
"""

import os, re, sys, json
from datetime import datetime
from html import escape

# ── CONFIG ──────────────────────────────────────────────────────────
SITE_DIR = os.path.dirname(os.path.abspath(__file__))
if "--dir" in sys.argv:
    SITE_DIR = sys.argv[sys.argv.index("--dir") + 1]

SKIP_DIRS = {"node_modules", ".git", "__pycache__", "assets", "css", "js", "fonts", "audio", "images", "img", "intro"}
SKIP_FILES = {"WEB_PAGE_INDEX.html", "build_web_index.py", "image-registry.html", "image-manifest.json"}

# Section metadata: folder_name -> {color, icon, description}
SECTION_META = {
    "genesis-to-quantum":      {"color": "#4a9eff", "icon": "fa-atom",          "desc": "Nine-part series mapping Genesis onto quantum mechanics"},
    "logos-papers-story":       {"color": "#2dd4bf", "icon": "fa-scroll",        "desc": "12-chapter narrative walk through the Theophysics framework"},
    "convergence":              {"color": "#d4af37", "icon": "fa-layer-group",   "desc": "Convergence series — why God drowned everybody and beyond"},
    "convergence-deep":         {"color": "#f59e0b", "icon": "fa-microscope",    "desc": "Deep-dive convergence articles"},
    "cross-domain":             {"color": "#22c55e", "icon": "fa-arrows-alt",    "desc": "Cross-domain bridge articles"},
    "duality-project":          {"color": "#a855f7", "icon": "fa-yin-yang",      "desc": "Wave-particle duality and theological parallels"},
    "formal-papers":            {"color": "#ef4444", "icon": "fa-file-alt",      "desc": "Formal academic papers (FP-001 through FP-016)"},
    "master-equation":          {"color": "#d4af37", "icon": "fa-square-root-alt","desc": "The master equation and its 10 laws"},
    "proof-architecture":       {"color": "#4a9eff", "icon": "fa-cubes",         "desc": "Proof bundles and architectural arguments"},
    "proof-explorer":           {"color": "#4a9eff", "icon": "fa-search",        "desc": "Interactive axiom and proof exploration"},
    "worldview-comparisons":    {"color": "#a855f7", "icon": "fa-balance-scale", "desc": "Theophysics vs every major worldview"},
    "moral-decline":            {"color": "#ef4444", "icon": "fa-chart-line",    "desc": "Moral decline as entropy — phase transitions in culture"},
    "spiritual-warfare":        {"color": "#ef4444", "icon": "fa-shield-alt",    "desc": "Spiritual warfare through the physics lens"},
    "consciousness":            {"color": "#e879f9", "icon": "fa-brain",         "desc": "Consciousness, observer effects, and the chi field"},
    "prophetic-synthesis":      {"color": "#f59e0b", "icon": "fa-bolt",          "desc": "Prophetic synthesis — coherence cascades and retrocausal clocks"},
    "revolution-of-truth":      {"color": "#22c55e", "icon": "fa-fist-raised",   "desc": "The revolution of truth — architecture, lock, key"},
    "socratic-axioms":          {"color": "#2dd4bf", "icon": "fa-comments",      "desc": "Socratic dialogues exploring each axiom"},
    "apologetics-debate":       {"color": "#d4af37", "icon": "fa-gavel",         "desc": "Apologetics debates and consciousness arguments"},
    "blue":                     {"color": "#4a9eff", "icon": "fa-palette",       "desc": "Blue series — derivatives, evolution probe, equations"},
    "bible-datalab":            {"color": "#22c55e", "icon": "fa-database",      "desc": "Interactive data visualizations of biblical patterns"},
    "one-page-stories":         {"color": "#f59e0b", "icon": "fa-file",          "desc": "One-page standalone explorations"},
    "be-glad-youre-a-loser":    {"color": "#2dd4bf", "icon": "fa-heart",         "desc": "Be Glad You're a Loser series"},
    "family-tests":             {"color": "#22c55e", "icon": "fa-flask",         "desc": "Family-facing test results and explanations"},
    "the-bidirectional-audit":  {"color": "#d4af37", "icon": "fa-exchange-alt",  "desc": "The bidirectional audit"},
    "incoming-for-kimmy":       {"color": "#e879f9", "icon": "fa-envelope",      "desc": "Templates for Kimmy"},
    "logos-papers":             {"color": "#2dd4bf", "icon": "fa-file-code",     "desc": "Logos papers template"},
    "HTML-Gallery-All-Images":  {"color": "#f59e0b", "icon": "fa-images",        "desc": "Full image gallery"},
}

def extract_title(filepath):
    """Pull <title> from an HTML file."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            head = f.read(8000)
        m = re.search(r"<title[^>]*>(.*?)</title>", head, re.IGNORECASE | re.DOTALL)
        if m:
            title = re.sub(r"\s+", " ", m.group(1)).strip()
            # Clean common suffixes
            for sep in [" — ", " | ", " - "]:
                if sep in title:
                    title = title.split(sep)[0].strip()
            return title
    except:
        pass
    return None

def scan_site(site_dir):
    """Scan site directory, return dict of section -> list of page dicts."""
    sections = {}
    root_pages = []

    for entry in sorted(os.listdir(site_dir)):
        full = os.path.join(site_dir, entry)

        # Root-level HTML files
        if os.path.isfile(full) and entry.endswith(".html") and entry not in SKIP_FILES:
            title = extract_title(full) or entry.replace(".html", "").replace("-", " ").title()
            root_pages.append({"file": entry, "title": title, "path": entry})

        # Subdirectories
        elif os.path.isdir(full) and entry not in SKIP_DIRS:
            pages = []
            for root, dirs, files in os.walk(full):
                # Skip nested skip dirs
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                rel_root = os.path.relpath(root, site_dir).replace("\\", "/")
                for fname in sorted(files):
                    if fname.endswith(".html") and fname not in SKIP_FILES:
                        fpath = os.path.join(root, fname)
                        title = extract_title(fpath) or fname.replace(".html", "").replace("-", " ").title()
                        rel_path = f"{rel_root}/{fname}"
                        is_index = (fname == "index.html")
                        pages.append({
                            "file": fname,
                            "title": title,
                            "path": rel_path,
                            "is_index": is_index,
                        })
            if pages:
                sections[entry] = pages

    return sections, root_pages

def build_html(sections, root_pages):
    """Generate the full WEB_PAGE_INDEX.html."""
    now = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    total_pages = sum(len(p) for p in sections.values()) + len(root_pages)
    total_sections = len(sections)

    # Count sections with/without index
    has_index = sum(1 for pages in sections.values() if any(p["is_index"] for p in pages))
    no_index = total_sections - has_index

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Theophysics Web Pages — Master Index</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600;700&family=Oswald:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"/>
<style>
:root{{
  --surface:#0a0a0a;--surface-card:#1a1a1a;--border:#2a2a2a;
  --gold:#d4af37;--blue:#4a9eff;--teal:#2dd4bf;--red:#ef4444;--green:#22c55e;--purple:#a855f7;
  --text:#e8e8e8;--text-dim:#909090;--text-muted:#606060;
}}
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:'Inter',sans-serif;background:var(--surface);color:var(--text);line-height:1.6;}}
.serif{{font-family:'Crimson Text',serif;}}
.mono{{font-family:'JetBrains Mono',monospace;}}
a{{color:var(--gold);text-decoration:none;}}
a:hover{{color:#f4d03f;text-decoration:underline;}}
.badge{{display:inline-block;padding:.15rem .5rem;border-radius:.25rem;font-size:.65rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;}}
.badge-index{{background:rgba(34,197,94,.12);color:var(--green);}}
.badge-page{{background:rgba(74,158,255,.12);color:var(--blue);}}
.badge-root{{background:rgba(212,175,55,.12);color:var(--gold);}}
.badge-no-index{{background:rgba(239,68,68,.12);color:var(--red);}}
.card{{background:var(--surface-card);border:1px solid var(--border);border-radius:.5rem;padding:1.25rem;transition:border-color .25s;}}
.card:hover{{border-color:var(--gold);}}
table{{width:100%;border-collapse:separate;border-spacing:0;}}
th{{text-align:left;font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;color:var(--gold);padding:.75rem 1rem;border-bottom:1px solid var(--border);background:var(--surface-card);position:sticky;top:0;z-index:1;}}
td{{padding:.55rem 1rem;border-bottom:1px solid rgba(42,42,42,.5);font-size:.85rem;vertical-align:top;}}
tr:hover td{{background:rgba(212,175,55,.03);}}
.section-block{{margin-bottom:2.5rem;}}
.section-header{{display:flex;align-items:center;gap:.75rem;margin-bottom:.5rem;cursor:pointer;}}
.section-header:hover .section-title{{color:white;}}
.section-dot{{width:12px;height:12px;border-radius:50%;flex-shrink:0;}}
.section-title{{font-family:'Crimson Text',serif;font-size:1.4rem;color:#ccc;transition:color .2s;}}
.section-count{{font-family:'JetBrains Mono',monospace;font-size:.7rem;color:var(--text-muted);margin-left:.5rem;}}
.section-desc{{font-size:.8rem;color:var(--text-dim);margin-bottom:1rem;margin-left:1.6rem;}}
.section-table{{border:1px solid var(--border);border-radius:.5rem;overflow:hidden;}}
#searchBox{{background:var(--surface-card);border:1px solid var(--border);color:var(--text);padding:.6rem 1rem;border-radius:.4rem;width:100%;max-width:400px;font-size:.9rem;}}
#searchBox:focus{{outline:none;border-color:var(--gold);}}
.hidden{{display:none !important;}}
</style>
</head>
<body>
<div class="max-w-6xl mx-auto px-6 py-12">

<header class="mb-8">
  <a href="index.html" style="font-size:.8rem;color:var(--text-muted);text-decoration:none;display:inline-flex;align-items:center;gap:.4rem;margin-bottom:1rem;">
    <i class="fas fa-arrow-left"></i> Back to Theophysics
  </a>
  <p class="mono text-sm font-semibold tracking-widest uppercase mb-2" style="color:var(--gold);">Theophysics Research Program</p>
  <h1 class="serif text-4xl font-bold text-white mb-3">Web Page Index</h1>
  <p style="color:var(--text-dim);">Auto-generated master tracking of every page on the site. Last rebuilt: <strong style="color:white;">{escape(now)}</strong></p>
  <p style="color:var(--text-muted);font-size:.75rem;margin-top:.25rem;">Run <code style="color:var(--gold);">python build_web_index.py</code> to rebuild.</p>
</header>

<!-- STATS -->
<section class="mb-10">
  <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
    <div class="card text-center">
      <p class="mono text-3xl font-bold" style="color:var(--gold);">{total_pages}</p>
      <p class="text-xs mt-1" style="color:var(--text-dim);">Total Pages</p>
    </div>
    <div class="card text-center">
      <p class="mono text-3xl font-bold" style="color:var(--blue);">{total_sections}</p>
      <p class="text-xs mt-1" style="color:var(--text-dim);">Sections</p>
    </div>
    <div class="card text-center">
      <p class="mono text-3xl font-bold" style="color:var(--green);">{has_index}</p>
      <p class="text-xs mt-1" style="color:var(--text-dim);">With Landing Page</p>
    </div>
    <div class="card text-center">
      <p class="mono text-3xl font-bold" style="color:var(--red);">{no_index}</p>
      <p class="text-xs mt-1" style="color:var(--text-dim);">Missing Landing Page</p>
    </div>
    <div class="card text-center">
      <p class="mono text-3xl font-bold" style="color:var(--purple);">{len(root_pages)}</p>
      <p class="text-xs mt-1" style="color:var(--text-dim);">Root Pages</p>
    </div>
  </div>
</section>

<!-- SEARCH -->
<section class="mb-8">
  <div class="flex items-center gap-3 flex-wrap">
    <input type="text" id="searchBox" placeholder="Search pages..." oninput="filterPages(this.value)"/>
    <button onclick="expandAll()" style="background:var(--surface-card);border:1px solid var(--border);color:var(--text-dim);padding:.4rem .8rem;border-radius:.4rem;font-size:.75rem;cursor:pointer;">Expand All</button>
    <button onclick="collapseAll()" style="background:var(--surface-card);border:1px solid var(--border);color:var(--text-dim);padding:.4rem .8rem;border-radius:.4rem;font-size:.75rem;cursor:pointer;">Collapse All</button>
  </div>
</section>
"""

    # ── ROOT PAGES ──
    if root_pages:
        html += """
<div class="section-block" data-section="root">
  <div class="section-header" onclick="toggleSection(this)">
    <div class="section-dot" style="background:var(--gold);"></div>
    <h2 class="section-title">Root Pages</h2>
    <span class="section-count">""" + str(len(root_pages)) + """ pages</span>
    <i class="fas fa-chevron-down ml-auto" style="color:var(--text-muted);font-size:.7rem;transition:transform .2s;"></i>
  </div>
  <p class="section-desc">Standalone pages at the site root level.</p>
  <div class="section-table section-content">
  <table>
    <thead><tr><th>#</th><th>Title</th><th>File</th></tr></thead>
    <tbody>
"""
        for i, p in enumerate(root_pages, 1):
            html += f'      <tr data-title="{escape(p["title"].lower())}" data-file="{escape(p["file"].lower())}"><td class="mono" style="color:var(--gold);">{i}</td><td class="font-semibold text-white">{escape(p["title"])}</td><td><a href="{escape(p["path"])}">{escape(p["file"])}</a> <span class="badge badge-root">Root</span></td></tr>\n'
        html += "    </tbody>\n  </table>\n  </div>\n</div>\n"

    # ── SECTIONS ──
    for folder in sorted(sections.keys()):
        pages = sections[folder]
        meta = SECTION_META.get(folder, {"color": "#666", "icon": "fa-folder", "desc": ""})
        color = meta["color"]
        icon = meta["icon"]
        desc = meta["desc"]
        page_count = len(pages)
        section_has_index = any(p["is_index"] for p in pages)

        html += f"""
<div class="section-block" data-section="{escape(folder)}">
  <div class="section-header" onclick="toggleSection(this)">
    <div class="section-dot" style="background:{color};"></div>
    <i class="fas {icon}" style="color:{color};font-size:.9rem;"></i>
    <h2 class="section-title">{escape(folder.replace('-', ' ').title())}</h2>
    <span class="section-count">{page_count} pages</span>
    {"" if section_has_index else '<span class="badge badge-no-index" style="margin-left:.5rem;">No Index</span>'}
    <i class="fas fa-chevron-down ml-auto" style="color:var(--text-muted);font-size:.7rem;transition:transform .2s;"></i>
  </div>
"""
        if desc:
            html += f'  <p class="section-desc">{escape(desc)}</p>\n'

        html += """  <div class="section-table section-content">
  <table>
    <thead><tr><th>#</th><th>Title</th><th>File</th><th>Type</th></tr></thead>
    <tbody>
"""
        for i, p in enumerate(pages, 1):
            badge = '<span class="badge badge-index">Index</span>' if p["is_index"] else '<span class="badge badge-page">Page</span>'
            html += f'      <tr data-title="{escape(p["title"].lower())}" data-file="{escape(p["file"].lower())}"><td class="mono" style="color:{color};">{i}</td><td class="font-semibold text-white">{escape(p["title"])}</td><td><a href="{escape(p["path"])}">{escape(p["file"])}</a></td><td>{badge}</td></tr>\n'

        html += "    </tbody>\n  </table>\n  </div>\n</div>\n"

    # ── FOOTER + JS ──
    html += f"""
<footer style="border-top:1px solid var(--border);padding:2rem 0;text-align:center;margin-top:3rem;">
  <p class="mono text-xs" style="color:var(--gold);opacity:.4;margin-bottom:.5rem;">&chi; = &int;&int;&int;(G&middot;M&middot;E&middot;S&middot;T&middot;K&middot;R&middot;Q&middot;F&middot;C) dx dy dt</p>
  <p class="text-sm" style="color:var(--text-muted);">David Lowe | Theophysics Research Program | Auto-generated {escape(now)}</p>
  <p class="text-xs mt-1" style="color:var(--text-muted);">{total_pages} pages across {total_sections} sections</p>
</footer>

</div>

<script>
function toggleSection(header) {{
  const content = header.parentElement.querySelector('.section-content');
  const chevron = header.querySelector('.fa-chevron-down, .fa-chevron-up');
  if (content.classList.contains('hidden')) {{
    content.classList.remove('hidden');
    if (chevron) chevron.className = chevron.className.replace('fa-chevron-up','fa-chevron-down');
  }} else {{
    content.classList.add('hidden');
    if (chevron) chevron.className = chevron.className.replace('fa-chevron-down','fa-chevron-up');
  }}
}}

function expandAll() {{
  document.querySelectorAll('.section-content').forEach(el => el.classList.remove('hidden'));
  document.querySelectorAll('.fa-chevron-up').forEach(el => el.className = el.className.replace('fa-chevron-up','fa-chevron-down'));
}}

function collapseAll() {{
  document.querySelectorAll('.section-content').forEach(el => el.classList.add('hidden'));
  document.querySelectorAll('.fa-chevron-down').forEach(el => el.className = el.className.replace('fa-chevron-down','fa-chevron-up'));
}}

function filterPages(query) {{
  const q = query.toLowerCase().trim();
  document.querySelectorAll('tr[data-title]').forEach(row => {{
    if (!q) {{ row.style.display = ''; return; }}
    const title = row.getAttribute('data-title') || '';
    const file = row.getAttribute('data-file') || '';
    row.style.display = (title.includes(q) || file.includes(q)) ? '' : 'none';
  }});
  // Show all sections when searching
  if (q) expandAll();
}}
</script>

</body>
</html>"""
    return html


def main():
    print(f"Scanning: {SITE_DIR}")
    sections, root_pages = scan_site(SITE_DIR)

    total = sum(len(p) for p in sections.values()) + len(root_pages)
    print(f"Found {total} pages across {len(sections)} sections + {len(root_pages)} root pages")

    html = build_html(sections, root_pages)

    out_path = os.path.join(SITE_DIR, "WEB_PAGE_INDEX.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Written: {out_path}")

    # Also write a JSON manifest
    manifest = {
        "generated": datetime.now().isoformat(),
        "total_pages": total,
        "sections": {k: [p["path"] for p in v] for k, v in sections.items()},
        "root_pages": [p["path"] for p in root_pages],
    }
    manifest_path = os.path.join(SITE_DIR, "web-manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
