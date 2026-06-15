@echo off
setlocal
cd /d "%~dp0"

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
  python run_axiom_7q_stations.py --openai --openai-model o3 --file-limit 1 --openai-limit 1
  exit /b %ERRORLEVEL%
)

py -3.11 run_axiom_7q_stations.py --openai --openai-model o3 --file-limit 1 --openai-limit 1
exit /b %ERRORLEVEL%
