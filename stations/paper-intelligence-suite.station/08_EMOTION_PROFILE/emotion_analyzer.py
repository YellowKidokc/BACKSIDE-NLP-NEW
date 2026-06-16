"""
L8 — EMOTION PROFILE
====================
Two-channel emotion analysis:
  Channel A: NRCLex (lexicon-based, 8 Plutchik emotions)
  Channel B: GoEmotions (BERT-based, 27 fine-grained emotions)

Maps both channels to Fruits of the Spirit alignment scores.

Fruits mapping rationale:
  Love      ← love, caring, admiration
  Joy       ← joy, amusement, excitement, optimism
  Peace     ← relief, neutral (low arousal)
  Patience  ← 1 - (anger + annoyance)  [inverse of impatience signals]
  Kindness  ← caring, approval, gratitude
  Goodness  ← admiration, approval, gratitude
  Faithfulness ← trust (NRC), 1 - (confusion + nervousness)
  Gentleness   ← caring, 1 - (anger + disgust + annoyance)
  Self-control ← 1 - (anger + desire + annoyance + disgust)

Anti-fruit signals:
  Hatred    ← anger, disgust, disapproval
  Despair   ← sadness, grief, disappointment
  Conflict  ← anger, annoyance, disapproval
  Impatience ← anger, annoyance
  Cruelty   ← disgust, disapproval, anger
  Corruption ← disgust, disapproval
  Betrayal  ← disappointment, disapproval, anger
  Harshness ← anger, annoyance, disgust
  Indulgence ← desire, amusement (without self-control signals)
"""
import re
import os
from pathlib import Path

# ---------- NRCLex (Channel A) ----------
try:
    from nrclex import NRCLex
    HAS_NRCLEX = True
except ImportError:
    HAS_NRCLEX = False

# ---------- GoEmotions (Channel B) ----------
_goemotions_pipe = None

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

def _get_goemotions():
    global _goemotions_pipe
    if _goemotions_pipe is None:
        from transformers import pipeline
        _goemotions_pipe = pipeline(
            'text-classification',
            model='monologg/bert-base-cased-goemotions-original',
            top_k=None,
            device=-1,
            batch_size=16,
            local_files_only=True,
        )
    return _goemotions_pipe


# 27 GoEmotions labels
GOEMOTIONS_LABELS = [
    'admiration', 'amusement', 'anger', 'annoyance', 'approval', 'caring',
    'confusion', 'curiosity', 'desire', 'disappointment', 'disapproval',
    'disgust', 'embarrassment', 'excitement', 'fear', 'gratitude', 'grief',
    'joy', 'love', 'nervousness', 'optimism', 'pride', 'realization',
    'relief', 'remorse', 'sadness', 'surprise', 'neutral'
]

# ═══════════════════════════════════════════════════════════════
# FRUITS OF THE SPIRIT ← GoEmotions BLENDED MAPPING
# ═══════════════════════════════════════════════════════════════
# Each fruit is scored as:
#   fruit = (positive_avg * 0.6) + ((1 - negative_avg) * 0.4)
#
# This means you need BOTH:
#   - Active presence of the positive signals (60%)
#   - Absence of the opposing signals (40%)
#
# Theological grounding for each mapping:
#
# LOVE (agape) — self-sacrificial, unconditional
#   Positive: love, caring, admiration, gratitude
#   Negative: anger, disgust, disapproval
#
# JOY (chara) — deep gladness rooted in truth
#   Positive: joy, optimism, excitement, pride, gratitude
#   Negative: sadness, grief, disappointment
#
# PEACE (eirene/shalom) — wholeness, harmony, inner stillness
#   Positive: relief, approval, realization, gratitude
#   Negative: anger, fear, nervousness, annoyance
#
# PATIENCE (makrothumia) — long-suffering, endurance under trial
#   Positive: caring, approval, relief, optimism
#   Negative: anger, annoyance, disappointment, disgust
#
# KINDNESS (chrestotes) — active benevolence, useful goodness
#   Positive: caring, approval, gratitude, love
#   Negative: disgust, disapproval, anger, annoyance
#
# GOODNESS (agathosune) — moral excellence, generosity
#   Positive: admiration, approval, gratitude, optimism
#   Negative: disgust, disapproval, anger
#
# FAITHFULNESS (pistis) — reliability, steadfast conviction
#   Positive: realization, approval, admiration, optimism
#   Negative: confusion, nervousness, fear, embarrassment
#
# GENTLENESS (prautes) — meekness = strength under control
#   Positive: caring, love, relief, approval
#   Negative: anger, annoyance, disgust, pride
#
# SELF-CONTROL (egkrateia) — mastery over impulses
#   Positive: realization, approval, relief
#   Negative: desire, anger, annoyance, disgust, excitement
# ═══════════════════════════════════════════════════════════════

FRUIT_BLEND = {
    'love': {
        'positive': ['love', 'caring', 'admiration', 'gratitude'],
        'negative': ['anger', 'disgust', 'disapproval'],
    },
    'joy': {
        'positive': ['joy', 'optimism', 'excitement', 'pride', 'gratitude'],
        'negative': ['sadness', 'grief', 'disappointment'],
    },
    'peace': {
        'positive': ['relief', 'approval', 'realization', 'gratitude'],
        'negative': ['anger', 'fear', 'nervousness', 'annoyance'],
    },
    'patience': {
        'positive': ['caring', 'approval', 'relief', 'optimism'],
        'negative': ['anger', 'annoyance', 'disappointment', 'disgust'],
    },
    'kindness': {
        'positive': ['caring', 'approval', 'gratitude', 'love'],
        'negative': ['disgust', 'disapproval', 'anger', 'annoyance'],
    },
    'goodness': {
        'positive': ['admiration', 'approval', 'gratitude', 'optimism'],
        'negative': ['disgust', 'disapproval', 'anger'],
    },
    'faithfulness': {
        'positive': ['realization', 'approval', 'admiration', 'optimism'],
        'negative': ['confusion', 'nervousness', 'fear', 'embarrassment'],
    },
    'gentleness': {
        'positive': ['caring', 'love', 'relief', 'approval'],
        'negative': ['anger', 'annoyance', 'disgust', 'pride'],
    },
    'self_control': {
        'positive': ['realization', 'approval', 'relief'],
        'negative': ['desire', 'anger', 'annoyance', 'disgust', 'excitement'],
    },
}

# Anti-fruits: direct opposition to each fruit
# These are scored purely from negative emotion presence
ANTI_FRUIT_MAP = {
    'hatred':      ['anger', 'disgust', 'disapproval'],         # vs love
    'despair':     ['sadness', 'grief', 'disappointment'],       # vs joy
    'conflict':    ['anger', 'annoyance', 'fear', 'nervousness'],# vs peace
    'impatience':  ['anger', 'annoyance', 'disappointment'],     # vs patience
    'cruelty':     ['disgust', 'disapproval', 'anger', 'annoyance'], # vs kindness
    'corruption':  ['disgust', 'disapproval', 'anger'],          # vs goodness
    'betrayal':    ['confusion', 'nervousness', 'disappointment', 'fear'], # vs faithfulness
    'harshness':   ['anger', 'annoyance', 'disgust'],            # vs gentleness
    'indulgence':  ['desire', 'excitement', 'anger', 'annoyance'], # vs self-control
}


def _split_sentences(text: str, max_len=350) -> list[str]:
    """Split text into sentence-ish chunks for the model (max 512 tokens).
    Using 350 chars to stay safely under the token limit even with dense text."""
    raw = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    buf = ""
    for s in raw:
        if len(buf) + len(s) > max_len:
            if buf:
                chunks.append(buf.strip())
            buf = s
        else:
            buf = buf + " " + s if buf else s
    if buf:
        chunks.append(buf.strip())
    return [c for c in chunks if len(c) > 20]


def analyze(paper_path: str) -> dict:
    text = Path(paper_path).read_text(encoding='utf-8', errors='replace')
    # Strip markdown headers/frontmatter for cleaner analysis
    text = re.sub(r'^---.*?---', '', text, flags=re.DOTALL)
    text = re.sub(r'#+\s+', '', text)
    text = re.sub(r'\|[^\n]+\|', '', text)  # strip tables
    text = re.sub(r'\s+', ' ', text).strip()

    result = {}

    # ── Channel A: NRCLex (Plutchik) ──
    if HAS_NRCLEX:
        try:
            nrc = NRCLex()
            nrc.load_raw_text(text)
            freqs = nrc.affect_frequencies
            for emo in ['fear', 'anger', 'anticipation', 'trust', 'surprise',
                         'positive', 'negative', 'sadness', 'disgust', 'joy']:
                result[f'nrc_{emo}'] = round(freqs.get(emo, 0), 4)

            # NRC top emotions
            top = sorted(freqs.items(), key=lambda x: -x[1])
            result['nrc_top_emotions'] = ', '.join(f"{e}:{v:.3f}" for e, v in top[:5] if v > 0)
        except Exception as e:
            result['nrc_status'] = f'fallback: {e}'
            for emo in ['fear', 'anger', 'anticipation', 'trust', 'surprise',
                         'positive', 'negative', 'sadness', 'disgust', 'joy']:
                result[f'nrc_{emo}'] = 0
            result['nrc_top_emotions'] = ''
    else:
        result['nrc_status'] = 'fallback: NRCLex not installed'
        for emo in ['fear', 'anger', 'anticipation', 'trust', 'surprise',
                     'positive', 'negative', 'sadness', 'disgust', 'joy']:
            result[f'nrc_{emo}'] = 0
        result['nrc_top_emotions'] = ''

    # ── Channel B: GoEmotions (27 emotions) ──
    try:
        pipe = _get_goemotions()
        sentences = _split_sentences(text)
        if not sentences:
            raise ValueError('no sentences found')

        # Aggregate across all sentences
        totals = {label: 0.0 for label in GOEMOTIONS_LABELS}
        n = len(sentences)

        for batch_start in range(0, n, 16):
            batch = sentences[batch_start:batch_start+16]
            results_batch = pipe(batch)
            for sent_result in results_batch:
                for item in sent_result:
                    totals[item['label']] += item['score']

        # Average across sentences
        for label in GOEMOTIONS_LABELS:
            result[f'emo_{label}'] = round(totals[label] / n, 4)

        # Top emotions
        sorted_emos = sorted(
            [(l, totals[l]/n) for l in GOEMOTIONS_LABELS if l != 'neutral'],
            key=lambda x: -x[1]
        )
        result['emo_top_5'] = ', '.join(f"{e}:{v:.3f}" for e, v in sorted_emos[:5])
        result['emo_dominant'] = sorted_emos[0][0] if sorted_emos else ''
        result['emo_sentence_count'] = n

        # ── Fruits of the Spirit alignment (BLENDED FORMULA) ──
        # fruit = (positive_signal_avg * 0.6) + ((1 - negative_signal_avg) * 0.4)
        # This requires BOTH active presence of virtue AND absence of vice.
        avgs = {l: totals[l]/n for l in GOEMOTIONS_LABELS}

        POS_WEIGHT = 0.6
        NEG_WEIGHT = 0.4

        for fruit, channels in FRUIT_BLEND.items():
            pos_signals = channels['positive']
            neg_signals = channels['negative']

            # Average of positive emotion signals (how much virtue is PRESENT)
            pos_avg = sum(avgs.get(s, 0) for s in pos_signals) / len(pos_signals) if pos_signals else 0

            # Average of negative emotion signals (how much vice is PRESENT)
            neg_avg = sum(avgs.get(s, 0) for s in neg_signals) / len(neg_signals) if neg_signals else 0

            # Blended: need both presence of good AND absence of bad
            blended = (pos_avg * POS_WEIGHT) + ((1.0 - neg_avg) * NEG_WEIGHT)

            result[f'fruit_emo_{fruit}'] = round(blended, 4)

            # Also store the raw components for transparency
            result[f'fruit_emo_{fruit}_pos'] = round(pos_avg, 4)
            result[f'fruit_emo_{fruit}_neg'] = round(neg_avg, 4)

        # Anti-fruit scores (direct negative emotion presence)
        for anti, sources in ANTI_FRUIT_MAP.items():
            result[f'anti_emo_{anti}'] = round(
                sum(avgs.get(s, 0) for s in sources) / len(sources), 4)

        # Composite scores
        fruit_vals = [result.get(f'fruit_emo_{f}', 0) for f in FRUIT_BLEND]
        anti_vals = [result.get(f'anti_emo_{a}', 0) for a in ANTI_FRUIT_MAP]
        result['fruit_emo_composite'] = round(sum(fruit_vals) / len(fruit_vals), 4)
        result['anti_emo_composite'] = round(sum(anti_vals) / len(anti_vals), 4)
        result['fruit_emo_net'] = round(
            result['fruit_emo_composite'] - result['anti_emo_composite'], 4)

        # Strongest and weakest fruit
        fruit_ranked = sorted(
            [(f, result.get(f'fruit_emo_{f}', 0)) for f in FRUIT_BLEND],
            key=lambda x: -x[1]
        )
        result['fruit_emo_strongest'] = fruit_ranked[0][0] if fruit_ranked else ''
        result['fruit_emo_weakest'] = fruit_ranked[-1][0] if fruit_ranked else ''

    except Exception as e:
        result['goemotions_status'] = f'fallback: {e}'

        # Deterministic fallback for Docker/public runs where the heavier
        # GoEmotions model is not cached. It preserves the fruit/anti-fruit
        # columns using the NRC lexicon channel, so the layer still produces
        # auditable scores instead of failing the whole paper.
        trust = result.get('nrc_trust', 0)
        positive = result.get('nrc_positive', 0)
        joy = result.get('nrc_joy', 0)
        anticipation = result.get('nrc_anticipation', 0)
        anger = result.get('nrc_anger', 0)
        fear = result.get('nrc_fear', 0)
        sadness = result.get('nrc_sadness', 0)
        disgust = result.get('nrc_disgust', 0)
        negative = result.get('nrc_negative', 0)

        fruit_seed = {
            'love': (positive + trust) / 2,
            'joy': (joy + positive) / 2,
            'peace': max(0, positive - ((anger + fear) / 2)),
            'patience': max(0, trust - anger),
            'kindness': (positive + trust) / 2,
            'goodness': positive,
            'faithfulness': trust,
            'gentleness': max(0, trust - ((anger + disgust) / 2)),
            'self_control': max(0, trust - ((anger + anticipation) / 2)),
        }
        anti_seed = {
            'hatred': (anger + disgust + negative) / 3,
            'despair': (sadness + fear + negative) / 3,
            'conflict': (anger + fear + negative) / 3,
            'impatience': anger,
            'cruelty': (anger + disgust) / 2,
            'corruption': disgust,
            'betrayal': (sadness + negative) / 2,
            'harshness': anger,
            'indulgence': anticipation,
        }
        for fruit, value in fruit_seed.items():
            result[f'fruit_emo_{fruit}'] = round(value, 4)
            result[f'fruit_emo_{fruit}_pos'] = round(value, 4)
            result[f'fruit_emo_{fruit}_neg'] = round(1 - value, 4)
        for anti, value in anti_seed.items():
            result[f'anti_emo_{anti}'] = round(value, 4)

        fruit_vals = [result.get(f'fruit_emo_{f}', 0) for f in FRUIT_BLEND]
        anti_vals = [result.get(f'anti_emo_{a}', 0) for a in ANTI_FRUIT_MAP]
        result['fruit_emo_composite'] = round(sum(fruit_vals) / len(fruit_vals), 4)
        result['anti_emo_composite'] = round(sum(anti_vals) / len(anti_vals), 4)
        result['fruit_emo_net'] = round(
            result['fruit_emo_composite'] - result['anti_emo_composite'], 4)
        result['emo_dominant'] = result.get('nrc_top_emotions', '').split(':', 1)[0]
        result['emo_top_5'] = result.get('nrc_top_emotions', '')
        fruit_ranked = sorted(
            [(f, result.get(f'fruit_emo_{f}', 0)) for f in FRUIT_BLEND],
            key=lambda x: -x[1]
        )
        result['fruit_emo_strongest'] = fruit_ranked[0][0] if fruit_ranked else ''
        result['fruit_emo_weakest'] = fruit_ranked[-1][0] if fruit_ranked else ''

    return result


if __name__ == '__main__':
    import sys, json
    if len(sys.argv) > 1:
        r = analyze(sys.argv[1])
        print(json.dumps(r, indent=2))
    else:
        print("Usage: python emotion_analyzer.py <paper.md>")
