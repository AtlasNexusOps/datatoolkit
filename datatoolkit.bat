@echo off
REM Atlas Data Toolkit — Windows Launcher
REM Just double-click or run: datatoolkit.bat convert data.csv -o data.json
python %~dp0datatoolkit-portable.py %*
