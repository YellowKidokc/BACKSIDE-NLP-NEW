# ST-AXIOM-001 — Axiom Promotion Gate

**Lane:** axiom
**Status:** active
**Folder:** `10_STATIONS/ST-AXIOM-001_promotion_gate`

## Purpose

Decide whether a candidate axiom is ready to be promoted into the 188-axiom canon (mirror: PostgreSQL @ `192.168.1.177:2665`, file source: `D:\01_Axioms\_001-188\`).

The gate verifies three things:

1. **Spine hookup** — the candidate connects cleanly into the derivation chain (Truth → Existence → Grounding → Observation → Moral Physics → Spiritual Reality → Grace).
2. **Non-contradiction** — does not violate any of the 188 standing axioms or the 22 public axioms in `D:\PUB_AXIOM_FOUNDATIONS\`.
3. **Gradient honesty** — labeled correctly as **load-bearing**, **suggestive**, or **overclaimed** per the contract (R7).

## Mental model

```
WORKFLOW -> STATION -> MODEL -> PROMPT -> SCRIPT -> OUTPUT -> GATE -> NEXT STATION
                ^
              you are here
```

Upstream: anything producing a candidate axiom (e.g. ST-7QS-003 evidence_pressure, or manual drop into `input/`).
Downstream on pass: `ST-AXIOM-002` (canon writer).
Downstream on fail: `ST-ERR-001`.

## Folders

| Folder    | What goes here                                                    |
|-----------|--------------------------------------------------------------------|
| `prompts/`| `P-AXIOM-001.md` (promotion review) and `P-AXIOM-002.md` (strict). |
| `scripts/`| `S-AXIOM-001` — `run_promotion_gate.py`.                           |
| `input/`  | One subfolder per candidate: `input/<candidate-slug>/candidate.md` + `derivation.md`. |
| `output/` | `verdict.json`, `verdict.md`, and (on accept) `canon_diff.md`.     |
| `review/` | Borderline calls — confidence below threshold or ambiguous gradient.|
| `logs/`   | One log file per run, append-only.                                 |
| `errors/` | Failed candidates with the trace.                                  |

## Gate

```
pass_if:
  - valid_json: true
  - decision_in: [accept, accept_with_revisions]
  - no_contradictions_with_canon: true
  - hooks_into_spine: true
  - gradient_labeled: true
```

Anything failing → `errors/` + route to `ST-ERR-001`.
Anything below confidence threshold → `review/` for human eye.

## Wiring notes

- Canon source of truth: `D:\01_Axioms\_001-188\` (files) and Postgres mirror (queryable).
- Spine reference: see `project_derivation_chain_spine` memory and the canon channel in comms.
- Per the contract: **no destructive writes**. Even on accept, this station only proposes a diff — actual canon insertion happens at `ST-AXIOM-002`.
