@echo off
setlocal
echo [INIT] ST-YAML-001
if not exist "..\output" mkdir "..\output"
if not exist "..\logs"   mkdir "..\logs"
if not exist "..\cache"  mkdir "..\cache"
if not exist "..\review" mkdir "..\review"
if not exist "..\errors" mkdir "..\errors"
echo [INIT] ok
