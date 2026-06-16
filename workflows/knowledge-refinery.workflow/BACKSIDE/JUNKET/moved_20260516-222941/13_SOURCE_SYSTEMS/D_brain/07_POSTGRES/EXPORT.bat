@echo off
setlocal
if "%~2"=="" (
    echo Usage: EXPORT.bat ^<table_name^> ^<out_csv_path^>
    echo Example: EXPORT.bat youtube_apologetics D:\brain\_LOGS\youtube_dump.csv
    exit /b 1
)
set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
"%PYTHON%" "%~dp0db_utils.py" export %1 %2
