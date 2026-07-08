from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from html import escape
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def esc(value: Any) -> str:
    return escape(str(value if value is not None else ""), quote=True)


def pct(value: int, total: int) -> str:
    return "0%" if total <= 0 else f"{round(100 * value / total, 1)}%"


def issue_counts(claims: list[dict[str, Any]]) -> Counter:
    out: Counter = Counter()
    for claim in claims:
        if claim.get("Q3_mechanism") == "missing":
            out["missing mechanism"] += 1
        if claim.get("Q4_evidence") == "missing":
            out["missing evidence"] += 1
        if claim.get("Q5_falsifiability") == "missing":
            out["missing falsifiability"] += 1
        if claim.get("Q6_boundary") == "missing":
            out["missing boundary"] += 1
        if claim.get("Q2_scope") == "broad":
            out["broad scope"] += 1
        if claim.get("Q7_listener_risk") == "high":
            out["listener risk"] += 1
    return out


def semantic_lookup(manifest_path: Path | None) -> dict[str, dict[str, Any]]:
    if not manifest_path or not manifest_path.exists():
        return {}
    manifest = load_json(manifest_path)
    rows = {}
    for row in manifest.get("rows") or []:
        rows[str(Path(row["source"]).resolve()).lower()] = row
        rows[Path(row["source"]).name.lower()] = row
    return rows


def grade_rows(grade_dir: Path, semantic_rows: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(grade_dir.glob("*.paper-grade.json")):
        data = load_json(path)
        metrics = data.get("metrics") or {}
        claims = data.get("claims") or []
        issues = issue_counts(claims)
        semantic = semantic_rows.get(str(path.resolve()).lower()) or semantic_rows.get(path.name.lower()) or {}
        rows.append(
            {
                "paper_id": data.get("paper_id") or path.name.replace(".paper-grade.json", ""),
                "path": path,
                "json": path,
                "xlsx": path.with_suffix("").with_suffix(".paper-grade.xlsx"),
                "html": path.with_suffix("").with_suffix(".paper-grade.html"),
                "dashboard": path.with_suffix("").with_suffix(".paper-grade-dashboard.html"),
                "words": metrics.get("word_count", 0),
                "sections": metrics.get("section_count", 0),
                "equations": metrics.get("equation_count", 0),
                "claims": metrics.get("claim_candidate_count", len(claims)),
                "issues": issues,
                "weak_total": sum(issues.values()),
                "vector": semantic.get("vector", ""),
                "hash": semantic.get("hash", ""),
                "address": semantic.get("address", ""),
                "filename_safe": semantic.get("filename_safe", ""),
            }
        )
    return rows


def link(path: Path, label: str) -> str:
    if not path.exists():
        return f"<span class='missing'>{esc(label)}</span>"
    return f"<a href='{esc(path.as_uri())}'>{esc(label)}</a>"


def build_html(rows: list[dict[str, Any]], manifest_path: Path | None, out_path: Path) -> str:
    totals = {
        "papers": len(rows),
        "words": sum(int(r["words"] or 0) for r in rows),
        "sections": sum(int(r["sections"] or 0) for r in rows),
        "equations": sum(int(r["equations"] or 0) for r in rows),
        "claims": sum(int(r["claims"] or 0) for r in rows),
    }
    vectors = Counter(r["vector"] or "NO_VECTOR" for r in rows)
    domains = Counter((r["filename_safe"].split("__")[0] if r["filename_safe"] else "NO_ADDRESS") for r in rows)
    addressed = sum(1 for r in rows if r["filename_safe"])
    dashboards = sum(1 for r in rows if r["dashboard"].exists())

    vector_rows = "\n".join(f"<tr><td>{esc(v)}</td><td>{c}</td><td>{pct(c, len(rows))}</td></tr>" for v, c in vectors.most_common(12))
    domain_rows = "\n".join(f"<tr><td>{esc(d)}</td><td>{c}</td></tr>" for d, c in domains.most_common())
    table_rows = "\n".join(
        "<tr>"
        f"<td><b>{esc(r['paper_id'])}</b><span>{esc(r['hash'])}</span></td>"
        f"<td>{esc(r['vector'] or 'missing')}</td>"
        f"<td>{esc(r['words'])}</td>"
        f"<td>{esc(r['claims'])}</td>"
        f"<td>{esc(r['equations'])}</td>"
        f"<td>{esc(r['weak_total'])}<span>{esc(', '.join(f'{k}: {v}' for k, v in r['issues'].most_common(3)))}</span></td>"
        f"<td>{link(r['html'], 'grade html')} {link(r['xlsx'], 'xlsx')} {link(r['dashboard'], 'dashboard')}</td>"
        "</tr>"
        for r in rows
    )
    generated = datetime.now().isoformat(timespec="seconds")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paper Grade Corpus Dashboard</title>
<style>
:root {{
  --bg:#10130d;
  --panel:#f8efd2;
  --panel2:#efe0ae;
  --ink:#17140d;
  --muted:#766a4c;
  --gold:#d7a629;
  --green:#3b7d50;
  --red:#a64732;
  --line:rgba(23,20,13,.16);
}}
body {{
  margin:0;
  background:
    linear-gradient(120deg, rgba(16,19,13,.94), rgba(43,35,13,.82)),
    radial-gradient(circle at top right, rgba(215,166,41,.45), transparent 34rem);
  color:var(--ink);
  font-family:"Aptos", "Segoe UI", sans-serif;
}}
main {{ max-width:1360px; margin:0 auto; padding:38px 22px 80px; }}
.hero,.panel {{
  background:linear-gradient(180deg, rgba(255,249,229,.96), rgba(239,224,174,.96));
  border:1px solid rgba(215,166,41,.35);
  border-radius:26px;
  box-shadow:0 24px 80px rgba(0,0,0,.25);
}}
.hero {{ padding:30px; }}
.eyebrow {{ color:#87610d; letter-spacing:.17em; text-transform:uppercase; font-size:.75rem; font-weight:900; }}
h1 {{ font-family:"Iowan Old Style","Palatino Linotype",Georgia,serif; font-size:clamp(2.2rem,4.8vw,5.4rem); line-height:.9; margin:.4rem 0; }}
.sub {{ max-width:920px; color:var(--muted); line-height:1.62; }}
.grid {{ display:grid; gap:16px; }}
.metrics {{ grid-template-columns:repeat(5,minmax(0,1fr)); margin:22px 0 0; }}
.metric {{ background:rgba(255,255,255,.36); border:1px solid var(--line); border-radius:18px; padding:16px; }}
.metric strong {{ display:block; font-size:2rem; }}
.metric span {{ color:var(--muted); text-transform:uppercase; letter-spacing:.09em; font-size:.73rem; }}
.two {{ grid-template-columns:.75fr 1.25fr; margin-top:16px; align-items:start; }}
.panel {{ padding:20px; overflow:hidden; }}
h2 {{ font-family:"Iowan Old Style","Palatino Linotype",Georgia,serif; margin:.2rem 0 1rem; }}
table {{ width:100%; border-collapse:collapse; font-size:.9rem; }}
th,td {{ border-bottom:1px solid var(--line); padding:10px 9px; vertical-align:top; text-align:left; }}
th {{ color:#87610d; text-transform:uppercase; letter-spacing:.09em; font-size:.68rem; }}
td span {{ display:block; margin-top:.28rem; color:var(--muted); font-size:.78rem; line-height:1.42; }}
a {{ color:#1d5d79; font-weight:800; margin-right:.55rem; }}
.missing {{ color:var(--red); font-weight:800; margin-right:.55rem; }}
.status {{ color:var(--muted); font-size:.82rem; line-height:1.55; overflow-wrap:anywhere; }}
@media (max-width:960px) {{ .metrics,.two {{ grid-template-columns:1fr; }} }}
</style>
</head>
<body>
<main>
  <section class="hero">
    <div class="eyebrow">Axioms Workflow / Paper-Grader Corpus</div>
    <h1>Paper Grade Corpus Dashboard</h1>
    <p class="sub">This is the review index for deterministic paper-grade outputs. It joins grader metrics to the semantic address canary so we can see whether the Master Equation filename/address layer works across the paper set before promoting anything into canon routing.</p>
    <section class="grid metrics">
      <div class="metric"><strong>{totals['papers']}</strong><span>Papers</span></div>
      <div class="metric"><strong>{totals['words']:,}</strong><span>Words</span></div>
      <div class="metric"><strong>{totals['sections']:,}</strong><span>Sections</span></div>
      <div class="metric"><strong>{totals['equations']:,}</strong><span>Equations</span></div>
      <div class="metric"><strong>{totals['claims']:,}</strong><span>Claims</span></div>
    </section>
  </section>

  <section class="grid two">
    <div class="panel">
      <h2>Address Pass</h2>
      <p class="status">Addressed: <b>{addressed}/{len(rows)}</b>. Individual dashboards present: <b>{dashboards}/{len(rows)}</b>. Semantic manifest: {esc(manifest_path or 'not loaded')}.</p>
      <table><thead><tr><th>Domain</th><th>Count</th></tr></thead><tbody>{domain_rows}</tbody></table>
    </div>
    <div class="panel">
      <h2>Vector Distribution</h2>
      <table><thead><tr><th>Vector</th><th>Count</th><th>Share</th></tr></thead><tbody>{vector_rows}</tbody></table>
    </div>
  </section>

  <section class="panel" style="margin-top:16px;">
    <h2>Paper Rows</h2>
    <table><thead><tr><th>Paper</th><th>Vector</th><th>Words</th><th>Claims</th><th>Equations</th><th>Repair Pressure</th><th>Artifacts</th></tr></thead><tbody>{table_rows}</tbody></table>
  </section>

  <p class="status" style="color:#e9dcae; margin-top:18px;">Generated {esc(generated)} at {esc(out_path)}.</p>
</main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a corpus-level dashboard for paper-grade outputs.")
    parser.add_argument("--grade-dir", type=Path, default=Path(__file__).resolve().parents[1] / "01_OUTBOX_REPORTS")
    parser.add_argument("--semantic-manifest", type=Path)
    parser.add_argument("--out-html", type=Path)
    args = parser.parse_args()

    semantic_rows = semantic_lookup(args.semantic_manifest)
    rows = grade_rows(args.grade_dir, semantic_rows)
    out_html = args.out_html or args.grade_dir / "paper-grade-corpus-dashboard.html"
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(build_html(rows, args.semantic_manifest, out_html), encoding="utf-8")
    print(json.dumps(
        {
            "ok": True,
            "paper_count": len(rows),
            "addressed_count": sum(1 for r in rows if r["filename_safe"]),
            "dashboard_html": str(out_html),
        },
        indent=2,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
