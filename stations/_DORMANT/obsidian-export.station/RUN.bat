@echo off
setlocal
cd /d "%~dp0"
python scripts\export_obsidian_notes.py %*
