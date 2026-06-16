"""
MDA SERIES FLOW GATE
====================
Required substage of 03_SCORED.
Vectorizes all MDA articles, computes handoff scores between consecutive
articles in manifest order, runs optimal-ordering analysis, and mutates
MANIFEST.json with gate fields.

Nothing enters 04_PROOF_PACKET, 05_READING_LEVELS, 06_HTML_BUILD, or
08_DEPLOY_READY unless series_flow_scored=true AND (order_verdict=pass
OR order_verdict=waived).

Usage:
    python run_series_flow.py
    python run_series_flow.py --waive
    python run_series_flow.py --threshold 0.3
    python run_series_flow.py --folder-order DEPLOY_ROOT

Inputs:
    ..\\01_LOSSLESS\\articles\\*.md
    ..\\MANIFEST.json

Outputs (to this directory):
    mda_series_flow_report.md
    mda_handoff_scores.csv
    mda_suggested_order.csv
    mda_series_flow_run.json

Mutates:
    ..\\MANIFEST.json  (adds series_flow block)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import re
import csv
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional

import numpy as np

# ── Model cache — same as paper-intelligence-suite ──────────────────────
MODEL_CACHE = Path(r"O:\999_IGNORE\Obsidian Programs\Python_Backend\core\truth_engine\model_cache")
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

try:
    from sentence_transformers import SentenceTransformer
    _model = SentenceTransformer("all-MiniLM-L6-v2", cache_folder=str(MODEL_CACHE), local_files_only=True)
    HAS_MODEL = True
except Exception as e:
    print(f"[FATAL] sentence-transformers not available: {e}")
    HAS_MODEL = False
    _model = None

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── Paths ───────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
WORKFLOW_ROOT = SCRIPT_DIR.parent.parent
ARTICLES_DIR = WORKFLOW_ROOT / "01_LOSSLESS" / "articles"
MANIFEST_PATH = WORKFLOW_ROOT / "MANIFEST.json"
OUTPUT_DIR = SCRIPT_DIR  # outputs go right here in series-flow/

# ── Configuration ───────────────────────────────────────────────────────
DEFAULT_THRESHOLD = 0.35   # handoff score below this = flagged
INTRO_WORDS = 500          # words from article start for intro embedding
OUTRO_WORDS = 500          # words from article end for conclusion embedding
PASS_MIN_RATIO = 0.80      # 80% of handoffs must pass threshold for order_verdict=pass

# ── Section map (folder-first architecture) ─────────────────────────────
# Used for section-aware scoring: cross-section handoffs are expected to be low.
SECTION_MAP = {
    "01-story":    ["MDA-001", "MDA-002", "MDA-008", "MDA-012", "MDA-016", "MDA-031", "MDA-050"],
    "02-method":   ["MDA-003", "MDA-004", "MDA-005", "MDA-006", "MDA-007",
                    "MDA-037", "MDA-038", "MDA-039", "MDA-040", "MDA-041"],
    "03-evidence": ["MDA-009", "MDA-010", "MDA-011", "MDA-013", "MDA-014",
                    "MDA-015", "MDA-017", "MDA-018", "MDA-019"],
    "04-collapse": ["MDA-020", "MDA-021", "MDA-022", "MDA-023", "MDA-024",
                    "MDA-025", "MDA-026", "MDA-027", "MDA-028", "MDA-029",
                    "MDA-030", "MDA-032", "MDA-033", "MDA-034", "MDA-035", "MDA-036"],
    "05-amish":    ["MDA-042", "MDA-043", "MDA-044", "MDA-045", "MDA-046",
                    "MDA-047", "MDA-048", "MDA-049", "MDA-051"],
    "06-recovery": ["MDA-052", "MDA-053", "MDA-054"],
}

def _id_from_filename(fname: str) -> str:
    m = re.match(r"(MDA-\d+)", fname)
    return m.group(1) if m else fname

def get_section(fname: str) -> str:
    fid = _id_from_filename(fname)
    for section, ids in SECTION_MAP.items():
        if fid in ids:
            return section
    return "appendix"

def is_cross_section(a: str, b: str) -> bool:
    return get_section(a) != get_section(b)


# ── Recommendation engine ───────────────────────────────────────────────

def get_last_sentences(text: str, n: int = 3) -> str:
    sents = re.split(r'(?<=[.!?])\s+', text.strip())
    return " ".join(sents[-n:]) if len(sents) >= n else text[-500:]

def get_first_sentences(text: str, n: int = 3) -> str:
    sents = re.split(r'(?<=[.!?])\s+', text.strip())
    return " ".join(sents[:n]) if len(sents) >= n else text[:500]

def extract_top_terms(text: str, n: int = 8) -> list[str]:
    """Extract top distinctive terms from text (crude but fast)."""
    words = re.findall(r'\b[a-z]{4,}\b', text.lower())
    from collections import Counter
    STOP = {'this','that','these','those','with','from','have','been','were',
            'their','they','will','would','could','should','into','about',
            'more','than','also','what','when','which','there','other','some',
            'each','only','most','same','such','very','much','just','even',
            'like','over','does','after','before','between','through','under',
            'many','every','still','while','during','being','without','within',
            'along','across','because','however','although','whether','rather',
            'since','until','upon','itself','something','anything','everything',
            'another','against'}
    counts = Counter(w for w in words if w not in STOP)
    return [w for w, _ in counts.most_common(n)]

def generate_recommendation(fname_a: str, fname_b: str,
                             handoff_score: float,
                             cross_section: bool) -> str:
    """Generate concrete improvement recommendation for a handoff."""
    path_a = ARTICLES_DIR / fname_a
    path_b = ARTICLES_DIR / fname_b
    if not path_a.exists() or not path_b.exists():
        return "Cannot analyze: file(s) missing."

    text_a = extract_text(path_a)
    text_b = extract_text(path_b)
    ending = get_last_sentences(text_a)
    opening = get_first_sentences(text_b)
    terms_a = extract_top_terms(ending)
    terms_b = extract_top_terms(opening)
    shared = set(terms_a) & set(terms_b)
    unique_a = [t for t in terms_a if t not in shared][:4]
    unique_b = [t for t in terms_b if t not in shared][:4]

    if cross_section:
        return (f"SECTION BOUNDARY ({get_section(fname_a)} → {get_section(fname_b)}). "
                f"Expected low handoff. Article A ends on [{', '.join(unique_a)}], "
                f"article B opens on [{', '.join(unique_b)}]. "
                f"Shared terms: [{', '.join(shared) or 'none'}]. "
                f"FIX: Add a 1-sentence section transition at end of A or start of B "
                f"that bridges the mode shift.")

    if handoff_score < 0.10:
        severity = "CRITICAL GAP"
        fix = (f"Article A ends on [{', '.join(unique_a)}] but B opens on "
               f"[{', '.join(unique_b)}] with NO semantic overlap. "
               f"Concrete steps: (1) Add a concluding sentence to A that introduces "
               f"the concept of [{unique_b[0] if unique_b else '?'}]. "
               f"(2) Add an opening sentence to B that references "
               f"[{unique_a[0] if unique_a else '?'}] from A. "
               f"(3) Consider whether these articles belong adjacent in reading order.")
    elif handoff_score < 0.25:
        severity = "WEAK LINK"
        fix = (f"Partial overlap but thin bridge. A ends on [{', '.join(unique_a)}], "
               f"B opens on [{', '.join(unique_b)}]. "
               f"Shared: [{', '.join(shared) or 'none'}]. "
               f"FIX: Strengthen A's conclusion by echoing one term from B's opening "
               f"({unique_b[0] if unique_b else '?'}), or strengthen B's opening "
               f"by referencing A's closing theme ({unique_a[0] if unique_a else '?'}).")
    else:
        severity = "SOFT FLAG"
        fix = (f"Near threshold. A ends on [{', '.join(unique_a[:2])}], "
               f"B opens on [{', '.join(unique_b[:2])}]. "
               f"Shared: [{', '.join(shared) or 'none'}]. "
               f"Minor polish: one bridging phrase would clear this.")

    return f"{severity}: {fix}"


# ── Helpers ─────────────────────────────────────────────────────────────

def load_manifest() -> dict:
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        return json.load(f)


def get_manifest_order(manifest: dict) -> list[str]:
    """Return article filenames in manifest order (excludes appendices)."""
    return [a["file"] for a in manifest["articles"]
            if not a["file"].startswith("MDA-9")]


def get_all_manifest_files(manifest: dict) -> list[str]:
    """Return all article filenames in manifest order."""
    return [a["file"] for a in manifest["articles"]]


def extract_text(path: Path) -> str:
    """Read article, strip markdown/HTML cruft and boilerplate, return clean text."""
    raw = path.read_text(encoding="utf-8", errors="replace")
    # Strip HTML tags if present
    text = re.sub(r"<[^>]+>", " ", raw)
    # Strip markdown headers/links/images
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"#{1,6}\s*", "", text)
    text = re.sub(r"[*_]{1,3}", "", text)
    # Strip ring navigation footer (present in all MDA articles)
    text = re.sub(r"Ring\s*\d\s*[—–-]\s*(Core Article|Supporting Evidence|Broader Context).*",
                  "", text, flags=re.DOTALL | re.IGNORECASE)
    # Strip orphaned nav fragments that might survive
    text = re.sub(r"No connections mapped yet\.?", "", text)
    text = re.sub(r"You are here\.?", "", text)
    text = re.sub(r"Audio\s*\d+:\d+.*", "", text, flags=re.DOTALL)
    text = re.sub(r"Theophysics Research Institute.*", "", text, flags=re.DOTALL)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def get_intro(text: str, n_words: int = INTRO_WORDS) -> str:
    words = text.split()
    return " ".join(words[:n_words])


def get_outro(text: str, n_words: int = OUTRO_WORDS) -> str:
    words = text.split()
    return " ".join(words[-n_words:])


def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    d = np.dot(a, b)
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(d / (na * nb))


def embed_articles(filenames: list[str]) -> dict:
    """Embed intro, outro, and full text for each article. Returns dict keyed by filename."""
    results = {}
    for fname in filenames:
        path = ARTICLES_DIR / fname
        if not path.exists():
            print(f"  [SKIP] {fname} — file not found")
            continue
        text = extract_text(path)
        if len(text.split()) < 20:
            print(f"  [SKIP] {fname} — too short ({len(text.split())} words)")
            continue

        intro = get_intro(text)
        outro = get_outro(text)

        emb_intro = _model.encode(intro, normalize_embeddings=True)
        emb_outro = _model.encode(outro, normalize_embeddings=True)
        emb_full  = _model.encode(text[:3000], normalize_embeddings=True)  # cap for speed

        results[fname] = {
            "intro_emb": emb_intro,
            "outro_emb": emb_outro,
            "full_emb":  emb_full,
            "word_count": len(text.split()),
        }
        print(f"  [OK] {fname} ({len(text.split())} words)")
    return results


def compute_handoffs(order: list[str], embeddings: dict, threshold: float) -> list[dict]:
    """Compute handoff score between consecutive articles in given order.
    Handoff = cosine_sim(article_N outro, article_N+1 intro)."""
    handoffs = []
    for i in range(len(order) - 1):
        a, b = order[i], order[i + 1]
        if a not in embeddings or b not in embeddings:
            handoffs.append({
                "from": a, "to": b, "position": i,
                "handoff_score": None, "flag": "MISSING",
                "section_from": get_section(a), "section_to": get_section(b),
                "cross_section": is_cross_section(a, b),
                "recommendation": "Cannot analyze: embedding missing.",
            })
            continue
        score = cosine_sim(embeddings[a]["outro_emb"], embeddings[b]["intro_emb"])
        full_score = cosine_sim(embeddings[a]["full_emb"], embeddings[b]["full_emb"])
        cross = is_cross_section(a, b)
        flag = "OK" if score >= threshold else ("BOUNDARY" if cross else "LOW")
        rec = ""
        if flag != "OK":
            rec = generate_recommendation(a, b, score, cross)
        handoffs.append({
            "from": a, "to": b, "position": i,
            "handoff_score": round(score, 4),
            "full_similarity": round(full_score, 4),
            "flag": flag,
            "section_from": get_section(a),
            "section_to": get_section(b),
            "cross_section": cross,
            "recommendation": rec,
        })
    return handoffs


def greedy_optimal_order(filenames: list[str], embeddings: dict) -> list[str]:
    """Greedy nearest-neighbor ordering through full-article embedding space.
    Start from first article, always pick closest unvisited next."""
    available = [f for f in filenames if f in embeddings]
    if len(available) < 2:
        return available
    order = [available[0]]
    remaining = set(available[1:])
    while remaining:
        current = order[-1]
        best, best_score = None, -1
        for candidate in remaining:
            s = cosine_sim(embeddings[current]["outro_emb"], embeddings[candidate]["intro_emb"])
            if s > best_score:
                best, best_score = candidate, s
        order.append(best)
        remaining.remove(best)
    return order


def compute_order_score(handoffs: list[dict]) -> dict:
    """Aggregate handoff scores into pass/fail verdict."""
    scored = [h for h in handoffs if h["handoff_score"] is not None]
    if not scored:
        return {"mean": 0, "min": 0, "flagged": 0, "total": 0, "pass_ratio": 0}
    scores = [h["handoff_score"] for h in scored]
    flagged = [h for h in scored if h["flag"] == "LOW"]
    return {
        "mean": round(float(np.mean(scores)), 4),
        "min": round(float(np.min(scores)), 4),
        "max": round(float(np.max(scores)), 4),
        "flagged_count": len(flagged),
        "total_handoffs": len(scored),
        "pass_ratio": round(1 - len(flagged) / len(scored), 4) if scored else 0,
    }


def write_handoff_csv(handoffs: list[dict], path: Path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["position", "from", "to",
                                          "handoff_score", "full_similarity",
                                          "section_from", "section_to",
                                          "cross_section", "flag",
                                          "recommendation"])
        w.writeheader()
        w.writerows(handoffs)
    print(f"  CSV: {path.name}")


def write_suggested_csv(suggested: list[str], manifest_order: list[str], path: Path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["suggested_position", "file", "manifest_position", "moved"])
        for i, fname in enumerate(suggested):
            orig = manifest_order.index(fname) if fname in manifest_order else -1
            w.writerow([i, fname, orig, "YES" if i != orig else ""])
    print(f"  CSV: {path.name}")


def write_report(manifest_order: list[str], handoffs: list[dict],
                 stats: dict, suggested: list[str],
                 threshold: float, verdict: str, path: Path):
    lines = [
        "# MDA Series Flow Report",
        f"Generated: {datetime.now().isoformat()}",
        f"Threshold: {threshold}",
        f"Verdict: **{verdict}**",
        "",
        "## Manifest Order — Handoff Scores",
        "",
        "| # | From | To | Handoff | Full Sim | Section | Flag |",
        "|---|------|-----|---------|----------|---------|------|",
    ]
    for h in handoffs:
        hs = h['handoff_score'] if h['handoff_score'] is not None else "N/A"
        fs = h.get('full_similarity', "N/A")
        sec = f"{h.get('section_from','')}→{h.get('section_to','')}"
        lines.append(f"| {h['position']} | {h['from']} | {h['to']} | {hs} | {fs} | {sec} | {h['flag']} |")

    # Section-aware stats
    within = [h for h in handoffs if not h.get("cross_section") and h["handoff_score"] is not None]
    cross = [h for h in handoffs if h.get("cross_section") and h["handoff_score"] is not None]
    within_flagged = [h for h in within if h["flag"] == "LOW"]
    within_scores = [h["handoff_score"] for h in within] if within else [0]
    cross_scores = [h["handoff_score"] for h in cross] if cross else [0]

    lines += [
        "",
        "## Aggregate Statistics",
        f"- Overall mean handoff: {stats['mean']}",
        f"- Min: {stats['min']} / Max: {stats['max']}",
        f"- Total flagged: {stats['flagged_count']} / {stats['total_handoffs']}",
        "",
        "### Section-Aware Breakdown",
        f"- **Within-section handoffs:** {len(within)} total, "
        f"{len(within_flagged)} flagged, "
        f"mean {round(float(np.mean(within_scores)), 4)}",
        f"- **Cross-section boundaries:** {len(cross)} total, "
        f"mean {round(float(np.mean(cross_scores)), 4)} (expected low)",
        f"- **Within-section pass ratio:** "
        f"{round(1 - len(within_flagged)/len(within), 4) if within else 0}",
        "",
        "## CONCRETE IMPROVEMENT STEPS",
        "",
        "### Critical Gaps (score < 0.10) — fix these first",
    ]
    critical = [h for h in handoffs if h["handoff_score"] is not None
                and h["handoff_score"] < 0.10 and not h.get("cross_section")]
    if not critical:
        lines.append("None.")
    for h in critical:
        lines += [f"", f"**#{h['position']}: {h['from']} → {h['to']}** "
                  f"(score: {h['handoff_score']})",
                  f"> {h.get('recommendation', '')}"]

    lines += ["", "### Weak Links (score 0.10–0.25) — strengthen bridges"]
    weak = [h for h in handoffs if h["handoff_score"] is not None
            and 0.10 <= h["handoff_score"] < 0.25 and not h.get("cross_section")]
    if not weak:
        lines.append("None.")
    for h in weak:
        lines += [f"", f"**#{h['position']}: {h['from']} → {h['to']}** "
                  f"(score: {h['handoff_score']})",
                  f"> {h.get('recommendation', '')}"]

    lines += ["", "### Soft Flags (score 0.25–threshold) — minor polish"]
    soft = [h for h in handoffs if h["handoff_score"] is not None
            and 0.25 <= h["handoff_score"] < threshold and not h.get("cross_section")]
    if not soft:
        lines.append("None.")
    for h in soft:
        lines += [f"", f"**#{h['position']}: {h['from']} → {h['to']}** "
                  f"(score: {h['handoff_score']})",
                  f"> {h.get('recommendation', '')}"]

    lines += ["", "### Section Boundaries — expected, bridge optional"]
    boundaries = [h for h in handoffs if h.get("cross_section")
                  and h["handoff_score"] is not None and h["flag"] == "BOUNDARY"]
    if not boundaries:
        lines.append("None.")
    for h in boundaries:
        lines += [f"", f"**#{h['position']}: {h['from']} → {h['to']}** "
                  f"(score: {h['handoff_score']}, {h.get('section_from')}→{h.get('section_to')})",
                  f"> {h.get('recommendation', '')}"]

    lines += ["", "---", f"Threshold: {threshold} | Pass ratio needed: {PASS_MIN_RATIO}"]
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Report: {path.name}")


def mutate_manifest(manifest: dict, stats: dict, verdict: str,
                    threshold: float, run_id: str) -> dict:
    """Add series_flow gate fields to MANIFEST.json."""
    manifest["series_flow"] = {
        "series_flow_scored": True,
        "series_flow_run": run_id,
        "series_flow_timestamp": datetime.now().isoformat(),
        "handoff_threshold": threshold,
        "handoff_mean": stats["mean"],
        "handoff_min_score": stats["min"],
        "handoff_max_score": stats["max"],
        "flagged_handoffs": stats["flagged_count"],
        "total_handoffs": stats["total_handoffs"],
        "pass_ratio": stats["pass_ratio"],
        "pass_ratio_required": PASS_MIN_RATIO,
        "order_verdict": verdict,
        "output_dir": str(OUTPUT_DIR),
    }
    return manifest


def save_manifest(manifest: dict):
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"  MANIFEST.json updated with series_flow gate")


def main():
    parser = argparse.ArgumentParser(description="MDA Series Flow Gate")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                        help=f"Handoff score threshold (default {DEFAULT_THRESHOLD})")
    parser.add_argument("--waive", action="store_true",
                        help="Force waiver — stamps manifest as waived")
    parser.add_argument("--folder-order", type=str, default=None,
                        help="Path to DEPLOY-READY root to also test folder ordering")
    args = parser.parse_args()

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    print("=" * 65)
    print("MDA SERIES FLOW GATE")
    print("=" * 65)
    print(f"Run ID:     {run_id}")
    print(f"Articles:   {ARTICLES_DIR}")
    print(f"Manifest:   {MANIFEST_PATH}")
    print(f"Threshold:  {args.threshold}")
    print(f"Output:     {OUTPUT_DIR}")
    print()

    if not HAS_MODEL:
        print("[FATAL] Cannot run without sentence-transformers. Aborting.")
        sys.exit(1)

    # Load manifest
    manifest = load_manifest()
    manifest_order = get_manifest_order(manifest)
    all_files = get_all_manifest_files(manifest)
    print(f"Manifest articles (excl appendix): {len(manifest_order)}")
    print(f"Total articles: {len(all_files)}")
    print()
    # Handle waiver
    if args.waive:
        print("[WAIVER] Forcing series_flow_scored=true, order_verdict=waived")
        stats = {"mean": 0, "min": 0, "max": 0, "flagged_count": 0,
                 "total_handoffs": 0, "pass_ratio": 0}
        manifest = mutate_manifest(manifest, stats, "waived", args.threshold, run_id)
        save_manifest(manifest)
        return

    # Embed all articles
    print("EMBEDDING ARTICLES...")
    embeddings = embed_articles(all_files)
    print(f"\nEmbedded {len(embeddings)} / {len(all_files)} articles")
    print()

    # Compute handoffs in manifest order (non-appendix)
    print("COMPUTING HANDOFF SCORES (manifest order)...")
    handoffs = compute_handoffs(manifest_order, embeddings, args.threshold)
    stats = compute_order_score(handoffs)
    print(f"  Mean: {stats['mean']}, Min: {stats['min']}, "
          f"Flagged: {stats['flagged_count']}/{stats['total_handoffs']}")
    print()

    # Optimal ordering
    print("COMPUTING SUGGESTED ORDER...")
    suggested = greedy_optimal_order(manifest_order, embeddings)
    print()

    # Determine verdict
    if stats["pass_ratio"] >= PASS_MIN_RATIO:
        verdict = "pass"
    else:
        verdict = "review_required"
    print(f"VERDICT: {verdict}")
    print()
    # Write outputs
    print("WRITING OUTPUTS...")
    write_handoff_csv(handoffs, OUTPUT_DIR / "mda_handoff_scores.csv")
    write_suggested_csv(suggested, manifest_order, OUTPUT_DIR / "mda_suggested_order.csv")
    write_report(manifest_order, handoffs, stats, suggested,
                 args.threshold, verdict, OUTPUT_DIR / "mda_series_flow_report.md")

    # Run-level JSON (machine-readable full dump)
    run_data = {
        "run_id": run_id,
        "timestamp": datetime.now().isoformat(),
        "threshold": args.threshold,
        "pass_ratio_required": PASS_MIN_RATIO,
        "verdict": verdict,
        "stats": stats,
        "handoffs": handoffs,
        "manifest_order": manifest_order,
        "suggested_order": suggested,
        "embedded_count": len(embeddings),
        "article_count": len(all_files),
    }
    run_path = OUTPUT_DIR / f"mda_series_flow_run.json"
    run_path.write_text(json.dumps(run_data, indent=2, default=str), encoding="utf-8")
    print(f"  JSON: {run_path.name}")

    # Mutate manifest
    manifest = mutate_manifest(manifest, stats, verdict, args.threshold, run_id)
    save_manifest(manifest)

    print()
    print("=" * 65)
    print(f"SERIES FLOW GATE — {verdict.upper()}")
    print("=" * 65)


if __name__ == "__main__":
    main()
