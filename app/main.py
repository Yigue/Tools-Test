import typer
from rich.console import Console

# Importación de nuevos modulos con Arquitectura Limpia
from cli.banners import get_main_banner
from cli.menu import show_main_menu, get_target_device_info
from core.network import run_preflight_checks
from core.ansible_manager import run_playbook

app = typer.Typer(help="CLI Principal de SCIPi para Automatización y Control")
console = Console()

@app.command()
def main():
    # 1. Dibujar el Banner principal
    console.print(get_main_banner())
    console.print()

    # 2. Iniciar el ciclo interactivo del usuario
    while True:
        opcion = show_main_menu()
        
        if "0." in opcion:
            console.print("\n[bold yellow]Saliendo del sistema SCIPi. ¡Hasta pronto![/bold yellow]")
            raise typer.Exit()
            
        elif "1." in opcion:
            # Flujo de ejecución Ansible refactorizado
            target, user, pwd, display_host = get_target_device_info()
            
            console.print(f"\n[bold yellow]Iniciando ejecución de:[/bold yellow] get_specs.yml \n[bold yellow]Destino:[/bold yellow] {display_host}")
            
            # Pre-Flight Check (Plan A)
            if run_preflight_checks(target):
                run_playbook("get_specs.yml", target, user, pwd)
                
        elif "3." in opcion:
            target, _, _, _ = get_target_device_info()
            run_preflight_checks(target)
            
        else:
            console.print(f"\n[bold green]Has seleccionado:[/bold green] [cyan]{opcion}[/cyan]")
            console.print("[dim]Esta funcionalidad está en desarrollo. Volviendo al menú principal...[/dim]\n")

if __name__ == "__main__":
    app()
