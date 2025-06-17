@echo off
setlocal EnableDelayedExpansion
cd /d %~dp0

:: config
set APP_NAME=simple-offline-viewer
set APP_ICON=app.ico

:: cleanup
rmdir /s /q "dist\%APP_NAME%" 2>nul
del "dist\%APP_NAME%-standalone-windows-x64.zip" 2>nul

echo.
echo ****************************************
echo Running pyinstaller...
echo ****************************************

pyinstaller --noupx -w -i "%APP_ICON%" -n "%APP_NAME%" -D main.py --exclude-module PyQt5 --exclude-module PyQt6 --exclude-module tornado

echo.
echo ****************************************
echo Copying resources...
echo ****************************************

xcopy /e resources "dist\%APP_NAME%\_internal\resources\" >nul

echo.
echo ****************************************
echo Optimizing dist folder...
echo ****************************************

del "dist\%APP_NAME%\_internal\api-ms-win-*.dll"

echo.
echo ****************************************
echo Creating ZIP...
echo ****************************************

cd dist
del "%APP_NAME%-standalone-windows-x64.zip" 2>nul
zip -q -r "%APP_NAME%-standalone-windows-x64.zip" "%APP_NAME%"
cd ..

echo.
pause
