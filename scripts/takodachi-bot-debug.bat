@echo off & title Takodachi Bot Debug
cd /d "%~dp0\.."
".venv\Scripts\python.exe" "src\takodachi-bot\takodachi.pyw"
pause
exit