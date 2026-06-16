# Snapshot Field Gap Report

Date: 2026-05-24

## Current Break

No live `.paper-snapshot.json` artifact was found in the first lane scan under:

- `X:\Backside\workflows\knowledge-refinery.workflow\exports`
- `X:\Backside\workflows\knowledge-refinery.workflow\root-leftovers\snapshot`
- `X:\Backside\workflows\knowledge-refinery.workflow\13_knowledge_graph`

That is the blocking dependency for a real export run.

## Closest Available Artifact

The nearest machine-readable file found was:

- `X:\Backside\workflows\knowledge-refinery.workflow\exports\seven-questions-snapshot_20260516-214743\metadata.json`

It is an export package manifest, not a paper snapshot.

## Contract Fields Missing From `metadata.json`

Relative to `PAPER_SNAPSHOT_CONTRACT_20260524.md`, the available manifest lacks the sections the exporter actually needs:

- Identity fields for one paper object: `snapshot_id`, `source_id`, `source_path`, `title`
- `claims`
- `tags`
- `seven_qs`
- `method_passes`
- `epistemic_status`
- `derivations`
- `station_marks`
- `math_translation_layer.translated_spans`

Without those sections, deterministic graph export would have to invent claim, evidence, and derivation structure, which would violate the contract.

## What Was Shipped Anyway

To keep Lane C moving without semantic invention, a contract-shaped fixture was added at:

- `X:\Backside\workflows\knowledge-refinery.workflow\13_knowledge_graph\sample.paper-snapshot.json`

That fixture is complete enough to verify exporter behavior and produce sample outputs, but it is not a substitute for a real station-generated snapshot.
