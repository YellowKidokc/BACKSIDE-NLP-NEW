# Vectorization Front Door — Implementation Assignment

**Status:** open · awaiting an AI partner to claim it
**Created:** 2026-05-19 by claude-code-forge
**Estimated effort:** ~3–5 hours focused work, including smoke tests
**Owner once claimed:** whoever picks it up posts ARRIVED to comms and owns it through green-smoke

---

## TL;DR for the inviter (David or another coordinating AI)

A versioned vector-store front door has been **fully spec'd and scaffolded** at `X:\embeddings\`. What's missing is the implementation of two Python modules: `corpus_writer.py` and `corpus_query.py`. The spec is normative, the brief is self-contained, the work is parallelizable in the sense that one AI can finish it end-to-end without coordination overhead. Codex is the natural owner (per AI partner role allocation: Codex = X drive infra), but any of Sonnet / Opus / Codex can take it.

**To invite a partner to take this on**, copy the "Prompt to send" block below into:
- The target AI's direct channel on comms hub (e.g. `codex`), OR
- The relevant workflow room (`workflow-1` for Brain/Obsidian)

---

## What's been done

- `X:\embeddings\README.md` — folder overview (Layer 1 + Layer 2 contract)
- `X:\embeddings\CORPUS_SPEC.md` — full Pattern C specification (versioned upsert, integrity invariants, schema)
- `X:\embeddings\_AGENT_BRIEF.md` — detailed implementation brief, build order, function signatures, smoke-test gates
- `X:\embeddings\corpus.yml` — runtime config mirroring the spec
- `X:\embeddings\STATUS.md` — honest snapshot of what's in the store today vs what the spec calls for
- This repo's `CORPUS_SPEC.md` — mirror of the spec for GitHub version history

## What's NOT done (the work being prompted out)

- `X:\embeddings\corpus_writer.py` — write functions, anchor hashing, Pattern C logic
- `X:\embeddings\corpus_query.py` — query functions, active-filter, similarity search
- `X:\embeddings\tests/smoke_test.py` — the gate: new → idempotent → revision → query → history-include
- `X:\embeddings\STATUS.md` update reflecting post-implementation state

---

## Prompt to send

Copy this entire block into the target AI's channel:

---

> You're being invited to implement the vectorization front door for David Lowe's Theophysics brain.
>
> **Read first (in order):**
> 1. `X:\embeddings\README.md` — what the folder is and the contract it owns
> 2. `X:\embeddings\CORPUS_SPEC.md` — the policy (Pattern C versioned upsert). Read in full. If you'd argue with it, say so in comms before coding.
> 3. `X:\embeddings\_AGENT_BRIEF.md` — your mission card: build order, function signatures, smoke test, coordination points
> 4. `X:\embeddings\corpus.yml` and `STATUS.md` — runtime config + current state of the store
>
> **Build:** `corpus_writer.py` and `corpus_query.py` in `X:\embeddings\`, per the signatures in the BRIEF §Step 2–3. Add `tests/smoke_test.py` per §Step 4. Update `STATUS.md` per §Step 5. Post to comms per §Step 6.
>
> **Constraints:** Pattern C is canon for this front door. No silent deviations from the spec — if something genuinely doesn't work, post to comms and pause. `qdrant-client` and `sentence-transformers` are already available in the brain's Python env; new deps need flagging. No file deletion (move to `_ARCHIVE/` instead per X:\ standing rule). Independence rule applies — check `codex` / `claude-code` / `workflow-1` channels first to make sure nobody else has started.
>
> **Success bar:** any AI in the hive can call `from corpus_query import query_similar_claims` and get back active-only project-wide retrieval, without ever touching Qdrant directly or reasoning about IDs. That's what you're shipping.
>
> Post ARRIVED on your channel when you start. Post a one-line update when smoke goes green. The full brief at `X:\embeddings\_AGENT_BRIEF.md` is your source of truth — this message is just the invitation.

---

## Coordination notes for the inviter

- **Don't invite two AIs to the same module.** The work decomposes cleanly into one owner. If you want parallelism, the natural split is "writer" + "query" but they share enough internals (config loading, client construction, anchor logic) that one person doing both is faster than two coordinating.
- **The spec has 4 open decisions in SPEC §8** — `session_handoffs` rename, cosmetic-diff policy, TTL, race policy. Defaults are picked; the implementer doesn't block on these. David can ratify after first working version lands.
- **Diagnose `paper_proof_grader` collection separately.** STATUS notes that the docs claim PPG writes to a `paper_proof_grader` collection but no such collection exists. That's a PPG bug, not a front-door bug. Don't bundle it.

---

## Where this comes from

David's directive 2026-05-19: vectorization is workflow-level / front-door-level, not station-level. Stations emit; the front door persists. Pattern C (versioned + active flag) chosen because the framework's value is partly in the refinement arc — overwriting prior versions would erase the history Theophysics depends on.

Spec drafted to be GitHub-versioned in this repo so the contract has change history independent of the live X:\ copy.

---

*If you take this on, you own it through smoke-test green. Post ARRIVED.*
