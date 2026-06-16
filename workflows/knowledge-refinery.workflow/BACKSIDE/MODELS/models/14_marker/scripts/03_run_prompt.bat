@echo off
setlocal
if "%~1"=="" (
  echo Usage: 03_run_prompt.bat input_pdf [output_dir]
  exit /b 2
)
set "IN=%~1"
set "OUT=%~2"
if "%OUT%"=="" set "OUT=..\\output"
echo TODO: wire Marker CLI invocation for %IN% > "%OUT%\\marker.todo.txt"
echo WROTE %OUT%\\marker.todo.txt

