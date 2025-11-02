@echo off
cd /d %~dp0

setlocal

set /p "LETTER=Enter drive letter of mounted VHD: "
if "%LETTER%"=="" goto :eof

call :get_volname %LETTER%
if "%OUTPUT%"=="" goto :eof

REM Get the last token
for %%A in (%OUTPUT%) do set VOLNAME=%%A

oscdimg -j2 -o -m %LETTER%:\ "%VOLNAME%.iso"

goto :eof

:get_volname
set cmd=vol %1:
for /F "usebackq tokens=*" %%a in (`%cmd%`) do (
	set OUTPUT=%%a
	goto :eof
)
