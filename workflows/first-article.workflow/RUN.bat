@echo off
setlocal
python "%~dp0pipeline.py" --drop "%~dp000_DROP" %*
pause
