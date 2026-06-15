@echo off
setlocal
title Public Article Refinery
powershell -NoProfile -ExecutionPolicy Bypass -File "X:\knowledge-refinery\scripts\run_public_article_refinery.ps1" %*
pause
