@echo off
REM Sobe o Steam Game Filter no Windows: cria o venv na primeira vez e abre o navegador.
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Criando ambiente virtual...
    python -m venv .venv || goto :erro
    ".venv\Scripts\python.exe" -m pip install --upgrade pip >nul
    echo Instalando dependencias...
    ".venv\Scripts\pip.exe" install -r requirements.txt || goto :erro
)

".venv\Scripts\python.exe" -m steam_filter serve %*
goto :fim

:erro
echo.
echo Falhou. Confira se o Python 3.10+ esta instalado e no PATH.
pause

:fim
endlocal
