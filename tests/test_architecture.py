"""Проверяет, что импорты модулей соответствуют диаграмме компонентов (стрелки только вниз)."""
import ast
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src"
ALLOWED = {  # модуль -> от каких модулей src ему можно зависеть (config доступен всем)
    "shell": {"syscalls"},
    "syscalls": {"kernel", "db"},   # db: только журналирование и инициализация БД
    "kernel": {"scheduler", "memory", "fs", "auth"},
    "scheduler": {"db"}, "memory": {"db"}, "fs": {"db"}, "auth": {"db"},
    "db": set(),
}


def imports_of(name):
    tree = ast.parse((SRC / f"{name}.py").read_text(encoding="utf-8"))
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            parts = node.module.split(".")
            if parts[0] == "src":
                found.update(parts[1:2] or [a.name for a in node.names])
                if len(parts) == 1:
                    found.update(a.name for a in node.names)
    return found - {"config"}


class ArchitectureTest(unittest.TestCase):
    def test_eight_modules_exist(self):
        for m in ALLOWED:
            self.assertTrue((SRC / f"{m}.py").exists(), m)

    def test_arrows_only_downward(self):
        for module, allowed in ALLOWED.items():
            extra = imports_of(module) - allowed
            self.assertFalse(extra, f"{module}.py импортирует лишнее: {extra}")

    def test_shell_never_touches_db_or_kernel(self):
        self.assertFalse(imports_of("shell") & {"db", "kernel"})


if __name__ == "__main__":
    unittest.main()
