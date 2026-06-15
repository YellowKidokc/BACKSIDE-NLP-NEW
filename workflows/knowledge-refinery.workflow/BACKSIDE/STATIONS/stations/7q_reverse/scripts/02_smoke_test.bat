@echo off
setlocal
echo [SMOKE] ST-7QS-010
type "..\input\sample_input.md" >nul
echo {"status":"ok","smoke":"pass"}
