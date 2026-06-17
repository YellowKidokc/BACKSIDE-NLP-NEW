@echo off
title POF2828 NLP API
echo ========================================
echo  POF 2828 NLP API
echo  Port: 8700
echo  Docs: http://localhost:8700/docs
echo ========================================
cd /d "%~dp0"
REM Pin to the 3.12 interpreter that actually has the full stack (transformers/torch/etc).
REM Bare "python" can resolve to the 3.14 install which lacks transformers -> 500s.
set PY=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
"%PY%" main.py
pause
