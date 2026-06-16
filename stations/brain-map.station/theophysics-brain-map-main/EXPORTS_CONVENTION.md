# X:\EXPORTS Convention

**What this is:** The rule for where final human-usable outputs land.
**Owner:** shared
**Status:** live proposal
**Last updated:** 2026-05-16

`X:\EXPORTS` is the front door for digestible results: Markdown, HTML, Excel, PDFs, prompt packs, galleries, and finished reports.

It is not the place for every intermediate JSON file, scratch artifact, run cache, model trace, or partial station state.

## Rule

```text
Internal state / machine intermediates -> workflow STATE, workflow OUTPUT, or X:\Backside\_state
Final human-usable export            -> X:\EXPORTS\<export-family>\<run-id>
```

## Recommended families

```text
X:\EXPORTS\
  paper-grader-station-lab\
  paper-grades\
  executive-summaries\
  math-layers\
  axiom-reports\
  article-packets\
  picture-prompts\
  session-handoffs\
  proof-explorer\
```

## What belongs here

- Readable Markdown reports.
- Polished HTML reports.
- Excel workbooks meant for review.
- Final prompt packs.
- Gallery pages.
- Index files that tell David what was produced.

## What does not belong here

- Raw station manifests unless intentionally exported.
- Temporary JSON used to build HTML.
- Cache folders.
- Model outputs that have not been reviewed or shaped.
- Logs.

Each export folder should include a small `README.md` naming the input, station/workflow, and where the internal state lives.
