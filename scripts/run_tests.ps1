$ErrorActionPreference = "Stop"

Write-Host "Running unit tests..."
& "C:/Program Files/Python313/python.exe" -m pytest -q
