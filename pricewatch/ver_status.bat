@echo off
chcp 65001 >nul
echo ================================================
echo   PriceWatch — Status do Sistema
echo ================================================
echo.
tasklist | findstr python.exe >nul
if %errorlevel% == 0 (
    echo STATUS: RODANDO
    echo O servidor esta ativo e monitorando.
) else (
    echo STATUS: PARADO
    echo Execute instalar_automatico.bat para iniciar.
)
echo.
echo Tarefa agendada:
schtasks /query /tn "PriceWatch Musical Presentes" 2>nul | findstr "Status"
echo.
pause
