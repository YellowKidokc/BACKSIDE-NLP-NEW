"""
TEMPLATE FILLER v2 — Uses ACTUAL templates as base
===================================================
Loads BLANK_TEMPLATE_1.md and PAPER_I_TEMPLATE.md as strings,
then does targeted section replacement from 7Q JSON.

Output is STRUCTURALLY IDENTICAL to the templates — just filled.
No custom markdown. No approximations. The real thing.
"""
import json, re, sys
from pathlib import Path
from datetime import datetime

# ─── TEMPLATE PATHS ──────────────────────────────────────────────────────
TEMPLATES_DIR = Path(r"O:\_Theophysics_v4\00_SYSTEM\Templates")
NODE_TEMPLATE  = TEMPLATES_DIR / "BLANK_TEMPLATE_1.md"
PAPER_TEMPLATE = TEMPLATES_DIR / "PAPER_I_TEMPLATE.md"

# Fallback: templates baked in from uploads if vault copies missing
# (copy from /mnt/user-data/uploads/ on first run)
UPLOAD_DIR = Path(r"/mnt/user-data/uploads")

def get_template(name):
    """Load template from vault, fallback to uploads."""
    vault_path = TEMPLATES_DIR / name
    if vault_path.exists():
        return vault_path.read_text(encoding='utf-8')
    upload_path = UPLOAD_DIR / name
    if upload_path.exists():
        t = upload_path.read_text(encoding='utf-8')
        # Cache to vault for next time
        vault_path.parent.mkdir(parents=True, exist_ok=True)
        vault_path.write_text(t, encoding='utf-8')
        return t
    raise FileNotFoundError(f"Template not found: {name}")

# ─── HELPERS ─────────────────────────────────────────────────────────────
def safe(s, limit=None):
    s = str(s).strip()
    if limit: s = s[:limit]
    return s

def list_to_bullets(lst, limit=3, maxlen=120):
    if isinstance(lst, str):
        lst = [lst]
    return '\n'.join(f'- {safe(i, maxlen)}' for i in lst[:limit])

def normalize_conf(raw):
    try:
        c = float(raw)
        return c if c <= 1.0 else round(c / 10.0, 2)
    except:
        return 0.5

def compute_tscore(fwd, rev, bridge_count):
    verdict = safe(rev.get('verdict','')).lower()
    if 'does not survive' in verdict or 'significantly' in verdict:
        deaths = 1
    elif 'weakened' in verdict:
        deaths = 2
    elif 'partial' in verdict:
        deaths = 3
    else:
        deaths = 2

    conf = normalize_conf(rev.get('confidence_score', 0.5))
    assumptions = rev.get('r2', [])
    if isinstance(assumptions, str):
        assumptions = [a.strip() for a in re.split(r'\n|;|•|-', assumptions) if a.strip()]
    alts = min(len(assumptions), 5)
    alt_ratio = alts / max(alts, 1) * 0.8
    q3 = fwd.get('q3', {})
    ev_str = str(q3).lower()
    ev_conf = 0.5 if 'empirical' in ev_str else 0.3

    t = (deaths/4)*25 + ev_conf*20 + (min(bridge_count,10)/10)*25 + alt_ratio*15 + 0.6*5 + 0.6*5 + conf*5
    t = round(t, 1)
    tier = 'NEAR-CANONICAL' if t >= 90 else 'STRONG' if t >= 75 else 'PROVISIONAL' if t >= 60 else 'WEAK'
    return t, tier, deaths

def get_domains(fwd):
    raw = fwd.get('q1', [])
    if isinstance(raw, str): raw = [d.strip() for d in raw.split(',')]
    if not isinstance(raw, list): raw = [str(raw)]
    return [d.strip().title() for d in raw if d.strip()]

def get_assumptions(rev):
    r2 = rev.get('r2', [])
    if isinstance(r2, str):
        r2 = [a.strip() for a in re.split(r'\n|;|•|\d+\.|-', r2) if a.strip()]
    return [a for a in r2 if a][:5]

def get_citations(fwd):
    q7 = fwd.get('q7', [])
    citations = []
    if isinstance(q7, list):
        for item in q7:
            if isinstance(item, dict):
                citations.append({
                    'citation': safe(item.get('citation',''), 80),
                    'theory':   safe(item.get('theory',''), 50),
                    'journal':  safe(item.get('journal',''), 50),
                })
            elif isinstance(item, str):
                citations.append({'citation': safe(item, 80), 'theory': '', 'journal': ''})
    elif isinstance(q7, str):
        citations.append({'citation': safe(q7, 80), 'theory': '', 'journal': ''})
    return citations

def get_missing(fwd):
    q3 = fwd.get('q3', {})
    if isinstance(q3, dict):
        m = q3.get('missing_evidence', q3.get('missing', []))
    else:
        m = [str(q3)]
    if isinstance(m, str): m = [m]
    return [safe(x, 100) for x in m if x][:3]

# ─── NODE TEMPLATE FILLER (BLANK_TEMPLATE_1) ─────────────────────────────
def fill_node_template(data):
    paper = data.get('paper', 'Unknown')
    fwd   = data.get('forward_7q', {})
    rev   = data.get('reverse_7q', {})
    ts    = data.get('analyzed_at', datetime.now().isoformat())[:10]

    claim       = safe(fwd.get('q2', ''), 200)
    summary     = safe(fwd.get('summary', ''), 400)
    domains     = get_domains(fwd)
    assumptions = get_assumptions(rev)
    citations   = get_citations(fwd)
    missing     = get_missing(fwd)
    weakest     = safe(rev.get('r4', ''), 200)
    counter     = safe(rev.get('r5', ''), 200)
    verdict     = safe(rev.get('verdict', ''), 100)
    prescription= safe(rev.get('r7', ''), 300)
    conf_raw    = rev.get('confidence_score', 0.5)
    conf        = normalize_conf(conf_raw)
    top3        = fwd.get('top_3_strengthening_actions', [])
    if not isinstance(top3, list): top3 = [str(top3)]

    q6 = fwd.get('q6', {})
    connections = q6.get('connections', []) if isinstance(q6, dict) else [str(q6)]

    bridge_count = len(domains)
    tscore, tier, deaths = compute_tscore(fwd, rev, bridge_count)
    short_id = re.sub(r'[^\w]', '_', paper.replace('.md',''))[:20]

    # Load actual template
    try:
        tmpl = get_template("BLANK_TEMPLATE_1.md")
    except FileNotFoundError:
        # Last resort: find in uploads
        up = Path("/mnt/user-data/uploads/BLANK_TEMPLATE_1.md")
        tmpl = up.read_text(encoding='utf-8')

    # ── YAML FRONTMATTER ──
    tmpl = re.sub(r'short_id: ""', f'short_id: "{short_id}"', tmpl)
    tmpl = re.sub(r'title: ""', f'title: "{claim[:100]}"', tmpl)
    tmpl = re.sub(r'scope_level: ""', 'scope_level: "paper"', tmpl)
    tmpl = re.sub(r'entity_class: ""', 'entity_class: "claim"', tmpl)
    tmpl = re.sub(r'question_type: ""', 'question_type: "Type 2"', tmpl)
    tmpl = re.sub(r'created_by: ""', 'created_by: "ai_gpt"', tmpl)
    tmpl = re.sub(r'created_at: ""', f'created_at: "{ts}"', tmpl)
    tmpl = re.sub(r't_score:', f't_score: {tscore}', tmpl)
    tmpl = re.sub(r'tier: ""', f'tier: "{tier}"', tmpl)

    # ── TITLE ──
    tmpl = re.sub(r'# \{\{title\}\}', f'# {claim[:150]}', tmpl)

    # ── CALLOUT HEADER ──
    tmpl = re.sub(
        r'\*\*ID:\*\* `\{\{short_id\}\}` \| \*\*Scope:\*\* \{\{scope_level\}\} \| \*\*Entity:\*\* \{\{entity_class\}\} \| \*\*Status:\*\* \{\{ops_status\}\} \| \*\*T-Score:\*\* \{\{t_score\}\} \(\{\{tier\}\}\)',
        f'**ID:** `{short_id}` | **Scope:** paper | **Entity:** claim | **Status:** draft | **T-Score:** {tscore} ({tier})',
        tmpl
    )

    # ── SECTION 0: SCOPE ──
    tmpl = re.sub(
        r'(\*\*Selected scope:\*\*)\n\n\*\*Justification:\*\*',
        f'**Selected scope:** paper\n\n**Justification:** Generated from 7Q analysis of full paper. Refine scope to sentence/claim level when drilling into a specific assertion.',
        tmpl
    )

    # ── SECTION 1: ENTITY ──
    tmpl = re.sub(r'(\*\*Entity class:\*\*)\n', f'**Entity class:** claim\n', tmpl)
    tmpl = re.sub(r'(\*\*Statement:\*\*)\n', f'**Statement:** {claim}\n', tmpl)

    # ── SECTION 2: ROLE ──
    tmpl = re.sub(r'(\*\*Primary role:\*\*)\n', '**Primary role:** bridge\n', tmpl)
    tmpl = re.sub(
        r'(\*\*If removed, what breaks:\*\*)\n',
        f'**If removed, what breaks:** {weakest}\n', tmpl
    )

    # ── SECTION 3a: DERIVATION METHOD ──
    tmpl = re.sub(
        r'- \[ \] \*\*Type 2:\*\* What IS X\? \(Identity/ontological\)',
        '- [x] **Type 2:** What IS X? (Identity/ontological)',
        tmpl
    )

    # ── SECTION 3b: BRANCHES ──
    branch_letters = 'ABCDE'
    branch_rows = ''
    for i, assumption in enumerate(assumptions):
        L = branch_letters[i]
        branch_rows += f'|{L}|{safe(assumption, 80)}|❌ dead / ✅ alive / ⚠️ partial||\n'
    # Fill remaining branch rows if fewer than 5 assumptions
    for i in range(len(assumptions), 5):
        L = branch_letters[i]
        branch_rows += f'|{L}||❌ dead / ✅ alive / ⚠️ partial||\n'
    # Replace the empty branch table
    branch_table_pattern = r'(\|A\|\|❌ dead.*?\n\|E\|\|❌ dead.*?\n)'
    tmpl = re.sub(branch_table_pattern,
                  f'|A|{safe(assumptions[0],80) if assumptions else ""}|❌ dead / ✅ alive / ⚠️ partial||\n'
                  f'|B|{safe(assumptions[1],80) if len(assumptions)>1 else ""}|❌ dead / ✅ alive / ⚠️ partial||\n'
                  f'|C|{safe(assumptions[2],80) if len(assumptions)>2 else ""}|❌ dead / ✅ alive / ⚠️ partial||\n'
                  f'|D|{safe(assumptions[3],80) if len(assumptions)>3 else ""}|❌ dead / ✅ alive / ⚠️ partial||\n'
                  f'|E|{safe(assumptions[4],80) if len(assumptions)>4 else ""}|❌ dead / ✅ alive / ⚠️ partial||\n',
                  tmpl, flags=re.DOTALL)

    # ── SECTION 3c: DEATH CONDITIONS ──
    death_table = (
        f'|1|**Self-Refutation** — Does denying this claim destroy itself?'
        f'|⚠️ PARTIAL|{verdict[:100]}|\n'
        f'|2|**Infinite Regress** — Does this answer push the question back forever?'
        f'|⚠️ PARTIAL|Weakest link: {weakest[:80]}|\n'
        f'|3|**Empirical Contradiction** — Does this contradict what we observe?'
        f'|⚠️ PARTIAL|Counter-theory: {counter[:80]}|\n'
        f'|4|**Logical Incoherence** — Does this contradict an established node?'
        f'|⚠️ PARTIAL|See R6 verdict and R5 counter-theory|\n'
    )
    tmpl = re.sub(
        r'\|1\|.*?Self-Refutation.*?\n\|2\|.*?Infinite Regress.*?\n\|3\|.*?Empirical Contradiction.*?\n\|4\|.*?Logical Incoherence.*?\n',
        death_table, tmpl, flags=re.DOTALL
    )
    tmpl = re.sub(r'\*\*Death tests survived:\*\* /4', f'**Death tests survived:** {deaths}/4 *(estimated from 7Q — verify manually)*', tmpl)

    # ── SECTION 3d: EVIDENCE SOURCES ──
    ev_rows = ''
    for c in citations[:5]:
        ev_rows += f'|{c["citation"]}|||citation|0.6|0.6|n/a|\n'
    if not ev_rows:
        ev_rows = '|[Chase citations from Q7]|||citation|0.5|0.5|n/a|\n'
    # Replace the empty evidence table rows
    tmpl = re.sub(
        r'(\|Source\|Author\|Year\|Type\|Confidence\|Independence\|Stat Sig\|\n\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|\n\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|\n)',
        f'|Source|Author|Year|Type|Confidence|Independence|Stat Sig|\n|---|---|---|---|---|---|---|\n{ev_rows}',
        tmpl, flags=re.DOTALL
    )

    # ── SECTION 3e: COUNTER-EVIDENCE ──
    tmpl = re.sub(
        r'(\|Source\|Claim\|Strength\|Response\|Resolved\?\|\n\|.*?\n)',
        f'|Source|Claim|Strength|Response|Resolved?|\n|---|---|---|---|---|\n'
        f'|7Q Reverse|{counter[:80]}|{conf}|[Your response here]|partially|\n',
        tmpl, flags=re.DOTALL
    )
    supports = round(conf * 10)
    total = 10
    tmpl = re.sub(
        r'\*\*Controversy score:\*\* supports / \(supports \+ attacks\) =',
        f'**Controversy score:** {supports}/{total} = {conf}',
        tmpl
    )

    # ── SECTION 5: OPS ──
    tmpl = re.sub(r'(\*\*Status:\*\*)\n\n', f'**Status:** draft\n\n', tmpl)
    tmpl = re.sub(r'(\*\*Owner:\*\*)\n', '**Owner:** David\n', tmpl)
    tmpl = re.sub(r'(\*\*Next action:\*\*)\n', f'**Next action:**\n{list_to_bullets(top3, 3, 120)}\n', tmpl)
    tmpl = re.sub(r'(\*\*Publication target:\*\*)\n', '**Publication target:** Substack / Logos Papers\n', tmpl)
    tmpl = re.sub(r'(\*\*Priority:\*\*) /10', '**Priority:** 7/10', tmpl)

    # ── SECTION 6: CONTEXT ──
    ALL_DOMAINS = ['Physics','Theology','Consciousness','Quantum','Scripture','Information','Mathematics']
    domain_rows = ''
    for d in ALL_DOMAINS:
        if d in domains:
            quality = 'strong'
            interp  = f'[7Q Q1: detected as primary domain]'
        else:
            quality = 'weak'
            interp  = ''
        domain_rows += f'|{d}|{interp}||{quality} / exact / analogy / weak / contested|\n'
    tmpl = re.sub(
        r'(\|Physics\|\|\|exact.*?\n.*?Mathematics\|\|\|exact.*?\n)',
        domain_rows, tmpl, flags=re.DOTALL
    )
    tmpl = re.sub(
        r'\*\*Bridge count:\*\* \(domains with exact or strong mapping\)',
        f'**Bridge count:** {bridge_count} domains from Q1 — verify exact vs strong mapping',
        tmpl
    )

    # ── SECTION 7: PROVENANCE ──
    tmpl = re.sub(r'(\*\*Created by:\*\*)\n', f'**Created by:** ai_gpt (7Q analysis)\n', tmpl)
    tmpl = re.sub(r'(\*\*Method:\*\*)\n', f'**Method:** ai_gpt\n', tmpl)
    tmpl = re.sub(r'(\*\*Source file:\*\*)\n', f'**Source file:** {paper}\n', tmpl)
    tmpl = re.sub(r'(\*\*Session reference:\*\*)\n', f'**Session reference:** 7Q run {ts}\n', tmpl)
    tmpl = re.sub(r'(\*\*Version tag:\*\*)\n', f'**Version tag:** v1.0-7q\n', tmpl)
    tmpl = re.sub(r'(\*\*Date:\*\*)\n', f'**Date:** {ts}\n', tmpl)

    # ── HONEST BLANKS ──
    blank_rows = ''
    for i, m in enumerate(missing, 1):
        blank_rows += f'|{i}|{m}|needs_source|7/10|[[]]|\n'
    if not blank_rows:
        blank_rows = '|1|[See 7Q Q3 missing evidence]|needs_source|7/10|[[]]|\n'
    if prescription:
        blank_rows += f'\n**R7 Prescription:** {prescription}\n'

    tmpl = re.sub(
        r'(## HONEST BLANKS\n\n> \[!warning\].*?\n\n---)',
        f'## HONEST BLANKS\n\n> [!warning] What do we NOT know about this node?\n\n'
        f'|#|Gap|Type|Priority|Blocks|\n|---|---|---|---|---|\n{blank_rows}\n\n---',
        tmpl, flags=re.DOTALL
    )

    # ── CROSS-DOMAIN BRIDGES in CONNECTIONS ──
    bridges = '\n'.join(f'- {safe(c, 100)}' for c in connections[:3]) or '- [[]] —'
    tmpl = re.sub(
        r'(### Cross-Domain Bridges\n\n- \[\[\]\] —)',
        f'### Cross-Domain Bridges\n\n{bridges}',
        tmpl
    )

    # ── NEXT NODE TRIGGER ──
    tmpl = re.sub(
        r'(\*\*The next forced question is:\*\*)\n\n\*\*It arises because:\*\*',
        f'**The next forced question is:** [Set when placed in ontological tree]\n\n**It arises because:** This claim forces downstream questions about mechanism and implication.',
        tmpl
    )

    return tmpl

# ─── BATCH RUNNER ────────────────────────────────────────────────────────
def process_json_file(json_path, output_dir=None):
    json_path = Path(json_path)
    data = json.loads(json_path.read_text(encoding='utf-8'))
    out = Path(output_dir) if output_dir else json_path.parent / "FILLED_TEMPLATES"
    out.mkdir(parents=True, exist_ok=True)
    stem = re.sub(r'_7Q_\d{8}', '', json_path.stem)

    node_md   = fill_node_template(data)
    node_path = out / f"{stem}_NODE.md"
    node_path.write_text(node_md, encoding='utf-8')
    print(f"    Node template: {node_path.name}")
    return node_path

def run_batch(folder, output_dir=None):
    folder = Path(folder)
    jsons  = sorted(folder.glob("*_7Q_*.json"))
    print(f"\n{'='*60}")
    print(f"TEMPLATE FILLER v2 — Real Templates")
    print(f"Found: {len(jsons)} 7Q JSON files")
    print(f"{'='*60}\n")
    for j in jsons:
        print(f"  {j.name}")
        try:
            process_json_file(j, output_dir)
        except Exception as e:
            print(f"    ERR: {e}")
    print(f"\nDone. Output: {output_dir or str(folder / 'FILLED_TEMPLATES')}")

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--json',   help='Single 7Q JSON file')
    p.add_argument('--folder', help='Folder of 7Q JSON files (batch)')
    p.add_argument('--output', help='Output directory')
    args = p.parse_args()
    if args.json:
        process_json_file(args.json, args.output)
    elif args.folder:
        run_batch(args.folder, args.output)
    else:
        print("Usage: python template_filler.py --folder path/to/_7Q_ANALYSIS/")
