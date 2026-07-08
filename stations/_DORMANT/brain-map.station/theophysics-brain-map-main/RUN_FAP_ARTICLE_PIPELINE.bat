@echo off
setlocal
title FAP Article Manufacturing Pipeline
powershell -NoProfile -ExecutionPolicy Bypass -File "X:\knowledge-refinery\scripts\run_fap_article_pipeline.ps1" %*
pause
