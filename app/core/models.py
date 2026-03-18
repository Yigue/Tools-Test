"""Modelos de datos de la aplicacion."""
from dataclasses import dataclass, field
from typing import Any


@dataclass
class MenuOption:
    key: str
    label: str
    playbook: str
    requires_input: bool = False
    input_prompt: str = ""
    action_type: str = "read"


@dataclass
class MenuCategory:
    key: str
    name: str
    icon: str
    options: list[MenuOption] = field(default_factory=list)


@dataclass
class ExecutionResult:
    success: bool
    data: dict[str, Any] = field(default_factory=dict)
    stdout: str = ""
    stderr: str = ""
    return_code: int = -1
    duration: float = 0.0


@dataclass
class HostInfo:
    hostname: str
    username: str
    password: str
    display_name: str = ""


@dataclass
class ExecutionRecord:
    timestamp: str
    hostname: str
    task_name: str
    success: bool
    duration: float = 0.0
