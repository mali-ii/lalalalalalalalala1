"""Ядро EduOS: загрузка системы."""
from src import config, db


def boot() -> None:
    db.init_db()
    print(f"[kernel] {config.OS_NAME} {config.OS_VERSION}: база данных готова")
