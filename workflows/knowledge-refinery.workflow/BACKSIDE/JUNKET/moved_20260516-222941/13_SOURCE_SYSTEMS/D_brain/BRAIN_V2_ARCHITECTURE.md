# BRAIN V2 ARCHITECTURE

## Purpose

Lock the next-stage architecture for `D:\brain` so the workstation grows into a
reliable local-first research factory instead of a loose collection of useful
scripts.

This document is the north star for the next iteration.

---

## Inputs Reviewed

- `D:\brain\README.md`
- `D:\brain\07_POSTGRES\db_utils.py`
- `D:\brain\02_SBERT\sbert_runner.py`
- `D:\brain\03_DEBERTA\deberta_runner.py`
- `D:\brain\00_WORKFLOWS\harvest-links\pipeline.py`
- `D:\brain\_BILL_BRAIN_PACKAGE\BILL_BRAIN_PACKAGE\NLP_WORKSTATION_ARCHITECTURE.md`
- `D:\brain\_BILL_BRAIN_PACKAGE\BILL_BRAIN_PACKAGE\PROMPT-8-NLP-WORKSTATION-BUILD.md`
- `D:\brain\_LOGS\*.log`

---

## Current State

V1 is real. It is not hypothetical.

The current workstation already has the right operational bones:

- Folder-per-tool layout is simple and usable.
- Shared Postgres utilities give the system a common spine.
- Null-row resumability is the right restart pattern.
- Local model caching is correct for a Windows workstation.
- Smoke tests exist and already proved value.
- Workflows are separate from individual model runners.

The correct diagnosis is:

**V1 is a working tool rack. V2 must become a factory.**

---

## Core Architectural Decision

The external shape stays familiar:

- keep the numbered model folders
- keep `00_WORKFLOWS`
- keep local logs
- keep local model cache
- keep Postgres as the durable store

The internal logic changes:

**V2 is document-centric, run-centric, and artifact-centric.**

That means:

1. Documents become the source objects.
2. Runs become first-class records.
3. Model outputs become artifacts, not just overwritten fields.

---

## Non-Negotiable Design Principles

### 1. Document-Centric

Every pipeline begins with a document-like unit:

- URL page
- transcript
- YouTube item
- OCR output
- local text file

The system should know what a document is before it knows which model touched
it.

### 2. Run-Centric

Every execution must create a run record with:

- tool/workflow name
- config snapshot or config hash
- model name/version
- start time
- end time
- attempted count
- success count
- failure count

If a run cannot be reconstructed, it is not production-grade.

### 3. Artifact-Centric

Embeddings, classifications, clusters, fetches, OCR, and transcripts should be
treated as artifacts produced from source material, not merely as anonymous
columns hanging off random tables.

### 4. Cheap-To-Expensive Routing

Do not spend expensive inference everywhere.

Canonical sequence:

1. ingest
2. normalize
3. embed
4. route
5. classify only where needed
6. cluster
7. human review for high-value ambiguity

### 5. Reproducibility

Every important output should be traceable to:

- content hash
- source URL/path
- model identity
- config identity
- run identity

### 6. Local-First Secrets

Secrets do not belong in shared JSON configuration.

Canonical secret policy:

- root `.env` for local machine values
- `.env.example` for shared template
- config files may name secret env vars but must not store live secrets

### 7. Human Review At The Edge

The workstation should automate triage, compression, clustering, and tagging.
It should not pretend to eliminate judgment where judgment matters most.

---

## Canonical V2 Processing Model

The factory model is:

1. **Ingest raw**
   - fetch URL
   - read file
   - load transcript
   - import JSON/API result

2. **Normalize**
   - canonical URL
   - content hash
   - dedupe
   - metadata cleanup

3. **Create document version**
   - preserve raw text
   - preserve cleaned text
   - preserve extraction metadata

4. **Chunk where needed**
   - long pages should not be handled as one giant blob
   - chunked text is a first-class representation

5. **Embed**
   - generate vector artifacts
   - store model/version and dimensionality

6. **Route**
   - nearest-neighbor or heuristic routing
   - identify uncertain or strategically important items

7. **Classify**
   - run zero-shot or task-specific labeling
   - store score distributions where useful

8. **Cluster**
   - cluster on embeddings
   - surface representatives and anomalies

9. **Review**
   - prioritize uncertain, novel, or strategically high-value clusters

10. **Publish**
   - write final artifacts to Postgres
   - export CSV/JSON/report mirrors

---

## Canonical V2 Data Model

This is the target model for the dedicated schema session.

### Source Layer

- `sources`
- `source_fetch_events`

### Document Layer

- `documents`
- `document_versions`
- `document_chunks`

### Artifact Layer

- `embeddings`
- `classifications`
- `clusters`
- `ocr_artifacts`
- `transcripts`

### Execution Layer

- `brain_runs`
- `brain_run_items`
- `brain_errors`

### Review Layer

- `review_queues`
- `review_decisions`

---

## Canonical V2 Folder Direction

The current folder structure stays.

Later additions should be:

- `D:\brain\_CORE\`
  - shared settings
  - env loading
  - logging helpers
  - path helpers
  - run-context helpers

- `D:\brain\_STATE\`
  - checkpoints
  - cached manifests
  - resumable cursor state where DB null-queries are not enough

- `D:\brain\_EVAL\`
  - labeled gold sets
  - evaluation scripts
  - benchmark outputs

- `D:\brain\_EXPORTS\`
  - durable workflow outputs meant for handoff

This is a controlled extension, not a rewrite.

---

## Immediate Decisions Locked Now

These decisions are now fixed unless a later audit breaks them:

1. Keep the current folder-per-tool operator experience.
2. Keep Postgres as the durable operational store.
3. Keep local output mirrors for operator visibility.
4. Centralize secrets into root `.env` instead of shared JSON.
5. Do not attempt the full schema redesign in the same session as small hardening work.
6. Treat SBERT as the broad routing layer and DeBERTa as the heavier semantic layer.
7. Add evaluation before adding more model complexity.

---

## Priority Order

### Phase 1: Lock And Harden

- write this architecture document
- clean secrets out of shared config
- keep the current system operational

### Phase 2: Schema Session

- define `documents / artifacts / runs`
- write migrations
- map current tables into the new model

### Phase 3: Workflow Refactor

- update workflows to emit run records
- separate raw documents from derived artifacts
- introduce chunk-aware processing

### Phase 4: Evaluation Layer

- build a labeled gold set
- score classifiers and routing
- track drift across model/config changes

### Phase 5: Operator Surface

- reports
- dashboards
- priority queues

---

## Explicitly Parked

The following items are intentionally deferred:

- full Postgres schema redesign
- mass rewiring of all runners
- dashboard/UI work
- broad multi-agent orchestration
- major model additions

Those belong in dedicated sessions, not in a cleanup pass.

---

## Success Criteria

V2 is successful if:

- a secret is never required to live in shared JSON
- a run can be reconstructed after the fact
- long documents are processed as structured chunks, not crude truncations
- expensive classifiers are not run blindly on everything
- outputs can be compared across model versions
- the system reduces grunt work without creating audit fog

---

## My Call

The workstation does not need a philosophical overhaul.

It needs discipline at the seams:

- secrets
- run tracking
- artifact separation
- chunking
- evaluation

That is the difference between a smart local toolkit and a durable research
engine.

---

## Audit Footer

### Where We Are Right

- The existing workstation already has real momentum and useful abstractions.
- The shared DB helper and resumable batch pattern are the strongest parts of the current design.
- The next gains are architectural and operational, not conceptual.

### Where We Might Be Wrong

- If the main bottleneck is human review capacity rather than model throughput, evaluation and queue design may deserve to move up even earlier.
- If this system is meant to stay strictly private and never be versioned, some provenance machinery could be lighter than described here.
- If future workflows become multimodal first, the chunk/document model will need to absorb image and audio artifacts more explicitly.

### What We Think

- `D:\brain` is worth building seriously.
- The right move is not to throw away V1, but to formalize the factory model around it.
- V2 should make the system more auditable, more resumable, and less dependent on memory or luck.
