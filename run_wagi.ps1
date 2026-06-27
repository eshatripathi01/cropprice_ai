# Run WAGI Server for Crop Price Predictor Web Application
# This script automates downloading the required binaries (WAGI and python.wasm)
# and starts the sandboxed server locally.

$ErrorActionPreference = "Stop"

# Force TLS 1.2 for network requests in PowerShell
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# Robust Download Helper that prefers curl.exe (more reliable for large downloads on Windows)
function Download-File {
    param (
        [string]$Url,
        [string]$OutFile
    )
    
    if (Get-Command "curl.exe" -ErrorAction SilentlyContinue) {
        Write-Host "Using curl.exe to download..." -ForegroundColor Gray
        # Use -L to follow redirects, -S for silent-but-show-errors
        curl.exe -L -o $OutFile $Url
    } else {
        Write-Host "Using Invoke-WebRequest..." -ForegroundColor Gray
        Invoke-WebRequest -Uri $Url -OutFile $OutFile
    }
}

# 1. Download WAGI binary if it doesn't exist
if (-not (Test-Path "wagi.exe")) {
    Write-Host "Downloading WAGI server (v0.8.1)..." -ForegroundColor Cyan
    $wagiUrl = "https://github.com/deislabs/wagi/releases/download/v0.8.1/wagi-v0.8.1-windows-amd64.tar.gz"
    $archiveName = "wagi.tar.gz"
    
    Download-File -Url $wagiUrl -OutFile $archiveName
    
    Write-Host "Extracting WAGI server..." -ForegroundColor Cyan
    # Windows 10/11 has tar built-in
    tar -zxf $archiveName wagi.exe
    
    # Cleanup
    if (Test-Path $archiveName) {
        Remove-Item $archiveName
    }
} else {
    Write-Host "WAGI server binary (wagi.exe) is already present." -ForegroundColor Green
}

# 2. Download python.wasm if it doesn't exist
if (-not (Test-Path "python.wasm")) {
    Write-Host "Downloading Python WebAssembly runtime (python.wasm) from VMware WLR..." -ForegroundColor Cyan
    # This is a precompiled, WASI-compliant Python WebAssembly binary
    $pythonUrl = "https://github.com/vmware-labs/webassembly-language-runtimes/releases/download/python%2F3.11.1%2B20230217-154df67/python-3.11.1.usr.bin.wasm"
    
    Download-File -Url $pythonUrl -OutFile "python.wasm"
    Write-Host "Python WebAssembly runtime downloaded." -ForegroundColor Green
} else {
    Write-Host "Python WASM runtime (python.wasm) is already present." -ForegroundColor Green
}

# 3. Start WAGI Server
Write-Host "`nStarting WAGI server on http://127.0.0.1:8080 ..." -ForegroundColor Magenta
Write-Host "Press Ctrl+C to stop the server.`n" -ForegroundColor Yellow

.\wagi.exe -c wagi-modules.toml --listen 127.0.0.1:8080
