"""
normalize_articles.py  (v2)
- REMOVES hamburger sidebar from all articles
- Ensures Honest Assessment section exists at bottom
- Keeps existing top nav bars intact

Usage: python normalize_articles.py
"""
import re, os, glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKIP_FILES = {'index.html', 'gtq-02-gold-preview.html', 'normalize_articles.py'}

# ─── Honest Assessment block ───
HONEST_ASSESSMENT_HTML = '''
      <!-- ═══ THE HONEST ASSESSMENT ═══ -->
      <hr style="border:none;border-top:2px solid var(--border, #333);margin:3rem 0;">

      <h2 style="text-align:center;font-size:2rem;margin-bottom:.5rem;font-family:'Crimson Text',serif,Georgia,serif;">The Honest Assessment</h2>
      <p style="text-align:center;font-size:.9rem;color:#a0a0a0;margin-bottom:2.5rem;">Every claim in this paper falls into one of three categories. This taxonomy is permanent.</p>

      <!-- WHAT WE GOT RIGHT -->
      <div style="background:linear-gradient(135deg,rgba(34,197,94,.08) 0%,rgba(34,197,94,.02) 100%);border:1px solid rgba(34,197,94,.25);border-left:5px solid #22c55e;border-radius:0 .75rem .75rem 0;padding:1.75rem 2rem;margin-bottom:1.5rem;">
        <div style="font-family:'Oswald',sans-serif;font-size:1.1rem;letter-spacing:.1em;text-transform:uppercase;color:#22c55e;margin-bottom:1rem;font-weight:700;">
          <i class="fas fa-check-circle" style="margin-right:.5rem;"></i>What We Got Right
        </div>
        <div style="padding:.75rem 1rem;margin-bottom:.5rem;border-radius:.375rem;border:1px solid rgba(34,197,94,.15);background:rgba(34,197,94,.04);">
          <strong style="color:#fff;">Placeholder &mdash; to be filled individually.</strong> This section will contain the claims from this paper that are well-supported by evidence.
        </div>
      </div>

      <!-- WHAT WE GOT WRONG -->
      <div style="background:linear-gradient(135deg,rgba(239,68,68,.08) 0%,rgba(239,68,68,.02) 100%);border:1px solid rgba(239,68,68,.25);border-left:5px solid #ef4444;border-radius:0 .75rem .75rem 0;padding:1.75rem 2rem;margin-bottom:1.5rem;">
        <div style="font-family:'Oswald',sans-serif;font-size:1.1rem;letter-spacing:.1em;text-transform:uppercase;color:#ef4444;margin-bottom:1rem;font-weight:700;">
          <i class="fas fa-times-circle" style="margin-right:.5rem;"></i>What We Got Wrong
        </div>
        <div style="padding:.75rem 1rem;margin-bottom:.5rem;border-radius:.375rem;border:1px solid rgba(239,68,68,.15);background:rgba(239,68,68,.04);">
          <strong style="color:#fff;">Placeholder &mdash; to be filled individually.</strong> This section will contain claims that turned out to be incorrect or unsupported.
        </div>
      </div>

      <!-- WHERE WE OVERCLAIMED -->
      <div style="background:linear-gradient(135deg,rgba(212,175,55,.08) 0%,rgba(212,175,55,.02) 100%);border:1px solid rgba(212,175,55,.25);border-left:5px solid #d4af37;border-radius:0 .75rem .75rem 0;padding:1.75rem 2rem;margin-bottom:1.5rem;">
        <div style="font-family:'Oswald',sans-serif;font-size:1.1rem;letter-spacing:.1em;text-transform:uppercase;color:#d4af37;margin-bottom:1rem;font-weight:700;">
          <i class="fas fa-exclamation-triangle" style="margin-right:.5rem;"></i>Where We Overclaimed
        </div>
        <div style="padding:.75rem 1rem;margin-bottom:.5rem;border-radius:.375rem;border:1px solid rgba(212,175,55,.15);background:rgba(212,175,55,.04);">
          <strong style="color:#fff;">Placeholder &mdash; to be filled individually.</strong> This section will contain claims where the evidence is suggestive but the language went too far.
        </div>
      </div>
'''


def remove_sidebar(content):
    """Remove all sidebar-related HTML: toggle buttons, overlays, and nav/div sidebars."""
    # Remove sidebar toggle button (various patterns)
    content = re.sub(
        r'<button class="sidebar-toggle"[^>]*>.*?</button>\s*',
        '', content, flags=re.DOTALL)
    content = re.sub(
        r'<div class="sidebar-toggle"[^>]*>.*?</div>\s*',
        '', content, flags=re.DOTALL)

    # Remove sidebar overlay
    content = re.sub(
        r'<div class="sidebar-overlay"[^>]*>.*?</div>\s*',
        '', content, flags=re.DOTALL)

    # Remove <nav class="sidebar" ...>...</nav>
    content = re.sub(
        r'<nav class="sidebar"[^>]*>.*?</nav>\s*',
        '', content, flags=re.DOTALL)

    # Remove <div class="sidebar" id="sidebar">...</div> (compact format)
    # This one is tricky because div can nest. Use a targeted approach:
    # Find the opening tag, then find matching close
    content = re.sub(
        r'<div\s+class="sidebar"\s+id="sidebar"[^>]*>.*?</div>\s*(?:</div>\s*)?',
        '', content, flags=re.DOTALL)

    # Remove toggleSidebar function
    content = re.sub(
        r'function toggleSidebar\(\)\s*\{[^}]*\}\s*',
        '', content)

    # Remove sidebar CSS rules (canonical block)
    content = re.sub(
        r'/\* ─+ SIDEBAR NAV \(canonical\) ─+ \*/.*?(?=\n/\*|\n</style>)',
        '', content, flags=re.DOTALL)

    # Remove old sidebar CSS (.sidebar{...} blocks) - be careful not to remove too much
    # Just remove the toggle hover and overlay CSS
    content = re.sub(r'\.sidebar-toggle:hover\{[^}]*\}\s*', '', content)
    content = re.sub(r'\.sidebar-overlay\{[^}]*\}\s*', '', content)
    content = re.sub(r'\.sidebar-overlay\.show\{[^}]*\}\s*', '', content)

    # Clean up empty script tags that might remain
    content = re.sub(r'<script>\s*</script>', '', content)

    return content


def has_honest_assessment(content):
    """Check if the honest assessment section already exists."""
    return 'The Honest Assessment' in content


def inject_honest_assessment(content):
    """Inject the honest assessment section before the final closing tags."""
    if has_honest_assessment(content):
        return content, False

    # Try: before the bottom nav or footer
    for marker in ['<div class="bottom-nav"', '<footer', '<div class="foot"']:
        if marker in content:
            content = content.replace(marker, HONEST_ASSESSMENT_HTML + '\n' + marker, 1)
            return content, True

    # Fallback: insert before </body>
    content = content.replace('</body>', HONEST_ASSESSMENT_HTML + '\n</body>', 1)
    return content, True


def ensure_font_awesome(content):
    """Ensure Font Awesome is loaded (needed for honest assessment icons)."""
    if 'font-awesome' in content.lower():
        return content
    fa_link = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"/>'
    content = content.replace('</head>', fa_link + '\n</head>', 1)
    return content


def process_file(filepath):
    """Process a single HTML file."""
    filename = os.path.basename(filepath)
    print(f"  Processing {filename}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Ensure Font Awesome
    content = ensure_font_awesome(content)

    # 2. Remove sidebar (hamburger, overlay, nav)
    had_sidebar = 'sidebar' in content.lower() and ('sidebar-toggle' in content or 'id="sidebar"' in content)
    content = remove_sidebar(content)
    if had_sidebar:
        print("    [OK] Sidebar removed")

    # 3. Inject Honest Assessment if missing
    content, added_ha = inject_honest_assessment(content)
    if added_ha:
        print("    [OK] Honest Assessment injected")
    else:
        print("    [skip] Honest Assessment already present")

    # Write back
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"    [SAVED] {filename}")
    else:
        print(f"    [NO CHANGE] {filename}")


def main():
    html_files = glob.glob(os.path.join(SCRIPT_DIR, 'gtq-*.html'))
    print(f"Found {len(html_files)} GTQ HTML files\n")

    for filepath in sorted(html_files):
        filename = os.path.basename(filepath)
        if filename in SKIP_FILES:
            continue
        process_file(filepath)

    print("\nDone!")


if __name__ == '__main__':
    main()
