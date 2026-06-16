@echo off
echo ============================================
echo  Installing Theophysics Refinery Scheduler
echo  Runs every hour when computer is idle
echo ============================================
echo.
powershell -ExecutionPolicy Bypass -Command "& {$action = New-ScheduledTaskAction -Execute "X:\knowledge-refinery\SCHEDULED_IDLE_RUN.bat"
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddHours(1) -RepetitionInterval (New-TimeSpan -Hours 1)
$settings = New-ScheduledTaskSettingsSet -IdleWaitTimeout (New-TimeSpan -Minutes 60) -RunOnlyIfIdle -IdleDuration (New-TimeSpan -Minutes 60) -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -RunLevel Highest

Register-ScheduledTask -TaskName "TheophysicsRefinery" -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description "Theophysics Knowledge Refinery - processes files every hour when idle" -Force}"
echo.
echo Task 'TheophysicsRefinery' installed.
echo It will run every hour when the computer has been idle for 60 minutes.
echo Processes up to 5 files per phase (HTML DUMP, C4C-wiki, Obsidian).
echo Log: X:\knowledge-refinery\12_HEALTH\scheduled_runs.log
pause
