<#
run_https_dev.ps1 — PowerShell helper to generate mkcert certs and run manage.py runserver_plus
Usage: Open PowerShell in project root and run: .\run_https_dev.ps1
Requires: mkcert installed and django-extensions + pyOpenSSL in venv
#>

param(
    [string]$Host = "127.0.0.1",
    [string]$Port = "8000",
    [string]$CertFile = "devcert.pem",
    [string]$KeyFile = "devkey.pem",
    [string]$Combined = "devcombined.pem"
)

Set-Location -Path $PSScriptRoot

Write-Host "Checking for mkcert..." -ForegroundColor Cyan
$mkcert = Get-Command mkcert -ErrorAction SilentlyContinue
if (-not $mkcert) {
    Write-Host "mkcert not found. Please install mkcert: https://mkcert.dev/" -ForegroundColor Yellow
    Write-Host "If you use Chocolatey, run as Admin: choco install mkcert; mkcert -install" -ForegroundColor Yellow
    exit 1
}

Write-Host "Generating certificate ($CertFile) and key ($KeyFile)..." -ForegroundColor Cyan
& mkcert -key-file $KeyFile -cert-file $CertFile $Host localhost ::1
if ($LASTEXITCODE -ne 0) {
    Write-Host "mkcert failed. See output above." -ForegroundColor Red
    exit 1
}

Write-Host "Combining key+cert into $Combined ..." -ForegroundColor Cyan
Get-Content $KeyFile, $CertFile | Out-File -Encoding ascii -FilePath $Combined -Force

Write-Host "Activating virtualenv (if present)..." -ForegroundColor Cyan
$activate = Join-Path $PSScriptRoot "venv\Scripts\Activate.ps1"
if (Test-Path $activate) {
    & $activate
} else {
    Write-Host "Virtualenv activation script not found at $activate. Activate manually if needed." -ForegroundColor Yellow
}

Write-Host "Starting runserver_plus on https://$Host:$Port ..." -ForegroundColor Green
python manage.py runserver_plus $Host:$Port --cert-file $Combined

Write-Host "Server stopped. You can remove generated cert files if desired." -ForegroundColor Cyan