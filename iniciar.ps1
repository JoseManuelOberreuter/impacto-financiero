# Levanta todo Impacto Financiero en local:
#   - la API (impacto-api) en una ventana nueva de PowerShell, en http://localhost:8000
#   - la app web (impacto-app) en esta misma terminal, en http://localhost:8081
# La primera vez instala lo que falte (entorno de Python y dependencias de Node).

$ErrorActionPreference = 'Stop'
$raiz = $PSScriptRoot
$api = Join-Path $raiz 'impacto-api'
$app = Join-Path $raiz 'impacto-app'
$python = Join-Path $api '.venv\Scripts\python.exe'

# Primera vez: entorno de Python de la API
if (-not (Test-Path $python)) {
    Write-Host 'Creando el entorno de Python de la API (solo la primera vez)...' -ForegroundColor Cyan
    python -m venv (Join-Path $api '.venv')
    & $python -m pip install -r (Join-Path $api 'requirements-dev.txt')
}

# Primera vez: dependencias de la app
if (-not (Test-Path (Join-Path $app 'node_modules'))) {
    Write-Host 'Instalando las dependencias de la app (solo la primera vez)...' -ForegroundColor Cyan
    npm --prefix $app install
}

# API en una ventana nueva. CACHE_SEGUNDOS=0 para que los cambios se vean al recargar.
$comandoApi = "`$env:CACHE_SEGUNDOS='0'; Set-Location '$api'; " +
    "& '$python' -m uvicorn app.main:app --reload --port 8000"
Start-Process powershell -ArgumentList '-NoExit', '-Command', $comandoApi

Write-Host ''
Write-Host 'API:  http://localhost:8000  (en la ventana nueva; docs en /docs)' -ForegroundColor Green
Write-Host 'App:  http://localhost:8081  (en esta terminal)' -ForegroundColor Green
Write-Host 'Para detener: Ctrl + C en cada ventana.' -ForegroundColor DarkGray
Write-Host ''

# App web en esta terminal
Set-Location $app
npm run web
