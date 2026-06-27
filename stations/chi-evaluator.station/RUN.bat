@echo off
echo === chi-evaluator.station ===
echo χ-Evaluator v2 — Coherence Diagnostic Engine
echo.
python "%~dp0pipeline.py" %*
pause
