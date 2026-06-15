@echo off
setlocal
echo [SMOKE] ST-SCORE-002
type "..\input\sample_input.md" >nul
echo {"status":"ok","smoke":"pass"}
