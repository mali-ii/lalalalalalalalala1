"""Командная оболочка (User Space). Знает только о syscalls.py: ни ядро, ни БД не импортирует."""
from src import config
from src.syscalls import (
    boot, sys_echo, sys_get_users, sys_login, sys_logout, sys_whoami,
    sys_create_file, sys_list_files, sys_ps, sys_logs, sys_shutdown,
)

BANNER = f"""
=====================================
  {config.OS_NAME} v{config.OS_VERSION} — учебная ОС
  Введите help для справки
====================================="""

HELP = """Команды:
  help         - справка
  echo <текст> - вернуть сообщение
  users        - список пользователей
  whoami       - текущий пользователь
  login        - войти (запросит логин и пароль)
  logout       - выйти (вернуться в guest)
  create       - создать файл (запросит путь и содержимое)
  ls           - список файлов
  ps           - список процессов
  logs         - последние 10 записей журнала вызовов
  exit         - выход"""


def run() -> None:
    boot()
    print(BANNER)
    current_user = "guest"
    while True:
        try:
            line = input(f"{current_user}@{config.OS_NAME.lower()}:~$ ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        cmd, _, arg = line.partition(" ")
        if cmd == "help":
            print(HELP)
        elif cmd == "echo":
            print(sys_echo(arg, current_user))
        elif cmd == "users":
            for u in sys_get_users(current_user):
                print(f"{u['id']:>3}  {u['login']:<12} {u['role']:<6} {u['created_at']}")
        elif cmd == "whoami":
            print(sys_whoami(current_user))
        elif cmd == "login":
            login = input("Логин: ")
            password = input("Пароль: ")
            if sys_login(login, password, current_user):
                current_user = login
                print(f"Вы вошли как {login}")
            else:
                print("Ошибка входа")
        elif cmd == "logout":
            if sys_logout(current_user):
                current_user = "guest"
                print("Вы вышли из системы")
        elif cmd == "create":
            path = input("Путь: ")
            content = input("Содержимое: ")
            fid = sys_create_file(path, content, current_user)
            print(f"Создан файл с id={fid}")
        elif cmd == "ls":
            for f in sys_list_files("/", current_user):
                print(f)
        elif cmd == "ps":
            for p in sys_ps(current_user):
                print(p)
        elif cmd == "logs":
            for r in sys_logs(10, current_user):
                print(f"{r['id']:>3}  {r['timestamp']}  {r['user']:<8} {r['syscall_name']:<16} {r['args']}  [{r['status']}]")
        elif cmd == "exit":
            sys_shutdown(current_user)
            print("Завершение работы.")
            break
        else:
            print(f"Неизвестная команда: {cmd}. Введите help.")


if __name__ == "__main__":
    run()
