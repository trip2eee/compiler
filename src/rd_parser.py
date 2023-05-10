"""
Recurrent-Descent Parser
@author Jongmin Park (trip2eee@gmail.com)
@date 2023-05-08
"""

from src.scanner import *
from src.syntax_tree import *

class RDParser:
    def __init__(self):
        self.program = None
        self.scanner = Scanner()
        self.list_tokens = []
        self.idx_token = -1
        self.token = None
        self.last_node = None

    def __del__(self):
        pass

    def parse(self, file_path):
        self.scanner : Scanner
        
        self.list_tokens = self.scanner.scan(file_path)

        # read a token
        self.idx_token += 1
        self.token = self.list_tokens[self.idx_token]

        self.program = self.stmt_sequence()

        return self.program

    def make_op_node(self, op):
        node = TreeNode()
        node.exp_kind = ExpKind.OP
        node.op = op

        return node

    def stmt_sequence(self):
        stmt_seq = None

        if self.token.type == TokenType.LBRACE:
            self.match(TokenType.LBRACE)
            stmt_seq = self.stmt_sequence()
            self.match(TokenType.RBRACE)
        else:
            last_stmt = None
            
            stmt = self.stmt()
            while stmt is not None:
                if last_stmt is None:
                    stmt_seq = stmt
                    last_stmt = stmt
                else:
                    last_stmt.sibling = stmt
                    last_stmt = stmt
                
                stmt = self.stmt()

        return stmt_seq

    def stmt(self):
        self.token: Token
        node = None
        
        if self.token is not None: # and self.token.type != TokenType.RBRACE:
            if self.token.type == TokenType.IF:
                # if statement
                node = TreeNode()
                node.stmt_kind = StmtKind.IF

                self.get_next_token()
                # condition
                self.match(TokenType.LPAREN)
                node.child[0] = self.exp()
                self.match(TokenType.RPAREN)
                
                # statement
                node.child[1] = self.stmt_sequence()

                if self.token.type == TokenType.ELSE:
                    self.get_next_token()

                    node.child[2] = self.stmt_sequence()
                else:
                    node.child[2] = None

            elif self.token.type == TokenType.FOR:
                node = TreeNode()
                node.stmt_kind = StmtKind.FOR

                self.get_next_token()
                self.match(TokenType.LPAREN)
                # initialization
                node.child[0] = self.exp()
                self.match(TokenType.SEMI)

                # comparison
                node.child[1] = self.exp()
                self.match(TokenType.SEMI)

                # expression
                node.child[2] = self.exp()                
                self.match(TokenType.RPAREN)

                node.child[3] = self.stmt_sequence()

            else:
                node = self.exp()
                if node is not None:
                    self.match(TokenType.SEMI)

        return node

    def exp(self):
        self.token: Token

        node = self.simple_exp()

        # while comparison operator
        while 400 <= self.token.type <= 410:            
            new_node = self.make_op_node(self.token.type)
            new_node.child[0] = node
            self.get_next_token()
            new_node.child[1] = self.simple_exp()
            node = new_node
        
        if node is not None:
            node.stmt_kind = StmtKind.EXP

        return node

    def simple_exp(self):
        self.token : Token
        node = self.term()

        if 300 <= self.token.type <= 310:
            new_node = self.make_op_node(self.token.type)
            new_node.child[0] = node
            self.get_next_token()
            new_node.child[1] = self.exp()
            node = new_node

        else:
            while self.token.type == TokenType.OP_PLUS or self.token.type == TokenType.OP_MINUS:
                if self.token.type == TokenType.OP_PLUS:
                    new_node = self.make_op_node(self.token.type)
                    new_node.child[0] = node
                    self.get_next_token()
                    new_node.child[1] = self.term()                
                    node = new_node
                elif self.token.type == TokenType.OP_MINUS:                
                    new_node = self.make_op_node(self.token.type)
                    new_node.child[0] = node
                    self.get_next_token()
                    new_node.child[1] = self.term()                
                    node = new_node
                else:
                    break
        
        return node
    
    def term(self):
        self.token : Token
        node = self.factor()

        while True:
            if self.token.type == TokenType.OP_TIMES:                
                new_node = self.make_op_node(self.token.type)
                new_node.child[0] = node
                self.get_next_token()
                new_node.child[1] = self.factor()                
                node = new_node

            elif self.token.type == TokenType.OP_DIV:                
                new_node = self.make_op_node(self.token.type)
                new_node.child[0] = node
                self.get_next_token()
                new_node.child[1] = self.factor()            
                node = new_node
            else:
                break
        
        return node
    
    def factor(self):
        self.token : Token
        node = None
        
        if self.token.type == TokenType.LPAREN:
            # if (
            self.match(TokenType.LPAREN)
            node = self.exp()
            self.match(TokenType.RPAREN)
        
        elif self.token.type == TokenType.NUM or self.token.type == TokenType.NUM_FLOAT:
            # if number
            node = TreeNode()
            node.exp_kind = ExpKind.CONST

            if self.token.type == TokenType.NUM:                
                node.exp_type = ExpType.INTEGER
                node.integer = self.token.int_val
                self.get_next_token()
            elif self.token.type == TokenType.NUM_FLOAT:                
                node.exp_type = ExpType.FLOAT
                node.float = self.token.float_val
                self.get_next_token()
        
        elif self.token.type == TokenType.ID:
            # identifier
            node = TreeNode()
            node.exp_kind = ExpKind.ID
            node.string = self.token.string_val
            self.get_next_token()

            # right unary id++, id--
            if self.token.type == TokenType.OP_INC or self.token.type == TokenType.OP_DEC:
                new_node = self.make_op_node(self.token.type)
                new_node.child[0] = node
                node = new_node
                self.get_next_token()
        
        elif self.token.type == TokenType.OP_MINUS:
            # signop -
            self.get_next_token()
            node = self.make_op_node(TokenType.OP_TIMES)
            node.exp_type = ExpType.INTEGER

            node.child[0] = TreeNode()
            node.child[0].exp_type = ExpType.INTEGER
            node.child[0].integer = -1
            node.child[0].float = -1.0            

            node.child[1] = self.factor()
        
        elif self.token.type == TokenType.OP_PLUS:
            # signop +
            self.get_next_token()
            node = self.factor()

        elif self.token.type == TokenType.OP_INC or self.token.type == TokenType.OP_DEC:
            # left unary ++id, --id
            node = self.make_op_node(self.token.type)
            
            self.get_next_token()
            node.child[1] = self.factor()

        return node
    
    def get_next_token(self):
        self.idx_token += 1

        if self.idx_token < len(self.list_tokens):
            self.token = self.list_tokens[self.idx_token]            
            return True
        else:
            self.token = None
            # end of token
            return False
    
    def match(self, exp_type: TokenType):

        self.token : Token
        if self.token.type == exp_type:
            self.get_next_token()
        else:
            self.error()
            return False
    
    def error(self, message=''):
        print('Error, line {}, {}'.format(self.token.line_number, message))