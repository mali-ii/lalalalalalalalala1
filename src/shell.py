"""Командная оболочка (User Space). Работает с ядром только через системные вызовы."""
from src import config, kernel, syscalls

BANNER = f"""
=====================================
  {config.OS_NAME} v{config.OS_VERSION} — учебная ОС
  Введите help для справки
====================================="""

HELP = """Команды:
  help         - справка
  echo <текст> - вернуть сообщение (sys_echo)
  users        - список пользователей (sys_get_users)
  exit         - выход"""


def run() -> None:
    kernel.boot()
    print(BANNER)
    while True:
        try:
            line = input("eduos> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        cmd, _, arg = line.partition(" ")
        if cmd == "help":
            print(HELP)
        elif cmd == "echo":
            print(syscalls.sys_echo(arg))
        elif cmd == "users":
            for u in syscalls.sys_get_users() or []:
                print(f"{u['id']:>3}  {u['login']:<12} {u['role']:<6} {u['created_at']}")
        elif cmd == "exit":
            print("Завершение работы.")
            break
        else:
            print(f"Неизвестная команда: {cmd}. Введите help.")


if __name__ == "__main__":
    run()
