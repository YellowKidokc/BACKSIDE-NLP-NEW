"""
apply_topbar.py
Replaces any existing top nav bar and header with the Gold Edge topbar
+ Minimal Centered hero across all GTQ articles.
"""
import re, os, glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKIP_FILES = {'index.html','gtq-02-gold-preview.html','TEMPLATE.html','topbar-template.html',
              'normalize_articles.py','fix_players.py','apply_topbar.py'}

# Article ordering for prev/next links
ARTICLE_ORDER = [
    'gtq-01-measurement-collapsed-reality',
    'gtq-01a-collapse-threshold',
    'gtq-02-the-first-quantum-state',
    'gtq-03-free-will-two-frames',
    'gtq-03a-macarthur-and-the-equation',
    'gtq-03b-the-three-pathways',
    'gtq-03c-why-god-drowned-everybody',
    'gtq-04-the-day-time-began',
    'gtq-04a-the-decoherence-curve',
    'gtq-04b-how-lies-kill',
    'gtq-05-the-substrate-fractured',
    'gtq-05a-trinity-mechanism',
    'gtq-05b-trinity-timeline',
    'gtq-05c-why-physics-is-broken-in-two',
    'gtq-06-why-reality-needs-three',
    'gtq-07-the-photon-isnt-watching',
    'gtq-07a-empirical-testing',
    'gtq-08-god-doesnt-need-a-clock',
    'gtq-08a-the-temporal-trap',
    'gtq-08b-how-god-restores',
    'gtq-08c-science-behind-restoration',
    'gtq-09-same-god-both-testaments',
    'gtq-09a-regime-dependent-theology',
    'gtq-09b-civilizational-decay',
    'gtq-10-the-counter-move',
    'gtq-10a-why-the-pattern-is-the-signal',
]

ARTICLES = {
    'gtq-01-measurement-collapsed-reality': {'num':'01','title':'The Measurement That Collapsed Reality','sub':'A Theophysics Treatment of Genesis 2\u20133'},
    'gtq-01a-collapse-threshold': {'num':'01-A','title':'The Collapse Threshold','sub':'Why Eve\u2019s measurement didn\u2019t collapse reality, but Adam\u2019s did.'},
    'gtq-02-the-first-quantum-state': {'num':'02','title':'The First Quantum State','sub':'Eden as Coherent Superposition \u2014 The Physics of the Pre-Fall World'},
    'gtq-03-free-will-two-frames': {'num':'03','title':'Free Will in Two Frames','sub':'The Coherence Equation, the Calvinist\u2013Arminian Dissolution, and Three Pathways Through the Fall'},
    'gtq-03a-macarthur-and-the-equation': {'num':'03-A','title':'MacArthur and the Equation','sub':'Where Calvinism and Arminianism Meet in One Line of Mathematics'},
    'gtq-03b-the-three-pathways': {'num':'03-B','title':'The Three Pathways','sub':'What Your Brain Does at s = \u22121, s = 0, and s = +1'},
    'gtq-03c-why-god-drowned-everybody': {'num':'03-C','title':'Why God Drowned Everybody','sub':'And Why He Stopped'},
    'gtq-04-the-day-time-began': {'num':'04','title':'The Day Time Began','sub':'The Fall Didn\u2019t Happen in Time \u2014 The Fall Created Time'},
    'gtq-04a-the-decoherence-curve': {'num':'04-A','title':'The Decoherence Curve','sub':'What Happens When You Graph the Genesis Genealogies Against a Physics Equation'},
    'gtq-04b-how-lies-kill': {'num':'04-B','title':'How Lies Kill','sub':'The Mathematics of Sin'},
    'gtq-05-the-substrate-fractured': {'num':'05','title':'The Substrate Fractured','sub':'Why Quantum Mechanics Is Fallen Physics'},
    'gtq-05a-trinity-mechanism': {'num':'05-A','title':'The Trinity Mechanism','sub':'How Three Persons Actualize Every Moment'},
    'gtq-05b-trinity-timeline': {'num':'05-B','title':'The Trinity Timeline','sub':'Three Persons, Six Events, One Architecture'},
    'gtq-05c-why-physics-is-broken-in-two': {'num':'05-C','title':'Why Physics Is Broken in Two','sub':'And Why That\u2019s the Point'},
    'gtq-06-why-reality-needs-three': {'num':'06','title':'Why Reality Needs Three','sub':'The minimum number of operations to generate time is exactly three'},
    'gtq-07-the-photon-isnt-watching': {'num':'07','title':'Why the Photon Isn\u2019t Watching You Back','sub':'Consciousness Is Not a Bystander to Physics \u2014 It Is a Variable in the Equation'},
    'gtq-07a-empirical-testing': {'num':'07-A','title':'Empirical Testing of the Master Equation','sub':'A Computational Analysis of 16 Independent Predictions'},
    'gtq-08-god-doesnt-need-a-clock': {'num':'08','title':'The Eraser and the Cross','sub':'The Delayed-Choice Quantum Eraser Proves the Mechanism. The Cross Is the Mechanism at Full Scale.'},
    'gtq-08a-the-temporal-trap': {'num':'08-A','title':'The Temporal Trap','sub':'Why Satan Executed His Own Defeat'},
    'gtq-08b-how-god-restores': {'num':'08-B','title':'How God Restores','sub':'The Mechanics of Coherence Restoration'},
    'gtq-08c-science-behind-restoration': {'num':'08-C','title':'The Science Behind Restoration','sub':'Physical Mechanisms of Coherence Recovery'},
    'gtq-09-same-god-both-testaments': {'num':'09','title':'The Same God in Both Testaments','sub':'One Author, One Equation, and One Patient'},
    'gtq-09a-regime-dependent-theology': {'num':'09-A','title':'Regime-Dependent Theology','sub':'Why God Behaves Differently Across Testaments'},
    'gtq-09b-civilizational-decay': {'num':'09-B','title':'Isomorphism &amp; Civilizational Decay','sub':'Canaanite Spiritual Architecture and Modern Western Structures'},
    'gtq-10-the-counter-move': {'num':'10','title':'The Counter-Move','sub':'Seven Moves, Seven Counter-Moves \u2014 Why the Fix Must Go to the Same Depth as the Break'},
    'gtq-10a-why-the-pattern-is-the-signal': {'num':'10-A','title':'Why the Pattern Is the Signal','sub':'A Bayesian Response to the Mythicist Reference Class'},
}


def get_prev_next(slug):
    idx = ARTICLE_ORDER.index(slug)
    prev_slug = ARTICLE_ORDER[idx-1] if idx > 0 else ARTICLE_ORDER[-1]
    next_slug = ARTICLE_ORDER[idx+1] if idx < len(ARTICLE_ORDER)-1 else ARTICLE_ORDER[0]
    return prev_slug + '.html', next_slug + '.html'


def build_topbar(slug):
    info = ARTICLES[slug]
    prev_url, next_url = get_prev_next(slug)
    num = info['num']
    title = info['title']

    # Use just the short number for display (e.g. "03" or "03-A")
    # For the big number, strip the letter for tangents
    big_num = num.split('-')[0] if '-' in num else num

    return f'''<!-- \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 GOLD EDGE TOP BAR \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 -->
<div class="topbar-gold-edge" style="background:linear-gradient(90deg,rgba(212,175,55,.08) 0%,rgba(10,10,10,1) 30%);border-bottom:1px solid #2b2b2b;border-left:4px solid #d4af37;padding:0 1.5rem;height:52px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:60;">
  <div style="display:flex;align-items:center;gap:.75rem;">
    <div style="font-family:'Oswald',sans-serif;font-size:1.4rem;font-weight:700;color:#d4af37;line-height:1;">{num}</div>
    <div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:.55rem;letter-spacing:.2em;text-transform:uppercase;color:#d4af37;">Genesis to Quantum</div>
      <div style="font-family:'Crimson Text',serif;font-size:.95rem;color:#e0e0e0;font-weight:600;line-height:1.2;">{title}</div>
    </div>
  </div>
  <div style="display:flex;gap:.3rem;align-items:center;">
    <a href="index.html" style="display:inline-flex;align-items:center;gap:.4rem;height:36px;padding:0 .85rem;border-radius:8px;font-size:.72rem;font-weight:500;color:#a0a0a0;text-decoration:none;border:1px solid #2b2b2b;background:#181818;"><i class="fas fa-th-list"></i> Index</a>
    <a href="{prev_url}" style="width:36px;height:36px;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#a0a0a0;text-decoration:none;border:1px solid #2b2b2b;background:#181818;font-size:.8rem;"><i class="fas fa-arrow-left"></i></a>
    <a href="{next_url}" style="width:36px;height:36px;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#a0a0a0;text-decoration:none;border:1px solid #2b2b2b;background:#181818;font-size:.8rem;"><i class="fas fa-arrow-right"></i></a>
  </div>
</div>'''


def build_hero(slug):
    info = ARTICLES[slug]
    num = info['num']
    title = info['title']
    sub = info['sub']
    # Determine if tangent or main
    label_type = 'Tangent' if '-' in num else 'Article'

    return f'''<!-- \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 MINIMAL CENTERED HERO \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 -->
<header class="hero-minimal-centered" style="text-align:center;padding:2.5rem 2rem 2rem;border-bottom:1px solid #2b2b2b;">
  <div style="font-family:'JetBrains Mono',monospace;font-size:.68rem;letter-spacing:.25em;text-transform:uppercase;color:#d4af37;margin-bottom:1rem;">{label_type} {num} &middot; Genesis to Quantum</div>
  <h1 style="font-family:'Crimson Text',serif;font-size:clamp(2rem,4.5vw,3.2rem);font-weight:700;color:#fff;margin-bottom:.85rem;line-height:1.1;">{title}</h1>
  <p style="font-size:.92rem;color:#a0a0a0;max-width:700px;margin:0 auto .8rem;line-height:1.7;">{sub}</p>
  <div style="display:flex;justify-content:center;gap:1rem;flex-wrap:wrap;font-size:.8rem;color:#6e6e6e;margin-top:1rem;">
    <span><i class="fas fa-user" style="color:#d4af37;margin-right:.3rem;"></i>David Lowe</span>
    <span><i class="fas fa-calendar-alt" style="color:#d4af37;margin-right:.3rem;"></i>2026</span>
    <span><i class="fas fa-fingerprint" style="color:#d4af37;margin-right:.3rem;"></i>GTQ-{num}</span>
    <span style="padding:.25rem .6rem;background:rgba(212,175,55,.12);color:#d4af37;border-radius:.25rem;font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;">Draft</span>
  </div>
</header>'''


def remove_old_header(content):
    """Remove old nav bars and headers. Returns content with HEADER_PLACEHOLDER."""

    # Pattern: old simple nav bar (← Main Index | Genesis to Quantum ... ← Prev Next →)
    content = re.sub(
        r'<nav style="position:sticky;top:0;z-index:1000;background:#0a0a0a[^"]*"[^>]*>.*?</nav>\s*',
        '', content, flags=re.DOTALL)

    # Pattern: Gold Edge top bar (already applied)
    content = re.sub(
        r'<!-- ═+ GOLD EDGE TOP BAR ═+ -->\s*<div class="topbar-gold-edge"[^>]*>.*?</div>\s*',
        '', content, flags=re.DOTALL)

    # Pattern: chip-style top bar
    content = re.sub(
        r'<!-- ═+ TOP LINE ═+ -->\s*<nav style="height:48px[^"]*"[^>]*>.*?</nav>\s*',
        '', content, flags=re.DOTALL)

    # Pattern: old site-header
    content = re.sub(
        r'<!-- ═+ HEADER ═+ -->\s*<header class="site-header">.*?</header>\s*',
        '', content, flags=re.DOTALL)

    # Pattern: minimal centered hero (already applied)
    content = re.sub(
        r'<!-- ═+ (HERO|MINIMAL CENTERED HERO) ═+ -->\s*<header[^>]*class="hero-minimal-centered"[^>]*>.*?</header>\s*',
        '', content, flags=re.DOTALL)

    # Pattern: old hero-minimal-centered without comment
    content = re.sub(
        r'<!-- ═+ HERO \u2014 MINIMAL CENTERED ═+ -->\s*<header[^>]*style="text-align:center[^"]*"[^>]*>.*?</header>\s*',
        '', content, flags=re.DOTALL)

    # Pattern: compact tangent-style top nav (← Main Index | Genesis to Quantum)
    content = re.sub(
        r'<nav style="position:sticky;top:0;[^"]*"[^>]*>\s*<div[^>]*>\s*<a[^>]*>.*?Main Index.*?</nav>\s*',
        '', content, flags=re.DOTALL)

    # Pattern: compact hero (hero class div)
    content = re.sub(
        r'<div class="hero">\s*<span class="hero-tag">.*?</div>\s*(?=<div class="story"|<div class="tab)',
        '', content, flags=re.DOTALL)

    return content


def process_file(filepath):
    slug = os.path.basename(filepath).replace('.html','')
    if slug not in ARTICLES:
        print(f"  [SKIP] {slug} - not in article map")
        return

    info = ARTICLES[slug]
    print(f"  Processing {slug} ({info['num']})")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Remove old headers/navs
    content = remove_old_header(content)

    # Build new topbar + hero
    topbar = build_topbar(slug)
    hero = build_hero(slug)

    # Insert after <body...>
    content = re.sub(r'(<body[^>]*>)\s*', r'\1\n' + topbar + '\n\n' + hero + '\n\n', content, count=1)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"    [SAVED]")
    else:
        print(f"    [NO CHANGE]")


def main():
    html_files = sorted(glob.glob(os.path.join(SCRIPT_DIR, 'gtq-*.html')))
    print(f"Found {len(html_files)} files\n")
    for f in html_files:
        fn = os.path.basename(f)
        if fn in SKIP_FILES:
            continue
        process_file(f)
    print("\nDone!")


if __name__ == '__main__':
    main()
