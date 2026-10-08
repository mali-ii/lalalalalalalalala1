import time
import unittest
from src import config, db, syscalls as sc
from tests.helpers import TempDB

# (вызов, ожидаемое значение)
CALLS = [
    (lambda: sc.sys_login("admin", "x", "guest"), True),
    (lambda: sc.sys_logout("admin"), True),
    (lambda: sc.sys_whoami("admin"), "admin"),
    (lambda: sc.sys_create_file("/t.txt", "hi", "admin"), 1),
    (lambda: sc.sys_read_file("/t.txt", "admin"), ""),
    (lambda: sc.sys_delete_file("/t.txt", "admin"), True),
    (lambda: sc.sys_list_files("/", "admin"), ["/test.txt"]),
    (lambda: sc.sys_exec("shell", "admin"), 42),
    (lambda: sc.sys_ps("admin"), []),
    (lambda: sc.sys_kill(42, "admin"), True),
    (lambda: sc.sys_mem_alloc(128, "admin"), 4096),
    (lambda: sc.sys_shutdown("admin"), True),
]


class SyscallsTest(TempDB, unittest.TestCase):
    def test_return_values_and_logging(self):
        for call, expected in CALLS:
            self.assertEqual(call(), expected)
        self.assertEqual(len(db.fetch_logs(100)), len(CALLS))

    def test_sys_logs_returns_list(self):
        sc.sys_whoami("admin")
        rows = sc.sys_logs(5, "admin")
        self.assertIsInstance(rows, list)
        self.assertEqual(rows[0]["syscall_name"], "sys_logs")

    def test_login_unknown_user_fails_and_password_not_logged(self):
        self.assertFalse(sc.sys_login("nobody", "secret123", "guest"))
        last = db.fetch_logs(1)[0]
        self.assertEqual((last["args"], last["status"]), ("nobody", "FAIL"))
        self.assertNotIn("secret123", str(last))

    def test_speed_nfr_p1(self):
        for call, _ in CALLS:
            t = time.perf_counter()
            call()
            self.assertLess((time.perf_counter() - t) * 1000, config.MAX_SYSCALL_MS)


if __name__ == "__main__":
    unittest.main()
