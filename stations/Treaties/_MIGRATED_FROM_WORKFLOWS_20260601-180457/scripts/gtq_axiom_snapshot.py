from __future__ import annotations

import argparse
import html
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path
from statistics import mean


CATEGORIES = (
    "problem",
    "method",
    "variables",
    "mechanism",
    "evidence",
    "limitations",
    "implications",
)

AXIOMS = [
    {
        "id": "AX-LOGOS-01",
        "name": "Logos coherence",
        "category": "metaphysics",
        "description": "Reality is intelligible where information, order, and meaning remain coherent across levels.",
        "keywords": ("logos", "coherence", "meaning", "order", "information", "word"),
    },
    {
        "id": "AX-BOUNDARY-02",
        "name": "Boundary makes relation measurable",
        "category": "method",
        "description": "A claim becomes analyzable when it states the boundary between domains, observers, or states.",
        "keywords": ("boundary", "observer", "frame", "domain", "interface", "threshold"),
    },
    {
        "id": "AX-COLLAPSE-03",
        "name": "Measurement changes state",
        "category": "mechanism",
        "description": "Observation, choice, or measurement constrains possible states into an actual state.",
        "keywords": ("measurement", "collapse", "observe", "choice", "state", "actual"),
    },
    {
        "id": "AX-CONSERVATION-04",
        "name": "Conservation constrains transformation",
        "category": "physics",
        "description": "Physical and symbolic transformations need an accounting rule for what is preserved or spent.",
        "keywords": ("conservation", "energy", "entropy", "thermodynamic", "law", "symmetry"),
    },
    {
        "id": "AX-FALSIFY-05",
        "name": "Falsifiability is required",
        "category": "epistemology",
        "description": "A serious claim names what would wound, weaken, or defeat it.",
        "keywords": ("falsify", "refute", "kill condition", "prediction", "test", "contradict"),
    },
    {
        "id": "AX-TRACE-06",
        "name": "Claims require traceable evidence",
        "category": "evidence",
        "description": "Every important claim should connect to a source, observation, derivation, or explicit argument.",
        "keywords": ("evidence", "source", "quote", "support", "derive", "proof", "argument"),
    },
    {
        "id": "AX-REPRO-07",
        "name": "Reproducibility strengthens knowledge",
        "category": "method",
        "description": "A result is stronger when another reader can repeat the method or audit the chain.",
        "keywords": ("reproduce", "replicate", "method", "steps", "dataset", "repository", "audit"),
    },
    {
        "id": "AX-VARIABLE-08",
        "name": "Variables must be operationalized",
        "category": "method",
        "description": "A variable should be named, bounded, and made observable before it bears weight.",
        "keywords": ("variable", "parameter", "operator", "constant", "metric", "measure"),
    },
]


@dataclass
class ModelItem:
    category: str
    claim: str
    source_quote: str
    confidence: float
    uncertainty_note: str


@dataclass
class AxiomMapping:
    axiom_id: str
    axiom_name: str
    category: str
    interpretation: str
    source_quote: str
    confidence: float


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.title_parts: list[str] = []
        self.skip_depth = 0
        self.in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "svg", "canvas", "noscript"}:
            self.skip_depth += 1
        if tag == "title":
            self.in_title = True
        if tag in {"p", "div", "section", "article", "li", "tr", "h1", "h2", "h3", "h4", "br"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "svg", "canvas", "noscript"} and self.skip_depth:
            self.skip_depth -= 1
        if tag == "title":
            self.in_title = False
        if tag in {"p", "div", "section", "article", "li", "tr", "h1", "h2", "h3", "h4"}:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        if self.in_title:
            self.title_parts.append(data)
        self.parts.append(data)


def normalize_text(raw: str) -> str:
    raw = re.sub(r"[A-Za-z0-9+/]{120,}={0,2}", " ", raw)
    raw = re.sub(r"\r\n?", "\n", raw)
    raw = re.sub(r"[ \t]+", " ", raw)
    raw = re.sub(r"\n{3,}", "\n\n", raw)
    return raw.strip()


def extract_text(path: Path) -> tuple[str, str]:
    parser = TextExtractor()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    title = normalize_text(" ".join(parser.title_parts)) or path.stem
    text = normalize_text("".join(parser.parts))
    return title, text


def paragraphs(text: str) -> list[str]:
    candidates = [normalize_text(p) for p in re.split(r"\n+|(?<=[.!?])\s{2,}", text)]
    return [p for p in candidates if 80 <= len(p) <= 900 and len(p.split()) >= 12]


def sentence_split(text: str) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if 50 <= len(s.strip()) <= 420]


def contains_any(value: str, words: tuple[str, ...]) -> bool:
    lower = value.lower()
    return any(word in lower for word in words)


def best_quote(pool: list[str], keywords: tuple[str, ...]) -> str:
    scored: list[tuple[int, int, str]] = []
    for paragraph in pool:
        lower = paragraph.lower()
        score = sum(lower.count(k) for k in keywords)
        if score:
            scored.append((score, -len(paragraph), paragraph))
    if not scored:
        return ""
    quote = sorted(scored, reverse=True)[0][2]
    return quote[:520].strip()


def claim_from_quote(category: str, quote: str) -> str:
    defaults = {
        "problem": "The work frames Genesis-to-Quantum as a cross-domain coherence problem.",
        "method": "The work uses layered conceptual mapping rather than a conventional experimental protocol.",
        "variables": "The work treats observers, information, entropy, coherence, state, and boundary as central variables.",
        "mechanism": "The work proposes that measurement, boundary, and information changes mediate collapse or transformation.",
        "evidence": "The work supports claims through argument structure, citations, analogies, and internal derivations.",
        "limitations": "The work needs explicit kill conditions, reproducible tests, and clearer separation between metaphor and mechanism.",
        "implications": "The work aims to connect theological meaning, physics language, and formal axiom structure.",
    }
    if not quote:
        return defaults[category]
    first = sentence_split(quote)
    if first:
        return first[0]
    return defaults[category]


def extract_model_items(paras: list[str]) -> list[ModelItem]:
    keywords = {
        "problem": ("problem", "question", "paradox", "gap", "collapse", "meaning", "origin"),
        "method": ("method", "model", "framework", "map", "derive", "layer", "formal"),
        "variables": ("variable", "observer", "entropy", "information", "state", "energy", "coherence", "boundary"),
        "mechanism": ("mechanism", "because", "therefore", "causal", "collapse", "transform", "coupling"),
        "evidence": ("evidence", "proof", "support", "experiment", "observation", "citation", "data"),
        "limitations": ("limit", "limitation", "cannot", "uncertain", "speculative", "test", "falsify"),
        "implications": ("imply", "therefore", "consequence", "prediction", "means", "suggests"),
    }
    items: list[ModelItem] = []
    for category in CATEGORIES:
        quote = best_quote(paras, keywords[category])
        confidence = 0.72 if quote else 0.35
        note = "Heuristic extraction from the HTML snapshot; ready for LLM review." if quote else "Not strongly explicit in the extracted text."
        items.append(ModelItem(category, claim_from_quote(category, quote), quote, confidence, note))
    return items


def score_signals(text: str) -> dict[str, bool | str]:
    lower = text.lower()
    signals: dict[str, bool | str] = {
        "sample_size_mentioned": bool(re.search(r"\b(n\s*=|sample size|participants|subjects)\b", lower)),
        "variables_defined": contains_any(lower, ("variable", "parameter", "operator", "metric", "measure")),
        "method_clear": contains_any(lower, ("method", "framework", "model", "procedure", "derivation")),
        "controls_present": contains_any(lower, ("control", "baseline", "comparison", "counterfactual")),
        "limitations_discussed": contains_any(lower, ("limitation", "uncertain", "speculative", "cannot", "falsify")),
        "data_available": contains_any(lower, ("dataset", "repository", "supplement", "github", "appendix")),
        "reproducible_steps": contains_any(lower, ("step", "procedure", "algorithm", "derivation", "audit")),
        "funding_or_conflicts_mentioned": contains_any(lower, ("funding", "conflict of interest", "competing interest")),
        "statistical_results_present": bool(re.search(r"\bp\s*[<=>]|confidence interval|regression|correlation|statistical\b", lower)),
        "direct_evidence_present": contains_any(lower, ("observation", "experiment", "measured", "simulation", "case study")),
    }
    signals["notes"] = (
        "Scores are computed from explicit textual signals in the exported HTML. "
        "This is a first-pass NLP-style grade, not a final peer-review judgment."
    )
    return signals


def component_scores(signals: dict[str, bool | str]) -> dict[str, int]:
    try:
        from app.schemas import ScoringSignals
        from app.services.scoring import _component_scores, _overall

        typed_signals = ScoringSignals(
            sample_size_mentioned=bool(signals["sample_size_mentioned"]),
            variables_defined=bool(signals["variables_defined"]),
            method_clear=bool(signals["method_clear"]),
            controls_present=bool(signals["controls_present"]),
            limitations_discussed=bool(signals["limitations_discussed"]),
            data_available=bool(signals["data_available"]),
            reproducible_steps=bool(signals["reproducible_steps"]),
            funding_or_conflicts_mentioned=bool(signals["funding_or_conflicts_mentioned"]),
            statistical_results_present=bool(signals["statistical_results_present"]),
            direct_evidence_present=bool(signals["direct_evidence_present"]),
            notes=str(signals["notes"]),
        )
        components = _component_scores(typed_signals)
        components["overall_score"] = _overall(components)
        components["engine"] = "Treaties app.services.scoring"
        return components
    except Exception as exc:
        rigor = (
            25 * int(bool(signals["variables_defined"]))
            + 25 * int(bool(signals["method_clear"]))
            + 25 * int(bool(signals["controls_present"]))
            + 25 * int(bool(signals["sample_size_mentioned"]))
        )
        evidence = (
            40 * int(bool(signals["direct_evidence_present"]))
            + 30 * int(bool(signals["statistical_results_present"]))
            + 30 * int(bool(signals["controls_present"]))
        )
        reproducibility = (
            50 * int(bool(signals["reproducible_steps"]))
            + 30 * int(bool(signals["data_available"]))
            + 20 * int(bool(signals["method_clear"]))
        )
        clarity = (
            50 * int(bool(signals["method_clear"]))
            + 30 * int(bool(signals["variables_defined"]))
            + 20 * int(bool(signals["limitations_discussed"]))
        )
        bias_risk = (
            40 * int(not bool(signals["limitations_discussed"]))
            + 40 * int(not bool(signals["funding_or_conflicts_mentioned"]))
            + 20 * int(not bool(signals["direct_evidence_present"]))
        )
        overall = round(
            rigor * 0.30
            + evidence * 0.30
            + reproducibility * 0.20
            + clarity * 0.10
            + (100 - bias_risk) * 0.10
        )
        return {
            "methodological_rigor": min(100, rigor),
            "evidence_strength": min(100, evidence),
            "reproducibility": min(100, reproducibility),
            "clarity": min(100, clarity),
            "bias_risk": min(100, bias_risk),
            "overall_score": overall,
            "engine": f"local fallback scoring ({type(exc).__name__}: {exc})",
        }


def run_nlp_stack(text: str, paras: list[str]) -> dict:
    labels = [
        "theophysics",
        "formal proof",
        "scientific paper",
        "research",
        "theology",
        "physics",
        "axiom mapping",
        "speculative synthesis",
    ]
    chunks = paras[:12] or [text[:2000]]
    try:
        sys.path.insert(0, str(Path(r"X:\models")))
        import nlp_layer

        model_root = Path(r"X:\models")
        nlp_layer.BRAIN = model_root
        nlp_layer.MODEL_PATHS.update(
            {
                "deberta": model_root / "deberta_nli",
                "sbert": model_root / "sbert_minilm",
                "bart": model_root / "bart_summarizer",
                "whisper": model_root / "whisper_large_v3",
                "mistral": model_root / "mistral_7b",
            }
        )
        analyses = [
            nlp_layer.analyze(chunk, labels=labels, run_sentiment=False, run_summary=False)
            for chunk in chunks[:5]
        ]
        top_scores = [float(a.get("top_score", 0.0)) for a in analyses]
        label_counts = Counter(str(a.get("top_label", "unknown")) for a in analyses)
        return {
            "engine": "X:\\models\\nlp_layer.py",
            "status": "ok",
            "labels": labels,
            "chunks_analyzed": len(analyses),
            "top_labels": dict(label_counts.most_common()),
            "mean_top_score": round(mean(top_scores), 3) if top_scores else 0.0,
            "sample": analyses[:3],
        }
    except Exception as exc:
        return lexical_nlp_fallback(text, paras, labels, exc)


def lexical_nlp_fallback(text: str, paras: list[str], labels: list[str], exc: Exception) -> dict:
    label_keywords = {
        "theophysics": ("god", "logos", "christ", "theology", "creation", "fall"),
        "formal proof": ("proof", "axiom", "theorem", "derive", "formal", "logic"),
        "scientific paper": ("method", "evidence", "experiment", "observation", "data"),
        "research": ("paper", "source", "claim", "model", "framework"),
        "theology": ("scripture", "god", "sin", "cross", "resurrection"),
        "physics": ("quantum", "entropy", "energy", "measurement", "wavefunction"),
        "axiom mapping": ("axiom", "mapping", "law", "layer", "operator"),
        "speculative synthesis": ("suggests", "framework", "analogy", "synthesis", "model"),
    }
    lower = text.lower()
    scores = {}
    for label in labels:
        words = label_keywords[label]
        scores[label] = sum(lower.count(word) for word in words)
    total = max(sum(scores.values()), 1)
    normalized = {label: round(value / total, 3) for label, value in scores.items()}
    top_label = max(normalized, key=normalized.get)
    return {
        "engine": "lexical NLP fallback",
        "status": "fallback",
        "fallback_reason": f"{type(exc).__name__}: {exc}",
        "labels": labels,
        "classification": normalized,
        "top_label": top_label,
        "top_score": normalized[top_label],
        "chunks_analyzed": len(paras),
    }


def map_axioms(paras: list[str]) -> list[AxiomMapping]:
    mappings: list[AxiomMapping] = []
    for axiom in AXIOMS:
        quote = best_quote(paras, tuple(axiom["keywords"]))
        if not quote:
            continue
        hits = sum(quote.lower().count(k) for k in axiom["keywords"])
        confidence = max(0.35, min(0.92, 0.38 + hits * 0.08))
        mappings.append(
            AxiomMapping(
                axiom_id=str(axiom["id"]),
                axiom_name=str(axiom["name"]),
                category=str(axiom["category"]),
                interpretation=(
                    f"The text engages {axiom['name']} by using language around "
                    f"{', '.join(axiom['keywords'][:3])} to carry part of the argument."
                ),
                source_quote=quote,
                confidence=round(confidence, 2),
            )
        )
    return sorted(mappings, key=lambda item: item.confidence, reverse=True)


def top_terms(text: str) -> list[tuple[str, int]]:
    stop = {
        "the", "and", "that", "with", "this", "from", "into", "are", "for", "not",
        "but", "you", "was", "have", "has", "its", "can", "all", "one", "their",
        "there", "which", "when", "then", "than", "through", "between",
    }
    words = re.findall(r"\b[a-zA-Z][a-zA-Z-]{4,}\b", text.lower())
    counts = Counter(w for w in words if w not in stop)
    return counts.most_common(24)


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def render_html(payload: dict) -> str:
    score = payload["score"]
    items = payload["paper_model"]
    mappings = payload["axiom_mappings"]
    terms = payload["top_terms"]
    nlp = payload["nlp_stack"]

    def score_row(label: str, key: str, bad: bool = False) -> str:
        value = int(score[key])
        color = "var(--red)" if bad else "var(--green)"
        return (
            f'<div class="score-row"><span>{esc(label)}</span>'
            f'<div class="bar"><b style="width:{value}%;background:{color}"></b></div>'
            f'<strong>{value}</strong></div>'
        )

    model_cards = "\n".join(
        f"""
        <article class="card">
          <div class="eyebrow">{esc(item["category"])}</div>
          <h3>{esc(item["claim"])}</h3>
          <blockquote>{esc(item["source_quote"] or "No direct quote found in first-pass extraction.")}</blockquote>
          <p class="muted">{esc(item["uncertainty_note"])} Confidence {esc(item["confidence"])}</p>
        </article>
        """
        for item in items
    )
    axiom_cards = "\n".join(
        f"""
        <article class="axiom">
          <div class="axiom-id">{esc(m["axiom_id"])} / {esc(m["category"])}</div>
          <h3>{esc(m["axiom_name"])}</h3>
          <p>{esc(m["interpretation"])}</p>
          <blockquote>{esc(m["source_quote"])}</blockquote>
          <div class="confidence">confidence {esc(m["confidence"])}</div>
        </article>
        """
        for m in mappings
    )
    term_tags = "\n".join(f"<span>{esc(term)} <b>{count}</b></span>" for term, count in terms)

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(payload["title"])} | Black Axiom Snapshot</title>
<style>
:root {{
  --bg:#050505; --panel:#0b0b0c; --card:#111214; --line:#252525;
  --text:#e8e3d6; --muted:#9b9487; --gold:#d4af37; --red:#c94040;
  --green:#22c55e; --teal:#14b8a6; --violet:#8b7fc2;
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--text); font-family:Inter,Segoe UI,Arial,sans-serif; line-height:1.55; }}
.nav {{ position:sticky; top:0; z-index:10; display:flex; gap:18px; align-items:center; padding:14px 24px; background:rgba(5,5,5,.94); border-bottom:1px solid var(--line); }}
.brand {{ color:var(--gold); font-weight:700; letter-spacing:.08em; text-transform:uppercase; }}
.nav a {{ color:var(--muted); text-decoration:none; font-size:13px; }}
main {{ max-width:1180px; margin:0 auto; padding:34px 24px 64px; }}
.hero {{ display:grid; grid-template-columns:1.4fr .8fr; gap:24px; align-items:stretch; border-bottom:1px solid var(--line); padding-bottom:28px; }}
h1 {{ font-family:Georgia,serif; font-size:clamp(34px,6vw,72px); line-height:1; margin:0 0 16px; color:var(--gold); letter-spacing:0; }}
h2 {{ margin:34px 0 14px; color:var(--gold); font-size:22px; }}
h3 {{ margin:6px 0 10px; font-size:18px; }}
.panel,.card,.axiom {{ background:var(--card); border:1px solid var(--line); border-radius:8px; padding:18px; }}
.overall {{ display:grid; place-items:center; min-height:220px; text-align:center; }}
.overall .num {{ font-size:82px; color:var(--gold); font-weight:800; line-height:1; }}
.muted,.meta {{ color:var(--muted); }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:14px; }}
.score-row {{ display:grid; grid-template-columns:190px 1fr 44px; gap:12px; align-items:center; margin:10px 0; color:var(--muted); }}
.bar {{ height:9px; background:#242424; border-radius:999px; overflow:hidden; }}
.bar b {{ display:block; height:100%; }}
blockquote {{ margin:12px 0 0; padding:10px 12px; border-left:3px solid var(--gold); background:#080808; color:#cfc7b6; font-size:14px; }}
.eyebrow,.axiom-id,.confidence {{ color:var(--teal); font-size:12px; text-transform:uppercase; letter-spacing:.08em; }}
.axiom {{ border-color:#2d2816; }}
.tags {{ display:flex; flex-wrap:wrap; gap:8px; }}
.tags span {{ border:1px solid var(--line); border-radius:999px; padding:5px 10px; color:var(--muted); background:#090909; }}
.tags b {{ color:var(--gold); }}
footer {{ margin-top:40px; padding-top:18px; border-top:1px solid var(--line); color:var(--muted); font-size:13px; }}
@media (max-width:760px) {{ .hero {{ grid-template-columns:1fr; }} .score-row {{ grid-template-columns:1fr; }} }}
@media print {{ .nav {{ position:static; }} body {{ background:white; color:black; }} .panel,.card,.axiom {{ break-inside:avoid; }} }}
</style>
</head>
<body>
<nav class="nav">
  <div class="brand">Treaties / Black Axiom Snapshot</div>
  <a href="#score">Score</a><a href="#model">Paper Model</a><a href="#axioms">Axioms</a><a href="#terms">Terms</a>
</nav>
<main>
  <section class="hero">
    <div>
      <p class="meta">Generated {esc(payload["generated_at"])} from {esc(payload["source_path"])}</p>
      <h1>{esc(payload["title"])}</h1>
      <p class="muted">{esc(payload["summary"])}</p>
    </div>
    <aside class="panel overall" id="score">
      <div>
        <div class="num">{esc(score["overall_score"])}</div>
        <div class="meta">overall first-pass grade</div>
      </div>
    </aside>
  </section>
  <section class="panel">
    <h2>Evidence Scorecard</h2>
    {score_row("Methodological rigor", "methodological_rigor")}
    {score_row("Evidence strength", "evidence_strength")}
    {score_row("Reproducibility", "reproducibility")}
    {score_row("Clarity", "clarity")}
    {score_row("Bias risk", "bias_risk", True)}
    <p class="muted">{esc(payload["signals"]["notes"])}</p>
    <p class="muted">Scoring engine: {esc(score.get("engine", "unknown"))}</p>
  </section>
  <section class="panel">
    <h2>NLP Stack Pass</h2>
    <p><strong>{esc(nlp.get("engine"))}</strong> / {esc(nlp.get("status"))}</p>
    <p class="muted">Chunks analyzed: {esc(nlp.get("chunks_analyzed", 0))}</p>
    <pre style="white-space:pre-wrap;background:#080808;border:1px solid var(--line);padding:12px;border-radius:8px;color:#cfc7b6;overflow:auto;">{esc(json.dumps(nlp, indent=2)[:3500])}</pre>
  </section>
  <h2 id="model">Universal Paper Model</h2>
  <section class="grid">{model_cards}</section>
  <h2 id="axioms">Black Axiom Map</h2>
  <section class="grid">{axiom_cards}</section>
  <h2 id="terms">NLP Term Surface</h2>
  <section class="panel tags">{term_tags}</section>
  <footer>Generated by Treaties standalone exporter. HTML is a review artifact; source text remains canonical.</footer>
</main>
</body>
</html>"""


def render_markdown(payload: dict) -> str:
    score = payload["score"]
    lines = [
        f"# {payload['title']} - Paper Grade",
        "",
        f"- Source: `{payload['source_path']}`",
        f"- Generated: {payload['generated_at']}",
        f"- Overall: {score['overall_score']}/100",
        f"- Scoring engine: {score.get('engine', 'unknown')}",
        f"- NLP engine: {payload['nlp_stack'].get('engine', 'unknown')} ({payload['nlp_stack'].get('status', 'unknown')})",
        f"- Methodological rigor: {score['methodological_rigor']}/100",
        f"- Evidence strength: {score['evidence_strength']}/100",
        f"- Reproducibility: {score['reproducibility']}/100",
        f"- Clarity: {score['clarity']}/100",
        f"- Bias risk: {score['bias_risk']}/100",
        "",
        "## Paper Model",
    ]
    for item in payload["paper_model"]:
        lines.extend(
            [
                f"### {item['category'].title()}",
                item["claim"],
                "",
                f"> {item['source_quote'] or 'No direct quote found in first-pass extraction.'}",
                "",
            ]
        )
    lines.append("## Axiom Map")
    for mapping in payload["axiom_mappings"]:
        lines.extend(
            [
                f"### {mapping['axiom_id']} - {mapping['axiom_name']}",
                f"Confidence: {mapping['confidence']}",
                "",
                mapping["interpretation"],
                "",
                f"> {mapping['source_quote']}",
                "",
            ]
        )
    return "\n".join(lines)


def build_payload(source: Path) -> dict:
    title, text = extract_text(source)
    paras = paragraphs(text)
    model = extract_model_items(paras)
    signals = score_signals(text)
    score = component_scores(signals)
    mappings = map_axioms(paras)
    nlp_stack = run_nlp_stack(text, paras)
    summary = (
        "A chunk-aware first-pass conversion of the Genesis-to-Quantum HTML into Treaties' "
        "paper-model, evidence grading, and axiom mapping surface."
    )
    return {
        "schema_version": "gtq-black-axiom-snapshot-0.1",
        "title": title,
        "source_path": str(source),
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "summary": summary,
        "text_stats": {
            "characters": len(text),
            "paragraphs": len(paras),
        },
        "signals": signals,
        "score": score,
        "nlp_stack": nlp_stack,
        "paper_model": [asdict(item) for item in model],
        "axiom_mappings": [asdict(mapping) for mapping in mappings],
        "top_terms": top_terms(text),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=r"D:\HTML_MASTER\00_GENESIS TO QUANTUM.html")
    parser.add_argument(
        "--snapshot-dir",
        default=r"E:\faiththru Physics\faiththruphysics.com-deploy-cannotical\proof-explorer",
    )
    parser.add_argument("--ratings-dir", default=r"X:\ratings")
    parser.add_argument("--axioms-dir", default=r"X:\axioms\papers")
    args = parser.parse_args()

    source = Path(args.source)
    payload = build_payload(source)
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "-", payload["title"]).strip("-") or "genesis-to-quantum"
    slug = slug[:80]

    snapshot_dir = Path(args.snapshot_dir)
    ratings_dir = Path(args.ratings_dir)
    axioms_dir = Path(args.axioms_dir)
    for folder in (snapshot_dir, ratings_dir, axioms_dir):
        folder.mkdir(parents=True, exist_ok=True)

    html_path = snapshot_dir / f"{slug}-black-axiom-snapshot.html"
    json_path = ratings_dir / f"{slug}-paper-grade.json"
    md_path = axioms_dir / f"{slug}-paper-grade.md"

    html_path.write_text(render_html(payload), encoding="utf-8")
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8")

    print(json.dumps({
        "html": str(html_path),
        "json": str(json_path),
        "markdown": str(md_path),
        "overall_score": payload["score"]["overall_score"],
        "axiom_mappings": len(payload["axiom_mappings"]),
        "paragraphs": payload["text_stats"]["paragraphs"],
    }, indent=2))


if __name__ == "__main__":
    main()
