@echo off
setlocal
title Axioms Paper Workflow
echo ============================================
echo  WORKFLOW: Axioms Paper Grader
echo.
echo  1. Drop papers into 00_INBOX_DROP_PAPERS_HERE
echo  2. This scores them and archives originals
echo  3. Reports go to 01_OUTBOX_REPORTS
echo  4. HTML copies go to 02_HTML_OUTPUTS
echo  5. Final-ready bundles go to 03_FINAL_READY
echo ============================================

set ROOT=%~dp0
set INBOX=\\dlowenas\brain\Backside\workflows\axioms.workflow\00_INBOX_DROP_PAPERS_HERE
set PYTHON_EXE=
if exist "C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe" set PYTHON_EXE=C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe
if not defined PYTHON_EXE if exist "C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe" set PYTHON_EXE=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
if not defined PYTHON_EXE set PYTHON_EXE=py -3

echo.
echo Active inbox: %INBOX%
echo.
echo Refreshing required reference HTML outputs...
%PYTHON_EXE% "%ROOT%scripts\update_required_html_outputs.py"

:loop
for /f %%C in ('powershell -NoProfile -Command "$ext=@('.txt','.md','.html','.htm'); (Get-ChildItem -LiteralPath '%INBOX%' -File -ErrorAction SilentlyContinue | Where-Object { $ext -contains $_.Extension.ToLowerInvariant() } | Measure-Object).Count"') do set COUNT=%%C
if "%COUNT%"=="0" (
  set RC=0
  goto organize
)

echo.
echo Processing %COUNT% paper file(s) still in inbox...
%PYTHON_EXE% "%ROOT%scripts\axiom_paper_grader.py"
set RC=%ERRORLEVEL%
if not "%RC%"=="0" goto done
goto loop

:organize
echo.
echo Organizing reports into HTML and final-ready folders...
%PYTHON_EXE% "%ROOT%scripts\organize_axiom_outputs.py"
set RC=%ERRORLEVEL%
if not "%RC%"=="0" goto done

echo.
echo Rendering one-page dashboard surfaces...
%PYTHON_EXE% "%ROOT%scripts\render_axiom_dashboard_surfaces.py"
set RC=%ERRORLEVEL%
if not "%RC%"=="0" goto done

echo.
echo Running Axiom rigor gate...
%PYTHON_EXE% "%ROOT%scripts\axiom_rigor_gate.py"
set RC=%ERRORLEVEL%
if not "%RC%"=="0" goto done

echo.
echo Exporting published HTML and final Excel to Brain EXPORTS...
%PYTHON_EXE% "%ROOT%scripts\export_published_outputs.py"
set RC=%ERRORLEVEL%

:done
echo ============================================
echo  Done (rc=%RC%).
echo  Logs: %ROOT%_LOGS
echo ============================================
if "%AXIOMS_NO_PAUSE%"=="1" exit /b %RC%
pause
exit /b %RC%

