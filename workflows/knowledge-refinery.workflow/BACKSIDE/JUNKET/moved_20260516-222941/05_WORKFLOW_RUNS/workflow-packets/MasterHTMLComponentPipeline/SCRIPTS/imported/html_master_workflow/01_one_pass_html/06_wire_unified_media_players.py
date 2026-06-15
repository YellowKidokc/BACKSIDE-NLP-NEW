from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VIDEO_ROOT = ROOT / "Video"

CANONICAL = {
    "gtq-01-measurement-collapsed-reality.html": "GTQ-01",
    "gtq-01a-collapse-threshold.html": "GTQ-01A",
    "gtq-02-the-first-quantum-state.html": "GTQ-02",
    "gtq-03-free-will-two-frames.html": "GTQ-03",
    "gtq-03a-macarthur-and-the-equation.html": "GTQ-03A",
    "gtq-03b-the-three-pathways.html": "GTQ-03B",
    "gtq-03c-why-god-drowned-everybody.html": "GTQ-03C",
    "gtq-04-the-day-time-began.html": "GTQ-04",
    "gtq-04a-the-decoherence-curve.html": "GTQ-04A",
    "gtq-04b-how-lies-kill.html": "GTQ-04B",
    "gtq-05-the-substrate-fractured.html": "GTQ-05",
    "gtq-05a-trinity-mechanism.html": "GTQ-05A",
    "gtq-05b-trinity-timeline.html": "GTQ-05B",
    "gtq-05c-why-physics-is-broken-in-two.html": "GTQ-05C",
    "gtq-06-why-reality-needs-three.html": "GTQ-06",
    "gtq-07-the-photon-isnt-watching.html": "GTQ-07",
    "gtq-07a-empirical-testing.html": "GTQ-07A",
    "gtq-08-god-doesnt-need-a-clock.html": "GTQ-08",
    "gtq-08a-the-temporal-trap.html": "GTQ-08A",
    "gtq-08b-how-god-restores.html": "GTQ-08B",
    "gtq-08c-science-behind-restoration.html": "GTQ-08C",
    "gtq-09-same-god-both-testaments.html": "GTQ-09",
    "gtq-09a-regime-dependent-theology.html": "GTQ-09A",
    "gtq-09b-civilizational-decay.html": "GTQ-09B",
    "gtq-10-the-counter-move.html": "GTQ-10",
    "gtq-10a-why-the-pattern-is-the-signal.html": "GTQ-10A",
}


CSS = """/* UNIFIED ARTICLE PLAYER */
.gtq-unified-player{
  grid-column:1/-1;
  margin:0 0 2rem;
  border:1px solid rgba(212,175,55,.24);
  border-radius:.75rem;
  overflow:hidden;
  background:linear-gradient(180deg,rgba(255,255,255,.045),rgba(255,255,255,.015));
}
.gtq-unified-player .player-shell{display:grid;grid-template-columns:minmax(0,1.7fr) minmax(280px,.8fr);}
.gtq-unified-player .player-stage{min-height:280px;background:#000;display:flex;align-items:center;justify-content:center;}
.gtq-unified-player video,.gtq-unified-player audio{width:100%;display:block;background:#000;}
.gtq-unified-player video{max-height:520px;}
.gtq-unified-player audio{padding:2rem;background:rgba(0,0,0,.9);}
.gtq-unified-player .player-panel{padding:1.25rem;border-left:1px solid var(--border);display:flex;flex-direction:column;gap:.85rem;}
.gtq-unified-player .player-eyebrow{font-family:'JetBrains Mono',monospace;font-size:.65rem;letter-spacing:.16em;text-transform:uppercase;color:var(--highlight);}
.gtq-unified-player .player-title{margin:0;font-family:'Oswald',sans-serif;font-size:1.35rem;color:#fff;line-height:1.1;}
.gtq-unified-player .player-note{margin:0;color:var(--text-secondary);font-size:.82rem;line-height:1.5;}
.gtq-unified-player .player-options{display:grid;gap:.55rem;margin-top:.25rem;}
.gtq-unified-player .player-option{width:100%;display:flex;align-items:center;justify-content:space-between;gap:.75rem;padding:.75rem .85rem;border:1px solid var(--border);border-radius:.45rem;background:var(--surface-light);color:var(--text-secondary);cursor:pointer;text-align:left;transition:all .2s ease;}
.gtq-unified-player .player-option:hover,.gtq-unified-player .player-option.active{color:#fff;border-color:var(--highlight);background:rgba(212,175,55,.08);}
.gtq-unified-player .player-option[disabled]{opacity:.42;cursor:not-allowed;}
.gtq-unified-player .option-main{display:flex;align-items:center;gap:.65rem;font-weight:600;}
.gtq-unified-player .option-meta{font-family:'JetBrains Mono',monospace;font-size:.62rem;color:var(--text-secondary);text-transform:uppercase;letter-spacing:.08em;}
@media(max-width:900px){
  .gtq-unified-player .player-shell{grid-template-columns:1fr;}
  .gtq-unified-player .player-panel{border-left:0;border-top:1px solid var(--border);}
}
"""


JS = """<script>
/* Unified article media player */
(function(){
  var players=document.querySelectorAll('.gtq-unified-player');
  players.forEach(function(player){
    var video=player.querySelector('.gtqUnifiedVideo');
    var audio=player.querySelector('.gtqUnifiedAudio');
    var title=player.querySelector('.gtqUnifiedTitle');
    var note=player.querySelector('.gtqUnifiedNote');
    var buttons=player.querySelectorAll('.player-option');
    if(!video || !audio || !buttons.length) return;
    function setSource(button){
      if(button.disabled) return;
      var kind=button.dataset.kind;
      var src=button.dataset.src;
      if(!kind || !src) return;
      video.pause();
      audio.pause();
      buttons.forEach(function(btn){btn.classList.remove('active');});
      button.classList.add('active');
      title.textContent=button.dataset.title || 'Article Media';
      note.textContent=button.dataset.note || '';
      if(kind==='video'){
        audio.style.display='none';
        video.style.display='block';
        if(video.currentSrc.indexOf(src)===-1){
          video.querySelector('source').src=src;
          video.load();
        }
      }else{
        video.style.display='none';
        audio.style.display='block';
        if(audio.currentSrc.indexOf(src)===-1){
          audio.querySelector('source').src=src;
          audio.load();
        }
      }
    }
    buttons.forEach(function(button){
      button.addEventListener('click',function(){setSource(button);});
    });
  });
})();
</script>
"""


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def best_video(slug: str) -> Path | None:
    video_dir = VIDEO_ROOT / slug / "video"
    if not video_dir.exists():
        return None
    preferred = [
        video_dir / f"{slug}-V-FULL.mp4",
        video_dir / f"{slug}-V-EVERYDAY.mp4",
        video_dir / f"{slug}-V-SLIDES.mp4",
        video_dir / f"{slug}-V.mp4",
    ]
    for candidate in preferred:
        if candidate.exists():
            return candidate
    files = sorted(video_dir.glob("*.mp4"), key=lambda p: p.stat().st_size, reverse=True)
    return files[0] if files else None


def audio(slug: str, kind: str) -> Path | None:
    candidate = VIDEO_ROOT / slug / "audio" / f"{slug}-{kind}.mp3"
    return candidate if candidate.exists() else None


def h1_title(text: str, slug: str) -> str:
    match = re.search(r"<h1[^>]*>(.*?)</h1>", text, flags=re.S | re.I)
    if not match:
        return slug
    return re.sub(r"<.*?>", "", match.group(1)).strip() or slug


def button(label: str, icon: str, meta: str, kind: str | None, src: Path | None, title: str, note: str, active: bool = False) -> str:
    classes = "player-option active" if active else "player-option"
    if not src or not kind:
        return (
            f'        <button class="player-option" type="button" disabled data-title="{html.escape(title)}" data-note="{html.escape(note)}">\n'
            f'          <span class="option-main"><i class="fas {icon}"></i> {html.escape(label)}</span><span class="option-meta">Soon</span>\n'
            "        </button>"
        )
    return (
        f'        <button class="{classes}" type="button" data-kind="{kind}" data-src="{html.escape(rel(src))}" data-title="{html.escape(title)}" data-note="{html.escape(note)}">\n'
        f'          <span class="option-main"><i class="fas {icon}"></i> {html.escape(label)}</span><span class="option-meta">{meta}</span>\n'
        "        </button>"
    )


def player_html(slug: str, title: str) -> str:
    v = best_video(slug)
    tts = audio(slug, "TTS")
    dd = audio(slug, "DD")
    debate = audio(slug, "DEBATE")
    first_title = "Executive Summary Video" if v else "TTS Read Aloud"
    first_note = f"The article video for {slug}." if v else "Clean article narration for TTS review."
    video_source = rel(v) if v else ""
    audio_source = rel(tts or dd or debate) if (tts or dd or debate) else ""
    poster = f"images/{slug.lower()}.webp"
    active_video = v is not None
    return f"""
<section class="gtq-unified-player" aria-label="Article media player">
  <div class="player-shell">
    <div class="player-stage">
      <video class="gtqUnifiedVideo" controls preload="metadata" playsinline poster="{poster}"{'' if v else ' style="display:none;"'}>
        <source src="{html.escape(video_source)}" type="video/mp4">
        Your browser does not support video playback.
      </video>
      <audio class="gtqUnifiedAudio" controls preload="metadata"{' style="display:none;"' if v else ''}>
        <source src="{html.escape(audio_source)}" type="audio/mpeg">
        Your browser does not support audio playback.
      </audio>
    </div>
    <div class="player-panel">
      <div class="player-eyebrow">Watch &amp; Listen</div>
      <h2 class="player-title gtqUnifiedTitle">{html.escape(first_title)}</h2>
      <p class="player-note gtqUnifiedNote">{html.escape(first_note)} One player for this article's video, TTS, deep dive, and debate audio.</p>
      <div class="player-options">
{button("Video", "fa-play-circle", "MP4", "video", v, "Executive Summary Video", f"The article video for {slug}.", active=active_video)}
{button("TTS", "fa-volume-up", "MP3", "audio", tts, "TTS Read Aloud", "Clean article narration for TTS review.", active=not active_video and tts is not None)}
{button("Deep Dive", "fa-headphones", "MP3", "audio", dd, "Deep Dive", f"Long-form deep dive audio for {slug}.")}
{button("Debate", "fa-comments", "MP3", "audio", debate, "Debate", f"Debate audio for {slug}.")}
      </div>
    </div>
  </div>
</section>
""".strip()


def remove_old_summary_video(text: str) -> str:
    return re.sub(
        r"\n?<!-- ARTICLE VIDEO -->\s*<figure class=\"article-fig\".*?</figure>\s*<!-- END ARTICLE VIDEO -->\s*",
        "\n",
        text,
        flags=re.S,
    )


def wire(path: Path, slug: str) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    title = h1_title(text, slug)

    if "/* UNIFIED ARTICLE PLAYER */" not in text:
        text = text.replace("</style>", CSS + "\n</style>", 1)
    text = re.sub(
        r"\n?<script>\s*/\* Unified article media player \*/.*?</script>\s*",
        "\n",
        text,
        flags=re.S,
    )
    text = text.replace("</body>", JS + "\n</body>", 1)

    text = remove_old_summary_video(text)
    text = re.sub(r"\n?<section class=\"gtq-unified-player\".*?</section>\s*", "\n", text, flags=re.S)
    block = player_html(slug, title)
    if "<!-- END HERO IMAGE -->" in text:
        text = text.replace("<!-- END HERO IMAGE -->", "<!-- END HERO IMAGE -->\n\n" + block, 1)
    else:
        new_text = re.sub(
            r'(<main\b[^>]*class="[^"]*\bmain-layout\b[^"]*"[^>]*>)',
            r"\1\n" + block,
            text,
            count=1,
        )
        if new_text == text:
            new_text = re.sub(r"(<body[^>]*>)", r"\1\n" + block, text, count=1, flags=re.I)
        text = new_text

    path.write_text(text, encoding="utf-8", newline="\n")
    v = "video" if best_video(slug) else "no-video"
    parts = [k for k in ["TTS", "DD", "DEBATE"] if audio(slug, k)]
    return f"{path.name}: {slug} {v} audio={','.join(parts) if parts else 'none'}"


def main() -> int:
    for name, slug in CANONICAL.items():
        path = ROOT / name
        if not path.exists():
            print(f"missing page {name}")
            continue
        print(wire(path, slug))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
