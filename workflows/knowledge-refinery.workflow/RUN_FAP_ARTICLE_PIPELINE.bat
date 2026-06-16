@echo off
setlocal
title FAP Article Manufacturing Pipeline
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\run_fap_article_pipeline.ps1" %*
pause
