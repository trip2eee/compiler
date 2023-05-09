import unittest
from src.scanner import *
from src.rd_parser import *


class ReccurentDescentParserTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_stmt_exp(self):
        parser = RDParser()
        program = parser.parse('unittest/stmt_exp.cmm')

        stmt : TreeNode
        stmt = program

        # a = 10;
        self.assertEqual(stmt.stmt_kind, StmtKind.ASSIGN)
        exp = stmt.child[1]
        self.assertEqual(exp.exp_kind, ExpKind.CONST)
        self.assertEqual(exp.exp_type, ExpType.INTEGER)
        self.assertEqual(exp.integer, 10)

        # b = 10 + 100;
        stmt = stmt.sibling
        exp = stmt.child[1]
        self.assertEqual(exp.exp_kind, ExpKind.OP)
        self.assertEqual(exp.op, TokenType.OP_PLUS)
        self.assertEqual(exp.child[0].integer, 10)
        self.assertEqual(exp.child[1].integer, 100)

        # c = 30 * (10 + 20);
        stmt = stmt.sibling
        exp = stmt.child[1]
        self.assertEqual(exp.exp_kind, ExpKind.OP)
        self.assertEqual(exp.op, TokenType.OP_TIMES)
        self.assertEqual(exp.child[0].integer, 30)

        self.assertEqual(exp.child[1].exp_kind, ExpKind.OP)
        self.assertEqual(exp.child[1].op, TokenType.OP_PLUS)
        self.assertEqual(exp.child[1].child[0].integer, 10)
        self.assertEqual(exp.child[1].child[1].integer, 20)

        # d = 10 + 20 * 30;
        stmt = stmt.sibling
        exp = stmt.child[1]
        self.assertEqual(exp.exp_kind, ExpKind.OP)
        self.assertEqual(exp.op, TokenType.OP_PLUS)
        self.assertEqual(exp.child[0].integer, 10)

        self.assertEqual(exp.child[1].exp_kind, ExpKind.OP)
        self.assertEqual(exp.child[1].op, TokenType.OP_TIMES)
        self.assertEqual(exp.child[1].child[0].integer, 20)
        self.assertEqual(exp.child[1].child[1].integer, 30)

    def test_stmt_if(self):
        parser = RDParser()
        program = parser.parse('unittest/stmt_if.cmm')

        stmt : TreeNode
        stmt = program

        # if(a == 1)
        self.assertEqual(stmt.stmt_kind, StmtKind.IF)
        exp = stmt.child[0]
        self.assertEqual(exp.op, TokenType.OP_EQ)
        self.assertEqual(exp.child[0].exp_kind, ExpKind.ID)
        self.assertEqual(exp.child[1].exp_kind, ExpKind.CONST)

        # b1 = 1;
        # b2 = 2;
        # b3 = 3;
        sub_stmt = stmt.child[1]
        self.assertEqual(sub_stmt.stmt_kind, StmtKind.ASSIGN)
        sub_stmt = sub_stmt.sibling
        self.assertEqual(sub_stmt.stmt_kind, StmtKind.ASSIGN)
        sub_stmt = sub_stmt.sibling
        self.assertEqual(sub_stmt.stmt_kind, StmtKind.ASSIGN)
        
        # else-part
        sub_stmt = stmt.child[2]
        self.assertEqual(sub_stmt, None)

        # if(c <= 3*10)
        stmt = stmt.sibling
        self.assertEqual(stmt.stmt_kind, StmtKind.IF)
        exp = stmt.child[0]
        self.assertEqual(exp.op, TokenType.OP_LTE)
        self.assertEqual(exp.child[0].exp_kind, ExpKind.ID)
        self.assertEqual(exp.child[1].exp_kind, ExpKind.OP)
        self.assertEqual(exp.child[1].op, TokenType.OP_TIMES)

        # d = 4;
        sub_stmt = stmt.child[1]
        self.assertEqual(sub_stmt.stmt_kind, StmtKind.ASSIGN)
        sub_stmt = sub_stmt.sibling
        self.assertEqual(sub_stmt, None)

        # else-part
        sub_stmt = stmt.child[2]
        # e = 5;
        self.assertEqual(sub_stmt.stmt_kind, StmtKind.ASSIGN)
        sub_stmt = sub_stmt.sibling
        self.assertEqual(sub_stmt, None)

if __name__ == '__main__':
    unittest.main()

