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
        self.assertEqual(self.runenv.stdout, 'Hello, World\n')
    
    def test_expressions(self):
        self.run_code('expressions.cmm')
        self.assertEqual(self.runenv.stdout, 'c = 20, d = -100\n')

    def test_if_stmt(self):
        self.run_code('if_stmt.cmm')
        self.assertEqual(self.runenv.stdout, 'a + b = 30\n')

    def test_for_stmt(self):
        self.run_code('for_stmt.cmm')
        self.assertEqual(self.runenv.stdout, 'sum = 55\n')
    
    def test_while_stmt(self):
        self.run_code('while_stmt.cmm')
        self.assertEqual(self.runenv.stdout, 'i = -1\n')

    def test_nested_stmt(self):
        self.run_code('nested_stmt.cmm')
        self.assertEqual(self.runenv.stdout, '1 0 1 1 0 1 \n')        

    def test_func_call(self):
        self.run_code('func_call.cmm')
        self.assertEqual(self.runenv.stdout, 'true\nk = 30\n')

    def test_func_recursive_call(self):
        self.run_code('func_recursive_call.cmm')
        self.assertEqual(self.runenv.stdout, '5! = 120\n')

if __name__ == '__main__':
    unittest.main()


