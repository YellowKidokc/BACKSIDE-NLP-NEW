# Workflow Guide

## Running the Analysis Pipeline

1. Start the API server:
   ```bash
   python 01_Scripts/api_server.py
   ```

2. Enable the Theophysics AI Engine plugin in Obsidian

3. Set the endpoint in plugin settings: `http://localhost:8001/analyze`

4. Run analysis via plugin command: **AI: Analyze Current Note**

## Full Vault Analysis

For comprehensive vault analysis, use the Grace Vault Manager:

```bash
python 01_Scripts/grace_vault_manager.py --cli --vault /path/to/vault --auto
```

This will:
- Scan and index all markdown files
- Compute co-occurrence statistics
- Find duplicates
- Auto-link related notes
- Generate validation metrics
