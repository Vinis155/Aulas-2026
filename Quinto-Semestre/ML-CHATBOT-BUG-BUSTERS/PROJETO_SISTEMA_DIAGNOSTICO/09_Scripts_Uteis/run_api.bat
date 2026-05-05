@echo off
REM ============================================================================
REM SCRIPT: run_api.bat
REM Executa APENAS a API REST
REM Porta: 8000
REM URL: http://localhost:8000
REM Swagger: http://localhost:8000/docs
REM ============================================================================

setlocal enabledelayedexpansion
set "BASE_DIR=%~dp0.."
cd /d "%BASE_DIR%\03_API"
uvicorn api_biomedicina:app --port 8000
