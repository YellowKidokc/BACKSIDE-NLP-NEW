import httpx
import sys
import os

# Read the paper text
paper_file = r"D:\GitHub\Treaties\temp_paper.txt"
with open(paper_file, 'r', encoding='utf-8', errors='replace') as f:
    text = f.read()

print(f"Paper length: {len(text)} chars")

# Step 1: Ingest via paste endpoint
print("Step 1: Ingesting paper...")
with httpx.Client(timeout=60) as client:
    resp = client.post("http://127.0.0.1:8000/papers/paste", data={
        "title": "GTQ-05: The Substrate Fractured",
        "authors": "David Lowe",
        "year": "2026",
        "text": text,
    }, follow_redirects=False)
    print(f"  Ingest status: {resp.status_code}")
    # Get paper ID from redirect location
    if resp.status_code == 303:
        loc = resp.headers.get('location', '')
        paper_id = loc.split('/')[-2] if '/view' in loc else loc.split('/')[-1]
        print(f"  Paper ID: {paper_id}")
    else:
        print(f"  Response: {resp.text[:200]}")
        # Try to get the latest paper ID
        papers = client.get("http://127.0.0.1:8000/papers").json()
        paper_id = papers[0]['id'] if papers else None
        print(f"  Latest paper ID: {paper_id}")

if not paper_id:
    print("ERROR: Could not determine paper ID")
    sys.exit(1)

# Step 2: Run full pipeline
print(f"\nStep 2: Running o3 pipeline on paper {paper_id}...")
print("  This may take 1-2 minutes...")
with httpx.Client(timeout=600) as client:
    resp = client.post(f"http://127.0.0.1:8000/papers/{paper_id}/run-all")
    print(f"  Status: {resp.status_code}")
    print(f"  Result: {resp.text[:500]}")

print(f"\nDone! View at: http://127.0.0.1:8000/papers/{paper_id}/view")
print(f"Snapshot at: http://127.0.0.1:8000/papers/{paper_id}/snapshot")