# Seven Questions Station

**Purpose:** Run the Seven Questions against a packet source and produce Foundations, Reversals, and Evidence outputs.
**Status:** candidate station
**Last updated:** 2026-05-16

This station is the reusable 7QS capability. It is not a workflow by itself.

## Public Language

- The Seven Questions
- Foundations
- Reversals
- Evidence

## Internal Language

- `7Q-F`
- `7Q-R`
- `7Q-E`
- `Q1-F / Q1-R / Q1-E` style addressing

## Contract

Input:

```text
packet/WORKING/source.md
```

Output:

```text
packet/WORKING/station-outputs/seven-questions/<source>_7QS_<date>.json
packet/WORKING/station-outputs/seven-questions/<source>_7QS_<date>.md
packet/MACHINE/station-log.json
```

The current `station.py` can also be run directly on a markdown file:

```bash
python station.py --paper "path/to/source.md" --output "path/to/_7QS_ANALYSIS"
```

## Verification Standard

The station is verified only when:

- Python files compile.
- It can run on a sample markdown input.
- JSON output includes `foundations_7q`, `reversals_7q`, `evidence_7q`, and legacy-compatible `forward_7q` / `reverse_7q`.
- It does not claim to prove the framework true.
- It separates structural isomorphism from analogy.
