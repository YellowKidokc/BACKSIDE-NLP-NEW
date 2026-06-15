# GTQ-03 Pipeline Gap Analysis - 2026-05-20

Gold/reference file:

```text
Backside/lossless_context_pipeline/calibration/GTQ_03_GOLD_LOSSLESS_CLASSIFICATION_2026-05-20.md
```

Deterministic pilot source:

```text
X:\EXPORTS\lossless-context\gtq-03-pilot\20260520-133246\gtq-03-first-quantum-state.canonical.md
```

## Alignment

After the `E` scoring patch, the deterministic pipeline and gold artifact agree on the 10-variable vector:

```text
G3M3E0S0T3K3R3Q0F3C3
```

This is the most important calibration result. It means the deterministic pipeline can now orient the artifact correctly before any LLM fill pass.

## Remaining Metadata Difference

Gold address:

```text
THEOPHYSICS/GTQ_03_FIRST_QUANTUM_STATE/P/PUBLIC/T/R0
```

Current deterministic address from converted Markdown:

```text
THEOPHYSICS/GTQ-03-FIRST-QUANTUM-STATE-CANONICAL/W/AI_RESEARCH/R/R1
```

Reason: the converted Markdown does not yet carry public HTML metadata such as formal canon / public / transformative / published state. The converter/pipeline needs a metadata extraction pass from the original HTML:

- `<meta name="paper-slug" content="GTQ-03">`
- title
- article identity labels
- formal/public state
- source collection / series

## Gold Beats Deterministic Extraction

The gold artifact is much better at:

- selecting only five major claims instead of many raw claim candidates
- preserving the article's actual argument spine
- distinguishing evidence source from evidence bridge
- stating real kill conditions
- labeling the Eden wavefunction as symbolic/interpreted
- grading Academic Readiness conservatively
- identifying rhetoric that should be softened
- tying the article to upstream/downstream GTQ dependencies

## Deterministic Pipeline Still Useful

The deterministic pipeline is still valuable because it supplies:

- stable IDs
- content hashes
- block inventory
- rough claim/equation/domain extraction
- JSON/HTML snapshot
- vector-ready object shell
- reproducible batch behavior

It should not be asked to produce final buried claims, evidence bridges, implicit kills, or reviewer repairs without an LLM fill pass.

## Next Required Stations

1. HTML metadata extractor
2. claim candidate cleaner
3. major-claim selector
4. equation semantics cleaner
5. evidence bridge LLM fill
6. kill architecture LLM fill
7. rhetoric/overstatement rewrite suggester
8. score calibration ledger
9. cross-dependency linker
10. vector-ready JSONL exporter

## Calibration Rule Added

Entropy/disorder `E=3` must not be triggered by a document discussing entropy, collapse, fall, corruption, or disorder.

`E=3` is reserved for artifact-level disorder:

```text
corrupted
fragmented
redacted
illegible
damaged
contradictory artifact
structural noise
ambiguous artifact
```

GTQ-03 is an orderly artifact about collapse and entropy, so `E=0`.
