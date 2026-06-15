"""
L9 — LINGUISTIC DEPTH
=====================
Comprehensive linguistic analysis using textdescriptives + lexicalrichness.

Outputs:
  - Sentence-level coherence (1st and 2nd order semantic similarity)
  - Dependency distance (syntactic complexity)
  - POS proportions (noun-heavy = academic, verb-heavy = narrative)
  - Vocabulary diversity (MTLD, MATTR, HD-D)
  - Information density metrics
"""
import re
from pathlib import Path

try:
    import spacy
    import textdescriptives as td
    HAS_TD = True
except ImportError:
    HAS_TD = False

try:
    from lexicalrichness import LexicalRichness
    HAS_LR = True
except ImportError:
    HAS_LR = False


_nlp = None

def _get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load('en_core_web_sm')
        # Add individual components (skip 'quality' which has a config bug)
        for component in ['textdescriptives/coherence',
                          'textdescriptives/readability',
                          'textdescriptives/dependency_distance',
                          'textdescriptives/pos_proportions',
                          'textdescriptives/descriptive_stats']:
            try:
                _nlp.add_pipe(component, config={}, last=True)
            except Exception:
                pass
    return _nlp


def analyze(paper_path: str) -> dict:
    text = Path(paper_path).read_text(encoding='utf-8', errors='replace')
    # Clean markdown
    text = re.sub(r'^---.*?---', '', text, flags=re.DOTALL)
    text = re.sub(r'#+\s+', '', text)
    text = re.sub(r'\|[^\n]+\|', '', text)
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)  # strip links
    text = re.sub(r'[*_`~]{1,3}', '', text)  # strip formatting
    text = re.sub(r'\s+', ' ', text).strip()

    result = {}

    # ── TextDescriptives (coherence, dependency, POS, quality) ──
    if HAS_TD:
        try:
            nlp = _get_nlp()
            # Process up to 100k chars to avoid memory issues
            doc = nlp(text[:100000])
            df = td.extract_df(doc)

            # Coherence
            for col in df.columns:
                if 'coherence' in col.lower():
                    val = df[col].iloc[0] if len(df) > 0 else None
                    if val is not None and not (isinstance(val, float) and val != val):
                        result[f'td_{col}'] = round(float(val), 4)

            # Dependency distance
            for col in df.columns:
                if 'dependency' in col.lower() or 'dep_distance' in col.lower():
                    val = df[col].iloc[0] if len(df) > 0 else None
                    if val is not None and not (isinstance(val, float) and val != val):
                        result[f'td_{col}'] = round(float(val), 4)

            # POS proportions
            for col in df.columns:
                if 'pos_prop' in col.lower():
                    val = df[col].iloc[0] if len(df) > 0 else None
                    if val is not None and not (isinstance(val, float) and val != val):
                        result[f'td_{col}'] = round(float(val), 4)

            # Readability (additional beyond textstat)
            for col in df.columns:
                if any(k in col.lower() for k in ['lix', 'rix', 'readability']):
                    val = df[col].iloc[0] if len(df) > 0 else None
                    if val is not None and not (isinstance(val, float) and val != val):
                        result[f'td_{col}'] = round(float(val), 4)

            # Quality metrics
            for col in df.columns:
                if 'quality' in col.lower() or 'duplicate' in col.lower():
                    val = df[col].iloc[0] if len(df) > 0 else None
                    if val is not None and not (isinstance(val, float) and val != val):
                        result[f'td_{col}'] = round(float(val), 4)

            # Token-level stats
            for col in df.columns:
                if any(k in col.lower() for k in ['token_length', 'sentence_length',
                                                    'syllables', 'n_tokens', 'n_sentences']):
                    val = df[col].iloc[0] if len(df) > 0 else None
                    if val is not None and not (isinstance(val, float) and val != val):
                        result[f'td_{col}'] = round(float(val), 4)

        except Exception as e:
            result['textdescriptives_status'] = f'fallback: {e}'
    else:
        result['textdescriptives_status'] = 'fallback: textdescriptives not installed'

    # ── Lexical Richness (vocabulary diversity) ──
    if HAS_LR:
        try:
            # Clean further for lexical analysis
            clean = re.sub(r'[^a-zA-Z\s]', ' ', text)
            clean = re.sub(r'\s+', ' ', clean).strip()

            if len(clean.split()) >= 50:
                lr = LexicalRichness(clean)
                result['lr_ttr'] = round(lr.ttr, 4)  # Type-Token Ratio
                result['lr_rttr'] = round(lr.rttr, 4)  # Root TTR
                result['lr_cttr'] = round(lr.cttr, 4)  # Corrected TTR
                result['lr_words'] = lr.words
                result['lr_terms'] = lr.terms

                try:
                    result['lr_mtld'] = round(lr.mtld(threshold=0.72), 4)
                except:
                    pass
                try:
                    result['lr_mattr'] = round(lr.mattr(window_size=25), 4)
                except:
                    pass
                try:
                    result['lr_hdd'] = round(lr.hdd(sample_size=42), 4)
                except:
                    pass
            else:
                result['lr_error'] = 'text too short for lexical analysis'

        except Exception as e:
            result['lr_error'] = str(e)
    else:
        result['lr_error'] = 'lexicalrichness not installed'

    return result


if __name__ == '__main__':
    import sys, json
    if len(sys.argv) > 1:
        r = analyze(sys.argv[1])
        print(json.dumps(r, indent=2))
    else:
        print("Usage: python linguistic_analyzer.py <paper.md>")
