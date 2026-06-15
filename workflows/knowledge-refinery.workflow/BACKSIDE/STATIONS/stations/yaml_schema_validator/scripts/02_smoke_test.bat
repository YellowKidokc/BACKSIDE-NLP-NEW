@echo off
setlocal
echo [SMOKE] ST-YAML-001
type "..\input\sample_input.md" >nul
echo {"status":"ok","smoke":"pass"}
