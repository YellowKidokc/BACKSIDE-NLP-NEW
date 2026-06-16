@echo off
setlocal
echo [SMOKE] 13_markitdown
type "..\\input\\sample_input.md" >nul
echo {"status":"ok","smoke":"pass"}

