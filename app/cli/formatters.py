"""Formateo de resultados de ejecucion."""
from rich.panel import Panel
from rich.table import Table

from app.config.settings import console
from app.core.models import ExecutionResult


def show_result(result: ExecutionResult, task_name: str) -> None:
    """Muestra el resultado de una ejecucion de playbook."""
    if not result.success:
        _show_error(result, task_name)
        return

    data = result.data
    plays = data.get("plays", [])

    for play in plays:
        for task in play.get("tasks", []):
            _show_task_result(task)

    _show_summary(result)


def show_raw_output(result: ExecutionResult) -> None:
    """Muestra la salida raw cuando no hay JSON parseado."""
    if result.stdout:
        console.print(Panel(result.stdout, title="Salida", border_style="cyan"))
    if result.stderr:
        console.print(Panel(result.stderr, title="Errores", border_style="red"))


def _show_task_result(task: dict) -> None:
    """Muestra el resultado de una tarea individual."""
    task_name = task.get("task", {}).get("name", "Tarea sin nombre")
    hosts = task.get("hosts", {})

    for host, host_data in hosts.items():
        msg = host_data.get("msg", "")
        stdout = host_data.get("stdout", "")
        stdout_lines = host_data.get("stdout_lines", [])
        changed = host_data.get("changed", False)
        failed = host_data.get("failed", False)
        unreachable = host_data.get("unreachable", False)

        if unreachable:
            console.print(f"  [red]x[/red] {task_name}: Host inalcanzable")
            return
        if failed:
            err = host_data.get("msg", "Error desconocido")
            console.print(f"  [red]x[/red] {task_name}: {err}")
            return

        status = "[yellow]modificado[/yellow]" if changed else "[green]ok[/green]"
        console.print(f"  [{status}] {task_name}")

        if msg:
            _print_msg(msg)
        elif stdout_lines:
            for line in stdout_lines[:50]:
                console.print(f"    {line}")
        elif stdout:
            for line in stdout.split("\n")[:50]:
                console.print(f"    {line}")


def _print_msg(msg) -> None:
    """Imprime un mensaje que puede ser string, dict o lista."""
    if isinstance(msg, dict):
        for k, v in msg.items():
            console.print(f"    [bold]{k}:[/bold] {v}")
    elif isinstance(msg, list):
        for item in msg:
            console.print(f"    {item}")
    else:
        console.print(f"    {msg}")


def _show_error(result: ExecutionResult, task_name: str) -> None:
    """Muestra un error de ejecucion."""
    console.print(f"\n[bold red]Error en: {task_name}[/bold red]")
    if result.stderr:
        console.print(f"  {result.stderr[:500]}")
    if result.data:
        plays = result.data.get("plays", [])
        for play in plays:
            for task in play.get("tasks", []):
                _show_task_result(task)


def _show_summary(result: ExecutionResult) -> None:
    """Muestra resumen de la ejecucion."""
    stats = result.data.get("stats", {})
    for host, s in stats.items():
        ok = s.get("ok", 0)
        changed = s.get("changed", 0)
        failed = s.get("failures", 0)
        unreachable = s.get("unreachable", 0)

        color = "green" if failed == 0 and unreachable == 0 else "red"
        console.print(
            f"\n[{color}]{host}[/{color}]: ok={ok} changed={changed} "
            f"failed={failed} unreachable={unreachable} "
            f"({result.duration:.1f}s)"
        )
