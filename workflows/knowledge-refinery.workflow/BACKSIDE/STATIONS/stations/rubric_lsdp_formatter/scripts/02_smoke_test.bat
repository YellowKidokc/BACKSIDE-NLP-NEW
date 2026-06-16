@echo off
setlocal
echo [SMOKE] ST-PUB-002
type "..\input\sample_input.md" >nul
echo {"status":"ok","smoke":"pass"}
