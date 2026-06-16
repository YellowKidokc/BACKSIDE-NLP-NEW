# WIRING SPEC SCHEMA
## For Section 07 Automator (`wire_section07.py`)

Each station that has real processing scripts needs a `wiring_spec.json`
in its station folder. The automator reads these and patches pipeline.py
Section 07 automatically.

## Schema

```json
{
  "description": "One-line description of what this station does",

  "imports": [
    "import numpy as np",
    "from pathlib import Path"
  ],

  "init": {
    "var_name": "client",
    "code": [
      "from my_runner import MyClient",
      "_client = MyClient(base_url=cfg['some_url'])",
      "log.info('Client ready: %s', _client.info)"
    ]
  },

  "process_code": [
    "client = _get_client(cfg, log)",
    "output = client.process(text)",
    "",
    "result['data'] = {",
    "    'action': STATION_DESC,",
    "    'worker': nlp_info.get('nlp_id', 'NONE'),",
    "    'input_type': path.suffix.lower(),",
    "    'my_output_key': output,",
    "}",
    "log.info('Processed %s: result_size=%d', path.name, len(str(output)))"
  ]
}
```

## Field Details

### `description` (string, required)
One-line description. Gets inserted as a docstring and comment.

### `imports` (list of strings, optional)
Module-level imports needed by this station's processing.
These go at the top of Section 07.

### `init` (object, optional)
For stations that need a client, model, or connection created once per run.
Omit this if the station just calls a function directly (no persistent state).

- `var_name`: Name for the lazy-init variable (e.g. "client", "model", "db")
- `code`: Lines of Python inside the init function. The function provides
  `cfg` (config dict) and `log` (logger). Assign to `_{var_name}`.

### `process_code` (list of strings, required)
Lines of Python inside `process_one()`, after reading the file text.
Available variables:
- `path` — Path to the input file
- `text` — File contents as string (already read)
- `nlp_info` — Dict with nlp_id and nlp_path from Section 06
- `cfg` — Full config dict
- `log` — Logger
- `result` — The result dict (set result["data"] with your output)
- `STATION_ID`, `STATION_NAME`, `STATION_DESC` — Station constants

If you used `init`, call `_get_{var_name}(cfg, log)` to get the instance.

## Important Rules

1. Each line in `process_code` gets indented 8 spaces (inside try block)
2. Each line in `init.code` gets indented 4 spaces (inside function)
3. Don't include the try/except — the automator wraps process_code in one
4. The `_read_text()` helper is auto-generated — you get `text` for free
5. Set `result["data"]` with your output dict
6. For errors, just raise — the automator catches and logs

## Example: sbert-embedder.station

Runner: `sbert_runner.py` — has an `InfinityClient` class for HTTP embeddings.

```json
{
  "description": "Embed text via Infinity SBERT service, return 384-dim vector",
  "imports": ["import numpy as np"],
  "init": {
    "var_name": "client",
    "code": [
      "from sbert_runner import InfinityClient",
      "ms = cfg.get('model_settings', {})",
      "_client = InfinityClient(",
      "    base_url=cfg['infinity_url'],",
      "    model=ms.get('model_name', 'sentence-transformers/all-MiniLM-L6-v2'),",
      "    http_batch_size=int(ms.get('http_batch_size', 32)),",
      ")",
      "log.info('InfinityClient ready: model=%s dim=%d', _client.model, _client.dim)"
    ]
  },
  "process_code": [
    "client = _get_client(cfg, log)",
    "vec = client.embed([text], normalize=True)[0]",
    "",
    "result['data'] = {",
    "    'action': STATION_DESC,",
    "    'worker': nlp_info.get('nlp_id', 'NONE'),",
    "    'input_type': path.suffix.lower(),",
    "    'embedding_dim': int(vec.shape[0]),",
    "    'embedding_model': client.model,",
    "    'text_length_chars': len(text),",
    "    'embedding': vec.tolist(),",
    "}",
    "log.info('Embedded %s: %d chars -> %d-dim vector', path.name, len(text), vec.shape[0])"
  ]
}
```

## Stations WITH Runner Scripts (need specs generated)

| Station | Runner(s) | Notes |
|---------|-----------|-------|
| 7q-classifier | seven_q_core.py, seven_q_runner_refined.py | 7Q classification engine |
| 7q-engine | destroy.py, html_report.py, id_system.py +5 | Full 7Q processing suite |
| ai-portal-generator | generator.py | Portal page generator |
| apologetic-pipeline | apologetics_pipeline.py | Apologetics processing |
| claim-extractor | extract.py, claims_7q_pass.py, export_excel.py | Claim extraction |
| deberta-runner | deberta_runner.py | DeBERTa NLI classification |
| fruits-spirit-canon | fruits_coherence_engine.py, run_fruits_engine.py | Fruits formalization |
| hdbscan-cluster | cluster_runner.py | HDBSCAN clustering |
| image-processor | image_classifier.py | Image classification |
| master-equation-canon | station.py | Master equation canonicalization |
| mda-citation-spine | claim_inventory.py | Citation spine builder |
| operators-canon | station.py | Operators canonicalization |
| paper-intelligence-suite | docker_entrypoint.py, fruit_dynamics.py | Full paper analysis |
| paper-proof-grader | expanded_report.py, formal_verification.py +2 | Paper grading |
| postgres-sync | db_utils.py | Database sync utility |
| trinity-canon | station.py | Trinity canonicalization |
| vault-rater-tsr100 | lowe_scorer.py | Vault rating/scoring |
| whisper-transcribe | whisper_runner.py | Audio transcription |
| youtube-fetch | transcript_puller.py, youtube_scraper.py | YouTube data fetch |

## Stations WITHOUT Runner Scripts (need logic written)

classify-documents, coherence-discoherence, contradiction-deep,
contradiction-detector, fact-verifier, file-intelligence, fis,
graph-linker, harvest-links, html-article, lightfm-recommender,
link-pull, link-research, llm-runner, math-layer,
math-translation-layer, math-verify, mda-publication,
metadata-extractor, obsidian-export, open-brain-map,
paper-grader-nlp, paper-recommender, paper-review, paperqa2,
preference-engine, preference-implicit, readability-rewriter,
reading-level-glossary, recbole-recommender, section-splitter,
series-flow-auditor, session-handoff-combined, session-handoff-drop,
summarizer, theophysics-engine, timeline-verifier,
transcribe-and-classify, youtube-qa, youtube-scrape
