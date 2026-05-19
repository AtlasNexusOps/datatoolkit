@echo off
REM Atlas Data Toolkit — Windows Installer
REM Run: install.bat
REM Or: curl -sL URL | cmd

echo Atlas Data Toolkit - Windows Installer
echo =======================================

set INSTALL_DIR=%USERPROFILE%\.datatoolkit
mkdir "%INSTALL_DIR%" 2>nul

echo Downloading datatoolkit...
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/AtlasNexusTech/datatoolkit/master/datatoolkit-portable.py' -OutFile '%INSTALL_DIR%\datatoolkit.py'"
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/AtlasNexusTech/datatoolkit/master/vendor/xmltodict.py' -OutFile '%INSTALL_DIR%\xmltodict.py'"

REM Create launcher
echo @echo off > "%INSTALL_DIR%\dtk.bat"
echo python "%INSTALL_DIR%\datatoolkit.py" %%* >> "%INSTALL_DIR%\dtk.bat"

REM Add to PATH
setx PATH "%PATH%;%INSTALL_DIR%" 2>nul

echo.
echo Installed to %INSTALL_DIR%
echo.
echo Usage:
echo   dtk convert data.csv -o data.json
echo   dtk validate data.csv
echo.
echo (Restart terminal or run: refreshenv)
