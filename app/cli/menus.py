"""Menus interactivos de la aplicacion."""
from InquirerPy import inquirer

from app.config.settings import console
from app.core.models import MenuCategory, MenuOption


def show_categories(categories: list[MenuCategory]) -> MenuCategory | None:
    """Muestra las categorias disponibles y retorna la seleccionada."""
    choices = []
    for cat in categories:
        choices.append({"name": f"[{cat.key}] {cat.name}", "value": cat.key})
    choices.append({"name": "[0] Salir", "value": None})

    selected = inquirer.select(
        message="Selecciona una categoria:",
        choices=choices,
        default=choices[0]["value"],
    ).execute()

    if selected is None:
        return None
    return next((c for c in categories if c.key == selected), None)


def show_options(category: MenuCategory) -> MenuOption | None:
    """Muestra las opciones de una categoria y retorna la seleccionada."""
    choices = []
    for opt in category.options:
        tag = _action_tag(opt.action_type)
        choices.append({"name": f"[{opt.key}] {opt.label} {tag}", "value": opt.key})
    choices.append({"name": "[0] Volver", "value": None})

    selected = inquirer.select(
        message=f"{category.name} - Selecciona una opcion:",
        choices=choices,
        default=choices[0]["value"],
    ).execute()

    if selected is None:
        return None
    return next((o for o in category.options if o.key == selected), None)


def confirm_action(message: str) -> bool:
    """Pide confirmacion al usuario para acciones destructivas."""
    return inquirer.confirm(message=message, default=False).execute()


def _action_tag(action_type: str) -> str:
    """Retorna un tag visual segun el tipo de accion."""
    tags = {
        "read": "",
        "modify": "[yellow](modifica)[/yellow]",
        "destructive": "[red](destructivo)[/red]",
    }
    return tags.get(action_type, "")
