# Model: science_embeddings_specter2

Purpose: science-domain embeddings for dedup, similarity, clustering, and retrieval over papers/articles.

Used by stations:
- `10_STATIONS/02_dedup`
- `10_STATIONS/08_7qs_evidence` (retrieval)
- `10_STATIONS/13_knowledge_graph` (similarity edges)

Good at:
- scientific paper similarity / nearest-neighbor retrieval

Do not use for:
- claim verification (NLI)
- routing decisions

How to run:
- `scripts\\01_healthcheck.bat`
- `scripts\\02_smoke_test.bat`

Last known status:
- downloaded snapshot present under `_MODELS/HF_SNAPSHOTS/science_embeddings_specter2`

