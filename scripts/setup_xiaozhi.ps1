$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot

$env:UV_CACHE_DIR = Join-Path $Root ".uv-cache"
$env:UV_PYTHON_INSTALL_DIR = Join-Path $Root ".uv-python"

Push-Location $Root
try {
    uv sync --extra gui --python 3.12
} finally {
    Pop-Location
}
