#!/bin/bash
# This script runs Amplifai using the embedded Python installation

echo "Starting Amplifai with embedded Python..."

# Set up environment variables
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_DIR="$SCRIPT_DIR/python_env/amplifai_env"

# Check if embedded Python exists
if [ ! -d "$PYTHON_DIR" ]; then
    echo "Embedded Python not found. Running setup script..."
    bash "$SCRIPT_DIR/setup_embedded_python.sh"
fi

# Activate the Python environment
source "$PYTHON_DIR/bin/activate"

# Run Amplifai main script
echo "Running Amplifai..."
python "$SCRIPT_DIR/Amplifai/main.py" "$@"

# Deactivate the Python environment
deactivate

echo "Amplifai execution completed."
