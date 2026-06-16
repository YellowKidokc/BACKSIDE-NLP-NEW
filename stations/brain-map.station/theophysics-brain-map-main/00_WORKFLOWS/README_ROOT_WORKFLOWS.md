# Brain Root Workflows

This is the root workflow hub for the brain share.

## Main Folders

- `ai-portal-generator` - builds the AI-facing proof-explorer portal.
- `link-pull-drop` - captures links from dropped text/markdown files.
- `paper-proof-grader` - scores papers and exports JSON, Markdown, HTML, CSV, and Excel.
- `session-handoff-drop` - turns dropped or pasted sessions into durable handoffs.
- `theophysics-comms-hub` - quick-start/orientation docs for comms hub work.

## Main Button

Run this first when checking the hub:

```text
RUN_WORKFLOWS_HEALTHCHECK.bat
```

It checks required files, config JSON, Python syntax, working folders, and optional vector services. It writes:

```text
WORKFLOWS_HEALTHCHECK_REPORT.latest.md
```

## Root Location

```text
\\dlowenas\brain
```

The older nested copy at `\\dlowenas\brain\brain\00_WORKFLOWS` was preserved as a fallback. This root folder is the working copy going forward.



