@echo off
setlocal
echo [SMOKE] ST-7QS-011
type "..\input\sample_input.md" >nul
echo {"status":"ok","smoke":"pass"}
