@echo off
title POF2828 NLP API
echo ========================================
echo  POF 2828 NLP API
echo  Port: 8700
echo  Docs: http://localhost:8700/docs
echo ========================================
cd /d "%~dp0"
REM Use the 3.12 interpreter that has the full stack (transformers/torch/etc).
REM py launcher resolves per-machine; bare "python" can hit a stack-less install -> 500s.
REM Override with NLP_API_PY env var if a specific interpreter is needed.
if "%NLP_API_PY%"=="" (set PY=py -3.12) else (set PY=%NLP_API_PY%)
%PY% main.py
pause
