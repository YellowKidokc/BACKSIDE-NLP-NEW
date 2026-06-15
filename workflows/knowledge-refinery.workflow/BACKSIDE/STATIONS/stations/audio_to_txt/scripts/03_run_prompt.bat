@echo off
setlocal
if "%~1"=="" (
  echo Usage: 03_run_prompt.bat input_file [output_file]
  exit /b 2
)
set "IN=%~1"
set "OUT=%~2"
if "%OUT%"=="" set "OUT=..\output\run_output.json"
REM TODO: wire actual runner. Default: invoke run.py in this folder.
if exist "%~dp0run.py" (
  python "%~dp0run.py" --in "%IN%" --out "%OUT%"
) else (
  echo {"status":"todo","note":"wire runner here"} > "%OUT%"
  echo WROTE %OUT%
)
