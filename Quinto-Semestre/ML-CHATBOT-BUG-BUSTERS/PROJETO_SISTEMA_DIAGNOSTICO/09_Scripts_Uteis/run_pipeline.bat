@echo off
REM ============================================================================
REM SCRIPT: run_pipeline.bat
REM Executa APENAS o pipeline de ML
REM ============================================================================

setlocal enabledelayedexpansion
set "BASE_DIR=%~dp0.."
cd /d "%BASE_DIR%\02_ML_Pipeline"
python 2_pipeline_ml.py
pause
