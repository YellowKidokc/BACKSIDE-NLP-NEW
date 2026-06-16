@echo off
setlocal
cd /d "%~dp0.."

echo ================================================
echo  L3 THEOPHYSICS METRICS - SINGLE FILE TEST
echo ================================================
echo.

set "DEFAULT_INPUT=C:\Users\lowes\OneDrive\Desktop\genesis-to-quantum\gtq-07a-empirical-testing.html"
set "INPUT=%~1"
if "%INPUT%"=="" set "INPUT=%DEFAULT_INPUT%"

echo Input:
echo   %INPUT%
echo.

if not exist "%INPUT%" (
  echo ERROR: Input file not found.
  echo Pass a file path as the first argument or edit DEFAULT_INPUT in this BAT.
  exit /b 1
)

python -c "import sys,json; sys.path.insert(0,r'T:\THEOPHYSICS_PAPER_INTELLIGENCE\03_THEOPHYSICS_METRICS'); import theophysics_scorer; r=theophysics_scorer.analyze(r'%INPUT%'); print(json.dumps(r, indent=2, ensure_ascii=False))"
set RC=%ERRORLEVEL%

echo.
echo Done. rc=%RC%
exit /b %RC%
