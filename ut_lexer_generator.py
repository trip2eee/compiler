import unittest
from src.lex.lexer_generator import *
from src.lex.lex_parser import *

from cmm_lexer import Lexer

COMMENT = 1
ID = 2
ASSIGN = 3
IF = 4
FOR = 5
PLUS = 6
MINUS = 7
LTE = 8
GTE = 9
EQUAL = 10

class ParserGeneratorTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_lex_parser(self):
        parser = LexParser()
        parser.open('unittest/cmm.lex')

        print('done')

    def test_lex_generator(self):
        gen = LexerGenerator()
        gen.open('unittest/cmm.lex')
        # gen.generate_code('./cmm_lexer.py')



    def test_lexer(self):
        lexer = Lexer()

        lexer.scan('unittest/lexer_test.cmm')


if __name__ == '__main__':
    unittest.main()
