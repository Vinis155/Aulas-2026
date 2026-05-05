@echo off
REM ============================================================================
REM SCRIPT: run_all.bat
REM Executa TODA a pipeline do sistema
REM Abre: Dataset -> Pipeline -> API -> Streamlit (4 terminais)
REM ============================================================================

setlocal enabledelayedexpansion
set "BASE_DIR=%~dp0.."

echo.
echo ============================================================================
echo   SISTEMA DE DIAGNOSTICO DE RISCO CLINICO
echo   Iniciando Pipeline Completa...
echo ============================================================================
echo.

REM 1. GERAR DATASET
echo [1/4] Abrindo gerador de dataset...
start cmd /k "cd /d ""%BASE_DIR%\01_Dataset"" && python 1_gerar_dataset.py && pause"
timeout /t 10 /nobreak

REM 2. TREINAR MODELOS
echo [2/4] Abrindo pipeline de ML (espere ~30s)...
start cmd /k "cd /d ""%BASE_DIR%\02_ML_Pipeline"" && python 2_pipeline_ml.py && pause"
timeout /t 35 /nobreak

REM 3. INICIAR API
echo [3/4] Iniciando API (port 8000)...
start cmd /k "cd /d ""%BASE_DIR%\03_API"" && uvicorn api_biomedicina:app --port 8000"
timeout /t 5 /nobreak

REM 4. INICIAR STREAMLIT
echo [4/4] Iniciando Streamlit (port 8501)...
start cmd /k "cd /d ""%BASE_DIR%\04_Interface"" && streamlit run interface_streamlit.py"

echo.
echo ============================================================================
echo   PIPELINE INICIADA COM SUCESSO!
echo.
echo   API:       http://localhost:8000
echo   Swagger:   http://localhost:8000/docs
echo   Streamlit: http://localhost:8501
echo.
echo   Para parar, feche os terminais ou pressione CTRL+C
echo ============================================================================
echo.

pause
