@echo off
setlocal
set "PACKAGE=%~dp0"
set "DATA=%LOCALAPPDATA%\Zelda ALttP"
if not exist "%DATA%" mkdir "%DATA%"
if not exist "%DATA%\zelda3_assets.dat" (
  echo Missing game assets. Follow README.md to extract your own ROM first.
  pause
  exit /b 1
)
if not exist "%DATA%\zelda3.ini" copy "%PACKAGE%zelda3.ini" "%DATA%\zelda3.ini" >nul
cd /d "%DATA%"
"%PACKAGE%zelda3.exe" --config "%DATA%\zelda3.ini"
if errorlevel 1 pause
