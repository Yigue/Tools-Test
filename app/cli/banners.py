"""Banner ASCII de la aplicacion."""
from rich.panel import Panel


def get_banner() -> Panel:
    """Retorna el banner principal de SCIPi."""
    art = (
        "[bold cyan]"
        "      ___           ___           ___           ___           ___      \n"
        "     /\\  \\         /\\  \\         /\\  \\         /\\  \\         /\\  \\     \n"
        "    /::\\  \\       /::\\  \\        \\:\\  \\       /::\\  \\        \\:\\  \\    \n"
        "   /:/\\ \\  \\     /:/\\:\\  \\        \\:\\  \\     /:/\\:\\  \\        \\:\\  \\   \n"
        "  _\\:\\~\\ \\  \\   /:/  \\:\\  \\       /::\\  \\   /::\\~\\:\\  \\       /::\\  \\  \n"
        " /\\ \\:\\ \\ \\__\\ /:/__/ \\:\\__\\     /:/\\:\\__\\ /:/\\:\\ \\:\\__\\     /:/\\:\\__\\ \n"
        " \\:\\ \\:\\ \\/__/ \\:\\  \\  \\/__/    /:/  \\/__/ \\/__\\:\\/:/  /    /:/  \\/__/ \n"
        "  \\:\\ \\:\\__\\    \\:\\  \\         /:/  /           \\::/  /    /:/  /      \n"
        "   \\:\\/:/  /     \\:\\  \\       \\/__/             \\/__/     \\/__/       \n"
        "    \\::/  /       \\:\\__\\                                               \n"
        "     \\/__/         \\/__/                                               \n"
        "[/bold cyan]\n"
        "[bold white]         Automatizacion IT - Ansible + Python + Docker[/bold white]"
    )
    return Panel.fit(
        art,
        title="[bold green]SCIPi v2.0[/bold green]",
        border_style="cyan",
    )
