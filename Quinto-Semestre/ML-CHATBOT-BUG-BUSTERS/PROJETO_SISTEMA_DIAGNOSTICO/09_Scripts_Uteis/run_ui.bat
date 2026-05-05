@echo off
REM ============================================================================
REM SCRIPT: run_ui.bat
REM Executa APENAS a Interface Streamlit
REM Porta: 8501
REM URL: http://localhost:8501
REM
REM Pre-requisito: API deve estar rodando em http://localhost:8000
REM ============================================================================

setlocal enabledelayedexpansion
set "BASE_DIR=%~dp0.."
cd /d "%BASE_DIR%\04_Interface"
streamlit run interface_streamlit.py
