<#
.SYNOPSIS
    Script de inicio para SCIPi v2.0 (CLI Python + Ansible en Docker).
.DESCRIPTION
    Verifica Docker, compila la imagen si es necesario, y abre la CLI interactiva.
    Para forzar recompilacion: .\inicio.ps1 -Rebuild
#>

param(
    [switch]$Rebuild
)

$ErrorActionPreference = "Stop"
$serviceName = "scipi"

Write-Host ""
Write-Host "  SCIPi v2.0 - Automatizacion IT" -ForegroundColor Cyan
Write-Host "  ================================" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar Docker
try {
    $null = docker --version 2>$null
    if ($LASTEXITCODE -ne 0) { throw }
    Write-Host "[+] Docker detectado" -ForegroundColor Green
}
catch {
    Write-Host "[-] Docker Desktop no esta instalado o no esta corriendo." -ForegroundColor Red
    exit 1
}

# 2. Compilar imagen si es necesario
$oldErrorAction = $ErrorActionPreference
$ErrorActionPreference = "Continue"
$imageExists = docker compose images -q $serviceName 2>$null
$ErrorActionPreference = $oldErrorAction

if (-not $imageExists -or $Rebuild) {
    if ($Rebuild) {
        Write-Host "[+] Recompilando imagen..." -ForegroundColor Yellow
    } else {
        Write-Host "[+] Primera ejecucion. Compilando entorno..." -ForegroundColor Yellow
    }

    try {
        & docker compose build $serviceName
        if ($LASTEXITCODE -ne 0) { throw "Build fallido" }
    } catch {
        Write-Host "[-] Limpiando cache y reintentando..." -ForegroundColor Yellow
        & docker builder prune -f 2>$null
        & docker compose build $serviceName
        if ($LASTEXITCODE -ne 0) {
            Write-Host "[-] No se pudo compilar la imagen." -ForegroundColor Red
            exit 1
        }
    }
    Write-Host "[+] Entorno listo." -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "[+] Imagen existente. Usar -Rebuild para recompilar." -ForegroundColor DarkGray
}

# 3. Levantar container si no esta corriendo
$containerId = docker compose ps -q $serviceName 2>$null

if (-not $containerId) {
    Write-Host "[+] Iniciando container..." -ForegroundColor Yellow
    & docker compose up -d $serviceName
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[-] No se pudo iniciar el container." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "[+] Container activo." -ForegroundColor Green
}

# 4. Abrir CLI
Write-Host "[+] Abriendo SCIPi..." -ForegroundColor Cyan
Write-Host "    (Ctrl+C para salir. El container sigue corriendo.)" -ForegroundColor DarkGray
Write-Host ""
& docker compose exec $serviceName python -m app.main
