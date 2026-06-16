import json
import os
import re # Still needed for re.search for axiom/law headers and for create_term_vector regex matching
import unicodedata # For Unicode normalization

def clean_brackets(text):
    """Replaces common Unicode variants of square brackets with ASCII equivalents."""
    text = text.replace('［', '[').replace('］', ']') # Full-width brackets
    text = text.replace('〔', '[').replace('〕', ']') # CJK brackets
    text = text.replace('〚', '[').replace('〛', ']') # Double square brackets (rare, but possible)
    text = text.replace('\uFF3B', '[').replace('\uFF3D', ']') # Full-width brackets Unicode
    text = text.replace('\u27E6', '[').replace('\u27E7', ']') # Mathematical white square brackets
    text = text.replace('\u201a', "'").replace('\u201b', "'").replace('\u201c', '"').replace('\u201d', '"') # Smart quotes
    return text

# Purely string-based link extraction function (reverted to original logic, without hex dump)
def extract_links_from_text_pure_string(text):
    """Extracts all Obsidian links from a given text block using pure string manipulation."""
    extracted_concepts = set()
    
    start_tag = "[["
    end_tag = "]]"
    
    current_pos = 0
    
    while True:
        start_index = text.find(start_tag, current_pos)
        if start_index == -1:
            break
        
        end_index = text.find(end_tag, start_index + len(start_tag))
        if end_index == -1:
            break
            
        link_raw = text[start_index + len(start_tag) : end_index]
        
        if '|' in link_raw:
            concept = link_raw.split('|')[0].strip()
        else:
            concept = link_raw.strip()
            
        if concept and '#' not in concept and concept != '→':
            extracted_concepts.add(concept)
            
        current_pos = end_index + len(end_tag)
            
    return extracted_concepts

def extract_blocks_internal(file_path, header_keyword):
    """Internal function to extract blocks of text and their key concepts."""
    blocks = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []

    header_indices = [i for i, line in enumerate(lines) if line.strip().startswith(header_keyword)]
    
    if not header_indices:
        return []

    for i, start_index in enumerate(header_indices):
        header_line = lines[start_index].strip()
        
        block_end_index = len(lines)
        for j in range(start_index + 1, len(lines)):
            line = lines[j].strip()
            if line.startswith(header_keyword) or line.startswith('---'):
                block_end_index = j
                break
        
        content_start_index = start_index + 1
        while content_start_index < block_end_index and not lines[content_start_index].strip():
            content_start_index += 1

        axiom_text_content = "".join(lines[content_start_index : block_end_index]).strip()
        
        full_block_for_links = header_line + '\n' + axiom_text_content
        
        # --- NEW: Aggressive Unicode Normalization (moved earlier) ---
        # Clean problematic bracket characters first
        full_block_for_links = clean_brackets(full_block_for_links)
        
        # Then convert to NFKD (Compatibility Decomposition), encode to ASCII (ignoring errors), then decode to UTF-8
        # This will convert many non-ASCII characters to their closest ASCII equivalents
        full_block_for_links = unicodedata.normalize('NFKD', full_block_for_links).encode('ascii', 'ignore').decode('utf-8')
        # --- End Unicode Normalization ---

        # Remove ALL occurrences of BOM character (not just at start)
        full_block_for_links = full_block_for_links.replace('\ufeff', '')
        
        cleaned_concepts = sorted(list(extract_links_from_text_pure_string(full_block_for_links)))

        axiom_num = 0
        axiom_name = "Unknown"

        axiom_num_match = re.search(r'AXIOM\s+(\d+)', header_line)
        if axiom_num_match:
            axiom_num = int(axiom_num_match.group(1))
            name_match = re.search(r'\|([^\\]+)\]\]', header_line) # Corrected regex to escape backslash
            axiom_name = name_match.group(1).strip() if name_match else f"Axiom {axiom_num}"
        else:
            law_num_match = re.search(r'Law\s+(\d+):\s+(.*)', header_line)
            if law_num_match:
                axiom_num = int(law_num_match.group(1))
                axiom_name = f"Law {axiom_num}: {law_num_match.group(2).strip()}"


        blocks.append({
            "number": axiom_num,
            "name": axiom_name,
            "header": header_line,
            "content": axiom_text_content,
            "key_concepts": cleaned_concepts
        })
        
    return blocks

def load_json_list(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError as e:
        print(f"Error: Could not find glossary file: {file_path}. {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Could not decode JSON from {file_path}. {e}")
        return None

def create_term_vector(text, glossary_terms):
    """
    Creates a set of glossary terms found within the given text.
    """
    found_terms = set()
    for term in glossary_terms:
        # Use regex to find whole words, case-insensitive
        # This regex should be fine as it's not the problematic [[...]]
        if re.search(r'\b' + re.escape(term) + r'\b', text, re.IGNORECASE):
            found_terms.add(term)
    return found_terms

def analyze_correlation_semantic(base_file, target_file, master_glossary_path, output_dir):
    """
    Analyzes the semantic correlation between two files based on shared glossary terms in their content.
    """
    # Load profiles using the internal extraction logic
    base_items = extract_blocks_internal(base_file, "**AXIOM")
    target_items = extract_blocks_internal(target_file, "### Law")

    master_glossary_list = load_json_list(master_glossary_path)

    if base_items is None or not base_items or target_items is None or not target_items or master_glossary_list is None:
        print(f"Error: One or more input profiles or glossary could not be loaded or were empty.")
        return

    glossary_terms = master_glossary_list # Now it's a flat list of terms
    print(f"\nDEBUG: Loaded Glossary Terms ({len(glossary_terms)}): {glossary_terms}")

    correlation_report = {
        "base_profile_source": os.path.basename(base_file),
        "target_profile_source": os.path.basename(target_file),
        "correlations": []
    }

    total_coherence_score = 0
    num_compared_items = 0

    for target_item in target_items:
        target_text = target_item.get("content", "") + " " + target_item.get("header", "")
        target_item_concepts = set(target_item.get("key_concepts", []))
        if not target_item_concepts: # If no explicit links, try to find glossary terms in content
            print(f"DEBUG: No explicit links found in Target Item '{target_item.get('name')}', falling back to create_term_vector.")
            target_item_concepts = create_term_vector(target_text, glossary_terms)
        
        best_match = {
            "target_item_name": target_item.get("name", "Unknown"),
            "target_item_header": target_item.get("header", ""),
            "top_matching_base_item_name": "None",
            "top_matching_base_item_header": "None",
            "coherence_score": 0,
            "shared_terms": sorted(list(target_item_concepts)) # Start with terms found in target
        }

        if not target_item_concepts:
            correlation_report["correlations"].append(best_match)
            continue

        for base_item in base_items:
            base_text = base_item.get("content", "") + " " + base_item.get("header", "")
            base_item_concepts = set(base_item.get("key_concepts", []))
            if not base_item_concepts: # If no explicit links, try to find glossary terms in content
                print(f"DEBUG: No explicit links found in Base Item '{base_item.get('name')}', falling back to create_term_vector.")
                base_item_concepts = create_term_vector(base_text, glossary_terms)
            
            if not base_item_concepts:
                continue

            intersection_set = target_item_concepts.intersection(base_item_concepts)
            union_set = target_item_concepts.union(base_item_concepts)

            # DEBUG PRINTS for comparison (removed from main loop to reduce verbosity, keep for local debugging)
            # print(f"\n--- Comparing Target: {target_item.get('name')} with Base: {base_item.get('name')} ---")
            # print(f"Target Concepts ({len(target_item_concepts)}): {target_item_concepts}")
            # print(f"Base Concepts for '{base_item.get('name')}' ({len(base_item_concepts)}): {base_item_concepts}")
            # print(f"Intersection Length: {len(intersection_set)}")
            # print(f"Union Length: {len(union_set)}")
            # print(f"Shared Terms: {sorted(list(intersection_set))}")

            # Jaccard similarity based on shared glossary terms or extracted concepts
            intersection = len(intersection_set)
            union = len(union_set)
            
            coherence_score = intersection / union if union > 0 else 0
            
            if coherence_score > best_match["coherence_score"]:
                best_match["top_matching_base_item_name"] = base_item.get("name", "Unknown")
                best_match["top_matching_base_item_header"] = base_item.get("header", "")
                best_match["coherence_score"] = round(coherence_score, 4)
                best_match["shared_terms"] = sorted(list(intersection_set))

        correlation_report["correlations"].append(best_match)
        total_coherence_score += best_match["coherence_score"]
        num_compared_items += 1
    
    correlation_report["average_coherence_score"] = round(total_coherence_score / num_compared_items, 4) if num_compared_items > 0 else 0

    output_filename = f"semantic_correlation_report_{os.path.splitext(os.path.basename(target_file))[0]}.json"
    output_path = os.path.join(output_dir, output_filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(correlation_report, f, indent=4, ensure_ascii=False)

    print(f"\nSemantic correlation report created at: {output_path}")
    print(f"Average Coherence Score: {correlation_report['average_coherence_score']}")

if __name__ == "__main__":
    base_md_file = r"D:\\THEOPHYSICS_MASTER\\02_LIBRARY\\THE CONSCIOUSNESS AXIOMS All.md"
    target_md_file = r"D:\\THEOPHYSICS_MASTER\\03_PUBLICATIONS\\COMPLETE_LOGOS_PAPERS_FINAL\\P01-Logos-Principle\\Paper-1-The-Logos-Principle-CANONICAL.md"
    master_glossary = r"D:\\THEOPHYSICS_MASTER\\00_VAULT_SYSTEM\\04_Analysis\\Master Sheets\\master_glossary_hardcoded.json"
    output_directory = r"D:\\THEOPHYSICS_MASTER\\00_VAULT_SYSTEM\\04_Analysis\\Data Analytics"
    
    analyze_correlation_semantic(base_md_file, target_md_file, master_glossary, output_directory)
