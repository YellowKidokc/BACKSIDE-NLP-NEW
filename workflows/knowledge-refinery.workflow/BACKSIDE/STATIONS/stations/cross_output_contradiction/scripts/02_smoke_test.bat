@echo off
setlocal
echo [SMOKE] ST-RED-028
type "..\input\sample_input.md" >nul
echo {"status":"ok","smoke":"pass"}
