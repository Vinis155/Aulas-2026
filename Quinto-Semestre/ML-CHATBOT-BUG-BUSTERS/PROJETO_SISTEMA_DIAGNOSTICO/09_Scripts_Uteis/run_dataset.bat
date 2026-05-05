@echo off
REM ============================================================================
REM SCRIPT: run_dataset.bat
REM Executa APENAS o gerador de dataset
REM ============================================================================

setlocal enabledelayedexpansion
set "BASE_DIR=%~dp0.."
cd /d "%BASE_DIR%\01_Dataset"
python 1_gerar_dataset.py
pause
