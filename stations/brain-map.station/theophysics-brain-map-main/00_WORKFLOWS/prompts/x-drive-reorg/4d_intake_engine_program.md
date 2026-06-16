# Prompt 4d — Intake engine as separable Python program

**Owner:** Codex
**Risk:** Medium (new code, but green-field — no existing-state risk)
**Depends on:** Nothing (parallel with 4a/4c)
**Blocks:** 4e (dashboard consumes engine state schema)

---

## Goal

Build the **intake engine** — the layer "in between" a user dropping a file and the NLP processing it — as a **separable, portable Python program**. David's explicit ask 2026-05-16: *"the file management program should be separate... it is, but it should be in that folder but it should be like a separate program."*

Key word: **separable**. Lives at `X:\Backside\intake_engine\` for this deployment, but structured so it could be unbundled and run on any folder tree elsewhere with a different YAML config.

---

## Architecture (target shape)

```
X:\Backside\intake_engine\
  pyproject.toml                     ← packaging metadata
  README.md                          ← Layer 1 + Layer 2 (this IS a workflow folder)
  src\theophysics_intake_engine\
    __init__.py
    __main__.py                      ← `python -m theophysics_intake_engine` entry
    watcher.py                       ← watchdog filesystem event handler
    classifier.py                    ← Ollama Mistral wrapper, returns class label
    router.py                        ← move file to matching NLP\00_DROP\ + launch RUN.bat
    config.py                        ← load + validate deployment YAML
    state.py                         ← write/read engine state for dashboard (JSON snapshot)
    log.py                           ← structured logging
  config\
    x_drive.yaml                     ← X-drive deployment config (paths, classes, NLPs)
    example.yaml                     ← template for new deployments
  tests\
    test_classifier.py               ← mocks Ollama, asserts class extraction
    test_router.py                   ← uses tmp_path fixture, asserts file moves
    test_config.py                   ← YAML schema validation
  bin\
    install_service.ps1              ← register as Task Scheduler "At Startup" job
    uninstall_service.ps1            ← stop + remove
```

## Required outcome

### Stage 1 — Package skeleton

`pyproject.toml` with:

```toml
[project]
name = "theophysics-intake-engine"
version = "0.1.0"
description = "Watcher + LLM classifier + router for folder-tree NLP pipelines"
requires-python = ">=3.10"
dependencies = [
  "watchdog>=4.0",
  "ollama>=0.4",
  "pyyaml>=6.0",
  "pydantic>=2.0",
]

[project.scripts]
intake-engine = "theophysics_intake_engine.__main__:main"

[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"
```

Installable: `pipx install -e X:\Backside\intake_engine` → `intake-engine --config x_drive.yaml` runs it.

### Stage 2 — Config schema (`config/x_drive.yaml`)

```yaml
deployment_name: x_drive
master_drop: X:\DROP_HERE
state_file: X:\Backside\intake_engine\state.json
log_dir: X:\_LOGS

classifier:
  enabled: true
  type: ollama
  endpoint: http://localhost:11434
  model: mistral
  classes:
    - PAPER
    - LINK
    - SESSION_HANDOFF
    - AXIOM
    - GENERAL

routes:
  PAPER:
    target: X:\00_WORKFLOWS\paper-proof-grader\00_DROP
    run: X:\00_WORKFLOWS\paper-proof-grader\RUN.bat
    debounce_seconds: 30
  LINK:
    target: X:\00_WORKFLOWS\link-pull-drop\00_DROP
    run: X:\00_WORKFLOWS\link-pull-drop\RUN.bat
    debounce_seconds: 30
  SESSION_HANDOFF:
    target: X:\00_WORKFLOWS\session-handoff-drop\00_DROP
    run: X:\00_WORKFLOWS\session-handoff-drop\RUN.bat
    debounce_seconds: 30
  AXIOM:
    target: X:\00_WORKFLOWS\axioms\00_DROP
    run: X:\00_WORKFLOWS\axioms\RUN_AXIOMS_WORKFLOW.bat
    debounce_seconds: 30
  GENERAL:
    target: X:\00_WORKFLOWS\knowledge-refinery\00_DROP
    run: X:\00_WORKFLOWS\knowledge-refinery\RUN_CONDUCTOR.bat
    debounce_seconds: 30

watchers:
  - X:\DROP_HERE                                            # master (uses classifier)
  - X:\00_WORKFLOWS\paper-proof-grader\00_DROP              # per-NLP (skips classifier)
  - X:\00_WORKFLOWS\link-pull-drop\00_DROP
  - X:\00_WORKFLOWS\session-handoff-drop\00_DROP
  - X:\00_WORKFLOWS\axioms\00_DROP
  - X:\00_WORKFLOWS\knowledge-refinery\00_DROP
```

`example.yaml` — same structure but generic, for someone else deploying.

### Stage 3 — Watcher behavior

- One `Observer` per watched dir.
- On file-created event: capture (path, time).
- Debounce: hold for `debounce_seconds`. If more files arrive in the same dir during debounce, batch them.
- After debounce:
  - If dir is master_drop: call classifier on each file, move to matching NLP `00_DROP`.
  - If dir is an NLP `00_DROP`: launch that NLP's RUN.bat with no args.
- After RUN.bat exits: log result (exit code, duration) to `state.json`.
- Update `state.json` after every event so the dashboard can read live state.

### Stage 4 — Classifier

```python
def classify(filename: str, content_preview: str, classes: list[str]) -> str:
    prompt = (
        f"A file is being dropped into a knowledge pipeline. "
        f"Filename: {filename}. First 500 chars: {content_preview}. "
        f"Classify as exactly one of: {', '.join(classes)}. "
        f"Reply with just the one word."
    )
    # call ollama
    # validate the reply matches one of `classes` (case-insensitive)
    # if no match: return classes[-1] (last class is treated as default/general)
```

Content preview is first 500 chars of file content. If binary (PDF / image / video), fall back to extension-based class guess (PDF → PAPER, .mp3/.wav → SESSION_HANDOFF, .url/.txt-with-https → LINK, else GENERAL).

### Stage 5 — State file schema

`state.json` (atomic write via tmp+rename):

```json
{
  "schema_version": 1,
  "last_updated": "2026-05-16T14:23:01Z",
  "watchers": [
    {"path": "X:\\DROP_HERE", "queue_depth": 0, "last_event": "2026-05-16T14:20:11Z"}
  ],
  "runs": [
    {"nlp": "paper-proof-grader", "started": "...", "ended": "...", "exit_code": 0, "files": ["..."]}
  ],
  "errors": []
}
```

Keep last 50 runs. Trim older.

### Stage 6 — Service registration

`bin/install_service.ps1`:
- Creates a Task Scheduler job "Theophysics_Intake_Engine"
- Trigger: at startup
- Action: `intake-engine --config X:\Backside\intake_engine\config\x_drive.yaml`
- Run with highest privileges, restart on failure (max 3 within 1 hour)

`bin/uninstall_service.ps1`: removes the job, stops the running process.

### Stage 7 — Tests

- `test_classifier.py`: mock the Ollama response, assert class extraction handles edge cases (extra whitespace, casing, multi-word response — clamp to first word, validate against classes).
- `test_router.py`: use `pytest tmp_path`, drop a fake file in a mock master_drop, assert it lands in the right target dir, RUN.bat is launched (mock subprocess).
- `test_config.py`: assert YAML schema rejects missing required fields, accepts valid example.yaml.

---

## Acceptance check

```powershell
# Package installs and runs
pipx install -e X:\Backside\intake_engine
intake-engine --version

# Config validates
intake-engine --config X:\Backside\intake_engine\config\x_drive.yaml --validate-config

# Tests pass
cd X:\Backside\intake_engine
pytest

# Smoke test (run for 60s, drop a file, see it routed)
intake-engine --config x_drive.yaml --once --timeout 60 &
echo "test paper content" > X:\DROP_HERE\test_paper.txt
sleep 30
Test-Path "X:\00_WORKFLOWS\paper-proof-grader\00_DROP\test_paper.txt"   # should be True
```

All four should pass.

---

## Log

`X:\_LOGS\prompt_4d_log_2026-05-16.md` — record the package structure, test results, config validation output.

---

## Absolute rules

- **No coupling to X: paths inside the source code.** Every path comes from the YAML config. Source code stays portable.
- **The package name `theophysics_intake_engine` is for the X:\ deployment.** If someone forks it for another project, they rename. Code shouldn't assume "theophysics" anywhere except the package-name string.
- **No emoji** in code, log output, or filenames.
- **Don't auto-register the Task Scheduler service** during install. David runs `install_service.ps1` explicitly when ready.
- **Don't delete the existing manual `RUN.bat` files** in each NLP. The engine launches them as-is.
