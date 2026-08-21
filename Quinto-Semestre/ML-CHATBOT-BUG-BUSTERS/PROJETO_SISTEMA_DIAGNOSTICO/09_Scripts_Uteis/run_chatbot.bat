@echo off
REM ========================================================
REM SCRIPT PARA RODAR CHATBOT CLINICA BIOMEDICINA
REM ========================================================

setlocal enabledelayedexpansion

echo.
echo ========================================================
echo.  CHATBOT CLINICA DE BIOMEDICINA
echo.
echo  Iniciando todos os servicos necessarios...
echo.
echo  - API (porta 8000)
echo  - Chatbot Streamlit (porta 8501)
echo.
echo ========================================================
echo.

REM Diretorio base
set BASE_DIR=%~dp0..
set API_DIR=%BASE_DIR%\03_API
set CHATBOT_DIR=%BASE_DIR%\04_Interface
set VENV=%BASE_DIR%\..\..\.venv

REM Verificar venv
if not exist "%VENV%\Scripts\python.exe" (
    echo ERROR: Virtual environment nao encontrado em %VENV%
    echo Execute configure_python_environment primeiro!
    pause
    exit /b 1
)

REM Inicia API em novo terminal
echo [1/2] Iniciando API na porta 8000...
start "API Diagnostico" cmd /k "cd /d "%API_DIR%" && "%VENV%\Scripts\python.exe" -m uvicorn api_biomedicina:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 3 /nobreak

REM Inicia Chatbot em novo terminal  
echo [2/2] Iniciando Chatbot Streamlit na porta 8501...
start "Chatbot Streamlit" cmd /k "cd /d "%CHATBOT_DIR%" && "%VENV%\Scripts\python.exe" -m streamlit run chatbot_clinica.py"

echo.
echo ========================================================
echo.
echo  ✅ SERVICOS INICIADOS!
echo.
echo  Acesso Chatbot:     http://localhost:8501
echo  API Docs:           http://localhost:8000/docs
echo.
echo  Feche os terminais para parar os servicos
echo.
echo ========================================================
echo.

pause
