"""
Run all analytics on the Genesis to Quantum Seven-Article Series.
Non-recursive: only top-level .md article files.
"""

import json
import re
import sys
import os
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime

import numpy as np

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ── Paths ────────────────────────────────────────────────────────────────
SERIES_DIR = Path(r"O:\_Theophysics_v4\04_THEOPYHISCS\[TX_A6.6] THE CONVERGENCE\GENESIS TO QUANTUM The Seven-Article Series")
OUTPUT_DIR = SERIES_DIR / "Data_Analytics"
CONFIG_PATH = OUTPUT_DIR / "config.json"

# ── Load config ──────────────────────────────────────────────────────────
with open(CONFIG_PATH) as f:
    config = json.load(f)

CORE_CONCEPTS = config["core_concepts"]
CORE_TAGS = config["core_tags"]
PARAMS = config["analysis_parameters"]

# ── Identify article files (top-level .md, numbered articles only) ───────
SKIP_PREFIXES = ("00_", "_", "README")
all_md = [f for f in SERIES_DIR.glob("*.md") if f.is_file()]
articles = sorted([
    f for f in all_md
    if not any(f.name.startswith(p) for p in SKIP_PREFIXES)
    and not f.name.endswith("_media_block.md")
    and not f.name.endswith("_publish_gate.md")
])

print("=" * 70)
print("GENESIS TO QUANTUM — SEVEN-ARTICLE SERIES ANALYTICS")
print("=" * 70)
print(f"Series folder : {SERIES_DIR}")
print(f"Output folder : {OUTPUT_DIR}")
print(f"Articles found: {len(articles)}")
for a in articles:
    print(f"  • {a.name}")
print()

# ── Helpers ──────────────────────────────────────────────────────────────

DOMAINS = {
    "physics": ["gravity", "mass", "energy", "entropy", "quantum", "spacetime",
                "relativity", "collapse", "decoherence", "entanglement", "photon",
                "wave function", "superposition", "measurement"],
    "theology": ["grace", "sin", "soul", "resurrection", "faith", "covenant",
                 "redemption", "salvation", "cross", "atonement", "holy"],
    "information": ["χ", "coherence", "information", "observer", "logos",
                    "signal", "noise", "error correction", "bit"],
    "consciousness": ["consciousness", "awareness", "choice", "agency",
                      "mind", "free will", "qualia"],
}

def count_concepts(text):
    lower = text.lower()
    counts = {}
    for c in CORE_CONCEPTS:
        n = lower.count(c.lower())
        if n > 0:
            counts[c] = n
    return counts

def domains_in_text(text):
    lower = text.lower()
    found = set()
    for domain, terms in DOMAINS.items():
        for t in terms:
            if t in lower:
                found.add(domain)
                break
    return found

def detect_breakthroughs(text):
    triggers = [
        r"this resolves", r"for the first time", r"we can now show",
        r"this unifies", r"unprecedented", r"novel connection",
        r"breakthrough", r"revolutionary", r"this means",
        r"the implication is", r"what makes this different",
    ]
    hits = []
    for pat in triggers:
        for m in re.finditer(pat, text, re.IGNORECASE):
            start = max(0, m.start() - 200)
            end = min(len(text), m.end() + 200)
            ctx = text[start:end]
            ctx_concepts = [c for c in CORE_CONCEPTS if c.lower() in ctx.lower()]
            ctx_domains = domains_in_text(ctx)
            hits.append({
                "trigger": m.group(),
                "position": m.start(),
                "concepts": ctx_concepts,
                "domains": list(ctx_domains),
                "integration_order": len(ctx_domains),
                "novelty": min(len(ctx_concepts) / 10.0, 1.0),
            })
    return [h for h in hits
            if h["integration_order"] >= PARAMS["breakthrough_detection"]["integration_order_min"]
            and h["novelty"] >= PARAMS["breakthrough_detection"]["novelty_score_min"]]

def tag_proximity(text, window=30):
    words = text.split()
    positions = defaultdict(list)
    for i, w in enumerate(words):
        for tag in CORE_TAGS:
            if tag.lower() in w.lower():
                positions[tag].append(i)
    edges = []
    tags = list(positions.keys())
    for a_idx, tag_a in enumerate(tags):
        for tag_b in tags[a_idx + 1:]:
            for p1 in positions[tag_a]:
                for p2 in positions[tag_b]:
                    if abs(p1 - p2) <= window:
                        edges.append((tag_a, tag_b))
                        break
    return edges

# ── Per-article analysis ─────────────────────────────────────────────────
article_results = []
all_concepts_global = Counter()
cross_refs = defaultdict(list)  # which articles reference which

for art in articles:
    text = art.read_text(encoding="utf-8")
    words = text.split()
    word_count = len(words)

    concepts = count_concepts(text)
    all_concepts_global.update(concepts)

    doms = domains_in_text(text)
    bts = detect_breakthroughs(text)
    edges = tag_proximity(text, PARAMS["network_analysis"]["word_proximity_window"])

    # Cross-references to other articles
    for other in articles:
        if other == art:
            continue
        stem = other.stem.split("_", 1)[-1] if "_" in other.stem else other.stem
        if stem.lower() in text.lower() or other.stem.lower() in text.lower():
            cross_refs[art.name].append(other.name)

    # Coherence sub-scores
    cr_score = min(len(bts) * 10, 100)
    cov_score = (len(concepts) / len(CORE_CONCEPTS)) * 100 if CORE_CONCEPTS else 0
    w = PARAMS["coherence_weights"]
    coherence = cr_score * w["cross_reference_weight"] + cov_score * w["concept_coverage_weight"]

    result = {
        "file": art.name,
        "word_count": word_count,
        "concepts": concepts,
        "concept_count": len(concepts),
        "domains": list(doms),
        "domain_count": len(doms),
        "breakthroughs": len(bts),
        "breakthrough_details": bts,
        "tag_edges": len(edges),
        "cross_refs": cross_refs.get(art.name, []),
        "coherence_score": round(coherence, 2),
        "coverage_pct": round(cov_score, 2),
    }
    article_results.append(result)

    print(f"[{art.name}]")
    print(f"  Words: {word_count:,}  |  Concepts: {len(concepts)}  |  Domains: {len(doms)}  |  Breakthroughs: {len(bts)}  |  Coherence: {coherence:.1f}")

# ── Series-wide metrics ──────────────────────────────────────────────────
print("\n" + "=" * 70)
print("SERIES-WIDE METRICS")
print("=" * 70)

total_words = sum(r["word_count"] for r in article_results)
avg_coherence = np.mean([r["coherence_score"] for r in article_results])
total_breakthroughs = sum(r["breakthroughs"] for r in article_results)
total_cross_refs = sum(len(r["cross_refs"]) for r in article_results)
unique_concepts = len(all_concepts_global)

print(f"Total articles     : {len(article_results)}")
print(f"Total words        : {total_words:,}")
print(f"Unique concepts    : {unique_concepts}")
print(f"Avg coherence      : {avg_coherence:.1f}/100")
print(f"Total breakthroughs: {total_breakthroughs}")
print(f"Cross-references   : {total_cross_refs}")

print(f"\nTop 15 concepts across series:")
for concept, count in all_concepts_global.most_common(15):
    print(f"  {concept:<25} {count:>4} mentions")

# Domain coverage per article
print(f"\nDomain coverage:")
for r in article_results:
    doms_str = ", ".join(r["domains"]) if r["domains"] else "(none)"
    print(f"  {r['file'][:50]:<52} -> {doms_str}")

# ── Save results ─────────────────────────────────────────────────────────
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# JSON
json_out = {
    "generated": datetime.now().isoformat(),
    "series_folder": str(SERIES_DIR),
    "article_count": len(article_results),
    "total_words": total_words,
    "unique_concepts": unique_concepts,
    "avg_coherence": round(avg_coherence, 2),
    "total_breakthroughs": total_breakthroughs,
    "cross_references_total": total_cross_refs,
    "top_concepts": dict(all_concepts_global.most_common(30)),
    "articles": article_results,
}
json_path = OUTPUT_DIR / "series_analytics.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(json_out, f, indent=2, default=str)
print(f"\nSaved JSON  → {json_path}")

# Markdown report
md_lines = [
    "# Genesis to Quantum — Series Analytics Report",
    f"> Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    "",
    "## Summary",
    f"| Metric | Value |",
    f"|--------|-------|",
    f"| Articles | {len(article_results)} |",
    f"| Total Words | {total_words:,} |",
    f"| Unique Concepts | {unique_concepts} |",
    f"| Avg Coherence | {avg_coherence:.1f}/100 |",
    f"| Total Breakthroughs | {total_breakthroughs} |",
    f"| Cross-References | {total_cross_refs} |",
    "",
    "## Per-Article Breakdown",
    "",
    "| Article | Words | Concepts | Domains | Breakthroughs | Coherence |",
    "|---------|-------|----------|---------|---------------|-----------|",
]
for r in article_results:
    name = r["file"][:45]
    md_lines.append(
        f"| {name} | {r['word_count']:,} | {r['concept_count']} | {r['domain_count']} | {r['breakthroughs']} | {r['coherence_score']:.1f} |"
    )

md_lines += [
    "",
    "## Top 20 Concepts",
    "",
    "| Concept | Mentions |",
    "|---------|----------|",
]
for concept, count in all_concepts_global.most_common(20):
    md_lines.append(f"| {concept} | {count} |")

md_lines += [
    "",
    "## Cross-Reference Map",
    "",
]
for r in article_results:
    refs = r["cross_refs"]
    if refs:
        md_lines.append(f"- **{r['file'][:40]}** → {', '.join(r[:30] for r in refs)}")
    else:
        md_lines.append(f"- **{r['file'][:40]}** → (no cross-refs detected)")

md_lines += [
    "",
    "## Domain Coverage",
    "",
    "| Article | Physics | Theology | Information | Consciousness |",
    "|---------|---------|----------|-------------|---------------|",
]
for r in article_results:
    name = r["file"][:35]
    phy = "Y" if "physics" in r["domains"] else "-"
    the = "Y" if "theology" in r["domains"] else "-"
    inf = "Y" if "information" in r["domains"] else "-"
    con = "Y" if "consciousness" in r["domains"] else "-"
    md_lines.append(f"| {name} | {phy} | {the} | {inf} | {con} |")

md_path = OUTPUT_DIR / "SERIES_ANALYTICS_REPORT.md"
md_path.write_text("\n".join(md_lines), encoding="utf-8")
print(f"Saved MD    → {md_path}")

# Text summary
txt_path = OUTPUT_DIR / "series_analytics_summary.txt"
txt_path.write_text(f"""GENESIS TO QUANTUM — SEVEN-ARTICLE SERIES ANALYTICS
{'='*60}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SUMMARY
  Articles:           {len(article_results)}
  Total Words:        {total_words:,}
  Unique Concepts:    {unique_concepts}
  Avg Coherence:      {avg_coherence:.1f}/100
  Total Breakthroughs:{total_breakthroughs}
  Cross-References:   {total_cross_refs}

TOP CONCEPTS
{chr(10).join(f'  {c:<25} {n:>4}' for c, n in all_concepts_global.most_common(20))}

PER-ARTICLE
{chr(10).join(f'  {r["file"][:45]:<47} words={r["word_count"]:>6}  concepts={r["concept_count"]:>2}  domains={r["domain_count"]}  bt={r["breakthroughs"]}  coh={r["coherence_score"]:.1f}' for r in article_results)}
""", encoding="utf-8")
print(f"Saved TXT   → {txt_path}")

print("\nDone.")
