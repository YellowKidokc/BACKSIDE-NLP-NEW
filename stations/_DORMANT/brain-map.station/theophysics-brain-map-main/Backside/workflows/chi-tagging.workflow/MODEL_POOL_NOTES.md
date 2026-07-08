# Model Pool Notes

The station split should not mean one full model stack per station.

## Recommended Runtime Shape

```text
station workers = many
heavy model pool = few
```

Run deterministic canon-index stations freely. They do not load large models.

For later NLP/LLM stations:

```text
sbert_minilm workers: 2-4
deberta_nli workers: 1-2
mistral_7b workers: 1 unless RAM/GPU proves otherwise
bart_summarizer workers: 1-2
```

## Rule

Do not let every station independently load Mistral/BART/DeBERTa. Put heavy models behind a shared queue or local service and let stations submit jobs.

## Why

Four station teams can run at once only if they share model processes. Otherwise the bottleneck becomes RAM, not reasoning.

