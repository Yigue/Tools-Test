"""Entry point de SCIPi v2.0."""
import sys

from app.config.settings import console
from app.config.menu_data import get_menu_categories
from app.cli.banners import get_banner
from app.cli.menus import show_categories, show_options, confirm_action
from app.cli.prompts import ask_hostname, ask_credentials, ask_extra_input
from app.cli.formatters import show_result, show_raw_output
from app.core.network import run_preflight
from app.core.ansible_executor import execute_playbook
from app.core.models import ExecutionRecord


def main() -> None:
    """Loop principal de la aplicacion."""
    console.print(get_banner())
    console.print()

    hostname, username, password = _ask_connection_info()
    categories = get_menu_categories()
    history: list[ExecutionRecord] = []

    while True:
        console.print()
        category = show_categories(categories)
        if category is None:
            _exit_app()

        option = show_options(category)
        if option is None:
            continue

        if option.action_type == "destructive":
            if not confirm_action(f"{option.label} - Confirmar ejecucion?"):
                console.print("[dim]Cancelado.[/dim]")
                continue

        extra_vars = {}
        if option.requires_input:
            value = ask_extra_input(option.input_prompt)
            extra_vars["target_input"] = value

        console.print(
            f"\n[bold cyan]Ejecutando:[/bold cyan] {option.label}"
            f"\n[bold cyan]Destino:[/bold cyan] {hostname}"
        )

        if not run_preflight(hostname):
            console.print("[yellow]Abortado: host no alcanzable.[/yellow]")
            continue

        result = execute_playbook(
            playbook_name=option.playbook,
            hostname=hostname,
            username=username,
            password=password,
            extra_vars=extra_vars if extra_vars else None,
        )

        if result.data:
            show_result(result, option.label)
        else:
            show_raw_output(result)

        _record_history(history, hostname, option.label, result)
        _pause()


def _ask_connection_info() -> tuple[str, str, str]:
    """Solicita los datos de conexion al inicio."""
    console.print("[bold]Datos de conexion al equipo destino[/bold]\n")
    hostname = ask_hostname()
    username, password = ask_credentials()
    console.print(f"\n[green]Conectando a:[/green] {hostname}")
    return hostname, username, password


def _record_history(
    history: list[ExecutionRecord],
    hostname: str,
    task_name: str,
    result,
) -> None:
    """Registra una ejecucion en el historial de sesion."""
    from datetime import datetime

    record = ExecutionRecord(
        timestamp=datetime.now().strftime("%H:%M:%S"),
        hostname=hostname,
        task_name=task_name,
        success=result.success,
        duration=result.duration,
    )
    history.append(record)


def _pause() -> None:
    """Espera a que el usuario presione Enter."""
    console.print("\n[dim]Presiona Enter para continuar...[/dim]")
    try:
        input()
    except EOFError:
        pass


def _exit_app() -> None:
    """Sale de la aplicacion."""
    console.print("\n[bold yellow]Saliendo de SCIPi. Hasta pronto![/bold yellow]")
    sys.exit(0)


if __name__ == "__main__":
    main()
