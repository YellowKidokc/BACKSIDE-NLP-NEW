# Axiom + 7Q Station Workflow

## Purpose

This station converts paper-proof-grader claim audits into a review package for
7Q scoring, canonical chain-node mapping, tag review, and pseudo knowledge-graph
edges.

## Runtime Home

The live runtime stays here:

```text
X:\paper-proof-grader
```

Do not duplicate the station code into `X:\knowledge-refinery`. This folder is
the workflow entrypoint and map. The runtime remains in one place so outputs,
references, and launchers do not drift.

## Inputs

Primary paper intake:

```text
X:\paper-proof-grader\DROP_PAPERS_HERE
```

Claim-audit inputs produced by the paper grader:

```text
X:\paper-proof-grader\OUTPUT\*.claim-audit.csv
```

Canonical chain-node registry:

```text
X:\paper-proof-grader\REFERENCE\canonical_chain_nodes.psv
```

Proof-explorer supplemental sequence pages:

```text
X:\paper-proof-grader\REFERENCE\axiom_sequence_sources
```

## Outputs

Each run creates one timestamped run folder:

```text
X:\paper-proof-grader\OUTPUT\station-runs\axiom-7q-YYYYMMDD_HHMMSS
```

Latest-run pointer files:

```text
X:\knowledge-refinery\10_STATIONS\12_axiom_promotion\LATEST_OUTPUT_POINTER.txt
X:\paper-proof-grader\OUTPUT\station-runs\LATEST_AXIOM_7Q_RUN.txt
```

The workflow launcher updates both pointers automatically.

Inside that folder:

- `index.html` - batch front door
- `axiom-7q-review.xlsx` - main review workbook
- `batch-index.json` - machine index
- `batch-index.md` - human handoff index
- `{paper_id}\axiom-7q-stations.html` - per-paper HTML
- `{paper_id}\axiom-7q-stations.json` - per-paper machine payload
- `{paper_id}\axiom-7q-stations.md` - per-paper markdown review

The workbook is the review surface:

- `Batch Summary`
- `Claim Review`
- `Chain Nodes`
- `Tag Graph Review`
- `Graph Edges`

## Launchers

Deterministic run, no API calls:

```text
X:\knowledge-refinery\10_STATIONS\12_axiom_promotion\RUN_AXIOM_7Q_STATION.bat
```

Bounded O3 sample:

```text
X:\knowledge-refinery\10_STATIONS\12_axiom_promotion\RUN_AXIOM_7Q_O3_SAMPLE.bat
```

Direct advanced run:

```text
X:\knowledge-refinery\10_STATIONS\12_axiom_promotion\RUN_AXIOM_7Q_STATION.bat --openai --openai-model o3 --openai-limit 1
```

## Workflow Placement

Recommended station order:

1. `05_claim_extractor`
2. `06_7qs_forward`
3. `07_7qs_reverse`
4. `08_7qs_evidence`
5. `12_axiom_promotion` - this station
6. `13_knowledge_graph`

This station should not promote nodes directly to canon. It prepares reviewable
outputs. Accepted rows in `Tag Graph Review` and `Graph Edges` can later feed
the knowledge graph station.

## Current Boundary

The ontology is now canonical, but matching is still lexical. Broad families
such as Truth, Information, Grace, and Moral Realism can over-match. The next
upgrade is family-aware ranking:

- keep deterministic candidate generation
- ask O3 to rank or reject candidates for high-value claims
- write model suggestions as `draft`
- require human/accepted status before graph ingestion
