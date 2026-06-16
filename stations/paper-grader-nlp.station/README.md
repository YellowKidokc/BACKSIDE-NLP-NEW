# Paper Grader NLP Wrapper

Role: local station wrapper for the deeper `paper-proof-grader.station` engine.

Use this station when you want a clean local drop-folder workflow:

```text
INPUT -> paper-proof-grader engine -> EXPORTS -> ARCHIVE
```

This wrapper does not own the grading philosophy. It resolves and drives the
`paper-proof-grader.station` engine, then mirrors JSON, Markdown, HTML, CSV, and
Excel outputs into typed `EXPORTS` folders.

## Goal

Grade dropped article/paper/series files through the paper proof grader without
having to run the engine station directly.

The resulting report should answer:

```text
What is being claimed?
What kind of claim is it?
What supports it?
What would break it?
Why should a physicist keep reading?
```

## Current Entrypoints

```text
RUN.bat
python -m paper_grader
RUN.bat schema
RUN.bat consolidate
```

## Related Engine

The main engine is:

```text
X:\Backside\stations\paper-proof-grader.station
```

That station owns the deeper grading workflow:

```text
text extraction
section detection
claim extraction
7Q pressure
formal verification annotation
DeBERTa / axiom scoring lanes
JSON / Markdown / HTML / CSV / Excel reports
```

## Older Snapshot Package Files

These files are still useful as UI/spec context, but they are not the station's
primary runtime identity:

```text
codex_prompt.md
snapshot_schema.json
snapshot_ui_spec.md
implementation_plan.md
```
