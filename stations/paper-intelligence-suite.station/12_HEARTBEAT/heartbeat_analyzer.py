"""
L12 — SENTENCE-LEVEL HEARTBEAT / EKG ANALYZER
===============================================
Scores every sentence against semantic anchors using SBERT embeddings.
Produces a time-series "heartbeat" showing exactly where a paper is strong
or weak across Fruits of the Spirit and Chi (Master Equation) dimensions.

Each sentence gets:
  - Fruit net score: cosine(sentence, fruit_anchor) - cosine(sentence, anti_anchor)
  - Chi net score:   cosine(sentence, chi_anchor) - cosine(sentence, anti_anchor)
  - Composite signal: weighted blend of all channels
  - Section marker: which heading this sentence falls under

Output: list of per-sentence dicts ready for Chart.js time-series rendering.
"""

import re
import numpy as np
from pathlib import Path

# ═══════════════════════════════════════════════════════════════
# SEMANTIC ANCHORS (from Truth Engine)
# ═══════════════════════════════════════════════════════════════

FRUIT_ANCHORS = {
    "love": "Sustained care for others at personal cost, relational binding, sacrificial commitment, other-regard over self-interest",
    "joy": "Stable positive state independent of circumstances, internal surplus, meaning that persists through suffering",
    "peace": "Internal stability under external pressure, low entropy in decision-space, absence of internal contradiction",
    "patience": "Delayed gratification under uncertainty, willingness to wait, resistance to premature closure",
    "kindness": "Positive-sum action without immediate return, cooperative behavior, gentle treatment of others",
    "goodness": "Alignment with truth, order preservation, norm-keeping, integrity maintenance",
    "faithfulness": "Consistency over time despite incentive drift, reliability, promise-keeping, temporal stability",
    "gentleness": "Low-force interaction when force would work faster, proportional response, restraint of power",
    "self_control": "Subordination of impulse to principle, boundary enforcement, delayed reward preference",
}

FRUIT_ANTI_ANCHORS = {
    "love": "Hatred, exploitation, using others as means, indifference to suffering, dehumanization",
    "joy": "Despair, nihilism, meaning-collapse, chronic dissatisfaction independent of circumstances",
    "peace": "Internal contradiction, cognitive dissonance, anxiety, chaos, logical incoherence",
    "patience": "Impulsivity, demand for instant results, intolerance of process, premature closure",
    "kindness": "Cruelty, zero-sum exploitation, harm for personal gain, callousness",
    "goodness": "Corruption, norm-violation, deception, entropy-acceleration, disorder promotion",
    "faithfulness": "Betrayal, inconsistency, broken commitments, opportunistic shifting, unreliability",
    "gentleness": "Coercion, force-maximization, domination, disproportionate response, intimidation",
    "self_control": "Addiction, boundary collapse, impulse dominance, rage, uncontrolled consumption",
}

CHI_ANCHORS = {
    "G": "Gravitational convergence, attraction, accumulation, gathering, structure formation, love as binding force",
    "M": "Strong binding, nuclear cohesion, holding things together, commitment, covenant, unbreakable bonds",
    "E": "Entropy, thermodynamic arrow, energy flow, decay resistance, the cost of maintaining order against chaos",
    "S": "Spacetime structure, geometry, curvature, the fabric of reality, context and framework",
    "T": "Time, sequence, causation, before-and-after, knowledge accumulation, temporal ordering",
    "K": "Knowledge, information, encoding, transmission, Logos, the word, intelligibility, meaning",
    "R": "Relationship, electromagnetic interaction, communication, connection between distinct entities",
    "Q": "Quantum consciousness, observation, measurement, wavefunction collapse, the role of the observer",
    "F": "Faith, coupling constant, how strongly an agent connects to the coherence field, voluntary alignment",
    "C": "Christ coherence, maximum integration, all things holding together, ultimate attractor, Colossians 1:17",
}

CHI_ANTI_ANCHORS = {
    "G": "Isolation, scattering, fragmentation, repulsion, nothing holds together",
    "M": "Dissolution, breaking apart, unbinding, nothing sticks, no commitment persists",
    "E": "Perfect order without cost, entropy denial, perpetual motion claims, no thermodynamic grounding",
    "S": "No structure, no context, no framework, pure abstraction with no spatial grounding",
    "T": "Timelessness denial, no sequence, no cause-effect, no temporal ordering",
    "K": "Ignorance, noise, meaninglessness, no information content, pure randomness",
    "R": "No relationship, no connection, pure isolation, no communication between entities",
    "Q": "No observer role, consciousness irrelevant, pure objectivism, measurement doesn't matter",
    "F": "No coupling, no faith, no alignment, pure autonomy from any coherence source",
    "C": "Fragmentation, incoherence, nothing holds together, anti-coherence, dissolution of meaning",
}


# ═══════════════════════════════════════════════════════════════
# SBERT ENGINE
# ═══════════════════════════════════════════════════════════════

_model = None

def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        cache_dir = str(Path(__file__).resolve().parent.parent / 'model_cache')
        _model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder=cache_dir)
    return _model


def _cosine_sim(a, b):
    """Cosine similarity: a (1D) against b (2D matrix of anchors)."""
    a_norm = a / (np.linalg.norm(a) + 1e-10)
    b_norm = b / (np.linalg.norm(b, axis=1, keepdims=True) + 1e-10)
    return (a_norm @ b_norm.T).flatten()


# ═══════════════════════════════════════════════════════════════
# STRUCTURAL FRUIT DETECTION (from fruits_scorer_v2.py)
# Per-sentence structural indicators for the heartbeat
# ═══════════════════════════════════════════════════════════════

# Each structural fruit maps to regex patterns that detect document-level
# properties at the sentence level. These are STRUCTURAL, not semantic.

STRUCTURAL_PATTERNS = {
    'definition': [
        r'(?:we\s+)?defin[e|ed|es|ing]\s+\w[\w\s]{1,40}?\s+as\s+',
        r'\w[\w\s]{1,40}?\s+is\s+defined\s+as\s+',
        r'[Ll]et\s+\w[\w\s]{1,30}?\s*[=≡:]\s*',
        r'where\s+\w[\w\s]{1,30}?\s+(?:represents?|denotes?)',
    ],
    'derivation': [
        r'\b(?:therefore|thus|hence|consequently|it follows that)\b',
        r'\b(?:from (?:this|equation|the above))\b',
        r'\b(?:combining|substituting|applying)\b',
        r'[⇒→∴⊢]',
    ],
    'scope_bound': [
        r'\b(?:does not claim|do not claim|we do not)\b',
        r'\b(?:limited to|only within|restricted to)\b',
        r'\b(?:beyond the scope|outside.*scope)\b',
        r'\b(?:falsifiabl[ey]|testabl[ey])\b',
    ],
    'prediction': [
        r'\b(?:this (?:predicts|implies|suggests|entails))\b',
        r'\b(?:we (?:predict|expect|anticipate))\b',
        r'\b(?:a testable (?:prediction|consequence))\b',
        r'\b(?:measurable (?:consequence|effect|outcome))\b',
    ],
    'evidence': [
        r'\bp\s*[<>=]\s*0?\.\d+',
        r'\bN\s*=\s*\d+',
        r'R[²2]\s*=\s*0?\.\d+',
        r'\b(?:et al\.?)\b',
        r'±\s*\d',
    ],
    'equation': [
        r'\$[^$]+\$',
        r'[A-Za-zΨΦΛχκρ]\s*[=≡≈∝→]\s*.+',
        r'∫.*d[xyzt]',
    ],
    'edge_case': [
        r'\b(?:edge case|corner case|boundary (?:case|condition))\b',
        r'\b(?:in the limit|limiting case)\b',
        r'\b(?:apparent (?:counter[- ]?example|exception|paradox))\b',
        r'\b(?:open (?:problem|question))\b',
    ],
    'modularity': [
        r'\b(?:even if.*(?:fails?|wrong).*(?:still|remains?))\b',
        r'\b(?:independent(?:ly)? of)\b',
        r'\b(?:separable|modular|standalone)\b',
    ],
    'steelman': [
        r'\b(?:the (?:strongest|best) (?:objection|argument))\b',
        r'\b(?:one (?:could|might) (?:reasonably|legitimately) (?:argue|object))\b',
        r'\b(?:to (?:be|remain) fair)\b',
    ],
    'overclaim': [  # NEGATIVE signal
        r'\b(?:proves?|proof|proven)\b',
        r'\b(?:obviously|clearly|undeniably|irrefutably)\b',
        r'\b(?:must be|can only be|the only (?:explanation|possibility))\b',
        r'\b(?:beyond (?:any |all )?doubt)\b',
    ],
    'cross_domain': [
        r'\b(?:correspond(?:s|ing)? to|maps? to|analogous to|isomorphic to)\b',
        r'\b(?:in (?:physical|spiritual|theological|mathematical) terms)\b',
        r'(?:→|↔|⟷)',
        r'\b(?:dual(?:ity)?|two (?:faces|sides) of)\b',
    ],
}

def _score_structural(sentence: str) -> dict:
    """Score a single sentence for structural indicators from fruits_v2."""
    result = {}
    total_pos = 0
    total_neg = 0
    for category, patterns in STRUCTURAL_PATTERNS.items():
        hits = 0
        for pat in patterns:
            hits += len(re.findall(pat, sentence, re.IGNORECASE))
        result[category] = hits
        if category == 'overclaim':
            total_neg += hits
        else:
            total_pos += hits
    result['structural_pos'] = total_pos
    result['structural_neg'] = total_neg
    result['structural_net'] = total_pos - total_neg * 2  # overclaims penalized 2x
    return result


# ═══════════════════════════════════════════════════════════════
# TEXT PROCESSING
# ═══════════════════════════════════════════════════════════════

def _extract_sentences_with_sections(text):
    """Split text into sentences, tracking which section each belongs to."""
    lines = text.split('\n')

    # Strip frontmatter
    if lines and lines[0].strip() == '---':
        end = next((i for i in range(1, len(lines)) if lines[i].strip() == '---'), 0)
        lines = lines[end + 1:]

    sentences = []
    current_section = "Introduction"
    section_idx = 0
    buf = []

    for line in lines:
        stripped = line.strip()

        # Detect section headings
        if stripped.startswith('#'):
            heading = stripped.lstrip('#').strip()
            if heading:
                # Flush buffer as part of previous section
                if buf:
                    paragraph = ' '.join(buf)
                    for sent in re.split(r'(?<=[.!?])\s+', paragraph):
                        sent = sent.strip()
                        if len(sent) > 15:
                            sentences.append({
                                'text': sent,
                                'section': current_section,
                                'section_idx': section_idx,
                            })
                    buf = []
                current_section = heading
                section_idx += 1
            continue

        # Skip tables, empty lines, markdown artifacts
        if stripped.startswith('|') or stripped.startswith('---') or not stripped:
            if buf:
                paragraph = ' '.join(buf)
                for sent in re.split(r'(?<=[.!?])\s+', paragraph):
                    sent = sent.strip()
                    if len(sent) > 15:
                        sentences.append({
                            'text': sent,
                            'section': current_section,
                            'section_idx': section_idx,
                        })
                buf = []
            continue

        # Clean markdown formatting
        cleaned = re.sub(r'[*_`~]{1,3}', '', stripped)
        cleaned = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()

        if cleaned:
            buf.append(cleaned)

    # Flush remaining
    if buf:
        paragraph = ' '.join(buf)
        for sent in re.split(r'(?<=[.!?])\s+', paragraph):
            sent = sent.strip()
            if len(sent) > 15:
                sentences.append({
                    'text': sent,
                    'section': current_section,
                    'section_idx': section_idx,
                })

    return sentences


# ═══════════════════════════════════════════════════════════════
# MAIN ANALYZER
# ═══════════════════════════════════════════════════════════════

def analyze(paper_path: str) -> dict:
    """
    Produce sentence-level heartbeat data for a paper.

    Returns dict with:
      - sentences: list of per-sentence score dicts
      - fruit_keys, chi_keys: dimension labels
      - section_boundaries: where sections change (for vertical markers)
      - summary stats
    """
    text = Path(paper_path).read_text(encoding='utf-8', errors='replace')
    sentences = _extract_sentences_with_sections(text)

    if not sentences:
        return {'heartbeat_error': 'no sentences extracted'}

    model = _get_model()

    # Pre-encode all anchors
    fruit_keys = list(FRUIT_ANCHORS.keys())
    fruit_vecs = model.encode([FRUIT_ANCHORS[k] for k in fruit_keys],
                               convert_to_numpy=True, show_progress_bar=False)
    fruit_anti_vecs = model.encode([FRUIT_ANTI_ANCHORS[k] for k in fruit_keys],
                                    convert_to_numpy=True, show_progress_bar=False)

    chi_keys = list(CHI_ANCHORS.keys())
    chi_vecs = model.encode([CHI_ANCHORS[k] for k in chi_keys],
                             convert_to_numpy=True, show_progress_bar=False)
    chi_anti_vecs = model.encode([CHI_ANTI_ANCHORS[k] for k in chi_keys],
                                  convert_to_numpy=True, show_progress_bar=False)

    # Encode all sentences in one batch
    sent_texts = [s['text'] for s in sentences]
    sent_vecs = model.encode(sent_texts, convert_to_numpy=True,
                              show_progress_bar=True, batch_size=64)

    # Score each sentence
    heartbeat = []
    section_boundaries = []
    prev_section_idx = -1

    for i, (svec, sdata) in enumerate(zip(sent_vecs, sentences)):
        # Track section boundaries
        if sdata['section_idx'] != prev_section_idx:
            section_boundaries.append({
                'index': i,
                'section': sdata['section'],
                'section_idx': sdata['section_idx'],
            })
            prev_section_idx = sdata['section_idx']

        # Fruit scores: net = pos_similarity - neg_similarity
        fruit_pos = _cosine_sim(svec, fruit_vecs)
        fruit_neg = _cosine_sim(svec, fruit_anti_vecs)
        fruit_net = fruit_pos - fruit_neg

        # Chi scores
        chi_pos = _cosine_sim(svec, chi_vecs)
        chi_neg = _cosine_sim(svec, chi_anti_vecs)
        chi_net = chi_pos - chi_neg

        # Composites
        fruit_composite = float(np.mean(fruit_net))
        chi_composite = float(np.mean(chi_net))
        combined = (fruit_composite + chi_composite) / 2

        # Find dominant fruit and chi variable for this sentence
        fruit_dominant_idx = int(np.argmax(fruit_net))
        chi_dominant_idx = int(np.argmax(chi_net))

        # Structural fruit v2 scores
        struct = _score_structural(sdata['text'])

        entry = {
            'idx': i,
            'text': sdata['text'][:200],  # truncate for JSON size
            'section': sdata['section'],
            'section_idx': sdata['section_idx'],
            # Per-fruit net scores (SBERT semantic)
            'fruits': {k: round(float(fruit_net[j]), 4)
                       for j, k in enumerate(fruit_keys)},
            'fruit_composite': round(fruit_composite, 4),
            'fruit_dominant': fruit_keys[fruit_dominant_idx],
            # Per-chi net scores (SBERT semantic)
            'chi': {k: round(float(chi_net[j]), 4)
                    for j, k in enumerate(chi_keys)},
            'chi_composite': round(chi_composite, 4),
            'chi_dominant': chi_keys[chi_dominant_idx],
            # Structural indicators (fruits_scorer_v2 patterns)
            'structural': struct,
            'structural_net': struct['structural_net'],
            # Combined signal (semantic + structural bonus)
            'combined': round(combined, 4),
        }
        heartbeat.append(entry)

    # Summary statistics
    fruit_composites = [h['fruit_composite'] for h in heartbeat]
    chi_composites = [h['chi_composite'] for h in heartbeat]
    combineds = [h['combined'] for h in heartbeat]

    # Find peaks and valleys
    peak_idx = int(np.argmax(combineds))
    valley_idx = int(np.argmin(combineds))

    # Moving average for smoothed signal (window=5)
    window = min(5, len(combineds))
    if window > 1:
        kernel = np.ones(window) / window
        smoothed = np.convolve(combineds, kernel, mode='same')
        for i, h in enumerate(heartbeat):
            h['combined_smooth'] = round(float(smoothed[i]), 4)

    # ── Run fruits_scorer_v2 (structural invariants) at document level ──
    v2_results = {}
    try:
        import sys as _sys
        _v2_path = str(Path(r'\\192.168.1.177\Desktop'))
        if _v2_path not in _sys.path:
            _sys.path.insert(0, _v2_path)
        from fruits_scorer_v2 import analyze_theory_fruits
        v2 = analyze_theory_fruits(text, name=Path(paper_path).stem)
        v2_results = {
            'total_score': v2.total_score,
            'normalized_score': v2.normalized_score,
            'grade': v2.grade,
            'interpretation': v2.interpretation,
            'word_count': v2.word_count,
        }
        # Extract individual fruit scores
        fruit_attrs = [
            ('love', 'f6_love'), ('joy', 'f12_joy'), ('peace', 'f7_peace'),
            ('patience', 'f3_patience'), ('kindness', 'f9_humility'),
            ('goodness', 'f10_goodness'), ('faithfulness', 'f4_faithfulness'),
            ('gentleness', 'f1_grace'), ('self_control', 'f5_self_control'),
            ('truth', 'f8_truth'), ('wisdom', 'f11_unity'), ('grace', 'f1_grace'),
        ]
        v2_fruits = {}
        for name, attr in fruit_attrs:
            fs = getattr(v2, attr, None)
            if fs:
                v2_fruits[name] = {
                    'score': fs.score,
                    'positive_hits': fs.positive_hits,
                    'negative_hits': fs.negative_hits,
                    'tier': fs.tier,
                    'interpretation': fs.interpretation,
                }
        v2_results['fruits'] = v2_fruits
        if v2.zones:
            v2_results['zones'] = {
                'theory_words': v2.zones.theory_word_count,
                'critique_words': v2.zones.critique_word_count,
                'defense_words': v2.zones.defense_word_count,
                'excluded_sections': v2.zones.excluded_sections,
            }
    except Exception as e:
        v2_results = {'error': str(e)}

    result = {
        'heartbeat': heartbeat,
        'fruit_keys': fruit_keys,
        'chi_keys': chi_keys,
        'section_boundaries': section_boundaries,
        'sentence_count': len(heartbeat),
        'v2_structural': v2_results,
        'summary': {
            'fruit_mean': round(float(np.mean(fruit_composites)), 4),
            'fruit_std': round(float(np.std(fruit_composites)), 4),
            'fruit_min': round(float(np.min(fruit_composites)), 4),
            'fruit_max': round(float(np.max(fruit_composites)), 4),
            'chi_mean': round(float(np.mean(chi_composites)), 4),
            'chi_std': round(float(np.std(chi_composites)), 4),
            'chi_min': round(float(np.min(chi_composites)), 4),
            'chi_max': round(float(np.max(chi_composites)), 4),
            'combined_mean': round(float(np.mean(combineds)), 4),
            'combined_std': round(float(np.std(combineds)), 4),
            'peak_sentence': peak_idx,
            'peak_text': heartbeat[peak_idx]['text'],
            'peak_score': heartbeat[peak_idx]['combined'],
            'valley_sentence': valley_idx,
            'valley_text': heartbeat[valley_idx]['text'],
            'valley_score': heartbeat[valley_idx]['combined'],
        },
    }

    return result


# ═══════════════════════════════════════════════════════════════
# HTML HEARTBEAT VISUALIZATION
# ═══════════════════════════════════════════════════════════════

def generate_heartbeat_html(hb_data: dict, paper_name: str = "Paper") -> str:
    """Generate a standalone HTML page with EKG-style heartbeat visualization."""
    import json

    heartbeat = hb_data.get('heartbeat', [])
    boundaries = hb_data.get('section_boundaries', [])
    summary = hb_data.get('summary', {})
    fruit_keys = hb_data.get('fruit_keys', [])
    chi_keys = hb_data.get('chi_keys', [])

    # Prepare Chart.js datasets
    labels_json = json.dumps(list(range(len(heartbeat))))
    combined_data = json.dumps([h['combined'] for h in heartbeat])
    smoothed_data = json.dumps([h.get('combined_smooth', h['combined']) for h in heartbeat])
    fruit_data = json.dumps([h['fruit_composite'] for h in heartbeat])
    chi_data = json.dumps([h['chi_composite'] for h in heartbeat])
    structural_data = json.dumps([h.get('structural_net', 0) for h in heartbeat])

    # Sentence texts for tooltips
    texts_json = json.dumps([h['text'] for h in heartbeat])
    sections_json = json.dumps([h['section'] for h in heartbeat])
    fruit_dom_json = json.dumps([h['fruit_dominant'] for h in heartbeat])
    chi_dom_json = json.dumps([h['chi_dominant'] for h in heartbeat])

    # Section boundary annotations
    annotations = []
    for b in boundaries:
        annotations.append({
            'type': 'line',
            'xMin': b['index'],
            'xMax': b['index'],
            'borderColor': 'rgba(212, 175, 55, 0.4)',
            'borderWidth': 1,
            'borderDash': [5, 5],
            'label': {
                'display': True,
                'content': b['section'][:25],
                'position': 'start',
                'color': '#d4af37',
                'font': {'size': 9, 'family': 'Inter'},
                'backgroundColor': 'rgba(10, 10, 10, 0.8)',
            }
        })
    annotations_json = json.dumps(annotations)

    # Per-fruit time series (for detail chart)
    fruit_series = {}
    for fk in fruit_keys:
        fruit_series[fk] = json.dumps([h['fruits'][fk] for h in heartbeat])

    # Per-chi time series
    chi_series = {}
    for ck in chi_keys:
        chi_series[ck] = json.dumps([h['chi'][ck] for h in heartbeat])

    # Color palette for fruits
    fruit_colors = {
        'love': '#ff6b6b', 'joy': '#ffd93d', 'peace': '#6bcb77',
        'patience': '#4d96ff', 'kindness': '#ff9a76', 'goodness': '#a8e6cf',
        'faithfulness': '#dda0dd', 'gentleness': '#87ceeb', 'self_control': '#c0c0c0',
    }

    # Color palette for chi variables
    chi_colors = {
        'G': '#ff6b6b', 'M': '#ff9a76', 'E': '#ffd93d', 'S': '#6bcb77',
        'T': '#4d96ff', 'K': '#dda0dd', 'R': '#87ceeb', 'Q': '#c0c0c0',
        'F': '#a8e6cf', 'C': '#d4af37',
    }

    # Build fruit dataset JS
    fruit_datasets_js = []
    for fk in fruit_keys:
        fruit_datasets_js.append(f"""{{
            label: '{fk.replace("_", " ").title()}',
            data: {fruit_series[fk]},
            borderColor: '{fruit_colors.get(fk, "#888")}',
            backgroundColor: 'transparent',
            borderWidth: 1.5,
            pointRadius: 0,
            tension: 0.3,
            hidden: true,
        }}""")

    # Build chi dataset JS
    chi_datasets_js = []
    for ck in chi_keys:
        chi_datasets_js.append(f"""{{
            label: '{ck} ({CHI_ANCHORS[ck].split(",")[0]})',
            data: {chi_series[ck]},
            borderColor: '{chi_colors.get(ck, "#888")}',
            backgroundColor: 'transparent',
            borderWidth: 1.5,
            pointRadius: 0,
            tension: 0.3,
            hidden: true,
        }}""")

    # V2 Structural panel
    v2 = hb_data.get('v2_structural', {})
    v2_panel_html = ""
    if v2 and 'error' not in v2:
        v2_fruits = v2.get('fruits', {})
        v2_bars = ""
        for fname, fdata in v2_fruits.items():
            sc = fdata.get('score', 0)
            pct = int((sc + 1) / 2 * 100)  # -1..+1 → 0..100
            color = '#6bcb77' if sc > 0.2 else '#ffd93d' if sc > -0.1 else '#ff6b6b'
            v2_bars += f"""<div style="display:flex;align-items:center;gap:8px;margin:3px 0;">
                <span style="width:100px;font-size:0.75rem;color:#888;text-transform:capitalize;">{fname}</span>
                <div style="flex:1;background:#1a1a1a;height:16px;border-radius:3px;overflow:hidden;">
                    <div style="width:{pct}%;height:100%;background:{color};border-radius:3px;"></div>
                </div>
                <span style="width:50px;font-family:'JetBrains Mono';font-size:0.75rem;color:{color};">{sc:+.3f}</span>
            </div>"""
        zones_info = ""
        if 'zones' in v2:
            z = v2['zones']
            zones_info = f"<div style='font-size:0.7rem;color:#555;margin-top:8px;'>Zones: theory={z.get('theory_words',0)}w, critique={z.get('critique_words',0)}w excluded</div>"

        v2_panel_html = f"""
        <div class="chart-section">
            <h2>Fruits Scorer v2 — Structural Invariants (Document-Level)</h2>
            <div class="cards" style="margin-bottom:12px;">
                <div class="card"><div class="label">Total</div><div class="value">{v2.get('total_score',0):+.2f}/12</div></div>
                <div class="card"><div class="label">Normalized</div><div class="value">{v2.get('normalized_score',0):.1f}/100</div></div>
                <div class="card"><div class="label">Grade</div><div class="value" style="font-size:2rem;">{v2.get('grade','?')}</div></div>
                <div class="card"><div class="label">Status</div><div class="value" style="font-size:0.8rem;">{v2.get('interpretation','')}</div></div>
            </div>
            {v2_bars}
            {zones_info}
        </div>"""

    # Top 5 peaks and valleys
    sorted_by_score = sorted(enumerate(heartbeat), key=lambda x: x[1]['combined'])
    top5 = sorted_by_score[-5:][::-1]
    bottom5 = sorted_by_score[:5]

    peaks_html = ""
    for idx, h in top5:
        peaks_html += f"""<tr>
            <td>{idx}</td>
            <td>{h['section'][:20]}</td>
            <td class="score high">{h['combined']:.4f}</td>
            <td class="fruit-tag">{h['fruit_dominant']}</td>
            <td class="chi-tag">{h['chi_dominant']}</td>
            <td class="text-cell">{h['text'][:120]}</td>
        </tr>"""

    valleys_html = ""
    for idx, h in bottom5:
        valleys_html += f"""<tr>
            <td>{idx}</td>
            <td>{h['section'][:20]}</td>
            <td class="score low">{h['combined']:.4f}</td>
            <td class="fruit-tag">{h['fruit_dominant']}</td>
            <td class="chi-tag">{h['chi_dominant']}</td>
            <td class="text-cell">{h['text'][:120]}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Heartbeat EKG — {paper_name}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation@3.0.1/dist/chartjs-plugin-annotation.min.js"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Crimson+Text:wght@400;600;700&family=Inter:wght@300;400;600&family=JetBrains+Mono:wght@400;600&family=Oswald:wght@400;600&display=swap');

:root {{
    --bg: #0a0a0a;
    --surface: #141414;
    --surface2: #1a1a1a;
    --gold: #d4af37;
    --gold-dim: rgba(212, 175, 55, 0.3);
    --text: #e8e8e8;
    --text-dim: #888;
    --green: #6bcb77;
    --red: #ff6b6b;
    --blue: #4d96ff;
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
    background: var(--bg);
    color: var(--text);
    font-family: 'Inter', sans-serif;
    line-height: 1.6;
}}

.container {{
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px;
}}

h1 {{
    font-family: 'Crimson Text', serif;
    color: var(--gold);
    font-size: 2rem;
    margin-bottom: 5px;
}}

.subtitle {{
    color: var(--text-dim);
    font-size: 0.85rem;
    margin-bottom: 20px;
}}

/* Summary cards */
.cards {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 12px;
    margin-bottom: 25px;
}}

.card {{
    background: var(--surface);
    border: 1px solid var(--gold-dim);
    border-radius: 8px;
    padding: 12px;
    text-align: center;
}}

.card .label {{
    font-size: 0.7rem;
    color: var(--text-dim);
    text-transform: uppercase;
    letter-spacing: 1px;
}}

.card .value {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.4rem;
    color: var(--gold);
    font-weight: 600;
}}

.card .value.positive {{ color: var(--green); }}
.card .value.negative {{ color: var(--red); }}

/* Chart containers */
.chart-section {{
    background: var(--surface);
    border: 1px solid var(--gold-dim);
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 20px;
}}

.chart-section h2 {{
    font-family: 'Oswald', sans-serif;
    color: var(--gold);
    font-size: 1.1rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 10px;
}}

.chart-wrapper {{
    position: relative;
    height: 300px;
}}

.chart-wrapper.tall {{
    height: 400px;
}}

/* Sentence inspector */
.inspector {{
    background: var(--surface2);
    border: 1px solid var(--gold-dim);
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 20px;
    min-height: 80px;
}}

.inspector h3 {{
    color: var(--gold);
    font-size: 0.9rem;
    margin-bottom: 8px;
}}

.inspector .sent-text {{
    font-family: 'Crimson Text', serif;
    font-size: 1.1rem;
    color: var(--text);
    margin-bottom: 8px;
}}

.inspector .sent-meta {{
    display: flex;
    gap: 20px;
    font-size: 0.8rem;
    color: var(--text-dim);
}}

.inspector .sent-meta span {{
    font-family: 'JetBrains Mono', monospace;
}}

/* Tables */
table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.8rem;
}}

th {{
    background: var(--surface2);
    color: var(--gold);
    padding: 8px 6px;
    text-align: left;
    font-family: 'Oswald', sans-serif;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 0.7rem;
}}

td {{
    padding: 6px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}}

.score {{ font-family: 'JetBrains Mono', monospace; font-weight: 600; }}
.score.high {{ color: var(--green); }}
.score.low {{ color: var(--red); }}
.fruit-tag {{ color: #ffd93d; }}
.chi-tag {{ color: #4d96ff; }}
.text-cell {{ color: var(--text-dim); font-size: 0.75rem; max-width: 400px; }}

/* Toggle buttons */
.toggle-row {{
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 10px;
}}

.toggle-btn {{
    background: var(--surface2);
    border: 1px solid var(--gold-dim);
    color: var(--text-dim);
    padding: 4px 10px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.75rem;
    font-family: 'Inter', sans-serif;
}}

.toggle-btn:hover {{ border-color: var(--gold); color: var(--text); }}
.toggle-btn.active {{ background: var(--gold); color: var(--bg); border-color: var(--gold); }}

.two-col {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}}

@media (max-width: 900px) {{
    .two-col {{ grid-template-columns: 1fr; }}
}}
</style>
</head>
<body>
<div class="container">

<h1>HEARTBEAT EKG — {paper_name}</h1>
<p class="subtitle">Sentence-level semantic alignment | {len(heartbeat)} sentences | SBERT all-MiniLM-L6-v2 | Theophysics Paper Intelligence L12</p>

<!-- Summary Cards -->
<div class="cards">
    <div class="card">
        <div class="label">Sentences</div>
        <div class="value">{len(heartbeat)}</div>
    </div>
    <div class="card">
        <div class="label">Fruit Mean</div>
        <div class="value {'positive' if summary.get('fruit_mean', 0) > 0 else 'negative'}">{summary.get('fruit_mean', 0):.4f}</div>
    </div>
    <div class="card">
        <div class="label">Chi Mean</div>
        <div class="value {'positive' if summary.get('chi_mean', 0) > 0 else 'negative'}">{summary.get('chi_mean', 0):.4f}</div>
    </div>
    <div class="card">
        <div class="label">Combined Mean</div>
        <div class="value {'positive' if summary.get('combined_mean', 0) > 0 else 'negative'}">{summary.get('combined_mean', 0):.4f}</div>
    </div>
    <div class="card">
        <div class="label">Fruit Std</div>
        <div class="value">{summary.get('fruit_std', 0):.4f}</div>
    </div>
    <div class="card">
        <div class="label">Chi Std</div>
        <div class="value">{summary.get('chi_std', 0):.4f}</div>
    </div>
    <div class="card">
        <div class="label">Sections</div>
        <div class="value">{len(boundaries)}</div>
    </div>
    <div class="card">
        <div class="label">Peak Score</div>
        <div class="value positive">{summary.get('peak_score', 0):.4f}</div>
    </div>
</div>

{v2_panel_html}

<!-- Sentence Inspector (updates on hover) -->
<div class="inspector" id="inspector">
    <h3>SENTENCE INSPECTOR — hover over any point on the charts</h3>
    <div class="sent-text" id="insp-text">Hover over a data point to inspect the sentence...</div>
    <div class="sent-meta">
        <div>Section: <span id="insp-section">—</span></div>
        <div>Index: <span id="insp-idx">—</span></div>
        <div>Combined: <span id="insp-combined">—</span></div>
        <div>Fruit: <span id="insp-fruit">—</span></div>
        <div>Chi: <span id="insp-chi">—</span></div>
    </div>
</div>

<!-- Main EKG Chart -->
<div class="chart-section">
    <h2>Combined Heartbeat Signal</h2>
    <div class="chart-wrapper tall">
        <canvas id="mainChart"></canvas>
    </div>
</div>

<!-- Fruit Detail Chart -->
<div class="chart-section">
    <h2>Fruits of the Spirit Channels</h2>
    <div class="toggle-row" id="fruitToggles"></div>
    <div class="chart-wrapper tall">
        <canvas id="fruitChart"></canvas>
    </div>
</div>

<!-- Chi Detail Chart -->
<div class="chart-section">
    <h2>Chi Variable Channels (Master Equation)</h2>
    <div class="toggle-row" id="chiToggles"></div>
    <div class="chart-wrapper tall">
        <canvas id="chiChart"></canvas>
    </div>
</div>

<!-- Peaks & Valleys -->
<div class="two-col">
    <div class="chart-section">
        <h2>Top 5 Peaks (Strongest Sentences)</h2>
        <table>
            <tr><th>#</th><th>Section</th><th>Score</th><th>Fruit</th><th>Chi</th><th>Text</th></tr>
            {peaks_html}
        </table>
    </div>
    <div class="chart-section">
        <h2>Top 5 Valleys (Weakest Sentences)</h2>
        <table>
            <tr><th>#</th><th>Section</th><th>Score</th><th>Fruit</th><th>Chi</th><th>Text</th></tr>
            {valleys_html}
        </table>
    </div>
</div>

</div>

<script>
const labels = {labels_json};
const combinedData = {combined_data};
const smoothedData = {smoothed_data};
const fruitData = {fruit_data};
const chiData = {chi_data};
const structuralData = {structural_data};
const sentTexts = {texts_json};
const sentSections = {sections_json};
const sentFruitDom = {fruit_dom_json};
const sentChiDom = {chi_dom_json};
const annotations = {annotations_json};

// Inspector update function
function updateInspector(idx) {{
    if (idx < 0 || idx >= sentTexts.length) return;
    document.getElementById('insp-text').textContent = sentTexts[idx];
    document.getElementById('insp-section').textContent = sentSections[idx];
    document.getElementById('insp-idx').textContent = idx;
    document.getElementById('insp-combined').textContent = combinedData[idx].toFixed(4);
    document.getElementById('insp-fruit').textContent = sentFruitDom[idx];
    document.getElementById('insp-chi').textContent = sentChiDom[idx];
}}

// Common chart options
const commonOpts = {{
    responsive: true,
    maintainAspectRatio: false,
    interaction: {{
        mode: 'index',
        intersect: false,
    }},
    onHover: (evt, elements) => {{
        if (elements.length > 0) {{
            updateInspector(elements[0].index);
        }}
    }},
    onClick: (evt, elements) => {{
        if (elements.length > 0) {{
            updateInspector(elements[0].index);
        }}
    }},
    plugins: {{
        legend: {{
            labels: {{ color: '#888', font: {{ family: 'Inter', size: 11 }} }}
        }},
        tooltip: {{
            backgroundColor: '#1a1a1a',
            titleColor: '#d4af37',
            bodyColor: '#e8e8e8',
            borderColor: 'rgba(212,175,55,0.3)',
            borderWidth: 1,
            callbacks: {{
                afterBody: function(ctx) {{
                    const idx = ctx[0].dataIndex;
                    return sentTexts[idx].substring(0, 100) + '...';
                }}
            }}
        }},
    }},
    scales: {{
        x: {{
            display: true,
            grid: {{ color: 'rgba(255,255,255,0.03)' }},
            ticks: {{ color: '#555', maxTicksLimit: 20, font: {{ size: 10 }} }},
            title: {{ display: true, text: 'Sentence Index', color: '#888' }},
        }},
        y: {{
            grid: {{ color: 'rgba(212,175,55,0.1)' }},
            ticks: {{ color: '#888', font: {{ family: 'JetBrains Mono', size: 10 }} }},
            title: {{ display: true, text: 'Net Score (pos - neg)', color: '#888' }},
        }}
    }}
}};

// Zero line reference
const zeroLine = {{
    type: 'line',
    yMin: 0, yMax: 0,
    borderColor: 'rgba(255,255,255,0.2)',
    borderWidth: 1,
    borderDash: [3, 3],
}};

// ── MAIN CHART ──
new Chart(document.getElementById('mainChart'), {{
    type: 'line',
    data: {{
        labels: labels,
        datasets: [
            {{
                label: 'Combined (raw)',
                data: combinedData,
                borderColor: 'rgba(212, 175, 55, 0.3)',
                backgroundColor: 'transparent',
                borderWidth: 1,
                pointRadius: 0,
                tension: 0.2,
            }},
            {{
                label: 'Combined (smoothed)',
                data: smoothedData,
                borderColor: '#d4af37',
                backgroundColor: 'transparent',
                borderWidth: 2.5,
                pointRadius: 0,
                tension: 0.3,
            }},
            {{
                label: 'Fruit Composite',
                data: fruitData,
                borderColor: '#6bcb77',
                backgroundColor: 'transparent',
                borderWidth: 1.5,
                pointRadius: 0,
                tension: 0.3,
                hidden: true,
            }},
            {{
                label: 'Chi Composite',
                data: chiData,
                borderColor: '#4d96ff',
                backgroundColor: 'transparent',
                borderWidth: 1.5,
                pointRadius: 0,
                tension: 0.3,
                hidden: true,
            }},
            {{
                label: 'Structural (v2)',
                data: structuralData,
                borderColor: '#ff6b6b',
                backgroundColor: 'transparent',
                borderWidth: 1.5,
                pointRadius: 0,
                tension: 0.1,
                stepped: 'middle',
                yAxisID: 'y2',
                hidden: true,
            }},
        ]
    }},
    options: {{
        ...commonOpts,
        scales: {{
            ...commonOpts.scales,
            y2: {{
                position: 'right',
                grid: {{ display: false }},
                ticks: {{ color: '#ff6b6b', font: {{ size: 10 }} }},
                title: {{ display: true, text: 'Structural Hits', color: '#ff6b6b' }},
            }}
        }},
        plugins: {{
            ...commonOpts.plugins,
            annotation: {{
                annotations: [...annotations, zeroLine]
            }}
        }}
    }}
}});

// ── FRUIT CHART ──
const fruitChart = new Chart(document.getElementById('fruitChart'), {{
    type: 'line',
    data: {{
        labels: labels,
        datasets: [
            {{
                label: 'Fruit Composite',
                data: fruitData,
                borderColor: '#d4af37',
                backgroundColor: 'transparent',
                borderWidth: 2,
                pointRadius: 0,
                tension: 0.3,
            }},
            {','.join(fruit_datasets_js)}
        ]
    }},
    options: {{
        ...commonOpts,
        plugins: {{
            ...commonOpts.plugins,
            annotation: {{ annotations: [zeroLine] }}
        }}
    }}
}});

// Fruit toggle buttons
const fruitKeys = {json.dumps(fruit_keys)};
const fruitToggleContainer = document.getElementById('fruitToggles');
fruitKeys.forEach((fk, i) => {{
    const btn = document.createElement('button');
    btn.className = 'toggle-btn';
    btn.textContent = fk.replace('_', ' ');
    btn.onclick = () => {{
        const dsIdx = i + 1; // +1 because composite is index 0
        const meta = fruitChart.getDatasetMeta(dsIdx);
        meta.hidden = !meta.hidden;
        btn.classList.toggle('active');
        fruitChart.update();
    }};
    fruitToggleContainer.appendChild(btn);
}});

// ── CHI CHART ──
const chiChart = new Chart(document.getElementById('chiChart'), {{
    type: 'line',
    data: {{
        labels: labels,
        datasets: [
            {{
                label: 'Chi Composite',
                data: chiData,
                borderColor: '#d4af37',
                backgroundColor: 'transparent',
                borderWidth: 2,
                pointRadius: 0,
                tension: 0.3,
            }},
            {','.join(chi_datasets_js)}
        ]
    }},
    options: {{
        ...commonOpts,
        plugins: {{
            ...commonOpts.plugins,
            annotation: {{ annotations: [zeroLine] }}
        }}
    }}
}});

// Chi toggle buttons
const chiKeys = {json.dumps(chi_keys)};
const chiNames = {json.dumps([CHI_ANCHORS[k].split(',')[0] for k in chi_keys])};
const chiToggleContainer = document.getElementById('chiToggles');
chiKeys.forEach((ck, i) => {{
    const btn = document.createElement('button');
    btn.className = 'toggle-btn';
    btn.textContent = ck + ' — ' + chiNames[i];
    btn.onclick = () => {{
        const dsIdx = i + 1;
        const meta = chiChart.getDatasetMeta(dsIdx);
        meta.hidden = !meta.hidden;
        btn.classList.toggle('active');
        chiChart.update();
    }};
    chiToggleContainer.appendChild(btn);
}});
</script>
</body>
</html>"""

    return html


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

if __name__ == '__main__':
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python heartbeat_analyzer.py <paper.md> [--html output.html] [--json output.json]")
        sys.exit(1)

    paper = sys.argv[1]
    print(f"Analyzing: {paper}")
    result = analyze(paper)

    if 'heartbeat_error' in result:
        print(f"ERROR: {result['heartbeat_error']}")
        sys.exit(1)

    print(f"  Sentences: {result['sentence_count']}")
    print(f"  Sections:  {len(result['section_boundaries'])}")
    print(f"  Fruit mean: {result['summary']['fruit_mean']:.4f}")
    print(f"  Chi mean:   {result['summary']['chi_mean']:.4f}")
    print(f"  Combined:   {result['summary']['combined_mean']:.4f}")
    print(f"  Peak [{result['summary']['peak_sentence']}]: {result['summary']['peak_score']:.4f}")
    print(f"  Valley [{result['summary']['valley_sentence']}]: {result['summary']['valley_score']:.4f}")

    # Output HTML
    if '--html' in sys.argv:
        idx = sys.argv.index('--html')
        html_path = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else 'heartbeat.html'
        name = Path(paper).stem
        html = generate_heartbeat_html(result, paper_name=name)
        Path(html_path).write_text(html, encoding='utf-8')
        print(f"  HTML: {html_path}")

    # Output JSON
    if '--json' in sys.argv:
        idx = sys.argv.index('--json')
        json_path = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else 'heartbeat.json'
        Path(json_path).write_text(json.dumps(result, indent=2, default=str), encoding='utf-8')
        print(f"  JSON: {json_path}")

    # Default: just print summary
    if '--html' not in sys.argv and '--json' not in sys.argv:
        print(json.dumps(result['summary'], indent=2))
