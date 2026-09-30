import unittest
from src import db, syscalls


class PrototypeTest(unittest.TestCase):
    def setUp(self):
        db.init_db()

    def test_echo_logged(self):
        self.assertEqual(syscalls.sys_echo("hi"), "hi")
        conn = db.get_connection()
        n = conn.execute("SELECT COUNT(*) FROM syscalls_log WHERE name='sys_echo'").fetchone()[0]
        conn.close()
        self.assertGreater(n, 0)

    def test_users_and_hash(self):
        users = syscalls.sys_get_users()
        self.assertTrue(any(u["login"] == "admin" for u in users))
        conn = db.get_connection()
        h = conn.execute("SELECT password_hash FROM users WHERE login='admin'").fetchone()[0]
        conn.close()
        self.assertEqual(len(h), 64)
        self.assertNotEqual(h, "admin123")


if __name__ == "__main__":
    unittest.main()
