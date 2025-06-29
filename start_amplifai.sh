#!/bin/bash
# AMPLIFAI SYSTEM LAUNCHER FOR UNIX/LINUX
# Starts the world's most powerful AI system

echo ""
echo "================================================================"
echo "               AMPLIFAI - WORLD'S MOST POWERFUL AI"
echo "================================================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

# Check if pip dependencies are installed
echo "Checking Python dependencies..."
python3 -c "import fastapi, uvicorn, llama_cpp, websockets, aiofiles" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing required dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
fi

# Create logs directory if it doesn't exist
mkdir -p logs

echo ""
echo "Starting Amplifai Master System..."
echo ""

# Start the master system
python3 amplifai_master.py

# If we get here, the system has stopped
echo ""
echo "Amplifai system has stopped."
