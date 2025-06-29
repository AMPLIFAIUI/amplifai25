@echo off
REM Run the Amplifai web UI using the embedded Python 3.10.11
SET "PYTHON_EXE=%~dp0python_embedded\python.exe"
IF NOT EXIST "%PYTHON_EXE%" (
    echo Embedded Python not found at %PYTHON_EXE%
    exit /b 1
)
"%PYTHON_EXE%" Amplifai\webui_sandbox.py
