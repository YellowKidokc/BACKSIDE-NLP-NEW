@echo off
setlocal
cd /d "%~dp0"
call RUN_AXIOMS_WORKFLOW.bat %*
