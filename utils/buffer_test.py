import unittest

from buffer import Buffer

class TestBuffer(unittest.TestCase):

    def test_print(self):
        b = Buffer()
        b.print("test")
        self.assertEqual(len(b._buf), 1)
        self.assertEqual(b._buf[0], "test")

    def test_console(self):
        b = Buffer()
        b.print("line 1")
        b.print("line 2")
        self.assertEqual(b.console(), "line 1\nline 2\n")

if __name__ == "__main__":
    unittest.main()