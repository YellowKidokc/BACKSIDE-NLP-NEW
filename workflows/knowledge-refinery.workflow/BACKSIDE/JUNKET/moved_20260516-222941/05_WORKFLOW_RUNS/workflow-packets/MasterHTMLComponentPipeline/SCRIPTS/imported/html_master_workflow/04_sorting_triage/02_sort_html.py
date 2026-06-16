import os

def categorize_html(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(2000)
            
        lower_content = content.lower()
        has_doctype = '<!doctype html>' in lower_content
        has_html = '<html' in lower_content
        has_head = '<head' in lower_content
        has_style = '<style' in lower_content or '<link rel="stylesheet"' in lower_content
        is_obsidian = 'obsidian.css' in lower_content or 'markdown-preview' in lower_content or 'site-lib' in lower_content
        
        if not has_doctype and not has_html and not has_head:
            return "Snippet (Bad - White Background)"
        if is_obsidian:
            return "Obsidian Export (Keep - Purple Background)"
        if has_doctype and has_style:
            return "Website Ready (Keep - Custom Theme)"
        return "Unknown/Edge Case"
    except Exception:
        return "Error"

root_dir = r'.'
results = {
    "Website Ready (Keep - Custom Theme)": [],
    "Obsidian Export (Keep - Purple Background)": [],
    "Snippet (Bad - White Background)": [],
    "Unknown/Edge Case": []
}

print("Starting scan...")
count = 0
for root, dirs, files in os.walk(root_dir):
    # Skip some large known folders to speed up if needed, but let's try full scan first
    if '_LIVE_DEPLOY' in root or '.git' in root:
        continue
        
    for file in files:
        if file.endswith('.html'):
            full_path = os.path.join(root, file)
            category = categorize_html(full_path)
            if category in results:
                results[category].append(full_path)
            else:
                results["Unknown/Edge Case"].append(full_path)
            
            count += 1
            if count % 100 == 0:
                print(f"Processed {count} files...")

for category, paths in results.items():
    print(f"\n=== {category} ({len(paths)} files) ===")
    for p in paths[:20]:
        print(f"  {p}")
    if len(paths) > 20:
        print(f"  ... and {len(paths) - 20} more")
