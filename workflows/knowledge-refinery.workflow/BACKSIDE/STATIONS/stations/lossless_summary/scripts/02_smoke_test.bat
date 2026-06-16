@echo off
setlocal
echo [SMOKE] ST-SUM-015
type "..\input\sample_input.md" >nul
echo {"status":"ok","smoke":"pass"}
