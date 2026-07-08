# Conversion Layer Workflow

Drop files or URL text files into `00_DROP`, run `RUN.bat`, and receive
canonical Markdown exports under `X:\EXPORTS\conversion-layer`.

This is the front-door wrapper around:

```text
X:\Conversions\conversion-layer
```

The workflow does not own finished artifacts. It only accepts inputs, runs the
conversion library, archives processed inputs, and writes a small latest-run
pointer.

## Folders

```text
00_DROP\   incoming source files or .txt URL files
OUTPUT\    latest-run pointers and workflow notes
ARCHIVE\   processed source files
```

## Run

```powershell
X:\00_WORKFLOWS\conversion-layer\RUN.bat
```
