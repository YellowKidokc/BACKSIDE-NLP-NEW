"""Quick vault statistics scanner"""
import os
import re
from pathlib import Path
from collections import Counter, defaultdict

VAULT = Path(r"C:/Users/lowes/OneDrive/Desktop/Theophysics Obsidian/00_CANONICAL")

def scan():
    stats = {
        'total_files': 0,
        'total_lines': 0,
        'total_bytes': 0,
        'by_folder': defaultdict(int),
        'tags': Counter(),
        'concepts': Counter(),
        'axioms': 0,
        'theorems': 0,
        'definitions': 0,
        'laws': 0,
        'claims': 0
    }
    
    concept_pattern = re.compile(r'\b(Grace|Entropy|Coherence|Logos|Trinity|Resurrection|Consciousness|Information|Quantum|Soul|Faith|Judgment|Observer|Decoherence|χ)\b', re.IGNORECASE)
    
    for root, dirs, files in os.walk(VAULT):
        for f in files:
            if not f.endswith('.md'):
                continue
            
            fp = Path(root) / f
            stats['total_files'] += 1
            stats['total_bytes'] += fp.stat().st_size
            
            # Folder tracking
            rel = fp.relative_to(VAULT)
            folder = rel.parts[0] if len(rel.parts) > 1 else 'root'
            stats['by_folder'][folder] += 1
            
            try:
                content = fp.read_text(encoding='utf-8', errors='ignore')
                stats['total_lines'] += content.count('\n')
                
                # Count element types
                if f.startswith('A') and '_' in f:
                    stats['axioms'] += 1
                elif f.startswith('TH'):
                    stats['theorems'] += 1
                elif f.startswith('D') and f[1].isdigit():
                    stats['definitions'] += 1
                elif f.startswith('L') and f[1].isdigit():
                    stats['laws'] += 1
                elif f.startswith('CL'):
                    stats['claims'] += 1
                
                # Extract concepts
                for match in concept_pattern.findall(content):
                    stats['concepts'][match.lower()] += 1
                    
                # Extract tags from YAML
                if content.startswith('---'):
                    yaml_end = content.find('---', 3)
                    if yaml_end > 0:
                        yaml = content[3:yaml_end]
                        tag_match = re.search(r'tags:\s*\[(.*?)\]', yaml)
                        if tag_match:
                            for t in tag_match.group(1).split(','):
                                stats['tags'][t.strip().strip('"').strip("'")] += 1
            except:
                pass
    
    return stats

if __name__ == "__main__":
    print("=" * 60)
    print("THEOPHYSICS VAULT STATISTICS")
    print("=" * 60)
    
    s = scan()
    
    print(f"\nTOTALS")
    print(f"   Files: {s['total_files']}")
    print(f"   Lines: {s['total_lines']:,}")
    print(f"   Size:  {s['total_bytes']/1024/1024:.2f} MB")
    
    print(f"\nELEMENT COUNTS")
    print(f"   Axioms:      {s['axioms']}")
    print(f"   Theorems:    {s['theorems']}")
    print(f"   Definitions: {s['definitions']}")
    print(f"   Laws:        {s['laws']}")
    print(f"   Claims:      {s['claims']}")
    
    print(f"\nBY FOLDER (top 10)")
    for folder, count in sorted(s['by_folder'].items(), key=lambda x: -x[1])[:10]:
        print(f"   {folder}: {count}")
    
    print(f"\nCONCEPT MENTIONS (top 15)")
    for concept, count in s['concepts'].most_common(15):
        print(f"   {concept}: {count}")
    
    print(f"\nTAGS (top 10)")
    for tag, count in s['tags'].most_common(10):
        print(f"   {tag}: {count}")
    
    print("\n" + "=" * 60)
