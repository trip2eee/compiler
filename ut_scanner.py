import unittest
from src.scanner import *

class ScannerTest(unittest.TestCase):

    def setUp(self):
        self.dummy = 0

    def tearDown(self):
        pass

    def test_numbers(self):
        scanner = Scanner()
        tokens = scanner.scan('unittest/digits.cmm')
        
        self.assertEqual(len(tokens), 2)

        self.assertEqual(tokens[0].type, TokenType.NUM)
        self.assertEqual(tokens[0].int_val, 1234)
        self.assertEqual(tokens[0].line_number, 1)
        self.assertEqual(tokens[0].col_number, 0)

        self.assertEqual(tokens[1].type, TokenType.NUM_FLOAT)
        self.assertEqual(tokens[1].float_val, 567.0123)
        self.assertEqual(tokens[1].line_number, 2)
        self.assertEqual(tokens[1].col_number, 0)

    def test_identifiers(self):
        scanner = Scanner()
        tokens = scanner.scan('unittest/identifiers.cmm')

        self.assertEqual(len(tokens), 6)
        self.assertEqual(tokens[0].type, TokenType.TYPE)
        self.assertEqual(tokens[0].col_number, 0)
        self.assertEqual(tokens[1].type, TokenType.ID)
        self.assertEqual(tokens[1].col_number, 4)
        self.assertEqual(tokens[2].type, TokenType.SEMI)
        self.assertEqual(tokens[2].col_number, 9)

        self.assertEqual(tokens[3].type, TokenType.TYPE)
        self.assertEqual(tokens[4].type, TokenType.ID)
        self.assertEqual(tokens[5].type, TokenType.SEMI)

    def test_comments(self):
        scanner = Scanner()
        tokens = scanner.scan('unittest/comments.cmm')

        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenType.COMMENT)
        self.assertEqual(tokens[1].type, TokenType.COMMENT)

    def test_operator(self):
        scanner = Scanner()
        tokens = scanner.scan('unittest/operators.cmm')

        self.assertEqual(len(tokens), 6)
        self.assertEqual(tokens[0].type, TokenType.ID)
        self.assertEqual(tokens[1].type, TokenType.OP_ASSIGN)
        self.assertEqual(tokens[2].type, TokenType.ID)
        self.assertEqual(tokens[3].type, TokenType.OP)
        self.assertEqual(tokens[4].type, TokenType.ID)
        self.assertEqual(tokens[5].type, TokenType.SEMI)

if __name__ == '__main__':
    unittest.main()

