import json, sys, traceback
sys.path.insert(0, r'X:\apps\paper-intelligence-suite-python\11_HTML_REPORT')
try:
    from generate_report import generate_paper_html
    snap = json.loads(open(r'X:\Backside\MDA\09_NLP_SNAPSHOTS\P-004ca0f070cd_snapshot.json', encoding='utf-8').read())
    html = generate_paper_html(snap)
    with open(r'X:\Backside\MDA\_LOGS\test_report_v2.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'SUCCESS: {len(html)} chars written')
except Exception as e:
    traceback.print_exc()
    print(f'FAILED: {e}')
