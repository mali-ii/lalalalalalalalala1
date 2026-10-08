import tempfile
from pathlib import Path
from src import config, db


class TempDB:
    """Подменяет config.DB_PATH на временный файл."""
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self._old = config.DB_PATH
        config.DB_PATH = Path(self._tmp.name) / "test.sqlite"
        db.init_db()

    def tearDown(self):
        config.DB_PATH = self._old
        self._tmp.cleanup()
