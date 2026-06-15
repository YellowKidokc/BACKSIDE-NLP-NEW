#!/usr/bin/env python3
"""
Extract missing sections from FINAL paper files and add them to paper folders.
"""

import os
import re

base_dir = r'C:\Users\Yellowkid\Desktop\Obisidan Final\THEOPHYSICS_MASTER\06_Publication\Logos_Papers'
final_dir = os.path.join(base_dir, 'COMPLETE_LOGOS_PAPERS_FINAL')

paper_folders = {
    1: "P01-Logos-Principle",
    2: "P02-Quantum-Bridge",
    3: "P03-Algorithm-Reality",
    4: "P04-Hard-Problem",
    5: "P05-Soul-Observer",
    6: "P06-Physics-Principalities",
    7: "P07-Grace-Function",
    8: "P08-Stretched-Heavens",
    9: "P09-Moral-Universe",
    10: "P10-Creatio-Silico",
    11: "P11-Protocols-Validation",
    12: "P12-Decalogue-Cosmos"
}

section_markers = {
    'evidence': [
        r'^##.*How Right We Are',
        r'^##.*Evidence.*Validation',
        r'^##.*Evidence',
        r'芒艙鈥.*Evidence'
    ],
    'enigmas': [
        r'^##.*Enigmas',
        r'^##.*What We Don.*Understand',
        r'芒聺鈥.*Enigmas'
    ],
    'what_wrong': [
        r'^##.*What We Got Wrong',
        r'^##.*What We.*Wrong',
        r'^##.*Where We.*Wrong',
        r'芒拧聽茂赂聫.*Wrong'
    ],
    'frameworks': [
        r'^##.*Relationship.*Frameworks',
        r'^##.*Connection.*Frameworks',
        r'^##.*Frameworks.*Combined',
        r'^##.*Existing Frameworks'
    ],
    'references': [
        r'^##.*References',
        r'冒鸥鈥溑.*References'
    ],
    'acknowledgments': [
        r'^##.*Acknowledgments',
        r'冒鸥鈥鈩⒙.*Acknowledgments'
    ]
}

section_names = {
    'evidence': 'Evidence-and-Validation',
    'enigmas': 'Enigmas',
    'what_wrong': 'What-We-Got-Wrong',
    'frameworks': 'Frameworks-Combined',
    'references': 'References',
    'acknowledgments': 'Acknowledgments'
}

def find_section(lines, section_type):
    """Find a section in the lines."""
    patterns = section_markers[section_type]
    start_idx = None
    
    for i, line in enumerate(lines):
        for pattern in patterns:
            if re.search(pattern, line, re.I):
                start_idx = i
                break
        if start_idx is not None:
            break
    
    if start_idx is None:
        return None, None
    
    # Find the end of this section (next major section or end of file)
    end_idx = len(lines)
    for i in range(start_idx + 1, len(lines)):
        line = lines[i]
        # Check if this is the start of another major section
        if re.match(r'^#+\s+(PAPER|CERTIFICATION|FINAL CONCLUSION)', line):
            end_idx = i
            break
        # Check if this is another section marker
        for other_type, other_patterns in section_markers.items():
            if other_type != section_type:
                for pattern in other_patterns:
                    if re.search(pattern, line, re.I):
                        end_idx = i
                        break
                if end_idx < len(lines):
                    break
        if end_idx < len(lines):
            break
    
    return start_idx, end_idx

def extract_and_save_section(paper_num, final_file_path, section_type):
    """Extract a section from FINAL file and save it."""
    with open(final_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    start_idx, end_idx = find_section(lines, section_type)
    
    if start_idx is None:
        return False
    
    # Extract the section
    section_lines = lines[start_idx:end_idx]
    section_content = ''.join(section_lines)
    
    # Add title if not present
    if not section_content.startswith('#'):
        section_content = f"# {section_names[section_type]}\n\n{section_content}"
    
    # Save to paper folder
    target_folder = os.path.join(base_dir, paper_folders[paper_num])
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    
    target_file = os.path.join(target_folder, f"Paper-{paper_num:02d}-{section_names[section_type]}.md")
    
    # Check if file already exists
    if os.path.exists(target_file):
        print(f"  Paper {paper_num:02d}: {section_names[section_type]} already exists, skipping")
        return False
    
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(section_content)
    
    print(f"  Paper {paper_num:02d}: Extracted {section_names[section_type]}")
    return True

def main():
    print("Scanning FINAL papers for missing sections...\n")
    
    for paper_num in range(1, 13):
        final_file = os.path.join(final_dir, f"Paper-{paper_num:02d}-{paper_folders[paper_num].split('-')[1].replace('_', '-')}-FINAL.md")
        
        # Handle naming variations
        if not os.path.exists(final_file):
            # Try alternative naming
            alt_names = [
                f"Paper-{paper_num:02d}-The-{paper_folders[paper_num].split('-')[1]}-FINAL.md",
                f"Paper-{paper_num:02d}-{paper_folders[paper_num].split('-')[1]}-FINAL.md"
            ]
            for alt_name in alt_names:
                alt_path = os.path.join(final_dir, alt_name)
                if os.path.exists(alt_path):
                    final_file = alt_path
                    break
        
        # Handle specific paper names
        if paper_num == 1 and not os.path.exists(final_file):
            final_file = os.path.join(final_dir, "Paper-01-The-Logos-Principle-FINAL.md")
        elif paper_num == 2 and not os.path.exists(final_file):
            final_file = os.path.join(final_dir, "Paper-02-The-Quantum-Bridge-FINAL.md")
        elif paper_num == 3 and not os.path.exists(final_file):
            final_file = os.path.join(final_dir, "Paper-03-The-Algorithm-of-Reality-FINAL.md")
        elif paper_num == 4 and not os.path.exists(final_file):
            final_file = os.path.join(final_dir, "Paper-04-The-Hard-Problem-of-Consciousness-FINAL.md")
        elif paper_num == 5 and not os.path.exists(final_file):
            final_file = os.path.join(final_dir, "Paper-05-The-Soul-Observer-FINAL.md")
        elif paper_num == 6 and not os.path.exists(final_file):
            final_file = os.path.join(final_dir, "Paper-06-A-Physics-of-Principalities-FINAL.md")
        elif paper_num == 7 and not os.path.exists(final_file):
            final_file = os.path.join(final_dir, "Paper-07-The-Grace-Function-FINAL.md")
        elif paper_num == 8 and not os.path.exists(final_file):
            final_file = os.path.join(final_dir, "Paper-08-The-Stretched-Out-Heavens-FINAL.md")
        elif paper_num == 9 and not os.path.exists(final_file):
            final_file = os.path.join(final_dir, "Paper-09-The-Moral-Universe-FINAL.md")
        elif paper_num == 10 and not os.path.exists(final_file):
            final_file = os.path.join(final_dir, "Paper-10-Creatio-ex-Silico-FINAL.md")
        elif paper_num == 11 and not os.path.exists(final_file):
            final_file = os.path.join(final_dir, "Paper-11-Protocols-for-Validation-FINAL.md")
        elif paper_num == 12 and not os.path.exists(final_file):
            final_file = os.path.join(final_dir, "Paper-12-The-Decalogue-of-the-Cosmos-FINAL.md")
        
        if not os.path.exists(final_file):
            print(f"Paper {paper_num:02d}: FINAL file not found")
            continue
        
        print(f"Paper {paper_num:02d}: Scanning {os.path.basename(final_file)}")
        
        # Check each section type
        for section_type in section_markers.keys():
            extract_and_save_section(paper_num, final_file, section_type)
        
        print()

if __name__ == '__main__':
    main()

