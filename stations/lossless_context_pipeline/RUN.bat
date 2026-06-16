@echo off
setlocal
chcp 65001 >nul
echo ============================================
echo  STATION: lossless-context
echo  sample_article.md -> EXPORTS\sample
echo ============================================

set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
if not exist "%PYTHON%" (
  set PYTHON=python
)

if not exist "%~dp0EXPORTS" mkdir "%~dp0EXPORTS"

pushd "%~dp0.."
"%PYTHON%" -m lossless_context_pipeline.cli run --input "%~dp0samples\sample_article.md" --out "%~dp0EXPORTS\sample" --vault-id theophysics-brain --embeddings none
set RC=%ERRORLEVEL%
popd

echo ============================================
echo  Done (rc=%RC%). Output: %~dp0EXPORTS\sample
echo ============================================
pause
exit /b %RC%
