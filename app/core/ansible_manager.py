import ansible_runner
from rich.console import Console

console = Console()

def run_playbook(playbook_name: str, target_host: str, ansible_user: str = "", ansible_pass: str = ""):
    """Encapsulación centralizada para ejecutar playbooks por ansible-runner de manera segura."""
    base_dir = "/app/app/ansible"
    
    # Configuramos el formato del límite del inventario
    host_limit = f"{target_host}," if target_host != "localhost" else "localhost"
    
    # Extra variables que se sobreescriben al vuelo para conectarnos por WinRM (Fileless)
    ansible_extra_vars = {}
    
    if target_host != "localhost":
        # Estas variables activan la conexión de Python hacia Windows mediante pywinrm y NTLM
        ansible_extra_vars = {
            'ansible_connection': 'winrm',
            'ansible_winrm_server_cert_validation': 'ignore',
            'ansible_winrm_transport': 'ntlm',
            'ansible_user': ansible_user,
            'ansible_password': ansible_pass
        }

    r = ansible_runner.run(
        private_data_dir=base_dir,
        playbook=f"playbooks/{playbook_name}",
        inventory=f"{base_dir}/inventory/inventory.yml",
        limit=host_limit,
        extravars=ansible_extra_vars,
        quiet=True,
        envvars={
            'ANSIBLE_DEPRECATION_WARNINGS': 'False',
            'ANSIBLE_HOST_KEY_CHECKING': 'False'
        }
    )

    console.print("\n[bold cyan]--- Resultados de la Ejecución ---[/bold cyan]")
    
    # Recorremos eventos buscando resultados directos
    for event in r.events:
        event_name = event['event']
        res = event.get('event_data', {}).get('res', {})
        
        if event_name == 'runner_on_ok' and 'msg' in res:
            console.print(f"[bold green]Éxito[/bold green]: {res['msg']}")
        elif event_name == 'runner_on_unreachable':
            console.print(f"[bold red]Host Inalcanzable[/bold red]: Verifica las credenciales WinRM y conectividad de red.")
        elif event_name == 'runner_on_failed':
            error_msg = res.get('msg', "Fallo detectado en el módulo (Revisar logs).")
            console.print(f"[bold red]Fallo ({target_host})[/bold red]: {error_msg}")

    console.print(f"\n[dim]Estado final: {r.status} | Código: {r.rc}[/dim]")
