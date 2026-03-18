"""Definicion de categorias y opciones del menu."""
from app.core.models import MenuCategory, MenuOption


def get_menu_categories() -> list[MenuCategory]:
    """Retorna todas las categorias del menu con sus opciones."""
    return [
        MenuCategory(
            key="A", name="Admin y Dominio", icon="[bold yellow]A[/]",
            options=[
                MenuOption("A1", "Desbloquear usuario de red (AD)",
                           "admin/unlock_user.yml",
                           requires_input=True, input_prompt="Usuario a desbloquear",
                           action_type="modify"),
                MenuOption("A2", "Obtener password Admin Local (LAPS)",
                           "admin/get_laps_password.yml"),
                MenuOption("A3", "Info de equipo en AD",
                           "admin/ad_info.yml"),
                MenuOption("A4", "Mantenimiento completo",
                           "admin/full_maintenance.yml",
                           action_type="modify"),
            ],
        ),
        MenuCategory(
            key="H", name="Hardware y Sistema", icon="[bold cyan]H[/]",
            options=[
                MenuOption("H1", "Informacion del Sistema",
                           "hardware/specs.yml"),
                MenuOption("H2", "Optimizar Sistema",
                           "hardware/optimize.yml",
                           action_type="modify"),
                MenuOption("H3", "Reiniciar Equipo",
                           "hardware/reboot.yml",
                           action_type="destructive"),
                MenuOption("H4", "Salud de Bateria",
                           "hardware/battery_health.yml"),
                MenuOption("H5", "Activar Windows",
                           "hardware/activate_windows.yml",
                           action_type="modify"),
            ],
        ),
        MenuCategory(
            key="R", name="Redes y Wi-Fi", icon="[bold green]R[/]",
            options=[
                MenuOption("R1", "Reparar Red",
                           "network/network_repair.yml",
                           action_type="modify"),
                MenuOption("R2", "Analizador Wi-Fi",
                           "network/wifi_analyzer.yml"),
            ],
        ),
        MenuCategory(
            key="S", name="Gestion de Software", icon="[bold magenta]S[/]",
            options=[
                MenuOption("S1", "Gestionar Aplicaciones",
                           "software/manage_apps.yml"),
                MenuOption("S2", "Instalar Office 365",
                           "software/install_office.yml",
                           action_type="modify"),
            ],
        ),
        MenuCategory(
            key="I", name="Impresoras", icon="[bold blue]I[/]",
            options=[
                MenuOption("I1", "Gestionar Impresoras",
                           "printers/manage_printers.yml"),
            ],
        ),
    ]
