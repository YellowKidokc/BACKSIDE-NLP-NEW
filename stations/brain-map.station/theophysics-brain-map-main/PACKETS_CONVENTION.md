# Packet Convention

**What this is:** The rule for portable work units that move through stations.
**Owner:** shared
**Status:** live proposal
**Last updated:** 2026-05-16

A packet is the front-facing unit of work. It may contain public material, working remnants, and machine metadata, but those layers stay separated.

## Core Rule

One packet per meaningful object or run, not one folder per remnant.

Good packet subjects:

- one paper
- one article
- one proof snapshot
- one claim/theorem
- one workflow run
- one export family

Avoid:

- one folder for every scratch artifact
- one giant `remnants` dump
- public pages mixed with raw model traces

## Packet Shape

```text
packets/
  2026/
    05/
      seven-questions-snapshot/
        PUBLIC/
        WORKING/
        MACHINE/
        ARCHIVE/
```

## Layers

```text
PUBLIC/
  index.html
  executive-summary.html
  translation.html
  seven-questions.html
  axiom-candidates.html

WORKING/
  source.md
  drafts/
  notes/
  station-outputs/

MACHINE/
  metadata.json
  provenance.json
  station-log.json
  tags.json
  embeddings.todo.json

ARCHIVE/
  superseded/
  raw/
  failed-runs/
```

## Public Addressing

The packet can be public-addressable, but only the `PUBLIC/` layer is consumer-facing.

The `WORKING/` and `MACHINE/` layers support the public artifact. They should not be rendered as the first page for a reader.

## Station Rule

Stations read a packet, write back into the packet, and log what they did.

```text
station = reusable capability
workflow = ordered use of stations
packet = thing being transformed
```

Every station should avoid side effects outside the packet unless its `station.json` explicitly declares them.

## Metadata Contract

Every packet should have:

```text
MACHINE/metadata.json
MACHINE/provenance.json
MACHINE/station-log.json
```

Metadata is what lets NLPs extract tags, summaries, station status, and routing decisions without moving or flattening every remnant.

## Axiom Boundary

The Seven Questions station can surface load-bearing claims. The axiom-candidates station can score and structure those claims.

It must not silently promote them into final axioms.

```text
Question -> Claim -> Dependency -> Reversal -> Evidence -> Axiom Candidate -> Promoted Axiom
```

A promoted axiom requires review after denial, reversal, dependency, evidence, and kill-condition testing.
