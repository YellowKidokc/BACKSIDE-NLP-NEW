# _MODELS — shared model weights

Models are downloaded here on first run by HuggingFace's cache (most tools point `HF_HOME` at this folder, so `transformers` and `sentence-transformers` will land here).

## Expected on-disk layout (created automatically)

```
_MODELS\
├── hub\                     # HF transformers + sentence-transformers cache
│   ├── models--openai--whisper-large-v3\
│   ├── models--sentence-transformers--all-MiniLM-L6-v2\
│   └── models--MoritzLaurer--DeBERTa-v3-large-mnli-fever-anli-ling-wanli\
├── easyocr\                 # EasyOCR character/recognition models
├── clip\                    # CLIP weights (06_IMAGES)
└── README.md                # this file
```

## Disk usage estimate

| Model | Size |
|---|---|
| whisper-large-v3 | ~3.0 GB |
| all-MiniLM-L6-v2 | ~90 MB |
| DeBERTa-v3-large-mnli | ~1.6 GB |
| EasyOCR (en) | ~75 MB |
| CLIP (ViT-B/32) | ~340 MB |
| **Total** | **~5.2 GB** |

## DO NOT manually edit this folder

- Tools manage their own subfolders.
- If a download corrupts, delete only the broken `models--*` directory and re-run the tool.
- To force re-download, delete `_MODELS\hub\models--<name>\`.

## Override location

Set `HF_HOME=D:\some\other\path` before running any tool to redirect cache.
