import sys
sys.path += '../../'
from examples.c_minus.cmm_parser import Parser
from examples.c_minus.cmm_lexer import Lexer
import unittest

class TestCMM(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse(self):
        lexer = Lexer()
        parser = Parser()

        lexer.scan('examples/c_minus/hello_world.cmm')
        list_tokens = lexer.list_tokens


        program = parser.parse(list_tokens)

        print('done')


if __name__ == '__main__':
    unittest.main()
