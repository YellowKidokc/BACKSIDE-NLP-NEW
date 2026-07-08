# 4a rollout generation log

Date: 2026-05-16
Generator: Codex

## Files generated

- Stage 1 READMEs: 15 files under `4a-output/<folder>/README.md`
- Stage 4 active NLP files for 7 workflows:
  - `_AGENT_BRIEF.md`
  - `RUN_AGENT.bat`
  - `health_check.bat`
  - `prompts/.gitkeep`
- `apply_4a.ps1` (replaced with dry-run-first safe migrator on 2026-05-16)

## Intake junctions handled by apply_4a.ps1

- `X:\axioms\00_INBOX_DROP_PAPERS_HERE -> X:\axioms\00_DROP`
- `X:\knowledge-refinery\00_INTAKE -> X:\knowledge-refinery\00_DROP`
- `X:\paper-proof-grader\INPUT -> X:\paper-proof-grader\00_DROP`
- `X:\paper-proof-grader\DROP_PAPERS_HERE -> X:\paper-proof-grader\00_DROP`
- `X:\session-handoff-drop\DROP_HERE -> X:\session-handoff-drop\00_DROP`

The current script no longer calls `mklink` directly over live folders. Default mode is a dry run. Apply mode creates `00_DROP`, moves legacy intake children into it, archives same-name conflicts under `ARCHIVE\4a_migration_conflicts_<stamp>\`, renames the emptied legacy folder to `<name>.PRE_4A_MIGRATION_<stamp>`, then creates the compatibility junction.

Usage:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\4a-output\apply_4a.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\4a-output\apply_4a.ps1 -Apply
```

## Unresolved fields (`<TBD — David to confirm>`)

Because this mirror repo does not contain workflow runtime files (`X:\<nlp>\config.json`, `RUN.bat`, `pipeline.py`, `_LOGS`), the following could not be inferred without fabricating:

- Per-workflow mission text, workflow type, and usage bullets in all `_AGENT_BRIEF.md`
- Inputs/outputs naming and downstream consumer specifics in all `_AGENT_BRIEF.md`
- Prompt file names and prompt-purpose entries in all `_AGENT_BRIEF.md`
- External service inventory in all `_AGENT_BRIEF.md`
- Stage 1 "What's inside" real child listings for each root README
- Pipeline contract accepted types and detailed behavior for `link-pull-drop`, `session-handoff-drop`, and `ollama`
- Ratings folder precise purpose (marked experimental)

## Notes

- No deletions performed.
- Junction preservation is represented in dry-run-first script form for local execution on David's Windows host.
- `paper-proof-grader` merge/dedupe of `INPUT` + `DROP_PAPERS_HERE` into `00_DROP` requires local data operation on X: and is not performed in this mirror artifact pack.

- `_BACKSIDE_STRUCTURE_PROBE.md` — probe response on Backside topology (models/stations/workflows/_archive), with migration map and decision calls.
