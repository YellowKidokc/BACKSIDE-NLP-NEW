@echo off
echo ============================================
echo  BRAIN CODEX EXPORT - Theophysics POF 2828
echo ============================================
echo.
echo This will create a clean export on your Desktop.
echo Stations, workflows, model/engine shells, orchestrator scripts.
echo NO model weights, NO private data, NO runtime state.
echo.
cd /d X:\07_ORCHESTRATOR
python create_codex_export.py
echo.
echo Export complete. Check your Desktop for BRAIN_CODEX_EXPORT folder.
echo Review before uploading to GitHub.
pause
