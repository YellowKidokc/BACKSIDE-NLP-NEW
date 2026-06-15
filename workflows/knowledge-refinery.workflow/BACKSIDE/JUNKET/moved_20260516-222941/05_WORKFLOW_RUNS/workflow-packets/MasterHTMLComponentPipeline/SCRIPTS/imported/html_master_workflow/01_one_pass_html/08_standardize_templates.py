#!/usr/bin/env python3
"""
Standardize non-modern templates to the Oswald/Crimson Text/Inter 'modern' template.
Preserves body content, replaces font imports and CSS variables.
Skips: formal-papers/, logos-papers/ (keep cormorant), _archive/, large generated files.
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
EXCLUDE = {'_archive', 'node_modules', '.git', 'Archive'}
KEEP_AS_IS = {'formal-papers', 'logos-papers', 'Logos_Papers'}

# Modern font import
MODERN_FONTS = '''<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600;700&family=Oswald:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"/>'''

# Modern CSS root variables
MODERN_CSS_VARS = """:root{
  --surface:#0a0a0a;
  --surface-light:#1a1a1a;
  --surface-hover:#2a2a2a;
  --surface2:#111;
  --surface3:#1f1f1f;
  --text-primary:#e0e0e0;
  --text-secondary:#a0a0a0;
  --text:#e0e0e0;
  --text-d:#a0a0a0;
  --text-m:#666;
  --highlight:#d4af37;
  --highlight-bright:#e8c547;
  --highlight-dim:#8b7a1e;
  --gold:#d4af37;
  --gold-dim:rgba(212,175,55,0.15);
  --gold-glow:rgba(212,175,55,0.06);
  --border:#333333;
  --teal:#2dd4bf;
  --blue:#4a9eff;
  --purple:#a855f7;
  --red:#ef4444;
  --green:#22c55e;
  --copper:#c17f3e;
}"""

# Font patterns to replace
FONT_PATTERNS = [
    # Source Serif 4
    re.compile(r'<link[^>]*Source\+Serif[^>]*/?>', re.IGNORECASE),
    # Cormorant Garamond
    re.compile(r'<link[^>]*Cormorant[^>]*/?>', re.IGNORECASE),
    # Courier Prime
    re.compile(r'<link[^>]*Courier\+Prime[^>]*/?>', re.IGNORECASE),
    # Generic google fonts link (not already modern)
    re.compile(r'<link[^>]*fonts\.googleapis\.com/css2\?family=[^>]*/?>', re.IGNORECASE),
]

# Preconnect patterns
PRECONNECT_RE = re.compile(r'<link\s+rel="preconnect"[^>]*/?>\s*', re.IGNORECASE)

# CSS variable replacements for Source Serif / Blue theme
SOURCE_SERIF_CSS = {
    "'Source Serif 4'": "'Crimson Text'",
    "Source Serif 4": "Crimson Text",
    '--bg:#020507': '--surface:#0a0a0a',
    '--surface:#07101a': '--surface-light:#1a1a1a',
    '--accent:#2563be': '--highlight:#d4af37',
    '--accent-l:#4d8fe0': '--highlight-bright:#e8c547',
    '--warm:#c49a40': '--gold:#d4af37',
}

# CSS variable replacements for Cormorant theme
CORMORANT_CSS = {
    "'Cormorant Garamond'": "'Crimson Text'",
    "Cormorant Garamond": "Crimson Text",
    '--accent-gold: #c9a962': '--highlight: #d4af37',
    '--accent-copper: #b87333': '--copper: #c17f3e',
}

def is_modern(content_head):
    """Check if file already uses the modern template."""
    return 'Oswald' in content_head and 'Crimson' in content_head

def get_series(path):
    """Get series name from file path."""
    rel = os.path.relpath(path, SITE_ROOT)
    parts = rel.split(os.sep)
    return parts[0] if len(parts) > 1 else 'root'

def detect_template(head):
    """Detect which template a file uses."""
    if 'Cormorant' in head:
        return 'cormorant'
    if 'Source Serif' in head:
        return 'source_serif'
    if 'Quartz' in head or 'index.css' in head:
        return 'quartz'
    return 'other'

def standardize_fonts(content):
    """Replace font imports with modern fonts."""
    # Remove existing preconnects
    content = PRECONNECT_RE.sub('', content)

    # Remove existing font links
    for pat in FONT_PATTERNS:
        content = pat.sub('', content)

    # Insert modern fonts after <meta name="viewport"...> or after <head>
    viewport_re = re.compile(r'(<meta\s+name="viewport"[^>]*/?>\s*)', re.IGNORECASE)
    m = viewport_re.search(content)
    if m:
        content = content[:m.end()] + '\n' + MODERN_FONTS + '\n' + content[m.end():]
    else:
        content = content.replace('<head>', '<head>\n' + MODERN_FONTS, 1)

    return content

def standardize_css_vars(content, template_type):
    """Replace CSS variables based on detected template."""
    if template_type == 'source_serif':
        for old, new in SOURCE_SERIF_CSS.items():
            content = content.replace(old, new)
    elif template_type == 'cormorant':
        for old, new in CORMORANT_CSS.items():
            content = content.replace(old, new)

    # Universal: make sure body uses Inter
    content = re.sub(
        r"font-family:\s*'Source Serif 4'[^;]*;",
        "font-family:'Inter',sans-serif;",
        content
    )
    content = re.sub(
        r"font-family:\s*'Cormorant Garamond'[^;]*;",
        "font-family:'Inter',sans-serif;",
        content
    )

    # Add .serif and .display utility classes if not present
    if '.serif{' not in content and '.display{' not in content:
        # Find first } in first <style> block and add after
        style_match = re.search(r'(<style[^>]*>)', content)
        if style_match:
            insert_pos = style_match.end()
            content = (content[:insert_pos] +
                      "\n.serif{font-family:'Crimson Text',serif;}" +
                      "\n.display{font-family:'Oswald',sans-serif;}" +
                      "\n.mono{font-family:'JetBrains Mono',monospace;}\n" +
                      content[insert_pos:])

    return content

def add_font_awesome(content):
    """Add Font Awesome if not present."""
    if 'font-awesome' not in content.lower() and 'fontawesome' not in content.lower():
        content = content.replace('</head>',
            '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"/>\n</head>', 1)
    return content

# Main loop
converted = 0
skipped = 0
errors = []

for root, dirs, files in os.walk(SITE_ROOT):
    dirs[:] = [d for d in dirs if d not in EXCLUDE]
    for fname in files:
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(root, fname)

        # Skip large files (generated/bundled)
        try:
            sz = os.path.getsize(fpath)
            if sz > 500000:
                continue
        except:
            continue

        series = get_series(fpath)
        if series in KEEP_AS_IS:
            continue

        try:
            with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except Exception as e:
            errors.append(f"READ: {fpath}: {e}")
            continue

        head_end = content.find('</head>')
        if head_end < 0:
            continue
        head = content[:head_end]

        if is_modern(head):
            continue

        template_type = detect_template(head)
        if template_type == 'quartz':
            skipped += 1
            continue

        original = content
        content = standardize_fonts(content)
        content = standardize_css_vars(content, template_type)
        content = add_font_awesome(content)

        if content != original:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            converted += 1
            rel = os.path.relpath(fpath, SITE_ROOT)
            print(f"  [{template_type}] {rel}")

print(f"\nConverted: {converted}")
print(f"Skipped (quartz): {skipped}")
if errors:
    print(f"Errors: {len(errors)}")
    for e in errors:
        print(f"  {e}")
