"""
GENESIS TO QUANTUM — FULL ANALYTICS SUITE
==========================================
Produces:
  1. High-level Series Overview (markdown)
  2. Knowledge Graph (JSON + Obsidian canvas + networkx PNG)
  3. Atoms extracted from each article (Obsidian notes with YAML frontmatter)
  4. Molecules (cross-article syntheses)
  5. Co-term density analysis
  6. Per-article concept hubs
  7. Series coherence matrix
  8. Tag index for Obsidian

Non-recursive: top-level .md articles only.
Output: Data Vault mirror folder.
"""

import json
import re
import sys
import os
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
import hashlib

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ── Paths ────────────────────────────────────────────────────────────────
SERIES_DIR = Path(r"O:\_Theophysics_v4\04_THEOPYHISCS\[TX_A6.6] THE CONVERGENCE\GENESIS TO QUANTUM The Seven-Article Series")
OUTPUT_DIR = Path(r"O:\_Theophysics_v4\Data Vault\04_THEOPYHISCS\[TX_A6.6] THE CONVERGENCE\GENESIS TO QUANTUM The Seven-Article Series")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Sub-folders
ATOMS_DIR = OUTPUT_DIR / "Atoms"
MOLECULES_DIR = OUTPUT_DIR / "Molecules"
GRAPHS_DIR = OUTPUT_DIR / "Graphs"
HUBS_DIR = OUTPUT_DIR / "Concept_Hubs"
for d in [ATOMS_DIR, MOLECULES_DIR, GRAPHS_DIR, HUBS_DIR]:
    d.mkdir(exist_ok=True)

# ── Config ───────────────────────────────────────────────────────────────
DOMAINS = {
    "physics": ["gravity", "mass", "energy", "entropy", "quantum", "spacetime",
                "relativity", "collapse", "decoherence", "entanglement", "photon",
                "wave function", "superposition", "measurement", "light", "field"],
    "theology": ["grace", "sin", "soul", "resurrection", "faith", "covenant",
                 "redemption", "salvation", "cross", "atonement", "holy", "genesis",
                 "creation", "god", "christ", "spirit", "prayer"],
    "information": ["coherence", "information", "observer", "logos",
                    "signal", "noise", "error correction", "bit", "entropy",
                    "data", "code", "channel"],
    "consciousness": ["consciousness", "awareness", "choice", "agency",
                      "mind", "free will", "qualia", "experience", "observer"],
}

CORE_CONCEPTS = [
    "Grace", "Entropy", "Coherence", "Logos", "Trinity", "Resurrection",
    "Consciousness", "Information", "Quantum", "Soul", "Faith", "Judgment",
    "Collapse", "Observer", "Decoherence", "Spacetime", "Gravity",
    "Wave function", "Superposition", "Measurement", "Entanglement",
    "Free will", "Sin", "Covenant", "Redemption", "Cross", "Atonement",
    "Error correction", "Signal", "Noise", "Photon", "Light",
    "Genesis", "Creation", "Time", "Eternity", "Truth",
]

SPECIALIZED_TERMS = [
    "chi", "logos", "coherence", "entropy", "field", "observer", "collapse",
    "grace", "consciousness", "quantum", "trinity", "faith", "covenant",
    "signal", "noise", "measurement", "superposition", "decoherence",
    "atonement", "redemption", "resurrection", "soul", "spirit",
]

# ── Load articles ────────────────────────────────────────────────────────
SKIP_PREFIXES = ("00_", "_", "README")
all_md = [f for f in SERIES_DIR.glob("*.md") if f.is_file()]
articles = sorted([
    f for f in all_md
    if not any(f.name.startswith(p) for p in SKIP_PREFIXES)
    and not f.name.endswith("_media_block.md")
    and not f.name.endswith("_publish_gate.md")
])

print("=" * 70)
print("GENESIS TO QUANTUM - FULL ANALYTICS SUITE")
print("=" * 70)
print(f"Articles: {len(articles)}")
print(f"Output:   {OUTPUT_DIR}")
print()

article_data = {}
for art in articles:
    text = art.read_text(encoding="utf-8")
    article_data[art.name] = {
        "path": art,
        "text": text,
        "words": text.split(),
        "word_count": len(text.split()),
    }

# ══════════════════════════════════════════════════════════════════════════
# 1. CONCEPT EXTRACTION & COUNTING
# ══════════════════════════════════════════════════════════════════════════
print("[1/8] Extracting concepts...")

for name, data in article_data.items():
    lower = data["text"].lower()
    concepts = {}
    for c in CORE_CONCEPTS:
        n = lower.count(c.lower())
        if n > 0:
            concepts[c] = n
    data["concepts"] = concepts

    # Domains
    doms = set()
    for domain, terms in DOMAINS.items():
        for t in terms:
            if t in lower:
                doms.add(domain)
                break
    data["domains"] = list(doms)

    # Extract Obsidian links
    links = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', data["text"])
    data["obsidian_links"] = links

    # Extract sections
    sections = re.findall(r'^#{1,3}\s+(.+)$', data["text"], re.MULTILINE)
    data["sections"] = sections

    print(f"  {name[:50]:<52} concepts={len(concepts):>2}  domains={len(doms)}  links={len(links):>3}  sections={len(sections):>2}")

# Global concept counts
global_concepts = Counter()
for data in article_data.values():
    global_concepts.update(data["concepts"])

# ══════════════════════════════════════════════════════════════════════════
# 2. KNOWLEDGE GRAPH
# ══════════════════════════════════════════════════════════════════════════
print("\n[2/8] Building knowledge graph...")

G = nx.Graph()

# Add article nodes
for name in article_data:
    short = name.replace(".md", "")[:40]
    G.add_node(short, type="article", weight=article_data[name]["word_count"])

# Add concept nodes (top 25)
top_concepts = [c for c, _ in global_concepts.most_common(25)]
for c in top_concepts:
    G.add_node(c, type="concept", weight=global_concepts[c])

# Connect articles to their concepts
for name, data in article_data.items():
    short = name.replace(".md", "")[:40]
    for c in top_concepts:
        if c in data["concepts"]:
            G.add_edge(short, c, weight=data["concepts"][c])

# Connect concepts that co-occur frequently
for i, c1 in enumerate(top_concepts):
    for c2 in top_concepts[i+1:]:
        co_count = 0
        for data in article_data.values():
            if c1 in data["concepts"] and c2 in data["concepts"]:
                co_count += min(data["concepts"][c1], data["concepts"][c2])
        if co_count >= 5:
            G.add_edge(c1, c2, weight=co_count, type="co-occurrence")

print(f"  Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
print(f"  Density: {nx.density(G):.3f}")
if nx.is_connected(G):
    print(f"  Connected: yes")
else:
    components = list(nx.connected_components(G))
    print(f"  Components: {len(components)}")

# Save graph as JSON (for Obsidian / D3 / etc.)
graph_json = {
    "nodes": [
        {"id": n, "type": G.nodes[n].get("type", ""), "weight": G.nodes[n].get("weight", 0)}
        for n in G.nodes
    ],
    "edges": [
        {"source": u, "target": v, "weight": G.edges[u, v].get("weight", 1)}
        for u, v in G.edges
    ],
    "stats": {
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "density": round(nx.density(G), 4),
    }
}
(GRAPHS_DIR / "knowledge_graph.json").write_text(json.dumps(graph_json, indent=2), encoding="utf-8")

# Save as Obsidian Canvas
canvas_nodes = []
canvas_edges = []
pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
for i, (node, (x, y)) in enumerate(pos.items()):
    ntype = G.nodes[node].get("type", "")
    color = "#FFD700" if ntype == "article" else "#00CED1"
    canvas_nodes.append({
        "id": hashlib.md5(node.encode()).hexdigest()[:8],
        "type": "text",
        "text": node,
        "x": int(x * 1500),
        "y": int(y * 1500),
        "width": 250,
        "height": 60,
        "color": color,
    })

node_id_map = {n["text"]: n["id"] for n in canvas_nodes}
for u, v in G.edges:
    u_short = u
    v_short = v
    if u_short in node_id_map and v_short in node_id_map:
        canvas_edges.append({
            "id": hashlib.md5(f"{u}{v}".encode()).hexdigest()[:8],
            "fromNode": node_id_map[u_short],
            "toNode": node_id_map[v_short],
            "fromSide": "right",
            "toSide": "left",
        })

canvas = {"nodes": canvas_nodes, "edges": canvas_edges}
(GRAPHS_DIR / "knowledge_graph.canvas").write_text(json.dumps(canvas, indent=2), encoding="utf-8")

# Render PNG
fig, ax = plt.subplots(figsize=(18, 14), facecolor='#0D1117')
node_colors = ["#FFD700" if G.nodes[n].get("type") == "article" else "#00CED1" for n in G.nodes]
node_sizes = [max(300, G.nodes[n].get("weight", 1) * 0.8) for n in G.nodes]
edge_weights = [G.edges[u, v].get("weight", 1) * 0.3 for u, v in G.edges]

nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.9, ax=ax)
nx.draw_networkx_edges(G, pos, width=edge_weights, alpha=0.4, edge_color="#555555", ax=ax)
nx.draw_networkx_labels(G, pos, font_size=7, font_color="white", font_weight="bold", ax=ax)

ax.set_title("Genesis to Quantum - Knowledge Graph", color="white", fontsize=16, fontweight="bold", pad=20)
ax.set_facecolor('#0D1117')
ax.axis('off')
plt.tight_layout()
plt.savefig(str(GRAPHS_DIR / "knowledge_graph.png"), dpi=200, facecolor='#0D1117', bbox_inches='tight')
plt.close()
print(f"  Saved: knowledge_graph.json, .canvas, .png")

# ══════════════════════════════════════════════════════════════════════════
# 3. ATOMS — Extract atomic concepts from each article
# ══════════════════════════════════════════════════════════════════════════
print("\n[3/8] Generating Atom notes...")

atom_count = 0
all_atoms = []
today = datetime.now().strftime("%Y-%m-%d")

for name, data in article_data.items():
    # Top concepts in this article become atoms
    sorted_concepts = sorted(data["concepts"].items(), key=lambda x: x[1], reverse=True)
    for concept, count in sorted_concepts[:8]:  # Top 8 per article
        # Determine atom type
        atom_type = "definition"
        lower_c = concept.lower()
        if lower_c in ["collapse", "decoherence", "entanglement", "error correction"]:
            atom_type = "mechanism"
        elif lower_c in ["coherence", "faith", "grace", "truth"]:
            atom_type = "principle"
        elif lower_c in ["measurement", "observation"]:
            atom_type = "observation"

        # Determine domains
        atom_domains = []
        for domain, terms in DOMAINS.items():
            if any(t in lower_c for t in terms) or lower_c in [t for t in terms]:
                atom_domains.append(domain)
        if not atom_domains:
            atom_domains = ["theophysics"]

        # Find related atoms from same article
        related = [c for c, _ in sorted_concepts[:8] if c != concept][:4]

        # Trinity mapping
        trinity = "Triune"
        if lower_c in ["logos", "truth", "information", "signal", "code", "light"]:
            trinity = "Son"
        elif lower_c in ["grace", "gravity", "creation", "genesis", "time", "eternity", "covenant"]:
            trinity = "Father"
        elif lower_c in ["consciousness", "faith", "free will", "observer", "spirit", "awareness"]:
            trinity = "Spirit"

        atom_id = f"ATOM_{concept.replace(' ', '_').upper()}_{name[:2]}"
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', f"{atom_id}.md")

        atom_md = f"""---
title: "{concept}"
type: atom
atom_type: {atom_type}
created: "{today}"
updated: "{today}"
status: child
phase: 02_Foundations
project: Quantum_Gospel
domains:
{chr(10).join(f'  - {d}' for d in atom_domains)}
tags:
  - genesis-to-quantum
  - {concept.lower().replace(' ', '-')}
trinity_aspect: {trinity}
related_atoms: [{', '.join(f'"{r}"' for r in related)}]
source_material: ["{name}"]
mention_count: {count}
coherence_score: {min(count / 50.0, 1.0):.2f}
---

# {concept}

## Definition
Atomic concept extracted from **{name.replace('.md', '')}** ({count} mentions).

## Trinity Connection
**Aspect:** {trinity}

## Physics <-> Theology Bridge
**Physics side:** {concept} as physical/informational phenomenon.

**Theology side:** {concept} as theological/spiritual principle.

## Source Context
- Extracted from: [[{name.replace('.md', '')}]]
- Series: Genesis to Quantum Seven-Article Series
- Mentions in source: {count}

## Related Atoms
{chr(10).join(f'- [[{r}]]' for r in related)}
"""
        (ATOMS_DIR / safe_name).write_text(atom_md, encoding="utf-8")
        atom_count += 1
        all_atoms.append({"id": atom_id, "concept": concept, "source": name, "count": count, "trinity": trinity, "domains": atom_domains})

print(f"  Generated {atom_count} Atom notes")

# ══════════════════════════════════════════════════════════════════════════
# 4. MOLECULES — Cross-article syntheses
# ══════════════════════════════════════════════════════════════════════════
print("\n[4/8] Generating Molecule notes...")

# Find concepts that appear across multiple articles
concept_articles = defaultdict(list)
for name, data in article_data.items():
    for c in data["concepts"]:
        concept_articles[c].append(name)

molecule_count = 0
all_molecules = []

# Concepts appearing in 4+ articles become molecules
for concept, art_list in sorted(concept_articles.items(), key=lambda x: len(x[1]), reverse=True):
    if len(art_list) < 4:
        continue

    total_mentions = sum(article_data[a]["concepts"].get(concept, 0) for a in art_list)
    component_atoms = [a for a in all_atoms if a["concept"] == concept][:5]

    mol_id = f"MOL_{concept.replace(' ', '_').upper()}"
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', f"{mol_id}.md")

    mol_md = f"""---
title: "{concept} - Cross-Article Synthesis"
type: molecule
synthesis_type: pattern
created: "{today}"
updated: "{today}"
status: assembling
phase: 04_Integration
project: Quantum_Gospel
domains:
  - theophysics
tags:
  - genesis-to-quantum
  - molecule
  - {concept.lower().replace(' ', '-')}
component_atoms: [{', '.join(f'"{a["id"]}"' for a in component_atoms)}]
article_coverage: {len(art_list)}/{len(articles)}
total_mentions: {total_mentions}
internal_consistency: needs-testing
predictive_power: untested
---

# {concept} - Cross-Article Synthesis

## Synthesis Statement
**{concept}** appears across {len(art_list)} of {len(articles)} articles ({len(art_list)/len(articles)*100:.0f}% coverage), with {total_mentions} total mentions. This makes it a structural load-bearing concept in the series.

## Articles Where Present
{chr(10).join(f'- [[{a.replace(".md", "")}]] ({article_data[a]["concepts"].get(concept, 0)} mentions)' for a in art_list)}

## Component Atoms
{chr(10).join(f'- [[{a["id"]}]] (from {a["source"][:40]})' for a in component_atoms)}

## The Integration
How does **{concept}** function differently across these articles? What pattern emerges?

## Emergent Properties
(Cross-article patterns that individual articles don't reveal)

## Connects To
**Related Molecules:**
{chr(10).join(f'- [[MOL_{c.replace(" ", "_").upper()}]]' for c, arts in concept_articles.items() if len(arts) >= 4 and c != concept)[:5]}
"""
    (MOLECULES_DIR / safe_name).write_text(mol_md, encoding="utf-8")
    molecule_count += 1
    all_molecules.append({"id": mol_id, "concept": concept, "articles": len(art_list), "mentions": total_mentions})

print(f"  Generated {molecule_count} Molecule notes")

# ══════════════════════════════════════════════════════════════════════════
# 5. CO-TERM DENSITY
# ══════════════════════════════════════════════════════════════════════════
print("\n[5/8] Computing co-term density...")

coterm_results = {}
window = 15

for term in ["coherence", "collapse", "observer", "grace", "quantum", "logos"]:
    co_counts = Counter()
    term_total = 0
    for name, data in article_data.items():
        words = [w.lower() for w in data["words"]]
        for i, w in enumerate(words):
            if term in w:
                term_total += 1
                start = max(0, i - window)
                end = min(len(words), i + window + 1)
                ctx = words[start:end]
                for st in SPECIALIZED_TERMS:
                    if st != term:
                        co_counts[st] += ctx.count(st)

    density = (sum(co_counts.values()) / term_total * 100) if term_total > 0 else 0
    coterm_results[term] = {
        "occurrences": term_total,
        "density": round(density, 2),
        "top_co_terms": co_counts.most_common(8),
    }
    print(f"  {term:<15} occ={term_total:>4}  density={density:.1f}  top={co_counts.most_common(3)}")

(OUTPUT_DIR / "co_term_density.json").write_text(json.dumps(coterm_results, indent=2, default=str), encoding="utf-8")

# ══════════════════════════════════════════════════════════════════════════
# 6. CONCEPT HUBS (Obsidian MOC notes)
# ══════════════════════════════════════════════════════════════════════════
print("\n[6/8] Generating Concept Hub notes...")

hub_count = 0
for concept, count in global_concepts.most_common(20):
    arts_with = [(n, d["concepts"][concept]) for n, d in article_data.items() if concept in d["concepts"]]
    arts_with.sort(key=lambda x: x[1], reverse=True)

    safe_name = re.sub(r'[<>:"/\\|?*]', '_', f"HUB_{concept.replace(' ', '_')}.md")

    hub_md = f"""---
title: "{concept} - Concept Hub"
type: concept_hub
created: "{today}"
tags:
  - concept-hub
  - genesis-to-quantum
  - {concept.lower().replace(' ', '-')}
total_mentions: {count}
article_coverage: {len(arts_with)}/{len(articles)}
---

# {concept} - Concept Hub

> **{count} mentions** across **{len(arts_with)} articles** ({len(arts_with)/len(articles)*100:.0f}% series coverage)

## Articles (by mention density)

| Article | Mentions | Density |
|---------|----------|---------|
{chr(10).join(f'| [[{n.replace(".md", "")}]] | {c} | {c/article_data[n]["word_count"]*1000:.1f}/1k words |' for n, c in arts_with)}

## Related Concepts
```dataview
TABLE mentions
FROM "Atoms"
WHERE contains(tags, "{concept.lower().replace(' ', '-')}")
SORT mentions DESC
```

## Co-Term Network
{chr(10).join(f'- **{ct}**: {cc} co-occurrences' for ct, cc in coterm_results.get(concept.lower(), {}).get("top_co_terms", [])[:5])}
"""
    (HUBS_DIR / safe_name).write_text(hub_md, encoding="utf-8")
    hub_count += 1

print(f"  Generated {hub_count} Concept Hub notes")

# ══════════════════════════════════════════════════════════════════════════
# 7. COHERENCE MATRIX
# ══════════════════════════════════════════════════════════════════════════
print("\n[7/8] Computing coherence matrix...")

art_names = list(article_data.keys())
n = len(art_names)
matrix = np.zeros((n, n))

for i, a1 in enumerate(art_names):
    set1 = set(article_data[a1]["concepts"].keys())
    for j, a2 in enumerate(art_names):
        if i == j:
            matrix[i][j] = 1.0
            continue
        set2 = set(article_data[a2]["concepts"].keys())
        if set1 | set2:
            matrix[i][j] = len(set1 & set2) / len(set1 | set2)

# Render heatmap
fig, ax = plt.subplots(figsize=(14, 12), facecolor='#0D1117')
short_names = [n.replace(".md", "")[:30] for n in art_names]
im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto', vmin=0, vmax=1)
ax.set_xticks(range(n))
ax.set_yticks(range(n))
ax.set_xticklabels(short_names, rotation=45, ha='right', fontsize=7, color='white')
ax.set_yticklabels(short_names, fontsize=7, color='white')
ax.set_title("Article Coherence Matrix (Jaccard Similarity)", color='white', fontsize=14, fontweight='bold', pad=15)
plt.colorbar(im, ax=ax, label='Jaccard Similarity')
ax.set_facecolor('#0D1117')
for i in range(n):
    for j in range(n):
        ax.text(j, i, f'{matrix[i][j]:.2f}', ha='center', va='center', fontsize=6, color='black' if matrix[i][j] > 0.5 else 'white')
plt.tight_layout()
plt.savefig(str(GRAPHS_DIR / "coherence_matrix.png"), dpi=200, facecolor='#0D1117', bbox_inches='tight')
plt.close()

# Save matrix as JSON
matrix_json = {"articles": art_names, "matrix": matrix.tolist()}
(GRAPHS_DIR / "coherence_matrix.json").write_text(json.dumps(matrix_json, indent=2), encoding="utf-8")
print(f"  Saved coherence_matrix.png + .json")

# ══════════════════════════════════════════════════════════════════════════
# 8. TAG INDEX + HIGH-LEVEL OVERVIEW
# ══════════════════════════════════════════════════════════════════════════
print("\n[8/8] Generating Tag Index + Series Overview...")

# Tag Index
all_tags = Counter()
for data in article_data.values():
    for c in data["concepts"]:
        all_tags[c.lower().replace(" ", "-")] += data["concepts"][c]

tag_index_md = f"""---
title: "Genesis to Quantum - Tag Index"
type: tag_index
created: "{today}"
---

# Tag Index - Genesis to Quantum Series

| Tag | Total Mentions | Articles |
|-----|---------------|----------|
{chr(10).join(f'| #{tag} | {count} | {sum(1 for d in article_data.values() if any(c.lower().replace(" ","-") == tag for c in d["concepts"]))} |' for tag, count in all_tags.most_common(30))}
"""
(OUTPUT_DIR / "TAG_INDEX.md").write_text(tag_index_md, encoding="utf-8")

# ── HIGH-LEVEL OVERVIEW ──────────────────────────────────────────────────
total_words = sum(d["word_count"] for d in article_data.values())
avg_jaccard = np.mean(matrix[np.triu_indices(n, k=1)])

overview_md = f"""---
title: "Genesis to Quantum - Series Overview"
type: overview
created: "{today}"
series: Genesis to Quantum
article_count: {len(articles)}
total_words: {total_words}
unique_concepts: {len(global_concepts)}
atoms_generated: {atom_count}
molecules_generated: {molecule_count}
avg_coherence: {avg_jaccard:.3f}
---

# Genesis to Quantum: The Seven-Article Series
## High-Level Analytics Overview

> Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Series at a Glance

| Metric | Value |
|--------|-------|
| Articles Analyzed | {len(articles)} |
| Total Words | {total_words:,} |
| Unique Concepts | {len(global_concepts)} |
| Atoms Generated | {atom_count} |
| Molecules Generated | {molecule_count} |
| Concept Hubs | {hub_count} |
| Knowledge Graph Nodes | {G.number_of_nodes()} |
| Knowledge Graph Edges | {G.number_of_edges()} |
| Graph Density | {nx.density(G):.3f} |
| Avg Inter-Article Coherence | {avg_jaccard:.3f} |

---

## Domain Coverage

| Domain | Articles | Coverage |
|--------|----------|----------|
| Physics | {sum(1 for d in article_data.values() if 'physics' in d['domains'])} | {sum(1 for d in article_data.values() if 'physics' in d['domains'])/len(articles)*100:.0f}% |
| Theology | {sum(1 for d in article_data.values() if 'theology' in d['domains'])} | {sum(1 for d in article_data.values() if 'theology' in d['domains'])/len(articles)*100:.0f}% |
| Information | {sum(1 for d in article_data.values() if 'information' in d['domains'])} | {sum(1 for d in article_data.values() if 'information' in d['domains'])/len(articles)*100:.0f}% |
| Consciousness | {sum(1 for d in article_data.values() if 'consciousness' in d['domains'])} | {sum(1 for d in article_data.values() if 'consciousness' in d['domains'])/len(articles)*100:.0f}% |

---

## Top 20 Concepts

| Rank | Concept | Mentions | Coverage | Status |
|------|---------|----------|----------|--------|
{chr(10).join(f'| {i+1} | **{c}** | {n} | {len(concept_articles[c])}/{len(articles)} articles | {"Molecule" if len(concept_articles[c]) >= 4 else "Atom"} |' for i, (c, n) in enumerate(global_concepts.most_common(20)))}

---

## Per-Article Breakdown

| # | Article | Words | Concepts | Domains | Sections |
|---|---------|-------|----------|---------|----------|
{chr(10).join(f'| {i+1} | [[{name.replace(".md", "")}]] | {data["word_count"]:,} | {len(data["concepts"])} | {len(data["domains"])} | {len(data["sections"])} |' for i, (name, data) in enumerate(article_data.items()))}

---

## Structural Load-Bearing Concepts (Molecules)

These concepts span 4+ articles, forming the structural backbone of the series:

{chr(10).join(f'- **{m["concept"]}**: {m["articles"]}/{len(articles)} articles, {m["mentions"]} mentions → [[{m["id"]}]]' for m in sorted(all_molecules, key=lambda x: x["mentions"], reverse=True))}

---

## Co-Term Density (Top Concepts)

| Term | Occurrences | Density | Top Co-Terms |
|------|------------|---------|--------------|
{chr(10).join(f'| {term} | {r["occurrences"]} | {r["density"]:.1f} | {", ".join(f"{t}({c})" for t, c in r["top_co_terms"][:3])} |' for term, r in coterm_results.items())}

---

## Knowledge Graph

![[knowledge_graph.png]]

## Coherence Matrix

![[coherence_matrix.png]]

---

## Output Files

### Graphs
- `Graphs/knowledge_graph.json` — D3-compatible graph data
- `Graphs/knowledge_graph.canvas` — Obsidian Canvas file
- `Graphs/knowledge_graph.png` — Network visualization
- `Graphs/coherence_matrix.json` — Article similarity matrix
- `Graphs/coherence_matrix.png` — Heatmap visualization

### Obsidian Notes
- `Atoms/` — {atom_count} atomic concept notes with YAML frontmatter
- `Molecules/` — {molecule_count} cross-article synthesis notes
- `Concept_Hubs/` — {hub_count} concept hub MOC notes
- `TAG_INDEX.md` — Searchable tag reference

### Data
- `co_term_density.json` — Term proximity analysis
- `SERIES_OVERVIEW.md` — This file
"""

(OUTPUT_DIR / "SERIES_OVERVIEW.md").write_text(overview_md, encoding="utf-8")

print(f"\n{'='*70}")
print(f"COMPLETE")
print(f"{'='*70}")
print(f"  Atoms:         {atom_count}")
print(f"  Molecules:     {molecule_count}")
print(f"  Concept Hubs:  {hub_count}")
print(f"  Graph nodes:   {G.number_of_nodes()}")
print(f"  Graph edges:   {G.number_of_edges()}")
print(f"  Coherence avg: {avg_jaccard:.3f}")
print(f"  Output:        {OUTPUT_DIR}")
