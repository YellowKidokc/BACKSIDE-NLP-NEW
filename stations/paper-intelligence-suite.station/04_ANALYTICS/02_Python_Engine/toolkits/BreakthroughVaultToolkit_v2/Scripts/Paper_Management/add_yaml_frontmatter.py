#!/usr/bin/env python3
"""
Add YAML frontmatter from YAML files to all paper files.
"""

import os
import re

base_dir = r'C:\Users\Yellowkid\Desktop\Obisidan Final\THEOPHYSICS_MASTER\06_Publication\Logos_Papers'
yaml_dir = r'D:\THEOPHYSICS_MASTER\03_PUBLICATIONS\Logos_Papers\COMPLETE_LOGOS_PAPERS_FINAL'

# Mapping of paper numbers to YAML files
yaml_mapping = {
    1: "P01_LOGOS_PRINCIPLE.yaml",
    2: "P02_QUANTUM_BRIDGE.yaml",
    3: "P03_ALGORITHM_OF_REALITY.yaml",
    4: "P04_HARD_PROBLEM.yaml",
    5: "P06_SOUL_QUANTUM_OBSERVER.yaml",  # Note: P06 YAML is for Paper 5 (Soul Observer)
    6: "P07_SPIRITUAL_WARFARE.yaml",  # Note: P07 YAML is for Paper 6 (Principalities)
    7: "P05_GRACE_FUNCTION.yaml",  # Note: P05 YAML is for Paper 7 (Grace Function)
    8: "P08_STRETCHED_HEAVENS.yaml",
    9: "P09_MORAL_UNIVERSE.yaml",
    10: "P10_CREATIO_EX_SILICO.yaml",
    11: "P11_VALIDATION_PROTOCOLS.yaml",
    12: "P12_MASTER_EQUATION.yaml"
}

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

def read_yaml_file(paper_num):
    """Read the YAML file for a paper."""
    yaml_filename = yaml_mapping.get(paper_num)
    if not yaml_filename:
        return None
    
    yaml_path = os.path.join(yaml_dir, yaml_filename)
    if not os.path.exists(yaml_path):
        print(f"  Warning: YAML file not found: {yaml_filename}")
        return None
    
    with open(yaml_path, 'r', encoding='utf-8') as f:
        return f.read()

def has_yaml_frontmatter(content):
    """Check if content already has YAML frontmatter."""
    return content.strip().startswith('---')

def add_yaml_to_file(filepath, yaml_content):
    """Add YAML frontmatter to a file if it doesn't already have it."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has YAML
    if has_yaml_frontmatter(content):
        # Check if it's the same YAML (rough check)
        if yaml_content[:100] in content:
            return False  # Already has this YAML
        else:
            # Has different YAML, replace it
            # Find where YAML ends (second ---)
            lines = content.split('\n')
            yaml_end = -1
            for i, line in enumerate(lines):
                if i > 0 and line.strip() == '---':
                    yaml_end = i
                    break
            
            if yaml_end > 0:
                # Replace existing YAML
                new_content = yaml_content + '\n' + '\n'.join(lines[yaml_end+1:])
            else:
                # Malformed, just prepend
                new_content = yaml_content + '\n\n' + content
    else:
        # No YAML, add it
        new_content = yaml_content + '\n\n' + content
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    print("Adding YAML frontmatter to all paper files...\n")
    
    for paper_num in range(1, 13):
        yaml_content = read_yaml_file(paper_num)
        if not yaml_content:
            continue
        
        folder = paper_folders[paper_num]
        folder_path = os.path.join(base_dir, folder)
        
        if not os.path.exists(folder_path):
            print(f"Paper {paper_num:02d}: Folder not found: {folder}")
            continue
        
        print(f"Paper {paper_num:02d}: Processing {folder}")
        
        # Find all markdown files in the folder
        md_files = [f for f in os.listdir(folder_path) if f.endswith('.md') and f.startswith(f'Paper-{paper_num:02d}-')]
        
        # Prioritize main paper file
        main_paper = None
        for f in md_files:
            if any(title in f for title in ['The-Logos-Principle', 'The-Quantum-Bridge', 'The-Algorithm-of-Reality',
                                            'The-Syzygy-Principle', 'The-Soul-Observer', 'A-Physics-of-Principalities',
                                            'The-Grace-Function', 'The-Stretched-Out-Heavens', 'The-Moral-Universe',
                                            'Creatio-ex-Silico', 'Protocols-for-Validation', 'The-Decalogue-of-the-Cosmos']):
                main_paper = f
                break
        
        # Add YAML to main paper
        if main_paper:
            main_path = os.path.join(folder_path, main_paper)
            if add_yaml_to_file(main_path, yaml_content):
                print(f"  Added YAML to: {main_paper}")
            else:
                print(f"  YAML already present in: {main_paper}")
        
        # Also add to section files (optional - user said "all the papers")
        for md_file in md_files:
            if md_file != main_paper:
                file_path = os.path.join(folder_path, md_file)
                if add_yaml_to_file(file_path, yaml_content):
                    print(f"  Added YAML to: {md_file}")
        
        print()

if __name__ == '__main__':
    main()

