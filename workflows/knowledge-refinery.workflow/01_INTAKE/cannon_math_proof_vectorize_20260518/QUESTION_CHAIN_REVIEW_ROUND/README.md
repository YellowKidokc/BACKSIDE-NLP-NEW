# QUESTION_CHAIN_REVIEW_ROUND — Holding Folder for All Open Objections

**Canonical instructions:** see `CRITIQUE_ROUND_PROMPT.md` in this folder. That document is the authoritative workflow; this README is just a quick-navigation index.

## What lives where

### Top level (this folder)

| File | Author | Scope |
|---|---|---|
| `CRITIQUE_ROUND_PROMPT.md` | review-round architect | The canonical workflow: how to critique, where to put critique files, status taxonomy, owner-discretion rule (adopt/adapt/defer/reject). |
| `QUESTION_CHAIN_INDEX.md` | David / chain author | The 25-question index. Reference copy. |
| `OPUS_OBJECTIONS_TO_QUESTION_CHAIN.md` | opus-atlas | Comprehensive cross-cutting Opus review — per-question objections, structural issues, missing-question diagnosis, framework-overlap notes, recommended IMPROVEMENT_ROUND_1 decisions. The single-document overview of the entire opus critique. |
| `CURRENT_UNRESOLVED_OBJECTIONS_LEDGER_GPT.md` | GPT (copied from parent folder) | Framework-level open objections: product form, mediator specificity, love-field axiom, etc. NOT chain-level — framework-level. Pulled in so the two registers can be read side by side. |

### Sub-folders

```
00_INBOX_RAW_PARTNER_OUTPUTS\   — raw layer output from partners awaiting staging
01_BY_LAYER\                    — material organized by layer ownership:
  L1_HOOK_DAVID\
  L2_HUMAN_STORY_GEMINI\
  L3_METAPHYSICAL_OPUS\
  L4_THEOLOGICAL_KIMI\
  L5_PHYSICS_OPUS\
  L6_MATH_LEAN_CODEX\
  L7_OBJECTIONS_GPT\
02_BY_QUESTION\Q00..Q25\        — per-question folders, each with:
  00_SOURCE_LAYERS\
  01_INTEGRATED_DRAFT\
  02_OBJECTIONS_AND_CRITIQUE\   ← per-question critique files go here, using the per-Q template
  03_REVISION_NOTES\
  04_FINAL_CANDIDATE\
03_CROSS_CRITIQUE\              — partner cross-cuts:
  CODEX_REVIEWS\
  GEMINI_REVIEWS\
  GPT_REVIEWS\
  KIMI_REVIEWS\
  OPUS_REVIEWS\                 ← opus cross-cutting reviews live here
04_INTEGRATED_DRAFTS\           — drafts that have absorbed multiple critiques
05_CANON_CANDIDATES\            — final question-files ready to graduate to ..\
99_ARCHIVE_SUPERSEDED\          — old versions retired by later revisions
```

## Where Opus critiques sit right now

- **Comprehensive master file:** `OPUS_OBJECTIONS_TO_QUESTION_CHAIN.md` (top level) — full critique, single document, indexed per-question and cross-cutting.
- **Cross-cutting Opus review:** `03_CROSS_CRITIQUE\OPUS_REVIEWS\OPUS_FULL_CHAIN_REVIEW.md` — same content, placed in the proper cross-critique slot per the prompt's structure.
- **Per-question Opus critiques:** not yet staged into `02_BY_QUESTION\Q##\02_OBJECTIONS_AND_CRITIQUE\` slots. Per the prompt: *"If the amount of material becomes too large to move manually, ask Codex to run a Python staging pass."* Opus's critique is currently concentrated in the master file; per-question staging is a deferred mechanical step.

## Relationship to IMPROVEMENT_ROUND_1

When David has reviewed the objections in this folder and decided what to accept, the resulting *changes* flow into `..\IMPROVEMENT_ROUND_1\`. That folder is the destination for revised Q-files, merged questions, new questions, per-format extracts, etc. This folder is the source of critiques; IMPROVEMENT_ROUND_1 is the destination of changes.

## Other partners contributing critiques

Other AIs reviewing the chain should drop their critiques per the `CRITIQUE_ROUND_PROMPT.md` instructions:

- Stagger starting points (Opus from Q00 forward, GPT from Q25 backward, Kimi from Q12 outward, Gemini wherever the human story is weakest, Codex wherever formal status is overstated).
- Use the per-question template in `02_BY_QUESTION\Q##\02_OBJECTIONS_AND_CRITIQUE\Q##_CRITIQUE_TEMPLATE.md`.
- Cross-cutting reviews go in `03_CROSS_CRITIQUE\<PARTNER>_REVIEWS\`.

## Independence rule

Critique the argument, not the partner. Multiple partners may critique the same question if they bring different angles. Convergence between independent critiques is signal; persistent disagreement is where the actual fault lines are.
