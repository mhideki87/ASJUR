# Sobe o Steam Game Filter no Windows (PowerShell).
Set-Location -Path $PSScriptRoot

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Criando ambiente virtual..."
    python -m venv .venv
    & ".venv\Scripts\python.exe" -m pip install --upgrade pip | Out-Null
    Write-Host "Instalando dependencias..."
    & ".venv\Scripts\pip.exe" install -r requirements.txt
}

& ".venv\Scripts\python.exe" -m steam_filter serve @args
