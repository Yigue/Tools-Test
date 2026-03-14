param(
  [Parameter(Mandatory=$true)][string]$SiteCode,
  [Parameter(Mandatory=$true)][string]$DeviceName,
  [string]$OutFile = "$env:TEMP\sccm_$($DeviceName).json"
)

$ErrorActionPreference = "Stop"

$psd1 = Join-Path $env:SMS_ADMIN_UI_PATH "..\ConfigurationManager.psd1"
if (-not (Test-Path $psd1)) {
  throw "No se encontró ConfigurationManager.psd1. ¿Está instalada la consola SCCM en este host?"
}

Import-Module $psd1 -Force

# REGLA / IMPORTANTE: NO creamos el drive. Solo usamos si ya existe.
$drive = Get-PSDrive -PSProvider CMSite -ErrorAction SilentlyContinue |
  Where-Object { $_.Name -ieq $SiteCode } |
  Select-Object -First 1

if (-not $drive) {
  $avail = (Get-PSDrive -PSProvider CMSite -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Name) -join ", "
  throw "No existe el drive '${SiteCode}:' (CMSite). Drives disponibles: ${avail:-ninguno}. Esto suele pasar si no hay conectividad/permiso al SMS Provider desde este PowerShell (fuera del GUI)."
}

Set-Location ("{0}:" -f $SiteCode)

$device = Get-CMDevice -Name $DeviceName |
  Select Name, ResourceId, IsClient, ClientType, LastActiveTime, LastLogonUserName, OperatingSystemNameAndVersion

if (-not $device) {
  @{ error="No encontrado"; device=$DeviceName; site=$SiteCode } |
    ConvertTo-Json | Set-Content -Encoding UTF8 $OutFile
  Write-Output $OutFile
  exit 0
}

$device | ConvertTo-Json -Depth 4 | Set-Content -Encoding UTF8 $OutFile
Write-Output $OutFile
