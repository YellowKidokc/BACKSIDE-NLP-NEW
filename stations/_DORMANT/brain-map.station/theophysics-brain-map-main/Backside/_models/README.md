# Backside Model Registry

**What this is:** The registry for models and NLP lanes used by the X-drive Brain.
**Owner:** shared
**Status:** live map
**Last updated:** 2026-05-20

This folder holds model cards, routing contracts, and evaluation notes. It does **not** hold large model weights in git.

Live weights and runtime caches belong on X:\ under the Backside model front door:

```text
X:\Backside\_models\<model-name>.model\
X:\Backside\_models\downloaded\<downloaded-model-folder>\
```

`X:\models\` is now a deprecated transition path. The 2026-05-20 root cleanup contract moves downloaded models into `X:\Backside\_models\downloaded\`.

The online repo keeps only enough metadata for another AI partner to know what each model is for, what it must not do, and which workflow/station should call it.

## Core lanes

| Model lane | Purpose | Primary output |
|---|---|---|
| `timeline.model` | Build chronologies from sessions, papers, repo logs, and project events. | dated event ledger |
| `facts.model` | Extract claims with source paths, evidence, uncertainty, and contradiction flags. | provenance-first fact ledger |
| `paper-citation.model` | Sort papers into represent / close-to-us / cite / contrast / ignore buckets. | paper-citation map |

## Supporting model cards

| Model card | Purpose |
|---|---|
| `mistral-7b-instruct.model` | local general classifier/router, especially for intake |
| `deberta-v3-large.model` | NLI / contradiction / entailment scoring |
| `clip-vision.model` | figure and image understanding |
| `whisper-large-v3.model` | audio/video transcription |
| `moon-streak.model` | future theopoetic style emitter |

## Downloaded model weights found 2026-05-20

These were found live at `X:\models\` and should move to `X:\Backside\_models\downloaded\`:

| Folder | Role |
|---|---|
| `bart_summarizer` | session and digest summarization |
| `clip_vision` | image / figure understanding |
| `deberta_nli` | entailment, contradiction, and NLI scoring |
| `mistral_7b` | local classifier/router/general LLM |
| `sbert_minilm` | embeddings / semantic similarity |
| `whisper_large_v3` | audio and video transcription |

## Rule

Every model folder gets a `card.json` and ends in `.model`. If it is a conceptual lane rather than a single weight file, use `"kind": "nlp-lane"` and list the backing models or stations.

Do not add weights, embeddings, caches, exported PDFs, or raw paper corpora to this repo.
