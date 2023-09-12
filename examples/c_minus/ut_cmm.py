import sys
sys.path += '../../'
from examples.c_minus.cmm_parser import Parser
from examples.c_minus.cmm_lexer import Lexer
from examples.c_minus.code_generator import CodeGenerator
from examples.c_minus.runenv import RunEnv
import unittest

class TestCMM(unittest.TestCase):
    def setUp(self):
        self.lexer = Lexer()
        self.parser = Parser()
        self.codegen = CodeGenerator()
        self.runenv = RunEnv()

    def tearDown(self):
        pass

    def test_hello_world(self):
        self.lexer.scan('examples/c_minus/tests/hello_world.cmm')
        program = self.parser.parse(self.lexer.list_tokens)
        self.codegen.generate(program, 'examples/c_minus/out.pcode', verbose=True)        
        self.runenv.exec('examples/c_minus/out.pcode')

        self.assertEqual(self.runenv.stdout[0], 'Hello, World\n')

    def test_if_stmt(self):
        self.lexer.scan('examples/c_minus/tests/if_stmt.cmm')
        program = self.parser.parse(self.lexer.list_tokens)
        self.codegen.generate(program, 'examples/c_minus/out.pcode', verbose=True)        
        self.runenv.exec('examples/c_minus/out.pcode')

        self.assertEqual(self.runenv.stdout[0], 'a + b = 30\n')

    def test_func_call(self):
        self.lexer.scan('examples/c_minus/tests/func_call.cmm')
        program = self.parser.parse(self.lexer.list_tokens)
        self.codegen.generate(program, 'examples/c_minus/out.pcode', verbose=True)        
        self.runenv.exec('examples/c_minus/out.pcode')

        self.assertEqual(self.runenv.stdout[0], 'true\n')

if __name__ == '__main__':
    unittest.main()
