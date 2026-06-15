"""
08_CLAIMS: Claim Extractor
Reads MD/HTML files from a folder, extracts claim-level blocks,
classifies each one, and writes results to JSON for the export step.

Usage:
    python extract.py <folder_path> [--recursive] [--format md|html|both]
    
Examples:
    python extract.py "O:\_Theophysics_v5\04_THEOPYHISCS" --recursive --format md
    python extract.py "K:\Folders\LEAN4\canonical" --format md
    python extract.py "T:\MASTER_EQUATION_TEST\theophysics-math" --recursive --format md
"""
import os, sys, re, json, hashlib, argparse
from datetime import datetime
from pathlib import Path

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

SCRIPT_DIR = Path(__file__).parent
CONFIG = json.loads((SCRIPT_DIR / "config.json").read_text(encoding="utf-8-sig"))
OUTPUT_DIR = Path(CONFIG["output_dir"])
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR = Path(CONFIG["log_dir"])
LOG_DIR.mkdir(parents=True, exist_ok=True)

SIGNALS = CONFIG["claim_signals"]
MIN_LEN = CONFIG["min_claim_length"]
MAX_LEN = CONFIG["max_claim_length"]

def content_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

def extract_frontmatter(text):
    if text.startswith("---"):
        end = text.find("---", 3)
        if end > 0 and HAS_YAML:
            try:
                fm = yaml.safe_load(text[3:end])
                return fm, text[end+3:].strip()
            except:
                pass
    return {}, text

def split_md_sections(text):
    sections = []
    current_heading = "PREAMBLE"
    current_lines = []
    for line in text.split("\n"):
        m = re.match(r'^(#{1,4})\s+(.+)', line)
        if m:
            if current_lines:
                sections.append((current_heading, "\n".join(current_lines).strip()))
            current_heading = m.group(2).strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_lines:
        sections.append((current_heading, "\n".join(current_lines).strip()))
    return sections

def extract_claims_from_text(text, source_file, section_heading=""):
    claims = []
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    # Group into claim-sized blocks (1-3 sentences)
    i = 0
    while i < len(sentences):
        block = sentences[i].strip()
        # Try to build a meaningful block
        j = i + 1
        while j < min(i + 3, len(sentences)) and len(block) < MIN_LEN:
            block += " " + sentences[j].strip()
            j += 1
        
        block = block.strip()
        if len(block) < MIN_LEN:
            i = j
            continue
        if len(block) > MAX_LEN:
            block = block[:MAX_LEN] + "..."
        
        # Skip purely structural/formatting content
        if re.match(r'^[\s\-\*\|\#\>\`]+$', block):
            i = j
            continue
        
        # Classify
        classification = classify_claim(block)
        
        claim_id = content_hash(block)
        claims.append({
            "claim_id": claim_id,
            "source_file": str(source_file),
            "section": section_heading,
            "text": block,
            "classification": classification,
            "confidence": score_confidence(block, classification),
            "length": len(block),
            "has_equation": bool(re.search(r'[=∫∑∏∂∇≡≠≤≥]|\\frac|\\int|\\sum', block)),
            "has_scripture_ref": bool(re.search(r'\b(?:Genesis|Exodus|Matthew|John|Romans|Ephesians|Revelation|Psalm|Isaiah|Hebrews|Corinthians|Galatians)\s+\d', block)),
        })
        i = j
    
    return claims

def classify_claim(text):
    text_lower = text.lower()
    scores = {}
    for cls, keywords in SIGNALS.items():
        score = sum(1 for kw in keywords if kw.lower() in text_lower)
        if score > 0:
            scores[cls] = score
    
    if not scores:
        # Heuristic fallbacks
        if re.search(r'[=∫∑∏]', text):
            return "EQUATION"
        if re.search(r'\d+\s*σ|\bp\s*[<>=]', text):
            return "EVIDENCE"
        return "UNCLASSIFIED"
    
    best = max(scores, key=scores.get)
    return best.upper()

def score_confidence(text, classification):
    if classification == "UNCLASSIFIED":
        return 0.1
    text_lower = text.lower()
    hits = sum(1 for kw in SIGNALS.get(classification.lower(), []) if kw.lower() in text_lower)
    return min(0.3 + hits * 0.2, 0.9)

def process_md_file(filepath):
    text = Path(filepath).read_text(encoding="utf-8", errors="replace")
    frontmatter, body = extract_frontmatter(text)
    sections = split_md_sections(body)
    
    all_claims = []
    for heading, content in sections:
        if not content.strip():
            continue
        claims = extract_claims_from_text(content, filepath, heading)
        all_claims.extend(claims)
    
    return {
        "doc_id": content_hash(str(filepath)),
        "source_file": str(filepath),
        "frontmatter": frontmatter if frontmatter else None,
        "total_claims": len(all_claims),
        "claims": all_claims
    }

def process_html_file(filepath):
    if not HAS_BS4:
        print(f"  SKIP {filepath} (bs4 not installed)")
        return None
    
    text = Path(filepath).read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(text, "html.parser")
    
    # Remove script/style
    for tag in soup.find_all(["script", "style", "nav", "footer"]):
        tag.decompose()
    
    all_claims = []
    
    # Process by section headings
    headings = soup.find_all(re.compile(r'^h[1-4]$'))
    if headings:
        for i, h in enumerate(headings):
            heading_text = h.get_text(strip=True)
            # Get content until next heading
            content_parts = []
            for sib in h.find_next_siblings():
                if sib.name and re.match(r'^h[1-4]$', sib.name):
                    break
                t = sib.get_text(strip=True)
                if t:
                    content_parts.append(t)
            content = " ".join(content_parts)
            if content:
                claims = extract_claims_from_text(content, filepath, heading_text)
                all_claims.extend(claims)
    else:
        # No headings, just extract from body text
        body_text = soup.get_text(separator=" ", strip=True)
        all_claims = extract_claims_from_text(body_text, filepath, "BODY")
    
    return {
        "doc_id": content_hash(str(filepath)),
        "source_file": str(filepath),
        "frontmatter": None,
        "total_claims": len(all_claims),
        "claims": all_claims
    }

def main():
    parser = argparse.ArgumentParser(description="Extract claims from MD/HTML files")
    parser.add_argument("folder", help="Folder to scan")
    parser.add_argument("--recursive", "-r", action="store_true", help="Scan subdirectories")
    parser.add_argument("--format", "-f", choices=["md", "html", "both"], default="both", help="File format to process")
    args = parser.parse_args()
    
    folder = Path(args.folder)
    if not folder.exists():
        print(f"ERROR: {folder} does not exist")
        sys.exit(1)
    
    # Collect files
    extensions = []
    if args.format in ("md", "both"):
        extensions.append(".md")
    if args.format in ("html", "both"):
        extensions.append(".html")
    
    files = []
    if args.recursive:
        for ext in extensions:
            files.extend(folder.rglob(f"*{ext}"))
    else:
        for ext in extensions:
            files.extend(folder.glob(f"*{ext}"))
    
    files = sorted(set(files))
    print(f"Found {len(files)} files in {folder}")
    
    # Process
    results = []
    total_claims = 0
    for i, f in enumerate(files):
        print(f"  [{i+1}/{len(files)}] {f.name}...", end=" ")
        try:
            if f.suffix == ".md":
                doc = process_md_file(f)
            elif f.suffix == ".html":
                doc = process_html_file(f)
            else:
                continue
            
            if doc:
                results.append(doc)
                total_claims += doc["total_claims"]
                print(f"{doc['total_claims']} claims")
            else:
                print("skipped")
        except Exception as e:
            print(f"ERROR: {e}")
    
    # Write output
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"claims_{run_id}.json"
    
    output = {
        "run_id": run_id,
        "source_folder": str(folder),
        "recursive": args.recursive,
        "format": args.format,
        "files_processed": len(results),
        "total_claims": total_claims,
        "classification_distribution": {},
        "documents": results
    }
    
    # Count distribution
    dist = {}
    for doc in results:
        for c in doc["claims"]:
            cls = c["classification"]
            dist[cls] = dist.get(cls, 0) + 1
    output["classification_distribution"] = dict(sorted(dist.items(), key=lambda x: -x[1]))
    
    output_file.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    
    print(f"\n{'='*60}")
    print(f"DONE: {len(results)} files, {total_claims} claims extracted")
    print(f"Output: {output_file}")
    print(f"\nClassification distribution:")
    for cls, count in sorted(dist.items(), key=lambda x: -x[1]):
        print(f"  {cls}: {count}")
    print(f"\nNext step: python export_excel.py {output_file}")

if __name__ == "__main__":
    main()
