import unittest
from src.scanner import *

class ScannerTest(unittest.TestCase):

    def setUp(self):
        self.idx_token = 0

    def tearDown(self):
        pass
    
    def _test_sequence(self, tokens, target):
        print('start sequence')
        
        for i in range(0, len(target)):
            self.assertEqual(tokens[self.idx_token].type, target[i])
            print('{} : {}'.format(self.idx_token, tokens[self.idx_token].string_val))
            self.idx_token += 1

        print('end of sequence')

    def test_numbers(self):
        scanner = Scanner()
        tokens = scanner.scan('unittest/digits.cmm')
        
        self.assertEqual(len(tokens), 3)

        self.assertEqual(tokens[0].type, TokenType.NUM)
        self.assertEqual(tokens[0].int_val, 1234)
        self.assertEqual(tokens[0].line_number, 1)
        self.assertEqual(tokens[0].col_number, 0)

        self.assertEqual(tokens[1].type, TokenType.NUM_FLOAT)
        self.assertEqual(tokens[1].float_val, 567.0123)
        self.assertEqual(tokens[1].line_number, 2)
        self.assertEqual(tokens[1].col_number, 0)

        self.assertEqual(tokens[2].type, TokenType.NUM)
        self.assertEqual(tokens[2].int_val, 100)
        self.assertEqual(tokens[2].line_number, 3)
        self.assertEqual(tokens[2].col_number, 0)

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

        target = [
            TokenType.ID, TokenType.OP_ASSIGN, TokenType.ID, TokenType.OP_PLUS, TokenType.ID, TokenType.SEMI
        ]
        self._test_sequence(tokens, target)


        target = [
            TokenType.ID, TokenType.OP_ADD_ASSIGN, TokenType.ID, TokenType.SEMI
        ]
        self._test_sequence(tokens, target)
        self.assertEqual(tokens[7].string_val, '+=')

        target = [
            TokenType.ID, TokenType.OP_BIT_AND_ASSIGN, TokenType.ID, TokenType.SEMI
        ]
        self._test_sequence(tokens, target)
        self.assertEqual(tokens[11].string_val, '&=')

        target = [
            TokenType.ID, TokenType.OP_SHL_ASSIGN, TokenType.ID, TokenType.SEMI
        ]
        self._test_sequence(tokens, target)

        self.assertEqual(tokens[15].string_val, '<<=')

        target = [
            TokenType.ID, TokenType.OP_SHR_ASSIGN, TokenType.ID, TokenType.SEMI
        ]
        self._test_sequence(tokens, target)

        self.assertEqual(tokens[19].string_val, '>>=')

        target = [
            TokenType.ID, TokenType.OP_INC, TokenType.SEMI
        ]
        self._test_sequence(tokens, target)
        self.assertEqual(tokens[23].string_val, '++')

        target = [
            TokenType.ID, TokenType.OP_DEC, TokenType.SEMI
        ]
        self._test_sequence(tokens, target)
        self.assertEqual(tokens[26].string_val, '--')

        target = [
            TokenType.ID, TokenType.OP_BIT_OR_ASSIGN, TokenType.NUM, TokenType.SEMI
        ]
        self._test_sequence(tokens, target)
        self.assertEqual(tokens[29].string_val, '|=')

        target = [
            TokenType.ID, TokenType.OP_BIT_AND_ASSIGN, TokenType.NUM, TokenType.SEMI
        ]
        self._test_sequence(tokens, target)
        self.assertEqual(tokens[33].string_val, '&=')

        target = [
            TokenType.ID, TokenType.OP_DIV_ASSIGN, TokenType.NUM_FLOAT,
        ]
        self._test_sequence(tokens, target)
        self.assertEqual(tokens[37].string_val, '/=')

        target = [
            TokenType.ID, TokenType.OP_ASSIGN, TokenType.NUM, TokenType.OP_DIV, TokenType.NUM,
        ]
        self._test_sequence(tokens, target)
        self.assertEqual(tokens[42].string_val, '/')

    def test_string(self):
        scanner = Scanner()
        tokens = scanner.scan('unittest/string.cmm')

        target = [
            TokenType.ID, TokenType.OP_ASSIGN, TokenType.STRING, TokenType.SEMI
        ]
        self._test_sequence(tokens, target)

        target = [
            TokenType.ID, TokenType.OP_ASSIGN, TokenType.CHAR, TokenType.SEMI
        ]
        self._test_sequence(tokens, target)
        self.assertEqual(tokens[6].string_val, "H")

    def test_control_statements(self):
        scanner = Scanner()
        tokens = scanner.scan('unittest/control_statements.cmm')

        target = [
            TokenType.IF, TokenType.LPAREN, TokenType.ID, TokenType.OP_NEQ, TokenType.NUM, TokenType.RPAREN, 
            TokenType.LBRACE, 
            TokenType.ID, TokenType.OP_ASSIGN, TokenType.NUM, TokenType.SEMI,
            TokenType.RBRACE
        ]
        self._test_sequence(tokens, target)

        target = [
            TokenType.FOR, TokenType.LPAREN, TokenType.ID, TokenType.OP_ASSIGN, TokenType.NUM, TokenType.SEMI, TokenType.ID, TokenType.OP_LT, TokenType.NUM, TokenType.SEMI, TokenType.ID, TokenType.OP_INC, TokenType.RPAREN, 
            TokenType.LBRACE, 
            TokenType.RBRACE
        ]
        self._test_sequence(tokens, target)


        target = [
            TokenType.TYPE, TokenType.ID, TokenType.OP_ASSIGN, TokenType.NUM, TokenType.SEMI,
            TokenType.WHILE, TokenType.LPAREN, TokenType.ID, TokenType.OP_LT, TokenType.NUM, TokenType.RPAREN, TokenType.LBRACE, 
            TokenType.ID, TokenType.OP_ADD_ASSIGN, TokenType.NUM, TokenType.SEMI,
            TokenType.ID, TokenType.OP_BIT_XOR_ASSIGN, TokenType.NUM, TokenType.SEMI,
            TokenType.ID, TokenType.OP_BIT_NOT_ASSIGN, TokenType.NUM, TokenType.SEMI,
            TokenType.RBRACE
        ]
        self._test_sequence(tokens, target)


if __name__ == '__main__':
    unittest.main()

