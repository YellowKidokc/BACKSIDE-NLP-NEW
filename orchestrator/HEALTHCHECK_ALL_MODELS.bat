@echo off
setlocal
title NLP Model Healthcheck - All Models
echo ============================================
echo  NLP Model Healthcheck - All Models
echo ============================================
echo.

set PYTHON=
if exist "C:\Python314\python.exe" set PYTHON=C:\Python314\python.exe
if not defined PYTHON if exist "C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe" set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe
if not defined PYTHON if exist "C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe" set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
if not defined PYTHON set PYTHON=python
set MODELS=\\dlowenas\brain\models

echo Python: %PYTHON%
%PYTHON% --version
if %errorlevel% neq 0 (
  echo [FAIL] Python was not found.
  pause
  exit /b 1
)

echo.
echo Checking existing models...
echo.

echo [bart_summarizer]
if exist "%MODELS%\bart_summarizer\model.safetensors" (echo   OK - weights present) else (echo   MISSING)

echo [sbert_minilm]
if exist "%MODELS%\sbert_minilm\model.safetensors" (echo   OK - weights present) else (echo   MISSING)

echo [deberta_nli]
if exist "%MODELS%\deberta_nli\model.safetensors" (echo   OK - weights present) else (echo   MISSING)

echo [clip_vision]
if exist "%MODELS%\clip_vision\pytorch_model.bin" (echo   OK - weights present) else (echo   MISSING)

echo [whisper_large_v3]
if exist "%MODELS%\whisper_large_v3\model.bin" (echo   OK - weights present) else (echo   MISSING)

echo [mistral_7b]
if exist "%MODELS%\mistral_7b\model-00001-of-00003.safetensors" (echo   OK - weights present) else (echo   MISSING)

echo.
echo Checking new model stations...
echo.

echo [math_verify]
%PYTHON% -c "import math_verify; print('  OK - library installed')" 2>nul || echo   NOT INSTALLED - run DOWNLOAD_NEW_MODELS.bat

echo [fact_verify]
if exist "%MODELS%\fact_verify\roberta_nli\config.json" (echo   OK - roberta_nli present) else (echo   NOT DOWNLOADED)

echo [contradiction_detect]
if exist "%MODELS%\contradiction_detect\roberta_nli\config.json" (echo   OK - roberta_nli present) else (echo   NOT DOWNLOADED)
echo   Note: deberta_nli also works for contradiction detection.

echo [timeline_verify]
if exist "%MODELS%\timeline_verify\TISER\README.md" (echo   OK - TISER cloned) else (echo   NOT CLONED)

echo [claim_extract]
if exist "%MODELS%\claim_extract\factdetect\README.md" (echo   OK - FactDetect cloned) else (echo   NOT CLONED)

echo [paper_review]
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% equ 0 (echo   OK - Ollama running) else (echo   Ollama NOT running)

echo.
echo ============================================
echo  Health check complete.
echo ============================================
pause
