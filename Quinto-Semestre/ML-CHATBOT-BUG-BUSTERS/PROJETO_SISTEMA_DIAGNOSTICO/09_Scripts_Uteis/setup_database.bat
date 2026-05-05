@echo off
REM ===========================================================================
REM  SCRIPT PARA INICIALIZAR O BANCO DE DADOS — WINDOWS
REM ===========================================================================
REM  Projeto  : Sistema de Diagnóstico Clínico
REM  Arquivo  : setup_database.bat
REM  Função   : Criar banco SQLite clinica.db e importar dados
REM
REM  Como usar:
REM      1. Navegue até PROJETO_SISTEMA_DIAGNOSTICO\
REM      2. Execute: setup_database.bat
REM      ou
REM      3. Dê dois cliques no arquivo
REM ===========================================================================

setlocal enabledelayedexpansion

REM Obter diretório do script
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."

cd /d "%PROJECT_ROOT%"

echo ============================================================================
echo  INICIALIZADOR DE BANCO DE DADOS — SISTEMA CLINICO
echo ============================================================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python nao encontrado no PATH!
    echo Por favor, instale Python ou adicione ao PATH do sistema.
    pause
    exit /b 1
)

echo [INFO] Iniciando criacao do banco de dados...
echo.

REM Executar script Python
python "10_Banco_Dados\criar_banco_dados.py"

if errorlevel 1 (
    echo.
    echo ERROR: Falha ao criar banco de dados!
    pause
    exit /b 1
)

echo.
echo ============================================================================
echo  BANCO DE DADOS CRIADO COM SUCESSO!
echo ============================================================================
echo.
echo Proximos passos:
echo   1. Execute: run_pipeline.bat (para treinar modelo)
echo   2. Execute: run_ui.bat (para iniciar interface)
echo.
pause
