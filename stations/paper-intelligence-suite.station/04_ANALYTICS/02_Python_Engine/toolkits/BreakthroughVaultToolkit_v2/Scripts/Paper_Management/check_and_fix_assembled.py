import re
import os
from pathlib import Path

# Paths
ASSEMBLED_PATH = Path(r"C:\Users\Yellowkid\Desktop\Obisidan Final\THEOPHYSICS_MASTER\06_Publication\Logos_Papers\COMPLETE_LOGOS_PAPERS_FINAL\THEOPHYSICS_MASTER_PAPER_ASSEMBLED.md")
INDIVIDUAL_DIR = Path(r"C:\Users\Yellowkid\Desktop\Obisidan Final\THEOPHYSICS_MASTER\06_Publication\Logos_Papers\COMPLETE_LOGOS_PAPERS_FINAL")

# Sections to check for
SECTION_HEADERS = {
    "Hypotheses": [r"## 🎯 Hypotheses", r"## 🎯\s+Hypotheses"],
    "Lexicon": [r"## 📖 Lexicon", r"## 📖\s+Lexicon"],
    "Evidence": [r"## ✅ How Right We Are", r"## ✅ Evidence", r"## ✅ Evidence & Validation"],
    "What We Got Wrong": [r"### E\. What We Got Wrong", r"### C\. What We Got Wrong", r"## What We Got Wrong"],
    "Enigmas": [r"## ❓ Enigmas", r"## ❓\s+Enigmas"],
    "References": [r"## 📚 References", r"## 📚\s+References"]
}

def find_paper_boundaries(content):
    """Find where each paper starts in the assembled file"""
    papers = []
    # Look for paper headers like "# **Paper 1:" or "# PAPER 1:"
    pattern = r'^#\s+\*\*Paper\s+(\d+):|^#\s+PAPER\s+(\d+):'
    for match in re.finditer(pattern, content, re.MULTILINE):
        paper_num = int(match.group(1) or match.group(2))
        papers.append((paper_num, match.start()))
    return sorted(papers, key=lambda x: x[0])

def extract_section_content(content, section_regexes, start_pos=0):
    """Extract content of a section until next major header"""
    for regex in section_regexes:
        match = re.search(regex, content[start_pos:], re.MULTILINE)
        if match:
            section_start = start_pos + match.start()
            # Find next major header (## or #) or end of file
            next_header = re.search(r'^(##|#)\s+', content[section_start+1:], re.MULTILINE)
            if next_header:
                section_end = section_start + 1 + next_header.start()
            else:
                section_end = len(content)
            return content[section_start:section_end].strip()
    return None

def check_encoding_issues(content):
    """Check for Chinese characters or encoding issues"""
    issues = []
    # Check for common Chinese characters
    chinese_pattern = r'[\u4e00-\u9fff]'
    matches = list(re.finditer(chinese_pattern, content))
    if matches:
        issues.append(f"Found {len(matches)} Chinese characters")
        # Show first few examples
        for i, match in enumerate(matches[:5]):
            context = content[max(0, match.start()-20):match.end()+20]
            issues.append(f"  Example {i+1}: ...{context}...")
    
    # Check for garbled text (repeated question marks, boxes, etc.)
    garbled_pattern = r'[]{2,}|[？]{3,}'
    garbled = list(re.finditer(garbled_pattern, content))
    if garbled:
        issues.append(f"Found {len(garbled)} potential encoding issues")
    
    return issues

def check_paper_sections(assembled_content, paper_num, paper_start, next_paper_start=None):
    """Check which sections are present after a paper"""
    if next_paper_start:
        paper_content = assembled_content[paper_start:next_paper_start]
    else:
        paper_content = assembled_content[paper_start:]
    
    found_sections = {}
    for section_name, regexes in SECTION_HEADERS.items():
        found = False
        for regex in regexes:
            if re.search(regex, paper_content, re.MULTILINE):
                found = True
                break
        found_sections[section_name] = found
    
    return found_sections

def get_individual_paper_path(paper_num):
    """Get path to individual paper file"""
    # Try different naming patterns
    patterns = [
        f"Paper-{paper_num:02d}-*-FINAL.md",
        f"Paper-{paper_num:02d}-*FINAL.md",
        f"Paper-{paper_num}-*-FINAL.md"
    ]
    
    for pattern in patterns:
        matches = list(INDIVIDUAL_DIR.glob(pattern))
        if matches:
            return matches[0]
    return None

def extract_sections_from_individual(paper_path):
    """Extract all sections from individual paper"""
    if not paper_path or not paper_path.exists():
        return {}
    
    with open(paper_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    sections = {}
    for section_name, regexes in SECTION_HEADERS.items():
        section_content = extract_section_content(content, regexes)
        if section_content:
            sections[section_name] = section_content
    
    return sections

# Main execution
print("Checking assembled paper for issues...\n")

with open(ASSEMBLED_PATH, 'r', encoding='utf-8', errors='ignore') as f:
    assembled_content = f.read()

# Check encoding issues
print("=" * 60)
print("ENCODING ISSUES:")
print("=" * 60)
encoding_issues = check_encoding_issues(assembled_content)
if encoding_issues:
    for issue in encoding_issues:
        print(issue)
else:
    print("✓ No obvious encoding issues found")
print()

# Check sections for each paper
print("=" * 60)
print("SECTION CHECK:")
print("=" * 60)
papers = find_paper_boundaries(assembled_content)
print(f"Found {len(papers)} papers\n")

missing_sections_report = {}

for i, (paper_num, paper_start) in enumerate(papers):
    next_start = papers[i+1][1] if i+1 < len(papers) else len(assembled_content)
    
    print(f"Paper {paper_num}:")
    found = check_paper_sections(assembled_content, paper_num, paper_start, next_start)
    
    missing = []
    for section_name, is_present in found.items():
        status = "✓" if is_present else "✗"
        print(f"  {status} {section_name}")
        if not is_present:
            missing.append(section_name)
    
    if missing:
        missing_sections_report[paper_num] = missing
        print(f"  → Missing: {', '.join(missing)}")
    
    print()

print("=" * 60)
print("SUMMARY:")
print("=" * 60)
if missing_sections_report:
    print(f"Papers with missing sections: {list(missing_sections_report.keys())}")
    for paper_num, missing in missing_sections_report.items():
        print(f"  Paper {paper_num}: {', '.join(missing)}")
else:
    print("✓ All sections appear to be present!")

