<#
.SYNOPSIS
    Script de Despliegue Automatizado para AWX Enterprise (Minikube/Docker)
.DESCRIPTION
    Levanta la infraestructura base de Kubernetes, instala AWX Operator, aplica la
    configuración de hardening y compila el Custom Execution Environment con Kerberos.
#>
$ErrorActionPreference = "Stop"

Write-Host "[*] Iniciando Secuencia de Despliegue Nivel L3..." -ForegroundColor Cyan

# 1. Validación de variables de entorno
if (-Not (Test-Path ".\.env")) {
    Write-Host "[!] ERROR: Archivo .env no encontrado. Por favor, crea uno a partir de .env.example." -ForegroundColor Red
    exit 1
}
$envData = Get-Content .\.env | ConvertFrom-StringData

Write-Host "[*] Fase 1: Levantando Infraestructura de Minikube..." -ForegroundColor Yellow
# Intentar levantar; si ya está arriba, solo refresca el contexto
minikube start --cpus=4 --memory=8192 --driver=docker --addons=storage-provisioner,default-storageclass

Write-Host "[*] Fase 2: Desplegando AWX Operator y Controller..." -ForegroundColor Yellow

# ACTUALIZACIÓN (Según la documentación oficial del repo awx-operator-helm)
# Agregamos el nuevo repositorio y actualizamos
helm repo add awx-operator https://ansible-community.github.io/awx-operator-helm/
helm repo update

# Instalamos usando el nuevo repositorio y aprovechamos --create-namespace nativo de Helm
helm upgrade --install my-awx-operator awx-operator/awx-operator -n awx --create-namespace

Write-Host "[*] Fase 3: Aplicando Instancia AWX Hardened..." -ForegroundColor Yellow
kubectl apply -f .\infra\awx\awx-enterprise.yaml -n awx

Write-Host "[*] Fase 4: Compilando Execution Environment Corporativo..." -ForegroundColor Yellow
# Generar krb5.conf desde la plantilla
$template = Get-Content .\infra\ee-build\krb5.conf.template -Raw
$template = $template -replace '\$\{AD_DOMAIN\}', $envData.AD_DOMAIN
$template = $template -replace '\$\{AD_DOMAIN_LOWER\}', $envData.AD_DOMAIN_LOWER
$template = $template -replace '\$\{AD_DC_IP\}', $envData.AD_DC_IP
Set-Content -Path .\infra\ee-build\krb5.conf -Value $template

# Apuntar Docker a Minikube y compilar
& minikube -p minikube docker-env --shell powershell | Invoke-Expression
Set-Location -Path .\infra\ee-build\
docker build -t awx-custom-ee:1.0 .
Set-Location -Path ..\..\

# Limpiar archivo temporal por seguridad
Remove-Item .\infra\ee-build\krb5.conf -Force

Write-Host "[*] Fase 5: Extracción de Credenciales..." -ForegroundColor Yellow
Write-Host "Esperando a que AWX genere el secreto de Admin (esto puede tardar unos minutos)..."
Start-Sleep -Seconds 15 # Breve pausa para que K8s procese el despliegue

try {
    $adminPass = kubectl get secret awx-pro-admin-password -n awx -o jsonpath="{.data.password}" | % { [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($_)) }
    $awxUrl = $(minikube service awx-pro-service -n awx --url)
    
    Write-Host ("=" * 50) -ForegroundColor Green
    Write-Host "🚀 DESPLIEGUE COMPLETADO CON ÉXITO 🚀" -ForegroundColor Green
    Write-Host "URL de AWX: $awxUrl" -ForegroundColor White
    Write-Host "Usuario: admin" -ForegroundColor White
    Write-Host "Contraseña: $adminPass" -ForegroundColor White
    Write-Host ("=" * 50) -ForegroundColor Green
} catch {
    Write-Host "[!] El pod aún está inicializando. Usa 'kubectl get pods -n awx -w' para monitorear." -ForegroundColor Yellow
}