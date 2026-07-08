# X Drive Root Reorg Target - 2026-05-20

**What this is:** The new target contract for cleaning `X:\` before more build work lands there.
**Owner:** David Lowe + Codex
**Status:** applied to live `X:\` on 2026-05-20
**Source of truth:** `X:\` is `\\dlowenas\brain`

Execution evidence:

- Live migration log: `X:\Backside\_archive\root\ROOT_REORG_LOG_2026-05-20.md`
- Repo copy: `Backside/_archive/root/ROOT_REORG_LOG_2026-05-20.md`
- Vectorization queue: `Backside/_state/vectorization_queue/root-corpus-moves-20260520.csv`

## Decision

The root should stop being the runtime shelf. The root should be a front door.

Target visible root:

```text
X:\
  David\
  GUI\
  Conversions\
  EXPORTS\
  Backside\
  README.md
  ARCHITECTURE.md
  THEOPHYSICS_PRIMER.md
  RUN_*.bat
```

Everything machine-facing belongs under `X:\Backside\`. Finished reproducible output packages stay under `X:\EXPORTS\`. Active format conversion gets a front door under `X:\Conversions\`. User-facing dashboards and control panels live under `X:\GUI\`. Human notes and maps stay under `X:\David\`.

## Outside Folders

These are the folders David should see and use directly:

| Folder | Purpose |
|---|---|
| `X:\David` | Human-facing notes, maps, session entrypoints, and personal working surfaces. |
| `X:\GUI` | Dashboards and control panels, including the Brain Dashboard. |
| `X:\Conversions` | Active conversion surface: convert source files/URLs into canonical Markdown and future output formats. |
| `X:\EXPORTS` | Final reproducible output packages: HTML, Excel, metadata, manifests, reports, and anything needed to rebuild or verify the artifact. |
| `X:\Backside` | Runtime machinery, models, workflows, stations, services, control-plane repos, archives, logs, state, and corpus/data lanes. |

## Backside Front Door

`X:\Backside\` becomes the workhorse layer, not a junk drawer.

```text
X:\Backside\
  README.md
  _archive\
  _logs\
  _models\
  _state\
  apps\
  control-plane\
  corpus\
  services\
  stations\
  workflows\
```

## Canonical Moves

| Current root path | Target path | Reason |
|---|---|---|
| `X:\Backside\brain_dashboard` | `X:\GUI\brain-dashboard` | Dashboard is a user-facing surface and should be outside Backside. |
| `X:\Backside\conversion_lib` | `X:\Conversions\conversion-layer` | Conversion is a frequently used front door, not hidden machinery. |
| `X:\models` | `X:\Backside\_models\downloaded` | Downloaded weights belong behind the model front door. |
| `X:\Backside\models` | `X:\Backside\_models\legacy-model-layer` | Preserve existing model wrappers and health scripts while normalizing under `_models`. |
| `X:\Preference Engine Build` | `X:\Backside\control-plane\Preference Engine Build` | Preference layer is control-plane machinery, not a root item. |
| `X:\knowledge-refinery` | `X:\Backside\workflows\knowledge-refinery.workflow` | Refinery is a live workflow runtime; Backside owns runtime machinery. |
| `X:\paper-proof-grader` | `X:\Backside\workflows\paper-proof-grader.workflow` | Paper grader is a workflow runtime. |
| `X:\session-handoff-drop` | `X:\Backside\workflows\session-handoff.workflow` | Session capture is a workflow runtime. |
| `X:\link-pull-drop` | `X:\Backside\workflows\link-pull.workflow` | Link capture is a workflow runtime. |
| `X:\ai-portal-generator` | `X:\Backside\workflows\ai-portal-generator.workflow` | Portal generator is a workflow runtime. |
| `X:\axioms` | `X:\Backside\workflows\axioms.workflow` | Axiom refresh is a workflow runtime. |
| `X:\ollama` | `X:\Backside\services\ollama` | Ollama is a local service layer, not a root workflow. |
| `X:\github` | `X:\Backside\control-plane\github` | Repo mirrors are control-plane material. |
| `X:\_LOGS` | `X:\Backside\_logs` | Logs should be out of the root. |
| `X:\_brain_DEPRECATED_20260516` | `X:\Backside\_archive\root\_brain_DEPRECATED_20260516` | Deprecated root material belongs in archive. |
| `X:\00_CONVERSION` | `X:\Backside\_archive\root\00_CONVERSION` | Legacy conversion staging should leave the root. |
| `X:\captures` | `X:\Backside\_state\captures` | Capture state is machine-facing. |
| `X:\digests` | `X:\Backside\_state\digests` | Digest state is machine-facing. |
| `X:\embeddings` | `X:\Backside\_state\embeddings` | Embedding caches are machine-facing. |
| `X:\ratings` | `X:\Backside\_state\ratings` | Rating outputs are machine-facing unless exported. |
| `X:\C4C` | `X:\Backside\corpus\C4C` | Corpus content should be grouped, not root-scattered. |
| `X:\C4C-wiki` | `X:\Backside\corpus\C4C-wiki` | Corpus companion wiki. |
| `X:\FAP` | `X:\Backside\corpus\FAP` | Source corpus/scaffold, distinct from workflow runtime. |
| `X:\BIL` | `X:\Backside\corpus\BIL` | BIL corpus placeholder / future corpus lane. |
| `X:\proof-architecture` | `X:\EXPORTS\proof-architecture` | Publish/output sink, not runtime. |
| `X:\proof-explorer` | `X:\EXPORTS\proof-explorer` | Publish/output sink, not runtime. |

## Compatibility Rule

Do not silently break old paths. The migration must either:

1. update every known script/config reference to the new path, or
2. leave an explicit compatibility pointer at the old location for one transition cycle.

Root-level compatibility pointers should be temporary and named in the migration log. They are allowed only to keep old runners alive while path references are updated.

## Model Front Door

`X:\Backside\_models\README.md` is the model front door. It must answer:

- which model folders exist,
- what each model is for,
- whether it is a real downloaded weight, wrapper, or conceptual model lane,
- which workflows consume it,
- how to health-check it.

Downloaded 2026-05-19 model folders found at `X:\models`:

```text
bart_summarizer
clip_vision
deberta_nli
mistral_7b
sbert_minilm
whisper_large_v3
```

These should move under `X:\Backside\_models\downloaded\`.

## Migration Sequence

1. Commit this target contract.
2. Add/update `Backside` docs and root README docs to point at the new shape.
3. Generate a dry-run migration report from live `X:\`.
4. Move low-risk folders first: deprecated/archive/log/state/model folders.
5. Move live workflows only after launchers/config references are patched or compatibility pointers are prepared.
6. Run health checks and record which old root paths remain as temporary compatibility pointers.

## /PROBE

The weak point is hard-coded path drift. If a workflow assumes `X:\knowledge-refinery` or `X:\paper-proof-grader`, moving the folder without a pointer breaks the run. The fix is not to leave the root dirty forever; the fix is to move with an explicit compatibility layer and then delete the compatibility layer only after all references are updated.

## Vectorization Queue

The root cleanup exposed four corpus lanes that should be indexed as corpus, not treated as runtime machinery:

| Target path | Files | Candidate text files | Candidate text bytes | Index status |
|---|---:|---:|---:|---|
| `X:\Backside\corpus\C4C` | 2,497 | 1,198 | 196,611,541 | needs vector index |
| `X:\Backside\corpus\C4C-wiki` | 862 | 839 | 39,198,724 | needs vector index |
| `X:\Backside\corpus\FAP` | 63 | 24 | 60,894 | needs vector index |
| `X:\Backside\corpus\BIL` | 1 | 1 | 858 | needs vector index |

Also index `X:\Backside\_state\digests` as small operational summaries: 14 candidate text files, 48,529 bytes.

Do not vectorize model weights under `X:\Backside\_models`. Workflows should be indexed only as workflow/station metadata unless a workflow explicitly emits corpus content.
