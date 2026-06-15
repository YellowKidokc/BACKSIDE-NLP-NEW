@echo off
setlocal
call "%~dp0RUN_AXIOM_7Q_STATION.bat" --openai --openai-model o3 --file-limit 1 --openai-limit 1
exit /b %ERRORLEVEL%
