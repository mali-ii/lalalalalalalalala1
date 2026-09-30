"""Системные вызовы ядра. Каждый вызов автоматически журналируется."""
import functools
import time

from src import config, db

current_user = "system"


def log_syscall(name: str, args: str, user: str, status: str) -> None:
    """Запись об обращении к ядру в таблицу syscalls_log."""
    conn = db.get_connection()
    try:
        with conn:
            conn.execute(
                "INSERT INTO syscalls_log (name, args, user, status) VALUES (?, ?, ?, ?)",
                (name, args, user, status),
            )
    finally:
        conn.close()


def syscall(func):
    """Декоратор: журналирование, замер времени и перехват исключений."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        status = "ok"
        try:
            return func(*args, **kwargs)
        except Exception as exc:  # ядро не должно падать
            status = f"error: {exc}"
            return None
        finally:
            elapsed = (time.perf_counter() - start) * 1000
            if status == "ok" and elapsed > config.MAX_SYSCALL_MS:
                status = f"ok (slow {elapsed:.1f} ms)"
            log_syscall(func.__name__, repr(args), current_user, status)
    return wrapper


@syscall
def sys_echo(message: str) -> str:
    return message


@syscall
def sys_get_users() -> list[dict]:
    conn = db.get_connection()
    try:
        rows = conn.execute("SELECT id, login, role, created_at FROM users").fetchall()
    finally:
        conn.close()
    return [dict(r) for r in rows]
