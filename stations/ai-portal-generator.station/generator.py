from __future__ import annotations

import csv
import hashlib
import html
import json
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.title_parts: list[str] = []
        self._in_title = False
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "svg"}:
            self._skip_depth += 1
        if tag == "title":
            self._in_title = True
        if tag in {"p", "div", "section", "article", "li", "br", "h1", "h2", "h3", "h4"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "svg"} and self._skip_depth:
            self._skip_depth -= 1
        if tag == "title":
            self._in_title = False
        if tag in {"p", "div", "section", "article", "li", "h1", "h2", "h3", "h4"}:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        if self._in_title:
            self.title_parts.append(data)
        self.parts.append(data)

    @property
    def text(self) -> str:
        raw = html.unescape(" ".join(self.parts))
        raw = raw.replace("\x00", " ")
        raw = re.sub(r"[ \t\r\f\v]+", " ", raw)
        raw = re.sub(r"\n\s*\n\s*", "\n\n", raw)
        return raw.strip()

    @property
    def title(self) -> str:
        return re.sub(r"\s+", " ", html.unescape(" ".join(self.title_parts))).strip()


@dataclass
class SourceDoc:
    slug: str
    file_name: str
    title: str
    text: str
    source_path: Path | None


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read_source_text(path: Path) -> tuple[str, str]:
    suffix = path.suffix.lower()
    raw = path.read_text(encoding="utf-8", errors="replace").replace("\x00", " ")
    if suffix == ".html":
        parser = TextExtractor()
        parser.feed(raw)
        title = clean_text(parser.title or path.stem.replace("_", " ").replace("-", " ").title())
        return title, clean_text(parser.text)
    if suffix == ".json":
        try:
            data = json.loads(raw)
            text = json.dumps(data, indent=2, ensure_ascii=False)
        except json.JSONDecodeError:
            text = raw
    else:
        text = raw
    title = path.stem.replace("_", " ").replace("-", " ").title()
    return clean_text(title), clean_text(text)


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"\.[a-z0-9]+$", "", value)
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "untitled"


def stable_doc_slug(path: Path, root: Path) -> str:
    rel = str(path.relative_to(root)).replace("\\", "/")
    digest = hashlib.sha1(rel.encode("utf-8")).hexdigest()[:10]
    return f"{slugify(path.stem)[:70]}-{digest}"


def clean_text(value: str) -> str:
    replacements = {
        "Ã¢â‚¬â€": "-",
        "Ã¢â‚¬â€œ": "-",
        "Ã¢â‚¬Ëœ": "'",
        "Ã¢â‚¬â„¢": "'",
        "Ã¢â‚¬Å“": '"',
        "Ã¢â‚¬Â": '"',
        "Ã‚Â·": "-",
        "Ã‚": "",
        "Ãâ€¡": "chi",
        "Ã¢Ë†Â­": "integral",
        "Ã¢Ë†â€™": "-",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    return value


def load_html_doc(path: Path) -> SourceDoc:
    parser = TextExtractor()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    title = clean_text(parser.title or path.stem.replace("-", " ").replace("_", " ").title())
    return SourceDoc(slug=slugify(path.name), file_name=path.name, title=title, text=clean_text(parser.text), source_path=path)


def split_sentences(text: str) -> list[str]:
    compact = re.sub(r"\s+", " ", text).strip()
    if not compact:
        return []
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'])", compact)
    return [p.strip() for p in parts if len(p.strip()) > 40]


def lossless_summary(text: str, max_items: int = 14) -> list[str]:
    sentences = split_sentences(text)
    priority_terms = [
        "claim", "therefore", "because", "equation", "axiom", "falsif", "predict",
        "observer", "coherence", "entropy", "quantum", "substrate", "grace", "truth",
        "measurement", "collapse", "information", "consciousness",
    ]
    scored: list[tuple[int, int, str]] = []
    for index, sentence in enumerate(sentences):
        lower = sentence.lower()
        score = sum(2 for term in priority_terms if term in lower)
        if index < 8:
            score += 4
        if len(sentence) > 220:
            score -= 1
        scored.append((score, -index, sentence))
    selected = sorted(scored, reverse=True)[:max_items]
    return [sentence for _, _, sentence in sorted(selected, key=lambda x: -x[1])]


def extract_equations(text: str) -> list[str]:
    patterns = [
        r"\$\$(.*?)\$\$",
        r"\$(.{2,180}?)\$",
        r"Ï‡\s*=.{0,220}",
        r"L(?:LC|agrangian)?\s*=.{0,220}",
        r"\b[A-Z]\s*=\s*[^.\n]{3,180}",
    ]
    equations: list[str] = []
    for pattern in patterns:
        for match in re.finditer(pattern, text, flags=re.DOTALL):
            eq = re.sub(r"\s+", " ", match.group(1) if match.groups() else match.group(0)).strip()
            if 3 <= len(eq) <= 260 and eq not in equations:
                equations.append(eq)
    return equations[:40]


def extract_claims_from_text(text: str, limit: int = 20) -> list[dict[str, str]]:
    sentences = split_sentences(text)
    markers = [
        "therefore", "we propose", "this means", "the claim", "the framework",
        "is not", "is the", "must", "requires", "predicts", "falsification",
        "kill if", "shows that", "suggests that", "demonstrates",
    ]
    claims: list[dict[str, str]] = []
    for sentence in sentences:
        lower = sentence.lower()
        if any(marker in lower for marker in markers):
            claims.append({
                "surface_claim": sentence[:900],
                "source": "text extraction",
                "review_status": "machine extracted; human reviewed corpus status applies",
            })
        if len(claims) >= limit:
            break
    return claims


def load_rows(run_dir: Path) -> list[dict[str, Any]]:
    row_files = sorted(run_dir.glob("paper_intelligence_rows_*.json"))
    return read_json(row_files[-1], []) if row_files else []


def find_report_html(run_dir: Path, file_name: str) -> Path | None:
    html_dir = run_dir / "html_reports"
    if not html_dir.exists():
        return None
    wanted = "PI_" + Path(file_name).stem
    matches = sorted(html_dir.glob(wanted + "*.html"))
    return matches[0] if matches else None


def find_snapshot(snapshot_dir: Path, slug: str) -> dict[str, Any]:
    path = snapshot_dir / f"{slug}.snapshot.json"
    return read_json(path, {})


def first_present(row: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in row and row[key] is not None:
            return row[key]
    return None


def score_block(row: dict[str, Any], fruits: dict[str, Any] | None) -> dict[str, Any]:
    block = {
        "chi_score": first_present(row, "L3_chi_score", "L10_chi_score", "L10_CHI_score", "CHI_score"),
        "truth_score": first_present(row, "L6_truth_score", "L9_truth_score", "truth_score", "PA_truth_score"),
        "coherence_score": first_present(row, "L6_coherence_score", "L8_coherence_score", "coherence_score"),
        "word_count": first_present(row, "L1_word_count", "PA_s_word_count"),
        "claim_count": first_present(row, "PA_a_claim_count", "L2_claim_marker_count"),
        "evidence_count": first_present(row, "PA_a_evidence_count", "L2_evidence_marker_count"),
        "equation_count": first_present(row, "L2_equation_count", "L3_equation_count", "equation_count"),
        "counterargument_count": first_present(row, "L2_counterargument_count", "L6_counterargument_count", "counterargument_count"),
        "readability_grade": first_present(row, "L1_flesch_kincaid_grade", "PA_r_flesch_kincaid_grade"),
        "academic_terms": first_present(row, "L2_academic_signal_count"),
        "human_review_status": "Human reviewed before publication",
        "formal_verification_status": "Partial; Lean/Colab package exists, full theorem proving not claimed",
    }
    if fruits:
        block["fruits_truth_score"] = fruits.get("truth")
        block["semantic_fruit_alignment"] = fruits.get("semantic_fruit_alignment")
        block["semantic_anti_alignment"] = fruits.get("semantic_anti_alignment")
        block["semantic_net_alignment"] = fruits.get("semantic_net_alignment")
        block["dominant_anchor"] = fruits.get("semantic_dominant_anchor")
        block["dominant_anti_anchor"] = fruits.get("semantic_dominant_anti_anchor")
    return block


def ai_page(title: str, meta: dict[str, Any], summary: list[str], links: dict[str, str], claims: list[dict[str, Any]]) -> str:
    score_items = "".join(
        f"<div><b>{html.escape(str(k).replace('_', ' ').title())}</b><span>{html.escape(str(v))}</span></div>"
        for k, v in meta.items()
        if v not in (None, "", [])
    )
    summary_items = "".join(f"<li>{html.escape(item)}</li>" for item in summary)
    claim_items = "".join(f"<li>{html.escape(str(c.get('surface_claim', c)))}</li>" for c in claims[:8])
    link_items = "".join(f"<a href=\"{html.escape(v)}\">{html.escape(k)}</a>" for k, v in links.items() if v)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} | AI Portal</title>
  <meta name="robots" content="index,follow">
  <style>
    body {{ margin:0; font-family: ui-sans-serif, system-ui, Segoe UI, Arial, sans-serif; background:#0b0f14; color:#e8edf2; line-height:1.55; }}
    main {{ max-width:1120px; margin:0 auto; padding:40px 22px 70px; }}
    a {{ color:#8bd3ff; text-decoration:none; }}
    a:hover {{ text-decoration:underline; }}
    h1 {{ font-size:34px; line-height:1.08; margin:0 0 10px; letter-spacing:0; }}
    h2 {{ margin-top:34px; font-size:20px; }}
    .meta {{ color:#aab7c4; margin-bottom:24px; }}
    .notice {{ border-left:4px solid #f1c761; background:#171714; padding:14px 16px; margin:22px 0; }}
    .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(190px,1fr)); gap:10px; }}
    .grid div {{ border:1px solid #293441; background:#121922; padding:12px; border-radius:8px; min-height:72px; }}
    .grid b {{ display:block; color:#9fb0c0; font-size:12px; text-transform:uppercase; margin-bottom:6px; }}
    .grid span {{ font-size:18px; }}
    .links {{ display:flex; flex-wrap:wrap; gap:10px; margin-top:14px; }}
    .links a {{ border:1px solid #2f4051; border-radius:999px; padding:7px 11px; background:#111923; }}
    code {{ color:#f3d17a; }}
    li {{ margin:8px 0; }}
  </style>
</head>
<body>
<main>
  <h1>{html.escape(title)}</h1>
  <p class="meta">Machine-facing companion page. This is structured for AI agents, retrieval systems, and verification workflows.</p>
  <section class="notice">
    <b>Structural audit, not a truth oracle.</b>
    This page exposes claims, scores, assumptions, objections, source links, and verification paths so another system can inspect the argument.
  </section>
  <section class="grid">{score_items}</section>
  <section>
    <h2>AI Entry Points</h2>
    <div class="links">{link_items}</div>
  </section>
  <section>
    <h2>Lossless Orientation</h2>
    <ol>{summary_items}</ol>
  </section>
  <section>
    <h2>Claim Surface</h2>
    <ol>{claim_items}</ol>
  </section>
  <section>
    <h2>Use Protocol</h2>
    <p>Read <code>paper.ai.json</code> first, then <code>claims.json</code>, then the source paper/report. Treat formal math and theorem verification as partial unless a linked Lean or Colab artifact explicitly proves the target statement.</p>
  </section>
</main>
</body>
</html>
"""


def build_gtq(config: dict[str, Any], output_dir: Path) -> list[dict[str, Any]]:
    gtq = config["gtq"]
    source_dir = Path(gtq["source_html_dir"])
    run_dir = Path(gtq["grader_run_dir"])
    snapshot_dir = Path(gtq["snapshot_dir"])
    fruits_by_name = {
        row.get("source_name"): row
        for row in read_json(Path(gtq["fruits_scores"]), [])
        if row.get("source_name")
    }
    rows = load_rows(run_dir)
    by_file = {row.get("file"): row for row in rows}
    html_files = sorted(source_dir.glob("gtq-*.html"))
    imported: list[dict[str, Any]] = []
    series_dir = output_dir / "gtq"
    for source_path in html_files:
        doc = load_html_doc(source_path)
        row = by_file.get(doc.file_name, {})
        fruits = fruits_by_name.get(doc.file_name)
        snapshot = find_snapshot(snapshot_dir, doc.slug)
        claims = snapshot.get("claims") or extract_claims_from_text(doc.text)
        equations = extract_equations(doc.text)
        summary = lossless_summary(doc.text)
        paper_dir = series_dir / doc.slug
        report_html = find_report_html(run_dir, doc.file_name)
        links = {
            "paper.ai.json": "paper.ai.json",
            "lossless summary": "summary.lossless.md",
            "claims.json": "claims.json",
            "scores.json": "scores.json",
            "vector.txt": "vector.txt",
            "public source html": str(source_path),
            "paper intelligence report": str(report_html) if report_html else "",
            "axiom snapshot": "../../axiom-snapshot.json",
            "proof explorer": "../..",
        }
        scores = score_block(row, fruits)
        ai_json = {
            "schema": "theophysics.ai_portal.paper.v1",
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "series": gtq["series_name"],
            "slug": doc.slug,
            "title": doc.title,
            "source_file": doc.file_name,
            "source_path": str(source_path),
            "human_review_status": "Human reviewed before publication",
            "machine_posture": "AI-facing structural substrate; not a truth oracle",
            "scores": scores,
            "lossless_orientation": summary,
            "claims": claims,
            "equations": equations,
            "snapshot": snapshot,
            "links": links,
        }
        write_json(paper_dir / "paper.ai.json", ai_json)
        write_json(paper_dir / "claims.json", claims)
        write_json(paper_dir / "scores.json", scores)
        write_text(paper_dir / "summary.lossless.md", "# Lossless Orientation\n\n" + "\n".join(f"{i+1}. {item}" for i, item in enumerate(summary)) + "\n")
        write_text(paper_dir / "claims.md", "# Claims\n\n" + "\n".join(f"{i+1}. {c.get('surface_claim', c)}" for i, c in enumerate(claims)) + "\n")
        vector_text = "\n\n".join([
            f"TITLE: {doc.title}",
            f"SERIES: {gtq['series_name']}",
            "SCORES: " + json.dumps(scores, ensure_ascii=False),
            "LOSSLESS ORIENTATION:\n" + "\n".join(summary),
            "CLAIMS:\n" + "\n".join(str(c.get("surface_claim", c)) for c in claims),
            "EQUATIONS:\n" + "\n".join(equations),
        ])
        write_text(paper_dir / "vector.txt", vector_text)
        write_text(paper_dir / "index.html", ai_page(doc.title, scores, summary, links, claims))
        imported.append({
            "series": gtq["series_name"],
            "slug": doc.slug,
            "title": doc.title,
            "url": f"gtq/{doc.slug}/index.html",
            "json": f"gtq/{doc.slug}/paper.ai.json",
            "word_count": scores.get("word_count"),
            "chi_score": scores.get("chi_score"),
            "truth_score": scores.get("truth_score"),
        })
    return imported


def build_yardstick(config: dict[str, Any], output_dir: Path) -> dict[str, Any] | None:
    yard = config.get("formal_yardstick", {})
    if not yard.get("enabled"):
        return None
    run_dir = Path(yard["run_dir"])
    rollup = read_json(run_dir / "formal_yardstick_rollup.json", {})
    manifest = read_json(run_dir / "formal_yardstick_manifest.json", [])
    grader_dir = run_dir / "grader"
    rows_files = sorted(grader_dir.glob("paper_intelligence_rows_*.json"))
    rows = read_json(rows_files[-1], []) if rows_files else []
    out = output_dir / "yardstick"
    write_json(out / "yardstick.ai.json", {
        "schema": "theophysics.ai_portal.yardstick.v1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "purpose": "Comparison corpus for reading Genesis to Quantum against conventional formal theories.",
        "rollup": rollup,
        "manifest": manifest,
        "paper_intelligence_rows": rows,
    })
    html_rows = "".join(
        f"<tr><td>{html.escape(str(row.get('file', row.get('source_file', ''))))}</td><td>{html.escape(str(row.get('L10_chi_score', '')))}</td><td>{html.escape(str(row.get('L9_truth_score', '')))}</td><td>{html.escape(str(row.get('L1_word_count', '')))}</td></tr>"
        for row in rows
    )
    write_text(out / "index.html", f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Formal Theory Yardstick | AI Portal</title>
<style>body{{font-family:ui-sans-serif,system-ui,Segoe UI,Arial,sans-serif;background:#0b0f14;color:#e8edf2;margin:0}}main{{max-width:1100px;margin:auto;padding:40px 22px}}a{{color:#8bd3ff}}table{{width:100%;border-collapse:collapse}}td,th{{border-bottom:1px solid #293441;padding:8px;text-align:left}}</style></head>
<body><main><h1>Formal Theory Yardstick</h1><p>Comparison corpus for AI agents evaluating Genesis to Quantum against conventional formal-theory documents.</p><p><a href="yardstick.ai.json">yardstick.ai.json</a></p><table><thead><tr><th>Document</th><th>CHI</th><th>Truth</th><th>Words</th></tr></thead><tbody>{html_rows}</tbody></table></main></body></html>""")
    return {"url": "yardstick/index.html", "json": "yardstick/yardstick.ai.json", "count": len(rows)}


def iter_library_files(root: Path, extensions: set[str], excluded_names: set[str]) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        parts = set(path.parts)
        if parts & excluded_names:
            continue
        if path.suffix.lower() in extensions:
            files.append(path)
    return sorted(files, key=lambda p: str(p).lower())


def build_library_doc(
    source_path: Path,
    source_root: Path,
    output_root: Path,
    public_root: str,
    collection: str,
) -> dict[str, Any]:
    rel = source_path.relative_to(source_root)
    slug = stable_doc_slug(source_path, source_root)
    domain = slugify(rel.parts[0]) if len(rel.parts) > 1 else "root"
    out_dir = output_root / public_root / domain / slug
    title, text = read_source_text(source_path)
    analysis_text = text[:120000]
    summary = lossless_summary(analysis_text, max_items=10)
    claims = extract_claims_from_text(analysis_text, limit=12)
    equations = extract_equations(analysis_text)
    stats = {
        "characters": len(text),
        "words": len(re.findall(r"\b[\w'-]+\b", text)),
        "sentences_estimated": len(split_sentences(analysis_text)),
        "equations_detected": len(equations),
        "claims_detected": len(claims),
        "analysis_note": "Summary/claims/equations were extracted from the first 120000 characters for bulk-import speed; content.txt preserves the full document.",
    }
    ai_json = {
        "schema": "theophysics.ai_portal.library_doc.v1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "collection": collection,
        "slug": slug,
        "title": title,
        "relative_path": str(rel).replace("\\", "/"),
        "source_path": str(source_path),
        "stats": stats,
        "lossless_orientation": summary,
        "claims": claims,
        "equations": equations,
        "files": {
            "content": "content.txt",
            "summary": "summary.lossless.md",
            "vector": "vector.txt",
        },
    }
    write_json(out_dir / "doc.ai.json", ai_json)
    write_json(out_dir / "claims.json", claims)
    write_text(out_dir / "content.txt", text)
    write_text(out_dir / "summary.lossless.md", "# Lossless Orientation\n\n" + "\n".join(f"{i+1}. {item}" for i, item in enumerate(summary)) + "\n")
    vector = "\n\n".join([
        f"TITLE: {title}",
        f"COLLECTION: {collection}",
        f"RELATIVE PATH: {str(rel).replace(chr(92), '/')}",
        "STATS: " + json.dumps(stats, ensure_ascii=False),
        "LOSSLESS ORIENTATION:\n" + "\n".join(summary),
        "CLAIMS:\n" + "\n".join(str(c.get("surface_claim", c)) for c in claims),
        "EQUATIONS:\n" + "\n".join(equations),
        "CONTENT:\n" + text,
    ])
    write_text(out_dir / "vector.txt", vector)
    write_text(out_dir / "index.html", ai_page(title, stats, summary, {
        "doc.ai.json": "doc.ai.json",
        "content.txt": "content.txt",
        "summary": "summary.lossless.md",
        "vector.txt": "vector.txt",
    }, claims))
    return {
        "collection": collection,
        "domain": domain,
        "slug": slug,
        "title": title,
        "relative_path": str(rel).replace("\\", "/"),
        "url": f"{public_root}/{domain}/{slug}/index.html",
        "json": f"{public_root}/{domain}/{slug}/doc.ai.json",
        "vector": f"{public_root}/{domain}/{slug}/vector.txt",
        **stats,
    }


def build_library_index(output_dir: Path, public_root: str, title: str, docs: list[dict[str, Any]]) -> None:
    root = output_dir / public_root
    by_domain: dict[str, int] = {}
    for doc in docs:
        by_domain[doc["domain"]] = by_domain.get(doc["domain"], 0) + 1
    write_json(root / "library.ai.json", {
        "schema": "theophysics.ai_portal.library.v1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "title": title,
        "document_count": len(docs),
        "domains": by_domain,
        "documents": docs,
    })
    domain_rows = "".join(
        f"<tr><td>{html.escape(domain)}</td><td>{count}</td></tr>"
        for domain, count in sorted(by_domain.items())
    )
    doc_rows = "".join(
        f"<tr><td><a href=\"{html.escape(doc['url'].split('/', 1)[1])}\">{html.escape(doc['title'])}</a></td><td>{html.escape(doc['domain'])}</td><td>{doc['words']}</td><td><a href=\"{html.escape(doc['json'].split('/', 1)[1])}\">JSON</a></td></tr>"
        for doc in docs[:500]
    )
    write_text(root / "index.html", f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} | AI Portal</title>
<style>body{{font-family:ui-sans-serif,system-ui,Segoe UI,Arial,sans-serif;background:#0b0f14;color:#e8edf2;margin:0;line-height:1.55}}main{{max-width:1160px;margin:auto;padding:40px 22px}}a{{color:#8bd3ff}}table{{width:100%;border-collapse:collapse;margin:16px 0}}td,th{{border-bottom:1px solid #293441;padding:8px;text-align:left}}th{{color:#aab7c4}}</style></head>
<body><main><h1>{html.escape(title)}</h1><p>{len(docs)} documents packaged for AI agents. Start with <a href="library.ai.json">library.ai.json</a>.</p><h2>Domains</h2><table><thead><tr><th>Domain</th><th>Documents</th></tr></thead><tbody>{domain_rows}</tbody></table><h2>First 500 Documents</h2><table><thead><tr><th>Document</th><th>Domain</th><th>Words</th><th>Machine File</th></tr></thead><tbody>{doc_rows}</tbody></table></main></body></html>""")


def build_verification_library(config: dict[str, Any], output_dir: Path) -> dict[str, Any] | None:
    ver = config.get("verification", {})
    if not ver.get("enabled"):
        return None
    root = Path(ver["root"])
    if not root.exists():
        return None
    extensions = {".md", ".txt", ".html", ".json", ".lean", ".ipynb", ".bat", ".ps1", ".py"}
    files = iter_library_files(root, extensions, {".git", "__pycache__", ".lake"})
    docs = [build_library_doc(path, root, output_dir, "verification", "Genesis Quantum Verification") for path in files]
    build_library_index(output_dir, "verification", "Genesis Quantum Verification", docs)
    return {"url": "verification/index.html", "json": "verification/library.ai.json", "count": len(docs)}


def build_canonical_library(config: dict[str, Any], output_dir: Path) -> dict[str, Any] | None:
    canon = config.get("canonical", {})
    if not canon.get("enabled"):
        return None
    root = Path(canon["root"])
    if not root.exists():
        return None
    extensions = set(canon.get("extensions", [".md", ".txt", ".html", ".json", ".lean"]))
    excluded = set(canon.get("exclude_dir_names", []))
    files = iter_library_files(root, extensions, excluded)
    docs = [build_library_doc(path, root, output_dir, "canonical", "Theophysics Canonical Library") for path in files]
    build_library_index(output_dir, "canonical", "Theophysics Canonical Library", docs)
    return {"url": "canonical/index.html", "json": "canonical/library.ai.json", "count": len(docs)}


def build_static_explorer_payload(config: dict[str, Any], output_dir: Path) -> None:
    proof_root = Path(config["gtq"]["proof_explorer_root"])
    pages = [
        "00_GENESIS-TO-QUANTUM-black-axiom-snapshot.html",
        "axioms-layer-0-core.html",
        "axioms-layer-2-derived.html",
        "axioms-layer-3-extended.html",
        "axioms-closure.html",
    ]
    payload = []
    for page in pages:
        path = proof_root / page
        if path.exists():
            doc = load_html_doc(path)
            payload.append({
                "file": page,
                "title": doc.title,
                "summary": lossless_summary(doc.text, max_items=8),
                "source_path": str(path),
            })
    write_json(output_dir / "axiom-snapshot.json", {
        "schema": "theophysics.ai_portal.axioms.v1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "purpose": "AI-facing orientation to the axiom and proof-explorer pages.",
        "pages": payload,
    })


def portal_index(
    title: str,
    papers: list[dict[str, Any]],
    yardstick: dict[str, Any] | None,
    verification: dict[str, Any] | None,
    canonical: dict[str, Any] | None,
) -> str:
    rows = "".join(
        f"<tr><td><a href=\"{p['url']}\">{html.escape(p['title'])}</a></td><td>{html.escape(str(p.get('chi_score', '')))}</td><td>{html.escape(str(p.get('truth_score', '')))}</td><td><a href=\"{p['json']}\">JSON</a></td></tr>"
        for p in papers
    )
    yard = f"<p><a href=\"{yardstick['url']}\">Formal Theory Yardstick</a> ({yardstick['count']} documents)</p>" if yardstick else ""
    ver = f"<p><a href=\"{verification['url']}\">Genesis Quantum Verification</a> ({verification['count']} files)</p>" if verification else ""
    canon = f"<p><a href=\"{canonical['url']}\">Canonical Library</a> ({canonical['count']} files)</p>" if canonical else ""
    return f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title>
<style>
body{{font-family:ui-sans-serif,system-ui,Segoe UI,Arial,sans-serif;background:#0b0f14;color:#e8edf2;margin:0;line-height:1.55}}
main{{max-width:1160px;margin:0 auto;padding:44px 22px 80px}}a{{color:#8bd3ff;text-decoration:none}}a:hover{{text-decoration:underline}}
.notice{{border-left:4px solid #f1c761;background:#171714;padding:14px 16px;margin:20px 0}}.links{{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0}}
.links a{{border:1px solid #2f4051;border-radius:999px;padding:7px 11px;background:#111923}}table{{width:100%;border-collapse:collapse;margin-top:18px}}
td,th{{border-bottom:1px solid #293441;padding:9px;text-align:left;vertical-align:top}}th{{color:#aab7c4;font-weight:600}}
</style></head>
<body><main>
<h1>{html.escape(title)}</h1>
<p>This portal is optimized for AI agents, retrieval systems, and verification workflows. It exposes the structure behind the public essays: claims, scores, evidence signals, axiom mapping, equations, objections, and machine-readable context.</p>
<div class="notice"><b>For AIs:</b> begin with <code>corpus.json</code> or <code>llms.txt</code>. Treat scores as structural measurements, not final truth claims.</div>
<div class="links"><a href="llms.txt">llms.txt</a><a href="corpus.json">corpus.json</a><a href="axiom-snapshot.json">axiom-snapshot.json</a><a href="sitemap.xml">sitemap.xml</a><a href="canonical/library.ai.json">canonical JSON</a></div>
{yard}{ver}{canon}
<h2>Genesis to Quantum</h2>
<table><thead><tr><th>Paper</th><th>CHI</th><th>Truth</th><th>Machine File</th></tr></thead><tbody>{rows}</tbody></table>
</main></body></html>"""


def build_llms(
    base_url: str,
    papers: list[dict[str, Any]],
    yardstick: dict[str, Any] | None,
    verification: dict[str, Any] | None,
    canonical: dict[str, Any] | None,
) -> str:
    lines = [
        "# Theophysics AI Portal",
        "",
        "This is the AI-facing substrate for the Theophysics / Genesis to Quantum corpus.",
        "",
        "Use this portal to inspect claims, scores, equations, assumptions, objections, and verification links.",
        "Do not treat scores as truth oracles. Treat them as structural measurements.",
        "",
        "Primary files:",
        f"- {base_url}/corpus.json",
        f"- {base_url}/axiom-snapshot.json",
        f"- {base_url}/sitemap.xml",
        "",
        "Genesis to Quantum papers:",
    ]
    for paper in papers:
        lines.append(f"- {paper['title']}: {base_url}/{paper['json']}")
    if yardstick:
        lines.extend(["", f"Formal yardstick: {base_url}/{yardstick['json']}"])
    if verification:
        lines.append(f"Verification library: {base_url}/{verification['json']}")
    if canonical:
        lines.append(f"Canonical library: {base_url}/{canonical['json']}")
    return "\n".join(lines) + "\n"


def build_sitemap(
    base_url: str,
    papers: list[dict[str, Any]],
    yardstick: dict[str, Any] | None,
    verification: dict[str, Any] | None,
    canonical: dict[str, Any] | None,
) -> str:
    urls = ["index.html", "corpus.json", "llms.txt", "axiom-snapshot.json"] + [p["url"] for p in papers]
    if yardstick:
        urls.append(yardstick["url"])
    if verification:
        urls.append(verification["url"])
    if canonical:
        urls.append(canonical["url"])
    items = "\n".join(f"  <url><loc>{html.escape(base_url.rstrip('/') + '/' + url)}</loc></url>" for url in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}\n</urlset>\n'


def prepare_output_dir(output_dir: Path) -> None:
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
        return
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive = output_dir.with_name(f"{output_dir.name}_previous_{stamp}")
    try:
        output_dir.rename(archive)
    except OSError:
        shutil.rmtree(output_dir, ignore_errors=True)
    output_dir.mkdir(parents=True, exist_ok=True)


def main() -> None:
    config = read_json(ROOT / "config.json", {})
    output_dir = Path(config["output_dir"])
    prepare_output_dir(output_dir)

    papers = build_gtq(config, output_dir) if config.get("gtq", {}).get("enabled") else []
    yardstick = build_yardstick(config, output_dir)
    verification = build_verification_library(config, output_dir)
    canonical = build_canonical_library(config, output_dir)
    build_static_explorer_payload(config, output_dir)

    corpus = {
        "schema": "theophysics.ai_portal.corpus.v1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "title": config["portal_title"],
        "base_url": config["portal_base_url"],
        "purpose": "AI-facing structural substrate for paper inspection, retrieval, verification, and comparison.",
        "posture": "Structural audit, not a truth oracle.",
        "papers": papers,
        "yardstick": yardstick,
        "verification": verification,
        "canonical": canonical,
        "entrypoints": {
            "llms": "llms.txt",
            "axioms": "axiom-snapshot.json",
            "sitemap": "sitemap.xml",
            "canonical": "canonical/library.ai.json",
            "verification": "verification/library.ai.json",
        },
    }
    write_json(output_dir / "corpus.json", corpus)
    write_text(output_dir / "index.html", portal_index(config["portal_title"], papers, yardstick, verification, canonical))
    write_text(output_dir / "llms.txt", build_llms(config["portal_base_url"], papers, yardstick, verification, canonical))
    write_text(output_dir / "robots.txt", "User-agent: *\nAllow: /\nSitemap: " + config["portal_base_url"].rstrip("/") + "/sitemap.xml\n")
    write_text(output_dir / "sitemap.xml", build_sitemap(config["portal_base_url"], papers, yardstick, verification, canonical))

    with (output_dir / "import_manifest.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["series", "slug", "title", "url", "json", "word_count", "chi_score", "truth_score"])
        writer.writeheader()
        writer.writerows(papers)

    print(f"Built AI portal at {output_dir}")
    print(f"Imported GTQ papers: {len(papers)}")
    print(f"Yardstick imported: {'yes' if yardstick else 'no'}")
    print(f"Verification files imported: {verification['count'] if verification else 0}")
    print(f"Canonical files imported: {canonical['count'] if canonical else 0}")


if __name__ == "__main__":
    main()

