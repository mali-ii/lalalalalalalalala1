"""Конфигурация учебной ОС EduOS."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "os.sqlite"
LOG_DIR = BASE_DIR / "logs"

OS_NAME = "EduOS"
OS_VERSION = "0.1"

MAX_SYSCALL_MS = 50      # НФТ: порог времени системного вызова, мс
MAX_PROCESSES = 10       # НФТ: максимум одновременных процессов
MEMORY_LIMIT_KB = 1024   # лимит памяти на процесс

DEFAULT_ADMIN = ("admin", "admin123", "admin")
