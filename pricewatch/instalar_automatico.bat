@echo off
chcp 65001 >nul
echo.
echo ================================================
echo   PriceWatch — Instalacao Automatica
echo   Musical Presentes · Ipatinga, MG
echo ================================================
echo.

:: Pega o caminho atual
set "PASTA=%~dp0"
set "PASTA=%PASTA:~0,-1%"
set "PYTHON=%LOCALAPPDATA%\Programs\Python\Python314\python.exe"
set "SERVIDOR=%PASTA%\backend\server.py"
set "TASK_NAME=PriceWatch Musical Presentes"

echo Pasta do sistema: %PASTA%
echo.

:: Verifica se Python existe
if not exist "%PYTHON%" (
    :: Tenta Python no PATH
    for /f "delims=" %%i in ('where python 2^>nul') do set "PYTHON=%%i"
)

echo Python encontrado: %PYTHON%
echo.

:: Remove tarefa antiga se existir
schtasks /delete /tn "%TASK_NAME%" /f >nul 2>&1

:: Cria a tarefa no Agendador
echo Criando tarefa no Agendador do Windows...
schtasks /create ^
  /tn "%TASK_NAME%" ^
  /tr "\"%PYTHON%\" \"%SERVIDOR%\"" ^
  /sc ONLOGON ^
  /rl HIGHEST ^
  /f >nul

if %errorlevel% == 0 (
    echo.
    echo ================================================
    echo   SUCESSO! PriceWatch configurado!
    echo ================================================
    echo.
    echo O servidor vai iniciar automaticamente
    echo toda vez que o Windows ligar.
    echo.
    echo Iniciando agora pela primeira vez...
    start "" "%PYTHON%" "%SERVIDOR%"
    echo.
    echo Servidor iniciado! Verifique o Telegram.
) else (
    echo.
    echo ERRO ao criar tarefa. Tentando metodo alternativo...
    :: Metodo alternativo via startup folder
    set "STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
    echo @echo off > "%STARTUP%\pricewatch.bat"
    echo start "" "%PYTHON%" "%SERVIDOR%" >> "%STARTUP%\pricewatch.bat"
    echo.
    echo Configurado via pasta Startup do Windows!
    echo O PriceWatch vai iniciar automaticamente ao ligar o PC.
    start "" "%PYTHON%" "%SERVIDOR%"
)

echo.
echo Pressione qualquer tecla para fechar...
pause >nul
