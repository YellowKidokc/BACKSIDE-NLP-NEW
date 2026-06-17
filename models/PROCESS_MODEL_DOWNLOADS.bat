@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM ================================================================
REM  Theophysics / Brain Model Downloader
REM  Downloads Hugging Face models into capability folders.
REM
REM  Default target matches your screenshot:
REM      X:\05_MODELS
REM
REM  Usage:
REM      PROCESS_MODEL_DOWNLOADS.bat
REM      PROCESS_MODEL_DOWNLOADS.bat D:\05_MODELS
REM
REM  Optional gated/private model access:
REM      set HF_TOKEN=hf_your_token_here
REM      PROCESS_MODEL_DOWNLOADS.bat
REM ================================================================

set "ROOT=%~1"
if "%ROOT%"=="" set "ROOT=X:\05_MODELS"

set "PYTHON_EXE=python"
set "VENV_DIR=%ROOT%\.venv_science_nlp"
set "STATE_DIR=%ROOT%\_state"
set "LOG_DIR=%ROOT%\_logs"
set "SCRIPT_PATH=%STATE_DIR%\download_models.py"

if not exist "%ROOT%" mkdir "%ROOT%"
if not exist "%STATE_DIR%" mkdir "%STATE_DIR%"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python was not found on PATH.
    echo Install Python 3.10+ and check "Add python.exe to PATH".
    pause
    exit /b 1
)

echo.
echo Target model root: %ROOT%
echo.

if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo Creating Python virtual environment...
    %PYTHON_EXE% -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo ERROR: Could not create virtual environment.
        pause
        exit /b 1
    )
)

call "%VENV_DIR%\Scripts\activate.bat"
python -m pip install --upgrade pip > "%LOG_DIR%\pip_upgrade.log" 2>&1
python -m pip install --upgrade huggingface_hub hf_transfer tqdm > "%LOG_DIR%\pip_install_hf.log" 2>&1
if errorlevel 1 (
    echo ERROR: Could not install huggingface_hub. See %LOG_DIR%\pip_install_hf.log
    pause
    exit /b 1
)

REM Faster downloads when supported by huggingface_hub.
set HF_HUB_ENABLE_HF_TRANSFER=1

if defined HF_TOKEN (
    echo HF_TOKEN detected. Gated/private models can use it if your account has access.
) else (
    echo No HF_TOKEN detected. Public models will download. Gated models may fail.
)

echo Writing downloader script...
> "%SCRIPT_PATH%" echo import os, json, time, traceback
>> "%SCRIPT_PATH%" echo from pathlib import Path
>> "%SCRIPT_PATH%" echo from huggingface_hub import snapshot_download
>> "%SCRIPT_PATH%" echo.
>> "%SCRIPT_PATH%" echo ROOT = Path(r"%ROOT%")
>> "%SCRIPT_PATH%" echo LOG_DIR = ROOT / "_logs"
>> "%SCRIPT_PATH%" echo STATE_DIR = ROOT / "_state"
>> "%SCRIPT_PATH%" echo LOG_DIR.mkdir(parents=True, exist_ok=True)
>> "%SCRIPT_PATH%" echo STATE_DIR.mkdir(parents=True, exist_ok=True)
>> "%SCRIPT_PATH%" echo token = os.environ.get("HF_TOKEN") or None
>> "%SCRIPT_PATH%" echo.
>> "%SCRIPT_PATH%" echo MODELS = [
>> "%SCRIPT_PATH%" echo     {"folder":"E02_embedder_quality__qwen3_0_6b", "repo":"Qwen/Qwen3-Embedding-0.6B", "job":"03_EMBEDDINGS_FAST / quality-light"},
>> "%SCRIPT_PATH%" echo     {"folder":"E04_embedder_quality__mxbai_large", "repo":"mixedbread-ai/mxbai-embed-large-v1", "job":"04_EMBEDDINGS_QUALITY"},
>> "%SCRIPT_PATH%" echo     {"folder":"E04_embedder_quality__bge_large_en", "repo":"BAAI/bge-large-en-v1.5", "job":"04_EMBEDDINGS_QUALITY"},
>> "%SCRIPT_PATH%" echo     {"folder":"E03_embedder_fast__sbert_minilm", "repo":"sentence-transformers/all-MiniLM-L6-v2", "job":"03_EMBEDDINGS_FAST"},
>> "%SCRIPT_PATH%" echo     {"folder":"E03_embedder_fast__e5_small", "repo":"intfloat/e5-small-v2", "job":"03_EMBEDDINGS_FAST"},
>> "%SCRIPT_PATH%" echo.
>> "%SCRIPT_PATH%" echo     {"folder":"C01_contradiction_primary__deberta_large_nli", "repo":"MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli", "job":"01_CONTRADICTION_PRIMARY"},
>> "%SCRIPT_PATH%" echo     {"folder":"C02_contradiction_fast__minilm_nli", "repo":"cross-encoder/nli-MiniLM2-L6-H768", "job":"02_CONTRADICTION_FAST"},
>> "%SCRIPT_PATH%" echo     {"folder":"C02_contradiction_fast__deberta_base_nli", "repo":"MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli", "job":"02_CONTRADICTION_FAST"},
>> "%SCRIPT_PATH%" echo     {"folder":"C14_contradiction_tiny__distilbert_mnli", "repo":"typeform/distilbert-base-uncased-mnli", "job":"14_CONTRADICTION_TINY"},
>> "%SCRIPT_PATH%" echo     {"folder":"C15_contradiction_long__tasksource_long_nli", "repo":"tasksource/deberta-base-long-nli", "job":"15_CONTRADICTION_ENSEMBLE / long NLI"},
>> "%SCRIPT_PATH%" echo.
>> "%SCRIPT_PATH%" echo     {"folder":"Z07_zero_shot__deberta_large_v2", "repo":"MoritzLaurer/deberta-v3-large-zeroshot-v2.0", "job":"07_ZERO_SHOT_CLASSIFIER"},
>> "%SCRIPT_PATH%" echo     {"folder":"N06_ner_general__bert_base_ner", "repo":"dslim/bert-base-NER", "job":"06_NER_GENERAL"},
>> "%SCRIPT_PATH%" echo     {"folder":"N16_ner_enhanced__gliner_multi", "repo":"urchade/gliner_multi-v2.1", "job":"16_NER_ENHANCED"},
>> "%SCRIPT_PATH%" echo.
>> "%SCRIPT_PATH%" echo     {"folder":"S08_summarizer__bart_cnn", "repo":"facebook/bart-large-cnn", "job":"08_SUMMARIZER / M13_bart_summarizer"},
>> "%SCRIPT_PATH%" echo     {"folder":"S08_summarizer_long__led_arxiv", "repo":"allenai/led-large-16384-arxiv", "job":"08_SUMMARIZER long papers"},
>> "%SCRIPT_PATH%" echo     {"folder":"S08_summarizer_short__pegasus_xsum", "repo":"google/pegasus-xsum", "job":"08_SUMMARIZER short abstractive"},
>> "%SCRIPT_PATH%" echo.
>> "%SCRIPT_PATH%" echo     {"folder":"R09_reranker__bge_v2_m3", "repo":"BAAI/bge-reranker-v2-m3", "job":"09_RERANKER"},
>> "%SCRIPT_PATH%" echo     {"folder":"R09_reranker_fast__msmarco_minilm", "repo":"cross-encoder/ms-marco-MiniLM-L12-v2", "job":"09_RERANKER fast"},
>> "%SCRIPT_PATH%" echo.
>> "%SCRIPT_PATH%" echo     {"folder":"T10_sentiment__twitter_roberta", "repo":"cardiffnlp/twitter-roberta-base-sentiment-latest", "job":"10_SENTIMENT"},
>> "%SCRIPT_PATH%" echo     {"folder":"T10_emotions__go_emotions", "repo":"SamLowe/roberta-base-go_emotions", "job":"10_SENTIMENT / emotion detail"},
>> "%SCRIPT_PATH%" echo.
>> "%SCRIPT_PATH%" echo     {"folder":"Q18_qa_extractor__roberta_squad2", "repo":"deepset/roberta-base-squad2", "job":"18_QA_EXTRACTOR"},
>> "%SCRIPT_PATH%" echo     {"folder":"Q18_qa_extractor_large__roberta_squad2", "repo":"deepset/roberta-large-squad2", "job":"18_QA_EXTRACTOR quality"},
>> "%SCRIPT_PATH%" echo.
>> "%SCRIPT_PATH%" echo     {"folder":"V13_image_caption__blip_large", "repo":"Salesforce/blip-image-captioning-large", "job":"13_IMAGE_CAPTION"},
>> "%SCRIPT_PATH%" echo     {"folder":"V13_image_caption__vit_gpt2", "repo":"nlpconnect/vit-gpt2-image-captioning", "job":"13_IMAGE_CAPTION fast/simple"},
>> "%SCRIPT_PATH%" echo.
>> "%SCRIPT_PATH%" echo     {"folder":"O11_math_ocr__pix2text_mfr", "repo":"breezedeus/pix2text-mfr-1.5", "job":"11_MATH_OCR"},
>> "%SCRIPT_PATH%" echo.
>> "%SCRIPT_PATH%" echo     {"folder":"L06_llm_optional__mistral_7b_instruct", "repo":"mistralai/Mistral-7B-Instruct-v0.3", "job":"M15_mistral_7b / optional gated LLM", "optional": True},
>> "%SCRIPT_PATH%" echo     {"folder":"A16_audio_transcribe__whisper_large_v3", "repo":"openai/whisper-large-v3", "job":"M16_whisper_large_v3 / transcription"}
>> "%SCRIPT_PATH%" echo ]
>> "%SCRIPT_PATH%" echo.
>> "%SCRIPT_PATH%" echo manifest = []
>> "%SCRIPT_PATH%" echo failures = []
>> "%SCRIPT_PATH%" echo print(f"Downloading {len(MODELS)} model snapshots into {ROOT}")
>> "%SCRIPT_PATH%" echo for i, m in enumerate(MODELS, 1):
>> "%SCRIPT_PATH%" echo     folder = ROOT / m["folder"]
>> "%SCRIPT_PATH%" echo     repo = m["repo"]
>> "%SCRIPT_PATH%" echo     print("\n" + "="*72)
>> "%SCRIPT_PATH%" echo     print(f"[{i}/{len(MODELS)}] {repo}")
>> "%SCRIPT_PATH%" echo     print(f"Folder: {folder.name}")
>> "%SCRIPT_PATH%" echo     try:
>> "%SCRIPT_PATH%" echo         folder.mkdir(parents=True, exist_ok=True)
>> "%SCRIPT_PATH%" echo         local_path = snapshot_download(
>> "%SCRIPT_PATH%" echo             repo_id=repo,
>> "%SCRIPT_PATH%" echo             repo_type="model",
>> "%SCRIPT_PATH%" echo             local_dir=str(folder),
>> "%SCRIPT_PATH%" echo             token=token,
>> "%SCRIPT_PATH%" echo             resume_download=True,
>> "%SCRIPT_PATH%" echo         )
>> "%SCRIPT_PATH%" echo         record = {**m, "status":"ok", "local_path":local_path}
>> "%SCRIPT_PATH%" echo         manifest.append(record)
>> "%SCRIPT_PATH%" echo         (folder / "_CAPABILITY.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
>> "%SCRIPT_PATH%" echo     except Exception as e:
>> "%SCRIPT_PATH%" echo         err = {**m, "status":"failed", "error":str(e)}
>> "%SCRIPT_PATH%" echo         failures.append(err)
>> "%SCRIPT_PATH%" echo         manifest.append(err)
>> "%SCRIPT_PATH%" echo         print(f"FAILED: {repo}: {e}")
>> "%SCRIPT_PATH%" echo         traceback.print_exc()
>> "%SCRIPT_PATH%" echo     time.sleep(1)
>> "%SCRIPT_PATH%" echo.
>> "%SCRIPT_PATH%" echo (STATE_DIR / "model_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
>> "%SCRIPT_PATH%" echo (STATE_DIR / "download_failures.json").write_text(json.dumps(failures, indent=2), encoding="utf-8")
>> "%SCRIPT_PATH%" echo print("\n" + "="*72)
>> "%SCRIPT_PATH%" echo print(f"Done. Successful: {sum(1 for x in manifest if x['status']=='ok')} / {len(manifest)}")
>> "%SCRIPT_PATH%" echo if failures:
>> "%SCRIPT_PATH%" echo     print(f"Failures: {len(failures)}. See: {STATE_DIR / 'download_failures.json'}")
>> "%SCRIPT_PATH%" echo else:
>> "%SCRIPT_PATH%" echo     print("No failures.")
>> "%SCRIPT_PATH%" echo print(f"Manifest: {STATE_DIR / 'model_manifest.json'}")

echo Starting downloads. This can take a long time.
echo Log file: %LOG_DIR%\model_download_run.log
echo.
python "%SCRIPT_PATH%" 2>&1 | tee "%LOG_DIR%\model_download_run.log"

if errorlevel 1 (
    echo.
    echo The run ended with an error. Check: %LOG_DIR%\model_download_run.log
) else (
    echo.
    echo Finished. Check: %STATE_DIR%\model_manifest.json
)

pause
endlocal
