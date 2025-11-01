<#
install_mkcert.ps1

This PowerShell script attempts to install Chocolatey (optional) and mkcert on Windows,
then runs `mkcert -install` to add the CA to your system trust store.

USAGE (Run as Administrator):
  1. Open PowerShell as Administrator
  2. cd to the project folder (where this script lives)
  3. .\install_mkcert.ps1

NOTES:
- Installing Chocolatey requires an interactive elevated PowerShell session.
- This script will NOT run in this environment for you. You must run it locally.
- The script is defensive: it will skip installing Chocolatey if already present.
- If you prefer to install mkcert manually, follow https://mkcert.dev/
#>

param(
    [switch]$InstallChocolatey
)

function Is-Administrator {
    $current = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($current)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

if (-not (Is-Administrator)) {
    Write-Warning "This script must be run as Administrator. Right-click PowerShell -> Run as Administrator. Exiting."
    exit 1
}

Write-Host "Checking for mkcert..." -ForegroundColor Cyan
$mkcert = Get-Command mkcert -ErrorAction SilentlyContinue
if ($mkcert) {
    Write-Host "mkcert is already installed at: $($mkcert.Path)" -ForegroundColor Green
} else {
    if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
        if ($InstallChocolatey) {
            Write-Host "Chocolatey not found. Installing Chocolatey..." -ForegroundColor Yellow
            Set-ExecutionPolicy Bypass -Scope Process -Force
            [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
            Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
            if ($LASTEXITCODE -ne 0) {
                Write-Error "Chocolatey install failed. Please install Chocolatey manually and re-run this script."
                exit 1
            }
        } else {
            Write-Host "Chocolatey not found. You can re-run this script with -InstallChocolatey to install it automatically, or install mkcert manually from https://mkcert.dev/." -ForegroundColor Yellow
            exit 1
        }
    }

    Write-Host "Installing mkcert via Chocolatey..." -ForegroundColor Cyan
    choco install mkcert -y
    if ($LASTEXITCODE -ne 0) {
        Write-Error "mkcert install failed via Chocolatey. Please install manually: https://mkcert.dev/"
        exit 1
    }
}

Write-Host "Running 'mkcert -install' to add CA to trust store..." -ForegroundColor Cyan
mkcert -install
if ($LASTEXITCODE -ne 0) {
    Write-Error "mkcert -install failed. You may need to run this command manually and accept prompts."
    exit 1
}

Write-Host "mkcert installed and CA installed into trust store." -ForegroundColor Green
Write-Host "You can now run the helper script: .\run_https_dev.ps1 or run_https_dev.bat to generate dev combined PEM and start runserver_plus." -ForegroundColor Green
