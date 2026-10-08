"""Модуль работы с базой данных SQLite (файловая система, реестр процессов, журнал)."""
import hashlib
import sqlite3

try:
    from src import config
except ImportError:  # запуск как `python src/db.py`
    import config


def hash_password(password: str) -> str:
    """SHA-256 хэш пароля (пароли в открытом виде не хранятся)."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def get_connection() -> sqlite3.Connection:
    config.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    login         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role          TEXT NOT NULL CHECK (role IN ('admin', 'user')),
    created_at    TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS processes (
    pid        INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL,
    state      TEXT NOT NULL DEFAULT 'ready'
               CHECK (state IN ('new','ready','running','waiting','terminated')),
    owner_id   INTEGER REFERENCES users(id),
    memory_kb  INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS files (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    path       TEXT NOT NULL UNIQUE,
    content    TEXT NOT NULL DEFAULT '',
    owner_id   INTEGER REFERENCES users(id),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS syscalls_log (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    syscall_name TEXT NOT NULL,
    args      TEXT,
    user      TEXT,
    status    TEXT NOT NULL,
    timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def _migrate_log_column(conn: sqlite3.Connection) -> None:
    """Занятие 1 называло колонку `name`; с занятия 2 она `syscall_name`."""
    cols = [r[1] for r in conn.execute("PRAGMA table_info(syscalls_log)")]
    if "name" in cols and "syscall_name" not in cols:
        conn.execute("ALTER TABLE syscalls_log RENAME COLUMN name TO syscall_name")


def fetch_logs(limit: int = 10) -> list[dict]:
    """Последние записи журнала системных вызовов (новые сверху)."""
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT id, syscall_name, args, user, status, timestamp "
            "FROM syscalls_log ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    finally:
        conn.close()
    return [dict(r) for r in rows]


def init_db() -> None:
    """Создаёт таблицы и учётную запись администратора (если её ещё нет)."""
    conn = get_connection()
    try:
        with conn:
            conn.executescript(SCHEMA)
            _migrate_log_column(conn)
            login, password, role = config.DEFAULT_ADMIN
            conn.execute(
                "INSERT OR IGNORE INTO users (login, password_hash, role) VALUES (?, ?, ?)",
                (login, hash_password(password), role),
            )
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
    print(f"База данных создана: {config.DB_PATH}")
