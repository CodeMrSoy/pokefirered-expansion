@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -STA -Command "& ([scriptblock]::Create([IO.File]::ReadAllText((Join-Path (Get-Location) 'launcher-windows.ps1'))))"
if errorlevel 1 pause
