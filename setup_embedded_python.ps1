# Download and set up embedded Python for Amplifai
# This script downloads and sets up a portable Python installation in the project directory

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"  # Speeds up downloads

# Configuration
$pythonVersion = "3.10.11"
$pythonDir = "python_embedded"
$pythonArchive = "python-$pythonVersion-embed-amd64.zip"
$pythonUrl = "https://www.python.org/ftp/python/$pythonVersion/$pythonArchive"
$getPipUrl = "https://bootstrap.pypa.io/get-pip.py"

Write-Host "Setting up embedded Python $pythonVersion for Amplifai..."

# Create python directory if it doesn't exist
if (-not (Test-Path $pythonDir)) {
    New-Item -ItemType Directory -Path $pythonDir | Out-Null
    Write-Host "Created directory: $pythonDir"
}

# Download Python embeddable package if it doesn't exist
$pythonZipPath = Join-Path $pythonDir $pythonArchive
if (-not (Test-Path $pythonZipPath)) {
    Write-Host "Downloading Python $pythonVersion embeddable package..."
    Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonZipPath
    Write-Host "Downloaded Python embeddable package to $pythonZipPath"
}

# Extract Python if not already extracted
$pythonExePath = Join-Path $pythonDir "python.exe"
if (-not (Test-Path $pythonExePath)) {
    Write-Host "Extracting Python embeddable package..."
    Expand-Archive -Path $pythonZipPath -DestinationPath $pythonDir -Force
    Write-Host "Extracted Python to $pythonDir"
}

# Modify python*._pth file to enable site-packages
$pthFile = Get-ChildItem -Path $pythonDir -Filter "python*._pth" | Select-Object -First 1
if ($pthFile) {
    $pthPath = $pthFile.FullName
    $pthContent = Get-Content -Path $pthPath
    $newContent = $pthContent -replace '#import site', 'import site'
    Set-Content -Path $pthPath -Value $newContent
    Write-Host "Enabled import site in $($pthFile.Name)"
}

# Download and install pip if not already installed
$pipPath = Join-Path $pythonDir "Scripts\pip.exe"
if (-not (Test-Path $pipPath)) {
    Write-Host "Setting up pip..."
    $getPipPath = Join-Path $pythonDir "get-pip.py"
    Invoke-WebRequest -Uri $getPipUrl -OutFile $getPipPath
    & "$pythonExePath" "$getPipPath" --no-warn-script-location
    Remove-Item -Path $getPipPath
    Write-Host "Pip has been installed"
    
    # Upgrade pip and install setuptools and scikit-build-core
    Write-Host "Upgrading pip and installing build dependencies..."
    & "$pythonDir\python.exe" -m pip install --upgrade pip setuptools scikit-build-core wheel
    Write-Host "Build dependencies installed."
}

# Install required packages
Write-Host "Installing required packages..."
$requirementsPath = "Amplifai\requirements.txt"
if (Test-Path $requirementsPath) {
    & "$pythonDir\python.exe" -m pip install -r $requirementsPath
    Write-Host "Installed packages from $requirementsPath"
} else {
    Write-Host "Warning: $requirementsPath not found. Skipping package installation."
}

# Create activation scripts

# PowerShell activation script
$activatePsContent = @"
# PowerShell script to activate the embedded Python environment
`$env:PATH = "`$PSScriptRoot\$pythonDir;`$env:PATH"
Write-Host "Amplifai Python environment activated. You can now run 'python' commands using the embedded Python $pythonVersion."
"@
Set-Content -Path "activate_python.ps1" -Value $activatePsContent
Write-Host "Created PowerShell activation script: activate_python.ps1"

# Batch activation script
$activateBatContent = @"
@echo off
SET PATH=%~dp0$pythonDir;%PATH%
echo Amplifai Python environment activated. You can now run 'python' commands using the embedded Python $pythonVersion.
"@
Set-Content -Path "activate_python.bat" -Value $activateBatContent -Encoding ASCII
Write-Host "Created batch activation script: activate_python.bat"

# Create run script for Amplifai
$runContent = @"
@echo off
SET PATH=%~dp0$pythonDir;%~dp0$pythonDir\Scripts;%PATH%
echo Running Amplifai with embedded Python $pythonVersion...
python.exe %~dp0Amplifai\main.py %*
"@
Set-Content -Path "run_amplifai.bat" -Value $runContent -Encoding ASCII
Write-Host "Created Amplifai run script: run_amplifai.bat"

Write-Host "Embedded Python setup completed successfully!"
Write-Host "To use this Python installation with Amplifai, run 'run_amplifai.bat' or activate the environment with 'activate_python.ps1'"
