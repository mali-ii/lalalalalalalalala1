"""Системные вызовы: интерфейс между оболочкой и ядром.
Каждый вызов записывается в syscalls_log. Параметр current_user — кто вызывает."""
from src import db, kernel
from src.db import get_connection


def boot() -> None:
    """Подготовка системы: создание БД и загрузка ядра (не системный вызов)."""
    db.init_db()
    kernel.boot()


def log_syscall(name, args="", user="system", status="OK"):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO syscalls_log (syscall_name, args, user, status) VALUES (?, ?, ?, ?)",
            (name, args, user, status),
        )
        conn.commit()
    finally:
        conn.close()


# --- вызовы из занятия 1 -------------------------------------------------------
def sys_echo(message: str, current_user="guest") -> str:
    log_syscall("sys_echo", message, current_user)
    return message


def sys_get_users(current_user="guest") -> list:
    log_syscall("sys_get_users", "", current_user)
    return kernel.list_users()


# --- 13 вызовов занятия 2 ------------------------------------------------------
def sys_login(login: str, password: str, current_user="guest") -> bool:
    ok = kernel.login(login, password)
    # пароль в журнал не пишем
    log_syscall("sys_login", login, current_user, "OK" if ok else "FAIL")
    return ok


def sys_logout(current_user="guest") -> bool:
    log_syscall("sys_logout", "", current_user)
    return kernel.logout(current_user)


def sys_whoami(current_user="guest") -> str:
    log_syscall("sys_whoami", "", current_user)
    return kernel.whoami(current_user)


def sys_create_file(path: str, content: str, current_user="guest") -> int:
    log_syscall("sys_create_file", path, current_user)
    return kernel.create_file(path, content, current_user)


def sys_read_file(path: str, current_user="guest") -> str:
    log_syscall("sys_read_file", path, current_user)
    return kernel.read_file(path, current_user)


def sys_delete_file(path: str, current_user="guest") -> bool:
    log_syscall("sys_delete_file", path, current_user)
    return kernel.delete_file(path, current_user)


def sys_list_files(path: str, current_user="guest") -> list:
    log_syscall("sys_list_files", path, current_user)
    return kernel.list_files(path, current_user)


def sys_exec(name: str, current_user="guest") -> int:
    log_syscall("sys_exec", name, current_user)
    return kernel.exec_process(name, current_user)


def sys_ps(current_user="guest") -> list:
    log_syscall("sys_ps", "", current_user)
    return kernel.ps()


def sys_kill(pid: int, current_user="guest") -> bool:
    log_syscall("sys_kill", str(pid), current_user)
    return kernel.kill(pid)


def sys_mem_alloc(size: int, current_user="guest") -> int:
    log_syscall("sys_mem_alloc", str(size), current_user)
    return kernel.mem_alloc(size, current_user)


def sys_logs(limit: int = 10, current_user="guest") -> list:
    log_syscall("sys_logs", str(limit), current_user)
    return db.fetch_logs(limit)


def sys_shutdown(current_user="guest") -> bool:
    log_syscall("sys_shutdown", "", current_user)
    return kernel.shutdown(current_user)


if __name__ == "__main__":
    db.init_db()
    print(sys_login("admin", "secret"))
    print(sys_whoami("admin"))
    print(sys_create_file("/test.txt", "hello", "admin"))
    print(sys_ps("admin"))
