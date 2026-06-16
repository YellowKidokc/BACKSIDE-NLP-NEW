# 01_WHISPER — Troubleshooting

## Install fails: `Could not build wheels for ...`

You need Microsoft C++ Build Tools.
Install: https://visualstudio.microsoft.com/visual-cpp-build-tools/
Then re-run `INSTALL.bat`.

## `RuntimeError: Library cublas64_*.dll is not found`

`device=cuda` was selected but CUDA isn't installed properly. Either:

- Install the matching CUDA toolkit + cuDNN, or
- Edit `config.json` → `model_settings.device` = `"cpu"` and `compute_type` = `"int8"`.

`device=auto` should fall back automatically. If it doesn't, set explicitly.

## `Could not find ffmpeg`

faster-whisper needs ffmpeg to decode anything that isn't WAV.

```
winget install Gyan.FFmpeg
```

then restart the terminal so PATH refreshes.

## Model download is very slow / fails partway

Models live under `_MODELS\hub\` (set via `HF_HOME`). If a download corrupts:

```
rmdir /s /q D:\brain\_MODELS\hub\models--openai--whisper-large-v3
```

then re-run.

## Out of memory on CUDA

Drop to a smaller model by editing `config.json`:

- `large-v3` → ~10 GB VRAM
- `medium` → ~5 GB
- `small` → ~2 GB
- `base` → ~1 GB
- `tiny` → ~0.4 GB

Or set `compute_type` = `"int8_float16"` to roughly halve memory.

## `OSError: [WinError 1455] The paging file is too small`

CPU fallback with `large-v3` and `int8` can still need >8GB RAM. Either:

- Use `medium` instead, or
- Increase Windows pagefile (System → Advanced → Performance → Virtual memory).

## TEST.bat hangs on first run

It's downloading the `tiny` model (~75 MB). Subsequent runs start in seconds.

## Self-test says `text=''`

That's correct. The synthetic 440 Hz tone has no speech. The pass criterion is "no exception" — the empty result confirms the pipeline runs end-to-end.
