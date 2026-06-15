# Model Station Map

## Conversion First

Before interpretation, convert the source into a stable form:

| Input | Conversion |
|---|---|
| video | audio, transcript, markdown |
| audio | transcript, markdown |
| PDF | text, markdown, HTML |
| HTML | clean markdown, metadata |
| image | OCR/caption, metadata |
| chat | session handoff markdown and JSON |

## Model Stations

| Station | Local folder | Role |
|---|---|---|
| `math_verify` | `\\dlowenas\brain\models\math_verify` | Equation and arithmetic checks |
| `claim_extract` | `\\dlowenas\brain\models\claim_extract` | Extract discrete factual claims |
| `fact_verify` | `\\dlowenas\brain\models\fact_verify` | Supported / refuted / not enough info |
| `contradiction_detect` | `\\dlowenas\brain\models\contradiction_detect` | Entailment / contradiction / neutral |
| `timeline_verify` | `\\dlowenas\brain\models\timeline_verify` | Dates, ordering, chronology conflicts |
| `paper_review` | `\\dlowenas\brain\models\paper_review` | LLM rubric review via Ollama prompt |
| `7q_forward` | `X:\knowledge-refinery\13_SOURCE_SYSTEMS\7Q\engine` | Forward Q0-Q7 claim classification and scoring |
| `7q_reverse` | `X:\knowledge-refinery\13_SOURCE_SYSTEMS\7Q\engine` | Reverse destruction pass: try to kill the claim first |
| `treaties_snapshot` | `\\dlowenas\brain\knowledge-refinery\06_HTML_REPORTS\treaties-handoff` | Downstream handoff for Treaties/proof-explorer HTML snapshots |

## LLM Checkpoints

Use large language models at gates, not everywhere:

- after conversion: did we extract the right thing?
- after normalization: is the text clean enough?
- after understanding: what is the structure?
- after verification: what failed or needs review?
- before output: is the report useful and safe?
- before archive: what should future AI know?

## Routing Examples

| Route | Stages |
|---|---|
| Session handoff | intake, conversion, normalize, session-handoff-drop, memory |
| Paper grade | intake, conversion, normalize, claim_extract, paper-proof-grader, 7q_forward, 7q_reverse, axiom-map, Treaties handoff, HTML, archive |
| Full verification | intake, conversion, normalize, claim_extract, math_verify, fact_verify, contradiction_detect, timeline_verify, HTML, Obsidian, memory |
| Link capture | intake, link-pull-drop, conversion, summary, archive |
