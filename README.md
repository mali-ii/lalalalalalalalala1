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
