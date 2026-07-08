# Packet Bridge - First Implementation

## What is now implemented

This `nlp_api` directory now contains a first working bridge layer:

- `packet_bridge.py`
- new FastAPI endpoints in `main.py`
- `test_packet_bridge.py`

## New endpoints

- `POST /packet/build`
- `POST /packet/bridge`
- `POST /packet/integrity`
- `POST /packet/schema`
- `POST /packet/project`
- `POST /packet/from-disk`

## What they do

### `/packet/build`

Takes source metadata plus station outputs and returns a bundle with:

- `bridge_packet`
- `integrity_packet`
- `schema_packet`

### `/packet/bridge`

Builds only the normalized bridge packet.

### `/packet/integrity`

Builds the “paper on the paper” layer:

- claim ladder
- support state
- weakest joint
- structural verdict

### `/packet/schema`

Builds the `schema.org` + `pof:` namespace JSON-LD projection from station outputs.

### `/packet/project`

Projects an already-built bridge packet into JSON-LD.

### `/packet/from-disk`

Loads a real article from disk, normalizes the scattered artifact ecosystem into station-shaped inputs, and returns:

- `source`
- `station_outputs`
- `evidence_files`
- `bundle`

## What the current implementation expects

It is designed to be useful even with **partial station outputs**.

Best current inputs:

- station 02 - thesis / claims
- station 05 - evidence / overclaim
- station 06 - domain classification
- station 07 - coherence
- station 08 - writing / SEO
- station 09 - series continuity
- station 12 - high school layer
- station 13 - academic layer
- station 14 - equation / evidence map
- station 15 - media asset map
- station 16 - page integrity

Missing stations do not break the bundle. They simply leave parts sparse.

## Important first limitation

This is the first deterministic bridge layer, not the final intelligence layer.

It does **not** yet:

- run the stations itself
- infer everything from raw HTML alone
- build the graph layer
- distinguish every nuance of deferred support perfectly

What it does do is give the system a real center of gravity:

- one bridge packet
- one integrity packet
- one JSON-LD projection

It now also has a first real disk-backed article loader. The initial validated target is:

- `consciousness / consciousness-chi-field-action`

That real loader pulls from:

- summary JSON
- reading-layer JSON
- framework-alignment JSON
- knowledge-graph JSON
- domain-scan JSON
- station output JSON where available
- MTL equation catalog
- local media evidence

## Immediate next build targets

1. Expand disk-loader coverage beyond the first validated consciousness page
2. Teach support-state resolution more series awareness
3. Add graph-shaped exports
4. Add workbook-row export directly from the packet bundle
5. Harden station synthesis rules for inconsistent historical outputs
