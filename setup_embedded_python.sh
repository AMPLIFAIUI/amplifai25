#!/bin/bash
# Download and set up embedded Python for Amplifai
# This script downloads and sets up a portable Python environment in the project directory

set -e

# Configuration
PYTHON_VERSION="3.10.11"
PYTHON_DIR="python_env"
VENV_NAME="amplifai_env"

echo "Setting up Python $PYTHON_VERSION environment for Amplifai..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 to continue."
    exit 1
fi

# Create python directory if it doesn't exist
if [ ! -d "$PYTHON_DIR" ]; then
    mkdir -p "$PYTHON_DIR"
    echo "Created directory: $PYTHON_DIR"
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$PYTHON_DIR/$VENV_NAME" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv "$PYTHON_DIR/$VENV_NAME"
    echo "Created virtual environment in $PYTHON_DIR/$VENV_NAME"
fi

# Activate virtual environment and install requirements
echo "Installing required packages..."
source "$PYTHON_DIR/$VENV_NAME/bin/activate"

# Check if requirements.txt exists
if [ -f "Amplifai/requirements.txt" ]; then
    pip install -r "Amplifai/requirements.txt"
    echo "Installed packages from Amplifai/requirements.txt"
else
    echo "Warning: Amplifai/requirements.txt not found. Skipping package installation."
fi

# Create activation script
ACTIVATE_SCRIPT="activate_python.sh"
cat > "$ACTIVATE_SCRIPT" << EOF
#!/bin/bash
# Script to activate the Python environment for Amplifai
source "\$(dirname "\$0")/$PYTHON_DIR/$VENV_NAME/bin/activate"
echo "Amplifai Python environment activated. You can now run Python commands."
EOF

chmod +x "$ACTIVATE_SCRIPT"
echo "Created activation script: $ACTIVATE_SCRIPT"

# Create run script for Amplifai
RUN_SCRIPT="run_amplifai.sh"
cat > "$RUN_SCRIPT" << EOF
#!/bin/bash
# Script to run Amplifai with the embedded Python environment
source "\$(dirname "\$0")/$PYTHON_DIR/$VENV_NAME/bin/activate"
echo "Running Amplifai with Python environment..."
python "\$(dirname "\$0")/Amplifai/main.py" "\$@"
EOF

chmod +x "$RUN_SCRIPT"
echo "Created Amplifai run script: $RUN_SCRIPT"

echo "Python environment setup completed successfully!"
echo "To use this Python installation with Amplifai, run './run_amplifai.sh' or activate the environment with 'source ./activate_python.sh'"

# Deactivate the virtual environment
deactivate
