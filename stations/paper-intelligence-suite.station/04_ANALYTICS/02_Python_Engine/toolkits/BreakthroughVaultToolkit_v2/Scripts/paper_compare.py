"""
Paper Comparison Engine
- Run statistics on individual papers
- Generate comparative analysis across papers
- Output aggregated view
"""
import os
import re
import json
from pathlib import Path
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict

@dataclass
class PaperStats:
    paper_id: str
    title: str
    path: str
    lines: int
    words: int
    chars: int
    concepts: dict
    domains: dict
    equations: int
    citations: int
    sections: int
    integration_order: int  # Number of domains bridged

CONCEPT_PATTERN = re.compile(
    r'\b(Grace|Entropy|Coherence|Logos|Trinity|Resurrection|'
    r'Consciousness|Information|Quantum|Soul|Faith|Judgment|'
    r'Observer|Decoherence|Spacetime|Gravity|Energy|Mass)\b', 
    re.IGNORECASE
)

DOMAINS = {
    'physics': ['gravity', 'mass', 'energy', 'entropy', 'quantum', 'spacetime', 
                'relativity', 'collapse', 'decoherence', 'entanglement', 'wave'],
    'theology': ['grace', 'sin', 'soul', 'resurrection', 'faith', 'covenant',
                 'redemption', 'salvation', 'holy', 'divine', 'trinity'],
    'information': ['coherence', 'information', 'observer', 'logos',
                    'data', 'bit', 'entropy', 'compression'],
    'consciousness': ['consciousness', 'awareness', 'choice', 'agency',
                      'mind', 'experience', 'qualia', 'observer']
}

def analyze_paper(paper_path: Path) -> PaperStats:
    """Analyze a single paper file"""
    content = paper_path.read_text(encoding='utf-8', errors='ignore')
    
    # Basic counts
    lines = content.count('\n')
    words = len(content.split())
    chars = len(content)
    
    # Concepts
    concepts = Counter()
    for match in CONCEPT_PATTERN.findall(content):
        concepts[match.lower()] += 1
    
    # Domains present
    domains_found = {}
    for domain, terms in DOMAINS.items():
        count = sum(1 for t in terms if t.lower() in content.lower())
        if count > 0:
            domains_found[domain] = count
    
    # Integration order = how many domains are bridged
    integration_order = len(domains_found)
    
    # Equations (look for $ or \begin{equation})
    equations = len(re.findall(r'\$[^$]+\$|\\\[.*?\\\]', content))
    
    # Citations (look for common patterns)
    citations = len(re.findall(r'\[@|\(\d{4}\)|\[[\w\s]+,\s*\d{4}\]', content))
    
    # Sections (## headers)
    sections = len(re.findall(r'^##\s', content, re.MULTILINE))
    
    # Extract title from first H1 or filename
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else paper_path.stem
    
    return PaperStats(
        paper_id=paper_path.stem[:3] if paper_path.stem[0] == 'P' else paper_path.stem,
        title=title[:60],
        path=str(paper_path),
        lines=lines,
        words=words,
        chars=chars,
        concepts=dict(concepts),
        domains=domains_found,
        equations=equations,
        citations=citations,
        sections=sections,
        integration_order=integration_order
    )

def compare_papers(paper_paths: list) -> dict:
    """Compare multiple papers and generate aggregate stats"""
    results = []
    
    for p in paper_paths:
        path = Path(p)
        if path.exists() and path.suffix == '.md':
            stats = analyze_paper(path)
            results.append(stats)
    
    if not results:
        return {"error": "No valid papers found"}
    
    # Aggregate
    total_words = sum(r.words for r in results)
    total_lines = sum(r.lines for r in results)
    
    # Concept totals across all papers
    all_concepts = Counter()
    for r in results:
        all_concepts.update(r.concepts)
    
    # Domain coverage
    domain_coverage = defaultdict(int)
    for r in results:
        for d in r.domains:
            domain_coverage[d] += 1
    
    # Find outliers
    avg_words = total_words / len(results)
    longest = max(results, key=lambda x: x.words)
    shortest = min(results, key=lambda x: x.words)
    most_integrated = max(results, key=lambda x: x.integration_order)
    
    return {
        "summary": {
            "papers_analyzed": len(results),
            "total_words": total_words,
            "total_lines": total_lines,
            "avg_words_per_paper": int(avg_words),
        },
        "concept_totals": dict(all_concepts.most_common(20)),
        "domain_coverage": dict(domain_coverage),
        "outliers": {
            "longest": {"id": longest.paper_id, "words": longest.words},
            "shortest": {"id": shortest.paper_id, "words": shortest.words},
            "most_integrated": {"id": most_integrated.paper_id, "order": most_integrated.integration_order}
        },
        "individual": [asdict(r) for r in results]
    }

def print_comparison(results: dict):
    """Pretty print comparison results"""
    print("=" * 70)
    print("PAPER COMPARISON REPORT")
    print("=" * 70)
    
    s = results["summary"]
    print(f"\nSUMMARY")
    print(f"  Papers analyzed: {s['papers_analyzed']}")
    print(f"  Total words: {s['total_words']:,}")
    print(f"  Total lines: {s['total_lines']:,}")
    print(f"  Avg words/paper: {s['avg_words_per_paper']:,}")
    
    print(f"\nDOMAIN COVERAGE (papers touching each domain)")
    for domain, count in results["domain_coverage"].items():
        bar = "#" * count
        print(f"  {domain:15} {bar} ({count})")
    
    print(f"\nTOP CONCEPTS ACROSS ALL PAPERS")
    for concept, count in list(results["concept_totals"].items())[:10]:
        print(f"  {concept:15} {count:,}")
    
    print(f"\nOUTLIERS")
    o = results["outliers"]
    print(f"  Longest:         {o['longest']['id']} ({o['longest']['words']:,} words)")
    print(f"  Shortest:        {o['shortest']['id']} ({o['shortest']['words']:,} words)")
    print(f"  Most integrated: {o['most_integrated']['id']} (order {o['most_integrated']['order']})")
    
    print(f"\nINDIVIDUAL PAPERS")
    print("-" * 70)
    for p in results["individual"]:
        domains = ", ".join(p["domains"].keys())
        print(f"  {p['paper_id']:5} | {p['words']:6,} words | {p['sections']:2} sections | {domains}")
    
    print("=" * 70)

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Paper Comparison Engine")
    ap.add_argument("papers", nargs="+", help="Paper file paths or directory")
    ap.add_argument("--json", action="store_true", help="Output as JSON")
    ap.add_argument("--output", help="Save results to file")
    args = ap.parse_args()
    
    # If single directory provided, find all .md files
    paper_paths = []
    for p in args.papers:
        path = Path(p)
        if path.is_dir():
            paper_paths.extend(path.glob("*.md"))
        else:
            paper_paths.append(path)
    
    results = compare_papers(paper_paths)
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_comparison(results)
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dumps(results, f, indent=2)
        print(f"\nResults saved to: {args.output}")
