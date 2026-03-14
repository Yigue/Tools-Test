<#
.SYNOPSIS
    Script de inicio para la aplicación de automatización (CLI Python + Ansible).
.DESCRIPTION
    Verifica si existe la imagen en Docker. Solo la compila la primera vez (o si hay caché corrupta).
    Si necesitas forzar una actualización (por ej. si cambiaste requirements.txt o Dockerfile),
    ejecuta: .\inicio.ps1 -Rebuild
#>

param(
    [switch]$Rebuild
)

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host " Iniciando el Entorno de Automatización " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar si Docker está instalado y ejecutándose
try {
    $dockerVersion = docker --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Docker no respondió."
    }
    Write-Host "[+] Docker detectado: $dockerVersion" -ForegroundColor Green
}
catch {
    Write-Host "[-] ERROR: Docker Desktop no está instalado o no está corriendo." -ForegroundColor Red
    exit 1
}

# 2. Comprobar si hay que construir la imagen
# Desactivamos Stop temporalmente porque si la imagen no existe, Docker tira un error a Stderr que crashea el script
$oldErrorAction = $ErrorActionPreference
$ErrorActionPreference = "Continue"
$imageExists = docker compose images -q server 2>$null
$ErrorActionPreference = $oldErrorAction

if (-not $imageExists -or $Rebuild) {
    if ($Rebuild) {
        Write-Host "[+] Reconstrucción solicitada (-Rebuild). Compilando desde cero..." -ForegroundColor Yellow
    } else {
        Write-Host "[+] No se encontró la imagen. Preparando el entorno por primera vez..." -ForegroundColor Yellow
    }
    
    # Tratamos de compilar. Si falla el build (común por bugs de caché), limpiamos y reintentamos.
    try {
        & docker compose build
        if ($LASTEXITCODE -ne 0) { throw "Construcción fallida" }
    } catch {
        Write-Host "[-] ADVERTENCIA: Fallo al compilar (Caché corrupta de Docker). Purificando caché interna..." -ForegroundColor Yellow
        & docker builder prune -f
        Write-Host "[+] Reintentando compilación tras la limpieza..." -ForegroundColor Cyan
        & docker compose build
        if ($LASTEXITCODE -ne 0) {
            Write-Host "[-] ERROR FATAL: No se pudo construir la imagen tras la limpieza." -ForegroundColor Red
            exit 1
        }
    }
    Write-Host "[+] Entorno preparado correctamente." -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "[+] Imagen detectada localmente. Saltando proceso de compilación." -ForegroundColor Green
    Write-Host "    (Si editaste requirements.txt o Dockerfile, ejecuta: .\inicio.ps1 -Rebuild)" -ForegroundColor DarkGray
    Write-Host ""
}

# 3. Administrar el contenedor y conectarse
# Comprobamos si el contenedor "server" ya está en ejecución
$containerId = docker compose ps -q server 2>$null

if (-not $containerId) {
    Write-Host "[+] Iniciando el contenedor SCIPi en segundo plano..." -ForegroundColor Yellow
    # Usamos "up -d" para levantarlo y que quede vivo en el fondo.
    # El archivo compose.yaml ya tiene stdin_open y tty que evitan que se muera.
    & docker compose up -d server
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[-] ERROR: No se pudo iniciar el contenedor." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "[+] El contenedor SCIPi ya estaba en ejecución." -ForegroundColor Green
}

Write-Host "[+] Abriendo interfaz de la aplicación..." -ForegroundColor Cyan
Write-Host "    (Puedes presionar Ctrl+C en cualquier momento. El contenedor seguirá corriendo para que vuelvas a entrar rápido)." -ForegroundColor DarkGray
Write-Host ""
# Entramos al contenedor vivo ejecutando el script principal de Python
& docker compose exec server python app/main.py
