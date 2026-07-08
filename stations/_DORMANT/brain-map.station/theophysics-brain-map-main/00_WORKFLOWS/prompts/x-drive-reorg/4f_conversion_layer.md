# Prompt 4f — Conversion layer (shared format-normalization service)

**Owner:** Codex
**Risk:** Medium (new code; integrates several existing tools)
**Depends on:** Nothing (parallel with 4a/4c/4d)
**Blocks:** Nothing strictly — but every NLP benefits from this, and 4d intake engine should consume it for binary inputs

---

## Goal

Consolidate the brain's **scattered conversion tools** into one shared layer. David flagged 2026-05-16: *"there should have been a conversion layer — we had MarkItDown for converting basically anything into HTML, and we had downloading YouTube videos, TTS, and something else."*

Pieces that exist today but are not unified:
- `D:\brain\01_WHISPER\` — Whisper (audio → text)
- `D:\brain\05_YOUTUBE\` — YouTube tooling
- `D:\brain\06_IMAGES\` — image processing
- `\\dlowenas\github\TTS\` — text-to-speech
- `X:\00_WORKFLOWS\link-pull-drop\` — already does YouTube transcripts + web fetch (partial overlap, keep)
- Microsoft **MarkItDown** (open-source, PyPI `markitdown`) — handles PDF, DOCX, PPTX, XLSX, HTML, IPYNB, audio (via OpenAI Whisper), images (via OCR), and more

Build a unified **conversion layer** as a separable Python program plus a standalone workflow folder (the "drop anything, get markdown back" pattern).

---

## Architecture

Same two-faced shape as 4d: library + standalone NLP wrapper.

```
X:\Backside\conversion_lib\
  pyproject.toml
  README.md
  src\theophysics_conversion\
    __init__.py
    detect.py                          ← sniff mime/extension → converter choice
    convert.py                         ← main API: convert(path) -> ConvertResult
    converters\
      markitdown_adapter.py            ← wraps Microsoft markitdown (PDF, DOCX, PPTX, HTML, IPYNB)
      whisper_adapter.py               ← wraps Whisper for audio/video (uses D:\brain\01_WHISPER models)
      youtube_adapter.py               ← yt-dlp + youtube-transcript-api
      ocr_adapter.py                   ← Tesseract or markitdown's OCR for images
      tts_adapter.py                   ← wraps \\dlowenas\github\TTS (output: WAV/MP3, opposite direction)
    models.py                          ← pydantic: ConvertResult { markdown: str, metadata: dict, warnings: list }
  config\
    x_drive.yaml
    example.yaml
  tests\
    test_detect.py
    test_markitdown.py                 ← uses fixture PDF/DOCX
    test_youtube.py                    ← mocks yt-dlp
    test_convert_end_to_end.py
  bin\
    convert-file.ps1                   ← convenience wrapper for one-shot use

X:\00_WORKFLOWS\conversion-layer\
  README.md                            ← Layer 1 + Layer 2 contract
  RUN.bat                              ← drop → convert → OUTPUT
  config.json
  00_DROP\
  OUTPUT\                              ← .md files, one per input
  ARCHIVE\                             ← processed inputs move here
```

Dependencies:
- `markitdown[all]>=0.0.1a3` (Microsoft, pip-installable)
- `yt-dlp>=2024.1`
- `youtube-transcript-api>=0.6`
- `openai-whisper>=20240930` (optional; only if local Whisper is enabled; D:\brain\01_WHISPER may have weights)
- `pytesseract>=0.3` (only if OCR enabled)
- `pydantic>=2.0`
- `pyyaml>=6.0`

---

## Required outcome

### Stage 1 — Library skeleton

`pyproject.toml`:

```toml
[project]
name = "theophysics-conversion"
version = "0.1.0"
description = "Unified format normalization: any input -> canonical markdown"
requires-python = ">=3.10"
dependencies = [
  "markitdown[all]>=0.0.1a3",
  "yt-dlp>=2024.1",
  "youtube-transcript-api>=0.6",
  "pydantic>=2.0",
  "pyyaml>=6.0",
]

[project.optional-dependencies]
whisper = ["openai-whisper>=20240930"]
ocr = ["pytesseract>=0.3"]

[project.scripts]
convert-file = "theophysics_conversion.convert:cli"
```

### Stage 2 — Format detection

`detect.py`:
- Sniff by extension first (.pdf, .docx, .pptx, .xlsx, .html, .htm, .ipynb, .mp3, .wav, .m4a, .mp4, .mov, .png, .jpg, .jpeg, .gif, .tiff, .url, .txt, .md).
- If file is `.txt` or `.url` with content starting with `http`, dispatch as URL → check if YouTube vs general web.
- If extension is ambiguous, sniff first 16 bytes (magic numbers): `%PDF` → pdf, `PK\x03\x04` → docx/pptx/xlsx (zip), `\x89PNG` → png, etc.
- Return a `Format` enum: `PDF | DOCX | PPTX | XLSX | HTML | IPYNB | MARKDOWN | AUDIO | VIDEO | IMAGE | YOUTUBE_URL | WEB_URL | UNKNOWN`.

### Stage 3 — Main `convert(path)` API

```python
def convert(
    source: str | Path,
    *,
    config: ConversionConfig | None = None,
) -> ConvertResult:
    """
    Convert anything to canonical markdown.

    Returns ConvertResult with:
      - markdown: str        the converted content
      - metadata: dict       source-specific (title, duration, author, page count, ...)
      - warnings: list[str]  non-fatal issues
    """
```

Dispatch chain (Format → Adapter):

| Format | Adapter | Notes |
|---|---|---|
| PDF, DOCX, PPTX, XLSX, HTML, IPYNB | markitdown_adapter | one call, handles most office formats |
| AUDIO, VIDEO | whisper_adapter | requires `[whisper]` extra |
| YOUTUBE_URL | youtube_adapter | transcript first; fallback yt-dlp + Whisper |
| WEB_URL | markitdown_adapter | markitdown can fetch URLs |
| IMAGE | ocr_adapter | requires `[ocr]` extra; markitdown also has built-in OCR |
| MARKDOWN | passthrough | normalize line endings, strip BOM |
| UNKNOWN | raise | with the file's extension + first 16 bytes in error |

### Stage 4 — TTS adapter (reverse direction)

TTS is the only adapter that goes *text → audio* not *anything → text*. Wrap the existing `\\dlowenas\github\TTS` repo as a separate function:

```python
def text_to_speech(
    text: str,
    out_path: str | Path,
    voice: str = "default",
) -> Path:
    """text -> audio file. Returns path written."""
```

Don't bundle into the main `convert()` flow — it's a different shape. Just expose it.

### Stage 5 — Config

`config/x_drive.yaml`:

```yaml
deployment_name: x_drive

markitdown:
  enabled: true
  use_llm_for_image_descriptions: false   # OpenAI/Azure key needed if true

whisper:
  enabled: true
  model_size: base                         # tiny/base/small/medium/large
  model_dir: D:\brain\01_WHISPER\_MODELS

youtube:
  prefer_transcript: true                  # try transcript API first; fallback yt-dlp+whisper
  yt_dlp_format: "bestaudio/best"
  cache_dir: X:\Pipeline\captures\youtube_cache

ocr:
  enabled: true
  tesseract_path: C:\Program Files\Tesseract-OCR\tesseract.exe  # adjust to env

tts:
  enabled: true
  repo_path: \\dlowenas\github\TTS
  default_voice: default
  output_dir: X:\Pipeline\captures\tts_out
```

### Stage 6 — Standalone NLP wrapper

`X:\00_WORKFLOWS\conversion-layer\` honors Layer 1 + Layer 2:

- `00_DROP\` accepts files or `.txt` of URLs
- `RUN.bat` calls `convert-file X:\00_WORKFLOWS\conversion-layer\00_DROP\<file>` and writes `OUTPUT\<file>.md`
- After processing, original moves to `ARCHIVE\`
- `config.json` references `X:\Backside\conversion_lib\config\x_drive.yaml`

### Stage 7 — Tests

- `test_detect.py`: assert each known extension maps to correct Format; assert magic-number fallback works on extensionless files.
- `test_markitdown.py`: fixture PDF + DOCX → assert non-empty markdown.
- `test_youtube.py`: mock transcript API, assert returns expected markdown shape.
- `test_convert_end_to_end.py`: drop a PDF in tmp_path, call `convert()`, assert markdown contains expected substring + warnings list is empty.

### Stage 8 — Integration with 4d intake engine

**Optional, don't block on this:** when prompt 4d's intake engine receives a non-text file at master `DROP_HERE`, it can call `theophysics_conversion.convert(path)` first, get markdown, then run the classifier on that markdown content (instead of binary bytes). This gives much better classification accuracy.

If you build 4d and 4f at roughly the same time, wire this in. If 4d is already deployed by another Codex worker, skip — add as a 4d revision later.

---

## Acceptance check

```powershell
# Library installs and CLI works
pipx install -e "X:\Backside\conversion_lib[whisper,ocr]"
convert-file --version

# Detect known formats
convert-file --detect "C:\path\to\some.pdf"     # prints: PDF
convert-file --detect "https://youtube.com/..."  # prints: YOUTUBE_URL

# Convert a PDF
convert-file "X:\C4C\ap_pdfs\AP Bible Timeline.pdf" --out test_out.md
Get-Content test_out.md | Select-String "Bible" | Measure-Object  # >0 matches

# YouTube transcript
echo "https://www.youtube.com/watch?v=dQw4w9WgXcQ" > test_url.txt
convert-file test_url.txt --out yt.md
Test-Path yt.md  # True

# Standalone NLP works end-to-end
copy "X:\C4C\ap_pdfs\Modern-Day Miracles.pdf" X:\00_WORKFLOWS\conversion-layer\00_DROP\
X:\00_WORKFLOWS\conversion-layer\RUN.bat
Test-Path X:\00_WORKFLOWS\conversion-layer\OUTPUT\Modern-Day*.md  # True

# Tests pass
cd X:\Backside\conversion_lib
pytest
```

All should pass.

---

## Log

`X:\_LOGS\prompt_4f_log_2026-05-16.md` — package structure, test results, sample conversion outputs (one PDF, one YouTube, one DOCX if available).

---

## Absolute rules

- **No coupling to X: paths inside source code.** Paths come from YAML config.
- **Whisper and OCR are OPTIONAL extras.** Don't force the install if D:\brain\01_WHISPER models aren't available — fall back gracefully with a clear "this format requires the [whisper] extra" warning.
- **Don't re-download Whisper weights** if they exist at `D:\brain\01_WHISPER\_MODELS\` — point to them.
- **MarkItDown does most formats** — prefer it over re-implementing converters. Don't reinvent.
- **Reuse `\\dlowenas\github\TTS` repo as-is.** Don't fork or rewrite the TTS engine; just shell out to its existing entry point.
- **No emoji** in code, output, filenames.
- **Audio output of TTS lands at `X:\Pipeline\captures\tts_out\`** (per config), not bundled with the source.
- **Don't bundle a giant test corpus.** Fixtures should be < 100 KB each; use small representative samples.
