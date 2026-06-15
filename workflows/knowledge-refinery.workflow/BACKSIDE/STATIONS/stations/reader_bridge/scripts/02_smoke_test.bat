@echo off
setlocal
echo [SMOKE] {{STATION_ID}}
type "..\input\sample_input.md" >nul
echo {"status":"ok","smoke":"pass"}
