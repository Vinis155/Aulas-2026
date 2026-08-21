@echo off
REM ========================================================
REM SCRIPT PARA RODAR CHATBOT GEMINI - CLINICA BIOMEDICINA
REM ========================================================

setlocal enabledelayedexpansion

echo.
echo ========================================================
echo.
echo  CHATBOT COM IA GEMINI - CLINICA DE BIOMEDICINA
echo.
echo  Iniciando servicos...
echo.
echo  - API Diagnostico (porta 8000)
echo  - Chatbot Gemini (porta 8501)
echo.
echo ========================================================
echo.

REM Verificar .env
set ENV_FILE=..\..\.env

if not exist "%ENV_FILE%" (
    echo.
    echo AVISO: Arquivo .env nao encontrado!
    echo.
    echo Voce precisa configurar a chave GEMINI_API_KEY antes de continuar.
    echo.
    echo Instrucoes:
    echo 1. Acesse: https://aistudio.google.com/app/apikey
    echo 2. Clique em "Create API Key"
    echo 3. Copie a chave gerada
    echo 4. Crie arquivo .env na raiz do projeto (ML-CHATBOT-BUG-BUSTERS\)
    echo 5. Cole isso no arquivo .env:
    echo    GEMINI_API_KEY=sua_chave_aqui
    echo.
    echo Exemplos de chaves:
    echo    AIzaSyD1234567890abcdefghijklmnopqrstuvwxyz
    echo    AIzaSyDexamplekeyforgeminiapi123456789
    echo.
    pause
    exit /b 1
)

echo [OK] Arquivo .env encontrado

REM Diretorio base
set BASE_DIR=%~dp0..
set API_DIR=%BASE_DIR%\03_API
set CHATBOT_DIR=%BASE_DIR%\04_Interface
set VENV=%BASE_DIR%\..\..\.venv

REM Verificar venv
if not exist "%VENV%\Scripts\python.exe" (
    echo ERROR: Virtual environment nao encontrado em %VENV%
    pause
    exit /b 1
)

echo.
echo [1/2] Iniciando API na porta 8000...
start "API Diagnostico" cmd /k "cd /d "%API_DIR%" && "%VENV%\Scripts\python.exe" -m uvicorn api_biomedicina:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 4 /nobreak

echo.
echo [2/2] Iniciando Chatbot Gemini na porta 8501...
start "Chatbot Gemini IA" cmd /k "cd /d "%CHATBOT_DIR%" && "%VENV%\Scripts\python.exe" -m streamlit run chatbot_clinica_gemini.py"

echo.
echo ========================================================
echo.
echo  ✅ SERVICOS INICIADOS!
echo.
echo  Abra seu navegador em:
echo  🤖 Chatbot Gemini: http://localhost:8501
echo  📚 API Docs:       http://localhost:8000/docs
echo.
echo ========================================================
echo.

pause
