$ErrorActionPreference = "Stop"

Write-Host "Installing Python dependencies..."
& "C:/Program Files/Python313/python.exe" -m pip install -r app/requirements.txt

Write-Host "Python setup complete."
