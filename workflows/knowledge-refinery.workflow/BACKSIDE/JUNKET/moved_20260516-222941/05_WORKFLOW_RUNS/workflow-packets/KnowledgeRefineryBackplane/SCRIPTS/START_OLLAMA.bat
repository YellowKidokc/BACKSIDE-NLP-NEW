@echo off
setlocal
where ollama >nul 2>nul
if errorlevel 1 (
  echo Ollama was not found on PATH.
  exit /b 2
)
echo Starting Ollama service if it is not already running...
start "Ollama" /min ollama serve
exit /b 0
