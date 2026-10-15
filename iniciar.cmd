@echo off
rem Atajo para iniciar.ps1 sin cambiar la política de ejecución de PowerShell.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0iniciar.ps1"
