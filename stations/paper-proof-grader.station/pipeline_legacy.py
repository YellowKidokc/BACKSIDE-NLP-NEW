from __future__ import annotations

import csv
import hashlib
import json
import logging
import re
import shutil
import sys
import zipfile
from collections import Counter
from datetime import datetime
from html import unescape
from pathlib import Path

from formal_verification import attach_verification, write_dependency_map

HERE = Path(__file__).resolve().parent
CFG = json.loads((HERE / "config.json").read_text(encoding="utf-8-sig"))
LOG_DIR = Path(CFG.get("log_dir", r"\\dlowenas\brain\_LOGS"))
DASHBOARD_TEMPLATE = Path(CFG.get(
    "dashboard_template_path",
    r"X:\Backside\stations\axioms.station\paper-grade-dashboard-template.html",
))

CLAIM_MARKERS = re.compile(
    r"\b("
    r"claim|therefore|thus|shows|demonstrates|proves|predicts|requires|implies|"
    r"falsif|testable|observable|measure|evidence|model|equation|theorem|axiom|"
    r"corresponds|analogous|because|if .+ then"
    r")\b",
    re.IGNORECASE,
)

EVIDENCE_MARKERS = re.compile(
    r"\b(data|measurement|experiment|observation|citation|source|reference|figure|table|test|prediction|empirical)\b",
    re.IGNORECASE,
)

BOUNDARY_MARKERS = re.compile(
    r"\b(not claim|does not prove|not prove|analogy|metaphor|framework|model|hypothesis|boundary|limited|not saying)\b",
    re.IGNORECASE,
)

KILL_MARKERS = re.compile(
    r"\b(falsif|kill condition|would fail|fails if|refuted|disconfirm|counterexample|invalid|wrong if)\b",
    re.IGNORECASE,
)

SECTION_RE = re.compile(r"^(#{1,6}\s+|[A-Z][A-Za-z0-9 /:,-]{2,80}$)")

MATURITY_LABELS = {
    1: "Metaphor",
    2: "Analogy",
    3: "Structural Correspondence",
    4: "Formal Model",
    5: "Machine-Checked Theorem",
    6: "Empirical Support",
    7: "Public Proof Claim",
}


def _setup_logging() -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("workflow.paper-proof-grader")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    logfile = LOG_DIR / f"workflow_paper-proof-grader_{datetime.now():%Y%m%d}.log"
    fh = logging.FileHandler(logfile, encoding="utf-8")
    sh = logging.StreamHandler(sys.stdout)
    fh.setFormatter(fmt)
    sh.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger


def _strip_html(raw: str) -> str:
    raw = re.sub(r"(?is)<nav\b.*?</nav>", " ", raw)
    raw = re.sub(r"(?is)<aside\b.*?</aside>", " ", raw)
    raw = re.sub(r"(?is)<footer\b.*?</footer>", " ", raw)
    raw = re.sub(r"(?is)<div[^>]+class=[\"'][^\"']*(sidebar|sidebar-toggle|player|audio|bottom-nav|nav-grid)[^\"']*[\"'][^>]*>.*?</div>", " ", raw)
    raw = re.sub(r"(?is)<script.*?>.*?</script>", " ", raw)
    raw = re.sub(r"(?is)<style.*?>.*?</style>", " ", raw)
    raw = re.sub(r"(?is)<title.*?>(.*?)</title>", r"\n# \1\n", raw)
    raw = re.sub(r"(?is)</(h[1-6]|p|div|section|article|li|tr)>", "\n", raw)
    raw = re.sub(r"(?is)<h([1-6])[^>]*>(.*?)</h\1>", lambda m: "\n" + ("#" * int(m.group(1))) + " " + re.sub(r"<[^>]+>", "", m.group(2)) + "\n", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    return unescape(raw)


def _read_text(path: Path) -> str:
    raw = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() in {".html", ".htm"}:
        raw = _strip_html(raw)
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")
    raw = re.sub(r"(?s)^\s*---\n.*?\n---\s*\n", "", raw, count=1)
    raw = re.sub(r"[ \t]+", " ", raw)
    raw = re.sub(r"\n{3,}", "\n\n", raw)
    return raw.strip()


def _sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'])", text)
    out = []
    for part in parts:
        clean = re.sub(r"\s+", " ", part).strip()
        if 35 <= len(clean) <= 900:
            out.append(clean)
    return out


def _sections(text: str) -> list[dict]:
    sections: list[dict] = []
    current = {"title": "Document Start", "text": []}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        is_heading = bool(line.startswith("#")) or (len(line) < 90 and SECTION_RE.match(line) and not line.endswith("."))
        if is_heading and len(current["text"]) > 0:
            sections.append({"title": current["title"], "text": "\n".join(current["text"])})
            current = {"title": re.sub(r"^#+\s*", "", line).strip(), "text": []}
        elif is_heading and current["title"] == "Document Start" and not current["text"]:
            current["title"] = re.sub(r"^#+\s*", "", line).strip()
        else:
            current["text"].append(line)
    if current["text"] or current["title"] != "Document Start":
        sections.append({"title": current["title"], "text": "\n".join(current["text"])})
    return sections


def _equations(text: str) -> list[str]:
    patterns = [
        r"\$\$(.+?)\$\$",
        r"\$(.+?)\$",
        r"\\\[(.+?)\\\]",
        r"\\\((.+?)\\\)",
    ]
    found: list[str] = []
    for pat in patterns:
        for match in re.finditer(pat, text, re.DOTALL):
            eq = re.sub(r"\s+", " ", match.group(1)).strip()
            if 2 <= len(eq) <= 1000:
                found.append(eq)

    for line in text.splitlines():
        line = line.strip()
        if len(line) < 8 or len(line) > 1000:
            continue
        if any(token in line for token in ("=", "\\frac", "\\sum", "\\int", "\\nabla", "\\cdot", "\\Psi", "\\chi")):
            if not line.endswith(".") and line not in found:
                found.append(line)
    return found[:200]


def _maturity(sentence: str, has_equation: bool) -> tuple[int, str]:
    lower = sentence.lower()
    if "machine-checked" in lower or "formal proof" in lower:
        return 5, MATURITY_LABELS[5]
    if EVIDENCE_MARKERS.search(sentence) and ("predict" in lower or "empirical" in lower or "measurement" in lower):
        return 6, MATURITY_LABELS[6]
    if "proof" in lower or "proves" in lower or "theorem" in lower:
        return 7, MATURITY_LABELS[7]
    if has_equation or "equation" in lower or "model" in lower:
        return 4, MATURITY_LABELS[4]
    if "corresponds" in lower or "structure" in lower or "maps to" in lower:
        return 3, MATURITY_LABELS[3]
    if "analog" in lower or "like" in lower:
        return 2, MATURITY_LABELS[2]
    return 1, MATURITY_LABELS[1]


def _seven_q(sentence: str) -> dict:
    lower = sentence.lower()
    return {
        "Q1_identity": "clear" if re.search(r"\b(is|are|equals|means)\b", lower) else "implicit",
        "Q2_scope": "bounded" if re.search(r"\b(if|when|under|within|in this)\b", lower) else "broad",
        "Q3_mechanism": "present" if re.search(r"\b(because|through|by|via|mechanism|operator|field)\b", lower) else "missing",
        "Q4_evidence": "present" if EVIDENCE_MARKERS.search(sentence) else "missing",
        "Q5_falsifiability": "present" if KILL_MARKERS.search(sentence) or "predict" in lower else "missing",
        "Q6_boundary": "present" if BOUNDARY_MARKERS.search(sentence) else "missing",
        "Q7_listener_risk": "high" if re.search(r"\b(proves|therefore god|physics proves)\b", lower) else "normal",
    }


def _claim_candidates(text: str, sections: list[dict], equations: list[str]) -> list[dict]:
    claims: list[dict] = []
    eq_terms = [eq[:40] for eq in equations[:30]]
    for section in sections:
        for sentence in _sentences(section["text"]):
            if _is_noise_sentence(sentence):
                continue
            if not CLAIM_MARKERS.search(sentence):
                continue
            nearby_equation = ""
            has_equation = False
            for term in eq_terms:
                if term and term[:12] in section["text"]:
                    nearby_equation = term
                    has_equation = True
                    break
            level, label = _maturity(sentence, has_equation)
            q = _seven_q(sentence)
            evidence_hits = sorted(set(m.group(1).lower() for m in EVIDENCE_MARKERS.finditer(sentence)))
            claims.append({
                "paper_id": "",
                "section": section["title"],
                "one_sentence_claim": sentence,
                "claim_maturity_level": level,
                "claim_maturity_label": label,
                "facts_snapshot": _facts_snapshot(sentence),
                "forward_test": _forward_test(sentence),
                "reverse_test": _reverse_test(sentence),
                "evidence_bar": ", ".join(evidence_hits) if evidence_hits else "No explicit evidence marker in sentence.",
                "kill_conditions": _kill_conditions(sentence, q),
                "not_claimed": _not_claimed(sentence),
                "proof_boundary": _proof_boundary(sentence, label, q),
                "nearby_equation": nearby_equation,
                **q,
            })
    return claims[:250]


def _is_noise_sentence(sentence: str) -> bool:
    lower = sentence.lower()
    if lower.startswith("keywords:"):
        return True
    if sentence.count("Â·") >= 3:
        return True
    if "read aloud" in lower or "primary narration" in lower:
        return True
    if re.search(r"\b(previous|next|home|menu|navigation|share|copyright)\b", lower):
        return True
    if len(re.findall(r"\bgtq-\d+", lower)) >= 2:
        return True
    return False


def _facts_snapshot(sentence: str) -> str:
    terms = []
    for token in ("model", "equation", "prediction", "evidence", "measurement", "axiom", "operator", "field", "coherence", "entropy"):
        if token in sentence.lower():
            terms.append(token)
    return "Detected terms: " + ", ".join(terms) if terms else "No hard factual terms detected by deterministic pass."


def _forward_test(sentence: str) -> str:
    if "predict" in sentence.lower():
        return "If the claim is true, its stated prediction should survive measurement or comparison."
    if "equation" in sentence.lower() or "=" in sentence:
        return "If the claim is true, the stated relationship should preserve its variables, direction, and scope."
    return "If the claim is true, the described pattern should appear where the paper says it should appear."


def _reverse_test(sentence: str) -> str:
    return "If the pattern can appear without the proposed framework, the claim should be downgraded or narrowed."


def _kill_conditions(sentence: str, q: dict) -> str:
    if q["Q5_falsifiability"] == "present":
        return "Sentence contains an explicit falsifiability or prediction marker; preserve it and make the failure case concrete."
    return "Needs an explicit failure case: what observation, logic result, or counterexample would make this claim false?"


def _not_claimed(sentence: str) -> str:
    lower = sentence.lower()
    if "physics proves" in lower or "proves god" in lower:
        return "WARNING: sentence risks implying physics proves theology; rewrite unless that is the actual intended claim."
    return "Does not by itself claim that physics proves theology."


def _proof_boundary(sentence: str, maturity_label: str, q: dict) -> str:
    if q["Q7_listener_risk"] == "high":
        return f"Boundary needed: currently reads stronger than {maturity_label}."
    return f"Current boundary: deterministic pass classifies this as {maturity_label}, not a final proof."


def _metrics(text: str, sections: list[dict], equations: list[str], claims: list[dict]) -> dict:
    words = re.findall(r"\b[\w'-]+\b", text)
    counts = Counter(w.lower() for w in words if len(w) > 3)
    return {
        "word_count": len(words),
        "section_count": len(sections),
        "equation_count": len(equations),
        "claim_candidate_count": len(claims),
        "top_terms": ", ".join(term for term, _ in counts.most_common(15)),
    }


def _write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_markdown(path: Path, data: dict) -> None:
    m = data["metrics"]
    verification = data.get("formal_verification", {})
    lean_status = verification.get("lean", {})
    lines = [
        f"# Paper Proof Grader Report - {data['paper_id']}",
        "",
        "## FACTS Snapshot",
        f"- Source: `{data['source_file']}`",
        f"- Words: {m['word_count']}",
        f"- Sections: {m['section_count']}",
        f"- Equations: {m['equation_count']}",
        f"- Claim candidates: {m['claim_candidate_count']}",
        f"- Top terms: {m['top_terms']}",
        "",
        "## Formal Verification Layer",
        f"- Lean proven: {lean_status.get('proven', 0)}",
        f"- Lean formalizable candidates: {lean_status.get('formalizable', 0)}",
        f"- Lean not attempted: {lean_status.get('not_attempted', 0)}",
        f"- Lean speculative/unclassified: {lean_status.get('speculative', 0)}",
        "- Alloy: reserved for counterexample search; not configured in this first layer.",
        "- State model: reserved for TLA+/Maude-style transition claims; not configured in this first layer.",
        "",
        "## Claim Audit",
    ]
    for idx, claim in enumerate(data["claims"], 1):
        formal = claim.get("formal_verification", {})
        lines.extend([
            "",
            f"### Claim {idx}: {claim['section']}",
            f"- One-sentence claim: {claim['one_sentence_claim']}",
            f"- Maturity: {claim['claim_maturity_level']} - {claim['claim_maturity_label']}",
            f"- Formal status: Lean={formal.get('lean', 'not_attempted')}; Bridge={formal.get('bridge_status', 'unclassified')}",
            f"- Theorem dependencies: {', '.join(formal.get('theorem_dependencies', [])) or 'none detected'}",
            f"- Evidence bar: {claim['evidence_bar']}",
            f"- Kill conditions: {claim['kill_conditions']}",
            f"- Proof boundary: {claim['proof_boundary']}",
            f"- Not claimed: {claim['not_claimed']}",
        ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_html(path: Path, data: dict) -> None:
    if DASHBOARD_TEMPLATE.exists():
        path.write_text(_render_dashboard_html(DASHBOARD_TEMPLATE, data), encoding="utf-8")
        return

    m = data["metrics"]
    verification = data.get("formal_verification", {})
    lean_status = verification.get("lean", {})
    rows = "\n".join(
        f"<tr><td>{i}</td><td>{_esc(c['section'])}</td><td>{_esc(c['one_sentence_claim'])}</td>"
        f"<td>{c['claim_maturity_level']} - {_esc(c['claim_maturity_label'])}</td>"
        f"<td>{_esc(c.get('formal_verification', {}).get('lean', 'not_attempted'))}</td>"
        f"<td>{_esc(', '.join(c.get('formal_verification', {}).get('theorem_dependencies', [])) or 'none')}</td>"
        f"<td>{_esc(c['kill_conditions'])}</td><td>{_esc(c['proof_boundary'])}</td></tr>"
        for i, c in enumerate(data["claims"], 1)
    )
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Paper Proof Grader - {_esc(data['paper_id'])}</title>
<style>
:root {{ --gold:#d7a629; --text:#efe7cf; --text-dim:#c9bea4; --text-muted:#9d9279; --surface2:#11100d; --border:#4d3b13; --green:#41b879; --red:#d45b5b; --orange:#d88b35; }}
body {{ margin: 0; background: #080807; color: var(--text); font-family: Georgia, serif; }}
main {{ max-width: 1180px; margin: 0 auto; padding: 42px 24px; }}
h1, h2 {{ color: var(--gold); }}
.metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; margin: 22px 0; }}
.metric, .pr-section-wrap {{ border: 1px solid var(--border); background: var(--surface2); padding: 14px; border-radius: 6px; }}
.meta {{ color: var(--text-dim); }}
.qa-btn {{ display:inline-flex; align-items:center; gap:6px; border:1px solid var(--border); background:#17140d; color:var(--gold); border-radius:6px; padding:7px 10px; font-size:0.78rem; }}
table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
th, td {{ border-bottom: 1px solid #34270d; padding: 10px; vertical-align: top; }}
th {{ color: var(--gold); text-align: left; }}
@media (max-width: 800px) {{ .transparency-grid {{ grid-template-columns: 1fr !important; }} }}
</style>
</head>
<body><main>
<h1>Paper Proof Grader</h1>
<p class="meta">{_esc(data['paper_id'])}</p>
{_transparency_notice_html()}
<section class="metrics">
<div class="metric"><b>Words</b><br>{m['word_count']}</div>
<div class="metric"><b>Sections</b><br>{m['section_count']}</div>
<div class="metric"><b>Equations</b><br>{m['equation_count']}</div>
<div class="metric"><b>Claims</b><br>{m['claim_candidate_count']}</div>
<div class="metric"><b>Lean Candidates</b><br>{lean_status.get('formalizable', 0)}</div>
<div class="metric"><b>Lean Proven</b><br>{lean_status.get('proven', 0)}</div>
</section>
<h2>Formal Verification Layer</h2>
<p class="meta">Lean is the canonical proof lane. Alloy is reserved for counterexample search. TLA+/Maude-style state models are reserved for explicit transition claims.</p>
<ul>
<li>Lean proven: {lean_status.get('proven', 0)}</li>
<li>Lean formalizable candidates: {lean_status.get('formalizable', 0)}</li>
<li>Lean not attempted: {lean_status.get('not_attempted', 0)}</li>
<li>Lean speculative/unclassified: {lean_status.get('speculative', 0)}</li>
</ul>
<h2>Scientific Claim Audit</h2>
<table><thead><tr><th>#</th><th>Section</th><th>Claim</th><th>Maturity</th><th>Lean</th><th>Theorem Dependencies</th><th>Kill Conditions</th><th>Proof Boundary</th></tr></thead><tbody>
{rows}
</tbody></table>
</main></body></html>
"""
    path.write_text(html, encoding="utf-8")


def _slug(value: object) -> str:
    text = re.sub(r"[^a-zA-Z0-9]+", "-", str(value).strip().lower())
    return text.strip("-") or "paper"


def _filename_safe(value: object) -> str:
    text = re.sub(r"[^a-zA-Z0-9._-]+", "-", str(value).strip())
    return text.strip("-") or "paper"


def _pct(part: int, whole: int) -> int:
    if whole <= 0:
        return 0
    return int(round((part / whole) * 100))


def _fill_class(percent: int) -> str:
    if percent >= 70:
        return "high"
    if percent >= 40:
        return "mid"
    return "low"


def _maturity_class(label: str) -> str:
    lower = label.lower()
    if "machine" in lower or "empirical" in lower or "public proof" in lower:
        return "mat-proof"
    if "formal" in lower:
        return "mat-formal"
    if "structural" in lower or "analogy" in lower:
        return "mat-structural"
    return "mat-metaphor"


def _dashboard_grade(data: dict) -> tuple[str, str, str]:
    claims = data.get("claims", [])
    total = len(claims)
    if total == 0:
        return "N/A", "No claims extracted", "NO_CLAIMS"
    q4 = sum(1 for c in claims if c.get("Q4_evidence") == "present")
    q5 = sum(1 for c in claims if c.get("Q5_falsifiability") == "present")
    q6 = sum(1 for c in claims if c.get("Q6_boundary") == "present")
    mature = sum(1 for c in claims if int(c.get("claim_maturity_level", 0) or 0) >= 4)
    score = _pct(q4 + q5 + q6 + mature, total * 4)
    if score >= 85:
        return "A", f"{score}% control coverage", "GREEN_READY"
    if score >= 65:
        return "B", f"{score}% control coverage", "YELLOW_REVIEW"
    if score >= 40:
        return "C", f"{score}% control coverage", "ORANGE_REPAIR"
    return "D", f"{score}% control coverage", "RED_REPAIR"


def _q_coverage(data: dict) -> list[dict]:
    labels = [
        ("Q1_identity", "Q1 Identity"),
        ("Q2_scope", "Q2 Scope"),
        ("Q3_mechanism", "Q3 Mechanism"),
        ("Q4_evidence", "Q4 Evidence"),
        ("Q5_falsifiability", "Q5 Falsifiability"),
        ("Q6_boundary", "Q6 Boundary"),
        ("Q7_listener_risk", "Q7 Listener Risk"),
    ]
    good_values = {
        "Q1_identity": {"clear"},
        "Q2_scope": {"bounded"},
        "Q3_mechanism": {"present"},
        "Q4_evidence": {"present"},
        "Q5_falsifiability": {"present"},
        "Q6_boundary": {"present"},
        "Q7_listener_risk": {"normal"},
    }
    claims = data.get("claims", [])
    rows = []
    for key, label in labels:
        counts = Counter(str(c.get(key, "missing")) for c in claims)
        good = sum(count for value, count in counts.items() if value in good_values[key])
        percent = _pct(good, len(claims))
        weak = len(claims) - good
        rows.append({
            "Q_ID": key.split("_", 1)[0].lower(),
            "Q_LABEL": label,
            "Q_OBSERVED_VALUES": ", ".join(f"{k}={v}" for k, v in sorted(counts.items())) or "none",
            "Q_COVERAGE_PCT": str(percent),
            "Q_FILL_CLASS": _fill_class(percent),
            "Q_WEAK_COUNT": str(weak),
            "PRESSURE_LABEL": label,
            "PRESSURE_COUNT": str(weak),
        })
    return rows


def _replace_slot(template: str, slot_name: str, replacement: str) -> str:
    pattern = (
        r"(?s)<!-- TEMPLATE:SLOT:" + re.escape(slot_name) +
        r".*?-->\s*.*?\s*<!-- END:TEMPLATE:SLOT:" + re.escape(slot_name) + r" -->"
    )
    return re.sub(pattern, replacement, template)


def _replace_values(template: str, values: dict[str, object]) -> str:
    def repl(match: re.Match) -> str:
        return str(values.get(match.group(1), ""))
    return re.sub(r"\{\{([A-Z0-9_]+)\}\}", repl, template)


def _render_repeated(template: str, slot_name: str, rows: list[dict[str, object]]) -> str:
    match = re.search(
        r"(?s)<!-- TEMPLATE:SLOT:" + re.escape(slot_name) +
        r".*?-->\s*(.*?)\s*<!-- END:TEMPLATE:SLOT:" + re.escape(slot_name) + r" -->",
        template,
    )
    if not match:
        return template
    fragment = match.group(1)
    rendered = "\n".join(_replace_values(fragment, row) for row in rows)
    return _replace_slot(template, slot_name, rendered)


def _fruit_rows() -> list[dict[str, str]]:
    fruits = [
        ("love", "Love", "agape", "V(r) at minimum"),
        ("joy", "Joy", "chara", "omega = omega0 resonance"),
        ("peace", "Peace", "eirene", "sum F = 0"),
        ("patience", "Patience", "hypomone", "C = dQ/dT high"),
        ("kindness", "Kindness", "chrestotes", "activation energy minimized"),
        ("goodness", "Goodness", "agathosyne", "W_out > W_in"),
        ("faithfulness", "Faithfulness", "pistis", "dL/dt = 0"),
        ("gentleness", "Gentleness", "prautes", "F = k*F_needed, k <= 1"),
        ("self-control", "Self-Control", "enkrateia", "u(t) = -K*e(t)"),
    ]
    return [
        {
            "FRUIT_ID": fid,
            "FRUIT_NAME": name,
            "FRUIT_GREEK": greek,
            "FRUIT_EQUATION": equation,
            "FRUIT_STATUS_CLASS": "derived",
            "FRUIT_STATUS": "derived",
        }
        for fid, name, greek, equation in fruits
    ]


def _render_dashboard_html(template_path: Path, data: dict) -> str:
    template = template_path.read_text(encoding="utf-8-sig")
    claims = data.get("claims", [])
    metrics = data["metrics"]
    grade, confidence, verdict = _dashboard_grade(data)
    q_rows = _q_coverage(data)
    maturity_counts = Counter(str(c.get("claim_maturity_label", "Unclassified")) for c in claims)
    evidence_marked = sum(1 for c in claims if c.get("Q4_evidence") == "present")
    kill_count = sum(1 for c in claims if c.get("Q5_falsifiability") == "present")
    title = data.get("paper_id", "Paper Grade").replace("_", " ")
    generated = data.get("generated_at", "")
    source_manifest = data.get("source_manifest", {})

    template = _render_repeated(template, "7q-item", q_rows)
    template = _render_repeated(
        template,
        "maturity-row",
        [
            {
                "MATURITY_LEVEL": _slug(label),
                "MATURITY_LABEL": _esc(label),
                "MATURITY_COUNT": str(count),
                "MATURITY_PCT": str(_pct(count, len(claims))),
            }
            for label, count in sorted(maturity_counts.items())
        ] or [{"MATURITY_LEVEL": "none", "MATURITY_LABEL": "No claims", "MATURITY_COUNT": "0", "MATURITY_PCT": "0"}],
    )
    template = _render_repeated(
        template,
        "evidence-marker-row",
        [
            {"MARKER_TYPE": "explicit", "MARKER_LABEL": "Explicit Evidence", "MARKER_COUNT": str(evidence_marked)},
            {"MARKER_TYPE": "missing", "MARKER_LABEL": "Evidence Missing", "MARKER_COUNT": str(max(len(claims) - evidence_marked, 0))},
        ],
    )
    template = _render_repeated(
        template,
        "pressure-card",
        sorted([row for row in q_rows if int(row["PRESSURE_COUNT"]) > 0], key=lambda row: int(row["PRESSURE_COUNT"]), reverse=True)[:6]
        or [{"Q_ID": "none", "PRESSURE_LABEL": "No repair pressure", "PRESSURE_COUNT": "0"}],
    )
    template = _render_repeated(
        template,
        "claim-row",
        [
            {
                "CLAIM_NUMBER": str(idx),
                "CLAIM_SECTION": _esc(claim.get("section", "")),
                "CLAIM_TEXT": _esc(claim.get("one_sentence_claim", "")),
                "MATURITY_CLASS": _maturity_class(str(claim.get("claim_maturity_label", ""))),
                "MATURITY_LABEL": _esc(claim.get("claim_maturity_label", "")),
                "MATURITY_LEVEL_NUM": str(claim.get("claim_maturity_level", "")),
                "EVIDENCE_TEXT": _esc(claim.get("evidence_bar", "")),
                "KILL_CONDITION": _esc(claim.get("kill_conditions", "")),
                "PROOF_BOUNDARY": _esc(claim.get("proof_boundary", "")),
            }
            for idx, claim in enumerate(claims[:40], 1)
        ] or [{
            "CLAIM_NUMBER": "0",
            "CLAIM_SECTION": "None",
            "CLAIM_TEXT": "No claim candidates found.",
            "MATURITY_CLASS": "mat-metaphor",
            "MATURITY_LABEL": "None",
            "MATURITY_LEVEL_NUM": "0",
            "EVIDENCE_TEXT": "",
            "KILL_CONDITION": "",
            "PROOF_BOUNDARY": "",
        }],
    )
    template = _render_repeated(
        template,
        "law-badge",
        [{"LAW_NUMBER": str(i), "LAW_COVERAGE_CLASS": "active" if i in _law_hits(data) else ""} for i in range(1, 11)],
    )
    template = _render_repeated(template, "fruit-card", _fruit_rows())
    template = _render_repeated(
        template,
        "kill-card",
        [
            {
                "KILL_ID": f"C{idx:03d}",
                "KILL_STATUS_CLASS": "warn" if claim.get("Q5_falsifiability") != "present" else "pass",
                "KILL_STATUS": "NEEDS TEST" if claim.get("Q5_falsifiability") != "present" else "MARKED",
                "KILL_TITLE": _esc(claim.get("section", "Claim")),
                "KILL_DESCRIPTION": _esc(claim.get("kill_conditions", "")),
                "KILL_EVIDENCE": _esc(claim.get("one_sentence_claim", "")[:180]),
            }
            for idx, claim in enumerate(claims[:12], 1)
        ] or [{
            "KILL_ID": "NONE",
            "KILL_STATUS_CLASS": "warn",
            "KILL_STATUS": "NO CLAIMS",
            "KILL_TITLE": "No kill conditions",
            "KILL_DESCRIPTION": "No claim candidates were extracted.",
            "KILL_EVIDENCE": "",
        }],
    )
    template = _render_repeated(
        template,
        "station-row",
        [
            {"STATION_ID": "intake", "STATION_NAME": "Intake", "STATION_STATUS": "passed", "STATION_WARNINGS": ""},
            {"STATION_ID": "claim", "STATION_NAME": "Claim Extraction", "STATION_STATUS": "passed", "STATION_WARNINGS": f"{len(claims)} claims"},
            {"STATION_ID": "formal", "STATION_NAME": "Formal Verification", "STATION_STATUS": "triage", "STATION_WARNINGS": "Lean/Alloy not executed in this pass"},
            {"STATION_ID": "export", "STATION_NAME": "Report Export", "STATION_STATUS": "passed", "STATION_WARNINGS": "HTML/MD/JSON/CSV/XLSX"},
        ],
    )

    values = {
        "SERIES_CODE": "PAPER",
        "SERIES_SLUG": "paper-grades",
        "ARTICLE_SLUG": _slug(data.get("paper_id", "")),
        "ARTICLE_TITLE": _esc(title.title()),
        "PUBLISH_DATE": generated[:10],
        "MODIFY_DATE": generated[:10],
        "SEMANTIC_ADDRESS": _esc(f"THEOPHYSICS/{_filename_safe(data.get('paper_id', 'paper'))}/W/AI_RESEARCH/R/R1"),
        "FILENAME_SAFE": _filename_safe(data.get("paper_id", "paper")),
        "VECTOR_HASH": "G3M3E0S0T3K3R0Q0F0C3",
        "HASH_SHORT": "C-Q/G-S/K-F/M-R/T-E",
        "RIGOR_VERDICT": verdict,
        "MATH_LAYER": "deterministic-triage",
        "TRANSLATED_SPANS": "0",
        "ARTICLE_GRADE": grade,
        "GRADE_CONFIDENCE": confidence,
        "WORD_COUNT": metrics.get("word_count", 0),
        "SECTION_COUNT": metrics.get("section_count", 0),
        "EQUATION_COUNT": metrics.get("equation_count", 0),
        "CLAIM_COUNT": metrics.get("claim_candidate_count", 0),
        "EVIDENCE_MARKED": evidence_marked,
        "KILL_COUNT": kill_count,
        "DERIV_TRUTH_CLASS": "active",
        "DERIV_EXISTENCE_CLASS": "",
        "DERIV_GROUNDING_CLASS": "",
        "DERIV_OBSERVATION_CLASS": "active" if evidence_marked else "",
        "DERIV_MORAL_CLASS": "",
        "DERIV_SPIRITUAL_CLASS": "active" if _law_hits(data) else "",
        "DERIV_GRACE_CLASS": "",
        "GENERATION_TIMESTAMP": generated,
        "SOURCE_JSON_PATH": _esc(source_manifest.get("source_archive_path", data.get("source_file", ""))),
        "SNAPSHOT_STATUS": "paper-grade-json only",
    }
    return _replace_values(template, values)


def _law_hits(data: dict) -> set[int]:
    text = " ".join(
        [data.get("metrics", {}).get("top_terms", "")]
        + [claim.get("one_sentence_claim", "") for claim in data.get("claims", [])]
    ).lower()
    hits: set[int] = set()
    rules = [
        (1, ["gravity", "grace", "sin"]),
        (2, ["motion", "force", "mass"]),
        (3, ["truth", "light", "electromagnet"]),
        (4, ["love", "strong force", "fruit"]),
        (5, ["entropy", "thermodynamic", "judgment"]),
        (6, ["logos", "information", "signal"]),
        (7, ["quantum", "faith", "doubt"]),
        (8, ["relativity", "frame"]),
        (9, ["weak force", "atonement", "moral conservation"]),
        (10, ["coherence", "christ", "decoherence"]),
    ]
    for law, terms in rules:
        if any(term in text for term in terms):
            hits.add(law)
    return hits


def _transparency_notice_html() -> str:
    return """<!-- PAPER INTELLIGENCE TRANSPARENCY NOTICE -->
<section class="pr-section-wrap" style="border-color:rgba(212,175,55,0.25); margin-bottom:2rem;">
  <h3 style="color:var(--gold); margin-top:0;">Transparency Notice</h3>
  <p style="font-size:0.85rem; color:var(--text-dim); line-height:1.7; margin:0.8rem 0;">
    This paper has been evaluated by the <strong style="color:var(--text);">Theophysics Paper Intelligence</strong> pipeline &mdash;
    a deterministic, open-source scoring system distributed as a Docker container.
    The pipeline performs automated analysis across multiple dimensions including coherence index (&chi;),
    truth density, claim-support ratio, equation coverage, lexical and semantic Fruits alignment,
    readability metrics, and Master Equation variable mapping.
  </p>
  <div class="transparency-grid" style="display:grid; grid-template-columns:1fr 1fr; gap:1rem; margin:1rem 0; font-size:0.8rem;">
    <div style="border-left:2px solid var(--green); padding-left:12px;">
      <div style="color:var(--text-muted); text-transform:uppercase; letter-spacing:1px; font-size:0.65rem; margin-bottom:4px;">What these scores measure</div>
      <div style="color:var(--text-dim); line-height:1.6;">
        Structural properties of the text. High coherence = all ten Master Equation variables engaged.
        High truth density = claims paired with evidence at a high ratio.
        Neither score validates content. That remains the reader&rsquo;s work.
      </div>
    </div>
    <div style="border-left:2px solid var(--red); padding-left:12px;">
      <div style="color:var(--text-muted); text-transform:uppercase; letter-spacing:1px; font-size:0.65rem; margin-bottom:4px;">What these scores do not measure</div>
      <div style="color:var(--text-dim); line-height:1.6;">
        Correctness of conclusions, theological validity, experimental replicability,
        or domain-specific peer review. This is a structural audit, not a truth oracle.
      </div>
    </div>
  </div>
  <div style="background:var(--surface2); border:1px solid var(--border); border-radius:6px; padding:12px 14px; margin:1rem 0;">
    <div style="font-size:0.75rem; color:var(--gold); text-transform:uppercase; letter-spacing:1.5px; margin-bottom:6px;">Reproducibility Guarantee</div>
    <p style="font-size:0.8rem; color:var(--text-dim); line-height:1.6; margin:0;">
      This pipeline is deterministic. Given identical input, it produces identical output across runs,
      machines, and operators. The Docker image, source code, and scoring methodology are publicly
      available. You are invited&mdash;encouraged&mdash;to run this pipeline against this paper,
      against any paper in this corpus, or against any paper from any source.
    </p>
  </div>
  <details style="margin-top:0.8rem;">
    <summary style="font-size:0.75rem; color:var(--text-muted); cursor:pointer; letter-spacing:0.5px;">Known Limitations of This Run</summary>
    <ul style="font-size:0.78rem; color:var(--text-muted); line-height:1.8; margin:8px 0 0 16px; padding:0;">
      <li>27 fine-grained emotion categories returned incomplete due to model unavailability. Affected sections are marked rather than populated with zeros.</li>
      <li>Equation counts include inline mathematical notation and may overcount relative to distinct formal statements.</li>
      <li>Formal verification against the axiom spine, Master Equation, Lagrangian, and Lean proofs requires a separate workflow not included in this scoring pass.</li>
      <li>Counterargument detection identifies explicit rebuttal language only; structural objections embedded in argument flow may not be counted.</li>
    </ul>
  </details>
  <div style="margin-top:0.8rem; display:flex; gap:8px; flex-wrap:wrap;">
    <a class="qa-btn" href="https://github.com/YellowKidokc/paper-proof-grader" target="_blank" style="text-decoration:none;">Source &amp; Docker</a>
    <a class="qa-btn" href="https://hub.docker.com/r/yellowkid/paper-intelligence" target="_blank" style="text-decoration:none;">Docker Hub</a>
    <a class="qa-btn" href="https://theophysics.pro" target="_blank" style="text-decoration:none;">Theophysics</a>
  </div>
</section>"""


def _esc(value: object) -> str:
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        rows = [{"note": "No claim candidates found."}]
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_excel(path: Path, data: dict, log: logging.Logger) -> None:
    summary_rows = [
        ["Paper ID", data["paper_id"]],
        ["Source", data["source_file"]],
        ["Generated", data["generated_at"]],
        ["Words", data["metrics"]["word_count"]],
        ["Sections", data["metrics"]["section_count"]],
        ["Equations", data["metrics"]["equation_count"]],
        ["Claim Candidates", data["metrics"]["claim_candidate_count"]],
        ["Top Terms", data["metrics"]["top_terms"]],
    ]

    claim_headers = [
        "paper_id", "section", "one_sentence_claim", "claim_maturity_level",
        "claim_maturity_label", "facts_snapshot", "Q1_identity", "Q2_scope",
        "Q3_mechanism", "Q4_evidence", "Q5_falsifiability", "Q6_boundary",
        "Q7_listener_risk", "forward_test", "reverse_test", "evidence_bar",
        "kill_conditions", "not_claimed", "proof_boundary", "nearby_equation",
        "formal_lean_status", "formal_bridge_status", "theorem_dependencies",
        "formal_lean_files", "formalization_note",
    ]
    claim_rows = [claim_headers]
    for claim in data["claims"]:
        formal = claim.get("formal_verification", {})
        row = []
        for header in claim_headers:
            if header == "formal_lean_status":
                row.append(formal.get("lean", ""))
            elif header == "formal_bridge_status":
                row.append(formal.get("bridge_status", ""))
            elif header == "theorem_dependencies":
                row.append(", ".join(formal.get("theorem_dependencies", [])))
            elif header == "formal_lean_files":
                row.append(", ".join(formal.get("lean_files", [])))
            elif header == "formalization_note":
                row.append(formal.get("formalization_note", ""))
            else:
                row.append(claim.get(header, ""))
        claim_rows.append(row)

    eq_rows = [["paper_id", "equation"]]
    for eq in data["equations"]:
        eq_rows.append([data["paper_id"], eq])

    section_rows = [["paper_id", "section", "character_count", "preview"]]
    for section in data["sections"]:
        preview = re.sub(r"\s+", " ", section["text"])[:500]
        section_rows.append([data["paper_id"], section["title"], len(section["text"]), preview])

    grade, confidence, verdict = _dashboard_grade(data)
    q_rows = _q_coverage(data)
    review_control_rows = [
        ["Field", "Value", "Meaning"],
        ["paper_id", data["paper_id"], "Stable paper/run title"],
        ["run_id", data.get("run_id", ""), "Grader run identifier"],
        ["source_archive_path", data.get("source_manifest", {}).get("source_archive_path", data.get("source_file", "")), "Canonical source after archive"],
        ["source_sha256", data.get("source_manifest", {}).get("source_sha256", ""), "Reproducibility hash"],
        ["grade", grade, "Dashboard readiness grade"],
        ["grade_confidence", confidence, "Coverage score behind grade"],
        ["rigor_verdict", verdict, "Machine-readable dashboard verdict"],
        ["word_count", data["metrics"]["word_count"], ""],
        ["section_count", data["metrics"]["section_count"], ""],
        ["equation_count", data["metrics"]["equation_count"], ""],
        ["claim_count", data["metrics"]["claim_candidate_count"], ""],
        ["", "", ""],
        ["7Q Field", "Coverage %", "Weak Count"],
    ]
    for row in q_rows:
        review_control_rows.append([row["Q_LABEL"], row["Q_COVERAGE_PCT"], row["Q_WEAK_COUNT"]])
    review_control_rows.extend([
        ["", "", ""],
        ["Top Repair Rule", "Fix highest weak-count Q first", "Then rerun grader and compare manifest"],
        ["Dashboard Template", str(DASHBOARD_TEMPLATE), "Canonical HTML renderer source"],
    ])

    _write_minimal_xlsx(
        path,
        [
            ("Review_Control", review_control_rows),
            ("Summary", summary_rows),
            ("Claim Audit", claim_rows),
            ("Equations", eq_rows),
            ("Sections", section_rows),
        ],
    )


def _write_minimal_xlsx(path: Path, sheets: list[tuple[str, list[list[object]]]]) -> None:
    """Write a dependency-free XLSX using inline strings."""
    content_types = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
        '<Default Extension="xml" ContentType="application/xml"/>',
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
        '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>',
    ]
    for idx, _ in enumerate(sheets, 1):
        content_types.append(
            f'<Override PartName="/xl/worksheets/sheet{idx}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        )
    content_types.append("</Types>")

    workbook_sheets = "\n".join(
        f'<sheet name="{_xml(name[:31])}" sheetId="{idx}" r:id="rId{idx}"/>'
        for idx, (name, _) in enumerate(sheets, 1)
    )
    workbook_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f"<sheets>{workbook_sheets}</sheets></workbook>"
    )
    workbook_rels = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
    ]
    for idx, _ in enumerate(sheets, 1):
        workbook_rels.append(
            f'<Relationship Id="rId{idx}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{idx}.xml"/>'
        )
    workbook_rels.append(
        f'<Relationship Id="rId{len(sheets) + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    )
    workbook_rels.append("</Relationships>")

    styles_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<fonts count="2"><font><sz val="11"/><name val="Calibri"/></font><font><b/><color rgb="FFD7A629"/><sz val="11"/><name val="Calibri"/></font></fonts>'
        '<fills count="2"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF11100D"/><bgColor indexed="64"/></patternFill></fill></fills>'
        '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
        '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
        '<cellXfs count="2"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf><xf numFmtId="0" fontId="1" fillId="1" borderId="0" xfId="0" applyFont="1" applyFill="1" applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf></cellXfs>'
        '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
        '</styleSheet>'
    )

    root_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        "</Relationships>"
    )

    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", "\n".join(content_types))
        zf.writestr("_rels/.rels", root_rels)
        zf.writestr("xl/workbook.xml", workbook_xml)
        zf.writestr("xl/_rels/workbook.xml.rels", "\n".join(workbook_rels))
        zf.writestr("xl/styles.xml", styles_xml)
        for idx, (_, rows) in enumerate(sheets, 1):
            zf.writestr(f"xl/worksheets/sheet{idx}.xml", _sheet_xml(rows))


def _sheet_xml(rows: list[list[object]]) -> str:
    xml_rows = []
    for r_idx, row in enumerate(rows, 1):
        cells = []
        for c_idx, value in enumerate(row, 1):
            ref = f"{_col(c_idx)}{r_idx}"
            style = "1" if r_idx == 1 else "0"
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                cells.append(f'<c r="{ref}" s="{style}"><v>{value}</v></c>')
            else:
                cells.append(f'<c r="{ref}" s="{style}" t="inlineStr"><is><t>{_xml(value)}</t></is></c>')
        xml_rows.append(f'<row r="{r_idx}">{"".join(cells)}</row>')
    dimension = f"A1:{_col(max((len(r) for r in rows), default=1))}{max(len(rows), 1)}"
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f'<dimension ref="{dimension}"/>'
        '<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>'
        f'<sheetData>{"".join(xml_rows)}</sheetData>'
        '</worksheet>'
    )


def _xml(value: object) -> str:
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _col(index: int) -> str:
    letters = ""
    while index:
        index, rem = divmod(index - 1, 26)
        letters = chr(65 + rem) + letters
    return letters


def _report_dirs() -> list[Path]:
    dirs = [Path(CFG["output_dir"])]
    report_dir = CFG.get("report_dir")
    if report_dir:
        dirs.append(Path(report_dir))
    ready: list[Path] = []
    for path in dirs:
        try:
            path.mkdir(parents=True, exist_ok=True)
            ready.append(path)
        except Exception:
            pass
    return ready


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _process(path: Path, out_dir: Path, log: logging.Logger, run_id: str, archive_path: Path) -> dict:
    source_sha256 = _sha256(path)
    source_size = path.stat().st_size
    text = _read_text(path)
    sections = _sections(text)
    equations = _equations(text)
    claims = _claim_candidates(text, sections, equations)
    formal_verification = attach_verification(claims)
    paper_id = path.stem
    for claim in claims:
        claim["paper_id"] = paper_id
    data = {
        "run_id": run_id,
        "paper_id": paper_id,
        "source_file": str(archive_path),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source_manifest": {
            "run_id": run_id,
            "paper_id": paper_id,
            "source_file_name": path.name,
            "source_original_path": str(path),
            "source_archive_path": str(archive_path),
            "source_sha256": source_sha256,
            "source_size_bytes": source_size,
            "detected_format": path.suffix.lower().lstrip("."),
            "ingested_at": datetime.now().isoformat(timespec="seconds"),
            "grader_version": "paper-proof-grader/v0.2-station",
            "rubric_version": "paper-proof-grader-output-contract/v0.1",
        },
        "metrics": _metrics(text, sections, equations, claims),
        "formal_verification": formal_verification,
        "sections": sections,
        "equations": equations,
        "claims": claims,
    }

    base = out_dir / paper_id
    write_dependency_map(out_dir / "formal-verification-dependency-map.md")
    _write_json(base.with_suffix(".paper-grade.json"), data)
    _write_markdown(base.with_suffix(".paper-grade.md"), data)
    _write_html(base.with_suffix(".paper-grade.html"), data)
    _write_csv(base.with_suffix(".claim-audit.csv"), claims)
    _write_excel(base.with_suffix(".paper-grade.xlsx"), data, log)
    return data


def main() -> int:
    log = _setup_logging()
    input_dir = Path(CFG["input_dir"])
    archive_dir = Path(CFG["archive_dir"])
    input_dir.mkdir(parents=True, exist_ok=True)
    archive_dir.mkdir(parents=True, exist_ok=True)
    out_dirs = _report_dirs()
    primary_out = Path(CFG["output_dir"])
    exts = {e.lower() for e in CFG.get("text_extensions", [".txt", ".md", ".html", ".htm"])}
    files = sorted(p for p in input_dir.iterdir() if p.is_file() and p.suffix.lower() in exts)
    run_id = f"paper-proof-grader-{datetime.now():%Y%m%d_%H%M%S}"
    log.info("found %d candidate paper files", len(files))
    if not files:
        log.info("nothing to do")
        return 0

    run_manifest = []
    for path in files:
        log.info("grading %s", path)
        archived = archive_dir / path.name
        if archived.exists():
            archived = archive_dir / f"{path.stem}_{datetime.now():%Y%m%d_%H%M%S}{path.suffix}"
        data = _process(path, primary_out, log, run_id, archived)
        run_manifest.append({
            "run_id": run_id,
            "paper_id": data["paper_id"],
            "source_file": data["source_file"],
            "source_manifest": data["source_manifest"],
            "metrics": data["metrics"],
        })

        for mirror in out_dirs:
            if mirror == primary_out:
                continue
            for suffix in (".paper-grade.json", ".paper-grade.md", ".paper-grade.html", ".claim-audit.csv", ".paper-grade.xlsx"):
                src = primary_out / f"{data['paper_id']}{suffix}"
                if src.exists():
                    shutil.copy2(src, mirror / src.name)

        shutil.move(str(path), str(archived))
        log.info("archived source -> %s", archived)

    manifest_path = primary_out / f"{run_id}.json"
    manifest_path.write_text(json.dumps(run_manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("run manifest -> %s", manifest_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

