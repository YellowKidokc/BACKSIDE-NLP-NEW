"""
ST_009 — Article Taxonomy Classifier
Hybrid approach: keyword density baseline + optional LLM refinement.

Input:  HTML or markdown article in _inbox/
Output: JSON classification in _outbox/

Usage:
  python pipeline.py                    # process all files in _inbox
  python pipeline.py --file article.html  # process single file
"""

import json
import re
import sys
from pathlib import Path
from collections import Counter

STATION_DIR = Path(__file__).parent
INBOX = STATION_DIR / "_inbox"
OUTBOX = STATION_DIR / "_outbox"
PROCESSED = STATION_DIR / "_processed"

for d in [INBOX, OUTBOX, PROCESSED]:
    d.mkdir(exist_ok=True)

# ── Keyword dictionaries (baseline classifier) ─────────────────
CATEGORY_KEYWORDS = {
    "physics": ["gravity","relativity","quantum","force","energy","momentum","spacetime","electromagnetic","photon","particle","wave","field","entropy","thermodynamic","mechanics","planck","einstein","newton","bohr","schrodinger","geodesic","curvature","tensor","hamiltonian","lagrangian","symmetry","conservation","wavelength","frequency","spectrum","nuclear","decay","radiation","coupling","spin","angular"],
    "theology": ["god","christ","jesus","spirit","scripture","bible","gospel","church","prayer","worship","faith","sin","salvation","resurrection","revelation","prophet","apostle","covenant","psalm","genesis","exodus","john","paul","matthew","luke","commandment","baptism","communion","testament","doctrine","creed","orthodox","catholic","protestant"],
    "math": ["theorem","proof","lean","lean4","axiom","lemma","corollary","verified","compiled","sorry","admit","formal","derivation","equation","formula","computation","algebra","calculus","topology","manifold","bijective","isomorphism","homomorphism","category","functor","lattice","boolean","predicate","quantifier"],
    "info-theory": ["shannon","information","entropy","channel","capacity","noise","signal","bit","bandwidth","encoding","decoding","compression","redundancy","error correction","landauer","kullback","leibler","mutual information","codec","data"],
    "consciousness": ["consciousness","observer","measurement","awareness","qualia","hard problem","experience","subjective","mind","perception","attention","cognition","watcher","sentience","phenomenal","intentionality","binding"],
    "trinity": ["trinity","father","son","spirit","triad","three-in-one","perichoresis","nicene","trinitarian","modalism","tritheism","homoousios","begotten","procession","filioque","triune"],
    "grace": ["grace","salvation","atonement","cross","redemption","ransom","substitution","propitiation","reconciliation","justification","sanctification","regeneration","forgiveness","mercy","pardon","restoration","healing","redeemer"],
    "entropy": ["entropy","decoherence","decay","disorder","chaos","degradation","collapse","fragmentation","dissipation","erosion","corruption","sin","noise","drift","heat death","irreversible","second law"],
    "justice": ["justice","mercy","judge","judgment","court","verdict","penalty","sentence","fair","righteous","impartial","proportional","retribution","restitution","equity","paradox"],
    "free-will": ["free will","choice","determinism","agency","volition","libertarian","compatibilist","moral weight","responsibility","autonomy","coercion","freedom","decision","consent","will"],
    "adversary": ["adversary","satan","devil","enemy","darkness","evil","deception","liar","accuser","tempter","destroyer","anti-christ","demonic","fallen","serpent","principality"],
    "genesis": ["genesis","creation","fall","garden","eden","adam","eve","tree","serpent","fruit","original sin","paradise","innocence","naked","curse","toil","expulsion"],
    "ten-laws": ["ten laws","law 1","law 2","law 3","law 4","law 5","law 6","law 7","law 8","law 9","law 10","symmetry pair","dual projection","physics-theology"],
    "master-eq": ["master equation","chi","chi-field","product structure","ten variables","coherence equation","dC/dt","ordering force","grace term","decay term","source term"],
    "method": ["7q","seven questions","bilateral audit","isomorphic event density","methodology","falsification","kill condition","protocol","rigor","reproducible","systematic"],
    "evidence": ["sigma","p-value","correlation","experiment","data","dataset","statistical","PEAR","GCP","MDA","R-squared","regression","empirical","replicate","measurement","observed","predicted"],
    "society": ["society","culture","institution","civilization","decline","amish","family","marriage","divorce","trust","community","political","government","policy","historical","nation"],
    "cross-domain": ["isomorphism","cross-domain","structural correspondence","mapping","bridge","convergence","dual","projection","parallel","analogy","homology","universal"],
    "story": ["testimony","journey","personal","fence","contractor","oklahoma","experience","dream","calling","mission","ministry","life","family","grew up","discovered"],
    "ai": ["artificial intelligence","AI","claude","GPT","gemini","codex","machine learning","neural","model","convergence","david effect","multi-AI","collaboration","preference engine"]
}


def strip_html(text: str) -> str:
    """Remove HTML tags, scripts, styles."""
    text = re.sub(r'<style[^>]*>[\s\S]*?</style>', '', text, flags=re.I)
    text = re.sub(r'<script[^>]*>[\s\S]*?</script>', '', text, flags=re.I)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()


def extract_title(html: str) -> str:
    """Pull title from <title> tag."""
    m = re.search(r'<title>(.*?)</title>', html, re.I)
    return m.group(1) if m else "Untitled"


def classify_by_keywords(text: str) -> dict:
    """Score each category by keyword density. Returns percentages summing to 100."""
    scores = {}
    words = text.split()
    total_words = len(words)
    if total_words == 0:
        return {cat: 5 for cat in CATEGORY_KEYWORDS}  # uniform if empty

    for cat, keywords in CATEGORY_KEYWORDS.items():
        count = 0
        for kw in keywords:
            if ' ' in kw:
                count += text.count(kw)
            else:
                count += words.count(kw)
        scores[cat] = count

    # Normalize to 100%
    total = sum(scores.values())
    if total == 0:
        return {cat: 5 for cat in CATEGORY_KEYWORDS}

    percentages = {}
    for cat, score in scores.items():
        percentages[cat] = round(score / total * 100)

    # Fix rounding to exactly 100
    diff = 100 - sum(percentages.values())
    if diff != 0:
        top_cat = max(percentages, key=percentages.get)
        percentages[top_cat] += diff

    return percentages


def classify_article(filepath: Path) -> dict:
    """Classify a single article. Returns full taxonomy result."""
    raw = filepath.read_text(encoding='utf-8', errors='ignore')
    title = extract_title(raw)
    text = strip_html(raw)

    categories = classify_by_keywords(text)

    # Top categories
    sorted_cats = sorted(categories.items(), key=lambda x: -x[1])
    top = [cat for cat, pct in sorted_cats[:5] if pct > 0]

    # Audience inference
    audience = []
    if categories.get("theology", 0) > 15 or categories.get("grace", 0) > 15:
        audience.append("believer")
    if categories.get("evidence", 0) > 10 or categories.get("method", 0) > 10:
        audience.append("skeptic")
    if categories.get("math", 0) > 15 or categories.get("method", 0) > 15:
        audience.append("researcher")
    if categories.get("story", 0) > 10 or categories.get("society", 0) > 15:
        audience.append("story")
    if not audience:
        audience = ["story"]

    # Reading complexity
    if categories.get("math", 0) > 20:
        complexity = "proof"
    elif categories.get("physics", 0) > 25 or categories.get("method", 0) > 20:
        complexity = "framework"
    else:
        complexity = "story"

    return {
        "file": filepath.name,
        "title": title,
        "categories": categories,
        "top_categories": top,
        "audience": audience,
        "reading_complexity": complexity
    }


def process_inbox():
    """Process all files in _inbox."""
    results = []
    for f in sorted(INBOX.glob("*.html")) + sorted(INBOX.glob("*.md")):
        print(f"Classifying: {f.name}")
        result = classify_article(f)
        results.append(result)

        # Save individual result
        out = OUTBOX / f"{f.stem}_taxonomy.json"
        out.write_text(json.dumps(result, indent=2), encoding='utf-8')

        # Move to processed
        f.rename(PROCESSED / f.name)

    # Save combined
    if results:
        combined = OUTBOX / "_all_taxonomy.json"
        combined.write_text(json.dumps(results, indent=2), encoding='utf-8')
        print(f"\nClassified {len(results)} articles → {combined}")

    return results


if __name__ == "__main__":
    if "--file" in sys.argv:
        idx = sys.argv.index("--file")
        if idx + 1 < len(sys.argv):
            f = Path(sys.argv[idx + 1])
            if f.exists():
                result = classify_article(f)
                print(json.dumps(result, indent=2))
            else:
                print(f"File not found: {f}")
    else:
        process_inbox()
