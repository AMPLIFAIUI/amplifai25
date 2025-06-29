# PowerShell script to activate the embedded Python environment
$env:PATH = "$PSScriptRoot\python_embedded;$env:PATH"
Write-Host "Amplifai Python environment activated. You can now run 'python' commands using the embedded Python 3.10.11."
