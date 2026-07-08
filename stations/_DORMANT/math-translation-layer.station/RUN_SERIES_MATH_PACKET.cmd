@echo off
setlocal

set "STATION_ROOT=%~dp0.."
set "SERIES_ROOT=\\dlowenas\HPWorkstation\Desktop\Master HTMl\_____ KIMI WORKFLOW\canonical\site\moral-decline"
set "OUT_DIR=%STATION_ROOT%\exports\series-math-packets"
set "WORKBOOK=%STATION_ROOT%\data\math_translation_table_updated_1.xlsx"

python "%STATION_ROOT%\scripts\build_series_math_review_packet.py" --series-root "%SERIES_ROOT%" --out "%OUT_DIR%" --series-code MDA --workbook "%WORKBOOK%"

echo.
echo Done. Review packet written under:
echo %OUT_DIR%
pause
