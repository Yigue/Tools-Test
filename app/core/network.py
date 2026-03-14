import socket
import subprocess
import platform
from rich.console import Console

console = Console()

def check_ping(host: str) -> bool:
    """Envía paquetes ICMP (ping) para validar que el host responde en la red."""
    # En Linux ping -c 1 espera una respuesta, en Windows sería -n 1
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', '-W', '1', host]
    
    # Ejecutamos silenciosamente, solo nos importa el exit code
    return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

def check_tcp_port(host: str, port: int, timeout: int = 2) -> bool:
    """Intenta abrir un socket TCP al host y puerto especificado."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))
            return True
    except (socket.timeout, ConnectionRefusedError, socket.gaierror):
        return False

def run_preflight_checks(target_host: str) -> bool:
    """Ejecuta los chequeos de red necesarios antes de lanzar Ansible."""
    if target_host.lower() == "localhost":
        return True # Asumimos que el contenedor local siempre está vivo
    
    console.print(f"\n[cyan][Pre-Flight Check][/cyan] Escaneando host destino: {target_host}...")
    
    # Check 1: ICMP Ping (Descartado temporalmente si se quiere solo guiarse por el de 5985)
    # Se añade como recomendación para seguir tu Plan A:
    console.print("  [dim]1/2 Realizando Ping ICMP...[/dim]")
    if check_ping(target_host):
         console.print("  [green]✓ Ping responde.[/green]")
    else:
         console.print("  [yellow]⚠ Ping no responde (puede estar bloqueado por Firewall, continuando...).[/yellow]")
    
    # Check 2: WinRM Port
    console.print("  [dim]2/2 Validando puerto TCP 5985 (WinRM)...[/dim]")
    if check_tcp_port(target_host, 5985):
        console.print("[green]✓[/green] Todo en orden. Host accesible y listo para WinRM.")
        return True
    else:
        console.print(f"[red]✗[/red] Fallo al alcanzar {target_host} por WinRM (TCP 5985).")
        console.print("[dim]Posibles Causas: Equipo apagado, Firewall bloqueando puerto, o servicio WinRM inactivo.[/dim]")
        return False
