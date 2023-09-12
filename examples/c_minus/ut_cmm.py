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

    def run_code(self, code_path):
        print('run', code_path)

        self.lexer.scan('examples/c_minus/tests/' + code_path)
        program = self.parser.parse(self.lexer.list_tokens)
        self.codegen.generate(program, 'examples/c_minus/out.pcode', verbose=True)
        self.runenv.exec('examples/c_minus/out.pcode')

    def test_hello_world(self):
        self.run_code('hello_world.cmm')
        
        self.assertEqual(self.runenv.stdout[0], 'Hello, World\n')

    def test_if_stmt(self):
        self.run_code('if_stmt.cmm')
        
        self.assertEqual(self.runenv.stdout[0], 'a + b = 30\n')

    def test_for_stmt(self):
        self.run_code('for_stmt.cmm')

        self.assertEqual(self.runenv.stdout[0], 'sum = 55\n')

    def test_func_call(self):
        self.run_code('func_call.cmm')
        
        self.assertEqual(self.runenv.stdout[0], 'true\n')

if __name__ == '__main__':
    unittest.main()
