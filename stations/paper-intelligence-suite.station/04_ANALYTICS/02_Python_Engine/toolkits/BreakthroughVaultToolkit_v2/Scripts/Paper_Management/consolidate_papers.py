"""
Consolidate all markdown papers in P01-P14 folders into single "Final ALL.md" files
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(r"D:\THEOPHYSICS_MASTER\03_PUBLICATIONS\COMPLETE_LOGOS_PAPERS_FINAL")

# Folders to process
FOLDERS = [
    "P01-[[Theophysics_Glossary#Logos|Logos]]-Principle",
    "P02-Quantum-Bridge",
    "P03-Algorithm-Reality",
    "P04-Hard-Problem",
    "P05-Soul-Observer",
    "P06-Physics-Principalities",
    "P07-Grace-Function",
    "P08-Stretched-Heavens",
    "P09-Moral-Universe",
    "P10-Creatio-Silico",
    "P11-Protocols-Validation",
    "P12-Decalogue-Cosmos",
    "P13_Test_ Predictions",
    "P14 Aggregated Data"
]

def consolidate_folder(folder_name):
    """Consolidate all .md files in a folder into one Final ALL.md file"""
    folder_path = BASE_DIR / folder_name
    
    if not folder_path.exists():
        print(f"Folder not found: {folder_path}")
        return
    
    # Find all markdown files (excluding the output file)
    md_files = []
    for file in folder_path.glob("*.md"):
        if "Final ALL" not in file.name and "README" not in file.name:
            md_files.append(file)
    
    if not md_files:
        print(f"No markdown files found in {folder_name}")
        return
    
    # Sort files alphabetically
    md_files.sort()
    
    # Create output file
    output_file = folder_path / f"{folder_name.replace('_', '-')} Final ALL.md"
    
    print(f"\nProcessing {folder_name}...")
    print(f"Found {len(md_files)} markdown files")
    
    with open(output_file, 'w', encoding='utf-8') as outf:
        # Write header
        outf.write(f"# {folder_name.upper()}: COMPLETE COLLECTION\n\n")
        outf.write(f"**All Papers from {folder_name} Folder**\n")
        outf.write(f"**Compiled:** November 22, 2025\n")
        outf.write(f"**Papers Included:** {len(md_files)}\n\n")
        outf.write("---\n\n")
        
        # Write table of contents
        outf.write("## TABLE OF CONTENTS\n\n")
        for i, file in enumerate(md_files, 1):
            outf.write(f"{i}. [{file.stem}](#{file.stem.lower().replace(' ', '-').replace('_', '-')})\n")
        outf.write("\n---\n\n")
        
        # Write each file's content
        for i, file in enumerate(md_files, 1):
            print(f"  Adding: {file.name}")
            outf.write(f"# {i}. {file.stem.upper()}\n\n")
            outf.write(f"**Source:** `{file.name}`\n\n")
            outf.write("---\n\n")
            
            try:
                with open(file, 'r', encoding='utf-8') as inf:
                    content = inf.read()
                    outf.write(content)
            except Exception as e:
                outf.write(f"*Error reading file: {e}*\n")
            
            outf.write("\n\n---\n\n")
            outf.write(f"**END OF {file.stem.upper()}**\n\n")
            outf.write("---\n\n\n")
    
    print(f"✓ Created: {output_file.name}")
    print(f"  Size: {output_file.stat().st_size:,} bytes")

def main():
    print("=" * 70)
    print("CONSOLIDATING [[Theophysics_Glossary#Logos|LOGOS]] PAPERS P01-P14")
    print("=" * 70)
    
    for folder in FOLDERS:
        consolidate_folder(folder)
    
    print("\n" + "=" * 70)
    print("CONSOLIDATION COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()
