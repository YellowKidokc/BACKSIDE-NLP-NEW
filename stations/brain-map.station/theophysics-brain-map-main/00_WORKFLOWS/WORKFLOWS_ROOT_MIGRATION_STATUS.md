# Root Workflows Migration Status

Generated: 2026-05-11 18:16 America/Chicago

## Result

The workflow hub was copied from:

```text
\\dlowenas\brain\brain\00_WORKFLOWS
```

to:

```text
\\dlowenas\brain\00_WORKFLOWS
```

The root copy is the working copy going forward. The older nested copy was preserved as a fallback.

## Verified Workflows

- `ai-portal-generator`
- `link-pull-drop`
- `paper-proof-grader`
- `session-handoff-drop`
- `theophysics-comms-hub`

## Root Updates

- Added `RUN_WORKFLOWS_HEALTHCHECK.bat`.
- Added `scripts\workflows_healthcheck.py`.
- Added root workflow README files.
- Updated root-copy configs from older `X:\brain\00_WORKFLOWS` paths to `\\dlowenas\brain\00_WORKFLOWS`.
- Updated root-copy link capture paths to `\\dlowenas\brain\captures\links`.
- Updated root-copy log paths to `\\dlowenas\brain\_LOGS`.

## Healthcheck

Latest report:

```text
\\dlowenas\brain\00_WORKFLOWS\WORKFLOWS_HEALTHCHECK_REPORT.latest.md
```

Status:

```text
Failures: 0
Warnings: 0
Infinity: OK HTTP 200
Qdrant: OK HTTP 200
```
