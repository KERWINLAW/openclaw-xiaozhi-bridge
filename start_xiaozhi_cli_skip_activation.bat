@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\run_xiaozhi_cli.ps1" -SkipActivation
if errorlevel 1 (
  echo.
  echo py-xiaozhi exited with error code %errorlevel%.
  pause
)
