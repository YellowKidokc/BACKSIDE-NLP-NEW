@echo off
setlocal
if "%~2"=="" (
    echo Usage: IMPORT.bat ^<table_name^> ^<csv_path^>
    echo Example: IMPORT.bat youtube_apologetics D:\brain\_LOGS\youtube_dump.csv
    exit /b 1
)
set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
"%PYTHON%" "%~dp0db_utils.py" import %1 %2
