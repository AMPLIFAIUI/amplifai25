# AMPLIFAI UI Customization

This repository contains the implementation of the AMPLIFAI UI customization feature that allows users to customize the website interface through natural language prompts.

## Features

- Customization bar that appears at the top of the page
- Natural language prompt processing
- Theme customization (dark/light modes)
- Font size adjustments
- Layout modifications
- History tracking of customization changes
- User preference storage
- Sandboxed code execution environment

## Easy Setup with Embedded Python

Amplifai comes with scripts to set up a dedicated Python environment in the project folder, so users don't need to install Python separately.

### Windows Setup

1. Run `setup_embedded_python.ps1` from PowerShell:
   ```
   .\setup_embedded_python.ps1
   ```

2. This will:
   - Download and extract Python 3.10.11 to the `python_embedded` folder
   - Install all required dependencies
   - Create helper scripts to use this Python installation

3. To run Amplifai with the embedded Python:
   ```
   .\run_amplifai.bat
   ```

4. To activate the embedded Python environment for development:
   ```
   .\activate_python.ps1
   ```

### Linux/macOS Setup

1. Run `setup_embedded_python.sh`:
   ```
   chmod +x setup_embedded_python.sh
   ./setup_embedded_python.sh
   ```

2. This will:
   - Create a Python virtual environment in the `python_env` folder
   - Install all required dependencies
   - Create helper scripts to use this environment

3. To run Amplifai with the embedded Python:
   ```
   ./run_amplifai.sh
   ```

4. To activate the Python environment for development:
   ```
   source ./activate_python.sh
   ```

## Implementation Files

- `index.html`: Main HTML file for standalone implementation
- `ui-customization.js`: JavaScript functionality
- `ui-customization.css`: CSS styling
- `announcement-bar-code.html`: HTML structure for implementation
- `Amplifai/app/sandbox/`: Sandbox implementation for secure code execution
- `Amplifai/tests/`: Test suite to verify functionality

## Manual Setup

If you prefer to use your own Python installation:

1. Ensure Python 3.10+ is installed
2. Install dependencies:
   ```
   pip install -r Amplifai/requirements.txt
   ```
3. Run the application:
   ```
   python Amplifai/main.py
   ```

## Testing

To run the test suite with the embedded Python:

1. Activate the Python environment:
   ```
   # Windows
   .\activate_python.ps1
   
   # Linux/macOS
   source ./activate_python.sh
   ```

2. Run the tests:
   ```
   python -m pytest Amplifai/tests/
   ```
- `inline-announcement-bar-code.js`: Complete code for Squarespace implementation

## Usage

This implementation can be:
1. Used as a standalone page
2. Embedded in a Squarespace site via a custom section
3. Linked from a Squarespace site

## Integration with Squarespace

To integrate with Squarespace:
1. Host this repository on GitHub Pages
2. Link to the GitHub Pages URL from your Squarespace site
3. Alternatively, embed the GitHub Pages URL in an iframe on your Squarespace site

## Development

This is a private repository for AMPLIFAI UI customization development.
