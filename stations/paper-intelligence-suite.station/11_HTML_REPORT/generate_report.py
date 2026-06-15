"""
L11 — HTML REPORT GENERATOR
============================
Generates single-file HTML scorecards from pipeline JSON results.
Matches the Theophysics dark/gold aesthetic.
Each report is self-contained (inline CSS, inline Chart.js).

Two input shapes supported:
  - Legacy flat row (existing pipeline output)
  - ProofExplorerSnapshot dict (Package A output) — adds 8 peer-review tabs.

Usage:
  python generate_report.py --json results.json --output report_dir/
  python generate_report.py --json snapshot.json --snapshot
  python generate_report.py --json results.json --single   # one combined report
"""
import json, argparse, html as _html
from pathlib import Path
from datetime import datetime


# ─── helpers ────────────────────────────────────────────────────────────────

def _bar(val, max_val=1.0, color='#d4af37'):
    """Inline SVG bar."""
    pct = min((val or 0) / max_val * 100, 100)
    return f'<div style="display:flex;align-items:center;gap:8px"><div style="flex:1;height:8px;background:#1a1a1a;border-radius:4px;overflow:hidden"><div style="width:{pct}%;height:100%;background:{color};border-radius:4px"></div></div><span class="mono" style="font-size:0.75rem;color:#a0a0a0;min-width:45px;text-align:right">{val:.3f}</span></div>'


def _fruit_row(name, l6_val, l8_val, anti_val):
    """Row for fruits comparison table."""
    l6 = l6_val or 0
    l8 = l8_val or 0
    anti = anti_val or 0
    avg = (l6 + l8) / 2 if (l6 > 0 and l8 > 0) else max(l6, l8)
    return f'''<tr>
        <td style="font-weight:500;color:#e8e8e8">{name}</td>
        <td>{_bar(l6, 0.3, '#d4af37')}</td>
        <td>{_bar(l8, 1.0, '#22c55e')}</td>
        <td>{_bar(anti, 0.1, '#ef4444')}</td>
        <td class="mono" style="text-align:center;color:#d4af37">{avg:.3f}</td>
    </tr>'''


def _esc(s):
    """HTML-escape a value, tolerating None and non-strings."""
    if s is None:
        return ''
    return _html.escape(str(s), quote=True)


def _is_snapshot(d):
    """Detect snapshot vs legacy flat row by structural signature."""
    if not isinstance(d, dict):
        return False
    return 'pipeline_metrics' in d and ('coherence' in d or 'claim_inventory' in d or 'identity' in d)


def _flatten_pipeline(snapshot):
    """Hoist snapshot.pipeline_metrics + identity to a flat row the existing dashboard understands."""
    row = dict(snapshot.get('pipeline_metrics') or {})
    ident = snapshot.get('identity') or {}
    # Filename / title fallbacks so the existing dashboard header works.
    row.setdefault('file', f"{snapshot.get('paper_id') or ident.get('paper_id') or 'unknown'}.md")
    row.setdefault('analyzed_at', snapshot.get('generated_at', ''))
    row.setdefault('schema_version', snapshot.get('schema_version', ''))
    return row


# ─── peer-review tab renderers ──────────────────────────────────────────────
#
# Each tab is a (label, icon, html_body) tuple. Empty sections render the
# "Not extracted — confidence low" placeholder so the panel never crashes.

_EMPTY = '<div class="pr-empty"><i class="fas fa-circle-notch"></i> Not extracted — confidence low</div>'


def _tab_claims(claims):
    if not claims:
        return _EMPTY
    rows = []
    for c in claims:
        importance = (c.get('importance') or 'support').lower()
        risk = (c.get('risk_level') or 'medium').lower()
        testability = (c.get('testability') or 'no').lower()
        imp_class = {'core': 'gold', 'support': 'blue', 'rhetorical': 'red'}.get(importance, 'blue')
        risk_class = {'low': 'green', 'medium': 'gold', 'high': 'red'}.get(risk, 'gold')
        test_class = {'yes': 'green', 'partial': 'gold', 'no': 'red'}.get(testability, 'red')
        cite = '<i class="fas fa-exclamation-triangle" style="color:var(--orange)" title="needs citation"></i>' if c.get('needs_citation') else ''
        ev = '<i class="fas fa-check" style="color:var(--green)" title="evidence present"></i>' if c.get('evidence_present') else '<i class="fas fa-minus" style="color:var(--text-muted)"></i>'
        rows.append(
            f'<tr>'
            f'<td style="max-width:380px">{_esc(c.get("claim",""))}'
            f'<div style="font-size:0.7rem;color:var(--text-muted);margin-top:0.2rem">{_esc(c.get("notes",""))}</div></td>'
            f'<td><span class="pr-badge pr-{_esc(c.get("claim_type","physical"))}">{_esc(c.get("claim_type","physical")).replace("_"," ")}</span></td>'
            f'<td><span class="pr-badge {imp_class}">{_esc(importance)}</span></td>'
            f'<td style="text-align:center">{ev}</td>'
            f'<td><span class="pr-badge {test_class}">{_esc(testability)}</span></td>'
            f'<td><span class="pr-badge {risk_class}">{_esc(risk)}</span></td>'
            f'<td style="text-align:center">{cite}</td>'
            f'</tr>'
        )
    return (
        '<table class="pr-table"><thead><tr>'
        '<th>Claim</th><th>Type</th><th>Importance</th><th>Evidence</th><th>Testable</th><th>Risk</th><th>Cite</th>'
        '</tr></thead><tbody>'
        + ''.join(rows)
        + '</tbody></table>'
    )


def _tab_equations(equations):
    if not equations:
        return _EMPTY
    rows = []
    for eq in equations:
        role = (eq.get('role') or 'structural').lower()
        op = (eq.get('operational_status') or 'symbolic').lower()
        dim = (eq.get('dimensional_status') or 'symbolic').lower()
        role_class = {'doing_work': 'green', 'predictive': 'gold', 'structural': 'blue', 'decorative': 'red'}.get(role, 'blue')
        op_class = {'computable': 'green', 'symbolic': 'gold', 'metaphorical': 'red'}.get(op, 'gold')
        var_status = '<i class="fas fa-check" style="color:var(--green)"></i>' if eq.get('variables_defined') else '<i class="fas fa-times" style="color:var(--red)"></i>'
        issues = eq.get('issues') or []
        issue_html = ''
        if issues:
            issue_html = '<div style="font-size:0.7rem;color:var(--orange);margin-top:0.3rem">⚠ ' + '; '.join(_esc(i) for i in issues) + '</div>'
        rows.append(
            f'<tr>'
            f'<td><div class="mono" style="font-size:0.78rem;color:var(--gold)">{_esc(eq.get("equation",""))}</div>'
            f'<div style="font-size:0.75rem;color:var(--text-dim);margin-top:0.2rem">{_esc(eq.get("purpose",""))}</div>{issue_html}</td>'
            f'<td><span class="pr-badge {role_class}">{_esc(role).replace("_"," ")}</span></td>'
            f'<td><span class="pr-badge {op_class}">{_esc(op)}</span></td>'
            f'<td>{_esc(dim)}</td>'
            f'<td style="text-align:center">{var_status}</td>'
            f'</tr>'
        )
    return (
        '<table class="pr-table"><thead><tr>'
        '<th>Equation / Purpose</th><th>Role</th><th>Operational</th><th>Dimensions</th><th>Vars Defined</th>'
        '</tr></thead><tbody>'
        + ''.join(rows)
        + '</tbody></table>'
    )


def _tab_assumptions(stack):
    if not stack:
        return _EMPTY
    cats = [
        ('explicit', 'Explicit', 'gold'),
        ('implicit', 'Implicit', 'red'),
        ('imported', 'Imported (existing physics)', 'blue'),
        ('theological', 'Theological', 'gold'),
        ('scientific', 'Scientific', 'blue'),
        ('philosophical', 'Philosophical', 'violet'),
        ('measurement', 'Measurement', 'teal'),
        ('causal', 'Causal', 'green'),
    ]
    cards = []
    any_filled = False
    for key, label, color in cats:
        items = stack.get(key) or []
        if items:
            any_filled = True
        body = '<ul class="pr-list">' + ''.join(f'<li>{_esc(i)}</li>' for i in items) + '</ul>' if items else '<div class="pr-empty-mini">none</div>'
        cards.append(
            f'<div class="pr-assump-card">'
            f'<div class="pr-assump-header"><span class="pr-badge {color}">{_esc(label)}</span>'
            f'<span style="color:var(--text-muted);font-size:0.7rem">{len(items)}</span></div>'
            f'{body}</div>'
        )
    if not any_filled:
        return _EMPTY
    return f'<div class="pr-assump-grid">{"".join(cards)}</div>'


def _tab_evidence(evidence):
    if not evidence:
        return _EMPTY
    rows = []
    for e in evidence:
        etype = (e.get('evidence_type') or 'interpretive').lower()
        equal = (e.get('evidence_quality') or 'moderate').lower()
        type_class = {'primary': 'green', 'secondary': 'blue', 'interpretive': 'gold', 'speculative': 'red'}.get(etype, 'gold')
        qual_class = {'strong': 'green', 'moderate': 'gold', 'weak': 'red'}.get(equal, 'gold')
        gap = e.get('gap') or ''
        gap_html = f'<div style="font-size:0.7rem;color:var(--orange);margin-top:0.3rem">Gap: {_esc(gap)}</div>' if gap else ''
        ce = e.get('counterevidence_needed') or ''
        ce_html = f'<div style="font-size:0.7rem;color:var(--text-muted);margin-top:0.2rem">Counter-evidence needed: {_esc(ce)}</div>' if ce else ''
        rows.append(
            f'<tr>'
            f'<td style="max-width:280px">{_esc(e.get("claim",""))}</td>'
            f'<td style="max-width:340px">{_esc(e.get("supporting_evidence",""))}{gap_html}{ce_html}</td>'
            f'<td><span class="pr-badge {type_class}">{_esc(etype)}</span></td>'
            f'<td><span class="pr-badge {qual_class}">{_esc(equal)}</span></td>'
            f'</tr>'
        )
    return (
        '<table class="pr-table"><thead><tr>'
        '<th>Claim</th><th>Supporting Evidence</th><th>Type</th><th>Quality</th>'
        '</tr></thead><tbody>'
        + ''.join(rows)
        + '</tbody></table>'
    )


def _tab_kills(kills):
    if not kills:
        return _EMPTY
    rows = []
    for k in kills:
        sev = (k.get('severity') or 'wounding').lower()
        status = (k.get('current_status') or 'open').lower()
        sev_class = {'fatal': 'red', 'wounding': 'gold', 'minor': 'blue'}.get(sev, 'gold')
        status_class = {'open': 'red', 'weak': 'orange', 'unresolved': 'gold', 'strong': 'green', 'satisfied': 'green'}.get(status, 'gold')
        rows.append(
            f'<tr>'
            f'<td style="max-width:280px">{_esc(k.get("claim",""))}</td>'
            f'<td style="max-width:300px"><div>{_esc(k.get("kill_condition",""))}</div>'
            f'<div style="font-size:0.72rem;color:var(--text-muted);margin-top:0.25rem">Test: {_esc(k.get("test_method",""))}</div></td>'
            f'<td><span class="pr-badge {sev_class}">{_esc(sev)}</span></td>'
            f'<td><span class="pr-badge {status_class}">{_esc(status)}</span></td>'
            f'</tr>'
        )
    return (
        '<table class="pr-table pr-kill-table"><thead><tr>'
        '<th>Claim</th><th>Kill Condition / Test</th><th>Severity</th><th>Status</th>'
        '</tr></thead><tbody>'
        + ''.join(rows)
        + '</tbody></table>'
    )


def _tab_comparison(comparisons):
    if not comparisons:
        return _EMPTY
    rows = []
    for c in comparisons:
        outperf = (c.get('does_paper_outperform') or 'unclear').lower()
        op_class = {'yes': 'green', 'no': 'red', 'unclear': 'gold'}.get(outperf, 'gold')
        risk = c.get('category_confusion_risk') or ''
        risk_html = f'<div style="font-size:0.7rem;color:var(--orange);margin-top:0.3rem">⚠ Category confusion: {_esc(risk)}</div>' if risk else ''
        rows.append(
            f'<tr>'
            f'<td><strong style="color:var(--gold)">{_esc(c.get("nearest_theory",""))}</strong>{risk_html}</td>'
            f'<td>{_esc(c.get("similarity",""))}</td>'
            f'<td>{_esc(c.get("difference",""))}</td>'
            f'<td><span class="pr-badge {op_class}">{_esc(outperf)}</span></td>'
            f'</tr>'
        )
    return (
        '<table class="pr-table"><thead><tr>'
        '<th>Nearest Theory</th><th>Similarity</th><th>Difference</th><th>Outperforms?</th>'
        '</tr></thead><tbody>'
        + ''.join(rows)
        + '</tbody></table>'
    )


def _tab_weak_points(overstatement, revision):
    overstatement = overstatement or {}
    revision = revision or {}
    passages = overstatement.get('overstated_passages') or []
    weak = revision.get('weakest_part') or ''
    rsi = overstatement.get('rhetorical_strength_index') or 0
    esi = overstatement.get('evidence_strength_index') or 0
    delta = overstatement.get('delta') or 0
    severity = (overstatement.get('severity') or 'none').lower()
    sev_class = {'none': 'green', 'mild': 'gold', 'moderate': 'orange', 'severe': 'red'}.get(severity, 'gold')

    if not passages and not weak and severity == 'none' and rsi == 0 and esi == 0:
        return _EMPTY

    bars = (
        '<div class="pr-row-3">'
        f'<div class="pr-stat-cell"><div class="pr-stat-label">Rhetorical strength</div>{_bar(rsi, 1.0, "#d4af37")}</div>'
        f'<div class="pr-stat-cell"><div class="pr-stat-label">Evidence strength</div>{_bar(esi, 1.0, "#22c55e")}</div>'
        f'<div class="pr-stat-cell"><div class="pr-stat-label">Δ (rhetoric − evidence)</div>'
        f'<div style="font-family:\'Oswald\',sans-serif;font-size:1.4rem;color:{"var(--red)" if delta > 0.15 else "var(--gold)" if delta > 0 else "var(--green)"}">{delta:+.2f}</div>'
        f'<span class="pr-badge {sev_class}" style="margin-top:0.3rem">{_esc(severity)}</span></div>'
        '</div>'
    )

    weak_html = f'<div class="pr-section"><h4>Weakest Part</h4><div class="pr-prose">{_esc(weak)}</div></div>' if weak else ''
    passages_html = ''
    if passages:
        items = ''.join(f'<li>{_esc(p)}</li>' for p in passages)
        passages_html = f'<div class="pr-section"><h4>Overstated Passages ({len(passages)})</h4><ul class="pr-list">{items}</ul></div>'

    return bars + weak_html + passages_html


def _tab_revision(revision):
    revision = revision or {}
    must_fix = revision.get('must_fix_before_publication') or []
    next_test = revision.get('best_next_test') or ''
    strongest = revision.get('strongest_part') or ''
    needs = revision.get('needs_expert_review') or []

    if not (must_fix or next_test or strongest or needs):
        return _EMPTY

    parts = []
    if strongest:
        parts.append(f'<div class="pr-section"><h4>Strongest Part</h4><div class="pr-prose" style="border-left-color:var(--green)">{_esc(strongest)}</div></div>')
    if must_fix:
        items = ''.join(f'<li>{_esc(m)}</li>' for m in must_fix)
        parts.append(f'<div class="pr-section"><h4>Must Fix Before Publication ({len(must_fix)})</h4><ul class="pr-list pr-list-numbered">{items}</ul></div>')
    if next_test:
        parts.append(f'<div class="pr-section"><h4>Best Next Test</h4><div class="pr-prose" style="border-left-color:var(--gold)">{_esc(next_test)}</div></div>')
    if needs:
        chips = ''.join(f'<span class="pr-badge violet" style="margin:0.15rem">{_esc(n)}</span>' for n in needs)
        parts.append(f'<div class="pr-section"><h4>Needs Expert Review</h4><div>{chips}</div></div>')

    return ''.join(parts)


def _build_peer_review(snapshot):
    """Build the 8-tab peer-review section. Returns html string (empty if no snapshot)."""
    if not snapshot:
        return ''

    coherence = snapshot.get('coherence') or {}
    overstate = snapshot.get('overstatement') or {}
    revision = snapshot.get('revision') or {}

    tabs = [
        ('claims', 'Claims', 'fa-list-check', _tab_claims(snapshot.get('claim_inventory') or [])),
        ('equations', 'Equations', 'fa-square-root-variable', _tab_equations(snapshot.get('equations') or [])),
        ('assumptions', 'Assumptions', 'fa-layer-group', _tab_assumptions(snapshot.get('assumptions') or {})),
        ('evidence', 'Evidence', 'fa-magnifying-glass', _tab_evidence(snapshot.get('evidence_map') or [])),
        ('falsifiability', 'Falsifiability', 'fa-skull', _tab_kills(snapshot.get('kill_conditions') or [])),
        ('comparison', 'Comparison', 'fa-balance-scale', _tab_comparison(snapshot.get('physics_comparison') or [])),
        ('weak', 'Weak Points', 'fa-triangle-exclamation', _tab_weak_points(overstate, revision)),
        ('revision', 'Revision Plan', 'fa-pen-to-square', _tab_revision(revision)),
    ]

    buttons = ''.join(
        f'<button class="pr-tab{" active" if i == 0 else ""}" data-pr="{key}" onclick="prSwitch(\'{key}\')">'
        f'<i class="fas {icon}"></i> {label}</button>'
        for i, (key, label, icon, _body) in enumerate(tabs)
    )

    panels = ''.join(
        f'<div class="pr-panel{" active" if i == 0 else ""}" id="pr-panel-{key}">{body}</div>'
        for i, (key, _label, _icon, body) in enumerate(tabs)
    )

    # Coherence sub-rubric (8 metrics) below the tabs
    metrics = [
        ('definition_clarity', 'Definitions'),
        ('equation_coherence', 'Equations'),
        ('claim_discipline', 'Claims'),
        ('scope_control', 'Scope'),
        ('falsifiability', 'Falsifiable'),
        ('citation_adequacy', 'Citations'),
        ('domain_separation', 'Domain Sep.'),
        ('reader_burden', 'Readability'),
    ]
    rubric_cells = ''.join(
        f'<div class="pr-rubric-cell"><div class="pr-rubric-label">{label}</div>'
        f'<div class="pr-rubric-bar"><div class="pr-rubric-fill" style="width:{(coherence.get(key, 0) or 0) * 10}%"></div></div>'
        f'<div class="pr-rubric-val">{coherence.get(key, 0) or 0}/10</div></div>'
        for key, label in metrics
    )

    return f'''
<!-- ══════════ PEER REVIEW ══════════ -->
<h2><i class="fas fa-microscope" style="margin-right:0.4rem;color:var(--gold)"></i>Peer Review</h2>
<div class="pr-section-wrap">
    <div class="pr-tabs">{buttons}</div>
    <div class="pr-panels">{panels}</div>
    <div class="pr-rubric">
        <h3 style="margin-top:0">Coherence Rubric (8-metric review-readiness)</h3>
        <div class="pr-rubric-grid">{rubric_cells}</div>
        <div style="margin-top:0.6rem;font-size:0.7rem;color:var(--text-muted)">Confidence: {_esc(coherence.get('ai_confidence', 'medium'))}. Not an objective truth score.</div>
    </div>
</div>
'''


def _peer_review_styles():
    """CSS additions for the peer-review section. Uses existing CSS variables."""
    return '''
.pr-section-wrap { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 1.25rem; margin: 1rem 0; }
.pr-tabs { display: flex; gap: 0.25rem; flex-wrap: wrap; padding-bottom: 0.75rem; border-bottom: 1px solid var(--border); margin-bottom: 1rem; overflow-x: auto; }
.pr-tab {
    font-family: 'Oswald', sans-serif; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.08em;
    color: var(--text-muted); background: transparent; border: 1px solid transparent; border-radius: 0.3rem;
    padding: 0.4rem 0.75rem; cursor: pointer; white-space: nowrap; transition: all 0.2s;
}
.pr-tab:hover { color: var(--text-dim); background: var(--surface2); }
.pr-tab.active { color: var(--gold); border-color: rgba(212,175,55,0.3); background: var(--gold-dim); }
.pr-tab i { margin-right: 0.35rem; }
.pr-panels { min-height: 100px; }
.pr-panel { display: none; }
.pr-panel.active { display: block; }
.pr-empty { padding: 2rem; text-align: center; color: var(--text-muted); font-size: 0.85rem; font-style: italic; }
.pr-empty i { margin-right: 0.5rem; color: var(--text-muted); }
.pr-empty-mini { color: var(--text-muted); font-size: 0.75rem; font-style: italic; padding: 0.3rem 0; }

.pr-table { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
.pr-table th { font-family: 'Oswald', sans-serif; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.1em;
    color: var(--text-muted); padding: 0.6rem 0.5rem; text-align: left; border-bottom: 1px solid var(--border); }
.pr-table td { padding: 0.6rem 0.5rem; border-bottom: 1px solid var(--border); color: var(--text-dim); vertical-align: top; }
.pr-table tr:hover td { background: rgba(212,175,55,0.03); }
.pr-kill-table { background: rgba(239,68,68,0.04); border-radius: 6px; padding: 0.5rem; }

.pr-badge { display: inline-block; font-family: 'JetBrains Mono', monospace; font-size: 0.65rem;
    padding: 0.15rem 0.45rem; border-radius: 0.25rem; border: 1px solid var(--border);
    background: var(--surface2); color: var(--text-dim); white-space: nowrap; }
.pr-badge.gold { color: var(--gold); border-color: rgba(212,175,55,0.3); background: var(--gold-dim); }
.pr-badge.green { color: var(--green); border-color: rgba(34,197,94,0.3); background: rgba(34,197,94,0.1); }
.pr-badge.red { color: var(--red); border-color: rgba(239,68,68,0.3); background: rgba(239,68,68,0.1); }
.pr-badge.blue { color: var(--blue); border-color: rgba(74,158,255,0.3); background: rgba(74,158,255,0.1); }
.pr-badge.orange { color: var(--orange); border-color: rgba(245,158,11,0.3); background: rgba(245,158,11,0.1); }
.pr-badge.violet { color: #8b7fc2; border-color: rgba(139,127,194,0.3); background: rgba(139,127,194,0.1); }
.pr-badge.teal { color: var(--teal); border-color: rgba(45,212,191,0.3); background: rgba(45,212,191,0.1); }

.pr-assump-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 0.75rem; }
.pr-assump-card { background: var(--surface2); border: 1px solid var(--border); border-radius: 6px; padding: 0.75rem; }
.pr-assump-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; }
.pr-list { list-style: disc; padding-left: 1.1rem; margin: 0; font-size: 0.78rem; color: var(--text-dim); line-height: 1.5; }
.pr-list li { margin-bottom: 0.3rem; }
.pr-list-numbered { list-style: decimal; }

.pr-section { margin-top: 1rem; }
.pr-section h4 { font-family: 'Oswald', sans-serif; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.1em;
    color: var(--text-muted); margin-bottom: 0.4rem; }
.pr-prose { background: var(--surface2); border-left: 3px solid var(--red); padding: 0.7rem 0.9rem; border-radius: 0 4px 4px 0;
    font-size: 0.85rem; color: var(--text-dim); line-height: 1.55; }

.pr-row-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem; margin-bottom: 1rem; }
.pr-stat-cell { background: var(--surface2); border: 1px solid var(--border); border-radius: 6px; padding: 0.75rem; }
.pr-stat-label { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-muted); margin-bottom: 0.4rem; }

.pr-rubric { margin-top: 1.25rem; padding-top: 1rem; border-top: 1px solid var(--border); }
.pr-rubric-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 0.5rem; }
.pr-rubric-cell { background: var(--surface2); border: 1px solid var(--border); border-radius: 5px; padding: 0.5rem 0.7rem; }
.pr-rubric-label { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted); margin-bottom: 0.35rem; }
.pr-rubric-bar { height: 4px; background: #1a1a1a; border-radius: 2px; overflow: hidden; margin-bottom: 0.25rem; }
.pr-rubric-fill { height: 100%; background: var(--gold); border-radius: 2px; }
.pr-rubric-val { font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: var(--gold); text-align: right; }

@media (max-width: 700px) {
    .pr-row-3 { grid-template-columns: 1fr; }
    .pr-rubric-grid { grid-template-columns: 1fr 1fr; }
    .pr-table { font-size: 0.75rem; }
    .pr-table th, .pr-table td { padding: 0.4rem 0.3rem; }
}
'''


def _peer_review_script():
    return '''
function prSwitch(key) {
    document.querySelectorAll('.pr-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.pr-panel').forEach(p => p.classList.remove('active'));
    var btn = document.querySelector('.pr-tab[data-pr="' + key + '"]');
    var panel = document.getElementById('pr-panel-' + key);
    if (btn) btn.classList.add('active');
    if (panel) panel.classList.add('active');
}
'''


# ─── main HTML generation ───────────────────────────────────────────────────

def generate_paper_html(input_dict: dict, snapshot_path: str | None = None) -> str:
    """Render a single paper report.

    Accepts either:
      - a legacy flat row dict (existing pipeline output)
      - a ProofExplorerSnapshot dict (Package A output)

    snapshot_path is the relative href to the snapshot JSON, used by the
    Download JSON quick action (only rendered when a snapshot is detected).
    """
    snapshot = input_dict if _is_snapshot(input_dict) else None
    row = _flatten_pipeline(snapshot) if snapshot else input_dict

    fname = row.get('file', 'Unknown')
    title = (snapshot.get('identity', {}).get('title') if snapshot else None) or fname.replace('.md', '').replace('_', ' ')
    analyzed = (row.get('analyzed_at') or '')[:19]

    # Collect key metrics (legacy flat row)
    chi = row.get('L3_chi_score', 0) or 0
    chi_status = row.get('L3_chi_status', '')
    ckg = row.get('L3_ckg_tier', 'N/A')
    truth = row.get('L6_truth_score', 0) or 0
    coherence = row.get('L6_coherence_score', 0) or 0
    combined = row.get('L6_combined_score', 0) or 0
    words = row.get('L1_word_count', 0) or 0
    grade = row.get('L2_academic_grade', 'N/A')
    reading_level = row.get('L1_text_standard', 'N/A')
    claims = row.get('L6_claim_count', 0) or 0
    contradictions = row.get('L6_contradiction_flags', 0) or 0
    evidence = row.get('L6_evidence_density', 0) or 0
    fruit_net = row.get('L8_fruit_emo_net', 0) or 0
    idea_density = row.get('L10_idea_density_mean', 0) or 0
    idea_level = row.get('L10_idea_density_level', 'N/A')
    mtld = row.get('L9_lr_mtld', 0) or 0
    nrc_top = row.get('L8_nrc_top_emotions', '')
    emo_dominant = row.get('L8_emo_dominant', '')
    emo_top5 = row.get('L8_emo_top_5', '')
    posture = row.get('L6_character_posture', '')
    integrity = row.get('L6_integrity_profiles', '')
    centrality = row.get('L7_centrality_within_series', '')
    cluster = row.get('L7_cluster', '')

    # ── v2 additions: richer profile data ──
    yake_kw = row.get('L1_yake_keywords', '')
    key_sent_1 = row.get('L5_key_sentence_1', '')
    key_sent_2 = row.get('L5_key_sentence_2', '')
    key_sent_3 = row.get('L5_key_sentence_3', '')
    # Filter out YAML frontmatter from key sentences
    for _i, _ks in enumerate([key_sent_1, key_sent_2, key_sent_3]):
        if _ks and ('---' in str(_ks)[:5] or 'scrape_mode' in str(_ks)):
            if _i == 0: key_sent_1 = ''
            elif _i == 1: key_sent_2 = ''
            else: key_sent_3 = ''

    # PA structural metrics
    pa_drift_avg = row.get('PA_sm_topic_drift_avg', 0) or 0
    pa_coh_flag = row.get('PA_sm_coherence_flag', '')
    pa_snr = row.get('PA_d_signal_noise_ratio', 0) or 0
    pa_density = row.get('PA_d_density_label', '')
    pa_flow = row.get('PA_f_flow_label', '')
    pa_reading_min = row.get('PA_r_reading_time_min', 0) or 0

    # Academic rubric breakdown
    rub_struct = row.get('L2_rubric_structure_points', 0) or 0
    rub_ground = row.get('L2_rubric_grounding_points', 0) or 0
    rub_claim = row.get('L2_rubric_claim_points', 0) or 0
    rub_quant = row.get('L2_rubric_quantitative_points', 0) or 0
    rub_falsif = row.get('L2_rubric_falsifiability_points', 0) or 0
    rub_total = row.get('L2_academic_rubric_total', 0) or 0

    # Character attributes (8 dimensions)
    _char_attrs = [
        ('Spiritual Coherence', 'spiritual_coherence'),
        ('Humility Index', 'humility_index'),
        ('Spiritual Discernment', 'spiritual_discernment'),
        ('Moral Courage', 'moral_courage'),
        ('Deception Mastery', 'deception_mastery'),
        ('Charismatic Manipulation', 'charismatic_manipulation'),
        ('Authority Usurpation', 'authority_usurpation'),
        ('Global Solution Complex', 'global_solution_complex'),
    ]
    char_attr_data = []
    for label, key in _char_attrs:
        net = row.get(f'L6_attr_{key}_net_score', 0) or 0
        strength = row.get(f'L6_attr_{key}_strength', 0) or 0
        kind = row.get(f'L6_attr_{key}_kind', '')
        pos = row.get(f'L6_attr_{key}_pos_hits', 0) or 0
        neg = row.get(f'L6_attr_{key}_neg_hits', 0) or 0
        char_attr_data.append((label, net, strength, kind, pos, neg))

    threat_score = row.get('L6_threat_score', 0) or 0
    protection_score = row.get('L6_protection_score', 0) or 0
    balance_score = row.get('L6_balance_score', 0) or 0
    primary_threats = row.get('L6_primary_threats', '')
    primary_protections = row.get('L6_primary_protections', '')
    warmth = row.get('L6_warmth_score', 0) or 0
    discipline = row.get('L6_discipline_score', 0) or 0
    wisdom = row.get('L3_wisdom_score', 0) or 0
    knowledge = row.get('L3_knowledge_score', 0) or 0
    wk_ratio = row.get('L3_wk_ratio', 0) or 0

    # Snapshot-derived headline (review readiness)
    review_readiness = 0
    review_conf = ''
    if snapshot:
        coh = snapshot.get('coherence') or {}
        review_readiness = coh.get('review_readiness', 0) or 0
        review_conf = coh.get('ai_confidence', 'medium') or 'medium'

    # Fruits data for radar chart
    fruits = ['love', 'joy', 'peace', 'patience', 'kindness',
              'goodness', 'faithfulness', 'gentleness', 'self_control']
    l6_fruits = [row.get(f'L6_fruit_{f}', 0) or 0 for f in fruits]
    l8_fruits = [row.get(f'L8_fruit_emo_{f}', 0) or 0 for f in fruits]
    fruit_labels = [f.replace('_', ' ').title() for f in fruits]

    # Anti-fruits (L8)
    anti_names = ['hatred', 'despair', 'conflict', 'impatience', 'cruelty',
                  'corruption', 'betrayal', 'harshness', 'indulgence']
    anti_vals = [row.get(f'L8_anti_emo_{a}', 0) or 0 for a in anti_names]

    # Master equation variables
    me_vars = ['G_gravity_belonging', 'M_mass_meaning', 'E_entropy_engagement',
               'S_spacetime_structure', 'T_time_eternity', 'K_knowledge_logos',
               'R_relationship', 'Q_quantum_observer', 'F_faith_coupling', 'C_christ_coherence']
    me_labels = [v.split('_', 1)[1].replace('_', ' ').title() for v in me_vars]
    me_values = [row.get(f'L3_me_{v}', 0) or 0 for v in me_vars]

    # GoEmotions 27 values for bar chart
    emo_labels_27 = ['admiration', 'amusement', 'anger', 'annoyance', 'approval', 'caring',
                     'confusion', 'curiosity', 'desire', 'disappointment', 'disapproval',
                     'disgust', 'embarrassment', 'excitement', 'fear', 'gratitude', 'grief',
                     'joy', 'love', 'nervousness', 'optimism', 'pride', 'realization',
                     'relief', 'remorse', 'sadness', 'surprise', 'neutral']
    emo_values_27 = [row.get(f'L8_emo_{e}', 0) or 0 for e in emo_labels_27]

    # NRC 8 emotions
    nrc_labels = ['joy', 'trust', 'fear', 'surprise', 'sadness', 'disgust', 'anger', 'anticipation']
    nrc_values = [row.get(f'L8_nrc_{e}', 0) or 0 for e in nrc_labels]

    # Layer health
    status = row.get('_layer_status', {})
    layer_html = ''
    for layer in sorted(status.keys()):
        st = status[layer]
        color = '#22c55e' if st == 'ok' else ('#f59e0b' if st == 'skipped' else '#ef4444')
        icon = '&#10003;' if st == 'ok' else ('&#8644;' if st == 'skipped' else '&#10007;')
        layer_html += f'<span style="display:inline-flex;align-items:center;gap:4px;padding:2px 8px;background:rgba({",".join(str(int(color.lstrip("#")[i:i+2],16)) for i in (0,2,4))},0.15);border-radius:4px;font-size:0.7rem;color:{color}">{icon} {layer}</span> '

    # Claims breakdown
    anchored = row.get('L6_anchored_claims', 0) or 0
    under = row.get('L6_under_supported_claims', 0) or 0
    over = row.get('L6_overstated_claims', 0) or 0
    falsifiable = row.get('L6_falsifiable_claims', 0) or 0
    speculative = row.get('L6_speculative_claims', 0) or 0

    # Headline review-readiness card (only when snapshot present)
    review_card_html = ''
    if snapshot:
        rr_color = 'var(--green)' if review_readiness >= 70 else ('var(--gold)' if review_readiness >= 40 else 'var(--red)')
        review_card_html = f'''
    <div class="card" style="border-color:rgba(212,175,55,0.4)">
        <div class="card-label">Review Readiness</div>
        <div class="card-value" style="color:{rr_color}">{review_readiness}</div>
        <div class="card-sub">/ 100 &middot; conf: {_esc(review_conf)}</div>
    </div>'''

    # Quick Actions (only render if snapshot, to surface Download JSON)
    quick_actions_html = ''
    if snapshot and snapshot_path:
        quick_actions_html = f'''
<div class="quick-actions">
    <a href="{_esc(snapshot_path)}" class="qa-btn" download><i class="fas fa-code"></i> Download JSON</a>
    <a href="javascript:window.print()" class="qa-btn"><i class="fas fa-print"></i> Print / PDF</a>
</div>'''

    peer_review_html = _build_peer_review(snapshot) if snapshot else ''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Paper Intelligence: {_esc(title)}</title>
<link href="https://fonts.googleapis.com/css2?family=Crimson+Text:wght@400;600&family=Inter:wght@300;400;500;600&family=Oswald:wght@400;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"/>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<style>
:root {{
    --bg: #0a0a0a; --surface: #0f0f0f; --surface2: #1a1a1a; --surface3: #222;
    --border: #2a2a2a; --gold: #d4af37; --gold-dim: rgba(212,175,55,0.1);
    --text: #e8e8e8; --text-dim: #a0a0a0; --text-muted: #666;
    --red: #ef4444; --blue: #4a9eff; --teal: #2dd4bf; --green: #22c55e; --orange: #f59e0b;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; font-size: 15px; }}
.serif {{ font-family: 'Crimson Text', serif; }}
.display {{ font-family: 'Oswald', sans-serif; }}
.mono {{ font-family: 'JetBrains Mono', monospace; }}
.main {{ max-width: 1000px; margin: 0 auto; padding: 2rem 1.5rem 4rem; }}
h1 {{ font-family: 'Oswald', sans-serif; font-size: 1.8rem; color: var(--gold); margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 2px; }}
h2 {{ font-family: 'Oswald', sans-serif; font-size: 1.2rem; color: var(--gold); margin: 2rem 0 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border); text-transform: uppercase; letter-spacing: 1px; }}
h3 {{ font-size: 0.9rem; color: var(--text-dim); margin: 1.2rem 0 0.6rem; text-transform: uppercase; letter-spacing: 1px; }}
.meta {{ font-size: 0.8rem; color: var(--text-muted); margin-bottom: 1.5rem; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem; margin: 1rem 0; }}
.card {{ background: var(--surface2); border: 1px solid var(--border); border-radius: 8px; padding: 1rem; }}
.card-label {{ font-size: 0.65rem; text-transform: uppercase; letter-spacing: 1px; color: var(--text-muted); margin-bottom: 0.3rem; }}
.card-value {{ font-family: 'Oswald', sans-serif; font-size: 1.6rem; color: var(--gold); }}
.card-sub {{ font-size: 0.75rem; color: var(--text-dim); margin-top: 0.2rem; }}
.chart-box {{ background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 1.5rem; margin: 1rem 0; }}
table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
th {{ text-align: left; padding: 8px 10px; border-bottom: 2px solid var(--border); color: var(--text-muted); font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px; }}
td {{ padding: 6px 10px; border-bottom: 1px solid var(--border); }}
.badge {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 600; }}
.badge-gold {{ background: rgba(212,175,55,0.15); color: var(--gold); }}
.badge-green {{ background: rgba(34,197,94,0.15); color: var(--green); }}
.badge-red {{ background: rgba(239,68,68,0.15); color: var(--red); }}
.badge-blue {{ background: rgba(74,158,255,0.15); color: var(--blue); }}
.two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }}
@media (max-width: 700px) {{ .two-col {{ grid-template-columns: 1fr; }} .grid {{ grid-template-columns: 1fr 1fr; }} }}
.footer {{ text-align: center; margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid var(--border); font-size: 0.75rem; color: var(--text-muted); }}
.quick-actions {{ display: flex; gap: 0.5rem; flex-wrap: wrap; margin: 1rem 0; }}
.qa-btn {{ display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.5rem 0.85rem;
    background: var(--surface2); border: 1px solid var(--border); border-radius: 6px;
    color: var(--text-dim); text-decoration: none; font-size: 0.8rem; transition: all 0.2s; }}
.qa-btn:hover {{ border-color: var(--gold); color: var(--gold); background: var(--gold-dim); }}
{_peer_review_styles()}
</style>
</head>
<body>
<div class="main">

<h1>{_esc(title)}</h1>
<div class="meta">
    Paper Intelligence Report &mdash; Schema {_esc(row.get('schema_version', ''))} &mdash; {_esc(analyzed)}<br/>
    {layer_html}
</div>
{quick_actions_html}

<!-- ══════════ KEY METRICS ══════════ -->
<div class="grid">
    {review_card_html}
    <div class="card">
        <div class="card-label">CHI Score</div>
        <div class="card-value">{chi:.2f}</div>
        <div class="card-sub">{_esc(chi_status)}</div>
    </div>
    <div class="card">
        <div class="card-label">Truth Score</div>
        <div class="card-value">{truth:.2f}</div>
        <div class="card-sub">Coherence: {coherence:.3f}</div>
    </div>
    <div class="card">
        <div class="card-label">Academic Grade</div>
        <div class="card-value">{_esc(grade)}</div>
        <div class="card-sub">{_esc(reading_level)}</div>
    </div>
    <div class="card">
        <div class="card-label">CKG Tier</div>
        <div class="card-value" style="font-size:1.2rem">{_esc(ckg)}</div>
        <div class="card-sub">{words:,} words</div>
    </div>
    <div class="card">
        <div class="card-label">Idea Density</div>
        <div class="card-value">{idea_density:.3f}</div>
        <div class="card-sub">{_esc(idea_level)}</div>
    </div>
    <div class="card">
        <div class="card-label">Fruit &minus; Anti</div>
        <div class="card-value" style="color:{'var(--green)' if fruit_net > 0 else 'var(--red)'}">{'+' if fruit_net > 0 else ''}{fruit_net:.3f}</div>
        <div class="card-sub">Emotion net score</div>
    </div>
    <div class="card">
        <div class="card-label">Vocab Diversity</div>
        <div class="card-value">{mtld:.0f}</div>
        <div class="card-sub">MTLD</div>
    </div>
    <div class="card">
        <div class="card-label">Claims Analyzed</div>
        <div class="card-value">{claims}</div>
        <div class="card-sub">{contradictions} contradictions</div>
    </div>
</div>

{peer_review_html}

<!-- ══════════ DOCUMENT PROFILE ══════════ -->
<h2>Document Profile</h2>
<div class="grid" style="grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));">
    <div class="card">
        <div class="card-label">Coherence</div>
        <div class="card-value" style="font-size:1.1rem;color:{'var(--green)' if pa_coh_flag == 'FOCUSED' else ('var(--orange)' if pa_coh_flag == 'MODERATE' else 'var(--red)')}">{_esc(pa_coh_flag) or 'N/A'}</div>
        <div class="card-sub">topic drift: {pa_drift_avg:.2f}</div>
    </div>
    <div class="card">
        <div class="card-label">Signal / Noise</div>
        <div class="card-value">{pa_snr:.2f}</div>
        <div class="card-sub">density: {_esc(pa_density)}</div>
    </div>
    <div class="card">
        <div class="card-label">Flow</div>
        <div class="card-value" style="font-size:1.1rem">{_esc(pa_flow) or 'N/A'}</div>
        <div class="card-sub">{pa_reading_min:.1f} min read</div>
    </div>
    <div class="card">
        <div class="card-label">Wisdom / Knowledge</div>
        <div class="card-value">{wk_ratio:.2f}</div>
        <div class="card-sub">W:{wisdom:.1f} K:{knowledge:.1f}</div>
    </div>
    <div class="card">
        <div class="card-label">Warmth</div>
        <div class="card-value">{warmth:.2f}</div>
        <div class="card-sub">Discipline: {discipline:.2f}</div>
    </div>
    <div class="card">
        <div class="card-label">Threat / Protect</div>
        <div class="card-value" style="color:{'var(--green)' if balance_score >= 0 else 'var(--red)'}">{'+' if balance_score >= 0 else ''}{balance_score:.1f}</div>
        <div class="card-sub">T:{threat_score:.1f} P:{protection_score:.1f}</div>
    </div>
</div>

<!-- ══════════ ACADEMIC RUBRIC ══════════ -->
<h2>Academic Rubric Breakdown</h2>
<div class="grid" style="grid-template-columns: repeat(5, 1fr);">
    <div class="card" style="text-align:center">
        <div class="card-label">Structure</div>
        <div style="height:4px;background:#1a1a1a;border-radius:2px;overflow:hidden;margin:0.5rem 0"><div style="width:{min(rub_struct/5*100,100):.0f}%;height:100%;background:var(--gold);border-radius:2px"></div></div>
        <div class="mono" style="font-size:0.85rem;color:var(--gold)">{rub_struct}/5</div>
    </div>
    <div class="card" style="text-align:center">
        <div class="card-label">Grounding</div>
        <div style="height:4px;background:#1a1a1a;border-radius:2px;overflow:hidden;margin:0.5rem 0"><div style="width:{min(rub_ground/5*100,100):.0f}%;height:100%;background:var(--gold);border-radius:2px"></div></div>
        <div class="mono" style="font-size:0.85rem;color:var(--gold)">{rub_ground}/5</div>
    </div>
    <div class="card" style="text-align:center">
        <div class="card-label">Claims</div>
        <div style="height:4px;background:#1a1a1a;border-radius:2px;overflow:hidden;margin:0.5rem 0"><div style="width:{min(rub_claim/5*100,100):.0f}%;height:100%;background:var(--gold);border-radius:2px"></div></div>
        <div class="mono" style="font-size:0.85rem;color:var(--gold)">{rub_claim}/5</div>
    </div>
    <div class="card" style="text-align:center">
        <div class="card-label">Quantitative</div>
        <div style="height:4px;background:#1a1a1a;border-radius:2px;overflow:hidden;margin:0.5rem 0"><div style="width:{min(rub_quant/5*100,100):.0f}%;height:100%;background:var(--gold);border-radius:2px"></div></div>
        <div class="mono" style="font-size:0.85rem;color:var(--gold)">{rub_quant}/5</div>
    </div>
    <div class="card" style="text-align:center">
        <div class="card-label">Falsifiability</div>
        <div style="height:4px;background:#1a1a1a;border-radius:2px;overflow:hidden;margin:0.5rem 0"><div style="width:{min(rub_falsif/5*100,100):.0f}%;height:100%;background:var(--gold);border-radius:2px"></div></div>
        <div class="mono" style="font-size:0.85rem;color:var(--gold)">{rub_falsif}/5</div>
    </div>
</div>

<!-- ══════════ CHARACTER ATTRIBUTES ══════════ -->
<h2>Character Attributes &mdash; 8 Dimensions</h2>
<div class="grid" style="grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));">
    {''.join(f"""<div class="card">
        <div class="card-label">{_esc(label)}</div>
        <div class="card-value" style="font-size:1.2rem;color:{'var(--green)' if net > 0 else ('var(--red)' if net < 0 else 'var(--text-muted)')}">{'+' if net > 0 else ''}{net:.2f}</div>
        <div class="card-sub">{_esc(kind)} &middot; +{pos} &minus;{neg} &middot; str:{strength:.2f}</div>
    </div>""" for label, net, strength, kind, pos, neg in char_attr_data)}
</div>
{'<div class="card" style="margin:1rem 0"><div style="font-size:0.8rem;color:var(--text-dim)"><strong>Threats:</strong> ' + _esc(primary_threats) + ' &nbsp;|&nbsp; <strong>Protections:</strong> ' + _esc(primary_protections) + '</div></div>' if primary_threats or primary_protections else ''}

<!-- ══════════ FRUITS RADAR ══════════ -->
<h2>Fruits of the Spirit &mdash; Dual Channel</h2>
<div class="two-col">
    <div class="chart-box">
        <canvas id="fruitRadar" height="300"></canvas>
    </div>
    <div class="chart-box">
        <h3>Fruits Comparison Table</h3>
        <table>
            <tr><th>Fruit</th><th>L6 (Lexical)</th><th>L8 (Emotion)</th><th>Anti-Fruit</th><th>Avg</th></tr>
            {''.join(_fruit_row(
                fruit_labels[i],
                l6_fruits[i],
                l8_fruits[i],
                anti_vals[i] if i < len(anti_vals) else 0
            ) for i in range(9))}
        </table>
    </div>
</div>

<!-- ══════════ 27 EMOTIONS ══════════ -->
<h2>GoEmotions &mdash; 27 Fine-Grained Emotions</h2>
<div class="chart-box">
    <canvas id="emoBar" height="200"></canvas>
    <div style="margin-top:0.8rem;font-size:0.8rem;color:var(--text-dim)">
        <strong>Dominant:</strong> {_esc(emo_dominant)} &nbsp;|&nbsp; <strong>Top 5:</strong> {_esc(emo_top5)}
    </div>
</div>

<!-- ══════════ NRC PLUTCHIK ══════════ -->
<h2>NRC Plutchik Emotion Wheel</h2>
<div class="two-col">
    <div class="chart-box">
        <canvas id="nrcRadar" height="280"></canvas>
    </div>
    <div class="chart-box">
        <h3>NRC Top Emotions</h3>
        <div style="font-size:0.85rem;color:var(--text-dim);line-height:2">{_esc(nrc_top).replace(', ', '<br/>')}</div>
    </div>
</div>

<!-- ══════════ MASTER EQUATION ══════════ -->
<h2>Master Equation Variables</h2>
<div class="chart-box">
    <canvas id="meBar" height="200"></canvas>
</div>

<!-- ══════════ CLAIMS ══════════ -->
<h2>Claims Analysis</h2>
<div class="grid" style="grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));">
    <div class="card"><div class="card-label">Total Claims</div><div class="card-value">{claims}</div></div>
    <div class="card"><div class="card-label">Anchored</div><div class="card-value" style="color:var(--green)">{anchored}</div></div>
    <div class="card"><div class="card-label">Under-Supported</div><div class="card-value" style="color:var(--orange)">{under}</div></div>
    <div class="card"><div class="card-label">Overstated</div><div class="card-value" style="color:var(--red)">{over}</div></div>
    <div class="card"><div class="card-label">Falsifiable</div><div class="card-value" style="color:var(--blue)">{falsifiable}</div></div>
    <div class="card"><div class="card-label">Speculative</div><div class="card-value" style="color:var(--text-muted)">{speculative}</div></div>
</div>

<!-- ══════════ CHARACTER ══════════ -->
<h2>Character Profile</h2>
<div class="card" style="margin:1rem 0">
    <div style="margin-bottom:0.5rem"><span class="badge badge-gold">{_esc(posture)}</span></div>
    <div style="font-size:0.85rem;color:var(--text-dim)">{_esc(integrity)}</div>
</div>

<!-- ══════════ KEY SENTENCES ══════════ -->
{'<h2>Key Sentences</h2><div class="card" style="margin:1rem 0"><ol style="font-size:0.85rem;color:var(--text-dim);line-height:1.7;padding-left:1.2rem;margin:0">' + (('<li style="margin-bottom:0.5rem">' + _esc(key_sent_1) + '</li>') if key_sent_1 else '') + (('<li style="margin-bottom:0.5rem">' + _esc(key_sent_2) + '</li>') if key_sent_2 else '') + (('<li style="margin-bottom:0.5rem">' + _esc(key_sent_3) + '</li>') if key_sent_3 else '') + '</ol></div>' if (key_sent_1 or key_sent_2 or key_sent_3) else ''}

<!-- ══════════ KEYWORDS ══════════ -->
<h2>Keywords &amp; Entities</h2>
<div class="two-col">
    <div class="card">
        <h3>Keywords (YAKE)</h3>
        <div style="font-size:0.8rem;color:var(--text-dim);line-height:1.8">
            {(_esc(yake_kw or row.get('L1_keybert_keywords', '') or '')).replace(' | ', '<br/>')}
        </div>
    </div>
    <div class="card">
        <h3>NLP Entities</h3>
        <div style="font-size:0.8rem;color:var(--text-dim);line-height:1.8">
            <strong>People:</strong> {_esc(row.get('L5_entity_people', 'N/A'))}<br/>
            <strong>Orgs:</strong> {_esc(row.get('L5_entity_orgs', 'N/A'))}<br/>
            <strong>Count:</strong> {row.get('L5_entity_count', 0)} entities, {_esc(row.get('L5_entity_types_found', ''))}
        </div>
    </div>
</div>

{'<h2>Knowledge Graph Position</h2><div class="card" style="margin:1rem 0"><div style="font-size:0.85rem;color:var(--text-dim)"><strong>Centrality:</strong> ' + _esc(centrality) + ' &nbsp;|&nbsp; <strong>Cluster:</strong> ' + _esc(cluster) + '</div></div>' if centrality else ''}

<div class="footer">
    Theophysics Paper Intelligence Pipeline v{_esc(row.get('schema_version', '2026'))} &mdash; 10-Layer Analysis + Peer-Review Snapshot<br/>
    Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}
</div>

</div>

<script>
{_peer_review_script()}

// Fruits Radar
new Chart(document.getElementById('fruitRadar'), {{
    type: 'radar',
    data: {{
        labels: {json.dumps(fruit_labels)},
        datasets: [
            {{ label: 'L6 Lexical', data: {json.dumps(l6_fruits)}, borderColor: '#d4af37', backgroundColor: 'rgba(212,175,55,0.1)', pointBackgroundColor: '#d4af37' }},
            {{ label: 'L8 Emotion', data: {json.dumps(l8_fruits)}, borderColor: '#22c55e', backgroundColor: 'rgba(34,197,94,0.1)', pointBackgroundColor: '#22c55e' }}
        ]
    }},
    options: {{
        responsive: true,
        scales: {{ r: {{ beginAtZero: true, grid: {{ color: '#2a2a2a' }}, ticks: {{ display: false }}, pointLabels: {{ color: '#a0a0a0', font: {{ size: 11 }} }} }} }},
        plugins: {{ legend: {{ labels: {{ color: '#a0a0a0' }} }} }}
    }}
}});

// GoEmotions Bar
new Chart(document.getElementById('emoBar'), {{
    type: 'bar',
    data: {{
        labels: {json.dumps([l.title() for l in emo_labels_27])},
        datasets: [{{ data: {json.dumps(emo_values_27)}, backgroundColor: {json.dumps(emo_values_27)}.map(v => v > 0.1 ? '#d4af37' : v > 0.01 ? 'rgba(212,175,55,0.5)' : 'rgba(212,175,55,0.15)') }}]
    }},
    options: {{
        responsive: true, indexAxis: 'y',
        scales: {{ x: {{ grid: {{ color: '#1a1a1a' }}, ticks: {{ color: '#666' }} }}, y: {{ ticks: {{ color: '#a0a0a0', font: {{ size: 10 }} }} }} }},
        plugins: {{ legend: {{ display: false }} }}
    }}
}});

// NRC Radar
new Chart(document.getElementById('nrcRadar'), {{
    type: 'radar',
    data: {{
        labels: {json.dumps([l.title() for l in nrc_labels])},
        datasets: [{{ label: 'NRC', data: {json.dumps(nrc_values)}, borderColor: '#4a9eff', backgroundColor: 'rgba(74,158,255,0.1)', pointBackgroundColor: '#4a9eff' }}]
    }},
    options: {{
        responsive: true,
        scales: {{ r: {{ beginAtZero: true, grid: {{ color: '#2a2a2a' }}, ticks: {{ display: false }}, pointLabels: {{ color: '#a0a0a0', font: {{ size: 11 }} }} }} }},
        plugins: {{ legend: {{ display: false }} }}
    }}
}});

// Master Equation Bar
new Chart(document.getElementById('meBar'), {{
    type: 'bar',
    data: {{
        labels: {json.dumps(me_labels)},
        datasets: [{{ data: {json.dumps(me_values)}, backgroundColor: '#d4af37' }}]
    }},
    options: {{
        responsive: true,
        scales: {{ x: {{ ticks: {{ color: '#a0a0a0', font: {{ size: 10 }} }} }}, y: {{ beginAtZero: true, grid: {{ color: '#1a1a1a' }}, ticks: {{ color: '#666' }} }} }},
        plugins: {{ legend: {{ display: false }} }}
    }}
}});
</script>
</body>
</html>'''
    return html


def main():
    parser = argparse.ArgumentParser(description="Generate HTML scorecards from pipeline JSON or snapshot")
    parser.add_argument('--json', required=True, help='Path to pipeline results JSON or snapshot JSON')
    parser.add_argument('--output', default=None, help='Output directory (default: same as JSON)')
    parser.add_argument('--single', action='store_true', help='Generate one combined report')
    parser.add_argument('--snapshot', action='store_true',
                        help='Force snapshot interpretation (auto-detected when omitted)')
    args = parser.parse_args()

    in_path = Path(args.json)
    data = json.loads(in_path.read_text(encoding='utf-8'))
    if not isinstance(data, list):
        data = [data]

    out_dir = Path(args.output) if args.output else in_path.parent / "html_reports"
    out_dir.mkdir(parents=True, exist_ok=True)

    for row in data:
        is_snap = args.snapshot or _is_snapshot(row)
        # Filename derivation works for both shapes
        fname_src = row.get('file') or row.get('paper_id') or 'unknown'
        fname = str(fname_src)
        for suffix in ('.md', '.markdown', '.html', '.htm', '.txt'):
            if fname.lower().endswith(suffix):
                fname = fname[: -len(suffix)]
                break
        snapshot_href = None
        if is_snap:
            # Same-folder snapshot JSON name (Package A convention)
            snapshot_href = f"{fname}_snapshot.json"
        html_str = generate_paper_html(row, snapshot_path=snapshot_href)
        path = out_dir / f"PI_{fname}.html"
        path.write_text(html_str, encoding='utf-8')
        print(f"  Generated: {path.name}")

    print(f"\n{len(data)} HTML reports written to {out_dir}")


if __name__ == '__main__':
    main()
