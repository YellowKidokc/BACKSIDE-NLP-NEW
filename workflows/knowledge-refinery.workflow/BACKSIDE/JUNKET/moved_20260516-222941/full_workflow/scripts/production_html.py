"""
production_html.py
Render a Kimi-staging-shape DRAFT HTML for a paper from its scorecard + station outputs.

This is a DRAFT only. It follows _KIMI-READ-FIRST/HTML-MARKING-STANDARD.md so Kimi can
ingest, clean, and promote to K-Production-Ready/. It NEVER writes into Master HTMl/.

Output:
  <batch>/<jobid>/production-draft.html

Includes:
  PAGE_META block, paired BEGIN/END COMPONENT markers, data-component + data-name attrs,
  exec summary section, body, station-result drawers (collapsible <details>), scorecard
  table at top.

Usage:
  python production_html.py <jobid> --batch <batch-dir>
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from datetime import date
from pathlib import Path


FAP_ROOT = Path(r"X:\knowledge-refinery\13_SOURCE_SYSTEMS\FAP")
LOSSLESS_ROOT = FAP_ROOT / "lossless"
DEFAULT_BATCH = Path(r"X:\knowledge-refinery\full_workflow\output")


def slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s or "untitled"


def load_lossless(jobid: str) -> dict | None:
    p = LOSSLESS_ROOT / jobid / "lossless.article.json"
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def detect_series(jobid: str, title: str) -> str:
    for prefix in ("gtq", "mda", "cross"):
        if prefix in jobid.lower():
            return prefix
        if prefix in title.lower():
            return prefix
    return "draft"


def gather_station_outputs(batch_dir: Path, jobid: str) -> dict[str, dict]:
    stations_dir = batch_dir / jobid / "stations"
    out: dict[str, dict] = {}
    if not stations_dir.exists():
        return out
    for p in sorted(stations_dir.glob("*.result.json")):
        try:
            payload = json.loads(p.read_text(encoding="utf-8"))
            out[payload["station"]] = payload
        except Exception:
            pass
    return out


def status_class(status: str) -> str:
    return {"PASS": "ok", "REVIEW": "warn", "FAIL": "bad"}.get(status, "warn")


def render_paragraphs(lossless: dict) -> str:
    blocks = lossless.get("text_blocks") or []
    out = []
    for b in blocks:
        pid = b.get("id", "")
        tag = b.get("tag", "p")
        text = html.escape((b.get("text") or "").strip())
        if not text:
            continue
        if tag in {"h1", "h2", "h3", "h4"}:
            out.append(
                f'<{tag} id="{pid}" data-paragraph-id="{pid}">{text}</{tag}>'
            )
        else:
            out.append(
                f'<p id="{pid}" data-paragraph-id="{pid}">{text}</p>'
            )
    return "\n".join(out)


def render_scorecard_table(scorecard: dict) -> str:
    tallies = scorecard.get("station_tallies") or {}
    rows = []
    for s in scorecard.get("stations") or []:
        cls = status_class(s.get("status") or "")
        rows.append(
            f"<tr class='{cls}'><td>{html.escape(s.get('station',''))}</td>"
            f"<td>{html.escape(s.get('status') or '')}</td>"
            f"<td>{s.get('evidence_count', 0)}</td>"
            f"<td>{s.get('blocker_count', 0)}</td></tr>"
        )
    return f"""
<table class="scorecard">
  <thead><tr><th>Station</th><th>Status</th><th>Ev</th><th>Blk</th></tr></thead>
  <tbody>{''.join(rows)}</tbody>
  <tfoot>
    <tr><td colspan="4">PASS={tallies.get('PASS',0)} · REVIEW={tallies.get('REVIEW',0)} · FAIL={tallies.get('FAIL',0)}
    · Station score={scorecard.get('station_score')}
    · Grader (norm)={scorecard.get('grader_score_normalized')}
    · <strong>Combined={scorecard.get('combined_score')}</strong>
    </td></tr>
  </tfoot>
</table>
"""


def render_station_drawers(station_outputs: dict[str, dict]) -> str:
    sections = []
    for station, payload in station_outputs.items():
        result = payload.get("result") or {}
        status = result.get("status", "?")
        cls = status_class(status)
        output = html.escape(result.get("output") or "(empty)")
        ev = result.get("evidence") or []
        ev_html = (
            "<ul class='evidence'>"
            + "".join(
                f"<li><code>{html.escape(e.get('paragraph_id',''))}</code> — "
                f"{html.escape(e.get('quote',''))}</li>"
                for e in ev
            )
            + "</ul>"
        ) if ev else "<p class='muted'>(no evidence cited)</p>"
        blockers = result.get("blockers") or []
        blockers_html = (
            "<ul class='blockers'>"
            + "".join(f"<li>{html.escape(b)}</li>" for b in blockers)
            + "</ul>"
        ) if blockers else ""

        sections.append(f"""
<!-- BEGIN:COMPONENT:section:station-{station} -->
<details class="station {cls}" data-component="section" data-name="station-{station}">
  <summary><strong>{html.escape(station)}</strong> · <span class="status">{status}</span></summary>
  <div class="station-body">
    <pre class="station-output">{output}</pre>
    <h4>Evidence</h4>
    {ev_html}
    {('<h4>Blockers</h4>' + blockers_html) if blockers else ''}
  </div>
</details>
<!-- END:COMPONENT:section:station-{station} -->
""")
    return "\n".join(sections)


def render_html(jobid: str, scorecard: dict, station_outputs: dict[str, dict],
                lossless: dict | None) -> str:
    title = scorecard.get("title") or jobid
    series = detect_series(jobid, title)
    article_slug = slugify(title)
    today = date.today().isoformat()

    exec_summary_output = ""
    es = station_outputs.get("executive_summary")
    if es:
        exec_summary_output = html.escape((es.get("result") or {}).get("output") or "")

    body_paragraphs = render_paragraphs(lossless) if lossless else "<p>(lossless missing)</p>"
    scorecard_table = render_scorecard_table(scorecard)
    drawers = render_station_drawers(station_outputs)

    return f"""<!DOCTYPE html>
<!--
  PAGE_META
  series: {series}
  article: {article_slug}
  title: {title}
  version: draft-0.1
  template: full-workflow-draft-v1
  marked_by: claude-code-forge
  marked_date: {today}
  source_jobid: {jobid}
  combined_score: {scorecard.get('combined_score')}
  note: DRAFT — for Kimi promotion to K-Production-Ready/. Do not deploy as-is.
-->
<html lang="en">
<head>
  <!-- BEGIN:COMPONENT:head:head-main -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{html.escape(title)} — Draft</title>
  <meta name="generator" content="full_workflow draft renderer">
  <!-- BEGIN:COMPONENT:style:style-draft -->
  <style>
    :root {{ --ok:#1f8a3a; --warn:#b97a00; --bad:#b32626; --muted:#666; }}
    body {{ font-family: Georgia, serif; max-width: 880px; margin: 2em auto; padding: 0 1em; line-height: 1.55; color: #1a1a1a; }}
    header.draft-banner {{ background:#fff7e0; border:1px solid #d8b755; padding: .75em 1em; border-radius:6px; margin-bottom:1.5em; }}
    h1 {{ font-size: 1.9em; margin: 0 0 .4em; }}
    table.scorecard {{ border-collapse: collapse; width: 100%; margin: 1em 0; font-size: .92em; }}
    table.scorecard th, table.scorecard td {{ border: 1px solid #ddd; padding: .4em .6em; text-align: left; }}
    table.scorecard tr.ok td:nth-child(2) {{ color: var(--ok); font-weight: 600; }}
    table.scorecard tr.warn td:nth-child(2) {{ color: var(--warn); font-weight: 600; }}
    table.scorecard tr.bad td:nth-child(2) {{ color: var(--bad); font-weight: 600; }}
    details.station {{ border-left: 4px solid #ccc; padding: .5em .8em; margin: .6em 0; background: #fafafa; }}
    details.station.ok {{ border-color: var(--ok); }}
    details.station.warn {{ border-color: var(--warn); }}
    details.station.bad {{ border-color: var(--bad); }}
    details.station .station-body {{ padding-top: .5em; }}
    details.station pre.station-output {{ white-space: pre-wrap; background: #f4f4f4; padding: .5em; border-radius: 4px; font-family: ui-monospace, monospace; font-size: .88em; }}
    .muted {{ color: var(--muted); }}
    section.exec-summary {{ background: #f0f7ff; border-left: 4px solid #2266cc; padding: .75em 1em; margin: 1em 0; }}
    section.body p, section.body h2, section.body h3 {{ scroll-margin-top: 4em; }}
  </style>
  <!-- END:COMPONENT:style:style-draft -->
  <!-- END:COMPONENT:head:head-main -->
</head>
<body data-series="{series}" data-article="{article_slug}" data-status="draft">

<header class="draft-banner" data-component="callout" data-name="callout-draft-banner">
  <strong>DRAFT</strong> — auto-generated by <code>full_workflow</code> on {today}.
  Source job: <code>{jobid}</code> · Combined score: <strong>{scorecard.get('combined_score')}</strong>.
  Kimi review required before promotion to K-Production-Ready/.
</header>

<!-- BEGIN:COMPONENT:hero:hero-main -->
<section class="hero" data-component="hero" data-name="hero-main">
  <h1>{html.escape(title)}</h1>
  <p class="muted">Generated draft · {today}</p>
</section>
<!-- END:COMPONENT:hero:hero-main -->

<!-- BEGIN:COMPONENT:executive-summary:executive-summary -->
<section class="exec-summary" data-component="executive-summary" data-name="executive-summary">
  <h2>Executive summary</h2>
  <pre>{exec_summary_output or '(executive_summary station not run or empty)'}</pre>
</section>
<!-- END:COMPONENT:executive-summary:executive-summary -->

<!-- BEGIN:COMPONENT:section:scorecard -->
<section class="scorecard-section" data-component="section" data-name="scorecard">
  <h2>Scorecard</h2>
  {scorecard_table}
</section>
<!-- END:COMPONENT:section:scorecard -->

<!-- BEGIN:COMPONENT:content:content-primary -->
<section class="body" data-component="content" data-name="content-primary">
  <h2>Paper body</h2>
  {body_paragraphs}
</section>
<!-- END:COMPONENT:content:content-primary -->

<!-- BEGIN:COMPONENT:section:station-results -->
<section class="stations" data-component="section" data-name="station-results">
  <h2>Station outputs</h2>
  {drawers}
</section>
<!-- END:COMPONENT:section:station-results -->

<!-- BEGIN:COMPONENT:footer:footer-draft -->
<footer data-component="footer" data-name="footer-draft" class="muted">
  Draft · full_workflow · jobid {jobid} · marked_by claude-code-forge
</footer>
<!-- END:COMPONENT:footer:footer-draft -->

</body>
</html>
"""


def write_draft(jobid: str, batch_dir: Path) -> Path:
    paper_dir = batch_dir / jobid
    if not paper_dir.exists():
        raise FileNotFoundError(f"Paper batch dir missing: {paper_dir}")
    scorecard_path = paper_dir / "scorecard.json"
    if not scorecard_path.exists():
        raise FileNotFoundError(f"Scorecard missing: {scorecard_path}")
    scorecard = json.loads(scorecard_path.read_text(encoding="utf-8"))
    station_outputs = gather_station_outputs(batch_dir, jobid)
    lossless = load_lossless(jobid)
    html_text = render_html(jobid, scorecard, station_outputs, lossless)
    out_path = paper_dir / "production-draft.html"
    out_path.write_text(html_text, encoding="utf-8")
    return out_path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("jobid")
    ap.add_argument("--batch", default=str(DEFAULT_BATCH))
    args = ap.parse_args()
    out = write_draft(args.jobid, Path(args.batch))
    print(f"Draft HTML: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
