@echo off
setlocal
if "%~1"=="" (
  echo Usage: 03_run_prompt.bat input_file [output_file]
  exit /b 2
)
set "IN=%~1"
set "OUT=%~2"
if "%OUT%"=="" set "OUT=..\\output\\graph.json"
echo {"status":"todo","note":"wire graph extractor runner here"} > "%OUT%"
echo WROTE %OUT%

