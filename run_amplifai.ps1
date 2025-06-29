# PowerShell script to start the Amplifai .bat launcher
$batFile = Join-Path $PSScriptRoot 'run_amplifai.bat'
if (Test-Path $batFile) {
    Write-Host "Starting Amplifai using $batFile..."
    Start-Process -FilePath $batFile -WorkingDirectory $PSScriptRoot
} else {
    Write-Error "Could not find run_amplifai.bat in $PSScriptRoot"
}
