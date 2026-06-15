#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path


DEFAULT_ROOT = Path(r"X:\WORKFLOWS\MDA-PUBLICATION")
DEFAULT_REPORT_DIR = Path(r"C:\Users\lowes\Documents\Codex\2026-05-30\okay-let-find-the-open-ai\outputs\deploy_ready_two_lane_openai_20260530")
DEFAULT_PIPELINE_ROWS = Path(r"C:\Users\lowes\Documents\Codex\2026-05-30\okay-let-find-the-open-ai\outputs\deploy_ready_full_pipeline_20260530\paper_intelligence\paper_rows.json")


def esc(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def strip_frontmatter(text: str) -> str:
    return re.sub(r"\A---\s.*?^---\s*", "", text, flags=re.S | re.M).strip()


def clean_markdown(text: str) -> str:
    text = strip_frontmatter(text)
    lines: list[str] = []
    skip_exact = {
        "Home", "Previous", "Next", "|", "Series Home", "Reader Mode", "Standard active",
        "Easy", "Plain-language bridge", "Standard", "Current article", "Academic",
        "Method + caveats", "Proof", "Proof pressure", "Audio Narration", "Coming Soon",
    }
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            lines.append("")
            continue
        if line in skip_exact:
            continue
        if "Standard is the live article" in line:
            continue
        if "Easy and Academic are reserved surfaces" in line:
            continue
        if line.startswith("source_html:") or line.startswith("deploy_relative:"):
            continue
        lines.append(raw.rstrip())
    return "\n".join(lines).strip()


def split_blocks(markdown: str) -> list[dict[str, str]]:
    blocks: list[dict[str, str]] = []
    buffer: list[str] = []

    def flush() -> None:
        nonlocal buffer
        text = "\n".join(buffer).strip()
        buffer = []
        if text:
            blocks.append({"kind": "p", "text": text})

    for line in markdown.splitlines():
        stripped = line.strip()
        if not stripped:
            flush()
            continue
        if stripped.startswith("#"):
            flush()
            level = min(3, len(stripped) - len(stripped.lstrip("#")))
            title = stripped.lstrip("#").strip()
            blocks.append({"kind": f"h{level}", "text": title})
        elif re.match(r"^[-*]\s+", stripped):
            flush()
            blocks.append({"kind": "li", "text": re.sub(r"^[-*]\s+", "", stripped)})
        else:
            buffer.append(stripped)
    flush()
    return blocks


def align_blocks(standard: list[dict[str, str]], easy: list[dict[str, str]], academic: list[dict[str, str]]) -> list[dict[str, str]]:
    total = max(len(standard), len(easy), len(academic))
    aligned: list[dict[str, str]] = []
    for idx in range(total):
        s = standard[idx] if idx < len(standard) else {"kind": "p", "text": ""}
        e = easy[idx] if idx < len(easy) else {"kind": s["kind"], "text": ""}
        a = academic[idx] if idx < len(academic) else {"kind": s["kind"], "text": ""}
        aligned.append({
            "kind": s.get("kind", "p"),
            "standard": s.get("text", ""),
            "easy": e.get("text", ""),
            "academic": a.get("text", ""),
        })
    return aligned


def render_inline(text: str) -> str:
    text = esc(text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"<a href='\2'>\1</a>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = text.replace("\n", "<br>")
    return text


def render_block(block: dict[str, str], idx: int, claim_marker: str = "") -> str:
    kind = block["kind"]
    tag = kind if kind in {"h1", "h2", "h3"} else "p"
    if kind == "li":
        tag = "p"
    easy = block.get("easy") or block.get("standard") or ""
    academic = block.get("academic") or block.get("standard") or ""
    standard = block.get("standard") or ""
    return f"""
      <section class="mda-para" data-para="{idx}">
        {claim_marker}
        <{tag} class="para-version para-easy">{render_inline(easy)}</{tag}>
        <{tag} class="para-version para-standard">{render_inline(standard)}</{tag}>
        <{tag} class="para-version para-academic">{render_inline(academic)}</{tag}>
      </section>
    """


def reading_file(reading_dir: Path, stem: str, suffix: str) -> Path | None:
    candidates = [
        reading_dir / f"{stem}_{suffix}.md",
        reading_dir / stem / f"{stem}_{suffix}.md",
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


def report_file(report_dir: Path, stem: str) -> Path | None:
    path = report_dir / f"{stem}_TWO_LANE_REPORT.md"
    return path if path.exists() else None


def load_rows(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    rows = json.loads(read_text(path))
    return {row.get("file", ""): row for row in rows}


def claim_markers(row: dict) -> list[dict[str, str]]:
    markers: list[dict[str, str]] = []
    for i in range(1, 4):
        txt = row.get(f"L2_claim_candidate_{i}") or row.get(f"L6_top_supported_{i}") or ""
        if txt:
            markers.append({
                "label": f"C{i}",
                "status": "candidate",
                "text": txt,
            })
    return markers


def proof_panel(row: dict, report: str) -> str:
    promoted = []
    for key in ("L6_top_supported_1", "L6_top_supported_2", "L2_evidence_candidate_1", "L2_evidence_candidate_2"):
        val = row.get(key)
        if val and "No promoted claim" not in val:
            promoted.append(val)
    if not promoted:
        promoted_html = "<p>No promoted claim has been deterministically passed into this proof tab yet.</p>"
    else:
        promoted_html = "".join(f"<article class='proof-card'><h3>Candidate</h3><p>{render_inline(p)}</p></article>" for p in promoted[:4])

    report_excerpt = report.strip()
    if len(report_excerpt) > 12000:
        report_excerpt = report_excerpt[:12000] + "\n\n[truncated for HTML proof panel]"

    return f"""
      <aside class="proof-panel" id="proof-panel">
        <div class="proof-head">
          <p class="eyebrow">Proof Layer</p>
          <h2>Evidence, Math Notes, and Claim Gate</h2>
        </div>
        <div class="proof-grid">
          <section>
            <h3>Promoted Claims</h3>
            {promoted_html}
          </section>
          <section>
            <h3>Paper Metrics</h3>
            <dl class="metrics">
              <div><dt>Truth</dt><dd>{esc(row.get('L6_truth_score', ''))}</dd></div>
              <div><dt>Coherence</dt><dd>{esc(row.get('L6_coherence_score', ''))}</dd></div>
              <div><dt>Chi</dt><dd>{esc(row.get('L3_chi_score', ''))}</dd></div>
              <div><dt>Argument</dt><dd>{esc(row.get('PA_a_argument_grade', ''))}</dd></div>
            </dl>
          </section>
        </div>
        <details open>
          <summary>Two-Lane Math + Attention Report</summary>
          <pre>{esc(report_excerpt or 'No two-lane report found for this article.')}</pre>
        </details>
      </aside>
    """


def page_html(stem: str, title: str, body_blocks: str, proof: str, has_easy: bool, has_academic: bool) -> str:
    status_easy = "ready" if has_easy else "fallback"
    status_academic = "ready" if has_academic else "fallback"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <style>
    :root {{
      --bg:#07080b; --panel:#10151c; --panel2:#151d27; --text:#edf2f7;
      --muted:#9aa8b6; --line:#263341; --gold:#d9b96e; --cyan:#83cfdf;
      --danger:#d68181; --ok:#8bcf96;
    }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:var(--bg); color:var(--text); font-family:ui-sans-serif,system-ui,Segoe UI,Arial,sans-serif; line-height:1.62; }}
    .reader-shell {{ min-height:100vh; }}
    .topbar {{ position:sticky; top:0; z-index:10; display:flex; flex-wrap:wrap; align-items:center; gap:10px; padding:10px 18px; background:rgba(7,8,11,.94); border-bottom:1px solid var(--line); backdrop-filter:blur(8px); }}
    .brand {{ font-weight:800; color:var(--gold); margin-right:auto; }}
    button {{ border:1px solid var(--line); background:var(--panel); color:var(--text); border-radius:6px; padding:8px 10px; cursor:pointer; }}
    button.active {{ border-color:var(--gold); background:#1f1a10; color:#ffe4a3; }}
    .status {{ font-size:12px; color:var(--muted); }}
    header {{ padding:42px clamp(20px,5vw,72px) 24px; border-bottom:1px solid var(--line); background:#090c12; }}
    .eyebrow {{ margin:0 0 8px; color:var(--gold); font-size:12px; font-weight:800; text-transform:uppercase; letter-spacing:.08em; }}
    h1 {{ margin:0; max-width:1000px; font-size:clamp(32px,5vw,62px); line-height:1.04; letter-spacing:0; }}
    .article-wrap {{ display:grid; grid-template-columns:minmax(0, 1fr); gap:24px; padding:28px clamp(18px,5vw,84px) 70px; }}
    .article {{ max-width:930px; width:100%; margin:0 auto; }}
    .mda-para {{ position:relative; padding:9px 0 13px 34px; border-bottom:1px solid rgba(255,255,255,.045); }}
    .mda-para h1,.mda-para h2,.mda-para h3 {{ line-height:1.18; margin:18px 0 8px; }}
    .mda-para p {{ margin:0; color:#d8e0e8; }}
    .para-version {{ display:none; }}
    body.mode-easy .para-easy, body.mode-standard .para-standard, body.mode-academic .para-academic {{ display:block; }}
    .claim-dot {{ position:absolute; left:0; top:14px; width:22px; height:22px; border-radius:50%; border:1px solid var(--gold); color:var(--gold); background:#12100a; font-size:11px; font-weight:800; }}
    .claim-pop {{ display:none; position:absolute; left:32px; top:42px; max-width:min(640px,80vw); padding:12px; background:var(--panel2); border:1px solid var(--line); border-radius:8px; box-shadow:0 18px 44px rgba(0,0,0,.38); color:#dbe4ec; }}
    .mda-para.show-claim .claim-pop {{ display:block; }}
    .proof-panel {{ display:none; max-width:1120px; margin:0 auto; padding:20px; background:var(--panel); border:1px solid var(--line); border-radius:8px; }}
    body.mode-proof .article {{ display:none; }}
    body.mode-proof .proof-panel {{ display:block; }}
    .proof-head h2 {{ margin:0 0 14px; }}
    .proof-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:14px; }}
    .proof-card, .proof-grid section {{ background:#0b1017; border:1px solid var(--line); border-radius:8px; padding:14px; }}
    .metrics {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:10px; margin:0; }}
    .metrics div {{ background:#0b1017; border:1px solid var(--line); border-radius:6px; padding:10px; }}
    dt {{ color:var(--muted); font-size:12px; }} dd {{ margin:2px 0 0; font-weight:800; }}
    details {{ margin-top:16px; }}
    summary {{ cursor:pointer; color:var(--gold); font-weight:800; }}
    pre {{ white-space:pre-wrap; overflow-wrap:anywhere; background:#05070a; border:1px solid #1b2633; border-radius:8px; padding:14px; color:#c6d0db; max-height:680px; overflow:auto; }}
    .fallback-note {{ color:var(--muted); margin-top:12px; }}
  </style>
</head>
<body class="mode-standard">
  <div class="reader-shell">
    <nav class="topbar" aria-label="Reader modes">
      <div class="brand">MDA Reader</div>
      <button data-mode="easy">Easy</button>
      <button data-mode="standard" class="active">Standard</button>
      <button data-mode="academic">Academic</button>
      <button data-mode="proof">Proof</button>
      <span class="status">Easy: {status_easy} | Academic: {status_academic}</span>
    </nav>
    <header>
      <p class="eyebrow">Moral Decline of America</p>
      <h1>{esc(title)}</h1>
      <p class="fallback-note">Generated from {esc(stem)} with paragraph-level Easy / Standard / Academic switching.</p>
    </header>
    <main class="article-wrap">
      <article class="article">
        {body_blocks}
      </article>
      {proof}
    </main>
  </div>
  <script>
    const buttons = Array.from(document.querySelectorAll('[data-mode]'));
    buttons.forEach(button => button.addEventListener('click', () => {{
      const mode = button.dataset.mode;
      document.body.className = 'mode-' + mode;
      buttons.forEach(b => b.classList.toggle('active', b === button));
    }}));
    document.querySelectorAll('.claim-dot').forEach(button => {{
      button.addEventListener('click', () => button.closest('.mda-para').classList.toggle('show-claim'));
    }});
  </script>
</body>
</html>
"""


def build_one(standard_path: Path, reading_dir: Path, report_dir: Path, rows: dict[str, dict], outdir: Path) -> Path:
    stem = standard_path.stem
    easy_path = reading_file(reading_dir, stem, "EASY")
    academic_path = reading_file(reading_dir, stem, "ACADEMIC")
    report_path = report_file(report_dir, stem)

    standard_text = clean_markdown(read_text(standard_path))
    easy_text = clean_markdown(read_text(easy_path)) if easy_path else standard_text
    academic_text = clean_markdown(read_text(academic_path)) if academic_path else standard_text
    report_text = read_text(report_path) if report_path else ""

    standard_blocks = split_blocks(standard_text)
    easy_blocks = split_blocks(easy_text)
    academic_blocks = split_blocks(academic_text)
    aligned = align_blocks(standard_blocks, easy_blocks, academic_blocks)

    row = rows.get(standard_path.name, {})
    markers = claim_markers(row)
    rendered: list[str] = []
    for idx, block in enumerate(aligned):
        marker_html = ""
        if idx < len(markers):
            marker = markers[idx]
            marker_html = (
                f"<button class='claim-dot' title='Claim candidate'>{esc(marker['label'])}</button>"
                f"<div class='claim-pop'><strong>{esc(marker['status'])}</strong><p>{render_inline(marker['text'])}</p></div>"
            )
        rendered.append(render_block(block, idx, marker_html))

    title = row.get("L2_title_detected") or re.sub(r"[-_]", " ", stem)
    proof = proof_panel(row, report_text)
    outdir.mkdir(parents=True, exist_ok=True)
    output = outdir / f"{stem}.html"
    output.write_text(
        page_html(stem, title, "\n".join(rendered), proof, easy_path is not None, academic_path is not None),
        encoding="utf-8",
    )
    return output


def build_index(outputs: list[Path], outdir: Path) -> None:
    links = "\n".join(f"<li><a href='{esc(path.name)}'>{esc(path.stem)}</a></li>" for path in sorted(outputs))
    index = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>MDA Reader Build</title>
<style>body{{margin:0;background:#07080b;color:#edf2f7;font-family:ui-sans-serif,system-ui,Segoe UI,Arial,sans-serif;padding:40px}}a{{color:#d9b96e}}li{{margin:8px 0}}</style>
</head><body><h1>MDA Reader Build</h1><p>Generated combined Easy / Standard / Academic / Proof HTML pages.</p><ol>{links}</ol></body></html>"""
    (outdir / "index.html").write_text(index, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Combine MDA Standard/Easy/Academic markdown plus proof data into reader HTML.")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--articles", type=Path, default=None)
    parser.add_argument("--reading-levels", type=Path, default=None)
    parser.add_argument("--reports", type=Path, default=DEFAULT_REPORT_DIR)
    parser.add_argument("--rows", type=Path, default=DEFAULT_PIPELINE_ROWS)
    parser.add_argument("--outdir", type=Path, default=None)
    parser.add_argument("--one", type=str, default="", help="Build one article stem or filename.")
    args = parser.parse_args()

    articles = args.articles or args.root / "01_LOSSLESS" / "articles"
    reading = args.reading_levels or args.root / "05_READING_LEVELS"
    outdir = args.outdir or args.root / "06_HTML_BUILD" / "reader_combined"
    rows = load_rows(args.rows)

    paths = sorted(articles.glob("*.md"))
    if args.one:
        needle = Path(args.one).stem
        paths = [p for p in paths if p.stem == needle or p.name == args.one]
    if not paths:
        raise SystemExit(f"No articles found in {articles}")

    outputs = [build_one(path, reading, args.reports, rows, outdir) for path in paths]
    build_index(outputs, outdir)
    print(json.dumps({
        "articles": len(outputs),
        "outdir": str(outdir),
        "index": str(outdir / "index.html"),
        "easy_academic_available": len(list(reading.glob("*_EASY.md"))),
    }, indent=2))


if __name__ == "__main__":
    main()
