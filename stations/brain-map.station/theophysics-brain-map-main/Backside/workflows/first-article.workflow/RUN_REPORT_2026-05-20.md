# First Article Workflow Run Report

**Date:** 2026-05-20  
**Workflow:** `first-article.workflow`  
**X-drive front door:** `X:\Backside\workflows\first-article.workflow`  
**Root launcher:** `X:\RUN_FIRST_ARTICLE_WORKFLOW.bat`

## What Was Wired

The workflow now chains:

```text
source
-> conversion / canonical Markdown
-> executive-summary
-> overview
-> math-layer
-> image-notes
-> lossless-context JSON + HTML
-> manifest
```

## Verified Inputs

| Input kind | Source | Result |
|---|---|---|
| HTML | `\\dlowenas\HPWorkstation\Desktop\Master HTMl\K-Production-Ready\02-genesis-to-quantum\gtq-03-first-quantum-state.html` | PASS |
| Markdown | `Backside\lossless_context_pipeline\calibration\pilot_preflight_checklist.md` | PASS |
| Image | `X:\Backside\apps\openrecall\images\black_mirror.png` | PASS |

## Main X Run

```text
X:\EXPORTS\first-article-workflow\20260520-153537_gtq-03-first-quantum-state_93c4b1ac52
```

GTQ-03 classified as:

```text
THEOPHYSICS/GTQ-03-THE-FIRST-QUANTUM-STATE-GENESIS-TO-QUANTUM/W/AI_RESEARCH/R/R1 :: G3M3E0S0T3K3R3Q0F3C3 :: C3Q0-G3S0-K3E0-M3F3-T3R3
```

## Image Station Result

The HTML image reference was URL-encoded and the referenced folder was not at the expected relative path. The workflow now falls back to filename search under the article folder.

Detected GTQ-03 hero image:

```text
\\dlowenas\HPWorkstation\Desktop\Master HTMl\K-Production-Ready\02-genesis-to-quantum\New Folder\03-first-quantum-state\images\hero\GTQ-03 - Hero - First Quantum State.webp
```

Extracted metadata:

```text
1122x1402, WEBP, RGB
```

Nearby quote context:

```text
Article 03 - Genesis to Quantum Main Article The First Quantum State Eden as pure superposition - no entropy, no decay. Physics Quantum Theology
```

## Verification

```powershell
$env:PYTHONPATH='D:\GitHub\theophysics-brain-map\Backside\conversion_lib\src;D:\GitHub\theophysics-brain-map'
python -m pytest Backside/lossless_context_pipeline/tests Backside/conversion_lib/tests Backside/brain_dashboard/tests -q
```

Result:

```text
17 passed
```

## Boundary

The image station currently performs metadata/alt/title/caption-context extraction. It does **not** perform true semantic visual captioning yet. Next station to add: `image-caption.station`.

