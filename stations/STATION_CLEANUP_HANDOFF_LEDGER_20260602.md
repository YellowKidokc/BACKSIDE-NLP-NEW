# Station Cleanup Handoff Ledger - 2026-06-02

## Rule

Do not bulk-clean from this point. Treat this ledger as the stop sign before any future station pass.

## Protected Roots

These roots were not edited in this cleanup pass and must not be touched by station hygiene jobs unless explicitly assigned:

- `X:\Backside\knowledge-refinery`
- `\\dlowenas\brain`
- `X:\brain`
- `X:\Backside\apps`
- `\\dlowenas\*\apps`

Observed references to these roots inside station docs/prompts are context references, not permission to move or rewrite those roots.

## Workflow Classification

| Workflow / Station | Classification | Reason | Next Rule |
|---|---|---|---|
| `deberta-runner.station` | LIVE | Export hygiene completed, root `EXPORTS` wired, later marked GREEN by David after operational checks. | Do not clean further unless model/config behavior changes. |
| `paper-recommender.station` | REVIEW_LATER | Export-safe skeleton with no runner/orchestrator and no sample output pair. | Needs implementation before GREEN; do not invent runner during cleanup. |
| `html-article.station` | LIVE | Export hygiene and local smoke wiring passed; canary output rooted in `EXPORTS`. | Keep `sample_output` fixtures; workflow completeness remains YELLOW by design. |
| `hdbscan-cluster.station` | LIVE | Export hygiene completed, dependency installed, self-test passed. | Live Postgres production run not exercised; do not call production GREEN from self-test alone. |
| `paper-grader-nlp.station` | LIVE | Export hygiene completed, local smoke run produced JSON/MD/HTML/CSV/XLSX under `EXPORTS`. | Keep nested `paper-proof-grader` scaffold until David decides ownership. |
| `math-translation-layer.station` | DO_NOT_ARCHIVE | Heavy unfinished lane with app/build/test structure, `node_modules`, `dist`, `exports`, and workflow-specific scripts. | Park it. No cleanup without explicit math-layer assignment. |
| `math-layer.station` | DO_NOT_ARCHIVE | Parallel math-layer scaffold; likely related to math-translation layer. | Park it. Do not merge with `math-translation-layer.station` blindly. |
| `paper-intelligence-suite.station` | DO_NOT_ARCHIVE | Large multi-lane suite with OpenAI/7Q/vector/HTML/report components and active `OUTPUT`. | Requires its own dedicated pass; do not bulk-move. |
| `html-article.station\07_MATH_TRANSLATION` | CONTEXT_ONLY | Lane fixture and active canary outputs exist; heavy math translation semantics are not cleanup material. | Keep parked unless assigned to math lane. |
| `html-article.station\configs\FILE-NAMING-SYSTEM.md` | CONTEXT_ONLY | Naming policy reference, not stale material. | Do not rename sources based on this without a naming task. |
| `html-article.station\08_SECTION_VECTORS` | CONTEXT_ONLY | Vector lane now writes root outputs for live tests, but vector semantics remain part of workflow design. | Do not rewrite vector contracts in hygiene pass. |
| OpenAI / o3 / vector lanes in `paper-intelligence-suite.station` | DO_NOT_ARCHIVE | Heavy/unfinished intelligence stack; not part of export cleanup closeout. | Needs separate assignment. |
| Proof injection / Master HTML injection references | REVIEW_LATER | Not directly altered in these station passes. | Handle only from the Master HTML/proof-injection workflow, not from station cleanup. |

## What Was Confirmed

- No protected roots were edited by this final pass.
- No active `_CANARY_RUNS` remains in `html-article.station`; old canaries were copied, verified, archived, and rerouted to `EXPORTS`.
- No active `OUTPUT` remains in `paper-grader-nlp.station`; the empty legacy folder was copied, verified, and archived.
- No unarchived `__pycache__` remains in the stations checked after final cleanup.
- `sample_output` fixtures in `html-article.station` are contract evidence and must not be deleted.
- Paper-grader 7Q/7QS surfaces are schema/UI/report logic, not duplicate cleanup targets.

## Stop Conditions

Abort future bulk cleanup if any pass proposes to:

- Delete or move `sample_output` fixtures without a lane-contract replacement.
- Merge `math-layer.station` with `math-translation-layer.station`.
- Rewrite references into `knowledge-refinery`, `brain`, or `apps`.
- Treat `paper-intelligence-suite.station` as simple output cleanup.
- Treat 7Q/7QS schema, UI, prompt, and report surfaces as duplicates merely because names overlap.

## Status Sentence

Good workflows are close enough for export hygiene, but not safe for bulk cleanup. Continue one station at a time with explicit LIVE / CONTEXT_ONLY / REVIEW_LATER / DO_NOT_ARCHIVE classification before any move.
