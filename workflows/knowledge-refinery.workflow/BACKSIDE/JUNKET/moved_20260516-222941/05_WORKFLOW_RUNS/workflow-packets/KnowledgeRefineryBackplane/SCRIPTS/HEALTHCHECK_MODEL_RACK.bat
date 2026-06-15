@echo off
setlocal
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0healthcheck_model_rack.ps1"
