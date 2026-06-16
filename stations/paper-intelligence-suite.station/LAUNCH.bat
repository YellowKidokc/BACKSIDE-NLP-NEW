@echo off
title THEOPHYSICS PAPER INTELLIGENCE SUITE
echo.
echo ================================================
echo  THEOPHYSICS PAPER INTELLIGENCE SUITE v2.0
echo ================================================
echo.
echo  What do you want to analyze?
echo.
echo  [1] Single paper
echo  [2] Full series folder
echo  [3] Genesis to Quantum series (preset)
echo  [4] Run Truth Engine only
echo  [5] Build Knowledge Graph only
echo  [6] Run OpenAI 7Q only (vault output)
echo.
set /p choice=Enter choice (1-6): 

if "%choice%"=="1" goto single
if "%choice%"=="2" goto series
if "%choice%"=="3" goto gtq
if "%choice%"=="4" goto truth
if "%choice%"=="5" goto graph
if "%choice%"=="6" goto openai

:single
set /p paper=Enter full path to paper .md file: 
python 00_ORCHESTRATOR\run_pipeline.py --paper "%paper%"
goto end

:series
set /p folder=Enter full path to series folder: 
python 00_ORCHESTRATOR\run_pipeline.py --series "%folder%"
goto end

:gtq
set SERIES="O:\_Theophysics_v4\04_THEOPYHISCS\[TX_A6.6] THE CONVERGENCE\GENESIS TO QUANTUM The Seven-Article Series"
set OUTPUT="O:\_Theophysics_v4 Data Vault\04_THEOPYHISCS_MIRROR\04_THEOPYHISCS\[TX_A6.6] THE CONVERGENCE\GENESIS TO QUANTUM The Seven-Article Series\_ANALYTICS"
python 00_ORCHESTRATOR\run_pipeline.py --series %SERIES% --output %OUTPUT%
goto end

:truth
set /p folder=Enter folder path: 
python 06_TRUTH_ENGINE\truth_runner.py --folder "%folder%"
goto end

:graph
set /p folder=Enter folder path: 
python 07_KNOWLEDGE_GRAPHS\graph_builder.py --folder "%folder%"
goto end

:openai
set /p folder=Enter folder path: 
python 04_OPENAI_7Q\seven_q_runner.py --folder "%folder%"
goto end

:end
echo.
echo Done. Check OUTPUT folder for results.
pause
