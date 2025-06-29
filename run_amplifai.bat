@echo off
SET PATH=%~dp0python_embedded;%~dp0python_embedded\Scripts;%PATH%
echo Running Amplifai with embedded Python 3.10.11...
python.exe %~dp0Amplifai\main.py %*
