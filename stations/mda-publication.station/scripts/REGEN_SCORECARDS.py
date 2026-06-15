"""Regenerate all MDA HTML scorecards from existing snapshots using updated template."""
import json, sys, os, glob
from pathlib import Path

sys.stdout.reconfigure(line_buffering=True)
sys.path.insert(0, r'X:\apps\paper-intelligence-suite-python\11_HTML_REPORT')
from generate_report import generate_paper_html

SNAPSHOTS = r'X:\Backside\MDA\09_NLP_SNAPSHOTS'
OUTPUT    = r'X:\Backside\MDA\07_NLP_SCORECARDS'
LOG       = r'X:\Backside\MDA\_LOGS\regen_scorecards.log'

snaps = sorted(glob.glob(os.path.join(SNAPSHOTS, '*.json')))
print(f'Found {len(snaps)} snapshots')

ok = 0
for sp in snaps:
    try:
        snap = json.loads(Path(sp).read_text(encoding='utf-8'))
        html = generate_paper_html(snap)
        # Derive filename from identity.title or paper_id
        ident = snap.get('identity', {})
        title = ident.get('title') or snap.get('paper_id', 'unknown')
        outfile = os.path.join(OUTPUT, f'PI_{title}.html')
        Path(outfile).write_text(html, encoding='utf-8')
        ok += 1
        print(f'  OK: {title}')
    except Exception as e:
        print(f'  FAIL: {sp} — {e}')

print(f'\nDone: {ok}/{len(snaps)} regenerated')
Path(LOG).write_text(f'Regenerated {ok}/{len(snaps)} scorecards', encoding='utf-8')
