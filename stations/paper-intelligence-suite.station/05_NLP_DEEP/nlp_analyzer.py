"""
L5: NLP DEEP ANALYZER
======================
Named entities (spacy), topic modeling (gensim LDA across corpus),
key sentence extraction (sumy TextRank).
"""
import re
from pathlib import Path

try:
    import spacy
    nlp = spacy.load('en_core_web_sm')
    HAS_SPACY = True
except Exception:
    HAS_SPACY = False; nlp = None

try:
    from sumy.parsers.plaintext import PlaintextParser
    from sumy.nlp.tokenizers import Tokenizer
    from sumy.summarizers.text_rank import TextRankSummarizer
    HAS_SUMY = True
except Exception:
    HAS_SUMY = False

try:
    from gensim import corpora, models
    import numpy as np
    HAS_GENSIM = True
except Exception:
    HAS_GENSIM = False

STOPWORDS = {
    'the','a','an','is','are','was','were','be','been','have','has','had',
    'do','does','did','will','would','shall','should','may','might','can',
    'could','that','this','these','those','it','its','i','we','you','they',
    'he','she','and','or','but','not','so','for','of','in','on','at','to',
    'from','with','by','about','into','through','over','after','also',
    'which','when','what','where','how','their','there','then','than',
    'more','some','only','such','very','just','been','each','like',
}

def strip_md(text):
    t = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    t = re.sub(r'\*{1,3}([^*]+)\*{1,3}', r'\1', t)
    t = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', t)
    return re.sub(r'`[^`]+`', '', t).strip()

def tokenize(text):
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    return [w for w in words if w not in STOPWORDS]

def extract_entities(text):
    if not HAS_SPACY or not nlp: return {}, 0
    doc = nlp(text[:40000])
    ents = {}
    for ent in doc.ents:
        ents.setdefault(ent.label_, [])
        if ent.text not in ents[ent.label_]:
            ents[ent.label_].append(ent.text)
    return ents, len(doc.ents)

def extract_key_sentences(text, n=3):
    if not HAS_SUMY:
        sents = [s.strip() for s in re.split(r'[.!?]', text) if len(s.strip()) > 60]
        return sents[:n]
    try:
        parser = PlaintextParser.from_string(text, Tokenizer('english'))
        return [str(s) for s in TextRankSummarizer()(parser.document, n)]
    except Exception:
        return []

# Corpus-level topic model — built once, reused per paper
_lda_model = None
_dictionary = None

def build_corpus_model(all_texts, num_topics=5, num_words=6):
    global _lda_model, _dictionary
    if not HAS_GENSIM: return
    try:
        all_tokens = [tokenize(t) for t in all_texts]
        _dictionary = corpora.Dictionary(all_tokens)
        _dictionary.filter_extremes(no_below=2, no_above=0.9, keep_n=2000)
        if len(_dictionary) < 10: return
        corpus = [_dictionary.doc2bow(t) for t in all_tokens]
        _lda_model = models.LdaModel(
            corpus, num_topics=num_topics, id2word=_dictionary,
            passes=10, random_state=42, alpha='auto'
        )
        print(f"  L5 corpus model: {num_topics} topics, {len(_dictionary)} terms")
    except Exception as e:
        print(f"  L5 topic model err: {e}")

def get_paper_topics(text, top_n=3):
    if not HAS_GENSIM or not _lda_model or not _dictionary: return []
    try:
        tokens = tokenize(text)
        bow = _dictionary.doc2bow(tokens)
        topic_dist = _lda_model.get_document_topics(bow, minimum_probability=0.05)
        topic_dist.sort(key=lambda x: -x[1])
        topics = []
        for topic_id, prob in topic_dist[:top_n]:
            words = [w for w,_ in _lda_model.show_topic(topic_id, topn=5)]
            topics.append(', '.join(words))
        return topics
    except Exception:
        return []

def analyze(path_or_text, is_path=True):
    if is_path:
        text = Path(path_or_text).read_text(encoding='utf-8', errors='ignore')
        fname = Path(path_or_text).name
    else:
        text = path_or_text; fname = 'inline'
    clean = strip_md(text)
    result = {'file': fname}

    ents, total = extract_entities(clean)
    result['entity_count'] = total
    result['entity_people'] = ', '.join(ents.get('PERSON',[])[:5])
    result['entity_orgs'] = ', '.join(ents.get('ORG',[])[:5])
    result['entity_concepts'] = ', '.join((ents.get('NORP',[]) + ents.get('LAW',[]))[:4])
    result['entity_types_found'] = ', '.join(ents.keys())

    sents = extract_key_sentences(clean, n=3)
    for i, s in enumerate(sents[:3], 1):
        result[f'key_sentence_{i}'] = s[:200]

    topics = get_paper_topics(clean)
    for i, t in enumerate(topics[:3], 1):
        result[f'topic_{i}'] = t
    result['topic_count'] = len(topics)
    return result

if __name__ == '__main__':
    import sys, json
    if len(sys.argv) > 1:
        print(json.dumps(analyze(sys.argv[1]), indent=2))
