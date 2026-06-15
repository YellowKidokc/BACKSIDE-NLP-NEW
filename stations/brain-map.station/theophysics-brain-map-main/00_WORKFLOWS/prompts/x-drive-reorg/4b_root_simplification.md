# Prompt 4b — Root simplification

**Owner:** Codex
**Risk:** Medium (touches NTFS junctions; many scripts hardcode current paths)
**Depends on:** 4a complete (convention + READMEs in place)
**Blocks:** Phase 3 GitHub push readiness (cleaner root before pushing the map)

---

## Goal

Take X:\ root from **24+ items** to **≤12** by grouping the 9 NLPs under `X:\00_WORKFLOWS\` and the vault content under `X:\Knowledge\`, the shared pipeline data under `X:\Pipeline\`. Leave NTFS junctions at the old root paths so existing `.bat`/`.ps1`/comms-hub references keep working for one transition cycle.

---

## Pre-conditions

- 4a delivered (every workflow folder has `00_DROP/` + `README.md`).
- Phase 1 verified (no `X:\brain\` subfolder, only `X:\_brain_DEPRECATED_20260516\` empty marker).
- Phase 2 dedup report read: don't move duplicates into deeper folders without resolving them.

## Target root shape (after this prompt)

```
X:\
  README.md
  ARCHITECTURE.md
  FOLDER_CONVENTIONS.md
  RUN_*.bat                        (3–5 click-buttons)
  David\                           (human maps & notes)
  00_WORKFLOWS\                    (all 9 NLPs as subfolders)
    ai-portal-generator\
    axioms\
    knowledge-refinery\
    link-pull-drop\
    ollama\
    paper-proof-grader\
    proof-architecture\
    proof-explorer\
    session-handoff-drop\
    prompts\                       (prompt bank — already exists)
    + existing 00_WORKFLOWS files (healthcheck, etc.)
  Knowledge\
    C4C\
    C4C-wiki\
    FAP\
  Pipeline\
    captures\
    digests\
    embeddings\
    models\
    ratings\
  Backside\                        (intake engine + automation)
  BIL\                             (post Phase 5 — full BIL contents)
  github\                          (keep at root — tool of tools)
  _LOGS\
  #recycle\
```

Target item count at root: ~12 items + a few `.md` and `.bat` at root.

## Required outcome

### Stage 1 — Move NLPs into `00_WORKFLOWS/`

For each of the 9 NLPs:
1. `Move-Item X:\<nlp> X:\00_WORKFLOWS\<nlp>` (PowerShell). On NAS-same-share, this is a metadata rename — fast.
2. `cmd /c mklink /J "X:\<nlp>" "X:\00_WORKFLOWS\<nlp>"` — junction at the old root path.

Result: scripts that reference `X:\paper-proof-grader\RUN.bat` still work via the junction.

### Stage 2 — Create `X:\Knowledge\` and move vault folders

```
Move-Item X:\C4C      X:\Knowledge\C4C
Move-Item X:\C4C-wiki X:\Knowledge\C4C-wiki
Move-Item X:\FAP      X:\Knowledge\FAP
```

Add junctions at the old root paths.

### Stage 3 — Create `X:\Pipeline\` and move shared data folders

```
Move-Item X:\captures   X:\Pipeline\captures
Move-Item X:\digests    X:\Pipeline\digests
Move-Item X:\embeddings X:\Pipeline\embeddings
Move-Item X:\models     X:\Pipeline\models
Move-Item X:\ratings    X:\Pipeline\ratings
```

Junctions at old root paths.

### Stage 4 — Update READMEs

- `X:\README.md` — rewrite top to reflect new layout. The current version reflects the partial May-13 cleanup.
- `X:\00_WORKFLOWS\README.md` — refresh; list the 9 NLPs as a TOC.
- New: `X:\Knowledge\README.md` — Layer 1 stub.
- New: `X:\Pipeline\README.md` — Layer 1 stub.

### Stage 5 — Sanity-test hot scripts

Run each of these and confirm exit code 0 (no actual file processing, just argv parsing):
- `X:\00_WORKFLOWS\paper-proof-grader\RUN.bat /?`
- `X:\00_WORKFLOWS\link-pull-drop\RUN.bat /?`
- `X:\00_WORKFLOWS\session-handoff-drop\RUN.bat /?`
- `X:\00_WORKFLOWS\knowledge-refinery\RUN_CONDUCTOR.bat /?`

If any hardcoded `X:\<nlp>\` path no longer resolves correctly via the junction, log it in the prompt log — don't fix in-place (that's 4c's job).

---

## Acceptance check

```powershell
# Root has 12 or fewer directories (excluding system #recycle, _brain_DEPRECATED)
$rootDirs = Get-ChildItem 'X:\' -Directory | Where-Object { $_.Name -notmatch '^(#recycle|_brain_DEPRECATED)' }
Write-Host "Root directory count: $($rootDirs.Count) (target: <=12)"

# All NLPs live under 00_WORKFLOWS
$nlps = 'ai-portal-generator','axioms','knowledge-refinery','link-pull-drop','ollama','paper-proof-grader','proof-architecture','proof-explorer','session-handoff-drop'
$nlps | ForEach-Object {
  $newP = "X:\00_WORKFLOWS\$_"
  $oldP = "X:\$_"
  Write-Host "$_ -- new exists: $(Test-Path -LiteralPath $newP), old junction exists: $(Test-Path -LiteralPath $oldP)"
}

# Junctions at old paths actually resolve (not just empty stubs)
$nlps | ForEach-Object {
  $oldReadme = "X:\$_\README.md"
  Write-Host "Junction-via-old-path README readable: $(Test-Path -LiteralPath $oldReadme)"
}

# Knowledge and Pipeline groups exist
Write-Host "X:\Knowledge\C4C exists? $(Test-Path 'X:\Knowledge\C4C')"
Write-Host "X:\Pipeline\digests exists? $(Test-Path 'X:\Pipeline\digests')"

# Old root paths still resolve via junction
Write-Host "X:\C4C (junction) exists? $(Test-Path 'X:\C4C')"
Write-Host "X:\digests (junction) exists? $(Test-Path 'X:\digests')"
```

All checks should pass.

---

## Log

`X:\_LOGS\prompt_4b_log_2026-05-16.md` — record every move + junction + any sanity-test fail.

---

## Absolute rules

- **No deletes.** Junctions everywhere old paths existed.
- **One transition cycle only** — claude-code-forge or Codex will remove junctions after 4c sweep verifies no script references break.
- **Don't move** `_LOGS\`, `#recycle\`, `_brain_DEPRECATED_20260516\`, `github\`, `Backside\`, `David\`, `00_WORKFLOWS\` (it's the destination), `BIL\` (Phase 5), the root `.md` files, or the root `.bat` files.
