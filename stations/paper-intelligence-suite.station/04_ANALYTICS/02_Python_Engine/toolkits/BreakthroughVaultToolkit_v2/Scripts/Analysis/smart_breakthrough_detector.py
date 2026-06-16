"""
Enhanced breakthrough detector - finds Order 2+ integrations anywhere
Not limited to trigger phrases
"""

import json
import re
from pathlib import Path
from collections import Counter, defaultdict

class SmartBreakthroughDetector:
    def __init__(self, paper_path, config_path):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        with open(paper_path, 'r', encoding='utf-8') as f:
            self.content = f.read()
        
        self.core_concepts = self.config['core_concepts']
        self.params = self.config['analysis_parameters']['breakthrough_detection']
        
        self.domains = {
            'physics': ['gravity', 'mass', 'energy', 'entropy', 'quantum', 'spacetime', 
                       'relativity', 'collapse', 'decoherence', 'entanglement'],
            'theology': ['grace', 'sin', 'soul', 'resurrection', 'faith', 'covenant',
                        'redemption', 'salvation', 'holy', 'divine'],
            'information': ['χ', 'coherence', 'information', 'observer', 'Logos',
                          'data', 'bit', 'entropy'],
            'consciousness': ['consciousness', 'awareness', 'choice', 'agency',
                            'mind', 'experience', 'qualia']
        }
    
    def find_breakthroughs(self):
        """Find all passages with Order 2+ integrations"""
        breakthroughs = []
        
        # Split into paragraphs
        paragraphs = self.content.split('\n\n')
        
        for i, para in enumerate(paragraphs):
            if len(para) < 100:  # Skip short paragraphs
                continue
            
            # Find all concepts in this paragraph
            concepts_found = [
                concept for concept in self.core_concepts
                if concept.lower() in para.lower()
            ]
            
            if len(concepts_found) < 3:  # Need at least 3 concepts
                continue
            
            # Calculate integration order
            order, domains_involved = self.calculate_integration_order(concepts_found)
            
            if order >= self.params['integration_order_min']:
                breakthroughs.append({
                    'paragraph_index': i,
                    'integration_order': order,
                    'domains': list(domains_involved),
                    'concepts': concepts_found,
                    'text': para[:300] + '...' if len(para) > 300 else para,
                    'concept_count': len(concepts_found)
                })
        
        return sorted(breakthroughs, key=lambda x: (-x['integration_order'], -x['concept_count']))
    
    def calculate_integration_order(self, concepts):
        """Calculate which domains are integrated"""
        domains_involved = set()
        
        for concept in concepts:
            for domain, terms in self.domains.items():
                if any(term.lower() in concept.lower() for term in terms):
                    domains_involved.add(domain)
        
        # Order = number of domains integrated
        return len(domains_involved), domains_involved

# Run on all papers
if __name__ == "__main__":
    PAPERS_ROOT = Path(r"D:\THEOPHYSICS_MASTER\06_Publication\Logos_Papers")
    OUTPUT_DIR = Path(r"D:\THEOPHYSICS_MASTER\_ANALYSIS\GLOBAL\Breakthrough_Maps")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    PAPERS = [
        "P01-Logos-Principle",
        "P02-Quantum-Bridge",
        "P03-Algorithm-Reality",
        "P04-Hard-Problem",
        "P05-Soul-Observer",
        "P06-Physics-Principalities",
        "P07-Grace-Function",
        "P08-Stretched-Heavens",
        "P09-Moral-Universe",
        "P10-Creatio-Silico",
        "P11-Protocols-Validation",
        "P12-Decalogue-Cosmos"
    ]
    
    all_breakthroughs = {}
    
    print("=" * 60)
    print("ENHANCED BREAKTHROUGH DETECTION")
    print("Finding Order 2+ integrations across all papers")
    print("=" * 60)
    print()
    
    for paper_name in PAPERS:
        paper_folder = PAPERS_ROOT / paper_name
        paper_file = None
        
        # Find the paper markdown file
        for f in paper_folder.glob("*.md"):
            if "README" not in f.name and "Paper" in f.name:
                paper_file = f
                break
        
        if not paper_file:
            print(f"[WARN] No paper file found in {paper_name}")
            continue
        
        config_file = paper_folder / "_LOCAL" / "config.json"
        if not config_file.exists():
            print(f"[WARN] No config in {paper_name}")
            continue
        
        try:
            detector = SmartBreakthroughDetector(paper_file, config_file)
            breakthroughs = detector.find_breakthroughs()
            
            all_breakthroughs[paper_name] = breakthroughs
            
            print(f"[OK] {paper_name}: {len(breakthroughs)} breakthroughs")
            if breakthroughs:
                orders = Counter(b['integration_order'] for b in breakthroughs)
                print(f"     Orders: {dict(orders)}")
        
        except Exception as e:
            print(f"[ERROR] {paper_name}: {str(e)[:60]}")
    
    # Write comprehensive report
    report_path = OUTPUT_DIR / "ALL_BREAKTHROUGHS.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# BREAKTHROUGH MAP - ALL PAPERS\n\n")
        f.write(f"**Integration Order Minimum:** 2\n")
        f.write(f"**Total Papers Analyzed:** {len(all_breakthroughs)}\n\n")
        
        total = sum(len(b) for b in all_breakthroughs.values())
        f.write(f"**Total Breakthroughs Found:** {total}\n\n")
        f.write("---\n\n")
        
        for paper_name, breakthroughs in all_breakthroughs.items():
            f.write(f"## {paper_name}\n\n")
            f.write(f"**Breakthroughs:** {len(breakthroughs)}\n\n")
            
            if not breakthroughs:
                f.write("No Order 2+ integrations found.\n\n")
                continue
            
            # Group by order
            by_order = defaultdict(list)
            for b in breakthroughs:
                by_order[b['integration_order']].append(b)
            
            for order in sorted(by_order.keys(), reverse=True):
                items = by_order[order]
                f.write(f"### Order {order} Integrations ({len(items)})\n\n")
                
                for i, breakthrough in enumerate(items[:5], 1):  # Top 5 per order
                    f.write(f"**{i}. Domains:** {', '.join(breakthrough['domains'])}\n")
                    f.write(f"**Concepts ({len(breakthrough['concepts'])}):** {', '.join(breakthrough['concepts'][:10])}\n")
                    f.write(f"**Text:**\n> {breakthrough['text']}\n\n")
            
            f.write("---\n\n")
    
    print()
    print("=" * 60)
    print(f"Report saved: {report_path}")
    print("=" * 60)
