# AI Research Agents Runtime

Runtime installs live here so the Obsidian vault stays clean.

## Installed

- `gpt-researcher`
- `local-deep-researcher`

## Vault Control Plane

Queue, prompts, and outputs live in:

`O:\_ Theophysics_Case_for_Christ\_AUTO_RESEARCH`

## Commands

Check environment keys without printing secrets:

```powershell
powershell -ExecutionPolicy Bypass -File "D:\AI-RESEARCH-AGENTS\check-env.ps1"
```

Start GPT Researcher:

```powershell
powershell -ExecutionPolicy Bypass -File "D:\AI-RESEARCH-AGENTS\start-gpt-researcher.ps1"
```

Start Local Deep Researcher:

```powershell
powershell -ExecutionPolicy Bypass -File "D:\AI-RESEARCH-AGENTS\start-local-deep-researcher.ps1"
```

GPT Researcher expects `TAVILY_API_KEY`. Local Deep Researcher can use
DuckDuckGo search by default, but needs Ollama or LM Studio running if using
the local model lane.

