# File Naming System — Local + R2 Deployment
> Version 1.0 | Kimi | May 12, 2026
>
> This is the canonical naming schema for ALL files in the Theophysics project.
> It covers local folders (R:\, Master HTMl\), R2 bucket paths, and public URLs.

---

## Philosophy

**Machines read these names. Humans read the page titles.**

File names are not titles. They are machine identifiers. They must be:
- **Parseable** — a script can split on `-` and know what it's looking at
- **Sortable** — files fall in natural order without tricks
- **URL-safe** — no spaces, no special characters, no mixed case chaos
- **Predictable** — given the article ID, you can guess the filename

---

## The Pattern

```
{series}-{article}[-{suffix}][-{descriptor}].{ext}
```

### 1. Series (Required)

Two-letter or three-letter uppercase abbreviation. Never changes.

| Series | Code | Notes |
|--------|------|-------|
| Genesis to Quantum | `GTQ` | Flagship series |
| Moral Decay of America | `MDA` | In production |
| Cross Domain | `CD` | Coherence framework |
| Three Gates | `3G` | Spiritual mechanics |
| Three Truths | `3T` | Self-refuting idioms |
| Logos Papers | `LP` | Formal papers |
| Convergence | `CNV` | Bridge articles |
| Evidence | `EV` | Proof articles |
| Standalone | `SA` | One-off articles |

### 2. Article (Required)

Zero-padded two-digit number. Sub-articles get a letter suffix.

| Example | Meaning |
|---------|---------|
| `01` | Article 1 |
| `01A` | Article 1, sub-article A |
| `10` | Article 10 |
| `10A` | Article 10, sub-article A |
| `00` | Series intro / cover |

**Rule:** Always two digits. `01` not `1`. `10A` not `10a`.

### 3. Suffix (Required for non-HTML content)

Tells you what kind of asset this is.

| Suffix | Meaning | Used For |
|--------|---------|----------|
| `-A` | Audio narration | Human-read MP3/M4A |
| `-DD` | Deep dive | Extended audio, academic depth |
| `-TTS` | Text-to-speech | AI-generated audio |
| `-DEBATE` | Debate format | Multi-voice or argument format |
| `-V-FULL` | Video full | Complete video |
| `-V-EVERYDAY` | Video everyday | Simplified language version |
| `-V-SLIDES` | Video slides | Slide presentation recording |
| `-S` | Slides | PDF or HTML slide deck |
| `-I` | Image | Hero image, diagram, figure |
| `-G` | Gallery | Image gallery bundle |
| `-T` | Transcript | Text transcript |
| `-M` | Markdown | Source markdown |
| `-S##` | Story | Generation narrative (S00–S99) |

### 4. Descriptor (Optional)

Only for stories or special variants. Lowercase, hyphen-separated.

| Example | Meaning |
|---------|---------|
| `samuel-1900` | Character name + year |
| `collapse-diagram` | What the image shows |
| `academic` | Academic variant |

### 5. Extension (Required)

Lowercase always.

| Extension | Use Case |
|-----------|----------|
| `.html` | Web pages |
| `.mp3` | Audio (primary) |
| `.m4a` | Audio (Apple/alternative) |
| `.mp4` | Video |
| `.pdf` | Slides, documents |
| `.webp` | Images (preferred) |
| `.png` | Images (diagrams with transparency) |
| `.jpg` | Images (photos) |
| `.txt` | Transcripts |
| `.md` | Markdown sources |
| `.zip` | Bundles |

---

## Examples — Correct vs Wrong

### ✅ CORRECT

| Filename | What It Is |
|----------|------------|
| `GTQ-01.html` | Genesis to Quantum article 1 |
| `GTQ-01-A.mp3` | GTQ-01 audio narration |
| `GTQ-01-DD.mp3` | GTQ-01 deep dive audio |
| `GTQ-01-TTS.mp3` | GTQ-01 AI-generated audio |
| `GTQ-01-V-FULL.mp4` | GTQ-01 full video |
| `GTQ-01-S.pdf` | GTQ-01 slide deck |
| `GTQ-01-I.webp` | GTQ-01 hero image |
| `GTQ-01A.html` | GTQ-01 sub-article A |
| `GTQ-01A-A.mp3` | GTQ-01A audio |
| `MDA-05.html` | Moral Decay article 5 |
| `MDA-05-DD.m4a` | MDA-05 deep dive |
| `MDA-S01-samuel-1900.mp3` | MDA story 1, Samuel 1900 |
| `CD-03-A.mp3` | Cross Domain article 3 audio |
| `SA-god-in-the-equations.html` | Standalone article |

### ❌ WRONG

| Filename | Why It's Wrong |
|----------|----------------|
| `gtq-01-a.mp3` | Lowercase series code |
| `GTQ_01_Why_Time_Is_Grace.mp3` | Spaces, underscores, descriptive title in filename |
| `01 - The Measurement.mp3` | Missing series code, spaces |
| `gtq01a.mp3` | Missing hyphens, unreadable |
| `Paper 01 - The Logos Principle - FULL.mp3` | Spaces, mixed separators, no series code |
| `blue__god_in_the_equations.mp3` | Nonsensical prefix, double underscores |
| `moral-decline-of-america.m4a` | No series code, no article number, descriptive |
| `GTQ-1-A.mp3` | Not zero-padded |
| `GTQ-01-A.MP3` | Uppercase extension |
| `GTQ-01-a.mp3` | Lowercase suffix |

---

## Local Folder Structure

Every series gets its own root folder. Every article gets its own subfolder.

```
R:\ or Master HTMl\
├── GTQ\
│   ├── GTQ-00\
│   │   ├── audio\
│   │   ├── video\
│   │   ├── slides\
│   │   ├── images\
│   │   └── _archive
│   ├── GTQ-01\
│   ├── GTQ-01A\
│   ├── GTQ-02\
│   └── ...
├── MDA\
│   ├── MDA-00\
│   ├── MDA-01\
│   ├── MDA-02\
│   ├── stories\
│   │   └── audio\
│   └── ...
├── CD\
├── 3G\
├── 3T\
├── LP\
└── _url_catalog\
    ├── URL Catalog.csv
    └── URL Catalog.html
```

### Subfolder Rules

| Subfolder | Contents |
|-----------|----------|
| `audio/` | All audio files for this article |
| `video/` | All video files for this article |
| `slides/` | PDF or HTML slide decks |
| `images/` | Hero images, diagrams, figures |
| `transcripts/` | `.txt` or `.md` transcripts |
| `_archive/` | Old versions, backups, rejected cuts |

**Rule:** Never mix content types in the same folder. Audio goes in `audio/`. Video goes in `video/`. No exceptions.

---

## R2 Bucket Structure

R2 mirrors the local structure but flattens for public serving.

### Option A: Series-First (Recommended)

```
r2theophysics:theophysics/
├── audio/
│   ├── GTQ/
│   │   ├── GTQ-01/
│   │   │   ├── GTQ-01-A.mp3
│   │   │   ├── GTQ-01-DD.mp3
│   │   │   └── GTQ-01-TTS.mp3
│   │   └── GTQ-02/
│   └── MDA/
│       └── MDA-01/
├── video/
│   ├── GTQ/
│   │   └── GTQ-01/
│   │       ├── GTQ-01-V-FULL.mp4
│   │       └── GTQ-01-V-EVERYDAY.mp4
│   └── MDA/
├── slides/
│   └── GTQ/
│       └── GTQ-01/
│           └── GTQ-01-S.pdf
└── images/
    └── GTQ/
        └── GTQ-01/
            └── GTQ-01-I.webp
```

**Public URLs:**
- `https://audio.faiththruphysics.com/GTQ/GTQ-01/GTQ-01-A.mp3`
- `https://media.faiththruphysics.com/video/GTQ/GTQ-01/GTQ-01-V-FULL.mp4`
- `https://media.faiththruphysics.com/slides/GTQ/GTQ-01/GTQ-01-S.pdf`
- `https://media.faiththruphysics.com/images/GTQ/GTQ-01/GTQ-01-I.webp`

### Option B: Article-First (Alternative)

```
r2theophysics:theophysics/
├── GTQ/
│   ├── GTQ-01/
│   │   ├── audio/
│   │   ├── video/
│   │   └── slides/
│   └── GTQ-02/
└── MDA/
    └── MDA-01/
```

**Public URLs:**
- `https://assets.faiththruphysics.com/GTQ/GTQ-01/audio/GTQ-01-A.mp3`
- `https://assets.faiththruphysics.com/GTQ/GTQ-01/video/GTQ-01-V-FULL.mp4`

**Recommendation:** Use Option A (series-first) because it aligns with subdomain specialization (`audio.`, `media.`) and makes bulk operations per content type easier.

---

## URL Catalog Integration

The `_url_catalog` folder on R: auto-generates `URL Catalog.csv` and `URL Catalog.html` every hour at :12 and :42.

**How it works:**
1. Files are scanned from `r2theophysics:theophysics/`
2. Named files get clean public URLs
3. Files with spaces or special characters get `%20`-encoded URLs

**What this means for you:**
- Follow this naming system → clean URLs
- Use spaces or special chars → ugly URLs that break in some players

**CSV columns:**
- `Bucket` — R2 bucket name
- `Type` — content type (audio, video, image)
- `File Name` — the actual filename
- `Folder` — R2 folder path
- `Size Bytes` — file size
- `Public URL` — the public URL (empty = not publicly accessible)
- `R2 URI` — internal R2 identifier
- `Path` — full path
- `Extension` — file extension

---

## Migration: Fixing Existing Files

### Step 1: Identify violations
Run a script that flags:
- Spaces in filenames
- Mixed separators (`_` and `-` in same name)
- Missing series codes
- Non-zero-padded numbers
- Uppercase extensions
- Descriptive titles in filenames

### Step 2: Rename in bulk
Use a Python script with regex patterns:

```python
import re
from pathlib import Path

def standardize_filename(old_name: str, series: str, article: str) -> str:
    """Convert old messy name to standard name."""
    # Extract extension
    ext = Path(old_name).suffix.lower()
    
    # Detect content type from old name patterns
    if 'tts' in old_name.lower():
        suffix = '-TTS'
    elif 'deep' in old_name.lower() or 'dd' in old_name.lower():
        suffix = '-DD'
    elif 'video' in old_name.lower() or '.mp4' in old_name:
        suffix = '-V-FULL'  # or detect variant
    elif '.mp3' in old_name or '.m4a' in old_name:
        suffix = '-A'
    else:
        suffix = ''
    
    return f"{series}-{article}{suffix}{ext}"
```

### Step 3: Update HTML references
After renaming, batch-update all `<audio src="...">`, `<video src="...">`, and `<img src="...">` tags in HTML files.

### Step 4: Regenerate URL catalog
The catalog auto-regenerates. Verify clean URLs.

---

## Special Cases

### Stories / Generation Narratives
Stories get a separate `stories/` folder and use `S##` numbering:

```
MDA/stories/audio/MDA-S01-samuel-1900.mp3
MDA/stories/audio/MDA-S02-henry-1926.mp3
```

### Standalone Articles
One-off articles without a series:

```
SA-god-in-the-equations.html
SA-math-is-moral.html
SA-the-same-equation.html
```

### Templates
Templates get version numbers:

```
topbar-template-v2.1.html
equation-template-v1.0.html
hero-template-v3.2.html
```

### Archive / Old Versions
Old versions go in `_archive/` with a timestamp:

```
GTQ-01/_archive/GTQ-01-A-2026-05-01.mp3
GTQ-01/_archive/GTQ-01-A-2026-05-08.mp3
```

---

## Checklist Before You Save

- [ ] Series code is uppercase (GTQ, MDA, CD)
- [ ] Article number is zero-padded (01, 02, 10)
- [ ] Sub-article uses uppercase letter (01A, 01B)
- [ ] Hyphens only, no spaces, no underscores
- [ ] Content suffix is uppercase and standard (-A, -DD, -TTS, -V-FULL)
- [ ] Extension is lowercase (.mp3, .mp4, .html)
- [ ] No descriptive titles in the filename
- [ ] File is in the correct subfolder (audio/, video/, slides/, images/)

---

## Questions?

If a file doesn't fit this system, ask Kimi before naming it. Don't guess.

— kimi-forge
