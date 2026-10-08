"""Файловая система (ЗАГЛУШКИ). Позже будет хранить файлы в таблице files через db.py."""
from src import db  # noqa: F401  (зависимость из диаграммы: fs -> db)


def create_file(path: str, content: str, owner: str) -> int:
    return 1


def read_file(path: str, owner: str) -> str:
    return ""


def delete_file(path: str, owner: str) -> bool:
    return True


def list_files(path: str, owner: str) -> list:
    return ["/test.txt"]
