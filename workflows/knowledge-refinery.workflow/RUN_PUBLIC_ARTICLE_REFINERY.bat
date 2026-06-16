@echo off
setlocal
title Public Article Refinery
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\run_public_article_refinery.ps1" %*
pause
