# _AGENT_BRIEF.md — Template (per-NLP workflow)

**What this is:** The AI-readable mission card every workflow folder ships with. Sits next to `README.md` (which is for humans). When an AI partner runs `RUN_AGENT.bat`, this file is loaded as the workflow-specific system prompt on top of `X:\THEOPHYSICS_PRIMER.md`.

**Where it goes:** `<workflow-folder>\_AGENT_BRIEF.md`
**Companion:** `<workflow-folder>\RUN_AGENT.bat` (launcher)
**Health gate:** `<workflow-folder>\health_check.bat` (probe)

---

## Template (copy/customize for each NLP)

```markdown
# Agent Brief — <workflow-name>

**Workflow type:** NLP | conversion | router | builder | publisher
**Owner:** <David | Codex | Kimi | shared>
**Last updated:** YYYY-MM-DD

---

## Mission

<2–4 sentences. What this workflow exists to do, framed for an AI walking in cold. Not what it CAN do — what it IS for.>

---

## When to use this

- <Use case 1 — drop type X here, expect output Y>
- <Use case 2>
- <Use case 3>

---

## Available jobs

| Job | What it does | When to run |
|---|---|---|
| `RUN.bat` | <full pipeline summary> | <when, from where> |
| `RUN_AGENT.bat` | Launches an LLM with this brief loaded as system context | When you need fuzzy decisions inside the pipeline (classify, score, summarize) |
| `health_check.bat` | Verifies models reachable, paths writable, required deps present | Before any session start; called by `X:\CHECKS\RUN_ALL.bat` |
| `<custom variant>.bat` | <variant pipeline — e.g. RUN_FRUITS_OF_SPIRIT.bat> | <when> |

---

## Inputs

- **Accepted types:** <PDF, MD, HTML, TXT, YouTube URL, etc.>
- **Drop location:** `./00_DROP/`
- **Naming:** <free | `{SERIES}-{ARTICLE}[-{SUFFIX}].{ext}` | other>

## Outputs

- **Lands in:** `./OUTPUT/`
- **Shape:** <JSON + MD + HTML + Excel | single JSON manifest | etc.>
- **Downstream consumers:** <Qdrant collection X | Obsidian vault Y | website staging Z>

## Archive

- Processed inputs move to `./ARCHIVE/` after success
- Failures stay in `./00_DROP/` with a `.error.json` sibling

---

## Prompts this workflow uses

Located in `./prompts/`:

- `<prompt-name-1>.md` — <purpose>
- `<prompt-name-2>.md` — <purpose>

Python loads these via `open("./prompts/<name>.md").read()`, sends to the model, parses the response, decides the next step.

---

## Models / external services

- <DeBERTa-v3-large via D:\brain\03_DEBERTA — or local model path>
- <Ollama Mistral @ localhost:11434>
- <Infinity embeddings @ 192.168.1.177:7997>
- <Qdrant @ 192.168.1.177:6333>

If any of these are unreachable, `health_check.bat` will report — DO NOT attempt to bypass.

---

## Framework anchoring

This workflow operates inside the Theophysics framework. Load `X:\THEOPHYSICS_PRIMER.md` before any reasoning step. Specifically relevant to this workflow:

- <Law N — how it shows up here>
- <7Q Q0 (humility prior) — apply when scoring fuzzy claims>
- <Theopoetic format — if output is public-facing>

If a workflow output contradicts canon: stop, flag in `OUTPUT/<id>.contradiction.json`, do NOT propagate.

---

## When you're stuck

1. Read `README.md` for the human-facing contract
2. Read `config.json` for paths and model names
3. Read `_LOGS/` for last few successful runs to understand expected output shape
4. Run `health_check.bat` — if it fails, that's your starting point
5. Still stuck — post to comms hub `workflow-<N>` channel (the room for active multi-AI work) with `[<your-callsign>] BLOCKED: <one-sentence>`

---

## Don't do

- Don't write to `ARCHIVE/` — pipeline-managed only
- Don't bypass `00_DROP/` by injecting into `OUTPUT/` directly
- Don't modify `config.json` without testing on a copy
- Don't delete files — use `_ARCHIVE/` (no-delete rule)
- Don't introduce hardcoded `D:\` paths — `D:\BIL` and `D:\FAP` are deprecated as of Phase 5
- Don't push past the Feb 14, 2026 Boundary Proof — see PRIMER §4

---

## Escalation

- Architectural questions: post to `workflow-<N>` channel
- Canon contradictions: post to `broadcast`, tag David
- Model behavior unexpected: log full request/response in `_LOGS/`, flag in `workflow-<N>`
```

---

## Per-NLP customization notes

When 4a generates these for the 9 NLPs, fill in the workflow-specific values from each NLP's existing `config.json` + `pipeline.py` + `README.md`. Do not invent — quote what's there. If a field can't be filled, mark `<TBD — David to confirm>` and flag in the rollout log.

**Workflows that need the full brief (active NLPs):**

- axioms
- knowledge-refinery
- paper-proof-grader
- link-pull-drop
- session-handoff-drop
- ai-portal-generator
- ollama (light variant — utility, not full pipeline)

**Workflows that don't need a brief (publish-only):**

- proof-architecture
- proof-explorer
