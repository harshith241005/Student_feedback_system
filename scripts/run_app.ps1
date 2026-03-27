$ErrorActionPreference = "Stop"

if (!(Test-Path "data")) {
    New-Item -ItemType Directory -Path "data" | Out-Null
}

Write-Host "Starting Flask app on http://localhost:5000"
& "C:/Program Files/Python313/python.exe" app/app.py
