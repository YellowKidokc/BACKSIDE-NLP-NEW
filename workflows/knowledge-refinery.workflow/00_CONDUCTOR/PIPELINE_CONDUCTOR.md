# Knowledge-Refinery Conductor (One Map, Strict Gates)

This is the routing clarity layer: **drop -> stations -> artifacts -> publish targets**.

Design:
- One conductor
- 13 model roles (M01..M13)
- Many stations (packet folders)
- Strict gates (REVIEW vs ERROR vs ARCHIVE vs CANON)
- 7QS is a controlled sequence, not one blob

## Canonical folder layout (front door)

```
X:\knowledge-refinery\
  00_DROP\
  01_INTAKE\
  02_WORKING\
  03_REVIEW\
  04_CANON\
  05_PUBLICATION\
  06_AI_PORTAL\
  10_STATIONS\
  20_REGISTRIES\
  30_PROMPTS\
  40_CONFIG\
  50_LOGS\
  90_ARCHIVE\
  99_ERROR\
```

## Station packets

Every station exists as:
- `X:\knowledge-refinery\10_STATIONS\<nn_station_id>\{INPUT,OUTPUT,REVIEW,ARCHIVE,ERROR,CONFIG,PREFS,PROMPTS,SCRIPTS,LOGS}`

The conductor’s enforcement rule:
- Outputs must use canonical filenames so downstream wiring is declarative.

## End-to-end flow (DAG)

```mermaid
flowchart TD

DROP["00_DROP<br/>papers / HTML / chats / audio / notes"]
INTAKE["01_INTAKE<br/>normalized source packets"]
WORK["02_WORKING<br/>active refinery"]
REVIEW["03_REVIEW<br/>human + AI checks"]
CANON["04_CANON<br/>approved knowledge"]
PUB["05_PUBLICATION<br/>website / Substack / Zenodo"]
AI["06_AI_PORTAL<br/>vector + JSON packages"]
ARCHIVE["90_ARCHIVE<br/>duplicates / rejected / old"]
ERROR["99_ERROR<br/>failed runs"]

DROP --> ROUTER

ROUTER["M01 Route Classifier<br/>decides file type + workflow"]
ROUTER --> INTAKE

INTAKE --> DEDUP["M02 Dedup / Canon Resolver<br/>same article? older version?"]
DEDUP -->|duplicate| ARCHIVE
DEDUP -->|unique| CLEAN["M03 Source Cleaner<br/>HTML->MD / STT cleanup / normalize"]

CLEAN --> LOSSLESS["M04 Lossless Summary<br/>preserve claims / equations / evidence"]
LOSSLESS --> CLAIMS["M05 Claim Extractor<br/>claim ledger + durable IDs"]

CLAIMS --> SEVENQ["M06 7QS Engine<br/>Forward Questions"]
SEVENQ --> REVERSE["M07 Reverse 7QS<br/>attack / weakest link / kill tests"]
REVERSE --> EVIDENCE["M08 Evidence 7QS<br/>what supports this? what is missing?"]

EVIDENCE --> SCIENCE["M09 Science Checker<br/>physics / math / overclaim audit"]
SCIENCE --> MATH["M10 Math Translator + Contradiction Checker<br/>equation meaning + variable drift"]

MATH --> LEAN["M11 Lean / Formalizer<br/>theorem skeletons / axiom templates"]
LEAN --> PROMOTE["M12 Axiom Promotion Gate<br/>candidate -> axiom?"]

PROMOTE -->|fails| REVIEW
PROMOTE -->|passes| GRAPH

GRAPH["M13 Knowledge Graph Builder<br/>nodes + edges + collapse map"]

GRAPH --> REGISTRY["Claim / Axiom Registry<br/>claims.yml / axioms.yml / graph.json"]
REGISTRY --> CANON

REGISTRY --> PACKET["AI Portal Packet<br/>paper.ai.json<br/>claims.json<br/>scores.json<br/>vector.txt"]
PACKET --> AI

CANON --> SIMPLE["Explain It Simple<br/>reader-facing teaching"]
CANON --> EXEC["Executive Summary<br/>what it says + why it matters"]
CANON --> PROOF["Proof Explorer Builder<br/>HTML proof page"]
CANON --> SEO["Publication / SEO Gate<br/>title / slug / audience / release tier"]

SIMPLE --> PUBREADY["Publication Bundle"]
EXEC --> PUBREADY
PROOF --> PUBREADY
SEO --> PUBREADY

PUBREADY -->|website| PUB
PUBREADY -->|Substack| PUB
PUBREADY -->|Zenodo| PUB
PUBREADY -->|hold| REVIEW

REVIEW --> FIX["Revision Packet<br/>specific fixes"]
FIX --> WORK
WORK --> SEVENQ

ROUTER -->|unknown| ERROR
CLEAN -->|parse fail| ERROR
LOSSLESS -->|structure lost| ERROR
SCIENCE -->|major contradiction| REVIEW
LEAN -->|formalization fail| REVIEW
SEO -->|not ready| REVIEW
```

## 13 model roles (contract)

```mermaid
flowchart LR

M01["M01 Router<br/>small fast model"]
M02["M02 Dedup<br/>embedding + reranker"]
M03["M03 Cleaner<br/>code/text model"]
M04["M04 Lossless Summarizer<br/>long-context model"]
M05["M05 Claim Extractor<br/>structured JSON model"]
M06["M06 7QS Forward<br/>reasoning model"]
M07["M07 7QS Reverse<br/>adversarial model"]
M08["M08 Evidence Finder<br/>citation/literature model"]
M09["M09 Science Checker<br/>physics/math model"]
M10["M10 Math Contradiction<br/>math/code model"]
M11["M11 Lean Formalizer<br/>Lean/proof model"]
M12["M12 Axiom Promoter<br/>highest reasoning model"]
M13["M13 Knowledge Graph<br/>graph extraction model"]

M01 --> M02 --> M03 --> M04 --> M05 --> M06 --> M07 --> M08 --> M09 --> M10 --> M11 --> M12 --> M13
```

## 7QS is a sequence (core loop)

```mermaid
flowchart TD
A["Claim"] --> B["7QS Forward<br/>What is it?"]
B --> C["7QS Reverse<br/>What breaks it?"]
C --> D["7QS Evidence<br/>What supports it?"]
D --> E["Science Check<br/>Is it physically sane?"]
E --> F["Math Check<br/>Any equation drift?"]
F --> G["Lean Formalization<br/>Can it be scaffolded?"]
G --> H["Axiom Promotion<br/>Does it become load-bearing?"]
```

## Next wiring step (minimal, high leverage)

1) Require every station to emit canonical filenames in its `OUTPUT/`.
2) Add a validator that fails runs when required artifacts are missing (routes to `99_ERROR` with reasons).
3) Point all station model paths to the canonical model base (`X:\knowledge-refinery\_MODELS\...`).

