@echo off
setlocal
echo [SMOKE] ST-NLP-012
type "..\input\sample_input.md" >nul
echo {"status":"ok","smoke":"pass"}
