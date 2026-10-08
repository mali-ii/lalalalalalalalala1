"""Ядро EduOS: принимает вызовы от syscalls.py и координирует подсистемы.
Ядро не обращается к БД напрямую: только через scheduler, memory, fs, auth."""
from src import auth, config, fs, memory, scheduler


def boot() -> None:
    print(f"[kernel] {config.OS_NAME} {config.OS_VERSION}: ядро загружено")


def login(login: str, password: str) -> bool:
    return auth.check_login(login, password)


def logout(user: str) -> bool:
    return True


def whoami(user: str) -> str:
    return user


def list_users() -> list[dict]:
    return auth.list_users()


def create_file(path: str, content: str, user: str) -> int:
    return fs.create_file(path, content, user)


def read_file(path: str, user: str) -> str:
    return fs.read_file(path, user)


def delete_file(path: str, user: str) -> bool:
    return fs.delete_file(path, user)


def list_files(path: str, user: str) -> list:
    return fs.list_files(path, user)


def exec_process(name: str, user: str) -> int:
    return scheduler.spawn(name, user)


def ps() -> list:
    return scheduler.list_processes()


def kill(pid: int) -> bool:
    return scheduler.kill(pid)


def mem_alloc(size: int, user: str) -> int:
    return memory.alloc(size, user)


def shutdown(user: str) -> bool:
    return True
