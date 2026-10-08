import unittest
from src import db, syscalls
from tests.helpers import TempDB


class PrototypeTest(TempDB, unittest.TestCase):
    def test_echo_logged(self):
        self.assertEqual(syscalls.sys_echo("hi"), "hi")
        self.assertEqual(db.fetch_logs(1)[0]["syscall_name"], "sys_echo")

    def test_users_and_hash(self):
        users = syscalls.sys_get_users()
        self.assertTrue(any(u["login"] == "admin" for u in users))
        conn = db.get_connection()
        h = conn.execute("SELECT password_hash FROM users WHERE login='admin'").fetchone()[0]
        conn.close()
        self.assertEqual(len(h), 64)
        self.assertNotEqual(h, "admin123")

    def test_old_column_is_migrated(self):
        conn = db.get_connection()
        conn.executescript("DROP TABLE syscalls_log; CREATE TABLE syscalls_log "
                           "(id INTEGER PRIMARY KEY, name TEXT, args TEXT, user TEXT, "
                           "status TEXT, timestamp TEXT DEFAULT CURRENT_TIMESTAMP);")
        conn.close()
        db.init_db()
        syscalls.sys_echo("x")
        self.assertEqual(db.fetch_logs(1)[0]["syscall_name"], "sys_echo")


if __name__ == "__main__":
    unittest.main()
