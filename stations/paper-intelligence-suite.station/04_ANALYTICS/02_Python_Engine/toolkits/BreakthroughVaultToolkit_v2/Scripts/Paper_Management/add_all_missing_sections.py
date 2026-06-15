import re
from pathlib import Path

# Paths
ASSEMBLED_PATH = Path(r"C:\Users\Yellowkid\Desktop\Obisidan Final\THEOPHYSICS_MASTER\06_Publication\Logos_Papers\COMPLETE_LOGOS_PAPERS_FINAL\THEOPHYSICS_MASTER_PAPER_ASSEMBLED.md")
INDIVIDUAL_DIR = Path(r"C:\Users\Yellowkid\Desktop\Obisidan Final\THEOPHYSICS_MASTER\06_Publication\Logos_Papers\COMPLETE_LOGOS_PAPERS_FINAL")

def find_paper_boundaries(content):
    """Find where each paper starts"""
    papers = []
    pattern = r'^#\s+\*\*Paper\s+(\d+):|^#\s+PAPER\s+(\d+):'
    for match in re.finditer(pattern, content, re.MULTILINE):
        paper_num = int(match.group(1) or match.group(2))
        papers.append((paper_num, match.start()))
    return sorted(papers, key=lambda x: x[0])

def get_individual_paper_file(paper_num):
    """Find the individual paper file"""
    patterns = [
        f"Paper-{paper_num:02d}-*-FINAL.md",
        f"Paper-{paper_num:02d}-*FINAL.md",
        f"Paper-{paper_num}-*-FINAL.md"
    ]
    
    for pattern in patterns:
        matches = list(INDIVIDUAL_DIR.glob(pattern))
        if matches:
            return matches[0]
    
    for file in INDIVIDUAL_DIR.glob("Paper-*.md"):
        if f"Paper-{paper_num}" in file.name or f"Paper-{paper_num:02d}" in file.name:
            return file
    
    return None

def extract_section_by_patterns(content, patterns, start_pos=0):
    """Extract section using multiple pattern options"""
    for pattern in patterns:
        match = re.search(pattern, content[start_pos:], re.MULTILINE | re.IGNORECASE)
        if match:
            section_start = start_pos + match.start()
            
            # Include --- before if present
            if section_start >= 3 and content[section_start-3:section_start] == '---':
                section_start -= 3
            
            # Find next major header
            next_match = re.search(r'^(---)?(##|#)\s+', content[section_start+1:], re.MULTILINE)
            if next_match:
                next_pos = section_start + 1 + next_match.start()
                # Check if it's a subsection (###)
                if content[next_pos:next_pos+3] == '###':
                    # Find next ## or #
                    next_match2 = re.search(r'^(---)?(##|#)\s+', content[next_pos+1:], re.MULTILINE)
                    if next_match2:
                        section_end = next_pos + 1 + next_match2.start()
                    else:
                        section_end = len(content)
                else:
                    section_end = next_pos
            else:
                section_end = len(content)
            
            section_content = content[section_start:section_end].strip()
            
            # Stop at navigation or status
            nav_patterns = [
                r'^## 📖 Series Navigation',
                r'^## 🔗 Series Navigation',
                r'^Paper \d+ Status:',
                r'^## NEXT STEPS',
                r'^## PAPER CONNECTIONS'
            ]
            for nav_pattern in nav_patterns:
                nav_match = re.search(nav_pattern, section_content, re.MULTILINE | re.IGNORECASE)
                if nav_match:
                    section_content = section_content[:nav_match.start()].strip()
            
            return section_content
    return None

def extract_all_sections_from_paper(paper_content):
    """Extract all possible sections from a paper"""
    sections = {}
    
    # Hypotheses
    patterns = [
        r'^---## 🎯 Hypotheses',
        r'^## 🎯 Hypotheses',
        r'^## 🎯\s+Hypotheses'
    ]
    sections['Hypotheses'] = extract_section_by_patterns(paper_content, patterns)
    
    # Lexicon
    patterns = [
        r'^## 📖 Lexicon',
        r'^## 📖\s+Lexicon'
    ]
    sections['Lexicon'] = extract_section_by_patterns(paper_content, patterns)
    
    # Evidence / How Right We Are
    patterns = [
        r'^## ✅ How Right We Are',
        r'^## ✅ Evidence',
        r'^## ✅ Evidence & Validation',
        r'^## ✅\s+Evidence'
    ]
    sections['Evidence'] = extract_section_by_patterns(paper_content, patterns)
    
    # What We Got Wrong
    patterns = [
        r'^### E\. What We Got Wrong',
        r'^### C\. What We Got Wrong \(Intellectual Honesty\)',
        r'^### C\. What We Got Wrong',
        r'^## What We Got Wrong',
        r'^##\s+\*\*WHERE WE STAND\s*\(HONESTLY\)\*\*',
        r'^##\s+WHERE WE STAND\s*\(HONESTLY\)',
        r'^##\s+WHERE WE STAND',
        r'⚠️.*Where We Might Be Wrong',
        r'Where We Might Be Wrong'
    ]
    sections['What We Got Wrong'] = extract_section_by_patterns(paper_content, patterns)
    
    # Enigmas
    patterns = [
        r'^## ❓ Enigmas',
        r'^## ❓\s+Enigmas',
        r'^##\s+\*\*THE ENIGMAS\*\*',
        r'^##\s+THE ENIGMAS',
        r'^##\s+Enigmas'
    ]
    sections['Enigmas'] = extract_section_by_patterns(paper_content, patterns)
    
    # References
    patterns = [
        r'^## 📚 References',
        r'^## 📚\s+References',
        r'^## References'
    ]
    sections['References'] = extract_section_by_patterns(paper_content, patterns)
    
    return sections

def standardize_section_header(section_name, content):
    """Convert section to standard header format"""
    if not content:
        return None
    
    # Remove existing headers and clean up
    content = content.strip()
    
    # Map to standard headers
    header_map = {
        'Hypotheses': '## 🎯 Hypotheses',
        'Lexicon': '## 📖 Lexicon',
        'Evidence': '## ✅ Evidence & Validation',
        'What We Got Wrong': '### E. What We Got Wrong (Or Haven\'t Figured Out Yet)',
        'Enigmas': '## ❓ Enigmas',
        'References': '## 📚 References'
    }
    
    standard_header = header_map.get(section_name, f'## {section_name}')
    
    # Remove old headers (more comprehensive patterns)
    patterns_to_remove = [
        r'^---?\s*##\s*\*\*?🎯\s*Hypotheses\*\*?.*?\n',
        r'^---?\s*##\s*\*\*?📖\s*Lexicon\*\*?.*?\n',
        r'^---?\s*##\s*\*\*?✅\s*.*?\*\*?.*?\n',
        r'^---?\s*##\s*\*\*?❓\s*Enigmas\*\*?.*?\n',
        r'^---?\s*##\s*\*\*?📚\s*References\*\*?.*?\n',
        r'^---?\s*##\s*\*\*?WHERE WE STAND.*?\*\*?.*?\n',
        r'^---?\s*##\s*\*\*?THE ENIGMAS\*\*?.*?\n',
        r'^---?\s*##\s*WHERE WE STAND.*?\n',
        r'^---?\s*##\s*THE ENIGMAS.*?\n',
        r'^---?\s*##\s*References.*?\n',
        r'^---?\s*###\s*.*?What We Got Wrong.*?\n'
    ]
    
    for pattern in patterns_to_remove:
        content = re.sub(pattern, '', content, flags=re.MULTILINE | re.IGNORECASE)
    
    # Clean up any remaining --- at start
    content = re.sub(r'^---+\s*', '', content)
    
    # Add standard header if content doesn't start with it
    if not re.match(r'^##\s+[🎯📖✅❓📚]', content):
        content = standard_header + '\n\n' + content
    
    return content

def check_section_exists(content, section_name, start_pos, end_pos):
    """Check if section exists in range"""
    section_content = content[start_pos:end_pos]
    patterns = {
        'Hypotheses': [r'## 🎯 Hypotheses'],
        'Lexicon': [r'## 📖 Lexicon'],
        'Evidence': [r'## ✅', r'## ✅ Evidence'],
        'What We Got Wrong': [r'What We Got Wrong', r'WHERE WE STAND'],
        'Enigmas': [r'## ❓ Enigmas', r'## THE ENIGMAS'],
        'References': [r'## 📚 References', r'## References']
    }
    
    for pattern in patterns.get(section_name, []):
        if re.search(pattern, section_content, re.MULTILINE | re.IGNORECASE):
            return True
    return False

def add_missing_sections():
    """Main function"""
    print("Reading assembled paper...")
    with open(ASSEMBLED_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        assembled_content = f.read()
    
    papers = find_paper_boundaries(assembled_content)
    print(f"Found {len(papers)} papers\n")
    
    changes_made = False
    
    for i, (paper_num, paper_start) in enumerate(papers):
        next_start = papers[i+1][1] if i+1 < len(papers) else len(assembled_content)
        
        print(f"Processing Paper {paper_num}...")
        
        # Check what's missing - use standard format check only
        missing = []
        for section_name in ['Hypotheses', 'Lexicon', 'Evidence', 'What We Got Wrong', 'Enigmas', 'References']:
            if not check_section_exists(assembled_content, section_name, paper_start, next_start):
                missing.append(section_name)
        
        if not missing:
            print(f"  ✓ All sections present")
            continue
        
        print(f"  Missing: {', '.join(missing)}")
        
        # Get individual paper
        individual_file = get_individual_paper_file(paper_num)
        if not individual_file:
            print(f"  ⚠ Could not find individual file")
            continue
        
        print(f"  Found: {individual_file.name}")
        
        # Read individual paper
        with open(individual_file, 'r', encoding='utf-8', errors='ignore') as f:
            individual_content = f.read()
        
        # Extract sections
        extracted = extract_all_sections_from_paper(individual_content)
        
        # Find insertion point (before navigation)
        insertion_point = next_start
        nav_match = re.search(r'^## 📖 Series Navigation|^## 🔗 Series Navigation|^Paper \d+ Status:', 
                             assembled_content[paper_start:next_start], re.MULTILINE)
        if nav_match:
            insertion_point = paper_start + nav_match.start()
        
        # Build sections to add
        sections_to_add = []
        for section_name in missing:
            if section_name in extracted and extracted[section_name]:
                standardized = standardize_section_header(section_name, extracted[section_name])
                if standardized:
                    sections_to_add.append((section_name, standardized))
                    print(f"    ✓ Extracted {section_name}")
            else:
                print(f"    ✗ {section_name} not found in individual file")
        
        if sections_to_add:
            # Insert sections
            insert_text = "\n\n---\n\n"
            for section_name, section_content in sections_to_add:
                insert_text += section_content + "\n\n---\n\n"
            
            assembled_content = assembled_content[:insertion_point] + insert_text + assembled_content[insertion_point:]
            changes_made = True
            print(f"  ✓ Added {len(sections_to_add)} sections")
        
        print()
    
    if changes_made:
        print("Writing updated assembled paper...")
        with open(ASSEMBLED_PATH, 'w', encoding='utf-8') as f:
            f.write(assembled_content)
        print("✓ Done! Missing sections have been added.")
    else:
        print("No changes needed.")

if __name__ == "__main__":
    add_missing_sections()

