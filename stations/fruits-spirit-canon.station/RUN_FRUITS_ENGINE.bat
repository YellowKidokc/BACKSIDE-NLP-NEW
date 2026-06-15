@echo off
setlocal
cd /d "%~dp0"
echo ============================================
echo  STATION: fruits-spirit-canon
echo  Fruits Coherence Engine
echo  Drop papers in DROP_HERE\, drop a lexicon .xlsx in LEXICON\, then run this.
echo  Output: EXPORTS\fruits_reports\run_<timestamp>\
echo ============================================
python run_fruits_engine.py %*
set RC=%ERRORLEVEL%
echo ============================================
echo  Done (rc=%RC%).
echo ============================================
exit /b %RC%
