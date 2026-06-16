@echo off
REM ============================================================
REM  READING LEVEL GENERATOR — Entry Point
REM  Generates Easy + Academic versions from Standard articles
REM ============================================================
REM
REM  USAGE:
REM    RUN.bat                          — runs on all staged MDA articles (manual prompt mode)
REM    RUN.bat MDA-001-story-intro.md   — runs on one article (manual prompt mode)
REM    RUN.bat MDA-001-story-intro.md --api openai    — calls OpenAI directly
REM    RUN.bat MDA-001-story-intro.md --api anthropic  — calls Anthropic directly
REM
REM  SEQUENCE (how it fits in the workflow):
REM    1. Codex runs Math Translation Layer + Paper Proof Grader → paper-grade.json
REM    2. This script takes Standard MD + paper-grade.json
REM    3. Stage 1: Generates Academic version + extracts TERM_INVENTORY
REM    4. Stage 2: Uses TERM_INVENTORY to generate Easy version
REM    5. Output lands in article_reading_levels\ folder
REM
REM  WITHOUT API KEY:
REM    Outputs prompt .txt files you can paste into any LLM manually.
REM
REM  WITH API KEY:
REM    Set OPENAI_API_KEY or ANTHROPIC_API_KEY as environment variable first.
REM    Then use --api openai or --api anthropic.
REM ============================================================

set SCRIPT_DIR=%~dp0
set PYTHON=python

REM Find Python - try system, then codex cache
where python >nul 2>&1
if %errorlevel% neq 0 (
    set PYTHON=C:\Users\lowes\.cache\codex-runtimes\node_modules\.cache\python\python.exe
)

if "%~1"=="" (
    echo.
    echo Running on all staged MDA articles...
    echo.
    for %%f in ("%SCRIPT_DIR%..\01_LOSSLESS\articles\MDA-*.md") do (
        echo Processing: %%~nxf
        %PYTHON% "%SCRIPT_DIR%generate_reading_levels.py" "%%f" %2 %3
        echo.
    )
) else (
    %PYTHON% "%SCRIPT_DIR%generate_reading_levels.py" %*
)

echo.
echo Done. Check output folders for _reading_levels\ directories.
pause
