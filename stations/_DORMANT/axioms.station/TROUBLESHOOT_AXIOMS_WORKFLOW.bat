@echo off
setlocal
title Troubleshoot Axioms Workflow
echo ============================================
echo  TROUBLESHOOT: Axioms Paper Workflow
echo ============================================

set ROOT=%~dp0
set PYTHON_EXE=
if exist "C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe" set PYTHON_EXE=C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe
if not defined PYTHON_EXE if exist "C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe" set PYTHON_EXE=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
if not defined PYTHON_EXE set PYTHON_EXE=py -3

echo [1/7] Creating required folders...
mkdir "%ROOT%00_INBOX_DROP_PAPERS_HERE" 2>nul
mkdir "%ROOT%01_OUTBOX_REPORTS" 2>nul
mkdir "%ROOT%02_HTML_OUTPUTS" 2>nul
mkdir "%ROOT%03_FINAL_READY" 2>nul
mkdir "%ROOT%04_ARCHIVE_ORIGINALS" 2>nul
mkdir "%ROOT%05_MANIFESTS" 2>nul
mkdir "%ROOT%_LOGS" 2>nul
mkdir "%ROOT%scripts" 2>nul

echo [2/7] Checking Python...
%PYTHON_EXE% --version
if errorlevel 1 goto fail

echo [3/7] Checking config JSON...
%PYTHON_EXE% -c "import json,pathlib; p=pathlib.Path(r'%ROOT%scripts\config.json'); cfg=json.loads(p.read_text(encoding='utf-8-sig')); print('config ok:', cfg.get('name'))"
if errorlevel 1 goto fail

echo [4/7] Checking script syntax...
%PYTHON_EXE% -m py_compile "%ROOT%scripts\axiom_paper_grader.py" "%ROOT%scripts\organize_axiom_outputs.py" "%ROOT%scripts\update_required_html_outputs.py" "%ROOT%scripts\axiom_rigor_gate.py"
if errorlevel 1 goto fail

echo [5/7] Checking required HTML source files...
%PYTHON_EXE% "%ROOT%scripts\update_required_html_outputs.py"

echo [6/7] Checking current inbox...
dir /b "%ROOT%00_INBOX_DROP_PAPERS_HERE"

echo [7/7] Checking optional vector services...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$cfg=Get-Content -LiteralPath '%ROOT%scripts\config.json' -Raw | ConvertFrom-Json; " ^
  "$inf=$cfg.embedding.infinity_url; $q=$cfg.qdrant.url; " ^
  "try { Invoke-WebRequest -Uri $inf -UseBasicParsing -TimeoutSec 5 | Out-Null; Write-Host 'Infinity reachable:' $inf } catch { Write-Host 'WARNING: Infinity not reachable:' $inf }; " ^
  "try { Invoke-WebRequest -Uri ($q + '/collections') -UseBasicParsing -TimeoutSec 5 | Out-Null; Write-Host 'Qdrant reachable:' $q } catch { Write-Host 'WARNING: Qdrant not reachable:' $q }"

echo.
echo Troubleshoot finished.
pause
exit /b 0

:fail
echo.
echo Troubleshoot found a blocker.
pause
exit /b 1

