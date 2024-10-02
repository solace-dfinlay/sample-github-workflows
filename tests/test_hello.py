# tests/test_hello.py
import unittest
from src.hello import greet

class TestHello(unittest.TestCase):
    def test_greet(self):
        self.assertEqual(greet("World"), "Hello, Woorld!")

if __name__ == '__main__':
    unittest.main()