"""
Create master document combining all P01-P14 Final ALL files
"""
from pathlib import Path

base = Path(r'D:\THEOPHYSICS_MASTER\03_PUBLICATIONS\COMPLETE_LOGOS_PAPERS_FINAL')

# List of all Final ALL files in order
final_all_files = [
    'P01-[[Theophysics_Glossary#Logos|Logos]]-Principle\\P01 Final ALL.md',
    'P02-Quantum-Bridge/P02-Quantum-Bridge Final ALL.md',
    'P03-Algorithm-Reality/P03-Algorithm-Reality Final ALL.md',
    'P04-Hard-Problem/P04-Hard-Problem Final ALL.md',
    'P05-Soul-Observer/P05-Soul-Observer Final ALL.md',
    'P06-Physics-Principalities/P06-Physics-Principalities Final ALL.md',
    'P07-Grace-Function/P07-Grace-Function Final ALL.md',
    'P08-Stretched-Heavens/P08-Stretched-Heavens Final ALL.md',
    'P09-Moral-Universe/P09-Moral-Universe Final ALL.md',
    'P10-Creatio-Silico/P10-Creatio-Silico Final ALL.md',
    'P11-Protocols-Validation/P11-Protocols-Validation Final ALL.md',
    'P12-Decalogue-Cosmos/P12-Decalogue-Cosmos Final ALL.md',
    'P13_Test_ Predictions/P13-Test- Predictions Final ALL.md',
    'P14 Aggregated Data/P14 Aggregated Data Final ALL.md'
]

output_file = base / '1-14 Final ALL.md'

print("=" * 70)
print("CREATING MASTER DOCUMENT: 1-14 Final ALL.md")
print("=" * 70)

with open(output_file, 'w', encoding='utf-8') as out:
    # Write master header
    out.write('# COMPLETE [[Theophysics_Glossary#Logos|LOGOS]] PAPERS: P01-P14 MASTER COLLECTION\n\n')
    out.write('**The Complete Theophysics Paper Series**\n\n')
    out.write('**Authors:** David Lowe & Claude (Anthropic)\n\n')
    out.write('**Compiled:** November 22, 2025\n\n')
    out.write('**Papers:** P01 through P14 (All papers from each folder)\n\n')
    out.write('---\n\n')
    
    # Write master table of contents
    out.write('## MASTER TABLE OF CONTENTS\n\n')
    for i, file_path in enumerate(final_all_files, 1):
        folder_name = file_path.split('/')[0]
        out.write(f'{i}. [{folder_name}](#{folder_name.lower().replace(" ", "-").replace("_", "-")})\n')
    out.write('\n---\n\n')
    
    # Combine all files
    for i, file_path in enumerate(final_all_files, 1):
        full_path = base / file_path
        
        if not full_path.exists():
            print(f'⚠️  File not found: {file_path}')
            continue
        
        folder_name = file_path.split('/')[0]
        print(f'\n{i}. Adding: {folder_name}')
        print(f'   Source: {file_path}')
        print(f'   Size: {full_path.stat().st_size:,} bytes')
        
        out.write(f'\n\n{"=" * 80}\n')
        out.write(f'# PAPER COLLECTION {i}: {folder_name.upper()}\n')
        out.write(f'{"=" * 80}\n\n')
        out.write(f'**Source:** `{file_path}`\n\n')
        out.write('---\n\n')
        
        try:
            with open(full_path, 'r', encoding='utf-8') as inf:
                content = inf.read()
                out.write(content)
        except Exception as e:
            out.write(f'*Error reading file: {e}*\n')
        
        out.write('\n\n---\n\n')
        out.write(f'**END OF {folder_name.upper()}**\n\n')
        out.write(f'{"=" * 80}\n\n')

print("\n" + "=" * 70)
print("MASTER DOCUMENT CREATED SUCCESSFULLY")
print("=" * 70)
print(f'\n✓ Created: {output_file.name}')
print(f'  Location: {output_file}')
print(f'  Size: {output_file.stat().st_size:,} bytes')
print(f'  Size: {output_file.stat().st_size / (1024*1024):.2f} MB')
