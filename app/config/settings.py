"""Configuracion global de la aplicacion."""
from pathlib import Path
from rich.console import Console

APP_NAME = "SCIPi"
APP_VERSION = "2.0"

BASE_DIR = Path(__file__).resolve().parent.parent
ANSIBLE_DIR = BASE_DIR / "ansible"
PLAYBOOKS_DIR = ANSIBLE_DIR / "playbooks"
ROLES_DIR = ANSIBLE_DIR / "roles"
LOGS_DIR = BASE_DIR / "logs"

console = Console()

WINRM_PORT = 5985
CONNECTION_TIMEOUT = 15
COMMAND_TIMEOUT = 120
PLAYBOOK_TIMEOUT = 1200
ANSIBLE_FORKS = 10
