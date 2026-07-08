# Backside Stations

**What this is:** Reusable single-purpose NLP/service steps called by workflows.
**Owner:** shared
**Status:** live map
**Last updated:** 2026-05-16

Stations are smaller than workflows. A workflow chains stations; a station does one job well.

The station is the reusable capability. Once a station is verified, any workflow can call it.

```text
station = reusable capability
workflow = ordered use of stations
packet = thing being transformed
```

7QS is the station grammar, not the station filesystem. Do not create seven physical folders inside every station unless that station truly produces separate Q artifacts. Put the 7Q mapping in `station.json`, prompts, reports, and tests.

Folder names end in `.station`:

```text
claim-extract.station
facts-extract.station
timeline-build.station
paper-proximity.station
contradiction-scan.station
math-clarify.station
```

## Planned station lanes

| Station | Uses |
|---|---|
| `facts-extract.station` | `facts.model` |
| `timeline-build.station` | `timeline.model` |
| `paper-proximity.station` | `paper-citation.model` |
| `claim-extract.station` | `mistral-7b-instruct.model` |
| `contradiction-scan.station` | `deberta-v3-large.model` |
| `math-clarify.station` | Math Translation Layer |
| `seven-questions.station` | refined 7QS runner; Foundations / Reversals / Evidence |
| `axiom-candidates.station` | refined 7QS JSON -> axiom candidates |
| `master-equation-canon.station` | Master Equation / formal layer canon index |
| `trinity-canon.station` | Trinity / Resurrection / Lean isomorphism canon index |
| `fruits-spirit-canon.station` | Fruits of Spirit canon/equation index |
| `operators-canon.station` | Grace / Justice / Mercy operator index |

Do not promote a station to workflow just because it is useful. Promote only when it has its own intake, run lifecycle, output contract, and dashboard tile.

## Composition rule

Do not copy station logic into workflow folders. Workflows reference stations by ID through `dependencies.json` and `configs/*.json`.

The canonical composition contract is:

```text
Backside\STATION_WORKFLOW_COMPOSITION.md
```

If a workflow needs different behavior, add parameters, create a new station ID, or add a workflow-specific prompt overlay. Do not create a private fork of `station.py` inside the workflow.

## Verification rule

A station is not real just because the folder exists. A station becomes reusable only when it has:

- input contract
- output contract
- no undeclared side effects outside the packet
- test example
- log/provenance behavior
- pass/fail criteria
