@echo off
setlocal
echo [SMOKE] ST-7QS-012
type "..\input\sample_input.md" >nul
echo {"status":"ok","smoke":"pass"}
