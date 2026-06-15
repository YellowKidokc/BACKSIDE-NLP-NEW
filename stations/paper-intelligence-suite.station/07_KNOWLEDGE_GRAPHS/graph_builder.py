"""
L7: KNOWLEDGE GRAPH BUILDER
=============================
Builds paper-to-paper graph from pipeline results.
"""
import json, re
from pathlib import Path
from datetime import datetime

# NumPy 2.0 compat — python-louvain uses removed np.float_
import numpy as np
if not hasattr(np, 'float_'): np.float_ = np.float64
if not hasattr(np, 'int_'):   np.int_ = np.int64

try:
    import networkx as nx; HAS_NX = True
except ImportError:
    HAS_NX = False

try:
    import community as community_louvain; HAS_LOUVAIN = True
except ImportError:
    HAS_LOUVAIN = False

try:
    from pyvis.network import Network; HAS_PYVIS = True
except ImportError:
    HAS_PYVIS = False

def build_graph(paper_rows, output_dir):
    if not HAS_NX:
        return {}
    G = nx.Graph()
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for row in paper_rows:
        fname = row.get('file', 'unknown')
        G.add_node(fname, **{
            'label': fname.replace('.md','')[:30],
            'chi_score': row.get('L3_chi_score', 0),
            'wk_ratio': row.get('L3_wk_ratio', 0),
            'dominant_variable': row.get('L3_me_dominant_variable', ''),
            'truth_tier': row.get('L3_ckg_tier', ''),
            'word_count': row.get('L1_word_count', 0),
            'topic_1': row.get('L5_topic_1', ''),
            'truth_score': row.get('L6_truth_score', 0),
            'combined_score': row.get('L6_combined_score', 0),
        })

    nodes = list(paper_rows)
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            a, b = nodes[i], nodes[j]
            fa, fb = a.get('file',''), b.get('file','')
            weight = 0
            dom_a, dom_b = a.get('L3_me_dominant_variable',''), b.get('L3_me_dominant_variable','')
            if dom_a and dom_b and dom_a == dom_b: weight += 3
            chi_a = float(a.get('L3_chi_score', 0) or 0)
            chi_b = float(b.get('L3_chi_score', 0) or 0)
            if abs(chi_a - chi_b) < 1.5: weight += 1
            tier_a, tier_b = a.get('L3_ckg_tier',''), b.get('L3_ckg_tier','')
            if tier_a and tier_b and tier_a == tier_b: weight += 2
            ta = set(a.get('L5_topic_1','').lower().split(', '))
            tb = set(b.get('L5_topic_1','').lower().split(', '))
            overlap = ta & tb - {''}
            if len(overlap) > 1: weight += len(overlap)
            if weight > 0 and fa and fb:
                G.add_edge(fa, fb, weight=weight)

    partition = {}
    if HAS_LOUVAIN and len(G.nodes) > 1:
        try:
            partition = community_louvain.best_partition(G)
            nx.set_node_attributes(G, partition, 'cluster')
        except Exception as e:
            print(f"  Louvain err: {e}")

    centrality, betweenness = {}, {}
    if len(G.nodes) > 0:
        try:
            centrality = nx.degree_centrality(G)
            betweenness = nx.betweenness_centrality(G)
        except Exception: pass

    node_data = {
        node: {
            'centrality': round(centrality.get(node, 0), 4),
            'betweenness': round(betweenness.get(node, 0), 4),
            'cluster': partition.get(node, 0),
            'degree': G.degree(node),
        } for node in G.nodes
    }

    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    nx.write_graphml(G, str(output_dir / f"knowledge_graph_{ts}.graphml"))

    json_data = {
        'nodes': [{'id': n, 'label': G.nodes[n].get('label', n),
                   'cluster': G.nodes[n].get('cluster', 0),
                   'centrality': round(centrality.get(n, 0), 4),
                   'chi_score': G.nodes[n].get('chi_score', 0)} for n in G.nodes],
        'edges': [{'source': u, 'target': v, 'weight': d.get('weight', 1)}
                  for u, v, d in G.edges(data=True)],
        'stats': {
            'node_count': len(G.nodes), 'edge_count': len(G.edges),
            'cluster_count': len(set(partition.values())) if partition else 0,
            'most_central': max(centrality, key=centrality.get) if centrality else '',
        }
    }
    (output_dir / f"knowledge_graph_{ts}.json").write_text(
        json.dumps(json_data, indent=2), encoding='utf-8')

    if HAS_PYVIS and len(G.nodes) > 0:
        try:
            COLORS = ['#4e79a7','#f28e2b','#e15759','#76b7b2','#59a14f','#edc948','#b07aa1','#ff9da7']
            net = Network(height='700px', width='100%', bgcolor='#1a1a2e', font_color='white')
            for n, attrs in G.nodes(data=True):
                cluster = attrs.get('cluster', 0)
                size = max(15, min(50, int(centrality.get(n, 0) * 100) + 15))
                net.add_node(n, label=attrs.get('label', n)[:25],
                             color=COLORS[cluster % len(COLORS)], size=size,
                             title=f"CHI: {attrs.get('chi_score',0)} | Tier: {attrs.get('truth_tier','')} | Truth: {attrs.get('truth_score',0)} | Cluster: {cluster}")
            for u, v, d in G.edges(data=True):
                net.add_edge(u, v, value=d.get('weight', 1))
            net.set_options('{"physics":{"forceAtlas2Based":{"gravitationalConstant":-50},"solver":"forceAtlas2Based"},"interaction":{"hover":true}}')
            html_path = output_dir / f"knowledge_graph_{ts}.html"
            net.save_graph(str(html_path))
            print(f"  Graph HTML: {html_path.name}")
        except Exception as e:
            print(f"  pyvis err: {e}")

    stats = json_data['stats']
    print(f"  Graph: {stats['node_count']} nodes | {stats['edge_count']} edges | {stats['cluster_count']} clusters | most central: {stats['most_central']}")
    return {'node_data': node_data, 'stats': stats}


if __name__ == '__main__':
    print("Graph builder ready. Call build_graph(paper_rows, output_dir).")
