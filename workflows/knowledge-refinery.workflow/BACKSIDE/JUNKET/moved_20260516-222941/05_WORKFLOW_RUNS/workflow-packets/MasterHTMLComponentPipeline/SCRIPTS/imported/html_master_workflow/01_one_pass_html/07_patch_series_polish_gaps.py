from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(r"C:\Users\lowes\OneDrive\Desktop\Cannon\genesis-to-quantum")
IMAGES = ROOT / "images"

ARTICLES = [
    ("GTQ-01", "The Measurement That Collapsed Reality", "gtq-01-measurement-collapsed-reality.html"),
    ("GTQ-01A", "The Collapse Threshold", "gtq-01a-collapse-threshold.html"),
    ("GTQ-02", "The First Quantum State", "gtq-02-the-first-quantum-state.html"),
    ("GTQ-03", "Free Will in Two Frames", "gtq-03-free-will-two-frames.html"),
    ("GTQ-03A", "MacArthur and the Equation", "gtq-03a-macarthur-and-the-equation.html"),
    ("GTQ-03B", "The Three Pathways", "gtq-03b-the-three-pathways.html"),
    ("GTQ-03C", "Why God Drowned Everybody", "gtq-03c-why-god-drowned-everybody.html"),
    ("GTQ-04", "The Day Time Began", "gtq-04-the-day-time-began.html"),
    ("GTQ-04A", "The Decoherence Curve", "gtq-04a-the-decoherence-curve.html"),
    ("GTQ-04B", "How Lies Kill", "gtq-04b-how-lies-kill.html"),
    ("GTQ-05", "The Substrate Fractured", "gtq-05-the-substrate-fractured.html"),
    ("GTQ-05A", "The Trinity Mechanism", "gtq-05a-trinity-mechanism.html"),
    ("GTQ-05B", "The Trinity Timeline", "gtq-05b-trinity-timeline.html"),
    ("GTQ-05C", "Why Physics Is Broken in Two", "gtq-05c-why-physics-is-broken-in-two.html"),
    ("GTQ-06", "Why Reality Needs Three", "gtq-06-why-reality-needs-three.html"),
    ("GTQ-07", "Why the Photon Isn't Watching You Back", "gtq-07-the-photon-isnt-watching.html"),
    ("GTQ-07A", "Empirical Testing of the Master Equation", "gtq-07a-empirical-testing.html"),
    ("GTQ-08", "The Eraser and the Cross", "gtq-08-god-doesnt-need-a-clock.html"),
    ("GTQ-08A", "The Temporal Trap", "gtq-08a-the-temporal-trap.html"),
    ("GTQ-08B", "How God Restores", "gtq-08b-how-god-restores.html"),
    ("GTQ-08C", "The Science Behind Restoration", "gtq-08c-science-behind-restoration.html"),
    ("GTQ-09", "The Same God in Both Testaments", "gtq-09-same-god-both-testaments.html"),
    ("GTQ-09A", "Regime-Dependent Theology", "gtq-09a-regime-dependent-theology.html"),
    ("GTQ-09B", "Isomorphism and Civilizational Decay", "gtq-09b-civilizational-decay.html"),
    ("GTQ-10", "The Counter-Move", "gtq-10-the-counter-move.html"),
    ("GTQ-10A", "Why the Pattern Is the Signal", "gtq-10a-why-the-pattern-is-the-signal.html"),
]

INFOGRAPHICS = {
    "GTQ-01": ("images/gtq-01-collapse-infographic.png", "Collapse Infographic", "Measurement turns a coherent possibility space into a definite, accountable state."),
    "GTQ-02": ("images/gtq-02-superposition-infographic.png", "Superposition Infographic", "Eden before the fracture is treated as coherent possibility, not a settled fallen state."),
    "GTQ-03": ("images/gtq-03-wavefunction-collapse-infographic.png", "Wavefunction Collapse Infographic", "Choice is framed as collapse viewed from the creature side and providence viewed from the eternal frame."),
    "GTQ-04": ("images/gtq-04-decoherence-curve-infographic.png", "Decoherence Curve", "The curve visualizes how record formation turns recoverable coherence into durable history."),
    "GTQ-05": ("images/gtq-05-gr-qm-incompatibility-infographic.png", "GR/QM Incompatibility", "The split between continuous geometry and discrete measurement becomes a symptom of a deeper fracture."),
    "GTQ-06": ("images/gtq-06-born-rule-triad-infographic.png", "Born Rule Triad", "The argument lives or dies on whether generation, structuring, and actualization remain genuinely distinct operations."),
    "GTQ-07": ("images/gtq-07-coherence-equation-infographic.png", "Coherence Equation", "The photon does not watch back; the issue is information, coupling, and the conditions of measurement."),
    "GTQ-08": ("images/gtq-08-delayed-choice-infographic.png", "Delayed Choice / Eraser", "The Cross is mapped to record erasure and restoration, not merely to a moral example."),
    "GTQ-09": ("images/gtq-09-boltzmann-entropy-infographic.png", "Entropy and Judgment", "Different covenantal regimes change the repair mechanism while leaving God's character constant."),
    "GTQ-10": ("images/gtq-10-one-story-two-states.png", "One Story, Two States", "The finale shows the same structure in fracture and restoration."),
}

SERIES_CSS = r"""
/* GTQ series polish: early nav, visual figures, slide galleries */
.gtq-series-rail{max-width:1120px;margin:1.25rem auto 2rem;padding:1rem 1.1rem;border:1px solid rgba(212,175,55,.28);border-radius:8px;background:rgba(212,175,55,.045);display:grid;grid-template-columns:1fr auto 1fr;gap:1rem;align-items:center}
.gtq-series-rail a,.gtq-series-rail .gtq-nav-disabled{min-height:42px;display:flex;align-items:center;gap:.55rem;padding:.55rem .8rem;border:1px solid rgba(255,255,255,.12);border-radius:7px;background:rgba(255,255,255,.035);color:var(--text-secondary,#b8b8b8);text-decoration:none;font-size:.82rem}
.gtq-series-rail a:hover{border-color:#d4af37;color:var(--text-primary,#f2f2f2)}
.gtq-series-rail .gtq-nav-next{justify-content:flex-end;color:#d4af37}
.gtq-series-rail .gtq-nav-disabled{opacity:.45}
.gtq-series-rail .gtq-series-position{text-align:center;font-family:'JetBrains Mono',monospace;font-size:.68rem;letter-spacing:.12em;text-transform:uppercase;color:#d4af37;white-space:nowrap}
.gtq-series-rail .gtq-series-title{display:block;margin-top:.25rem;font-family:'Crimson Text',serif;font-size:.95rem;letter-spacing:0;text-transform:none;color:var(--text-primary,#e8e0d0)}
.gtq-visual-figure,.gtq-slide-gallery{max-width:980px;margin:2rem auto;padding:1rem;border:1px solid rgba(212,175,55,.22);border-radius:8px;background:rgba(255,255,255,.025)}
.gtq-visual-figure img{width:100%;display:block;border-radius:6px;background:#080808}
.gtq-visual-figure figcaption{margin-top:.75rem;color:var(--text-secondary,#b8b8b8);font-size:.9rem;line-height:1.5}
.gtq-slide-gallery h2{margin:.25rem 0 .35rem;color:#d4af37;font-family:'Oswald',sans-serif;letter-spacing:.04em;text-transform:uppercase;font-size:1.05rem}
.gtq-slide-gallery p{color:var(--text-secondary,#b8b8b8);font-size:.9rem;margin:0 0 1rem}
.gtq-slide-strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:.75rem}
.gtq-slide-strip figure{margin:0;background:rgba(0,0,0,.25);border:1px solid rgba(255,255,255,.08);border-radius:7px;overflow:hidden}
.gtq-slide-strip img{width:100%;display:block;aspect-ratio:16/9;object-fit:cover}
.gtq-slide-strip figcaption{padding:.5rem .6rem;color:var(--text-secondary,#b8b8b8);font-size:.72rem}
.gtq-break-claim{max-width:980px;margin:2.5rem auto;padding:1.5rem;border:1px solid rgba(239,68,68,.32);border-left:4px solid #ef4444;border-radius:8px;background:rgba(239,68,68,.055)}
.gtq-break-claim h2{font-family:'Oswald',sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#fff;margin:0 0 .75rem;font-size:1.2rem}
.gtq-break-claim p,.gtq-break-claim li{color:var(--text-secondary,#c8c8c8);line-height:1.6}
.gtq-break-claim ul{margin:.75rem 0 0 1.25rem}
@media(max-width:720px){.gtq-series-rail{grid-template-columns:1fr}.gtq-series-rail .gtq-nav-next{justify-content:flex-start}.gtq-series-rail .gtq-series-position{text-align:left}.gtq-slide-strip{grid-template-columns:1fr 1fr}}
"""


def add_css(doc: str) -> str:
    if ".gtq-series-rail" in doc:
        return doc
    idx = doc.find("</style>")
    if idx == -1:
        idx = doc.find("</head>")
        return doc[:idx] + f"<style>\n{SERIES_CSS}\n</style>\n" + doc[idx:]
    return doc[:idx] + "\n" + SERIES_CSS + "\n" + doc[idx:]


def series_rail(i: int) -> str:
    slug, title, _ = ARTICLES[i]
    prev = ARTICLES[i - 1] if i > 0 else None
    nxt = ARTICLES[i + 1] if i < len(ARTICLES) - 1 else None
    prev_html = (
        f'<a class="gtq-nav-prev" href="{html.escape(prev[2])}"><i class="fas fa-arrow-left"></i><span>Previous: {html.escape(prev[1])}</span></a>'
        if prev
        else '<span class="gtq-nav-disabled"><i class="fas fa-arrow-left"></i><span>Start of series</span></span>'
    )
    next_html = (
        f'<a class="gtq-nav-next" href="{html.escape(nxt[2])}"><span>Next: {html.escape(nxt[1])}</span><i class="fas fa-arrow-right"></i></a>'
        if nxt
        else '<span class="gtq-nav-disabled"><span>End of series</span><i class="fas fa-arrow-right"></i></span>'
    )
    return f"""
<!-- GTQ SERIES RAIL -->
<nav class="gtq-series-rail" aria-label="Genesis to Quantum series navigation">
  {prev_html}
  <div class="gtq-series-position">Article {i + 1} of {len(ARTICLES)}<span class="gtq-series-title">{html.escape(slug)} · {html.escape(title)}</span></div>
  {next_html}
</nav>
<!-- END GTQ SERIES RAIL -->
"""


def add_series_rail(doc: str, i: int) -> str:
    block = series_rail(i)
    if "<!-- GTQ SERIES RAIL -->" in doc:
        return re.sub(r"<!-- GTQ SERIES RAIL -->.*?<!-- END GTQ SERIES RAIL -->", block, doc, count=1, flags=re.S)
    media_end = doc.find("</section>", doc.find('class="gtq-unified-player"'))
    if media_end != -1:
        return doc[: media_end + len("</section>")] + "\n" + block + doc[media_end + len("</section>") :]
    main_idx = doc.find("<main")
    if main_idx != -1:
        return doc[:main_idx] + block + doc[main_idx:]
    body_idx = doc.find("<body")
    body_close = doc.find(">", body_idx)
    return doc[: body_close + 1] + "\n" + block + doc[body_close + 1 :]


def localize_broken_infographics(doc: str) -> str:
    return re.sub(r'https://media\.faiththruphysics\.comimages/(gtq-[^"\']+\.(?:png|webp))', r"images/\1", doc)


def infographic_figure(slug: str) -> str:
    src, label, caption = INFOGRAPHICS[slug]
    return f"""
<!-- GTQ INFOGRAPHIC INSERT -->
<figure class="gtq-visual-figure">
  <img src="{html.escape(src)}" alt="{html.escape(slug + ' ' + label)}" loading="lazy">
  <figcaption><strong>{html.escape(label)}.</strong> {html.escape(caption)}</figcaption>
</figure>
<!-- END GTQ INFOGRAPHIC INSERT -->
"""


def add_infographic(doc: str, slug: str) -> str:
    if slug not in INFOGRAPHICS:
        return doc
    src = INFOGRAPHICS[slug][0]
    if src in doc and "<!-- GTQ INFOGRAPHIC INSERT -->" not in doc:
        return doc
    block = infographic_figure(slug)
    if "<!-- GTQ INFOGRAPHIC INSERT -->" in doc:
        return re.sub(r"<!-- GTQ INFOGRAPHIC INSERT -->.*?<!-- END GTQ INFOGRAPHIC INSERT -->", block, doc, count=1, flags=re.S)
    tab_idx = doc.find('class="tab-content')
    story_idx = doc.find('class="story"', tab_idx if tab_idx != -1 else 0)
    insert_at = -1
    if story_idx != -1:
        story_open_end = doc.find(">", story_idx)
        first_p_end = doc.find("</p>", story_open_end)
        first_h2 = doc.find("<h2", story_open_end)
        candidates = [x for x in [first_p_end + 4 if first_p_end != -1 else -1, first_h2] if x != -1]
        insert_at = min(candidates) if candidates else story_open_end + 1
    if insert_at == -1:
        insert_at = doc.find('<div class="bottom-nav"')
    if insert_at == -1:
        insert_at = doc.find("</body>")
    return doc[:insert_at] + "\n" + block + doc[insert_at:]


def slide_gallery(slug: str, title: str) -> str:
    folder = IMAGES / slug.lower()
    slides = sorted(folder.glob("slide_*.webp")) if folder.exists() else []
    if not slides:
        return ""
    figs = []
    for n, path in enumerate(slides, start=1):
        src = f"images/{slug.lower()}/{path.name}"
        figs.append(
            f'<figure><img src="{html.escape(src)}" alt="{html.escape(slug)} slide {n}" loading="lazy"><figcaption>Slide {n:02d}</figcaption></figure>'
        )
    return f"""
<!-- GTQ SLIDE GALLERY -->
<section class="gtq-slide-gallery" aria-label="{html.escape(slug)} slide deck">
  <h2>{html.escape(slug)} Slide Deck</h2>
  <p>{html.escape(title)} visual sequence. These are wired from the local slide images so the article has the same visual support as the deck.</p>
  <div class="gtq-slide-strip">
    {''.join(figs)}
  </div>
</section>
<!-- END GTQ SLIDE GALLERY -->
"""


def add_slide_gallery(doc: str, slug: str, title: str) -> str:
    if slug not in {f"GTQ-{n:02d}" for n in range(1, 11)}:
        return doc
    block = slide_gallery(slug, title)
    if not block:
        return doc
    if "<!-- GTQ SLIDE GALLERY -->" in doc:
        return re.sub(r"<!-- GTQ SLIDE GALLERY -->.*?<!-- END GTQ SLIDE GALLERY -->", block, doc, count=1, flags=re.S)
    idx = doc.find('<div class="bottom-nav"')
    if idx == -1:
        idx = doc.find("</main>")
    if idx == -1:
        idx = doc.find("</body>")
    return doc[:idx] + "\n" + block + doc[idx:]


GTQ07_BREAK = r"""
<!-- GTQ BREAK THIS CLAIM -->
<section class="gtq-break-claim" aria-label="Break this claim">
  <h2>Break This Claim</h2>
  <p><strong>Claim under pressure:</strong> the photon is not conscious, but measurement is still an information event with physical consequences. The article should survive both naive mysticism and reductive dismissal.</p>
  <ul>
    <li><strong>Break it if</strong> a standard account of measurement can explain every cited anomaly without any informational boundary condition beyond ordinary apparatus interaction.</li>
    <li><strong>Break it if</strong> the argument slides from "consciousness is not required for collapse" into "consciousness never matters in any physical system." The first is defensible; the second is stronger than the evidence.</li>
    <li><strong>Break it if</strong> PEAR/GCP-style data fail under clean preregistered replication or if the claimed effects disappear after multiple-comparison correction.</li>
  </ul>
</section>
<!-- END GTQ BREAK THIS CLAIM -->
"""


def add_gtq07_break(doc: str) -> str:
    if "<!-- GTQ BREAK THIS CLAIM -->" in doc:
        return re.sub(r"<!-- GTQ BREAK THIS CLAIM -->.*?<!-- END GTQ BREAK THIS CLAIM -->", GTQ07_BREAK, doc, count=1, flags=re.S)
    idx = doc.find("<!-- ----------------------------------------------------------------\n     SYSTEM AUDIT")
    if idx == -1:
        idx = doc.find('<section class="gtq-system-audit"')
    if idx == -1:
        idx = doc.find("</main>")
    return doc[:idx] + "\n" + GTQ07_BREAK + "\n" + doc[idx:]


GTQ06_OBJECTION = r"""
<div class="blue-box">
<span class="blabel">Physicist's Objection — Born Rule as Postulate</span>
<p>The strongest objection is fair: in standard quantum mechanics the Born Rule is usually introduced as a postulate, not derived from deeper dynamics. So the article should not claim that the Born Rule itself proves the Trinity. The narrower claim is that any working measurement account must still do three jobs: maintain a state space, specify a measurement basis or observable, and turn amplitudes into outcome weights. The Trinity bridge is strongest when it is framed as a cross-domain structural constraint, not as a derivation of Christian doctrine from one unexplained physics rule.</p>
</div>
"""


def strengthen_gtq06(doc: str) -> str:
    if "Physicist's Objection — Born Rule as Postulate" not in doc:
        anchor = '<span class="blabel">Born Rule Irreducibility</span>'
        box_end = doc.find("</div>", doc.find(anchor))
        if box_end != -1:
            doc = doc[: box_end + 6] + "\n\n" + GTQ06_OBJECTION + doc[box_end + 6 :]
    doc = doc.replace(
        "No formulation of quantum mechanics has ever derived the Born Rule from fewer than three components. Copenhagen, Many-Worlds, Bohmian, and Consistent Histories all require the state vector, measurement basis, and probability projection. The three-fold structure is interpretation-independent.",
        "The Born Rule is not a solved derivation in the usual textbook presentation; it is commonly taken as a postulate. That matters. The usable claim is more modest: across major interpretations, a complete measurement account still has to specify a state, a basis or observable, and a rule that turns amplitudes into outcome weights. The three-fold structure is therefore interpretation-resilient, even if the Born Rule itself remains foundationally contested.",
    )
    doc = doc.replace(
        "<li>If the Born Rule can be reformulated with only two irreducible components &mdash; if someone shows that two operations are sufficient to go from possibility to definite outcome &mdash; the three-fold necessity argument falls.</li>",
        "<li>If a successful foundation of quantum mechanics reduces measurement to two irreducible operations without smuggling in a basis, state space, or probability projection under another name, the three-fold necessity argument falls.</li>",
    )
    doc = doc.replace(
        "Physics calls them components of the Born Rule.<br/>Theology calls them Father, Son, and Holy Spirit.<br/>The equation is the same.",
        "Physics exposes the three jobs most clearly in the measurement rule.<br/>Theology names a triune source, ordering Word, and actualizing Spirit.<br/>The bridge is structural; it must remain falsifiable.",
    )
    return doc


def main() -> None:
    changed = []
    for i, (slug, title, filename) in enumerate(ARTICLES):
        path = ROOT / filename
        doc = path.read_text(encoding="utf-8", errors="replace")
        original = doc
        doc = add_css(doc)
        doc = localize_broken_infographics(doc)
        doc = add_series_rail(doc, i)
        doc = add_infographic(doc, slug)
        doc = add_slide_gallery(doc, slug, title)
        if slug == "GTQ-07":
            doc = add_gtq07_break(doc)
        if slug == "GTQ-06":
            doc = strengthen_gtq06(doc)
        if doc != original:
            path.write_text(doc, encoding="utf-8", newline="\n")
            changed.append(filename)
    print(f"changed={len(changed)}")
    for name in changed:
        print(name)


if __name__ == "__main__":
    main()
