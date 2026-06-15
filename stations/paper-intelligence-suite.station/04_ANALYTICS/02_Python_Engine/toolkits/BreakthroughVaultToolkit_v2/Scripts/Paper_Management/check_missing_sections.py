#!/usr/bin/env python3
"""
Check which sections are missing for each paper.
"""

import os
import re

base_dir = r'C:\Users\Yellowkid\Desktop\Obisidan Final\THEOPHYSICS_MASTER\06_Publication\Logos_Papers'

# Expected sections for each paper type
expected_sections = {
    'main': ['The-Logos-Principle', 'The-Quantum-Bridge', 'The-Algorithm-of-Reality', 
             'The-Syzygy-Principle', 'The-Soul-Observer', 'A-Physics-of-Principalities',
             'The-Grace-Function', 'The-Stretched-Out-Heavens', 'The-Moral-Universe',
             'Creatio-ex-Silico', 'Protocols-for-Validation', 'The-Decalogue-of-the-Cosmos'],
    'evidence': 'Evidence-and-Validation',
    'enigmas': 'Enigmas',
    'what_wrong': 'What-We-Got-Wrong',
    'frameworks': 'Frameworks-Combined',
    'references': 'References',
    'acknowledgments': 'Acknowledgments'
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

def check_paper_sections(paper_num):
    """Check what sections exist for a paper."""
    folder = paper_folders.get(paper_num)
    if not folder:
        return None
    
    folder_path = os.path.join(base_dir, folder)
    if not os.path.exists(folder_path):
        return None
    
    files = [f for f in os.listdir(folder_path) if f.endswith('.md') and f.startswith(f'Paper-{paper_num:02d}-')]
    
    sections = {
        'main': False,
        'evidence': False,
        'enigmas': False,
        'what_wrong': False,
        'frameworks': False,
        'references': False,
        'acknowledgments': False
    }
    
    for filename in files:
        if 'Evidence-and-Validation' in filename:
            sections['evidence'] = True
        elif 'Enigmas' in filename:
            sections['enigmas'] = True
        elif 'What-We-Got-Wrong' in filename:
            sections['what_wrong'] = True
        elif 'Frameworks-Combined' in filename:
            sections['frameworks'] = True
        elif 'References' in filename:
            sections['references'] = True
        elif 'Acknowledgments' in filename:
            sections['acknowledgments'] = True
        elif any(title in filename for title in expected_sections['main']):
            sections['main'] = True
    
    return sections

def main():
    print("Checking for missing sections:\n")
    
    for paper_num in range(1, 13):
        sections = check_paper_sections(paper_num)
        if sections:
            missing = []
            if not sections['main']:
                missing.append('Main Paper')
            if not sections['evidence']:
                missing.append('Evidence & Validation')
            if not sections['enigmas']:
                missing.append('Enigmas')
            if not sections['what_wrong']:
                missing.append('What We Got Wrong')
            if paper_num == 1 and not sections['frameworks']:
                missing.append('Frameworks Combined')
            if not sections['references']:
                missing.append('References')
            if not sections['acknowledgments']:
                missing.append('Acknowledgments')
            
            if missing:
                print(f"Paper {paper_num:02d} ({paper_folders[paper_num]}):")
                print(f"  Missing: {', '.join(missing)}")
                print()

if __name__ == '__main__':
    main()

