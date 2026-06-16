"""
L1: TEXT ANALYTICS (v2)
textstat (10 readability formulas) + KeyBERT + YAKE + N-grams
"""
import re
import os
from pathlib import Path
from collections import Counter

try:
    import textstat
    HAS_TEXTSTAT = True
except ImportError:
    HAS_TEXTSTAT = False

try:
    import yake
    HAS_YAKE = True
except ImportError:
    HAS_YAKE = False

# KeyBERT lazy-loaded to avoid import-time model crash
HAS_KEYBERT = False
kw_model = None

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

def _get_keybert():
    global HAS_KEYBERT, kw_model
    if kw_model is not None:
        return kw_model
    try:
        from keybert import KeyBERT
        from sentence_transformers import SentenceTransformer
        CACHE = Path(r"O:\999_IGNORE\Obsidian Programs\Python_Backend\core\truth_engine\model_cache")
        st_model = SentenceTransformer(
            "all-MiniLM-L6-v2",
            cache_folder=str(CACHE),
            local_files_only=True,
        )
        kw_model = KeyBERT(model=st_model)
        HAS_KEYBERT = True
    except Exception as e:
        kw_model = None
        HAS_KEYBERT = False
    return kw_model


def strip_markdown(text):
    clean = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    clean = re.sub(r'\*{1,3}([^*]+)\*{1,3}', r'\1', clean)
    clean = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', clean)
    clean = re.sub(r'`[^`]+`', '', clean)
    clean = re.sub(r'!\[.*?\]\(.*?\)', '', clean)
    clean = re.sub(r'\n{3,}', '\n\n', clean)
    return clean.strip()


def readability_suite(text):
    if not HAS_TEXTSTAT:
        return {}
    return {
        'flesch_reading_ease':   round(textstat.flesch_reading_ease(text), 1),
        'flesch_kincaid_grade':  round(textstat.flesch_kincaid_grade(text), 1),
        'gunning_fog':           round(textstat.gunning_fog(text), 1),
        'smog_index':            round(textstat.smog_index(text), 1),
        'automated_readability': round(textstat.automated_readability_index(text), 1),
        'coleman_liau':          round(textstat.coleman_liau_index(text), 1),
        'dale_chall':            round(textstat.dale_chall_readability_score(text), 1),
        'text_standard':         textstat.text_standard(text),
        'reading_time_min':      round(textstat.reading_time(text, ms_per_char=14.69)/60, 1),
        'syllable_count':        textstat.syllable_count(text),
        'lexicon_count':         textstat.lexicon_count(text, removepunct=True),
        'sentence_count':        textstat.sentence_count(text),
    }


def keybert_keywords(text, top_n=12):
    model = _get_keybert()
    if not model:
        return []
    try:
        kws = model.extract_keywords(
            text, keyphrase_ngram_range=(1, 2),
            stop_words='english', top_n=top_n
        )
        return [f"{kw}({round(s,3)})" for kw, s in kws]
    except Exception:
        return []


def yake_keywords(text, top_n=12):
    if not HAS_YAKE:
        return []
    try:
        ext = yake.KeywordExtractor(lan='en', n=2, dedupLim=0.7, top=top_n)
        return [f"{kw}({round(s,4)})" for kw, s in ext.extract_keywords(text)]
    except Exception:
        return []


def ngrams(text, n=2, top=8):
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    stop = {'this','that','with','have','from','they','been','were','their','what',
            'when','which','there','will','would','could','should','about','into',
            'than','then','each','also','more','some','only','other','these','very'}
    words = [w for w in words if w not in stop]
    grams = [' '.join(words[i:i+n]) for i in range(len(words)-n+1)]
    return [g for g,_ in Counter(grams).most_common(top)]


def analyze(path_or_text, is_path=True):
    if is_path:
        text = Path(path_or_text).read_text(encoding='utf-8', errors='ignore')
        fname = Path(path_or_text).name
    else:
        text = path_or_text
        fname = 'inline'

    clean = strip_markdown(text)
    words = clean.split()
    paragraphs = [p.strip() for p in clean.split('\n\n') if len(p.strip()) > 30]
    headers = re.findall(r'^#{1,4} .+', text, re.MULTILINE)
    unique = set(w.lower().strip('.,;:!?"\'') for w in words if len(w) > 2)

    result = {
        'file': fname,
        'word_count': len(words),
        'unique_word_count': len(unique),
        'vocab_richness': round(len(unique)/max(len(words),1), 4),
        'paragraph_count': len(paragraphs),
        'header_count': len(headers),
        'avg_paragraph_words': round(len(words)/max(len(paragraphs),1), 1),
    }
    result.update(readability_suite(clean))
    result['keybert_keywords'] = ' | '.join(keybert_keywords(clean))
    result['yake_keywords'] = ' | '.join(yake_keywords(clean))
    result['top_bigrams'] = ' | '.join(ngrams(clean, 2, 6))
    result['top_trigrams'] = ' | '.join(ngrams(clean, 3, 4))
    return result


if __name__ == '__main__':
    import sys, json
    if len(sys.argv) > 1:
        r = analyze(sys.argv[1])
        print(json.dumps(r, indent=2))
