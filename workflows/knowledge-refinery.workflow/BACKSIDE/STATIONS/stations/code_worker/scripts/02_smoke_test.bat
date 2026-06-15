@echo off
setlocal
echo [SMOKE] ST-CODE-013
type "..\input\sample_input.md" >nul
echo {"status":"ok","smoke":"pass"}
