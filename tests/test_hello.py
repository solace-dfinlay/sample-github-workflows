import unittest
from hello import hello, goodbye

class TestHello(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(hello("Worrld"), "Hello, World!")
    
    def test_goodbye(self):
        self.assertEqual(goodbye("Worldd"), "Goodbye, World!")

if __name__ == "__main__":
    unittest.main()