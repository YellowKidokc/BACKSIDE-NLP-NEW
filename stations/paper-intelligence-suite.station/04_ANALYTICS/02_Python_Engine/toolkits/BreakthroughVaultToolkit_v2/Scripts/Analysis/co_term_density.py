# co_term_density.py
"""
Calculate co-term density for a given term in the vault.
Shows how often specialized terms appear near the target term.
"""

import os
import re
from collections import Counter

def calculate_co_term_density(vault_path, term, window_size=15):
    """
    Scan vault for 'term' and count specialized terms within ±window_size words.
    
    Args:
        vault_path: Path to Obsidian vault
        term: Target term to analyze
        window_size: Words to scan before/after term (default: 15)
    
    Returns:
        Dictionary with co-term density analysis
    """
    # Define specialized Theophysics terms
    specialized_terms = [
        'χ', 'chi', 'logos', 'coherence', 'entropy', 'field', 
        'observer', 'collapse', 'grace', 'pneumatological',
        'actualization', 'lagrangian', 'master', 'equation',
        'consciousness', 'wavefunction', 'quantum', 'spiritual',
        'divine', 'redemption', 'salvation', 'faith', 'prayer',
        'scripture', 'prophecy', 'covenant', 'trinity'
    ]
    
    co_occurrences = Counter()
    term_count = 0
    
    # Walk through vault
    for root, dirs, files in os.walk(vault_path):
        # Skip hidden folders and scripts
        if any(skip in root for skip in ['_SCRIPTS', '_META', '_TEMPLATES', '.obsidian']):
            continue
            
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read().lower()
                        words = re.findall(r'\b\w+\b', content)
                        
                        # Find all occurrences of target term
                        for i, word in enumerate(words):
                            if word == term.lower():
                                term_count += 1
                                # Look at ±window_size words
                                start = max(0, i - window_size)
                                end = min(len(words), i + window_size + 1)
                                context = words[start:end]
                                
                                # Count specialized terms in context
                                for spec_term in specialized_terms:
                                    co_occurrences[spec_term] += context.count(spec_term.lower())
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")
                    continue
    
    if term_count == 0:
        return {
            'term': term,
            'occurrences': 0,
            'co_term_density': 0,
            'top_co_terms': []
        }
    
    total_co_terms = sum(co_occurrences.values())
    density = (total_co_terms / term_count) * 100
    
    return {
        'term': term,
        'occurrences': term_count,
        'co_term_density': round(density, 2),
        'top_co_terms': co_occurrences.most_common(10),
        'total_co_terms': total_co_terms
    }


if __name__ == "__main__":
    # Example usage
    vault_path = r"C:\Users\Yellowkid\Desktop\Obisidan Final\THEOPHYSICS_MASTER"
    
    # Test with multiple terms
    test_terms = ['coherence', 'observer', 'field', 'grace']
    
    print("="*60)
    print("CO-TERM DENSITY ANALYSIS")
    print("="*60)
    print()
    
    for term in test_terms:
        result = calculate_co_term_density(vault_path, term)
        
        print(f"TERM: {result['term'].upper()}")
        print(f"  Occurrences: {result['occurrences']}")
        print(f"  Co-Term Density: {result['co_term_density']} terms per 100 words")
        print(f"  Total Co-Terms Found: {result['total_co_terms']}")
        print(f"  Top Co-Occurring Terms:")
        for spec_term, count in result['top_co_terms'][:5]:
            print(f"    - {spec_term}: {count} times")
        print()
        print("-"*60)
        print()
