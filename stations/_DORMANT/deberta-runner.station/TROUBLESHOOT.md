# 03_DEBERTA — Troubleshooting

## Install: torch wheel takes forever

CPU-only torch is ~250 MB; the GPU build is ~2 GB. If you don't have CUDA hardware, you can keep the CPU build and edit `config.json` → `model_settings.device` = `"cpu"`. To force CPU torch on install:

```
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

## First run downloads ~1.6 GB

That's the DeBERTa-v3-large weights. They land in `_MODELS\hub\`. Subsequent runs start in seconds.

## CUDA out of memory

DeBERTa-v3-large is heavy. Drop `model_settings.batch_size` in `config.json` from 50 → 10 (or further). Or fall back to a smaller model:

| Model | Size | Quality |
|---|---|---|
| `MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli` | 1.6 GB | best (default) |
| `cross-encoder/nli-deberta-v3-large` | 1.6 GB | strong |
| `MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli` | 700 MB | medium |
| `valhalla/distilbart-mnli-12-3` | 250 MB | fast/lightweight |
| `facebook/bart-large-mnli` | 1.6 GB | classic baseline |

## Self-test fails — wrong top label

The model is fine; the test sentence has multiple plausible labels. Inspect the printed scores. If the runner-up was very close, that's not a real failure — but the assertion is strict. Re-run; if persistently wrong, the model is loading a wrong checkpoint (verify the cache hasn't been corrupted).

## A row produces a UTF-8 / token error

Set `model_settings.max_text_chars` lower. The runner already truncates to 2000 chars by default — descriptions occasionally exceed model context after concatenation.

## Resume after interrupt

Just re-run. The runner only pulls rows where `deberta_label IS NULL`, so completed rows are skipped automatically.

## All rows getting the same label

Two failure modes:
1. The text columns are mostly empty or very short — model defaults to a generic label. Verify `text_cols` in `config.json` and inspect a sample row.
2. The labels in `config.labels` aren't actually distinct in NLI space. Reduce overlap or rephrase them.

## How to re-classify everything

```
UPDATE youtube_apologetics SET deberta_label = NULL, deberta_confidence = NULL;
```

then re-run.
