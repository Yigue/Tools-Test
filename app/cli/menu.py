from InquirerPy import inquirer
from rich.console import Console

console = Console()

def show_main_menu() -> str:
    """Muestra el menú principal y retorna la opción seleccionada."""
    opcion = inquirer.select(
        message="Seleccione una acción a realizar:",
        choices=[
            "1. Obtener Specs del Equipo (Ejecutar Ansible)",
            "2. Consultar dispositivo en SCCM",
            "3. Verificar estado de la red (Ping / TCP)",
            "0. Salir de SCIPi"
        ],
    ).execute()
    return opcion

from typing import Tuple

def get_target_device_info() -> Tuple[str, str, str, str]:
    """Pregunta al usuario los datos de conexión para Ansible e imprime los detalles."""
    target_host = inquirer.text(
        message="Ingrese el hostname/IP destino (Ej: nb102237 o localhost):",
        default="localhost"
    ).execute()

    ansible_user = ""
    ansible_pass = ""

    # Parche de Conectividad Docker (Fase 3): Si el usuario intenta pegarle a su propio equipo anfitrión,
    # Docker necesita usar su DNS interno especial para enrutar tráfico fuera del contenedor.
    if target_host.lower() in ["localhost", "127.0.0.1", "nb102237"]:
        console.print(f"[dim]Traduciendo {target_host} a host.docker.internal para alcanzar la máquina base de Windows...[/dim]")
        
        # Guardamos el original para mostrar en pantalla, pero Ansible usará el internal
        display_host = target_host
        target_host = "host.docker.internal" 
        
        # Incluso siendo el propio equipo (ahora tratado remotamente por Docker), el WinRM requiere credenciales Windows
        console.print("[yellow]Conexión WinRM requerida hacia el Host Base de Windows.[/yellow]")
        ansible_user = inquirer.text(message="Usuario Administrador (ej: dominio\\usuario):").execute()
        ansible_pass = inquirer.secret(message="Contraseña:").execute()
        
    else:
        display_host = target_host
        console.print("[yellow]Destino remoto detectado. Se requieren credenciales WinRM.[/yellow]")
        ansible_user = inquirer.text(message="Usuario Administrador:").execute()
        ansible_pass = inquirer.secret(message="Contraseña:").execute()
        
    return target_host, ansible_user, ansible_pass, display_host
