param(
    [string]$RepoBase = "openclaw-xiaozhi-bridge",
    [string]$Description = "OpenClaw voice bridge built on py-xiaozhi with Xiaozhi MCP tools",
    [switch]$Public
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$OpenClawDir = Join-Path $env:USERPROFILE ".openclaw"
$TokenPattern = "(github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9_]{20,})"
$SafeDir = ($Root -replace "\\", "/")

Set-Location -LiteralPath $Root

if (-not (Get-Command rg -ErrorAction SilentlyContinue)) {
    throw "ripgrep (rg) is required to locate GitHub token candidates safely."
}

$tokenSet = New-Object "System.Collections.Generic.HashSet[string]"
$files = @(& rg -l --no-messages $TokenPattern $OpenClawDir 2>$null)
foreach ($file in $files) {
    try {
        $text = Get-Content -LiteralPath $file -Raw -ErrorAction Stop
        foreach ($match in [regex]::Matches($text, $TokenPattern)) {
            [void]$tokenSet.Add($match.Value)
        }
    } catch {
    }
}

if ($tokenSet.Count -eq 0) {
    throw "No GitHub token candidates were found in OpenClaw data."
}

$created = $null
$usedToken = $null
$owner = $null

foreach ($token in $tokenSet) {
    $headers = @{
        Authorization = "Bearer $token"
        Accept = "application/vnd.github+json"
        "X-GitHub-Api-Version" = "2022-11-28"
        "User-Agent" = "Codex-OpenClaw-Xiaozhi-Uploader"
    }

    try {
        $user = Invoke-RestMethod -Method Get -Uri "https://api.github.com/user" -Headers $headers -TimeoutSec 20
    } catch {
        continue
    }

    $owner = $user.login

    try {
        $existing = Invoke-RestMethod -Method Get -Uri "https://api.github.com/repos/$owner/$RepoBase" -Headers $headers -TimeoutSec 20
        $created = $existing
        $usedToken = $token
        break
    } catch {
    }

    for ($i = 0; $i -lt 8 -and -not $created; $i++) {
        $repoName = if ($i -eq 0) {
            $RepoBase
        } else {
            "$RepoBase-$((Get-Date).ToString('yyyyMMdd-HHmmss'))-$i"
        }

        $body = @{
            name = $repoName
            description = $Description
            private = -not [bool]$Public
            auto_init = $false
        } | ConvertTo-Json

        try {
            $created = Invoke-RestMethod -Method Post -Uri "https://api.github.com/user/repos" -Headers $headers -Body $body -ContentType "application/json" -TimeoutSec 30
            $usedToken = $token
            break
        } catch {
            $status = $null
            try {
                $status = $_.Exception.Response.StatusCode.value__
            } catch {
            }
            if ($status -eq 422) {
                continue
            }
            break
        }
    }

    if ($created) {
        break
    }
}

if (-not $created) {
    throw "Could not create a GitHub repository with the available token candidates."
}

git -c "safe.directory=$SafeDir" config user.name $owner
git -c "safe.directory=$SafeDir" config user.email "$owner@users.noreply.github.com"

git -c "safe.directory=$SafeDir" add -A

$staged = git -c "safe.directory=$SafeDir" diff --cached --name-only
if ($staged) {
    git -c "safe.directory=$SafeDir" commit -m "Add OpenClaw Xiaozhi voice bridge" | Out-Null
}

$remoteUrl = $created.clone_url
$remoteNames = @(git -c "safe.directory=$SafeDir" remote)
if ($remoteNames -contains "github") {
    git -c "safe.directory=$SafeDir" remote set-url github $remoteUrl
} else {
    git -c "safe.directory=$SafeDir" remote add github $remoteUrl
}

$basicToken = [Convert]::ToBase64String(
    [Text.Encoding]::ASCII.GetBytes("x-access-token:$usedToken")
)
$authHeader = "AUTHORIZATION: Basic $basicToken"
git -c "safe.directory=$SafeDir" -c "http.https://github.com/.extraheader=$authHeader" push -u github main
if ($LASTEXITCODE -ne 0) {
    throw "Git push failed."
}

Write-Host "Created and pushed:"
Write-Host $created.html_url
