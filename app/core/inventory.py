"""Construccion de inventario dinamico para Ansible."""
import tempfile


def build_dynamic_inventory(
    hostname: str,
    username: str,
    password: str,
    port: int = 5985,
) -> str:
    """Genera un archivo de inventario temporal INI para el host objetivo."""
    content = (
        "[target]\n"
        f"{hostname}\n\n"
        "[target:vars]\n"
        "ansible_connection=winrm\n"
        "ansible_winrm_transport=ntlm\n"
        "ansible_winrm_scheme=http\n"
        f"ansible_port={port}\n"
        "ansible_winrm_server_cert_validation=ignore\n"
        "ansible_winrm_message_encryption=never\n"
        f"ansible_user={username}\n"
        f"ansible_password={password}\n"
        "ansible_shell_type=powershell\n"
    )
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".ini", prefix="scipi_inv_", delete=False
    )
    tmp.write(content)
    tmp.close()
    return tmp.name
