# EduOS — учебная операционная система

Учебная ОС с монолитным ядром на Python 3.10+ и SQLite.

## Запуск
```
python src/db.py        # создать базу db/os.sqlite
python -m src.shell     # запустить командную оболочку
python -m unittest discover tests
```
Учётная запись по умолчанию: `admin` / `admin123` (пароль хранится как SHA-256).

## Структура
- `src/` — исходный код (kernel, syscalls, shell, db, config)
- `docs/` — проектная документация
- `db/` — файл базы данных
- `tests/` — тесты
- `logs/` — журналы работы

## Занятие 2
- Архитектура и диаграмма компонентов: `docs/02_OS_Architecture.md`, `docs/02_component_diagram.png`
- 13 системных вызовов `sys_*` в `src/syscalls.py`; самопроверка: `python3 -m src.syscalls`
- Оболочка: команды `whoami`, `login`, `logout`, `create`, `ls`, `ps`, `logs`
- Тесты: `python3 -m unittest discover tests`
