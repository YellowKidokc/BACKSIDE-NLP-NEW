@echo off
setlocal
title NLP Model Download - New Model Stations
echo ============================================
echo  NLP Model Download - New Model Stations
echo  Downloads to \\dlowenas\brain\models
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
  echo [FAIL] Python was not found. Install Python or fix this batch file.
  pause
  exit /b 1
)

echo.
echo [1/5] Installing math-verify equation checker...
%PYTHON% -m pip install math-verify
echo Done.
echo.

echo [2/5] Downloading fact_verify RoBERTa NLI model...
%PYTHON% -c "from huggingface_hub import snapshot_download; snapshot_download('ynie/roberta-large-snli_mnli_fever_anli_R1_R2_R3-nli', local_dir=r'%MODELS%\fact_verify\roberta_nli')"
echo Done.
echo.

echo [3/5] Downloading contradiction_detect RoBERTa NLI model...
%PYTHON% -c "from huggingface_hub import snapshot_download; snapshot_download('ynie/roberta-large-snli_mnli_fever_anli_R1_R2_R3-nli', local_dir=r'%MODELS%\contradiction_detect\roberta_nli')"
echo Note: contradiction_detect can also use the existing deberta_nli model.
echo Done.
echo.

echo [4/5] Cloning timeline_verify TISER repository...
where git >nul 2>&1
if %errorlevel% neq 0 (
  echo [WARN] git is not available. Skipping TISER clone.
) else (
  cd /d "%MODELS%\timeline_verify"
  git clone https://github.com/amazon-science/TISER.git 2>nul || echo Already cloned.
)
echo Done.
echo.

echo [5/5] Cloning claim_extract FactDetect repository...
where git >nul 2>&1
if %errorlevel% neq 0 (
  echo [WARN] git is not available. Skipping FactDetect clone.
) else (
  cd /d "%MODELS%\claim_extract"
  git clone https://github.com/nazaninjafar/factdetect.git 2>nul || echo Already cloned.
)
echo Done.
echo.

echo ============================================
echo  New model station download pass complete.
echo  Run HEALTHCHECK_ALL_MODELS.bat to verify.
echo ============================================
pause
