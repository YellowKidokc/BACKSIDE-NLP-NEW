"""
7Q HTML Report Generator — Beautiful per-claim cover pages.

Takes a scored ClaimProfile + ScoreResult and generates a self-contained
HTML report using the same dark theme as the 7Q method pages.

Each scored claim gets its own .html file that can be:
  - Opened locally in any browser
  - Hosted as a static page
  - Used as a "cover page" for papers

David Lowe | POF 2828 | March 2026
"""

import os
from datetime import datetime
from scorer import ClaimProfile, ScoreResult
from id_system import (
    DOMAINS, Q0_MODE, Q1_ENTITY_TYPE, Q1_AXIOM_CLASS, Q1_STATUS, Q1_SOURCE,
    Q2_CROSS_DOMAIN_MULTIPLIER, Q2_ISO_STATUS,
    Q3_CLAIM_TYPE, Q3_PRECISION, Q3_CERTAINTY, Q3_SCOPE,
    Q4_EVIDENCE_TYPE, Q4_TIER, Q4_STRENGTH, Q4_LINKAGE,
    Q5_TERMINUS, Q5_DERIVATION,
    Q6_PREDICTION_TYPE, Q6_COMPETING,
    Q7_DEATH_TYPES, Q7_ROBUSTNESS, Q7_CASCADE_SCOPE,
    get_confidence_class,
)


def _label(registry, key, field="label"):
    entry = registry.get(key, {})
    return entry.get(field, key) if isinstance(entry, dict) else str(entry)


def _score_color(val):
    """Return CSS color for a 0-1 score."""
    if val >= 0.85:
        return "#2dd4a0"
    elif val >= 0.65:
        return "#38bdf8"
    elif val >= 0.40:
        return "#f59e0b"
    elif val >= 0.15:
        return "#f97316"
    else:
        return "#ef4444"


def _bar_html(label, value, color, max_width=200):
    """Generate a score bar."""
    w = int(value * max_width)
    return f'''<div class="bar-row">
  <span class="bar-label">{label}</span>
  <div class="bar-track"><div class="bar-fill" style="width:{w}px;background:{color}"></div></div>
  <span class="bar-val" style="color:{color}">{value:.2f}</span>
</div>'''


def _death_icon(result):
    return {"SURVIVES": "&#x2713;", "DIES": "&#x2620;", "WEAKENED": "&#x26A0;", "UNTESTED": "&#x25CB;"}.get(result, "?")


def _death_color(result):
    return {"SURVIVES": "#2dd4a0", "DIES": "#ef4444", "WEAKENED": "#f59e0b", "UNTESTED": "#555869"}.get(result, "#555869")


# ═══════════════════════════════════════════════
# TREE SVG (inline, data-driven)
# ═══════════════════════════════════════════════

def build_tree_svg(result: ScoreResult) -> str:
    """Build an inline SVG tree where each part's opacity reflects its score."""
    q = result.q_scores

    def op(key, floor=0.15):
        return max(floor, min(1.0, q.get(key, 0)))

    return f'''<svg viewBox="0 0 200 320" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:280px;height:auto">
  <!-- Bedrock (Q5) -->
  <rect x="0" y="260" width="200" height="60" fill="#2a2035" opacity="{op('Q5') * 0.8:.2f}"/>
  <text x="100" y="295" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="8" fill="#a0724a" opacity="0.7">Q5 GROUND ({q.get('Q5',0):.2f})</text>
  <!-- Roots -->
  <path d="M100 200 C75 225 35 235 15 260" stroke="#a0724a" stroke-width="{2 + op('Q5') * 2:.1f}" fill="none" opacity="{op('Q5'):.2f}"/>
  <path d="M100 200 C125 225 165 235 185 260" stroke="#a0724a" stroke-width="{2 + op('Q5') * 2:.1f}" fill="none" opacity="{op('Q5'):.2f}"/>
  <path d="M100 200 C100 230 100 250 100 270" stroke="#a0724a" stroke-width="{1 + op('Q5'):.1f}" fill="none" opacity="{op('Q5') * 0.7:.2f}"/>
  <!-- Soil (Q2) -->
  <rect x="0" y="185" width="200" height="15" fill="#7c6340" opacity="{op('Q2') * 0.8:.2f}"/>
  <text x="100" y="195" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="7" fill="#7c6340" opacity="0.8">Q2 ({q.get('Q2',0):.2f})</text>
  <!-- Trunk (Q3) -->
  <rect x="90" y="100" width="20" height="85" rx="3" fill="#5c3d2e" opacity="{op('Q3') * 0.9:.2f}"/>
  <line x1="100" y1="180" x2="100" y2="105" stroke="#6b8c42" stroke-width="1.5" stroke-dasharray="4,3" opacity="{op('Q3') * 0.6:.2f}"/>
  <!-- Canopy (Q6) -->
  <ellipse cx="100" cy="65" rx="65" ry="48" fill="#2d5a2a" opacity="{op('Q6') * 0.85:.2f}"/>
  <ellipse cx="78" cy="55" rx="40" ry="32" fill="#3a6b35" opacity="{op('Q6') * 0.75:.2f}"/>
  <ellipse cx="125" cy="60" rx="35" ry="28" fill="#336630" opacity="{op('Q6') * 0.7:.2f}"/>
  <text x="100" y="68" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="8" fill="#34d399" opacity="0.8">Q6 ({q.get('Q6',0):.2f})</text>
  <!-- Fruit (predictions) -->
  <circle cx="60" cy="82" r="6" fill="#d4a853" opacity="{op('Q6') * 0.8:.2f}"/>
  <circle cx="145" cy="78" r="6" fill="#d4a853" opacity="{op('Q6') * 0.7:.2f}"/>
  <circle cx="100" cy="35" r="5" fill="#d4a853" opacity="{op('Q6') * 0.6:.2f}"/>
  <!-- Rain (Q4 evidence) -->
  <line x1="55" y1="12" x2="62" y2="48" stroke="#38bdf8" stroke-width="1.5" opacity="{op('Q4') * 0.7:.2f}"/>
  <line x1="100" y1="8" x2="100" y2="44" stroke="#38bdf8" stroke-width="1.5" opacity="{op('Q4') * 0.6:.2f}"/>
  <line x1="148" y1="10" x2="142" y2="46" stroke="#38bdf8" stroke-width="1.5" opacity="{op('Q4') * 0.7:.2f}"/>
  <text x="100" y="8" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="7" fill="#38bdf8" opacity="0.7">Q4 ({q.get('Q4',0):.2f})</text>
  <!-- Axe (Q7) -->
  <line x1="18" y1="145" x2="85" y2="145" stroke="#ef4444" stroke-width="{1 + (1 - op('Q7')) * 3:.1f}" opacity="{max(0.2, 1 - op('Q7')):.2f}"/>
  <polygon points="14,138 18,145 14,152 8,145" fill="#ef4444" opacity="{max(0.15, 1 - op('Q7')):.2f}"/>
  <!-- Seed (Q1) -->
  <ellipse cx="100" cy="190" rx="6" ry="4" fill="#d4a853" opacity="{op('Q1') * 0.7:.2f}"/>
  <text x="100" y="210" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="7" fill="#d4a853" opacity="0.7">Q1 ({q.get('Q1',0):.2f})</text>
</svg>'''


# ═══════════════════════════════════════════════
# FULL HTML REPORT
# ═══════════════════════════════════════════════

def build_html_report(profile: ClaimProfile, result: ScoreResult, mode: str = "forward") -> str:
    """Generate a self-contained HTML report for a scored claim."""
    domain_label = DOMAINS.get(profile.domain, profile.domain)
    entity_label = _label(Q1_ENTITY_TYPE, profile.entity_type)
    status_label = _label(Q1_STATUS, profile.status)
    xdm_entry = Q2_CROSS_DOMAIN_MULTIPLIER.get(profile.cross_domain_key, {})
    t_color = _score_color(result.T_final)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Q scores
    q_labels = {"Q0": "Posture", "Q1": "Identity", "Q2": "Domain", "Q3": "Assertion",
                "Q4": "Evidence", "Q5": "Dependencies", "Q6": "Consequences", "Q7": "Falsification"}

    # Score bars HTML
    bars = []
    for qk in ["Q0", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7"]:
        v = result.q_scores.get(qk, 0)
        bars.append(_bar_html(f"{qk} {q_labels[qk]}", v, _score_color(v)))
    bars_html = "\n".join(bars)

    # Pillar bars
    pillar_bars = "\n".join([
        _bar_html("S Structural", result.S, _score_color(result.S)),
        _bar_html("E Evidence", result.E, _score_color(result.E)),
        _bar_html("L Logical", result.L, _score_color(result.L)),
        _bar_html("D Discriminatory", result.D, _score_color(result.D)),
        _bar_html("P Posture", result.P, _score_color(result.P)),
        _bar_html("C Combat", result.C, _score_color(result.C)),
    ])

    # Evidence cards
    ev_cards = []
    for i, ev in enumerate(profile.evidence, 1):
        ev_type_label = _label(Q4_EVIDENCE_TYPE, ev.evidence_type)
        tier_label = _label(Q4_TIER, ev.tier)
        str_label = _label(Q4_STRENGTH, ev.strength)
        vulns = ", ".join(ev.vulnerabilities) if ev.vulnerabilities else "None"
        from scorer import score_evidence_item
        ev_score = score_evidence_item(ev, profile.domain)
        ev_cards.append(f'''<div class="ev-card">
  <div class="ev-num">E{i}</div>
  <div class="ev-body">
    <div class="ev-name">{ev.name}</div>
    <div class="ev-meta">{ev.evidence_type} ({ev_type_label}) &middot; Tier {ev.tier} &middot; {ev.strength}</div>
    <div class="ev-channels">
      <div class="ch"><span class="ch-label" style="color:var(--ps)">PS</span><span class="ch-val">{ev_score["ps"]:.2f}</span></div>
      <div class="ch"><span class="ch-label" style="color:var(--ed)">ED</span><span class="ch-val">{ev.ed:.2f}</span></div>
      <div class="ch"><span class="ch-label" style="color:var(--ec)">EC</span><span class="ch-val">{ev.ec:.2f}</span></div>
      <div class="ch"><span class="ch-label" style="color:var(--gold)">CF</span><span class="ch-val">{ev_score["cf"]:.2f}</span></div>
      <div class="ch"><span class="ch-label" style="color:var(--text)">E</span><span class="ch-val">{ev_score["e_item"]:.2f}</span></div>
    </div>
    {"<div class='ev-why'>WHY-PENALTY ACTIVE</div>" if ev_score["why_capped"] else ""}
    <div class="ev-vulns">Vulns: {vulns}</div>
  </div>
</div>''')
    ev_html = "\n".join(ev_cards) if ev_cards else '<div class="empty">No evidence entered.</div>'

    # Death tests
    death_rows = []
    for dt in profile.death_tests:
        dtype_label = Q7_DEATH_TYPES.get(dt.death_type, {}).get("label", dt.death_type)
        icon = _death_icon(dt.result)
        color = _death_color(dt.result)
        notes = f'<div class="dt-notes">{dt.notes}</div>' if dt.notes else ""
        death_rows.append(f'''<div class="dt-row">
  <span class="dt-icon" style="color:{color}">{icon}</span>
  <div class="dt-body">
    <div class="dt-type">{dt.death_type}</div>
    <div class="dt-label">{dtype_label}</div>
    <div class="dt-result" style="color:{color}">{dt.result}</div>
    {notes}
  </div>
</div>''')
    death_html = "\n".join(death_rows)

    # Predictions
    pred_rows = []
    for i, p in enumerate(profile.predictions, 1):
        conf = '<span style="color:#2dd4a0">CONFIRMED</span>' if p.confirmed else '<span style="color:#555869">unconfirmed</span>'
        pred_rows.append(f'''<div class="pred-row">
  <span class="pred-num">P{i}</span>
  <div class="pred-body">
    <div class="pred-desc">{p.description}</div>
    <div class="pred-meta">{p.pred_type} &middot; {_label(Q6_COMPETING, p.competing)} &middot; {conf}</div>
  </div>
</div>''')
    pred_html = "\n".join(pred_rows) if pred_rows else '<div class="empty">No predictions listed.</div>'

    # Dependencies
    deps_html = ""
    for dep in profile.dependency_chain:
        deps_html += f'<div class="dep-item">{dep}</div>\n'
    if not deps_html:
        deps_html = '<div class="empty">None listed.</div>'

    tree_svg = build_tree_svg(result)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>7Q Report: {profile.claim_text[:60]}</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;600&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {{
  --bg:#0a0b0f;--card:#12141c;--border:#1e2233;--border2:#2a3050;
  --text:#e8e6e1;--text2:#8a8d9b;--text3:#555869;--gold:#d4a853;
  --ps:#38bdf8;--ed:#a78bfa;--ec:#34d399;--fail:#ef4444;--pass:#2dd4a0;--warn:#f59e0b;
  --q0:#8a8d9b;--q1:#d4a853;--q2:#7c6340;--q3:#6b8c42;--q4:#38bdf8;
  --q5:#a0724a;--q6:#34d399;--q7:#ef4444;
}}
*{{margin:0;padding:0;box-sizing:border-box}}
html{{scroll-behavior:smooth;background:var(--bg)}}
body{{font-family:'DM Sans',sans-serif;color:var(--text);background:var(--bg);min-height:100vh}}
body::before{{content:'';position:fixed;inset:0;background:radial-gradient(ellipse at 20% 0%,rgba(56,189,248,0.03),transparent 50%),radial-gradient(ellipse at 80% 100%,rgba(167,139,250,0.03),transparent 50%);pointer-events:none}}
.container{{position:relative;z-index:1;max-width:1000px;margin:0 auto;padding:40px 24px 80px}}

/* Hero */
.hero{{text-align:center;padding:48px 0 40px;border-bottom:1px solid var(--border);margin-bottom:40px}}
.hero-tag{{font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:4px;text-transform:uppercase;color:var(--gold);margin-bottom:14px}}
.hero h1{{font-family:'Cormorant Garamond',serif;font-size:clamp(26px,4vw,44px);font-weight:700;line-height:1.15;margin-bottom:16px}}
.hero .sub{{font-size:14px;color:var(--text2);max-width:650px;margin:0 auto;line-height:1.7}}

/* Badges */
.badges{{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin:20px 0}}
.badge{{padding:6px 12px;border:1px solid var(--border);border-radius:999px;font-size:12px;color:var(--text2);background:var(--card)}}
.badge.gold{{border-color:rgba(212,168,83,0.4);color:var(--gold)}}

/* Big Score */
.big-score{{text-align:center;padding:32px;margin:32px 0;border:1px solid var(--border2);border-radius:18px;background:linear-gradient(180deg,rgba(18,20,28,0.95),rgba(10,11,15,0.96))}}
.big-score .t-val{{font-family:'Cormorant Garamond',serif;font-size:72px;font-weight:700;line-height:1}}
.big-score .t-label{{font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:3px;text-transform:uppercase;color:var(--text2);margin-top:8px}}
.big-score .t-class{{font-family:'JetBrains Mono',monospace;font-size:14px;letter-spacing:2px;margin-top:6px}}

/* Layout */
.grid-2{{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin:32px 0}}
@media(max-width:700px){{.grid-2{{grid-template-columns:1fr}}}}
.panel{{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:24px}}
.panel-title{{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:2px;text-transform:uppercase;color:var(--gold);margin-bottom:16px}}

/* Score Bars */
.bar-row{{display:flex;align-items:center;gap:10px;margin-bottom:10px}}
.bar-label{{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--text2);width:140px;flex-shrink:0}}
.bar-track{{flex:1;height:6px;background:rgba(255,255,255,0.05);border-radius:3px;overflow:hidden}}
.bar-fill{{height:100%;border-radius:3px;transition:width 0.6s ease}}
.bar-val{{font-family:'JetBrains Mono',monospace;font-size:12px;width:40px;text-align:right}}

/* Evidence Cards */
.ev-card{{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:16px;margin-bottom:12px;border-left:3px solid var(--ps)}}
.ev-num{{font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--gold);letter-spacing:2px;margin-bottom:6px}}
.ev-name{{font-weight:600;margin-bottom:4px}}
.ev-meta{{font-size:12px;color:var(--text3);margin-bottom:10px}}
.ev-channels{{display:flex;gap:16px;flex-wrap:wrap}}
.ch{{display:flex;flex-direction:column;align-items:center;gap:2px}}
.ch-label{{font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:1px}}
.ch-val{{font-family:'JetBrains Mono',monospace;font-size:14px;font-weight:600}}
.ev-why{{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--fail);margin-top:8px;padding:4px 8px;background:rgba(239,68,68,0.08);border-radius:4px;display:inline-block}}
.ev-vulns{{font-size:11px;color:var(--text3);margin-top:6px}}

/* Death Tests */
.dt-row{{display:flex;gap:14px;align-items:start;padding:12px 0;border-bottom:1px solid rgba(255,255,255,0.03)}}
.dt-icon{{font-size:20px;width:28px;text-align:center;flex-shrink:0}}
.dt-type{{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:1px;color:var(--text3)}}
.dt-label{{font-size:13px;color:var(--text2)}}
.dt-result{{font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:600;margin-top:2px}}
.dt-notes{{font-size:12px;color:var(--text3);margin-top:2px;font-style:italic}}

/* Predictions */
.pred-row{{display:flex;gap:12px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.03)}}
.pred-num{{font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--q6);width:24px;flex-shrink:0}}
.pred-desc{{font-size:13px;color:var(--text)}}
.pred-meta{{font-size:11px;color:var(--text3);margin-top:2px}}

/* Dependencies */
.dep-item{{padding:8px 12px;margin-bottom:6px;background:rgba(160,114,74,0.06);border:1px solid rgba(160,114,74,0.15);border-radius:6px;font-size:13px;color:var(--text2)}}

/* Tree */
.tree-center{{text-align:center;padding:20px 0}}

/* Footer */
.footer{{text-align:center;padding:32px;border-top:1px solid var(--border);margin-top:32px}}
.footer p{{font-size:12px;color:var(--text3);line-height:1.7}}
.empty{{font-size:13px;color:var(--text3);font-style:italic;padding:8px 0}}

/* Section titles */
.section{{margin:40px 0;padding-bottom:32px;border-bottom:1px solid var(--border)}}
.s-tag{{font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:3px;text-transform:uppercase;margin-bottom:8px}}
.s-title{{font-family:'Cormorant Garamond',serif;font-size:clamp(22px,3vw,32px);font-weight:700;margin-bottom:12px}}

/* Info grid */
.info-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin:20px 0}}
.info-cell{{padding:12px;background:var(--card);border:1px solid var(--border);border-radius:8px}}
.info-cell .info-label{{font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:1px;color:var(--text3);text-transform:uppercase;margin-bottom:4px}}
.info-cell .info-val{{font-size:14px;font-weight:500}}
</style>
</head>
<body>
<div class="container">

<div class="hero">
  <div class="hero-tag">7Q Scored Report &middot; {mode.upper()}</div>
  <h1>{profile.claim_text}</h1>
  <div class="sub">{profile.claim_id} &middot; {domain_label} &middot; {entity_label} &middot; {status_label}</div>
  <div class="badges">
    <span class="badge">{profile.domain}</span>
    <span class="badge">{profile.entity_type}</span>
    <span class="badge">{profile.status}</span>
    <span class="badge">XDM x{result.xdm:.2f}</span>
    <span class="badge gold">{result.confidence_class}</span>
  </div>
</div>

<!-- BIG SCORE -->
<div class="big-score">
  <div class="t-val" style="color:{t_color}">{result.T_final:.3f}</div>
  <div class="t-label">Truth Score (Enhanced)</div>
  <div class="t-class" style="color:{t_color}">{result.confidence_class} &mdash; {result.confidence_label}</div>
  <div style="font-size:12px;color:var(--text3);margin-top:8px">T_raw: {result.T_raw:.4f} &times; XDM {result.xdm:.2f} = T_final: {result.T_final:.4f}</div>
</div>

<!-- TREE + SCORES -->
<div class="grid-2">
  <div class="panel">
    <div class="panel-title">Tree Health</div>
    <div class="tree-center">{tree_svg}</div>
  </div>
  <div class="panel">
    <div class="panel-title">Q0&ndash;Q7 Scores</div>
    {bars_html}
    <div style="margin-top:20px;padding-top:16px;border-top:1px solid var(--border)">
      <div class="panel-title">Six Pillars</div>
      {pillar_bars}
    </div>
  </div>
</div>

<!-- IDENTITY -->
<div class="section">
  <div class="s-tag" style="color:var(--q1)">Q1 &mdash; Identity</div>
  <div class="info-grid">
    <div class="info-cell"><div class="info-label">Entity Type</div><div class="info-val">{profile.entity_type} &mdash; {entity_label}</div></div>
    <div class="info-cell"><div class="info-label">Axiom Class</div><div class="info-val">{profile.axiom_class} &mdash; {_label(Q1_AXIOM_CLASS, profile.axiom_class)}</div></div>
    <div class="info-cell"><div class="info-label">Status</div><div class="info-val">{profile.status} &mdash; {status_label}</div></div>
    <div class="info-cell"><div class="info-label">Source</div><div class="info-val">{profile.source} &mdash; {_label(Q1_SOURCE, profile.source)}</div></div>
  </div>
</div>

<!-- ASSERTION -->
<div class="section">
  <div class="s-tag" style="color:var(--q3)">Q3 &mdash; Assertion</div>
  <div class="info-grid">
    <div class="info-cell"><div class="info-label">Claim Type</div><div class="info-val">{profile.claim_type} &mdash; {_label(Q3_CLAIM_TYPE, profile.claim_type)}</div></div>
    <div class="info-cell"><div class="info-label">Precision</div><div class="info-val">{profile.precision} &mdash; {_label(Q3_PRECISION, profile.precision)}</div></div>
    <div class="info-cell"><div class="info-label">Certainty</div><div class="info-val">{profile.certainty} &mdash; {_label(Q3_CERTAINTY, profile.certainty)}</div></div>
    <div class="info-cell"><div class="info-label">Scope</div><div class="info-val">{profile.scope} &mdash; {_label(Q3_SCOPE, profile.scope)}</div></div>
  </div>
</div>

<!-- EVIDENCE -->
<div class="section">
  <div class="s-tag" style="color:var(--q4)">Q4 &mdash; Evidence (E = {result.E:.2f})</div>
  <div class="s-title">Three Channels. One Score.</div>
  <div style="display:flex;gap:24px;margin:16px 0;flex-wrap:wrap">
    <div style="font-family:'JetBrains Mono',monospace;font-size:13px"><span style="color:var(--ps)">PS avg:</span> {result.ps_avg:.2f}</div>
    <div style="font-family:'JetBrains Mono',monospace;font-size:13px"><span style="color:var(--ed)">CF avg:</span> {result.cf_avg:.2f}</div>
    <div style="font-family:'JetBrains Mono',monospace;font-size:13px"><span style="color:var(--text)">E_final:</span> {result.E:.2f}</div>
    {"<div style='font-family:JetBrains Mono,monospace;font-size:13px;color:var(--fail)'>Vuln penalty: " + f"{result.vuln_penalty:+.2f}</div>" if result.vuln_penalty else ""}
  </div>
  {ev_html}
</div>

<!-- DEPENDENCIES -->
<div class="section">
  <div class="s-tag" style="color:var(--q5)">Q5 &mdash; Dependencies (L = {result.L:.2f})</div>
  <div class="info-grid">
    <div class="info-cell"><div class="info-label">Terminus</div><div class="info-val">{profile.terminus} &mdash; {_label(Q5_TERMINUS, profile.terminus)}</div></div>
    <div class="info-cell"><div class="info-label">Derivation</div><div class="info-val">{profile.derivation} &mdash; {_label(Q5_DERIVATION, profile.derivation)}</div></div>
  </div>
  <div style="margin-top:12px">{deps_html}</div>
</div>

<!-- PREDICTIONS -->
<div class="section">
  <div class="s-tag" style="color:var(--q6)">Q6 &mdash; Consequences (D = {result.D:.2f})</div>
  {pred_html}
</div>

<!-- KILL CONDITIONS -->
<div class="section" style="border-bottom:none">
  <div class="s-tag" style="color:var(--q7)">Q7 &mdash; Falsification (C = {result.C:.2f})</div>
  <div class="s-title">Five Death Types</div>
  {death_html}
  <div class="info-grid" style="margin-top:16px">
    <div class="info-cell"><div class="info-label">Robustness</div><div class="info-val">{profile.robustness} &mdash; {_label(Q7_ROBUSTNESS, profile.robustness)}</div></div>
    <div class="info-cell"><div class="info-label">Cascade Scope</div><div class="info-val">{profile.cascade_scope} &mdash; {_label(Q7_CASCADE_SCOPE, profile.cascade_scope) if profile.cascade_scope else "—"}</div></div>
  </div>
</div>

<div class="footer">
  <p><strong>David Lowe &middot; POF 2828 &middot; Theophysics</strong></p>
  <p>Scored by 7Q Engine v2 &middot; {mode} mode &middot; {now}</p>
  <p style="margin-top:8px">CSS: 7q-scored-callouts.css &middot; Method: <a href="7q-explorer.html" style="color:var(--gold)">Explorer</a> &middot; <a href="7q-evidence.html" style="color:var(--ps)">Evidence</a> &middot; <a href="7q-reverse.html" style="color:var(--fail)">Reverse</a></p>
</div>

</div>
</body>
</html>'''


def write_html_report(profile: ClaimProfile, result: ScoreResult,
                      mode: str = "forward", output_dir: str = None) -> str:
    """Write the HTML report to a file. Returns the file path."""
    d = output_dir or os.path.join(os.path.dirname(os.path.abspath(__file__)), "scored_output")
    os.makedirs(d, exist_ok=True)

    safe_text = "".join(c if c.isalnum() or c in " -_" else "" for c in profile.claim_text)
    safe_text = safe_text[:60].strip().replace(" ", "_")
    filename = f"{profile.claim_id}_{safe_text}.html"
    filepath = os.path.join(d, filename)

    html = build_html_report(profile, result, mode)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  >> HTML report: {filepath}")
    return filepath


if __name__ == "__main__":
    from scorer import ClaimProfile, EvidenceItem, PredictionItem, DeathTest, compute_truth_score

    profile = ClaimProfile(
        claim_id="CL-PHY-0001",
        claim_text="Planet size and position follow predictable patterns based on orbital mechanics",
        domain="PHY", mode="INVEST", entity_type="LAW", axiom_class="DERIVED",
        status="CANONICAL", source="PEERREV", scales=["COSMIC"],
        iso_status="CONFIRMED", cross_domain_key="ISO2", domains_present=["PHY", "MTH"],
        claim_type="MATHEMATICAL", precision="PRECISE", certainty="PROVEN", scope="UNIVERSAL",
        evidence=[
            EvidenceItem(name="Kepler's laws + centuries of observation", evidence_type="EXPERIMENTAL",
                        tier="T1", strength="CONCLUSIVE", linkage="DIRECT", ps_raw=0.95, ed=0.90, ec=0.85),
            EvidenceItem(name="Exoplanet surveys (Kepler/TESS)", evidence_type="OBSERVATIONAL",
                        tier="T1", strength="STRONG", linkage="DIRECT", ps_raw=0.85, ed=0.80, ec=0.75),
        ],
        terminus="EMPIRICAL", derivation="DEDUCTIVE",
        dependency_chain=["Newtonian mechanics", "Kepler's laws", "Conservation of angular momentum"],
        predictions=[
            PredictionItem(description="Next planet position from orbital elements",
                          pred_type="CONFIRMED", competing="EXCLUSIVE", confirmed=True),
            PredictionItem(description="Exoplanet transit timing",
                          pred_type="PREDICTIVE", competing="DISCRIMIN", confirmed=False),
        ],
        death_tests=[
            DeathTest(death_type="SELFREF", result="SURVIVES"),
            DeathTest(death_type="REGRESS", result="SURVIVES"),
            DeathTest(death_type="EMPIRICAL", result="SURVIVES", notes="Centuries of observation"),
            DeathTest(death_type="INCOHERENT", result="SURVIVES"),
            DeathTest(death_type="EXPLAIN", result="SURVIVES", notes="No competing model works better"),
        ],
        robustness="SURVIVED_ADV", cascade_scope="FRAMEWORK",
    )
    result = compute_truth_score(profile)
    write_html_report(profile, result, mode="test")
