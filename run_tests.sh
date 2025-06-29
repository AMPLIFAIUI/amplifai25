#!/bin/bash
# This script runs Amplifai tests using the embedded Python installation

echo "Running Amplifai tests with embedded Python..."

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

# Run specified test or all tests
if [ -z "$1" ]; then
    echo "Running all Amplifai tests..."
    python -m pytest "$SCRIPT_DIR/Amplifai/tests"
else
    echo "Running specified test: $@"
    python -m pytest "$@"
fi

# Deactivate the Python environment
deactivate

echo "Test execution completed."
