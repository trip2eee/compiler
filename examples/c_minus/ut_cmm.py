import sys
sys.path += '../../'
from examples.c_minus.cmm_parser import Parser
from examples.c_minus.cmm_lexer import Lexer
from examples.c_minus.code_generator import CodeGenerator
from examples.c_minus.runenv import RunEnv
import unittest

class TestCMM(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse(self):
        lexer = Lexer()
        parser = Parser()
        codegen = CodeGenerator()

        lexer.scan('examples/c_minus/hello_world.cmm')
        list_tokens = lexer.list_tokens

        program = parser.parse(list_tokens)

        codegen.generate(program, 'examples/c_minus/test.pcode', verbose=True)

        runenv = RunEnv()
        runenv.exec('examples/c_minus/test.pcode')

        print('done')

if __name__ == '__main__':
    unittest.main()
