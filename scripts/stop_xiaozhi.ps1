$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot

$matches = Get-CimInstance Win32_Process | Where-Object {
    $_.CommandLine -and
    $_.CommandLine.Contains($Root) -and
    $_.CommandLine -match "main\.py"
}

if (-not $matches) {
    Write-Host "No py-xiaozhi process found for: $Root"
    exit 0
}

foreach ($proc in $matches) {
    Write-Host "Stopping py-xiaozhi PID $($proc.ProcessId)"
    Stop-Process -Id $proc.ProcessId -Force
}
