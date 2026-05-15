$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$env:PYTHONIOENCODING = "utf-8"
$env:PY_XIAOZHI_DATA_DIR = Join-Path $Root ".runtime\data"

$Python = Join-Path $Root ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $Python)) {
    throw "Python environment not found: $Python. Run: .\scripts\setup_xiaozhi.ps1"
}

Push-Location $Root
try {
    & $Python ".\scripts\check_xiaozhi_setup.py"
} finally {
    Pop-Location
}
