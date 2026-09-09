@echo off
REM ---------------------------------------------------------------------------
REM Steam Game Filter — duplo clique neste arquivo para abrir o app.
REM Na primeira vez ele prepara o ambiente sozinho (demora ~1 min).
REM ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0"
title Steam Game Filter

REM --- acha o Python (py -3 primeiro: evita o atalho falso da Microsoft Store)
set "PY="
py -3 --version >nul 2>&1
if not errorlevel 1 set "PY=py -3"
if defined PY goto :temPython
python --version >nul 2>&1
if not errorlevel 1 set "PY=python"
:temPython
if not defined PY goto :semPython

REM --- primeira execucao: cria o ambiente e instala as dependencias
if exist ".venv\Scripts\python.exe" goto :rodar
echo.
echo   Primeira execucao: preparando o ambiente. Isso leva cerca de 1 minuto...
echo.
%PY% -m venv .venv
if errorlevel 1 goto :erroVenv
".venv\Scripts\python.exe" -m pip install --upgrade pip >nul 2>&1
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto :erroDeps
echo.
echo   Ambiente pronto.

:rodar
echo.
echo   Abrindo o app no navegador. Deixe esta janela aberta enquanto usar.
echo   Para fechar o app: clique nesta janela e aperte Ctrl+C.
echo.
".venv\Scripts\python.exe" -m steam_filter serve %*
if errorlevel 1 goto :erroApp
goto :fim

:semPython
echo.
echo   NAO ENCONTREI O PYTHON.
echo.
echo   Instale em https://www.python.org/downloads/  e marque a caixinha
echo   "Add python.exe to PATH" na primeira tela do instalador.
echo   Depois feche esta janela e clique de novo em run.bat.
echo.
pause
goto :fim

:erroVenv
echo.
echo   Falhou ao criar o ambiente virtual (.venv).
echo   Verifique se a pasta nao esta somente-leitura ou sincronizada pelo OneDrive.
echo.
pause
goto :fim

:erroDeps
echo.
echo   Falhou ao instalar as dependencias (precisa de internet).
echo   Apague a pasta .venv e rode o run.bat de novo.
echo.
pause
goto :fim

:erroApp
echo.
echo   O app parou com erro. Se a mensagem acima falar em "address already in use",
echo   o app ja esta aberto em outra janela ^(veja http://127.0.0.1:8777^).
echo.
pause

:fim
endlocal
