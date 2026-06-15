# Theophysics Paper Intelligence Docker Runner

Private-local packaging for the paper grader, 7Q forward/reverse audit, and
scientific paper snapshot layer.

## What It Runs

- Deterministic paper grader across a folder of HTML/Markdown/text papers
- Excel/JSON outputs from the existing paper-intelligence suite
- Optional local Ollama 7Q/snapshot pass
- Postgres concept-ledger schema export

## Folder Contract

Inside the container:

```text
/data/input   papers to grade
/data/output  generated results
```

On Windows with Docker:

```powershell
docker build -t theophysics/paper-intelligence:local .
docker run --rm `
  -v "C:\Users\lowes\OneDrive\Desktop\genesis-to-quantum:/data/input:ro" `
  -v "C:\paper-intelligence-runs:/data/output" `
  theophysics/paper-intelligence:local grade --pattern "*.html"
```

## Commands

Run deterministic grader only:

```powershell
docker run --rm -v "C:\path\papers:/data/input:ro" -v "C:\path\out:/data/output" theophysics/paper-intelligence:local grade
```

Run local Ollama 7Q/snapshot only:

```powershell
docker run --rm `
  -e OLLAMA_URL="http://host.docker.internal:11434/api/generate" `
  -e OLLAMA_MODEL="qwen2.5:3b" `
  -v "C:\path\papers:/data/input:ro" `
  -v "C:\path\out:/data/output" `
  theophysics/paper-intelligence:local 7q --pattern "*.html"
```

Run deterministic grader plus 7Q/snapshot:

```powershell
docker run --rm `
  -e OLLAMA_URL="http://host.docker.internal:11434/api/generate" `
  -v "C:\path\papers:/data/input:ro" `
  -v "C:\path\out:/data/output" `
  theophysics/paper-intelligence:local all --pattern "*.html"
```

Generate HTML scorecards from the latest grader JSON:

```powershell
docker run --rm `
  -v "C:\path\out:/data/output" `
  theophysics/paper-intelligence:local report
```

Export the Postgres schema file:

```powershell
docker run --rm -v "C:\path\out:/data/output" theophysics/paper-intelligence:local schema
```

## Expected Outputs

```text
/data/output/grader/
  paper_intelligence_master_*.xlsx
  paper_intelligence_rows_*.json
  paper_intelligence_summary_*.json

/data/output/html_reports/
  PI_*.html

/data/output/ollama_7q/
  *_OLLAMA_7Q_*.json
  *_OLLAMA_7Q_*.md
  ollama_7q_manifest_*.json

/data/output/schema_concept_system.sql
```

## Notes

- The Docker image does not publish anything to GitHub.
- The deterministic grader works offline after the image is built.
- The 7Q/snapshot layer needs an Ollama server reachable from the container.
- For reproducibility, keep the same model name and runner settings.
- Docker Desktop may not write cleanly to mapped NAS drives like `T:`. For test runs,
  write to a normal local folder such as `C:\paper-intelligence-runs`, then copy
  outputs to NAS/private storage after the run.
