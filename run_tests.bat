@echo off
REM This script runs Amplifai tests using the embedded Python installation

echo Running Amplifai tests with embedded Python...

REM Set up environment variables
SET SCRIPT_DIR=%~dp0
SET PYTHON_DIR=%SCRIPT_DIR%python_embedded
SET PATH=%PYTHON_DIR%;%PYTHON_DIR%\Scripts;%PATH%

REM Check if embedded Python exists
IF NOT EXIST "%PYTHON_DIR%\python.exe" (
    echo Embedded Python not found. Running setup script...
    powershell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%setup_embedded_python.ps1"
)

REM Run specified test or all tests
IF "%~1"=="" (
    echo Running all Amplifai tests...
    "%PYTHON_DIR%\python.exe" -m pytest "%SCRIPT_DIR%Amplifai\tests"
) ELSE (
    echo Running specified test: %*
    "%PYTHON_DIR%\python.exe" -m pytest %*
)

echo Test execution completed.
