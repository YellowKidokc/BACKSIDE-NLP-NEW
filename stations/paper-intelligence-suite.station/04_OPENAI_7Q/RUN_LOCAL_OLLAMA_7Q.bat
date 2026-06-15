@echo off
setlocal

set "SCRIPT=%~dp0ollama_7q_runner.py"
set "DEFAULT_PAPER=C:\Users\lowes\OneDrive\Desktop\genesis-to-quantum\gtq-07a-empirical-testing.html"
set "OUT_DIR=T:\THEOPHYSICS_PAPER_INTELLIGENCE\OUTPUT\GTQ_LOCAL_OLLAMA_7Q_FAST"

if "%~1"=="" (
  set "PAPER=%DEFAULT_PAPER%"
) else (
  set "PAPER=%~1"
)

echo Running local Ollama 7Q audit...
echo Paper: %PAPER%
echo Output: %OUT_DIR%

python "%SCRIPT%" ^
  --paper "%PAPER%" ^
  --output "%OUT_DIR%" ^
  --model qwen2.5:3b ^
  --sections classic,snapshot ^
  --head 1800 ^
  --tail 400 ^
  --timeout 210 ^
  --classic-tokens 950 ^
  --section-tokens 1100

pause
