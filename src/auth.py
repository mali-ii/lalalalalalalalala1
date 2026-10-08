"""Аутентификация и права доступа. Обращается только к db.py."""
from src import db


def user_exists(login: str) -> bool:
    conn = db.get_connection()
    try:
        row = conn.execute("SELECT 1 FROM users WHERE login = ?", (login,)).fetchone()
    finally:
        conn.close()
    return row is not None


def check_login(login: str, password: str) -> bool:
    """ЗАГЛУШКА: проверяет только наличие логина в таблице users.
    Сверка SHA-256 хэша пароля (db.hash_password) будет добавлена позже."""
    return user_exists(login)


def list_users() -> list[dict]:
    conn = db.get_connection()
    try:
        rows = conn.execute("SELECT id, login, role, created_at FROM users").fetchall()
    finally:
        conn.close()
    return [dict(r) for r in rows]
