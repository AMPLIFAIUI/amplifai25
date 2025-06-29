@echo off
REM AMPLIFAI SYSTEM LAUNCHER FOR WINDOWS
REM Starts the world's most powerful AI system

echo.
echo ================================================================
echo               AMPLIFAI - WORLD'S MOST POWERFUL AI
echo ================================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if pip dependencies are installed
echo Checking Python dependencies...
python -c "import fastapi, uvicorn, llama_cpp, websockets, aiofiles" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Create logs directory if it doesn't exist
if not exist "logs" mkdir logs

echo.
echo Starting Amplifai Master System...
echo.

REM Start the master system
python amplifai_master.py

REM If we get here, the system has stopped
echo.
echo Amplifai system has stopped.
pause
