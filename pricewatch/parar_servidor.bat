@echo off
chcp 65001 >nul
echo Parando PriceWatch...
taskkill /f /im python.exe /fi "WINDOWTITLE eq PriceWatch*" >nul 2>&1
taskkill /f /fi "IMAGENAME eq python.exe" >nul 2>&1
echo PriceWatch parado com sucesso.
pause
