"""Prompts de entrada del usuario."""
from InquirerPy import inquirer

from app.config.settings import console


def ask_hostname() -> str:
    """Solicita el hostname o IP del equipo destino."""
    hostname = inquirer.text(
        message="Hostname o IP del equipo:",
        validate=lambda val: len(val.strip()) > 0,
        invalid_message="Debe ingresar un hostname o IP.",
    ).execute()
    return _translate_docker_host(hostname.strip())


def ask_credentials() -> tuple[str, str]:
    """Solicita usuario y password para la conexion WinRM."""
    username = inquirer.text(
        message="Usuario (dominio\\usuario):",
        validate=lambda val: len(val.strip()) > 0,
        invalid_message="Debe ingresar un usuario.",
    ).execute()

    password = inquirer.secret(
        message="Password:",
        validate=lambda val: len(val) > 0,
        invalid_message="Debe ingresar un password.",
    ).execute()

    return username.strip(), password


def ask_extra_input(prompt: str) -> str:
    """Solicita un valor extra requerido por la opcion."""
    value = inquirer.text(
        message=prompt,
        validate=lambda val: len(val.strip()) > 0,
    ).execute()
    return value.strip()


def _translate_docker_host(hostname: str) -> str:
    """Traduce localhost a host.docker.internal dentro del container."""
    local_names = {"localhost", "127.0.0.1"}
    if hostname.lower() in local_names:
        return "host.docker.internal"
    return hostname
