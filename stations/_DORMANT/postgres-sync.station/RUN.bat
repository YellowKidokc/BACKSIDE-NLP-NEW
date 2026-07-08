@echo off
setlocal
cd /d "%~dp0"
if /I "%~1"=="connect" goto connect
if /I "%~1"=="export" goto export
if /I "%~1"=="import" goto import
if /I "%~1"=="load-youtube" goto load_youtube
if /I "%~1"=="install" goto install
echo Usage: RUN.bat connect ^| export ^| import ^| load-youtube ^| install
exit /b 0
:connect
call CONNECT.bat
exit /b %ERRORLEVEL%
:export
call EXPORT.bat
exit /b %ERRORLEVEL%
:import
call IMPORT.bat
exit /b %ERRORLEVEL%
:load_youtube
call LOAD_YOUTUBE_JSON.bat
exit /b %ERRORLEVEL%
:install
call INSTALL.bat
exit /b %ERRORLEVEL%
