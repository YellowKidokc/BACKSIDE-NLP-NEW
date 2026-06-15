import httpx
import sys

paper_id = int(sys.argv[1]) if len(sys.argv) > 1 else 3

print(f"Running full pipeline on paper {paper_id}...")
print("This calls o3 multiple times — may take 30-60 seconds...")

try:
    with httpx.Client(timeout=300) as client:
        resp = client.post(f"http://127.0.0.1:8000/papers/{paper_id}/run-all")
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text}")
except Exception as e:
    print(f"ERROR: {e}")
