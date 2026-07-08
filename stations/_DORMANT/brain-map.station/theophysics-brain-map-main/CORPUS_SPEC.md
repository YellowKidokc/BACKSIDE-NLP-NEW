# Corpus Specification — Pattern C (Versioned Upsert)

**Spec version:** 0.1 (draft)
**Last updated:** 2026-05-19
**Owner:** David Lowe · drafted by claude-code-forge
**Status:** draft · awaiting implementation
**Live location on brain:** `X:\embeddings\CORPUS_SPEC.md` (this file mirrors it for GitHub version history)

The contract every NLP that touches the vector store must honor. This document is authoritative. If the code disagrees with the spec, the code is wrong.

---

## 1. Why this exists

The pathological case: re-running a paper through the pipeline produces a "new" claim that is semantically identical to yesterday's claim. The contradiction engine, naively configured, flags the new claim as contradicting the old claim — even though they're the same idea. The engine starts screaming at phantom contradictions, signal-to-noise collapses, the output becomes untrustable.

Pattern C — versioned upsert with an `active` flag — prevents this by giving every claim a stable anchor, tracking its revision lineage, and exposing only the latest version to default queries.

---

## 2. Collections

The store hosts multiple collections, one per object type. All collections honor this spec.

| Collection name      | What lives here                                | Dim | Model                | Anchor scope                          |
|----------------------|------------------------------------------------|-----|----------------------|---------------------------------------|
| `claims_corpus`      | Every claim extracted from every paper         | 384 | `M-EMB-GEN-001` (MiniLM) | per workflow + source_doc + claim text |
| `axioms_corpus`      | 188 technical + 22 public axioms               | 768 | `M-EMB-SCI-001` (SPECTER2) | per axiom_id                           |
| `papers_corpus`      | Per-paper document-level embeddings            | 768 | `M-EMB-SCI-001` (SPECTER2) | per source_doc                         |
| `sessions_corpus`    | Session handoff summaries (renamed from `session_handoffs`) | 384 | `M-EMB-GEN-001` | per session_id                         |

**Existing today:** `session_handoffs` (one collection, contents unverified by this spec). Migration to `sessions_corpus` is a transition task.

**Created on first write:** all others. Collection creation is idempotent — the writer creates if missing, no-ops if present.

---

## 3. Point ID scheme

Qdrant point IDs must be UUIDs or unsigned integers. We use **deterministic UUIDv5** so the same (anchor, version) pair always produces the same ID.

```
namespace_uuid  = UUID('a1b2c3d4-0000-0000-0000-000000000001')   # constant, defined in corpus.yml
corpus_id_str   = f"{claim_anchor}__v{version}"                  # human-readable
point_uuid      = uuid.uuid5(namespace_uuid, corpus_id_str)      # Qdrant point id
```

Where `claim_anchor` is:

```python
claim_anchor = sha256(
    f"{workflow_id}|{source_doc_id}|{canonicalize(claim_text)}"
).hexdigest()[:16]
```

`canonicalize(claim_text)` strips whitespace, lowercases, removes punctuation runs. Two claims with cosmetic differences hash the same → idempotent re-upsert. Two claims with semantic differences hash differently → distinct anchors.

**Why anchor + version:** the anchor is the *identity* of the claim across revisions. The version is the *generation*. Together they're the corpus_id. Without versioning, revising a claim would silently overwrite the old vector and erase the refinement history Theophysics depends on.

---

## 4. Payload schema

Every point carries this payload. Fields marked **required** are non-nullable. Additional fields are allowed (tags, metrics, anything else).

```yaml
corpus_id:         "abc123def456__v1"     # required, str  — human-readable identity
claim_anchor:      "abc123def456"          # required, str  — stable hash (no version)
version:           1                       # required, int  — starts at 1
active:            true                    # required, bool — only the highest version is true
superseded_by:     null                    # str or null    — corpus_id of next version, when versioned

source_doc_id:     "gtq-01-measurement"    # required, str  — stable paper/source identifier
source_doc_path:   "X:/knowledge-refinery/.../source.md"  # str — best-effort, may go stale
workflow:          "paper-proof-grader"    # required, str  — which NLP wrote this
station_id:        "ST-CLAIM-001"          # str — which station emitted the claim, if traceable

text:              "Surrender is the physics of grace."   # required, str — the actual claim text
text_canonical:    "surrender is the physics of grace"    # str — what was hashed
text_chars:        37                                     # int

model_id:          "M-EMB-GEN-001"         # required, str — which embedding model produced the vector
model_dim:         384                     # required, int

created_at:        "2026-05-19T03:14:00Z"  # required, ISO8601 UTC
created_by:        "claude-code-forge"     # str — AI partner or human who triggered the write

tags:              ["axiom-touchpoint:A1.1", "7q-pass"]   # list[str] — free-form labels
```

---

## 5. Lifecycle operations

### 5.1 `write_claim(...)` — the only public write entry point

Resolves one of three cases based on whether the anchor exists:

| Case               | Trigger                                                              | Action                                                                                                            |
|--------------------|----------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| **new**            | `claim_anchor` not in collection                                     | upsert at `version=1`, `active=true`. Return `corpus_id`.                                                          |
| **idempotent**     | `claim_anchor` exists, `text_canonical` matches latest active version | no-op. Return existing `corpus_id`. Log at INFO.                                                                   |
| **revision**       | `claim_anchor` exists, `text_canonical` differs from latest active   | upsert at `version=N+1`, `active=true`. Patch previous active point: `active=false`, `superseded_by=<new corpus_id>`. Return new `corpus_id`. |

The check uses payload filtering: `filter: {claim_anchor==X, active==true}`. If zero results → new. If one → compare text_canonical. If >1 active for the same anchor → **integrity error** (raise, don't auto-heal).

### 5.2 `write_claims_batch(...)`

Same semantics applied per-claim, in a single batched upsert call. Failures in the batch don't abort the whole batch — log and continue.

### 5.3 `query_similar_claims(text, k=10, filters=None, include_history=False)`

- Embeds `text` with the collection's bound model.
- Searches by cosine similarity, top-k.
- **Default filter: `active=true`.** Pass `include_history=true` to also return inactive versions.
- Additional `filters` merge into the search filter (e.g. `{"workflow": "paper-proof-grader"}`).

### 5.4 `query_active(filter, limit=100)`

Plain payload-filter query. Returns latest-active points matching the filter. Useful for "give me all claims from paper X" or "all claims tagged with A1.1."

### 5.5 `rollback(claim_anchor, to_version)` *(rare, manual)*

Flips a previous version back to active and demotes whatever was active. Audit-logged. Reserved for human intervention.

---

## 6. Integrity invariants

These MUST hold at all times. The writer enforces; the rebuilder (when written) repairs.

1. **Single active per anchor.** For any `claim_anchor`, exactly one point in the collection has `active=true`.
2. **Monotonic versions.** Versions increment by 1. No gaps, no duplicates.
3. **Superseded chain.** If `version=N` has `active=false`, its `superseded_by` MUST point to a real `corpus_id` with `version=N+1`.
4. **Latest is leaf.** The active version has `superseded_by=null`.

Violation of any invariant is a bug, not a state to query around.

---

## 7. What the front door is NOT

- **Not a router.** It doesn't decide which collection a write goes to. The caller (workflow/NLP) specifies `collection_name`.
- **Not a model.** It doesn't embed text on its own — it delegates to the bound model named in `corpus.yml` for that collection.
- **Not a contradiction engine.** It supplies retrieval, not judgment. The contradiction engine sits *on top of* this and uses `query_similar_claims` to find candidates.
- **Not a station.** Stations transform; the front door persists.

---

## 8. Open decisions (David ratifies)

1. **Migration:** rename `session_handoffs` → `sessions_corpus` or leave as-is? Renaming requires recreating the collection (Qdrant doesn't rename in place). Leaving as-is means the spec has one "legacy name" exception forever.
2. **Whose claim text wins on cosmetic diff?** If the canonical form matches but the raw text differs (e.g. punctuation, capitalization), do we update `text` to the new raw or keep the first one written? Spec currently says "no-op" which keeps the first.
3. **TTL on `active=false` points?** Forever, or sunset after N years to bound storage? Theophysics is 15 months old; storage is cheap; spec defaults to *forever*.
4. **Two writers racing on the same anchor.** Qdrant upserts are atomic per-point but not transactional across the read-then-write of a revision. Two AIs revising the same claim simultaneously could create two `version=N+1` points (one would win the active flag race). For now: accept the race, log, manual cleanup. Future: per-anchor lock file in this directory.

---

## Related

- `X:\embeddings\_AGENT_BRIEF.md` — implementation assignment for whoever builds `corpus_writer.py` / `corpus_query.py`
- `X:\embeddings\corpus.yml` — the runtime config that mirrors this spec
- `X:\embeddings\STATUS.md` — what exists today vs what this spec calls for
- This repo's `00_WORKFLOWS/prompts/vectorization-front-door/00_BRIEF.md` — the ready-to-paste implementation prompt
