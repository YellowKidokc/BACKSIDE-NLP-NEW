@echo off
chcp 65001 > nul
setlocal
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
cd /d "%~dp0"

if /I "%~1"=="schema" (
  python -m json.tool snapshot_schema.json
  exit /b %ERRORLEVEL%
)

if /I "%~1"=="consolidate" (
  shift
  python -m paper_grader.consolidate_metrics %*
  exit /b %ERRORLEVEL%
)

rem Default: grade every paper dropped in .\INPUT using the local engine.
echo ============================================
echo  STATION: paper-grader-nlp (local, no Docker)
echo  Drop papers into .\INPUT, then run this.
echo ============================================
set PAPER_GRADER_OUTPUT=%~dp0EXPORTS\paper_grade_runs
python -m paper_grader %*
set RC=%ERRORLEVEL%
echo ============================================
echo  Done (rc=%RC%). Reports in .\EXPORTS\paper_grade_runs
echo ============================================
exit /b %RC%
