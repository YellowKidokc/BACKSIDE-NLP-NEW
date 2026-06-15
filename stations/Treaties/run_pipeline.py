import sys

import httpx


paper_id = int(sys.argv[1]) if len(sys.argv) > 1 else 3

print(f"Running full pipeline on paper {paper_id}...")
print("This calls the configured LLM backend multiple times and may take 30-90 seconds...")

try:
    with httpx.Client(timeout=300) as client:
        resp = client.post(f"http://127.0.0.1:8000/papers/{paper_id}/run-all")
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text}")
        resp.raise_for_status()

        axioms = client.get("http://127.0.0.1:8000/axioms")
        axioms.raise_for_status()
        print("Refreshing axiom HTML pages...")
        for axiom in axioms.json():
            snap = client.post(f"http://127.0.0.1:8000/axioms/{axiom['id']}/snapshot")
            print(f"  axiom {axiom['id']}: {snap.status_code} {snap.text}")
            snap.raise_for_status()

        export = client.post("http://127.0.0.1:8000/exports/structured")
        print(f"Structured export: {export.status_code} {export.text}")
        export.raise_for_status()
except Exception as e:
    print(f"ERROR: {e}")
