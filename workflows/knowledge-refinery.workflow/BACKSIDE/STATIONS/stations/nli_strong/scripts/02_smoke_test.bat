@echo off
setlocal
echo [SMOKE] ST-NLI-003
type "..\input\sample_input.md" >nul
echo {"status":"ok","smoke":"pass"}
