# Prompt 4a — Folder convention rollout

**Owner:** Codex
**Risk:** Low (only file creation + folder rename with junctions)
**Depends on:** Nothing
**Blocks:** 4b (root simplification needs convention locked first)

---

## Goal

Honor the 3-layer folder contract from `X:\FOLDER_CONVENTIONS.md` across X:\ root:

1. **Layer 1:** generate `README.md` for the 15 folders that don't have one.
2. **Layer 2:** rename intake folders inside the 9 NLPs to `00_DROP/` (junctions at old names preserve current scripts).
3. **Layer 2:** add the `Pipeline contract` block to each workflow folder's README.
4. **Layer 2 (new):** generate `_AGENT_BRIEF.md`, `RUN_AGENT.bat`, `health_check.bat`, and `prompts/` directory for each active NLP — using `_AGENT_BRIEF_TEMPLATE.md` as the source.

---

## Pre-conditions

- `X:\FOLDER_CONVENTIONS.md` exists and is the canonical spec (read it first).
- `X:\ARCHITECTURE.md` exists with the 11 Mermaid maps for context.
- These root folders have README today (skip them): 00_WORKFLOWS, ai-portal-generator, axioms, Backside, BIL, David, knowledge-refinery, paper-proof-grader.

## Required outcome

### Stage 1 — Layer 1 READMEs (15 folders)

Create `<folder>\README.md` for each, using the L1 template from FOLDER_CONVENTIONS.md:

```markdown
# <folder-name>

**What this is:** <one sentence, inferred from folder contents>
**Owner:** <best guess: David, shared, Codex, claude-code-forge, or specific AI>
**Status:** live | archive | experimental | placeholder
**Last updated:** 2026-05-16

<1–2 paragraphs context>

## What's inside
- `<child>` — <one line>
- ...
```

Folders to create READMEs for (infer purpose from contents — sample 5 child names + the largest 3 files):

| Folder | Hint |
|---|---|
| `C4C` | Obsidian vault — Case for Christ apologetics. Has `00-START-HERE`, `.obsidian/`, 21 topic folders. README should point to `00-START-HERE/`. |
| `C4C-wiki` | Companion wiki with `raw/`, `wiki/`, `wiki/.drafts/` and `vault-schema.md`. |
| `captures` | Raw drops from external tools (currently has `links/`). Inbound staging. |
| `digests` | Pipeline output — session handoff summaries, BART/SBERT digests. |
| `embeddings` | Local Qdrant-style vector store (`.dat`, `.mappings`, `.versions`). |
| `FAP` | Folder Automation Pipeline scaffold (11 stage subfolders, all empty today). |
| `github` | Local clones of GitHub repos used by the brain. |
| `link-pull-drop` | NLP — YouTube transcript + web fetch. **Also needs L2 block (Stage 3).** |
| `models` | Cached ML model weights (Whisper, SBERT, DeBERTa pointers). |
| `ollama` | Ollama Mistral session-handoff scripts. **Also needs L2-light block.** |
| `proof-architecture` | Static HTML output (no L2 — publish-only). |
| `proof-explorer` | Static HTML output (no L2 — publish-only). |
| `ratings` | Purpose unclear from filename alone — inspect contents, write honest README. If unknown, status=experimental and flag for David. |
| `session-handoff-drop` | NLP — pastes processed by Mistral. **Also needs L2 block.** |
| `theophysics-comms-hub` | Comms hub API docs (single README inside today). |

### Stage 2 — Rename intake folders to `00_DROP/` + junctions

For each NLP, rename its current intake folder to `00_DROP/` and create an NTFS junction at the old name pointing to the new one:

| NLP | Old name | New name | Junction at old name |
|---|---|---|---|
| `axioms` | `00_INBOX_DROP_PAPERS_HERE/` | `00_DROP/` | yes |
| `knowledge-refinery` | `00_INTAKE/` | `00_DROP/` | yes |
| `paper-proof-grader` | `INPUT/` + `DROP_PAPERS_HERE/` | `00_DROP/` (merge both — copy files in, dedupe by hash) | yes, both |
| `link-pull-drop` | external `X:\captures\links\DROP_HERE/` | new `X:\link-pull-drop\00_DROP/` | leave captures path alone |
| `session-handoff-drop` | `DROP_HERE/` | `00_DROP/` | yes |
| `ai-portal-generator` | none | `00_DROP/` (create empty) | n/a |
| `proof-architecture`, `proof-explorer` | none | skip — publish-only | n/a |

Junction command pattern:
```powershell
cmd /c mklink /J "X:\<nlp>\<old_name>" "X:\<nlp>\00_DROP"
```

### Stage 3 — Add Layer 2 block to workflow READMEs

For each of axioms, knowledge-refinery, paper-proof-grader, link-pull-drop, session-handoff-drop, ai-portal-generator, ollama: append (or insert below L1 fields) the `## Pipeline contract` + `## What happens` block per FOLDER_CONVENTIONS.md.

Use existing `config.json` / `RUN.bat` / `pipeline.py` to fill in the contract fields. Don't invent — quote what's there.

### Stage 4 — Generate `_AGENT_BRIEF.md` + `RUN_AGENT.bat` + `health_check.bat` per active NLP

For each active NLP (axioms, knowledge-refinery, paper-proof-grader, link-pull-drop, session-handoff-drop, ai-portal-generator, ollama):

**1. `<nlp>/_AGENT_BRIEF.md`** — start from `_AGENT_BRIEF_TEMPLATE.md` (in this prompts dir). Fill placeholders from the NLP's existing `config.json` + `pipeline.py` + `README.md`. Do not invent values — for fields that can't be sourced, write `<TBD — David to confirm>` and log it.

**2. `<nlp>/RUN_AGENT.bat`** — launcher that loads `X:\THEOPHYSICS_PRIMER.md` + `./_AGENT_BRIEF.md` as system context, then drops into an interactive session with Ollama (default model: configurable in `config.json` under `agent_model`, default `mistral:7b-instruct`).

Reference shape:
```batch
@echo off
REM Launches an LLM session with this workflow's mission loaded.
REM Combines X:\THEOPHYSICS_PRIMER.md (framework floor) + ./_AGENT_BRIEF.md (workflow mission).

setlocal
set "PRIMER=X:\THEOPHYSICS_PRIMER.md"
set "BRIEF=%~dp0_AGENT_BRIEF.md"
set "MODEL=mistral:7b-instruct"

REM Read config override if present
if exist "%~dp0config.json" (
  for /f "delims=" %%i in ('powershell -NoP -C "(Get-Content '%~dp0config.json' | ConvertFrom-Json).agent_model" 2^>nul') do set "MODEL=%%i"
)

REM Stitch system prompt
set "SYS_TMP=%TEMP%\agent_sys_%RANDOM%.txt"
type "%PRIMER%" > "%SYS_TMP%"
echo. >> "%SYS_TMP%"
echo --- >> "%SYS_TMP%"
echo. >> "%SYS_TMP%"
type "%BRIEF%" >> "%SYS_TMP%"

REM Launch Ollama with system prompt
ollama run %MODEL% --system "$(type '%SYS_TMP%')"

del "%SYS_TMP%" 2>nul
endlocal
```

**3. `<nlp>/health_check.bat`** — read-only probe, exits 0/1/2 (PASS/FAIL/WARN). Must validate:
- Required files exist: `README.md`, `_AGENT_BRIEF.md`, `RUN.bat`, `config.json`, `00_DROP/`, `OUTPUT/`, `ARCHIVE/`
- Models/services reachable (read from `config.json`): if `config.json` lists `model_endpoint`, ping it
- `00_DROP/` writable (touch test, then delete touch file)
- Last run log present in `_LOGS/` (warn if older than 7 days)

Reference shape:
```batch
@echo off
setlocal enabledelayedexpansion
set "EXIT_CODE=0"
set "WARNINGS=0"

REM Required files
for %%f in (README.md _AGENT_BRIEF.md RUN.bat config.json) do (
  if not exist "%~dp0%%f" (
    echo FAIL: missing %%f
    set "EXIT_CODE=1"
  )
)

REM Required dirs
for %%d in (00_DROP OUTPUT ARCHIVE) do (
  if not exist "%~dp0%%d" (
    echo FAIL: missing dir %%d
    set "EXIT_CODE=1"
  )
)

REM Write probe on 00_DROP
echo probe > "%~dp000_DROP\.health_probe" 2>nul
if exist "%~dp000_DROP\.health_probe" (
  del "%~dp000_DROP\.health_probe"
) else (
  echo FAIL: 00_DROP not writable
  set "EXIT_CODE=1"
)

REM Model endpoint probe (if config defines one)
for /f "delims=" %%i in ('powershell -NoP -C "(Get-Content '%~dp0config.json' | ConvertFrom-Json).model_endpoint" 2^>nul') do set "ENDPOINT=%%i"
if defined ENDPOINT (
  curl -s -o nul -w "%%{http_code}" --max-time 5 "%ENDPOINT%" > "%TEMP%\probe_%RANDOM%.txt"
  set /p HTTP_CODE=<"%TEMP%\probe_%RANDOM%.txt"
  if "!HTTP_CODE!"=="200" (
    echo OK: %ENDPOINT% reachable
  ) else (
    echo WARN: %ENDPOINT% returned !HTTP_CODE!
    set "WARNINGS=1"
  )
)

if "%EXIT_CODE%"=="0" (
  if "%WARNINGS%"=="1" (
    echo OVERALL: WARN
    exit /b 2
  ) else (
    echo OVERALL: PASS
    exit /b 0
  )
) else (
  echo OVERALL: FAIL
  exit /b 1
)
```

**4. `<nlp>/prompts/`** — create empty directory with a `.gitkeep` if no existing prompt templates exist. If the NLP already calls LLMs from inline Python strings, flag in log so a follow-up can extract them to `.md` files (don't do that extraction in 4a — separate concern).

---

## Acceptance check

```powershell
# All 23 root folders (minus #recycle, _LOGS, _brain_DEPRECATED) have README.md
$missing = Get-ChildItem 'X:\' -Directory | Where-Object { $_.Name -notmatch '^(#recycle|_brain_DEPRECATED|_LOGS)' -and -not (Test-Path "$($_.FullName)\README.md") }
if ($missing) { Write-Host "FAIL — missing READMEs:"; $missing.Name } else { Write-Host "PASS — all root folders have README.md" }

# Every active NLP has 00_DROP
$nlps = 'axioms','knowledge-refinery','paper-proof-grader','link-pull-drop','session-handoff-drop','ai-portal-generator'
$nlps | ForEach-Object {
  $p = "X:\$_\00_DROP"
  Write-Host "$p exists? $(Test-Path -LiteralPath $p)"
}

# Old intake names still resolve (junctions in place)
$pairs = @(
  @{old='X:\axioms\00_INBOX_DROP_PAPERS_HERE'},
  @{old='X:\knowledge-refinery\00_INTAKE'},
  @{old='X:\paper-proof-grader\DROP_PAPERS_HERE'},
  @{old='X:\session-handoff-drop\DROP_HERE'}
)
$pairs | ForEach-Object { Write-Host "$($_.old) exists? $(Test-Path -LiteralPath $_.old)" }

# Stage 4: every active NLP has the new L2 files
$active = 'axioms','knowledge-refinery','paper-proof-grader','link-pull-drop','session-handoff-drop','ai-portal-generator','ollama'
$active | ForEach-Object {
  $nlp = $_
  foreach ($f in '_AGENT_BRIEF.md','RUN_AGENT.bat','health_check.bat') {
    $p = "X:\$nlp\$f"
    Write-Host "$p exists? $(Test-Path -LiteralPath $p)"
  }
  Write-Host "X:\$nlp\prompts dir? $(Test-Path -LiteralPath ""X:\$nlp\prompts"")"
}

# Each NLP's health_check.bat returns 0 or 2 (PASS or WARN — FAIL is a real problem)
$active | ForEach-Object {
  $p = "X:\$_\health_check.bat"
  if (Test-Path -LiteralPath $p) {
    & $p > $null 2>&1
    Write-Host "$_ health: exit $LASTEXITCODE"
  }
}
```

All four blocks should pass (Stage 4 may show WARN for NLPs whose model endpoints are down — that's not a 4a failure, it's infrastructure state).

---

## Log

Write `X:\_LOGS\prompt_4a_log_2026-05-16.md` with:
- Folders that got new READMEs (list with one-line WHAT for each)
- Folders renamed and junctions created
- Any files that couldn't be inferred (status=experimental flagged for David)

---

## Absolute rules

- **No file deletions.** Old intake names become junctions, not gone.
- **No content changes** to existing READMEs without explicit reason. If an existing README is wrong, flag it in the log — don't silently rewrite.
- **Status=placeholder is fine** for folders where purpose is unclear. Don't fabricate a story.
- **No emoji** in README content.
