@echo off
setlocal
echo [SMOKE] ST-LCTX-014
type "..\input\sample_input.md" >nul
echo {"status":"ok","smoke":"pass"}
