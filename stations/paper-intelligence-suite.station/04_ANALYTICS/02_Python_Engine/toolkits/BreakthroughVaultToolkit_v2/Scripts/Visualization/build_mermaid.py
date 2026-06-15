#!/usr/bin/env python3
"""
build_mermaid.py - Generate Mermaid diagrams from extracted data.

Usage:
    python build_mermaid.py [--input INPUT] [--output OUTPUT]
"""

import json
import argparse
from pathlib import Path
from datetime import datetime


def load_json(filepath):
    """Load JSON file safely."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def generate_axiom_flowchart(axioms):
    """Generate Mermaid flowchart for axiom chain."""
    if not axioms:
        return "```mermaid\nflowchart TD\n    Empty[No axioms found]\n```"

    # Sort by number
    sorted_axioms = sorted(axioms, key=lambda x: x.get('number', 0))

    # Build flowchart
    lines = ["```mermaid", "flowchart TD"]

    # Group by level
    levels = {
        'L1': (1, 3, 'Existence'),
        'L2': (4, 7, 'Properties'),
        'L3': (8, 11, 'Origin'),
        'L4': (12, 15, 'Source'),
        'L5': (16, 18, 'Moral'),
        'L6': (19, 20, 'Identity'),
        'L7': (21, 22, 'Alternative'),
        'L8': (23, 24, 'Gap')
    }

    for level_id, (start, end, name) in levels.items():
        level_axioms = [a for a in sorted_axioms if start <= a.get('number', 0) <= end]
        if level_axioms:
            lines.append(f"    subgraph {level_id}[Level {level_id[-1]}: {name}]")
            for ax in level_axioms:
                ax_id = ax.get('id', f"A{ax.get('number', 0)}")
                # Truncate statement for display
                stmt = ax.get('statement', '')[:30] + '...' if len(ax.get('statement', '')) > 30 else ax.get('statement', '')
                lines.append(f'        {ax_id}["{ax_id}: {stmt}"]')
            lines.append("    end")

    # Add connections between levels
    for i, (level_id, (start, end, name)) in enumerate(list(levels.items())[:-1]):
        next_level = list(levels.keys())[i + 1]
        # Get last axiom of current level and first of next
        current_axioms = [a for a in sorted_axioms if start <= a.get('number', 0) <= end]
        next_start, next_end, _ = levels[next_level]
        next_axioms = [a for a in sorted_axioms if next_start <= a.get('number', 0) <= next_end]

        if current_axioms and next_axioms:
            last_current = current_axioms[-1].get('id', f"A{end}")
            first_next = next_axioms[0].get('id', f"A{next_start}")
            lines.append(f"    {last_current} --> {first_next}")

    lines.append("```")
    return "\n".join(lines)


def generate_tag_network(tags):
    """Generate Mermaid graph for tag relationships."""
    if not tags:
        return "```mermaid\ngraph LR\n    Empty[No tags found]\n```"

    lines = ["```mermaid", "graph LR"]

    # Categorize
    categories = {
        'Physics': [],
        'Theology': [],
        'Mathematics': [],
        'Information': [],
        'Consciousness': [],
        'Other': []
    }

    category_keywords = {
        'Physics': ['quantum', 'entropy', 'field', 'wave', 'particle'],
        'Theology': ['grace', 'sin', 'logos', 'trinity', 'scripture'],
        'Mathematics': ['axiom', 'theorem', 'equation', 'proof'],
        'Information': ['information', 'complexity', 'compression'],
        'Consciousness': ['consciousness', 'observer', 'mind', 'soul']
    }

    for tag in tags:
        tag_lower = tag.lower()
        found = False
        for cat, keywords in category_keywords.items():
            if any(kw in tag_lower for kw in keywords):
                categories[cat].append(tag)
                found = True
                break
        if not found:
            categories['Other'].append(tag)

    # Build subgraphs
    for cat, cat_tags in categories.items():
        if cat_tags:
            lines.append(f"    subgraph {cat}")
            for tag in cat_tags[:5]:  # Limit to 5 per category
                safe_tag = tag.replace('-', '_').replace(' ', '_')
                lines.append(f'        {safe_tag}["#{tag}"]')
            lines.append("    end")

    lines.append("```")
    return "\n".join(lines)


def generate_link_diagram(links):
    """Generate Mermaid diagram for link relationships."""
    internal = links.get('internal', [])
    external = links.get('external', [])

    lines = ["```mermaid", "graph TD"]
    lines.append("    subgraph Internal[Internal Links]")
    for i, link in enumerate(internal[:10]):  # Limit
        safe_link = link.replace(' ', '_').replace('/', '_')[:20]
        lines.append(f'        I{i}["{safe_link}"]')
    lines.append("    end")

    lines.append("    subgraph External[External Links]")
    for i, link in enumerate(external[:5]):  # Limit
        domain = link.split('/')[2] if len(link.split('/')) > 2 else link[:20]
        lines.append(f'        E{i}["{domain}"]')
    lines.append("    end")

    lines.append("```")
    return "\n".join(lines)


def update_mermaid_dashboard(axioms, tags, links, dashboard_path):
    """Update Mermaid_Maps.md dashboard."""
    template = f"""---
uid: DA-mermaid-dashboard
type: dashboard
created: 2025-11-29
updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
purpose: Visual connection maps for current paper
---

# Connection Maps

> Auto-generated Mermaid diagrams. Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## Axiom Chain

{generate_axiom_flowchart(axioms)}

---

## Tag Network

{generate_tag_network(tags)}

---

## Link Map

{generate_link_diagram(links)}

---

*Auto-generated by `build_mermaid.py`*
"""

    with open(dashboard_path, 'w', encoding='utf-8') as f:
        f.write(template)


def main():
    parser = argparse.ArgumentParser(description='Generate Mermaid diagrams')
    parser.add_argument('--input', type=str, help='Master_Sheet folder path')
    parser.add_argument('--output', type=str, help='Dashboard output path')
    args = parser.parse_args()

    script_dir = Path(__file__).parent
    master_sheet = Path(args.input) if args.input else script_dir.parent / 'Master_Sheet'
    dashboard = Path(args.output) if args.output else script_dir.parent / 'Dashboards' / 'Mermaid_Maps.md'

    print(f"[build_mermaid] Reading from: {master_sheet}")

    # Load data
    axioms = load_json(master_sheet / 'Axioms.json')
    tags = load_json(master_sheet / 'Tags.json')
    links = load_json(master_sheet / 'Links.json')

    # Update dashboard
    update_mermaid_dashboard(axioms, tags, links, dashboard)

    print(f"[build_mermaid] Mermaid diagrams generated!")
    print(f"  Axioms mapped: {len(axioms)}")
    print(f"  Tags mapped: {len(tags)}")
    print(f"[build_mermaid] Dashboard updated: {dashboard}")


if __name__ == '__main__':
    main()
