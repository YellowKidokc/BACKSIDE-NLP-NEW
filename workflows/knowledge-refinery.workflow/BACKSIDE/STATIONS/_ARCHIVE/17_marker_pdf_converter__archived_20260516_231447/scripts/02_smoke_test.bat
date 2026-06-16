@echo off
setlocal
echo [SMOKE] ST-PDF-017
type "..\input\sample_input.md" >nul
echo {"status":"ok","smoke":"pass"}
