# 06_IMAGES — Troubleshooting

## EasyOCR first-run download

EasyOCR downloads detection + recognition models (~75 MB) into `_MODELS\easyocr\`. First run takes a minute; subsequent runs are fast.

## CLIP first-run download

`openai/clip-vit-base-patch32` is ~340 MB and lands in `_MODELS\hub\`. To use a different size:

| Model | Size | Quality |
|---|---|---|
| `openai/clip-vit-base-patch32` | 340 MB | default — fast |
| `openai/clip-vit-base-patch16` | 340 MB | slightly slower, sharper |
| `openai/clip-vit-large-patch14` | 1.7 GB | best |

Edit `clip_settings.model_name` in `config.json`.

## Self-test fails: `'HELLO' not found in OCR output`

Two common causes:
1. Default font on this Windows install renders too thin for OCR. The runner falls back to `arial.ttf` then PIL default — if neither produces readable output, install/repair Windows fonts.
2. The recognition model is downloading slowly and the test moved on. Re-run after the model has fully cached.

## OCR returns `[]` on real images

Real photos with text often need:
- `min_confidence` lower (try 0.1 in `config.json`) — strict default filters too aggressively for stylized fonts.
- Add languages — `["en"]` only does English. Add `"de"`, `"fr"` etc. as needed (each language pulls a separate ~50 MB recognition model).

## CLIP confidence scores all near uniform

The labels are too similar in CLIP's embedding space. Make labels more distinctive (concrete nouns/scenes beat abstract concepts). Or change `prompt_template` to `"this is a {}"` or `"a picture showing {}"` and re-run.

## CUDA out of memory

CLIP-base is small enough for any modern GPU. If you're hitting OOM, you're sharing the GPU with another model. Set `clip_settings.device = "cpu"`.

## Want to write results to Postgres instead of JSON sidecars

Not implemented yet — extend `run()` to call `db_utils.Database` and update an `images` table. The pattern is the same as 02_SBERT and 03_DEBERTA.
