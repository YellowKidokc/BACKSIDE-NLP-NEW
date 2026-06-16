#!/usr/bin/env python3
"""Inject a sticky series ribbon (top nav bar) into articles that don't have one."""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
EXCLUDE = {'_archive', 'node_modules', '.git', 'Archive'}
SKIP_SERIES = {'formal-papers', 'logos-papers', 'Logos_Papers'}

# Series display names and accent colors
SERIES_CONFIG = {
    'be-glad-youre-a-loser':    ('Be Glad You\'re a Loser',        '#22c55e'),  # green
    'bible-datalab':            ('Bible DataLab',                   '#4a9eff'),  # blue
    'blue':                     ('Blue Series',                     '#4a9eff'),  # blue
    'consciousness':            ('Consciousness',                   '#a855f7'),  # purple
    'convergence-deep':         ('Convergence Deep',                '#c17f3e'),  # copper
    'Convergence_Series':       ('Convergence Series',              '#c17f3e'),  # copper
    'cross-domain':             ('Cross-Domain Coherence',          '#2dd4bf'),  # teal
    'duality-project':          ('The Duality Project',             '#e88fa5'),  # rose
    'family-tests':             ('Family Tests',                    '#22c55e'),  # green
    'genesis-to-quantum':       ('Genesis to Quantum',              '#d4af37'),  # gold
    'master-equation':          ('Master Equation',                 '#ef4444'),  # red
    'moral-decline':            ('Moral Decline of America',        '#ef4444'),  # red
    'one-page-stories':         ('One-Page Stories',                '#d4af37'),  # gold
    'proof-architecture':       ('Proof Architecture',              '#a855f7'),  # purple
    'proof-explorer':           ('Proof Explorer',                  '#a855f7'),  # purple
    'prophetic-synthesis':      ('Prophetic Synthesis',             '#e8c547'),  # bright gold
    'revolution-of-truth':      ('The Revolution of Truth',         '#ef4444'),  # red
    'socratic-axioms':          ('Socratic Axioms',                 '#2dd4bf'),  # teal
    'spiritual-warfare':        ('Spiritual Warfare',               '#ef4444'),  # red
    'the-bidirectional-audit':  ('The Bidirectional Audit',         '#4a9eff'),  # blue
    'root':                     ('Theophysics',                     '#d4af37'),  # gold
}


def build_ribbon(series, accent):
    name = SERIES_CONFIG.get(series, (series, '#d4af37'))[0]
    color = SERIES_CONFIG.get(series, (series, '#d4af37'))[1]
    return f'''<nav class="tp-ribbon" style="position:sticky;top:0;z-index:1000;background:#0a0a0a;border-bottom:2px solid {color}33;padding:.5rem 1.5rem;display:flex;align-items:center;justify-content:space-between;font-family:'Inter',sans-serif;font-size:.8rem;">
  <div style="display:flex;gap:1rem;align-items:center;">
    <a href="/index.html" style="color:#999;text-decoration:none;transition:color .2s;" onmouseover="this.style.color='{color}'" onmouseout="this.style.color='#999'">&larr; Main Index</a>
    <span style="color:#333;">|</span>
    <span style="color:{color};font-weight:500;">{name}</span>
  </div>
</nav>'''


injected = 0
skipped = 0

for root, dirs, files in os.walk(SITE_ROOT):
    dirs[:] = [d for d in dirs if d not in EXCLUDE]
    for fname in files:
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(root, fname)

        try:
            if os.path.getsize(fpath) > 500000:
                continue
        except:
            continue

        rel = os.path.relpath(fpath, SITE_ROOT)
        parts = rel.split(os.sep)
        series = parts[0] if len(parts) > 1 else 'root'

        if series in SKIP_SERIES:
            continue

        # Skip index files
        if fname in ('index.html', 'index-backup.html', 'index-gtq.html',
                     'image-registry.html', '_ring-template.html'):
            continue
        if 'gallery' in fname.lower():
            continue

        try:
            content = open(fpath, 'r', encoding='utf-8', errors='replace').read()
        except:
            continue

        if '<body>' not in content and '<body ' not in content:
            continue

        # Already has a ribbon or top nav
        if 'tp-ribbon' in content or ('Main Index' in content and 'sticky' in content):
            skipped += 1
            continue

        # Build and inject ribbon right after <body> or <body ...>
        ribbon = build_ribbon(series, SERIES_CONFIG.get(series, (series, '#d4af37'))[1])

        # Handle <body> with or without attributes
        body_match = re.search(r'<body[^>]*>', content)
        if not body_match:
            continue

        insert_pos = body_match.end()
        content = content[:insert_pos] + '\n' + ribbon + '\n' + content[insert_pos:]

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)

        injected += 1
        print(f'  {rel}')

print(f'\nRibbons injected: {injected}')
print(f'Already had nav: {skipped}')
