import unittest
from src.lexer_generator import *
from src.lex_parser import *

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



if __name__ == '__main__':
    unittest.main()