"""
PAPER ANALYZER — GROUND UP
===========================
Built from the Text-as-System + Link Topology spec.
Two documents. One analyzer. 14 metric categories.

NO fluff. Every metric is load-bearing.

Levels:
  L1 — Structural Baseline
  L2 — Grammatical Composition (POS + verb types)
  L3 — Semantic Structure (clustering, recurrence, term stability)
  L4 — Information Density (compression, redundancy, signal/noise)
  L5 — Readability + Cognitive Load
  L6 — Argument Structure (claims, evidence, falsifiability)
  L7 — Flow + Coherence (transitions, topic drift)
  L8 — Link Topology (types, network, quality, balance)
"""
import re, zlib
import os
from pathlib import Path
from collections import Counter

try:
    import spacy
    nlp = spacy.load('en_core_web_sm')
    HAS_SPACY = True
except Exception:
    HAS_SPACY = False; nlp = None

try:
    import numpy as np
    from sentence_transformers import SentenceTransformer
    CACHE = Path(r"O:\999_IGNORE\Obsidian Programs\Python_Backend\core\truth_engine\model_cache")
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
    _st_model = SentenceTransformer(
        "all-MiniLM-L6-v2",
        cache_folder=str(CACHE),
        local_files_only=True,
    )
    HAS_ST = True
except Exception:
    HAS_ST = False; _st_model = None

try:
    import networkx as nx
    HAS_NX = True
except Exception:
    HAS_NX = False

STOPWORDS = {
    'the','a','an','is','are','was','were','be','been','have','has','had',
    'do','does','did','will','would','shall','should','may','might','can',
    'could','that','this','these','those','it','its','i','we','you','they',
    'he','she','and','or','but','not','so','for','of','in','on','at','to',
    'from','with','by','about','into','through','over','after','then','than',
}

MODAL_VERBS = {'can','could','may','might','should','would','shall','must','ought'}
ASSERTIVE_VERBS = {'proves','demonstrates','shows','establishes','confirms',
                   'validates','derives','concludes','requires','necessitates'}
PASSIVE_PATTERNS = [r'\b(is|are|was|were|be|been|being)\s+\w+ed\b',
                    r'\b(is|are|was|were)\s+\w+en\b']

TRANSITION_WORDS = {
    'therefore','thus','hence','consequently','accordingly','so',
    'however','nevertheless','nonetheless','although','whereas',
    'because','since','as a result','furthermore','moreover',
    'additionally','in contrast','on the other hand','specifically',
    'for example','for instance','in summary','in conclusion',
    'first','second','third','finally','next','then',
}

CLAIM_MARKERS = [
    r'\b(we claim|we argue|we propose|we demonstrate|we show|we prove)\b',
    r'\b(the evidence suggests|the data shows|this implies|this means)\b',
    r'\b(it follows that|therefore|thus|hence|necessarily|must be)\b',
    r'\b(is defined as|is given by|equals|is equivalent to)\b',
]

EVIDENCE_MARKERS = [
    r'\b(evidence|empirical|experimental|measured|observed|data)\b',
    r'\b(statistically|sigma|p-value|confidence interval|correlation)\b',
    r'\b(study|experiment|trial|test|analysis|result|finding)\b',
    r'\[[\d,\s]+\]',                   # [1] [2,3]
    r'\([A-Z][a-z]+,\s*\d{4}\)',       # (Author, 2024)
    r'\bet al\.',
]

FALSIFY_MARKERS = [
    r'\b(falsif|disprove|refute|if.*then|prediction|test|measurable)\b',
    r'\b(would be wrong if|fails when|breaks down|limit of)\b',
    r'\b(null hypothesis|counter-example|boundary condition)\b',
]

LINK_PATTERNS = {
    'citation':   [r'\([A-Z][a-z]+,\s*\d{4}\)', r'\[\d+\]', r'\bet al\.',
                   r'\b(doi|DOI):', r'https?://\S+'],
    'concept':    [r'\b(see|refer to|as defined|per|following)\b',
                   r'\b(above|below|previous|next|section \d)\b'],
    'dependency': [r'\b(relies on|depends on|requires|builds on|assumes)\b',
                   r'\b(given that|provided that|if and only if)\b'],
    'evidence':   [r'\b(supports|validates|confirms|demonstrates|shows that)\b',
                   r'\b(consistent with|in agreement with)\b'],
    'navigation': [r'\b(figure|table|equation|appendix|section)\s*\d+\b'],
}

CROSS_DOMAIN_MARKERS = [
    r'\b(isomorphism|maps to|analogous|mirrors|corresponds)\b',
    r'\b(physics|quantum|entropy|thermodynamic)\b.*\b(theolog|spirit|god|faith)\b',
    r'\b(theolog|spirit|god|faith)\b.*\b(physics|quantum|entropy|information)\b',
    r'\b(mathematical|equation|formula)\b.*\b(moral|ethical|virtue|sin)\b',
]

def strip_md(text):
    t = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    t = re.sub(r'\*{1,3}([^*]+)\*{1,3}', r'\1', t)
    t = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', t)
    t = re.sub(r'`[^`]+`', '', t)
    return t.strip()

def get_sentences(text):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if len(s.strip()) > 20]

def get_paragraphs(text):
    return [p.strip() for p in text.split('\n\n') if len(p.strip()) > 40]

# ── L1: STRUCTURAL BASELINE ───────────────────────────────────────────────
def l1_structural(text, raw_text):
    words = text.split()
    sentences = get_sentences(text)
    paragraphs = get_paragraphs(raw_text)
    unique = set(w.lower().strip('.,;:!?"\'') for w in words if len(w) > 2)
    ttr = round(len(unique) / max(len(words), 1), 4)
    avg_wps = round(len(words) / max(len(sentences), 1), 1)
    avg_spp = round(len(sentences) / max(len(paragraphs), 1), 1)
    headers = re.findall(r'^#{1,4} .+', raw_text, re.MULTILINE)
    return {
        'word_count': len(words),
        'unique_word_count': len(unique),
        'ttr': ttr,
        'sentence_count': len(sentences),
        'paragraph_count': len(paragraphs),
        'header_count': len(headers),
        'avg_words_per_sentence': avg_wps,
        'avg_sentences_per_paragraph': avg_spp,
    }

# ── L2: GRAMMATICAL COMPOSITION ───────────────────────────────────────────
def l2_grammar(text):
    if not HAS_SPACY or not nlp:
        return {'pos_note': 'spacy not available'}
    doc = nlp(text[:40000])
    total = len([t for t in doc if not t.is_space])
    if total == 0: return {}
    pos_counts = Counter(t.pos_ for t in doc if not t.is_space and not t.is_punct)
    noun_pct   = round(pos_counts.get('NOUN', 0) / total * 100, 1)
    verb_pct   = round(pos_counts.get('VERB', 0) / total * 100, 1)
    adj_pct    = round(pos_counts.get('ADJ', 0) / total * 100, 1)
    adv_pct    = round(pos_counts.get('ADV', 0) / total * 100, 1)
    prep_pct   = round(pos_counts.get('ADP', 0) / total * 100, 1)
    tl = text.lower()
    verbs = [t for t in doc if t.pos_ == 'VERB']
    modal_count = sum(1 for t in doc if t.lower_ in MODAL_VERBS)
    assertive_count = sum(1 for t in doc if t.lower_ in ASSERTIVE_VERBS)
    passive_count = sum(len(re.findall(p, tl)) for p in PASSIVE_PATTERNS)
    verb_total = max(len(verbs), 1)
    # Signal-heavy: high nouns = conceptual weight, high adj/adv = possible fluff
    weight_signal = 'CONCEPTUAL' if noun_pct > 20 else 'VERBAL' if verb_pct > 15 else 'MIXED'
    fluff_flag = adj_pct + adv_pct > 15
    return {
        'noun_pct': noun_pct,
        'verb_pct': verb_pct,
        'adj_pct': adj_pct,
        'adv_pct': adv_pct,
        'prep_pct': prep_pct,
        'passive_voice_count': passive_count,
        'passive_pct': round(passive_count / max(len(verbs), 1) * 100, 1),
        'modal_verb_count': modal_count,
        'assertive_verb_count': assertive_count,
        'modal_vs_assertive_ratio': round(modal_count / max(assertive_count, 1), 2),
        'weight_signal': weight_signal,
        'fluff_flag': fluff_flag,
    }

# ── L3: SEMANTIC STRUCTURE (term stability, topic drift) ──────────────────
def l3_semantic(text):
    result = {}
    if not HAS_ST or not _st_model:
        return {'semantic_note': 'sentence-transformers not available'}
    paragraphs = get_paragraphs(text)
    if len(paragraphs) < 2:
        return {'topic_drift_avg': 0, 'topic_drift_max': 0}
    try:
        vecs = _st_model.encode(paragraphs[:20], convert_to_numpy=True, show_progress_bar=False)
        from numpy.linalg import norm
        drifts = []
        for i in range(len(vecs) - 1):
            a, b = vecs[i], vecs[i+1]
            sim = float(np.dot(a, b) / (norm(a) * norm(b) + 1e-10))
            drift = round(1 - sim, 4)
            drifts.append(drift)
        result['topic_drift_avg'] = round(sum(drifts)/len(drifts), 4)
        result['topic_drift_max'] = round(max(drifts), 4)
        result['topic_drift_scores'] = drifts[:10]
        result['coherence_flag'] = 'COHERENT' if result['topic_drift_avg'] < 0.3 else \
                                   'MODERATE' if result['topic_drift_avg'] < 0.5 else 'SCATTERED'
    except Exception as e:
        result['semantic_error'] = str(e)
    return result

# ── L4: INFORMATION DENSITY ───────────────────────────────────────────────
def l4_density(text):
    encoded = text.encode('utf-8')
    compressed = zlib.compress(encoded, level=9)
    compression_ratio = round(len(compressed) / max(len(encoded), 1), 4)
    # Lower ratio = higher information density (less compressible)
    density_label = 'HIGH' if compression_ratio < 0.4 else \
                    'MODERATE' if compression_ratio < 0.6 else 'LOW'
    words = text.lower().split()
    total = len(words)
    stopword_count = sum(1 for w in words if w.strip('.,;:!?"\'') in STOPWORDS)
    stopword_ratio = round(stopword_count / max(total, 1), 4)
    # n-gram redundancy (3-gram repeats)
    trigrams = [' '.join(words[i:i+3]) for i in range(len(words)-2)]
    tg_counts = Counter(trigrams)
    repeated = sum(c-1 for c in tg_counts.values() if c > 1)
    redundancy = round(repeated / max(len(trigrams), 1), 4)
    signal_noise = round((1 - stopword_ratio) * (1 - redundancy), 4)
    return {
        'compression_ratio': compression_ratio,
        'density_label': density_label,
        'stopword_ratio': stopword_ratio,
        'trigram_redundancy': redundancy,
        'signal_noise_ratio': signal_noise,
    }

# ── L5: READABILITY + COGNITIVE LOAD ─────────────────────────────────────
def l5_readability(text):
    result = {}
    try:
        import textstat
        result['flesch_kincaid_grade'] = round(textstat.flesch_kincaid_grade(text), 1)
        result['gunning_fog'] = round(textstat.gunning_fog(text), 1)
        result['smog_index'] = round(textstat.smog_index(text), 1)
        result['text_standard'] = textstat.text_standard(text)
        result['reading_time_min'] = round(textstat.reading_time(text, ms_per_char=14.69)/60, 1)
    except Exception:
        result['readability_note'] = 'textstat not available'
    sentences = get_sentences(text)
    if HAS_SPACY and nlp and sentences:
        try:
            clause_depths = []
            for sent in sentences[:30]:
                doc = nlp(sent)
                depth = max((len(list(t.ancestors)) for t in doc), default=0)
                clause_depths.append(depth)
            result['avg_dependency_depth'] = round(sum(clause_depths)/len(clause_depths), 2)
            result['max_dependency_depth'] = max(clause_depths)
            result['cognitive_load'] = 'HIGH' if result['avg_dependency_depth'] > 4 else \
                                       'MODERATE' if result['avg_dependency_depth'] > 2 else 'LOW'
        except Exception as e:
            result['cognitive_load_error'] = str(e)
    return result

# ── L6: ARGUMENT STRUCTURE ────────────────────────────────────────────────
def l6_argument(text):
    tl = text.lower()
    words = text.split()
    per1k = 1000 / max(len(words), 1)
    claim_count = sum(len(re.findall(p, tl)) for p in CLAIM_MARKERS)
    evidence_count = sum(len(re.findall(p, tl)) for p in EVIDENCE_MARKERS)
    falsify_count = sum(len(re.findall(p, tl)) for p in FALSIFY_MARKERS)
    ev_ratio = round(evidence_count / max(claim_count, 1), 2)
    claim_density = round(claim_count * per1k, 2)
    ev_density = round(evidence_count * per1k, 2)
    if ev_ratio >= 2.0:   arg_grade = 'A — Evidence-Rich'
    elif ev_ratio >= 1.0: arg_grade = 'B — Supported'
    elif ev_ratio >= 0.5: arg_grade = 'C — Partial'
    else:                 arg_grade = 'D — Underevidenced'
    return {
        'claim_count': claim_count,
        'claim_density_per1k': claim_density,
        'evidence_count': evidence_count,
        'evidence_density_per1k': ev_density,
        'evidence_to_claim_ratio': ev_ratio,
        'falsifiability_markers': falsify_count,
        'argument_grade': arg_grade,
    }

# ── L7: FLOW + COHERENCE ──────────────────────────────────────────────────
def l7_flow(text):
    tl = text.lower()
    sentences = get_sentences(text)
    total_sents = max(len(sentences), 1)
    transition_hits = sum(1 for s in sentences
                          if any(tw in s.lower() for tw in TRANSITION_WORDS))
    transition_density = round(transition_hits / total_sents * 100, 1)
    return {
        'transition_density_pct': transition_density,
        'transition_count': transition_hits,
        'flow_label': 'HIGH' if transition_density > 25 else
                      'MODERATE' if transition_density > 12 else 'LOW',
    }

# ── L8: LINK TOPOLOGY ─────────────────────────────────────────────────────
def l8_links(text, raw_text):
    tl = text.lower()
    words = text.split()
    per1k = 1000 / max(len(words), 1)

    # Count by type
    link_counts = {}
    for ltype, patterns in LINK_PATTERNS.items():
        count = sum(len(re.findall(p, tl if ltype != 'citation' else raw_text))
                    for p in patterns)
        link_counts[ltype] = count

    total_links = sum(link_counts.values())
    link_density = round(total_links * per1k, 2)

    # Internal vs external
    internal = link_counts.get('concept', 0) + link_counts.get('dependency', 0) + \
               link_counts.get('navigation', 0)
    external = link_counts.get('citation', 0)
    balance  = round(internal / max(external, 1), 2)

    # Cross-domain bridges
    cross_domain = sum(len(re.findall(p, tl, re.DOTALL)) for p in CROSS_DOMAIN_MARKERS)

    # Link quality — classify
    assertion_links = len(re.findall(r'\b(is|are|the \w+ is)\b', tl))
    supporting_links = link_counts.get('evidence', 0)
    strong_links = len(re.findall(r'\b(sigma|p-value|statistically|empirically)\b', tl))
    quality_score = round((supporting_links*2 + strong_links*3) /
                          max(assertion_links + supporting_links + strong_links, 1), 2)

    # Failure mode detection
    underlink_flag = total_links < 5
    overlink_flag  = link_density > 50

    # Network graph of concepts (paragraph-level)
    graph_stats = {}
    if HAS_NX:
        try:
            G = nx.Graph()
            paragraphs = get_paragraphs(text)
            for i, p in enumerate(paragraphs[:20]):
                G.add_node(i, text=p[:50])
            # Connect paragraphs that share significant terms
            sig_terms = [w for w, c in Counter(
                re.findall(r'\b[a-zA-Z]{5,}\b', tl)).most_common(30)
                if w not in STOPWORDS]
            for i, pi in enumerate(paragraphs[:20]):
                for j, pj in enumerate(paragraphs[i+1:20], i+1):
                    shared = sum(1 for t in sig_terms
                                 if t in pi.lower() and t in pj.lower())
                    if shared >= 2:
                        G.add_edge(i, j, weight=shared)
            if len(G.nodes) > 1 and len(G.edges) > 0:
                graph_stats['concept_nodes'] = len(G.nodes)
                graph_stats['concept_edges'] = len(G.edges)
                graph_stats['avg_degree'] = round(
                    sum(d for _, d in G.degree()) / len(G.nodes), 2)
                graph_stats['clustering_coeff'] = round(
                    nx.average_clustering(G), 4)
                central = nx.degree_centrality(G)
                top_node = max(central, key=central.get)
                graph_stats['most_central_paragraph'] = top_node
                graph_stats['centralization'] = round(max(central.values()), 4)
                # Isolated nodes = concepts that don't connect
                graph_stats['isolated_nodes'] = len(list(nx.isolates(G)))
        except Exception as e:
            graph_stats['graph_error'] = str(e)

    return {
        'total_links': total_links,
        'link_density_per1k': link_density,
        'link_citation': link_counts.get('citation', 0),
        'link_concept': link_counts.get('concept', 0),
        'link_dependency': link_counts.get('dependency', 0),
        'link_evidence': link_counts.get('evidence', 0),
        'link_navigation': link_counts.get('navigation', 0),
        'internal_links': internal,
        'external_links': external,
        'internal_external_ratio': balance,
        'cross_domain_bridges': cross_domain,
        'link_quality_score': quality_score,
        'underlink_flag': underlink_flag,
        'overlink_flag': overlink_flag,
        **graph_stats,
    }

# ── MASTER ANALYZE ────────────────────────────────────────────────────────
def analyze(path_or_text, is_path=True):
    if is_path:
        raw = Path(path_or_text).read_text(encoding='utf-8', errors='ignore')
        fname = Path(path_or_text).name
    else:
        raw = path_or_text; fname = 'inline'
    clean = strip_md(raw)
    result = {'file': fname}

    r1 = l1_structural(clean, raw);        result.update({f"s_{k}":v for k,v in r1.items()})
    r2 = l2_grammar(clean);               result.update({f"g_{k}":v for k,v in r2.items()})
    r3 = l3_semantic(clean);              result.update({f"sm_{k}":v for k,v in r3.items()})
    r4 = l4_density(clean);               result.update({f"d_{k}":v for k,v in r4.items()})
    r5 = l5_readability(clean);           result.update({f"r_{k}":v for k,v in r5.items()})
    r6 = l6_argument(clean);              result.update({f"a_{k}":v for k,v in r6.items()})
    r7 = l7_flow(clean);                  result.update({f"f_{k}":v for k,v in r7.items()})
    r8 = l8_links(clean, raw);            result.update({f"lk_{k}":v for k,v in r8.items()})

    return result

if __name__ == '__main__':
    import sys, json
    if len(sys.argv) > 1:
        r = analyze(sys.argv[1])
        # Remove raw lists for display
        r.pop('sm_topic_drift_scores', None)
        print(json.dumps(r, indent=2, default=str))
