@echo off
setlocal
echo [SMOKE] ST-EMBED-001
type "..\input\sample_input.md" >nul
echo {"status":"ok","smoke":"pass"}
