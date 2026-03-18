"""Ejecucion de playbooks Ansible via subprocess."""
import json
import os
import subprocess
import time

from app.config.settings import ANSIBLE_DIR, PLAYBOOKS_DIR, PLAYBOOK_TIMEOUT, console
from app.core.inventory import build_dynamic_inventory
from app.core.models import ExecutionResult


def execute_playbook(
    playbook_name: str,
    hostname: str,
    username: str,
    password: str,
    extra_vars: dict | None = None,
    timeout: int = PLAYBOOK_TIMEOUT,
) -> ExecutionResult:
    """Ejecuta un playbook de Ansible contra un host remoto via WinRM."""
    playbook_path = PLAYBOOKS_DIR / playbook_name
    if not playbook_path.exists():
        return ExecutionResult(
            success=False,
            stderr=f"Playbook no encontrado: {playbook_name}",
        )

    inventory_path = build_dynamic_inventory(hostname, username, password)

    try:
        cmd = _build_command(str(playbook_path), inventory_path, extra_vars)
        env = _get_ansible_env()
        start = time.time()

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(ANSIBLE_DIR),
            env=env,
        )

        duration = time.time() - start
        data = _parse_output(result.stdout)

        return ExecutionResult(
            success=result.returncode == 0,
            data=data,
            stdout=result.stdout,
            stderr=result.stderr,
            return_code=result.returncode,
            duration=duration,
        )
    except subprocess.TimeoutExpired:
        return ExecutionResult(
            success=False,
            stderr=f"Timeout: la ejecucion supero los {timeout}s",
        )
    finally:
        _cleanup(inventory_path)


def _build_command(
    playbook_path: str,
    inventory_path: str,
    extra_vars: dict | None = None,
) -> list[str]:
    """Construye el comando ansible-playbook."""
    cmd = [
        "ansible-playbook",
        playbook_path,
        "-i", inventory_path,
        "--limit", "target",
    ]
    if extra_vars:
        pairs = " ".join(f"{k}={v}" for k, v in extra_vars.items())
        cmd.extend(["--extra-vars", pairs])
    return cmd


def _get_ansible_env() -> dict[str, str]:
    """Prepara variables de entorno para Ansible."""
    env = os.environ.copy()
    env["ANSIBLE_STDOUT_CALLBACK"] = "json"
    env["ANSIBLE_HOST_KEY_CHECKING"] = "False"
    env["ANSIBLE_DEPRECATION_WARNINGS"] = "False"
    env["ANSIBLE_COMMAND_WARNINGS"] = "False"
    cfg = ANSIBLE_DIR / "ansible.cfg"
    if cfg.exists():
        env["ANSIBLE_CONFIG"] = str(cfg)
    return env


def _parse_output(stdout: str) -> dict:
    """Intenta parsear la salida JSON de Ansible."""
    try:
        return json.loads(stdout)
    except (json.JSONDecodeError, ValueError):
        return {}


def _cleanup(path: str) -> None:
    """Elimina archivo temporal de inventario."""
    try:
        os.unlink(path)
    except OSError:
        pass
