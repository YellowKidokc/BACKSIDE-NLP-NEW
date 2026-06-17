"""Stage 0 verify + Stage 1 HTML->Markdown for MDA test article."""
import re
from pathlib import Path

SRC = Path(r"D:\GitHub\faiththruphysics-site\moral-decline\02-method-and-metrics\MDA-039-physics-of-coherence.html")
OUT = Path(r"D:\GitHub\BACKSIDE-NLP-NEW\stations\exec-summary.station\_inbox\MDA-039-physics-of-coherence.md")

text = SRC.read_text(encoding="utf-8")

# ── STAGE 0: VERIFY ──
eqs = re.findall(r'data-eq-id="([^"]+)"', text)
mathjax = "mathjax" in text.lower()
mtl_css = "mtl-equation" in text
blocks = len(re.findall(r"math-translation-block", text))
print(f"=== STAGE 0: SOURCE VERIFICATION ===")
print(f"File: {SRC.name}")
print(f"Size: {len(text):,} chars")
print(f"MathJax loaded: {mathjax}")
print(f"MTL CSS linked: {mtl_css}")
print(f"Equation blocks: {blocks}")
print(f"Equation IDs: {eqs}")
s0 = bool(eqs and mathjax)
print(f"Stage 0: {'PASS' if s0 else 'FAIL'}")
if not s0:
    raise SystemExit(1)


# ── STAGE 1: HTML -> MARKDOWN ──
print(f"\n=== STAGE 1: HTML -> MARKDOWN ===")

# Try to use BeautifulSoup for clean extraction
try:
    from bs4 import BeautifulSoup
    print("Using BeautifulSoup")
except ImportError:
    print("Installing beautifulsoup4...")
    import subprocess
    subprocess.check_call(["pip", "install", "beautifulsoup4", "--break-system-packages", "-q"])
    from bs4 import BeautifulSoup

soup = BeautifulSoup(text, "html.parser")

# Extract title
title_tag = soup.find("title")
title = title_tag.get_text(strip=True) if title_tag else SRC.stem
# Clean title - remove site suffix
title = re.sub(r"\s*\|.*$", "", title).strip()

# Extract meta description
meta_desc = ""
meta = soup.find("meta", attrs={"name": "description"})
if meta and meta.get("content"):
    meta_desc = meta["content"]

# Extract PAGE_META from comment
page_meta = ""
for comment in soup.find_all(string=lambda t: isinstance(t, type(soup.new_string(""))) and "PAGE_META" in str(t)):
    page_meta = str(comment).strip()


# Find main article content - try common containers
article = None
for selector in ["main", "article", ".article-content", ".content",
                  "#content", ".prose", "section.article"]:
    found = soup.select_one(selector)
    if found:
        article = found
        break

# Fallback: use body minus nav/footer/sidebar
if not article:
    article = soup.find("body")
    if article:
        for tag in article.find_all(["nav", "footer", "header",
                                      "script", "style", "noscript"]):
            tag.decompose()
        # Remove sidebar if present
        for sidebar in article.select(".sidebar, .side-nav, .toc, .nav-links"):
            sidebar.decompose()

if not article:
    print("Stage 1: FAIL - no content found")
    raise SystemExit(1)

# Build markdown
md_lines = []
md_lines.append(f"# {title}")
md_lines.append("")
if meta_desc:
    md_lines.append(f"> {meta_desc}")
    md_lines.append("")


def element_to_md(el):
    """Convert an HTML element to markdown text."""
    lines = []
    if el.name in ("h1", "h2", "h3", "h4", "h5", "h6"):
        level = int(el.name[1])
        text = el.get_text(strip=True)
        if text:
            lines.append(f"{'#' * level} {text}")
            lines.append("")

    elif el.name == "p":
        text = el.get_text(separator=" ", strip=True)
        if text:
            lines.append(text)
            lines.append("")

    elif el.name == "blockquote":
        text = el.get_text(separator=" ", strip=True)
        if text:
            lines.append(f"> {text}")
            lines.append("")

    elif el.name in ("ul", "ol"):
        for li in el.find_all("li", recursive=False):
            text = li.get_text(separator=" ", strip=True)
            if text:
                lines.append(f"- {text}")
        lines.append("")

    elif el.name == "details" and el.get("data-eq-id"):
        eq_id = el["data-eq-id"]
        summary = el.find("summary")
        summary_text = summary.get_text(strip=True) if summary else "Equation"

        # Extract the translation content from the details block
        body = el.find(class_="mtl-body") or el
        body_text = body.get_text(separator="\n", strip=True)
        lines.append(f"**[EQUATION {eq_id}]** {summary_text}")
        lines.append("")
        if body_text and body_text != summary_text:
            for bt in body_text.split("\n"):
                bt = bt.strip()
                if bt and bt != summary_text:
                    lines.append(f"> {bt}")
            lines.append("")

    elif el.name == "table":
        rows = el.find_all("tr")
        for i, row in enumerate(rows):
            cells = row.find_all(["th", "td"])
            cell_texts = [c.get_text(strip=True) for c in cells]
            lines.append("| " + " | ".join(cell_texts) + " |")
            if i == 0:
                lines.append("| " + " | ".join(["---"] * len(cells)) + " |")
        lines.append("")

    elif el.name == "div":
        # Recurse into divs but skip UI-only divs
        skip_classes = {"sidebar", "nav", "footer", "header", "toc",
                       "top-nav", "bottom-bar", "framework-tabs",
                       "fw-panel", "audio-dock", "mda-tb"}
        el_classes = set(el.get("class", []))
        if not el_classes & skip_classes:
            for child in el.children:
                if hasattr(child, "name") and child.name:
                    lines.extend(element_to_md(child))

    return lines


# Walk content and convert
for child in article.children:
    if hasattr(child, "name") and child.name:
        md_lines.extend(element_to_md(child))

# Clean up: remove multiple blank lines
markdown = "\n".join(md_lines)
markdown = re.sub(r"\n{3,}", "\n\n", markdown).strip()

# Write markdown to staging
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(markdown, encoding="utf-8")

word_ct = len(re.findall(r"\b\w+\b", markdown))
eq_ct = len(re.findall(r"\[EQUATION ", markdown))
heading_ct = len(re.findall(r"^#{1,6} ", markdown, re.M))

print(f"Output: {OUT}")
print(f"Words: {word_ct}")
print(f"Headings: {heading_ct}")
print(f"Equations preserved: {eq_ct}")
print(f"Stage 1: {'PASS' if word_ct > 100 else 'FAIL'}")

print(f"\n=== READY FOR STAGE 2 (vectorize) + STAGE 3 (NLP pipeline) ===")
print(f"Article is in ST_001 _inbox. Run the station to begin processing.")
print(f"FastAPI must be running on port 8700.")
