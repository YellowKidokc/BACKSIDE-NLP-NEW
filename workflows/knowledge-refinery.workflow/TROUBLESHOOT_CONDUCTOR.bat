@echo off
echo ============================================
echo  Refinery Conductor Troubleshoot
echo ============================================
echo.

set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python313\python.exe

echo [1] Checking Python...
"%PYTHON%" --version 2>nul
if %errorlevel% neq 0 echo FAIL: Python not found at %PYTHON%

echo.
echo [2] Checking Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (echo FAIL: Ollama not responding) else (echo OK: Ollama running)

echo.
echo [3] Checking pipeline folders...
for %%d in (00_INTAKE 01_CONVERSION 02_NORMALIZATION 03_ROUTING 04_MODEL_STATIONS 05_WORKFLOW_RUNS 06_HTML_REPORTS 07_OBSIDIAN_EXPORT 08_ARCHIVE 09_MEMORY) do (
    if exist "X:\knowledge-refinery\%%d\" (echo OK: %%d) else (echo FAIL: %%d missing)
)

echo.
echo [4] Checking FAP prompts...
for %%f in (classify_document.md grade_paper.md vault_page_compiler.md) do (
    if exist "D:\FAP\wiki\prompts\%%f" (echo OK: %%f) else (echo FAIL: %%f missing)
)

echo.
echo [5] Checking script...
"%PYTHON%" -c "import py_compile; py_compile.compile(r'X:\knowledge-refinery\scripts\refinery_conductor.py', doraise=True); print('OK: Script compiles')" 2>&1

echo.
echo [6] Intake folder contents:
dir /b "X:\knowledge-refinery\00_INTAKE\" 2>nul
if %errorlevel% neq 0 echo (empty)

echo.
echo [7] Output folder contents:
dir /b "X:\knowledge-refinery\07_OBSIDIAN_EXPORT\" 2>nul
if %errorlevel% neq 0 echo (empty)

echo.
pause
