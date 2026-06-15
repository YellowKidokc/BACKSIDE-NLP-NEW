# PIL Build Prompt — Hand this to Claude Code
# Claude Code will read this and execute everything top to bottom

You are the foreman for the Personal Intelligence Layer (PIL) project.
Your job is to build, install, and wire everything described below.
Work autonomously. Fix errors as they come. Don't ask for permission on small decisions.

---

## CONTEXT

David has an existing system at D:\BIL\ that includes:
- BIL server (behavioral preference engine) at D:\BIL\behavioral-intelligence-layer-OBS-Plugin-Final-Claude\
- Browser extension at D:\BIL\browser\
- Desktop capture scripts at D:\BIL\desktop-capture\
- Data folders at D:\BIL\data\
- A Synology NAS at 192.168.1.177 running Docker, Ollama (:11434), Postgres, n8n, SearXNG

The README at D:\BIL\README.md has the full architecture.
The docker-compose.yml at D:\BIL\docker-compose.yml has the engine stack.

---

## YOUR TASKS — DO THESE IN ORDER

### TASK 1 — Install Phase 1 Python deps
```
pip install mss keyboard pillow requests pystray pywin32 sentence-transformers chromadb
```
Confirm each installs without error. Fix any version conflicts.

### TASK 2 — Pull Ollama vision models
```
ollama pull moondream
ollama pull llava
```
Confirm both pull successfully.

### TASK 3 — Add /bil/github endpoint to BIL server
File: D:\BIL\behavioral-intelligence-layer-OBS-Plugin-Final-Claude\bil\bil_server.py

Add a new POST handler at /bil/github that:
- Receives GitHub repo data (repo name, stars, forks, language, topics, time_on_page, copied_code, bookmarked)
- Logs it to D:\BIL\data\github\github_events.jsonl
- Extracts features and sends to BIL web model as a scored signal
- Returns {"status": "ok", "repo": repo_name, "score": score}

Signal scoring for GitHub:
- base signal = 0.3 (visited)
- +0.2 if copied_code
- +0.2 if bookmarked
- +0.1 if time_on_page > 60
- +0.1 if time_on_page > 180
- cap at 1.0

### TASK 4 — Test BIL server + new endpoint
Start BIL server:
```
cd D:\BIL\behavioral-intelligence-layer-OBS-Plugin-Final-Claude
python -m bil.bil_server
```
Test with curl:
```
curl -X POST http://localhost:8420/bil/github -H "Content-Type: application/json" -d "{\"repo\":\"test/repo\",\"stars\":\"100\",\"language\":\"Python\",\"time_on_page\":120,\"copied_code\":true}"
```
Confirm 200 response.

### TASK 5 — Test hotkey capture
Run:
```
python D:\BIL\desktop-capture\hotkey_capture.py
```
Press Ctrl+Shift+S. Confirm:
- Screenshot saved to D:\BIL\data\captures\
- describe_one.py called, description saved to D:\BIL\data\understood\
- Rating file created at D:\BIL\data\ratings\ratings.jsonl after rating

### TASK 6 — Test passive watcher
Run for 10 seconds to confirm it doesn't crash:
```
python D:\BIL\desktop-capture\watcher.py
```
Confirm screenshot + description saved.

### TASK 7 — Deploy Docker engines on NAS
SSH or use available tools to deploy on 192.168.1.177.
Copy D:\BIL\docker-compose.yml to /volume1/PIL/docker-compose.yml on NAS.

Deploy in this order (don't deploy all at once):
1. qdrant (vector DB — no dependencies)
2. open-webui (image understander UI)
3. infinity (embedding service)
4. gpt-researcher (research agent)
5. ragflow LAST — it's heavy, needs MySQL + ES

For each: confirm container is running and port responds.

### TASK 8 — Wire embedding service into BIL
Once infinity is running on :7997, add a helper to BIL:

File: D:\BIL\engines\embeddings\text_embedder.py
```python
import requests

INFINITY_URL = "http://192.168.1.177:7997"

def embed_text(text: str) -> list:
    r = requests.post(f"{INFINITY_URL}/embeddings", json={
        "input": [text],
        "model": "sentence-transformers/all-MiniLM-L6-v2"
    }, timeout=10)
    return r.json()["data"][0]["embedding"]
```

Test it returns a vector.

### TASK 9 — Create START_PIL.bat
Update D:\BIL\START_PIL.bat to start:
1. BIL server
2. Hotkey capture
3. Watcher

All in separate windows. Confirm it runs without errors.

### TASK 10 — Final status report
Print a clean summary:
- Which services are running and on what ports
- Which tasks completed vs failed
- What needs manual intervention (NAS SSH, etc.)
- Suggested next steps

---

## RULES

- Work in D:\BIL\ unless otherwise specified
- If a port conflicts with existing services, pick the next available port and document it
- If Ollama isn't running, start it before pulling models
- If NAS SSH isn't available, skip Task 7 and document it clearly
- The BIL server is Python — don't rewrite it in another language
- Don't touch anything in D:\BIL\behavioral-intelligence-layer-OBS-Plugin-Final-Claude\ except bil_server.py
- Log everything to D:\BIL\data\logs\claude_code_build.log as you go
- When done, post a session summary to the comms hub:
  curl -X POST https://ai-comms-hub.davidokc28.workers.dev/channel/claude-code \
    -H "Content-Type: application/json" \
    -d '{"to":"broadcast","content":"PIL Phase 1 build complete. [YOUR SUMMARY HERE]","priority":"high","category":"session-log"}'

---

## FILES TO READ FIRST

Before starting, read these in order:
1. D:\BIL\README.md
2. D:\BIL\behavioral-intelligence-layer-OBS-Plugin-Final-Claude\bil\bil_server.py
3. D:\BIL\docker-compose.yml
4. D:\BIL\desktop-capture\hotkey_capture.py

Go.
