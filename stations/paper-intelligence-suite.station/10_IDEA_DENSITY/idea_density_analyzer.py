"""
L10 — IDEA DENSITY
==================
Measures propositional density: how many ideas per word.

Higher density = more intellectually packed text.
Academic papers typically score 0.45-0.55.
Casual writing typically scores 0.30-0.40.

Uses ideadensity library (CPIDR algorithm).
"""
import re
from pathlib import Path

try:
    from ideadensity import cpidr
    HAS_ID = True
except ImportError:
    HAS_ID = False


def analyze(paper_path: str) -> dict:
    text = Path(paper_path).read_text(encoding='utf-8', errors='replace')
    # Clean markdown
    text = re.sub(r'^---.*?---', '', text, flags=re.DOTALL)
    text = re.sub(r'#+\s+', '', text)
    text = re.sub(r'\|[^\n]+\|', '', text)
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'[*_`~]{1,3}', '', text)
    text = re.sub(r'\s+', ' ', text).strip()

    result = {}

    if not HAS_ID:
        words = re.findall(r"[A-Za-z']+", text)
        sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
        clauses = re.findall(r'[,;:]|\b(and|but|because|therefore|so|if|then|when|where|which|that)\b', text, re.I)
        concept_words = [
            w for w in words
            if len(w) >= 7 or w.lower() in {
                'grace', 'faith', 'truth', 'logos', 'quantum', 'entropy',
                'observer', 'coherence', 'collapse', 'measurement'
            }
        ]
        word_count = max(len(words), 1)
        proposition_count = len(sentences) + len(clauses) + len(concept_words)
        density = proposition_count / word_count
        result['idea_density_mean'] = round(density, 4)
        result['idea_density_min'] = round(density, 4)
        result['idea_density_max'] = round(density, 4)
        result['idea_density_std'] = 0
        result['idea_total_propositions'] = proposition_count
        result['idea_paragraphs_analyzed'] = max(1, len([p for p in text.split('\n\n') if p.strip()]))
        result['idea_density_status'] = 'fallback: lexical proposition estimate'
        if density >= 0.55:
            result['idea_density_level'] = 'VERY HIGH (dense academic)'
        elif density >= 0.45:
            result['idea_density_level'] = 'HIGH (academic)'
        elif density >= 0.35:
            result['idea_density_level'] = 'MODERATE (accessible)'
        else:
            result['idea_density_level'] = 'LOW (casual/narrative)'
        return result

    try:
        # Process in chunks (ideadensity works best on paragraphs)
        paragraphs = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 50]
        if not paragraphs:
            paragraphs = [text]

        densities = []
        word_counts = []
        prop_counts = []

        for para in paragraphs[:100]:  # cap at 100 paragraphs
            try:
                # cpidr returns (word_count, proposition_count, density, word_list)
                wc, pc, d, _ = cpidr(para)
                if d and d > 0:
                    densities.append(d)
                    word_counts.append(wc)
                    prop_counts.append(pc)
            except:
                continue

        if densities:
            result['idea_density_mean'] = round(sum(densities) / len(densities), 4)
            result['idea_density_min'] = round(min(densities), 4)
            result['idea_density_max'] = round(max(densities), 4)
            result['idea_density_std'] = round(
                (sum((d - result['idea_density_mean'])**2 for d in densities)
                 / len(densities)) ** 0.5, 4)
            result['idea_total_propositions'] = sum(prop_counts)
            result['idea_paragraphs_analyzed'] = len(densities)

            # Classify density level
            mean = result['idea_density_mean']
            if mean >= 0.55:
                result['idea_density_level'] = 'VERY HIGH (dense academic)'
            elif mean >= 0.45:
                result['idea_density_level'] = 'HIGH (academic)'
            elif mean >= 0.35:
                result['idea_density_level'] = 'MODERATE (accessible)'
            else:
                result['idea_density_level'] = 'LOW (casual/narrative)'
        else:
            result['idea_density_error'] = 'no valid paragraphs processed'

    except Exception as e:
        result['idea_density_error'] = str(e)

    return result


if __name__ == '__main__':
    import sys, json
    if len(sys.argv) > 1:
        r = analyze(sys.argv[1])
        print(json.dumps(r, indent=2))
    else:
        print("Usage: python idea_density_analyzer.py <paper.md>")
