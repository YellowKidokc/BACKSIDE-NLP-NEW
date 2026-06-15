"""Consolidate P01 papers"""
from pathlib import Path

base = Path(r'D:\THEOPHYSICS_MASTER\03_PUBLICATIONS\COMPLETE_LOGOS_PAPERS_FINAL')
folder = base / 'P01-[[Theophysics_Glossary#Logos|Logos]]-Principle'

if not folder.exists():
    print(f"Folder not found: {folder}")
    exit(1)

md_files = [f for f in folder.glob('*.md') if 'Final ALL' not in f.name and 'README' not in f.name]
md_files.sort()

output = folder / 'P01 Final ALL.md'

print(f'Processing P01-[[Theophysics_Glossary#Logos|Logos]]-Principle...')
print(f'Found {len(md_files)} markdown files')

with open(output, 'w', encoding='utf-8') as out:
    out.write('# P01-[[Theophysics_Glossary#Logos|LOGOS]]-PRINCIPLE: COMPLETE COLLECTION\n\n')
    out.write('**All Papers from P01-[[Theophysics_Glossary#Logos|Logos]]-Principle Folder**\n')
    out.write('**Compiled:** November 22, 2025\n')
    out.write(f'**Papers Included:** {len(md_files)}\n\n')
    out.write('---\n\n')
    out.write('## TABLE OF CONTENTS\n\n')
    
    for i, f in enumerate(md_files, 1):
        out.write(f'{i}. [{f.stem}](#{f.stem.lower().replace(" ", "-").replace("_", "-")})\n')
    out.write('\n---\n\n')
    
    for i, f in enumerate(md_files, 1):
        print(f'  Adding: {f.name}')
        out.write(f'# {i}. {f.stem.upper()}\n\n')
        out.write(f'**Source:** `{f.name}`\n\n')
        out.write('---\n\n')
        
        with open(f, 'r', encoding='utf-8') as inf:
            out.write(inf.read())
        
        out.write('\n\n---\n\n')
        out.write(f'**END OF {f.stem.upper()}**\n\n')
        out.write('---\n\n\n')

print(f'✓ Created: {output.name}')
print(f'  Size: {output.stat().st_size:,} bytes')
