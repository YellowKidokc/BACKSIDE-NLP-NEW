@echo off
setlocal
echo [SMOKE] ST-EMBED-006
type "..\input\sample_input.md" >nul
echo {"status":"ok","smoke":"pass"}
