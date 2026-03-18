#!/bin/bash
set -e

SERVICE="scipi"

echo ""
echo "  SCIPi v2.0 - Automatizacion IT"
echo "  ================================"
echo ""

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "[-] Docker no esta instalado."
    exit 1
fi
echo "[+] Docker detectado"

# Compilar si es necesario
if [ "$1" = "--rebuild" ] || ! docker compose images -q "$SERVICE" 2>/dev/null | grep -q .; then
    echo "[+] Compilando entorno..."
    docker compose build "$SERVICE"
    echo "[+] Entorno listo."
else
    echo "[+] Imagen existente. Usar --rebuild para recompilar."
fi

# Levantar container
if ! docker compose ps -q "$SERVICE" 2>/dev/null | grep -q .; then
    echo "[+] Iniciando container..."
    docker compose up -d "$SERVICE"
else
    echo "[+] Container activo."
fi

# Abrir CLI
echo "[+] Abriendo SCIPi..."
echo ""
docker compose exec "$SERVICE" python -m app.main
