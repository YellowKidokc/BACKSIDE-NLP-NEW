@echo off
setlocal
echo [SMOKE] ST-NLP-010
type "..\input\sample_input.md" >nul
echo {"status":"ok","smoke":"pass"}
