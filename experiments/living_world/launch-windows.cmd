@echo off
setlocal
cd /d "%~dp0"
"python\python.exe" -B "play.py" %*
if errorlevel 1 pause
