# 05_CLAIMS — Claims Lane

Owner this round: **worker-2** (claude-code-worker-2) — round-1 swarm.
Pipeline step: **8**. Upstream: `02_SECTION_MAP` (hard), `07_MATH_TRANSLATION` (soft, preferred when present). Downstream: `06_CONTRADICTIONS`, `09_GRAPH_LINKS`, `10_RIGOR`, `15_SECTION_PACKETS`.

## What this lane does

Extracts per-section claims as a **three-layer arch**:

- **surface_claim** — what the section explicitly says.
- **buried_claim** — the implicit claim the surface claim presupposes.
- **operational_claim** — what the surface claim commits the reader or system to do or measure.

Plus per-claim metadata: `rhetorical_load` (low|medium|high), `domain_shift` (bool), `domain_badges` (list), `support_needed` (bool), `station_classification` (carried through from the station first pass), `confidence`.

Claim shape conforms to `configs/shared_lib/schemas.py:ClaimArch`. No fork.

## Two-pass design

This lane is not greenfield. `\\dlowenas\brain\Backside\stations\claim-extractor.station` already exists with:

- `extract.py` — splits MD/HTML on `^#{1,4}` headings, groups sentences into 1–3-sentence claim blocks, classifies via keyword signals into `AXIOM | DEFINITION | THEOREM | PREDICTION | EVIDENCE | THEOLOGICAL_POSTULATE | CONJECTURE | RESTATEMENT | EQUATION | UNCLASSIFIED`.
- `export_excel.py` — produces a review workbook.
- `config.json` — signal keywords, min/max claim length.

**Pass 1** runs `extract.py` against the article. The station's hard-coded output dir (`D:\brain\08_CLAIMS\_OUTPUT`) is overridden so output lands in `05_CLAIMS/station-firstpass.json`.

**Pass 2** is LLM-driven (see `run_prompt.md`). For each first-pass claim block, the LLM produces the surface/buried/operational triplet, rhetorical load, domain-shift flag, and badges. The station's flat `classification` is preserved on each claim as `station_classification` so downstream lanes can still target axioms/definitions/theorems specifically.

When the lane has a dedicated claim-arch model (round-2 work), pass 2 will move from LLM prompt to deterministic runner.

## Inputs

| Required | Source |
|---|---|
| `section-map.json` | `02_SECTION_MAP/` (worker-1 round-1) |
| `normalized-text.md` | `01_LOSSLESS/` (or raw `00_DROP/` file as fallback) |
| `metadata.json` | `03_YAML_METADATA/` (for `paper_uuid`, domain context) |
| `math-payload.json` (optional) | `07_MATH_TRANSLATION/` — math-translated claims preferred when present |

If `02` is absent, the lane falls back to running the station's section splitter on the raw drop file. Mock provenance is recorded under `claim-packets.json.provenance.mocked = true`.

## Outputs

| Artifact | Form |
|---|---|
| `claim-packets.json` | Machine-readable. Page + per-section ClaimArch lists. |
| `claim-ledger.csv` | Excel-ready flat projection. One row per (claim × layer). |
| `claims.md` | Human-readable rollup per section. |
| `station-firstpass.json` | Raw output of `claim-extractor.station/extract.py` for traceability. |

JSON first, Markdown second, CSV third. Excel `Claim_Ledger` sheet is a rollup of `claim-ledger.csv`, not the source of truth.

## How to run

Round-1 runner is `run_prompt.md` (LLM-first). When the local environment has Python + `bs4` + `pyyaml`:

```powershell
# Pass 1 (station first pass)
python "\\dlowenas\brain\Backside\stations\claim-extractor.station\extract.py" `
  "\\dlowenas\brain\Backside\workflows\html-article.workflow\00_DROP" `
  --format both
# Move/copy the resulting claims_<run_id>.json into 05_CLAIMS/station-firstpass.json

# Pass 2 (LLM refinement) — drive an LLM with run_prompt.md
```

A `run.py` wrapper that does both passes deterministically is round-2 work and is intentionally not added in round-1.

## Calibration check (run BEFORE GTQ-03)

Input: `00_DROP/CALIBRATION_pilot-preflight-checklist.md`

Expected (from `configs/CALIBRATION_EXPECTED.md`):

- **surface_claim**: "This checklist ensures aircraft, crew, instruments, fuel, communication systems, and safety controls are ready before flight."
- **buried_claim**: "Flight safety depends on completing standardized checks before takeoff."
- **operational_claim**: "Each checklist item must have a pass/fail state."
- **rhetorical_load**: low
- **domain_shift**: false (none expected)
- **domain_badges**: AVIATION, SAFETY, PROCEDURE
- 1 surface + 1 buried + 1 operational (minimum) for the page.
- Kill condition section should emit its own ClaimArch with operational_claim about pass/fail state.

Sample output in `sample_output/calibration/` exactly hits these targets.

## Loopback conditions

Written to `14_LOOPBACK_REVIEW/05_claims_loopback.json` when:

1. A claim depends on a source span no longer present in `01_LOSSLESS` (broken span — skip the claim, write loopback).
2. Station returns 0 claims AND text length > 200 chars (probable upstream split failure).
3. LLM refinement produces buried/operational identical to surface across all sections (prompt or input failure).
4. A math-bearing claim arrives with no matching `07_MATH_TRANSLATION` entry (math lane should revisit before rigor).

## Known gaps

- `02_SECTION_MAP` and `03_YAML_METADATA` are not produced yet (worker-1 round-1). Sample output uses mocked upstream.
- The station's hard-coded output path needs an `--output-dir` flag — file an issue to claim-extractor.station for round-2 (or override the env var path). Round-1 captures station output by post-hoc move.
- The station's keyword-signal classification can be brittle. The `confidence` field on each claim carries the station's signal score so downstream rigor knows what to trust.
- FAP overlap with claims has not been checked this round — flagged but not blocking per round-1 call.
- No Postgres write-back yet — that lives downstream in lane `12_EXPORTS`.

## Excel columns

Tab: `Claim_Ledger`. Columns: `paper_uuid`, `page_id`, `section_id`, `claim_id`, `claim_type` (surface|buried|operational), `claim_text`, `rhetorical_load`, `domain_shift`, `domain_badges`, `support_needed`, `station_classification`, `confidence`, `provenance`. Aligned to `MASTER_INDEX_WORKBOOK_CONTRACT.md`.

## Cross-references

- `04_TAGS` — the workflow tag `needs-evidence` should be emitted by lane 04 when this lane sets `support_needed = true` for a claim.
- `06_CONTRADICTIONS` — runs an NLI pass on `surface_claim` pairs. Buried + operational layers are not run through NLI in round-1.
- `10_RIGOR` — consumes `support_needed` flags to compute readiness pressure.
