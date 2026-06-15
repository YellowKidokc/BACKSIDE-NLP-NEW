@echo off
REM Launches an LLM session with this workflow mission loaded.
setlocal
set "PRIMER=X:\THEOPHYSICS_PRIMER.md"
set "BRIEF=%~dp0_AGENT_BRIEF.md"
set "MODEL=mistral:7b-instruct"

if exist "%~dp0config.json" (
  for /f "delims=" %%i in ('powershell -NoP -C "(Get-Content ''%~dp0config.json'' | ConvertFrom-Json).agent_model" 2^>nul') do set "MODEL=%%i"
)

set "SYS_TMP=%TEMP%\agent_sys_%RANDOM%.txt"
type "%PRIMER%" > "%SYS_TMP%"
echo. >> "%SYS_TMP%"
echo --- >> "%SYS_TMP%"
echo. >> "%SYS_TMP%"
type "%BRIEF%" >> "%SYS_TMP%"

for /f "delims=" %%i in ('powershell -NoP -C "Get-Content -Raw ''%SYS_TMP%''"') do set "SYS_PROMPT=%%i"
ollama run %MODEL% --system "%SYS_PROMPT%"

del "%SYS_TMP%" 2>nul
endlocal
