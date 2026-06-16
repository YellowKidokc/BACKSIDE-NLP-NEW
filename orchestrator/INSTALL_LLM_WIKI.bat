@echo off
echo ============================================
echo  Installing Karpathy LLM Wiki (obsidian-llm-wiki)
echo  + obsidiantools (vault analysis library)
echo ============================================
echo.

set PYTHON=C:\Python314\python.exe

echo [1/3] Installing obsidian-llm-wiki...
%PYTHON% -m pip install obsidian-llm-wiki --break-system-packages
echo.

echo [2/3] Installing obsidiantools (vault graph analysis)...
%PYTHON% -m pip install obsidiantools --break-system-packages
echo.

echo [3/3] Verifying installation...
%PYTHON% -c "import subprocess; result = subprocess.run(['olw', '--version'], capture_output=True, text=True); print(result.stdout or 'olw installed')"
%PYTHON% -c "import obsidiantools; print(f'obsidiantools {obsidiantools.__version__} installed')"
echo.

echo ============================================
echo  Installation complete.
echo.
echo  QUICK START:
echo.
echo  1. Initialize a wiki workspace:
echo     olw init
echo.
echo  2. Configure your wiki.toml:
echo     - Set Ollama URL (default: localhost:11434)
echo     - Set fast model (e.g., gemma3:4b or mistral)
echo     - Set heavy model (e.g., mistral or qwen2.5:14b)
echo.
echo  3. Drop raw notes into raw/ folder
echo.
echo  4. Compile:
echo     olw compile
echo.
echo  5. Watch mode (auto-process new files):
echo     olw watch
echo.
echo  6. Lint (find broken links, orphans, gaps):
echo     olw lint
echo.
echo  7. Open wiki/ folder as Obsidian vault
echo.
echo ============================================
pause
