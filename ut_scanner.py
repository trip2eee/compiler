import unittest
from src.scanner import Scanner

class ScannerTest(unittest.TestCase):

    def setUp(self):
        self.dummy = 0

    def tearDown(self):
        pass

    def test_scanner(self):
        scanner = Scanner()
        scanner.scan('test.cmm')

if __name__ == '__main__':
    unittest.main()

