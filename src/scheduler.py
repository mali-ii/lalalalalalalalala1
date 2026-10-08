"""Планировщик и реестр процессов (ЗАГЛУШКИ). Позже: таблица processes через db.py."""
from src import db  # noqa: F401  (зависимость из диаграммы: scheduler -> db)


def spawn(name: str, owner: str) -> int:
    return 42


def list_processes() -> list:
    return []


def kill(pid: int) -> bool:
    return True
