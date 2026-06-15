# mda-publication.station

Station identity for the MDA publication workflow.

## Rule

All workflow logic lives here. `X:\Backside\MDA` is an output/archive landing zone, not the process home.

## Current Scripts

- `scripts\ROUTE_MDA_OUTPUTS.ps1` routes Math Translation Layer and NLP outputs into the MDA output/archive folders.
- `scripts\REGEN_SCORECARDS.py` regenerates NLP HTML scorecards from snapshots.
- `scripts\check_scanner.py` and `scripts\test_gen.py` are utility/debug scripts moved out of the old output logs folder.

## Correct Workflow Direction

The production sequence must be vector-first:

`lossless -> sbert-embedder -> hdbscan-cluster -> categorization-router -> paper graders -> proof/math/7Q -> publication build -> Obsidian export`

This station owns MDA publication routing and output dispatch. It should consume upstream station outputs instead of rediscovering source folders ad hoc.

## Output Contract

Workflow run artifacts should move toward:

`\\dlowenas\brain\Backside\station_outputs\<station_id>\mda-publication\<run_id>\`

Legacy MDA outputs currently remain at:

`X:\Backside\MDA`

