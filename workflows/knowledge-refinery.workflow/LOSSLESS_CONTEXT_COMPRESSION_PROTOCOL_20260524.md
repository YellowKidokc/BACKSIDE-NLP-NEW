# Lossless Context Compression + Semantic Addressing Protocol

Status: build spec v1.0  
Purpose: universal file/document mapping layer for snapshots, classifiers, graph export, vector search, contradiction detection, and repair queues.

## Core Principle

Score the artifact, not the topic.

A paper about entropy can be structurally clean, so `E=0`. A legal contract about love can be primarily binding, not emotional. A checklist about safety can be procedural, not experiential. The system classifies what the document is and how it functions, not only what it talks about.

## Address Layer

Permanent identity format:

```text
D/N/V/A/U/R :: VECTOR :: HASH
```

Where:

```text
D = broad domain
N = named entity / subject / artifact
V = lifecycle state
A = audience / access
U = use / direction
R = filing risk
```

The address classifies the article. The snapshot reconstructs the article. The grades audit the article. The embeddings find similar articles. The ledger explains every score.

## Semantic Vector

Use ten artifact variables, scored only `0` or `3`.

```text
G = Authority/Ground
M = Mechanism/Action
E = Entropy/Disorder
S = Identity/Self
T = Time/Sequence
K = Knowledge/Info
R_sem = Relation/Bond
Q = Experience/Felt
F = Faith/Trust
C = Coherence/Unity
```

Rules:

```text
0 = absent / not dominant
3 = dominant artifact signal
```

Confidence is separate:

```text
orientation = 0 or 3, determines address
confidence = 0.00-1.00, determines review priority
```

Never let confidence change the canonical address.

## Locked Tie-Break

When variables tie, rank with:

```text
E -> C -> G -> K -> M -> T -> R -> F -> S -> Q
```

Pair strongest with weakest inward:

```text
[#1.#10] [#2.#9] [#3.#8] [#4.#7] [#5.#6]
```

Pair 1 is an anchor, not the whole meaning. The full vector and full hash preserve semantic density.

## Critical Edge Rules

`C=3` only when synthesis, integration, reconciliation, or unification is the artifact's explicit dominant function. A clean document is not automatically `C=3`.

`E=3` only when the artifact itself is noisy, fragmented, contradictory, corrupted, redacted, illegible, or unstable. A document about disorder is not automatically `E=3`.

`R_sem` means relation/bond in the vector. `R_file` means filing risk in the address. Namespacing is mandatory.

Grades are audit metadata, not identity. Do not put grades into permanent filenames.

## Required Snapshot Additions

The paper snapshot should gain:

```json
{
  "semantic_address": {
    "address": "D/N/V/A/U/R :: VECTOR :: HASH",
    "filename_safe": "D__N__V__A__U__R__VECTOR__HASH",
    "domain": "THEOPHYSICS",
    "named_entity": "GTQ-17",
    "version_state": "W",
    "audience": "PUBLIC",
    "use_direction": "I",
    "risk": "R1"
  },
  "semantic_vector": {
    "vector": "G3M3E0S0T3K3R3Q0F3C3",
    "scores": {"G": 3, "M": 3, "E": 0, "S": 0, "T": 3, "K": 3, "R": 3, "Q": 0, "F": 3, "C": 3},
    "confidence": {"G": 0.83, "M": 0.78}
  },
  "semantic_hash": {
    "pairs": ["C.Q", "G.S", "K.E", "M.F", "T.R"],
    "hash": "CQ-GS-KE-MF-TR"
  },
  "classifier_tags": {
    "domain": [],
    "subject": [],
    "artifact_function": [],
    "canon_folder_route": null,
    "route_confidence": 0.0
  }
}
```

## Grading Boundaries

Never collapse the four scores:

```text
Academic_Readiness
Framework_Coherence
Public_Communication
Risk
```

Every score must have ledger events:

```text
metric
max_points
positive_points
deductions
evidence_quote
section
fix_to_improve
```

Bad grades create repair queues:

```text
repair_item
fix_to_improve
priority
affected_claims
affected_downstream_papers
```

## System Placement

```text
Obsidian = human surface
Postgres = audit memory
Python/NLP = extraction/classification
LLM = reconstruction/review
HTML = review surface
Repair queue = quality-control layer
```

Do not make Obsidian the audit database. Store IDs, hashes, runs, snapshots, ledgers, and repairs in Postgres.

## Object Identity

At vault scale, the unit is the claim/block, not the paper.

Required IDs:

```text
vault_id
doc_id
note_version
content_hash
block_id
claim_id
equation_id
evidence_id
run_id
audit_snapshot_id
repair_item_id
prompt_version
schema_version
model_version
```

Snapshots append. They do not overwrite.

## Build Order

1. Deterministic semantic-address engine for Markdown/HTML/text.
2. Feed `semantic_address`, `semantic_vector`, `semantic_hash`, and `classifier_tags` into `.paper-snapshot.json`.
3. Feed snapshot tags and canon route into graph exporter.
4. Store addresses, block IDs, claims, equations, score events, and repair items in Postgres.
5. Add optional NLP/LLM passes for buried claims, evidence bridges, implicit kills, hostile review, and repair reasoning.

## Final Rule

Lossless means reconstruction seed, not magic compression. Future AI must be able to reconstruct thesis, claims, definitions, decisions, rationale, entities, mechanisms, open threads, proof boundaries, and repair path.
