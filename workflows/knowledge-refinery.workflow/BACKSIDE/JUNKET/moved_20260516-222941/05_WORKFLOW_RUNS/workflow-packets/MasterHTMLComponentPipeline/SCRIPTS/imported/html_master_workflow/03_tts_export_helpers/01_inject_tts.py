"""
TTS INJECTOR
Injects a floating TTS player into all HTML files.
Also pushes article text to ClipSync when play is pressed.
Run once — backs up originals to _ORIGINALS/ first.
"""
import os, shutil, re
from pathlib import Path

FOLDER = Path(r"C:\Users\lowes\Desktop\Html Export")
CLIPSYNC_API = "https://clipsync-api.davidokc28.workers.dev/api"
DEVICE_ID = "html-articles"

TTS_BLOCK = '''
<style>
#tts-bar {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 99999;
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(15,23,42,0.95);
  border: 1px solid rgba(99,102,241,0.4);
  border-radius: 50px;
  padding: 10px 18px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.5);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  color: #e2e8f0;
  font-size: 13px;
  backdrop-filter: blur(12px);
  transition: opacity 0.3s;
}
#tts-bar:hover { opacity: 1 !important; }
#tts-play  { cursor:pointer; width:36px; height:36px; border-radius:50%;
  background:linear-gradient(135deg,#6366f1,#8b5cf6);
  border:none; color:#fff; font-size:16px; display:flex;
  align-items:center; justify-content:center; flex-shrink:0;
  transition:transform 0.15s; }
#tts-play:hover { transform:scale(1.1); }
#tts-speed { background:transparent; border:1px solid rgba(255,255,255,0.2);
  color:#e2e8f0; border-radius:6px; padding:3px 6px; font-size:12px; cursor:pointer; }
#tts-label { font-size:11px; opacity:0.6; max-width:180px;
  white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
#tts-clip-btn { cursor:pointer; font-size:11px; opacity:0.5;
  background:none; border:none; color:#e2e8f0; padding:2px 6px;
  border-radius:4px; transition:opacity 0.2s; }
#tts-clip-btn:hover { opacity:1; background:rgba(255,255,255,0.1); }
</style>

<div id="tts-bar">
  <button id="tts-play" title="Play / Pause">&#9654;</button>
  <select id="tts-speed" title="Speed">
    <option value="0.8">0.8x</option>
    <option value="1" selected>1x</option>
    <option value="1.2">1.2x</option>
    <option value="1.5">1.5x</option>
    <option value="2">2x</option>
  </select>
  <span id="tts-label">Ready</span>
  <button id="tts-clip-btn" title="Send to ClipSync">&#128203;</button>
</div>

<script>
(function(){
  const API = "''' + CLIPSYNC_API + '''";
  const DEVICE = "''' + DEVICE_ID + '''";

  function getArticleText(){
    // Try to find the main content area
    const selectors = [
      '.markdown-preview',
      '.markdown-preview-view',
      '.markdown-rendered',
      '.view-content',
      'article',
      'main',
      '.content',
      '#content'
    ];
    for(const sel of selectors){
      const el = document.querySelector(sel);
      if(el && el.innerText && el.innerText.trim().length > 200){
        return el.innerText.replace(/\\s+/g,' ').trim();
      }
    }
    return document.body.innerText.slice(0, 50000).replace(/\\s+/g,' ').trim();
  }

  let utterance = null;
  let playing = false;
  let fullText = '';
  let charIndex = 0;

  const playBtn  = document.getElementById('tts-play');
  const speedSel = document.getElementById('tts-speed');
  const label    = document.getElementById('tts-label');
  const clipBtn  = document.getElementById('tts-clip-btn');

  function setLabel(txt){ label.textContent = txt.slice(0,60); }

  function speak(fromChar){
    if(!window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const chunk = fullText.slice(fromChar);
    utterance = new SpeechSynthesisUtterance(chunk);
    utterance.rate  = parseFloat(speedSel.value);
    utterance.pitch = 1;
    utterance.onboundary = (e) => {
      if(e.name === 'word'){
        charIndex = fromChar + e.charIndex;
        const word = fullText.slice(charIndex, charIndex+30).split(' ')[0];
        setLabel('Playing: ' + word + '...');
      }
    };
    utterance.onend = () => {
      playing = false;
      playBtn.innerHTML = '&#9654;';
      charIndex = 0;
      setLabel('Finished');
    };
    utterance.onerror = () => {
      playing = false;
      playBtn.innerHTML = '&#9654;';
      setLabel('Error — try again');
    };
    window.speechSynthesis.speak(utterance);
  }

  playBtn.addEventListener('click', () => {
    if(!fullText) fullText = getArticleText();
    if(!fullText){ setLabel('No content found'); return; }
    if(!playing){
      playing = true;
      playBtn.innerHTML = '&#9646;&#9646;';
      setLabel('Loading...');
      speak(charIndex);
    } else {
      playing = false;
      playBtn.innerHTML = '&#9654;';
      window.speechSynthesis.pause();
      setLabel('Paused');
    }
  });

  speedSel.addEventListener('change', () => {
    if(playing){
      window.speechSynthesis.cancel();
      speak(charIndex);
    }
  });

  clipBtn.addEventListener('click', () => {
    if(!fullText) fullText = getArticleText();
    const title = document.title || 'Article';
    setLabel('Sending to ClipSync...');
    fetch(API + '/clips/push', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({
        device_id: DEVICE,
        content: title + '\\n\\n' + fullText.slice(0,5000),
        type: 'text',
        device_type: 'html-article'
      })
    })
    .then(r => r.json())
    .then(() => setLabel('Sent to ClipSync!'))
    .catch(() => setLabel('ClipSync send failed'));
  });

  // Auto-fade bar after 4s
  setTimeout(() => {
    const bar = document.getElementById('tts-bar');
    if(bar) bar.style.opacity = '0.7';
  }, 4000);

})();
</script>
'''

# Backup originals
backup = FOLDER / "_ORIGINALS"
backup.mkdir(exist_ok=True)

html_files = sorted(FOLDER.glob("*.html"))
print(f"Injecting TTS into {len(html_files)} HTML files...")

ok = err = 0
for p in html_files:
    try:
        bak = backup / p.name
        if not bak.exists():
            shutil.copy2(str(p), str(bak))
        text = p.read_text(encoding='utf-8', errors='ignore')
        if 'tts-bar' in text:
            print(f"  SKIP (already injected): {p.name}")
            continue
        if '</body>' in text:
            text = text.replace('</body>', TTS_BLOCK + '\n</body>', 1)
        else:
            text += TTS_BLOCK
        p.write_text(text, encoding='utf-8')
        print(f"  OK: {p.name}")
        ok += 1
    except Exception as e:
        print(f"  ERR {p.name}: {e}")
        err += 1

print(f"\nDone: {ok} injected, {err} errors")
print(f"Originals backed up to: {backup}")
