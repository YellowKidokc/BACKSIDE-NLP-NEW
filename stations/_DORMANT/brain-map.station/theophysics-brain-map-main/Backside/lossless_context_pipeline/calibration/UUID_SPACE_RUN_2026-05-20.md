# UUID + 3D Semantic Space Calibration Run - 2026-05-20

Purpose: run multiple document types through the lossless UUID/address pipeline and produce a first 3D semantic projection.

Runtime export:

```text
X:\EXPORTS\lossless-context\calibration-corpus\20260520-uuid-space-v2
```

Projection files:

```text
X:\EXPORTS\lossless-context\calibration-corpus\20260520-uuid-space-v2\semantic-space\semantic-space.csv
X:\EXPORTS\lossless-context\calibration-corpus\20260520-uuid-space-v2\semantic-space\semantic-space.json
```

## Inputs

| Input | Type | Route |
|---|---|---|
| `Backside/lossless_context_pipeline/calibration/lossless_context_protocol_v1.md` | Markdown protocol | direct lossless run |
| `Backside/lossless_context_pipeline/samples/sample_article.md` | Markdown article | direct lossless run |
| `Backside/lossless_context_pipeline/calibration/pilot_preflight_checklist.md` | Markdown operational control | direct lossless run |
| `\\dlowenas\HPWorkstation\Desktop\Master HTMl\K-Production-Ready\02-genesis-to-quantum\gtq-03-first-quantum-state.html` | HTML article | conversion layer -> canonical Markdown -> lossless run |

## Results

| Artifact | Address | Vector |
|---|---|---|
| Protocol | `TECH/LOSSLESS-CONTEXT-COMPRESSION-SEMANTIC-ADDRESSING-PROTOCOL-V1-0/W/AI_RESEARCH/T/R1` | `G3M3E0S0T3K3R3Q0F3C3` |
| Sample article | `THEOPHYSICS/GRACE-ENTROPY-BRIDGE/W/AI_RESEARCH/R/R1` | `G3M3E0S0T3K3R3Q0F3C3` |
| Pilot checklist | `AVIATION/PILOT-PRE-FLIGHT-CHECKLIST/F/TEAM/B/R4` | `G3M3E0S0T3K3R3Q0F3C0` |
| GTQ-03 HTML | `THEOPHYSICS/GTQ-03-FIRST-QUANTUM-STATE-CANONICAL/W/AI_RESEARCH/R/R1` | `G3M3E0S0T3K3R3Q0F3C3` |

## 3D SBERT PCA Coordinates

These coordinates are not canonical identity. They are a visualization/proximity layer over the lossless artifacts.

| Artifact | x | y | z |
|---|---:|---:|---:|
| Protocol | 0.2343839086 | -0.4575717578 | -0.4541937150 |
| Sample article | 0.0590794255 | 0.7443484690 | -0.1672502990 |
| Pilot checklist | -0.7638464887 | -0.1605590275 | 0.1425829034 |
| GTQ-03 HTML | 0.4703831546 | -0.1262176837 | 0.4788611107 |

## Interpretation

- UUID/address layer worked for all three routes: Markdown protocol, Markdown article/control, and HTML-converted article.
- The aviation checklist separates structurally because `C=0`; it is procedural/safety-binding, not a synthesis artifact.
- Protocol, sample Theophysics article, and GTQ-03 share the high-integration vector `G3M3E0S0T3K3R3Q0F3C3`, but SBERT 3D projection still separates them by content.
- This supports the intended split:
  - address/vector = artifact function and identity
  - embedding/projection = semantic neighborhood
  - snapshot JSON = reconstructable proof object

## Calibration Lessons

1. `audience:` frontmatter must alias to `access:`.
2. A checklist must score `K=3` even without equations or citations because it is structured operational knowledge.
3. `C=3` should not be awarded just because a checklist is coherent.
4. `E=3` should not be awarded just because a document discusses entropy/collapse.
5. The 3D projection is useful for navigation, but it must not replace the permanent address.

## Next

Build `RUN_CALIBRATION_CORPUS.bat` after the next round, then expand the corpus to at least 20 artifacts:

- 5 Theophysics articles
- 5 operational docs/checklists
- 5 code/workflow specs
- 5 personal/testimonial or affective artifacts

That will make the 3D space meaningful enough to inspect clusters.
