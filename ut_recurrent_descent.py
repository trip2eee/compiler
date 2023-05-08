import unittest
from src.scanner import *
from src.rd_parser import *


class ReccurentDescentParserTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_exp(self):
        parser = RDParser()
        program = parser.parse('unittest/exp.cmm')

        exp : TreeNode
        exp = program

        self.assertEqual(exp.exp_kind, ExpKind.CONST)
        self.assertEqual(exp.exp_type, ExpType.INTEGER)
        self.assertEqual(exp.integer, 10)

        exp = exp.sibling
        self.assertEqual(exp.exp_kind, ExpKind.OP)
        self.assertEqual(exp.op, TokenType.OP_PLUS)
        self.assertEqual(exp.child[0].integer, 10)
        self.assertEqual(exp.child[1].integer, 100)

        exp = exp.sibling
        self.assertEqual(exp.exp_kind, ExpKind.OP)
        self.assertEqual(exp.op, TokenType.OP_TIMES)
        self.assertEqual(exp.child[0].integer, 30)

        self.assertEqual(exp.child[1].exp_kind, ExpKind.OP)
        self.assertEqual(exp.child[1].op, TokenType.OP_PLUS)
        self.assertEqual(exp.child[1].child[0].integer, 10)
        self.assertEqual(exp.child[1].child[1].integer, 20)


if __name__ == '__main__':
    unittest.main()

