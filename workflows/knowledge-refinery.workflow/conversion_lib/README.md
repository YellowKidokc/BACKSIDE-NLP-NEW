# Theophysics Conversion Layer

Shared format-normalization layer for the X-drive workflow stack.

The contract is simple:

```text
source file or URL -> canonical markdown + metadata + warnings
```

Human-usable converted Markdown belongs under:

```text
X:\EXPORTS\conversion-layer\<run-id>\
```

Internal state belongs under:

```text
X:\Backside\_state\conversion-layer\<run-id>\
```

This first implementation is intentionally conservative. It handles HTML, Markdown,
plain text, and URL text files now. Other formats are detected and routed to
MarkItDown/Whisper/OCR when those optional dependencies are installed.

## Quick Use

```powershell
$env:PYTHONPATH="D:\GitHub\theophysics-brain-map\Backside\conversion_lib\src"
python -m theophysics_conversion.convert "C:\path\article.html" --export-root "X:\EXPORTS\conversion-layer"
```

Detect only:

```powershell
python -m theophysics_conversion.convert --detect "C:\path\article.html"
```

## Why This Exists

The accessible, medium, academic, math, and audit layers should not parse raw
HTML differently each time. They should all consume the same canonical Markdown
and compare that Markdown back against the original extraction.

