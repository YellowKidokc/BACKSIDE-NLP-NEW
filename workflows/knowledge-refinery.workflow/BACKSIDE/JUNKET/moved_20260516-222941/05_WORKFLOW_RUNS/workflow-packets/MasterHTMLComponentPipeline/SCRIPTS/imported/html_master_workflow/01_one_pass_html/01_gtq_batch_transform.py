#!/usr/bin/env python3
"""
GTQ Batch Transform - 4 operations across all 26 articles
POF 2828 | May 8, 2026

Operations:
  1. HERO REORDER - Move hero grid below topbar
  2. REMOVE WATCH & LISTEN TAB - Strip media tab button + section
  3. SIDEBAR COLLAPSE - Add toggle button, CSS, JS
  4. VIDEO BREAKOUT - Widen video when sidebar collapsed

Usage:
  python gtq_batch_transform.py                      # dry-run
  python gtq_batch_transform.py --apply              # apply all
  python gtq_batch_transform.py --apply --single 01  # single article
"""
import os, sys, re, shutil, argparse
from datetime import datetime
from pathlib import Path
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("pip install beautifulsoup4"); sys.exit(1)

ARTICLES_DIR = Path(r"D:\GTQ-BUILD\articles")
BACKUP_DIR = ARTICLES_DIR / "_transform_backups"

SIDEBAR_CSS = """
/* === SIDEBAR COLLAPSE (batch) === */
.main-layout{transition:all .35s ease;}
.main-layout.sidebar-collapsed{grid-template-columns:1fr;max-width:960px;}
.main-layout.sidebar-collapsed .kill-sidebar,
.main-layout.sidebar-collapsed .article-sidebar{display:none;}
.sidebar-collapse-btn{position:fixed;right:1.2rem;bottom:5rem;z-index:90;width:36px;height:36px;border-radius:50%;border:1px solid var(--border,#2a2a2a);background:var(--surface-light,#1a1a1a);color:var(--text-secondary,#999);font-size:.75rem;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .2s;box-shadow:0 4px 16px rgba(0,0,0,.4);}
.sidebar-collapse-btn:hover{border-color:var(--highlight,#d4af37);color:var(--highlight,#d4af37);background:rgba(212,175,55,.08);}
.main-layout.sidebar-collapsed .summary-video-card{width:min(1280px,calc(100% + 16rem));margin-left:-8rem;margin-right:-8rem;}
@media(max-width:1024px){.sidebar-collapse-btn{display:none;}}
/* === END SIDEBAR COLLAPSE === */
"""

SIDEBAR_HTML = """<!-- Sidebar collapse (batch) -->
<button class="sidebar-collapse-btn" onclick="toggleKillSidebar()" title="Toggle sidebar" id="sidebarCollapseBtn">&#x25a8;</button>
<script>
function toggleKillSidebar(){
  var ml=document.querySelector('.main-layout');
  if(!ml)return;
  ml.classList.toggle('sidebar-collapsed');
  document.getElementById('sidebarCollapseBtn').title=
    ml.classList.contains('sidebar-collapsed')?'Show sidebar':'Hide sidebar';
}
</script>
"""

def find_html(d):
    for f in sorted(d.iterdir()):
        if f.suffix=='.html' and f.stem.startswith('gtq-') and not any(x in f.stem for x in ['labeled','bak','backup']):
            return f
    return None

def read_raw(p):
    raw=p.read_bytes(); return raw.decode('utf-8'), raw

def detect_eol(raw):
    cr=raw.count(b'\r\n'); lf=raw.count(b'\n')-cr
    return '\r\n' if cr>lf else '\n'

def write_out(p, text, eol):
    t=text.replace('\r\n','\n')
    if eol=='\r\n': t=t.replace('\n','\r\n')
    p.write_bytes(t.encode('utf-8'))

def op_hero(text):
    ch=[]
    m=re.search(r'(<!-- BEGIN: HERO -->.*?<!-- END: HERO -->)',text,re.DOTALL)
    if not m: return text,["SKIP: no HERO markers"]
    hero=m.group(1); hs=m.start()
    t=re.search(r'<!-- END: TOPBAR -->',text)
    if not t: return text,["SKIP: no TOPBAR end"]
    if hs<t.end()+100: return text,["SKIP: hero already after topbar"]
    text2=text[:m.start()]+text[m.end():]
    t2=re.search(r'<!-- END: TOPBAR -->',text2)
    ip=t2.end()
    sn=re.search(r'<!-- END: SIDEBAR-NAV -->',text2[ip:ip+5000])
    if sn: ip+=sn.end()
    text2=text2[:ip]+'\n'+hero+'\n'+text2[ip:]
    ch.append(f"MOVED hero ({len(hero)}ch)")
    return text2,ch

def op_media(text):
    ch=[]
    bp=re.compile(r"""<button[^>]*onclick=["']switchTab\(['"]media['"]\)["'][^>]*>.*?</button>\s*""",re.DOTALL)
    if bp.search(text): text=bp.sub('',text); ch.append("REMOVED media tab button")
    sp=re.compile(r'\s*<!-- BEGIN: TAB-MEDIA -->.*?<!-- END: TAB-MEDIA -->\s*',re.DOTALL)
    if sp.search(text): text=sp.sub('\n',text); ch.append("REMOVED TAB-MEDIA section")
    else:
        rp=re.compile(r'\s*<section\s+id="media"[^>]*>.*?</section>\s*',re.DOTALL)
        if rp.search(text): text=rp.sub('\n',text); ch.append("REMOVED id=media section")
    if not ch: ch.append("SKIP: no media tab")
    return text,ch

def op_sidebar(text):
    ch=[]
    if 'sidebar-collapse-btn' in text or 'SIDEBAR COLLAPSE' in text:
        return text,["SKIP: already has sidebar collapse"]
    i=text.rfind('</style>')
    if i<0: return text,["ERROR: no </style>"]
    text=text[:i]+SIDEBAR_CSS+'\n'+text[i:]
    ch.append("INJECTED sidebar CSS")
    j=text.rfind('</body>')
    if j<0: return text,["ERROR: no </body>"]
    text=text[:j]+SIDEBAR_HTML+'\n'+text[j:]
    ch.append("INJECTED sidebar button+JS")
    return text,ch

def process(d, dry):
    f=find_html(d)
    if not f: return d.name,["SKIP: no HTML"],False
    text,raw=read_raw(f); eol=detect_eol(raw); changes=[]; mod=False
    for label,op in [("HERO",op_hero),("MEDIA",op_media),("SIDEBAR",op_sidebar)]:
        text,ch=op(text)
        changes.extend([f"[{label}] {c}" for c in ch])
        if any(x in c for c in ch for x in ['MOVED','REMOVED','INJECTED']): mod=True
    if not dry and mod:
        ts=datetime.now().strftime('%Y%m%d-%H%M%S')
        bd=BACKUP_DIR/ts; bd.mkdir(parents=True,exist_ok=True)
        shutil.copy2(f,bd/f.name)
        write_out(f,text,eol)
        changes.append(f"WRITTEN: {f.name}")
    return d.name,changes,mod

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--apply',action='store_true')
    ap.add_argument('--single',type=str)
    a=ap.parse_args()
    dry=not a.apply
    if dry: print("="*50+"\nDRY RUN\n"+"="*50)
    dirs=sorted([d for d in ARTICLES_DIR.iterdir() if d.is_dir() and not d.name.startswith('_')])
    if a.single: dirs=[d for d in dirs if d.name.startswith(a.single)]
    mc=ec=0
    for d in dirs:
        nm,ch,mod=process(d,dry)
        st="MOD" if mod else "OK"
        if any('ERROR' in c for c in ch): st="ERR"; ec+=1
        if mod: mc+=1
        print(f"\n{'~'*40}\n  {nm}  [{st}]")
        for c in ch: print(f"    {c}")
    print(f"\n{'='*50}\n  {len(dirs)} articles | {mc} modified | {ec} errors | {'APPLIED' if not dry else 'DRY RUN'}\n{'='*50}")

if __name__=='__main__': main()
