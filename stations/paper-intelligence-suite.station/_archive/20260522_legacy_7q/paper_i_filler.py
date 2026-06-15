"""
INFOBOX BUILDER + PAPER I FILLER
Appended to template_filler.py

Generates the 7Q_INFOBOX callout from 7Q + Promotion Pass data,
then assembles the complete Paper I document:

  [!7q-infobox] FACTS callout
  ---
  Paper I FACTS+UADP body (filled)
"""
from pathlib import Path
from datetime import datetime
import re, json, sys
sys.path.insert(0, str(Path(__file__).parent))
from template_filler import normalize_conf, get_domains, get_assumptions, get_citations, get_missing

PAPER_I_TEMPLATE_PATH = Path(r"O:\_Theophysics_v4\00_SYSTEM\02_Master_Templates\7Q\PAPER_I_TEMPLATE.md")


def build_infobox(seven_q_data, promotion_data, tscore, tier, ckg_raw=None):
    """
    Builds the > [!7q-infobox]- FACTS callout block.
    Matches 7Q_INFOBOX_TEMPLATE.md format exactly.
    """
    fwd = seven_q_data.get('forward_7q', {})
    rev = seven_q_data.get('reverse_7q', {})

    claim = str(fwd.get('q2', '')).strip()[:200]
    paper_name = seven_q_data.get('paper', 'Unknown').replace('.md','')

    # Confidence label
    ib = promotion_data.get('infobox_fields', {}) if promotion_data else {}
    conf_label   = ib.get('confidence_label', tier.title() if tier else 'Provisional')
    struct_count = ib.get('structural_count', 1)
    analog_count = ib.get('analogical_count', 1)

    # Theory resonance table — from Promotion Pass P1
    theory_rows = ''
    frameworks = promotion_data.get('p1_posture_frameworks', []) if promotion_data else []
    if frameworks:
        for f in frameworks[:4]:
            name  = str(f.get('name',''))[:30]
            ftype = f.get('type', 'ANALOGICAL')
            bold  = '**STRUCTURAL**' if ftype == 'STRUCTURAL' else 'ANALOGICAL'
            theory_rows += f'| {name} | {bold} |\n'
    else:
        theory_rows = '| [Run Promotion Pass] | — |\n'

    # Strongest / Weakest from infobox fields
    sq = ib.get('strongest_q', {})
    wq = ib.get('weakest_q', {})
    strongest_str = f"**{sq.get('q_num','?')} {sq.get('q_label','?')}** ({sq.get('score','?')}) — {str(sq.get('explanation',''))[:100]}"
    weakest_str   = f"**{wq.get('q_num','?')} {wq.get('q_label','?')}** ({wq.get('score','?')}) — {str(wq.get('explanation',''))[:100]}"

    # Kill threat — from 7Q reverse
    q5 = str(fwd.get('q5', '')).strip()
    kill_count   = ib.get('bundled_claims', 3)
    most_danger  = str(rev.get('r4', q5))[:120]

    # ISO status
    iso_status = ib.get('iso_status', 'Partial')
    iso_hint   = ib.get('iso_hint', str(promotion_data.get('p7_integration_map', {}).get('iso_hint',''))[:100]) if promotion_data else 'Run Promotion Pass'

    # Bundled claims
    bundled = ib.get('bundled_claims', 2)

    # At a glance
    paper_type = ib.get('paper_type', 'Convergence Paper')
    domain_count = ib.get('domain_count', len(promotion_data.get('p3_domain_isomorphism',[]))) if promotion_data else 3
    eff_n = ib.get('effective_n', struct_count + analog_count)
    decisive = str(ib.get('decisive_test_short', 'See Kill Conditions'))[:80]
    ckg_display = f"{ckg_raw:.2f}" if ckg_raw else '—'

    infobox = f"""> [!7q-infobox]- FACTS
>
> ## {paper_name}
>
> **{conf_label}** | T = **{tscore}** | CKG = **{ckg_display}**
>
> ### Core Claim
>
> {claim}
>
> ### Theory Resonance
>
> | . | . |
> |---|---|
{('>' + theory_rows.replace(chr(10), chr(10) + '>') ).rstrip('>')}
>
> {struct_count} structural mappings carry real predictive weight. {analog_count} analogical mappings suggest pattern but don't transfer equations.
>
> ### Strongest
>
> {strongest_str}
>
> ### Weakest
>
> {weakest_str}
>
> ### Kill Threat
>
> {kill_count} kill conditions | **Most dangerous:**
> {most_danger}
>
> ### ISO Status
>
> **{iso_status}** — {iso_hint}
>
> ### Bundled Claims
>
> **{bundled}** independently killable claims in one paper.
>
> ### At A Glance
>
> | . | . |
> |---|---|
> | Type | {paper_type} |
> | Domains | {domain_count} |
> | Effective n | {eff_n} |
> | Decisive test | {decisive} |

"""
    return infobox


def fill_paper_i_template(seven_q_data, promotion_data, tscore, tier, deaths, output_path):
    """
    Assembles the complete Paper I document:
      1. 7Q infobox (FACTS callout)
      2. Paper I FACTS+UADP body (filled from template)
    """
    paper  = seven_q_data.get('paper', 'Unknown')
    fwd    = seven_q_data.get('forward_7q', {})
    rev    = seven_q_data.get('reverse_7q', {})
    ts     = seven_q_data.get('analyzed_at', datetime.now().isoformat())[:10]

    claim   = str(fwd.get('q2', '')).strip()
    summary = str(fwd.get('summary', '')).strip()
    q5      = str(fwd.get('q5', '')).strip()
    top3    = fwd.get('top_3_strengthening_actions', [])
    if not isinstance(top3, list): top3 = [str(top3)]
    verdict = str(rev.get('verdict', '')).strip()
    weakest = str(rev.get('r4', '')).strip()
    counter = str(rev.get('r5', '')).strip()
    prescription = str(rev.get('r7', '')).strip()
    conf = normalize_conf(rev.get('confidence_score', 0.5))

    assumptions = get_assumptions(rev)
    citations   = get_citations(fwd)
    missing     = get_missing(fwd)
    domains     = get_domains(fwd)
    bridge_count = len(domains)

    short_id = re.sub(r'[^\w]', '_', paper.replace('.md',''))[:20]
    ib = promotion_data.get('infobox_fields', {}) if promotion_data else {}

    # ── INFOBOX ──
    infobox = build_infobox(seven_q_data, promotion_data, tscore, tier)

    # ── PAPER I BODY ──
    # Load template or build from known structure
    try:
        body = PAPER_I_TEMPLATE_PATH.read_text(encoding='utf-8')
    except:
        # Fall back to embedded minimal structure
        body = _PAPER_I_FALLBACK

    # ── YAML FRONTMATTER ──
    body = re.sub(r'title: "Paper I — Foundational Claim"', f'title: "{claim[:100]}"', body)
    body = re.sub(r'created: YYYY-MM-DD', f'created: {ts}', body)
    body = re.sub(r'thesis_unit: "DT-XXX"', 'thesis_unit: "DT-AUTO"', body)
    body = re.sub(r'node_id: ""', 'node_id: ""', body)
    body = re.sub(r'short_id: ""', f'short_id: "{short_id}"', body)
    body = re.sub(r't_score:', f't_score: {tscore}', body)
    body = re.sub(r'tier: ""', f'tier: "{tier}"', body)
    body = re.sub(r'bridge_count:', f'bridge_count: {bridge_count}', body)
    body = re.sub(r'death_tests_survived:', f'death_tests_survived: {deaths}', body)

    # ── CALLOUT HEADER ──
    body = re.sub(
        r'\{\{short_id\}\}.*?\{\{alternatives_tested\}\}',
        f'`{short_id}` | **Scope:** system | **Entity:** claim | **Q-Type:** Type 2 | **T-Score:** {tscore} ({tier}) | **Deaths Survived:** {deaths}/4 | **Bridges:** {bridge_count} | **Alternatives Tested:** {len(assumptions)}',
        body, flags=re.DOTALL
    )

    # ── PAGE ZERO ──
    body = re.sub(
        r'> \[State the single bedrock assumption\. If this is false, the entire paper fails\.\]',
        f'> {claim[:200]}',
        body
    )

    # ── [F] FIND ──
    find_text = str(rev.get('r1', fwd.get('summary', ''))).strip()[:500]
    body = re.sub(
        r'\[Write 2-3 paragraphs\. State the anomaly plainly\. No throat-clearing\.\]',
        f'{find_text}\n\n*[Expand with 2-3 paragraphs from the paper — anomaly stated plainly.]*',
        body
    )

    # ── [A] ADMIT ──
    gradient = promotion_data.get('p2_confidence_gradient', {}) if promotion_data else {}
    tier_a = '; '.join(gradient.get('tier_a', ['[From Promotion Pass P2]'])[:2])
    tier_b = '; '.join(gradient.get('tier_b', ['[From Promotion Pass P2]'])[:2])
    tier_c = '; '.join(gradient.get('tier_c', ['[From Promotion Pass P2]'])[:1])

    body = re.sub(r'\|_What would change my mind:_ \[specific falsification condition\]\|', f'|{q5[:120]}|', body)
    body = re.sub(r'\|_Honest limitations:_ \[specific gaps acknowledged\]\|',
                  f'|Tier A: {tier_a[:80]} | Tier B: {tier_b[:60]} | Tier C: {tier_c[:60]}|', body)

    # ── [C] CLAIM ──
    body = re.sub(r'> \[One question\. The question this paper answers\.\]',
                  f'> What is the nature and mechanism of the claim: {claim[:100]}?', body)
    body = re.sub(r'> \[One sentence\. The claim\. No hedging\.\]', f'> {claim}', body)

    # Support from top3
    supports = top3[:3] + ['[Add from paper]'] * (3 - len(top3))
    body = re.sub(r'1\. \[First supporting argument\]', f'1. {str(supports[0])[:120]}', body)
    body = re.sub(r'2\. \[Second supporting argument\]', f'2. {str(supports[1])[:120]}', body)
    body = re.sub(r'3\. \[Third supporting argument\]', f'3. {str(supports[2])[:120]}', body)

    # If removed
    body = re.sub(r'\|If removed, what breaks\|\|', f'|If removed, what breaks|{weakest[:100]}|', body)

    # Predictions from P6
    preds = promotion_data.get('p6_forward_predictions', []) if promotion_data else []
    true_preds = [str(p.get('prediction',''))[:100] for p in preds[:3]] + ['[Add prediction]'] * 3
    body = re.sub(r'- \[Observable consequence 1\]', f'- {true_preds[0]}', body)
    body = re.sub(r'- \[Observable consequence 2\]', f'- {true_preds[1]}', body)
    body = re.sub(r'- \[Observable consequence 3\]', f'- {true_preds[2]}', body)

    # ── T.1 BRANCHES ──
    letters = 'ABCDE'
    for i, assumption in enumerate(assumptions[:5]):
        L = letters[i]
        body = re.sub(
            rf'\|{L}\|\|✅ continues / ❌ dead / ⚠️ partial / ■ terminal\|\|\|',
            f'|{L}|{str(assumption)[:80]}|⚠️ partial||From 7Q R2|',
            body
        )

    # ── T.2 DEATH CONDITIONS ──
    body = re.sub(r'\|1\|.*?Self-Refutation.*?FAIL\|\|',
                  f'|1|**Self-Refutation**|yes|PARTIAL|{verdict[:80]}|', body)
    body = re.sub(r'\|2\|.*?Infinite Regress.*?FAIL\|\|',
                  f'|2|**Infinite Regress**|yes|PARTIAL|Weakest link: {weakest[:60]}|', body)
    body = re.sub(r'\|3\|.*?Empirical Contradiction.*?FAIL\|\|',
                  f'|3|**Empirical Contradiction**|yes|PARTIAL|Counter: {counter[:60]}|', body)
    body = re.sub(r'\|4\|.*?Logical Incoherence.*?FAIL\|\|',
                  f'|4|**Logical Incoherence**|yes|PARTIAL|See R6 verdict|', body)
    body = re.sub(r'\*\*Death tests survived:\*\* /4', f'**Death tests survived:** {deaths}/4 *(7Q estimated — verify)*', body)

    # ── T.3 EVIDENCE ──
    for i, c in enumerate(citations[:5], 1):
        body = re.sub(
            rf'\|{i}\|\|\|\|\|\|/1\.0\|/1\.0\|\|',
            f'|{i}|{c.get("citation","")[:60]}||{c.get("journal","")[:20] or "citation"}|{c.get("theory","")[:30]}|0.6|0.5|n/a|',
            body
        )

    body = re.sub(r'> \[The main result in plain language\]', f'> {summary[:200]}', body)
    body = re.sub(r'> \[What you didn\'t expect to find\]', '> [Complete after deep reading of paper]', body)
    body = re.sub(r'> \[What you tested that returned nothing — intellectual honesty\]',
                  f'> {prescription[:150] or "[Complete after reading]"}', body)

    # ── T.4 COUNTER-EVIDENCE ──
    body = re.sub(r'\|1\|\|\|/1\.0\|\|yes / no / partially\|',
                  f'|1|{counter[:80]}|7Q Reverse|{conf}|[Your response]|partially|', body)
    supports_n = round(conf * 10)
    body = re.sub(r'\*\*Controversy score:\*\* supports / \(supports \+ attacks\) =',
                  f'**Controversy score:** {supports_n}/10 = {conf}', body)

    # ── T.5 CROSS-DOMAIN ──
    iso_domains = promotion_data.get('p3_domain_isomorphism', []) if promotion_data else []
    ALL_DOMAINS = ['Physics','Theology','Consciousness','Quantum Mechanics','Scripture','Information Theory','Mathematics','Law','History','Ethics']
    iso_map = {d.get('domain','').title(): d for d in iso_domains}
    for d in ALL_DOMAINS:
        iso = iso_map.get(d, {})
        maps_yn = 'Yes' if iso else 'No'
        interp = str(iso.get('interpretation',''))[:60]
        quality = 'strong' if iso.get('mapping_type') == 'STRUCTURAL' else 'analogy' if iso else 'weak'
        body = re.sub(
            rf'\|{re.escape(d)}\|\|\|\|exact / strong / analogy / weak / contested\|',
            f'|{d}|{maps_yn}|{interp}||{quality}|',
            body
        )
    body = re.sub(r'\*\*Bridge count \(exact \+ strong\):\*\* /10',
                  f'**Bridge count (exact + strong):** {bridge_count}/10', body)

    # ── [S] SNAP KILL CONDITIONS ──
    body = re.sub(r'\|1\|\[How to destroy this\]\|\[What would count\]\|Not yet tested\|.*?\|',
                  f'|1|{q5[:80]}|Demonstrate with evidence|Not yet tested|empirical|', body)
    body = re.sub(r'\|2\|\|\|Not yet tested\|\|',
                  f'|2|{weakest[:80]}|Counter-example exists|Not yet tested|incoherence|', body)

    # ── HONEST BLANKS ──
    blank_rows = ''
    for i, m in enumerate(missing[:3], 1):
        blank_rows += f'|{i}|{m}|needs_source|8/10|[[]]|\n'
    if not blank_rows:
        blank_rows = '|1|[See 7Q Q3 missing evidence]|needs_source|8/10|[[]]|\n'
    body = re.sub(
        r'\|1\|\|needs_math / needs_source / needs_review / honest_blank\|/10\|\[\[\]\]\|',
        blank_rows, body
    )

    # ── AUDIT BLOCK ──
    body = re.sub(r'Date:                YYYY-MM-DD', f'Date:                {ts}', body)
    body = re.sub(r'T-Score:             /100', f'T-Score:             {tscore}/100', body)
    body = re.sub(r'Tier:                $', f'Tier:                {tier}', body, flags=re.MULTILINE)
    body = re.sub(r'Death Tests:         /4', f'Death Tests:         {deaths}/4', body)
    body = re.sub(r'Bridge Count:        /10', f'Bridge Count:        {bridge_count}/10', body)

    # ── T-SCORE BLOCK ──
    body = re.sub(r'death_survived       = ___/4', f'death_survived       = {deaths}/4', body)
    body = re.sub(r'bridge_count         = ___/10', f'bridge_count         = {bridge_count}/10', body)
    body = re.sub(r'  TOTAL                           = _____/100', f'  TOTAL                           = {tscore}/100', body)
    # Mark the correct tier
    tier_map = {'NEAR-CANONICAL': '≥90', 'STRONG': '75-89', 'PROVISIONAL': '60-74', 'WEAK': '<60'}
    for t_name, t_range in tier_map.items():
        if t_name == tier:
            body = body.replace(f'[ ] {t_name} ({t_range})', f'[x] {t_name} ({t_range})')

    # ── FINAL ASSEMBLY ──
    full_doc = f"""{infobox}
---

{body}"""

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(full_doc, encoding='utf-8')
    print(f"  Paper I: {out.name}")
    return out
