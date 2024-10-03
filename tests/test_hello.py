import unittest
from src.hello import hello, goodbye

class TestHello(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(hello("World"), "Hello, World!")
    
    def test_goodbye(self):
        self.assertEqual(goodbye("World"), "Goodbye, World!")

    def test_hello_2(self):
        self.assertEqual(hello("World"), "Hi, World!")  # This will fail
    
    def test_goodbye_2(self):
        self.assertEqual(goodbye("World"), "Bye, World!")  # This will fail

if __name__ == "__main__":
    unittest.main()