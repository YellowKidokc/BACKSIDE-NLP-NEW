@echo off
setlocal enabledelayedexpansion
set "EXIT_CODE=0"
set "WARNINGS=0"
set "ENDPOINT="

for %%f in (README.md _AGENT_BRIEF.md RUN.bat config.json) do (
  if not exist "%~dp0%%f" (
    echo FAIL: missing %%f
    set "EXIT_CODE=1"
  )
)

for %%d in (00_DROP OUTPUT ARCHIVE) do (
  if not exist "%~dp0%%d" (
    echo FAIL: missing dir %%d
    set "EXIT_CODE=1"
  )
)

echo probe > "%~dp000_DROP\.health_probe" 2>nul
if exist "%~dp000_DROP\.health_probe" (
  del "%~dp000_DROP\.health_probe" 2>nul
) else (
  echo FAIL: 00_DROP not writable
  set "EXIT_CODE=1"
)

for /f "delims=" %%i in ('powershell -NoP -C "(Get-Content ''%~dp0config.json'' | ConvertFrom-Json).model_endpoint" 2^>nul') do set "ENDPOINT=%%i"
if defined ENDPOINT (
  set "HTTP_FILE=%TEMP%\http_probe_%RANDOM%.txt"
  curl -s -o nul -w "%%{http_code}" --max-time 5 "%ENDPOINT%" > "!HTTP_FILE!"
  set /p HTTP_CODE=<"!HTTP_FILE!"
  del "!HTTP_FILE!" 2>nul
  if "!HTTP_CODE!"=="200" (
    echo OK: %ENDPOINT% reachable
  ) else (
    echo WARN: %ENDPOINT% returned !HTTP_CODE!
    set "WARNINGS=1"
  )
)

set "LATEST_LOG="
for /f "delims=" %%i in ('powershell -NoP -C "$f=Get-ChildItem ''%~dp0_LOGS'' -File -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1; if($f){$f.LastWriteTime.ToString('yyyy-MM-dd')}"') do set "LATEST_LOG=%%i"
if not defined LATEST_LOG (
  echo WARN: no run logs found in _LOGS
  set "WARNINGS=1"
) else (
  for /f "delims=" %%i in ('powershell -NoP -C "if((Get-Date ''%LATEST_LOG%'') -lt (Get-Date).AddDays(-7)){''OLD''} else {''FRESH''}"') do set "LOG_STATE=%%i"
  if "!LOG_STATE!"=="OLD" (
    echo WARN: latest _LOGS entry older than 7 days (%LATEST_LOG%)
    set "WARNINGS=1"
  )
)

if "%EXIT_CODE%"=="0" (
  if "%WARNINGS%"=="1" (
    echo OVERALL: WARN
    exit /b 2
  ) else (
    echo OVERALL: PASS
    exit /b 0
  )
) else (
  echo OVERALL: FAIL
  exit /b 1
)
