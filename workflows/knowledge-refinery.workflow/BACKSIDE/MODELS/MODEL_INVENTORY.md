# Model Inventory (Backside)

Canonical location for model assets now:
- `X:\knowledge-refinery\98_BACKSIDE\MODELS\_MODELS`

## Consolidated caches (copied earlier)

Under: `X:\knowledge-refinery\98_BACKSIDE\MODELS\_MODELS\OTHER_MODELS\...`
- `from_local_NLP_ACTIONS_models\nli\fever_anli_base`
- `from_local_NLP_ACTIONS_models\nli\strong_cross_encoder`
- `from_userprofile_hf_cache\hub\models--cross-encoder--nli-deberta-v3-base`
- `from_userprofile_hf_cache\hub\models--sentence-transformers--all-MiniLM-L6-v2`
- `from_userprofile_hf_cache\hub\models--Systran--faster-whisper-base`
- `from_knowledge_refinery_D_brain__MODELS\hub\models--sentence-transformers--all-MiniLM-L6-v2` (duplicate model id, different cache)

## Downloaded (explicit snapshot downloads)

Under: `X:\knowledge-refinery\98_BACKSIDE\MODELS\_MODELS\HF_SNAPSHOTS\...`
- `science_embeddings_specter2` (science / paper similarity embeddings)
- `timeline_temporal_information` (timeline/temporal signal model)
- `nli_deberta_v3_large` (stronger NLI model for â€œscience/overclaim auditâ€ lane)
- `mnli_fever_anli` (NLI for claim/contradiction checks)
- `roberta_large_nli` (NLI variant; good adversarial cross-check)

## /PROBE notes

- The â€œscience modelâ€ and â€œtimeline modelâ€ are now downloaded as explicit snapshots (not just HF cache stubs).
- Next wiring step is config: point all station roles that need embeddings/NLI/temporal tagging to this canonical base path.

## GitHub ecosystem downloads (supporting code/data)

These are NOT model weights, but they are valuable for the Science/Timeline lanes:
- `X:\knowledge-refinery\98_BACKSIDE\JUNKET\github_repos\scifact`
- `X:\knowledge-refinery\98_BACKSIDE\JUNKET\github_repos\multivers`
- `X:\knowledge-refinery\98_BACKSIDE\JUNKET\github_repos\awslabs_fever`
- `X:\knowledge-refinery\98_BACKSIDE\JUNKET\github_repos\ETEREX-REBEL`

