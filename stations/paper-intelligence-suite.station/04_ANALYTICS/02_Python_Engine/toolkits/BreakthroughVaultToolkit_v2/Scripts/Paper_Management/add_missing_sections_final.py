import re
import os
from pathlib import Path

# Paths
ASSEMBLED_PATH = Path(r"C:\Users\Yellowkid\Desktop\Obisidan Final\THEOPHYSICS_MASTER\06_Publication\Logos_Papers\COMPLETE_LOGOS_PAPERS_FINAL\THEOPHYSICS_MASTER_PAPER_ASSEMBLED.md")
INDIVIDUAL_DIR = Path(r"C:\Users\Yellowkid\Desktop\Obisidan Final\THEOPHYSICS_MASTER\06_Publication\Logos_Papers\COMPLETE_LOGOS_PAPERS_FINAL")

# Section headers to look for
SECTION_PATTERNS = {
    "Hypotheses": [
        r"^---## 🎯 Hypotheses",
        r"^## 🎯 Hypotheses",
        r"^## 🎯\s+Hypotheses",
        r"^## 🎯 Hypotheses"
    ],
    "Lexicon": [
        r"^## 📖 Lexicon",
        r"^## 📖\s+Lexicon"
    ],
    "Evidence": [
        r"^## ✅ How Right We Are",
        r"^## ✅ Evidence",
        r"^## ✅ Evidence & Validation"
    ],
    "What We Got Wrong": [
        r"^### E\. What We Got Wrong",
        r"^### C\. What We Got Wrong \(Intellectual Honesty\)",
        r"^### C\. What We Got Wrong",
        r"^## What We Got Wrong"
    ],
    "Enigmas": [
        r"^## ❓ Enigmas",
        r"^## ❓\s+Enigmas"
    ],
    "References": [
        r"^## 📚 References",
        r"^## 📚\s+References"
    ]
}

def find_paper_boundaries(content):
    """Find where each paper starts and ends"""
    papers = []
    pattern = r'^#\s+\*\*Paper\s+(\d+):|^#\s+PAPER\s+(\d+):'
    for match in re.finditer(pattern, content, re.MULTILINE):
        paper_num = int(match.group(1) or match.group(2))
        papers.append((paper_num, match.start()))
    return sorted(papers, key=lambda x: x[0])

def extract_section_from_content(content, section_name, start_pos=0):
    """Extract a section from content"""
    patterns = SECTION_PATTERNS[section_name]
    
    for pattern in patterns:
        match = re.search(pattern, content[start_pos:], re.MULTILINE)
        if match:
            section_start = start_pos + match.start()
            # If pattern started with ---, include it
            if content[section_start:section_start+3] == '---':
                # Already included
                pass
            elif section_start > 0 and content[section_start-3:section_start] == '---':
                # Include the --- before
                section_start -= 3
            
            # Find next major header (## or #) that's not a subsection
            # Look for next ## or # that starts at beginning of line (or after ---)
            next_match = re.search(r'^(---)?(##|#)\s+', content[section_start+1:], re.MULTILINE)
            if next_match:
                # Check if it's just a subsection (###) - if so, continue
                next_header_pos = section_start + 1 + next_match.start()
                header_text = content[next_header_pos:next_header_pos+50]
                # If it's ###, it's a subsection, so look further
                if header_text.startswith('###'):
                    # Find next ## or # 
                    next_match2 = re.search(r'^(---)?(##|#)\s+', content[next_header_pos+1:], re.MULTILINE)
                    if next_match2:
                        section_end = next_header_pos + 1 + next_match2.start()
                    else:
                        section_end = len(content)
                else:
                    section_end = next_header_pos
            else:
                section_end = len(content)
            
            section_content = content[section_start:section_end].strip()
            # Remove any trailing navigation or status sections
            # Stop at Series Navigation or Paper Status
            nav_match = re.search(r'^## 📖 Series Navigation|^## 📖\s+Series Navigation|^## 🔗 Series Navigation|^Paper \d+ Status:', section_content, re.MULTILINE)
            if nav_match:
                section_content = section_content[:nav_match.start()].strip()
            
            return section_content
    return None

def get_individual_paper_file(paper_num):
    """Find the individual paper file"""
    # Try different patterns
    patterns = [
        f"Paper-{paper_num:02d}-*-FINAL.md",
        f"Paper-{paper_num:02d}-*FINAL.md",
        f"Paper-{paper_num}-*-FINAL.md",
        f"Paper-{paper_num:02d}-*.md"
    ]
    
    for pattern in patterns:
        matches = list(INDIVIDUAL_DIR.glob(pattern))
        if matches:
            return matches[0]
    
    # Try listing all files and matching
    for file in INDIVIDUAL_DIR.glob("Paper-*.md"):
        if f"Paper-{paper_num}" in file.name or f"Paper-{paper_num:02d}" in file.name:
            return file
    
    return None

def check_section_exists(content, section_name, start_pos, end_pos):
    """Check if section exists in given range"""
    section_content = content[start_pos:end_pos]
    patterns = SECTION_PATTERNS[section_name]
    
    for pattern in patterns:
        if re.search(pattern, section_content, re.MULTILINE):
            return True
    return False

def clean_encoding_issues(text):
    """Remove Chinese characters and fix encoding issues"""
    # Remove Chinese characters
    text = re.sub(r'[\u4e00-\u9fff]', '', text)
    # Remove repeated question marks or boxes
    text = re.sub(r'[？]{3,}', '', text)
    # Fix common encoding issues
    text = text.replace('脗', '')
    text = text.replace('脙', '')
    text = text.replace('脕', '')
    text = text.replace('脧', 'χ')
    text = text.replace('脦', 'Φ')
    return text

def add_missing_sections():
    """Main function to add missing sections"""
    print("Reading assembled paper...")
    with open(ASSEMBLED_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        assembled_content = f.read()
    
    # Clean encoding issues first
    print("Cleaning encoding issues...")
    assembled_content = clean_encoding_issues(assembled_content)
    
    # Find paper boundaries
    papers = find_paper_boundaries(assembled_content)
    print(f"Found {len(papers)} papers\n")
    
    # Process each paper
    changes_made = False
    
    for i, (paper_num, paper_start) in enumerate(papers):
        next_start = papers[i+1][1] if i+1 < len(papers) else len(assembled_content)
        
        print(f"Processing Paper {paper_num}...")
        
        # Get individual paper file
        individual_file = get_individual_paper_file(paper_num)
        if not individual_file:
            print(f"  ⚠ Could not find individual file for Paper {paper_num}")
            continue
        
        print(f"  Found: {individual_file.name}")
        
        # Read individual paper
        with open(individual_file, 'r', encoding='utf-8', errors='ignore') as f:
            individual_content = f.read()
        
        # Clean encoding issues
        individual_content = clean_encoding_issues(individual_content)
        
        # Check which sections are missing
        missing_sections = []
        for section_name in SECTION_PATTERNS.keys():
            if not check_section_exists(assembled_content, section_name, paper_start, next_start):
                missing_sections.append(section_name)
        
        if not missing_sections:
            print(f"  ✓ All sections present")
            continue
        
        print(f"  Missing: {', '.join(missing_sections)}")
        
        # Find insertion point (before Series Navigation or end of paper)
        insertion_point = next_start
        nav_match = re.search(r'^## 📖 Series Navigation|^## 📖\s+Series Navigation|^Paper \d+ Status:', assembled_content[paper_start:next_start], re.MULTILINE)
        if nav_match:
            insertion_point = paper_start + nav_match.start()
        
        # Extract and insert missing sections
        sections_to_add = []
        for section_name in missing_sections:
            section_content = extract_section_from_content(individual_content, section_name)
            if section_content:
                sections_to_add.append((section_name, section_content))
                print(f"    ✓ Extracted {section_name}")
            else:
                print(f"    ✗ Could not extract {section_name} from individual file")
        
        if sections_to_add:
            # Insert sections before navigation
            insert_text = "\n\n---\n\n"
            for section_name, section_content in sections_to_add:
                insert_text += section_content + "\n\n---\n\n"
            
            assembled_content = assembled_content[:insertion_point] + insert_text + assembled_content[insertion_point:]
            changes_made = True
            print(f"  ✓ Added {len(sections_to_add)} sections")
        
        print()
    
    if changes_made:
        # Write back
        print("Writing updated assembled paper...")
        with open(ASSEMBLED_PATH, 'w', encoding='utf-8') as f:
            f.write(assembled_content)
        print("✓ Done!")
    else:
        print("No changes needed.")

if __name__ == "__main__":
    add_missing_sections()

