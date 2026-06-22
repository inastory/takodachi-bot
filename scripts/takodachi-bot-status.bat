@echo off & title Takodachi Bot Status
cd /d "%~dp0\.."
".venv\Scripts\python.exe" "src\takodachi-bot\helper.py" "STATUS"
pause
exit