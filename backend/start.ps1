$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

Write-Host "Starting ScribeIt Backend..." -ForegroundColor Green
uvicorn main:app --host 0.0.0.0 --port 8000 --reload 