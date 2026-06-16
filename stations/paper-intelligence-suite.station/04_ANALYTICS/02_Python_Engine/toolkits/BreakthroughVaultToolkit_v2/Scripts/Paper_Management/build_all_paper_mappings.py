#!/usr/bin/env python3
"""
Build complete image mappings for all papers by scanning organized assets
"""
import re
from pathlib import Path

ASSETS_BASE = Path("COMPLETE_LOGOS_PAPERS_FINAL/assets")

# Build mappings for all papers
all_mappings = {}

for paper_dir in sorted(ASSETS_BASE.iterdir()):
    if not paper_dir.is_dir() or paper_dir.name == "charts":
        continue
    
    match = re.match(r'P(\d+)', paper_dir.name)
    if not match:
        continue
    
    paper_num = int(match.group(1))
    all_mappings[paper_num] = {}
    
    for img_file in sorted(paper_dir.glob("*.png")):
        new_name = img_file.name
        # Create old name variants
        # Remove P1- prefix and -O-X-of-Y suffix
        desc_part = new_name.replace(f'P{paper_num}-', '').split('-O-')[0]
        
        # Common old name patterns
        old_variants = [
            new_name.replace(f'P{paper_num}-', f'P{paper_num}_').replace('-O-', '_').replace('-', '_'),
            new_name.replace(f'P{paper_num}-', '').replace('-O-', '_').replace('-', '_'),
            desc_part.replace('-', '_') + '.png',
            f'P{paper_num}_{desc_part.replace("-", "_")}.png',
        ]
        
        # Store mapping
        for old_var in old_variants:
            if old_var.endswith('.png'):
                all_mappings[paper_num][old_var] = new_name

# Print mappings for use in update script
print("IMAGE_MAPPINGS = {")
for paper_num in sorted(all_mappings.keys()):
    print(f"    {paper_num}: {{")
    for old, new in sorted(all_mappings[paper_num].items()):
        print(f'        "{old}": "{new}",')
    print("    },")
print("}")

