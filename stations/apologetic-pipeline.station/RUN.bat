@echo off
setlocal
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
cd /d "%~dp0"
if "%~1"=="" (
  python apologetics_pipeline.py --help
) else (
  python apologetics_pipeline.py %*
)
