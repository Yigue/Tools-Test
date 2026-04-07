"""Verificaciones de red previas a la ejecucion."""
import socket
import subprocess

from app.config.settings import WINRM_PORT, CONNECTION_TIMEOUT, console


def check_ping(host: str, timeout: int = 3) -> bool:
    """Verifica conectividad ICMP con el host."""
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", str(timeout), host],
            capture_output=True, text=True, timeout=timeout + 2,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def check_port(host: str, port: int = WINRM_PORT, timeout: int = CONNECTION_TIMEOUT) -> bool:
    """Verifica si un puerto TCP esta abierto."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False


def run_preflight(host: str) -> bool:
    """Ejecuta verificaciones de red. Retorna True si WinRM es alcanzable."""
    console.print(f"\n[bold cyan]Verificando conectividad con {host}...[/bold cyan]")

    ping_ok = check_ping(host)
    if ping_ok:
        console.print("  [green]>[/green] Ping exitoso")
    else:
        console.print("  [yellow]![/yellow] Ping bloqueado (puede ser firewall)")

    port_ok = check_port(host)
    if port_ok:
        console.print(f"  [green]>[/green] Puerto WinRM ({WINRM_PORT}) abierto")
    else:
        console.print(f"  [red]x[/red] Puerto WinRM ({WINRM_PORT}) cerrado")
        console.print("  [dim]Verifica que WinRM este habilitado en el equipo destino[/dim]")
        console.print("  [dim]Si atacas al propio Host desde Docker, verifica las reglas del Firewall de Windows para la subred de Docker.[/dim]")
        return False

    return True
