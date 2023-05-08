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
        
    def __del__(self):
        pass

    def parse(self, file_path):
        self.scanner : Scanner
        
        self.list_tokens = self.scanner.scan(file_path)

        # read a token
        self.idx_token += 1
        self.token = self.list_tokens[self.idx_token]

        last_node = None

        while self.idx_token < len(self.list_tokens) - 1:
            node = self.exp()

            if self.program is None:
                self.program = node
            
            if last_node is not None:
                last_node.sibling = node
            
            last_node = node

            if self.match(TokenType.SEMI) == False:
                break

        return self.program

    def exp(self):
        self.token : Token
        node = self.term()

        while self.token.type == TokenType.OP_PLUS or self.token.type == TokenType.OP_MINUS:
            if self.token.type == TokenType.OP_PLUS:
                self.match(TokenType.OP_PLUS)
                new_node = TreeNode()
                new_node.exp_kind = ExpKind.OP
                new_node.op = TokenType.OP_PLUS
                new_node.child[0] = node
                new_node.child[1] = self.term()                
                node = new_node
            elif self.token.type == TokenType.OP_MINUS:
                self.match(TokenType.OP_MINUS)
                new_node = TreeNode()
                new_node.exp_kind = ExpKind.OP
                new_node.op = TokenType.OP_MINUS
                new_node.child[0] = node
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
                self.match(TokenType.OP_TIMES)
                new_node = TreeNode()
                new_node.exp_kind = ExpKind.OP
                new_node.op = TokenType.OP_TIMES
                new_node.child[0] = node
                new_node.child[1] = self.factor()                
                node = new_node

            elif self.token.type == TokenType.OP_DIV:
                self.match(TokenType.OP_DIV)
                new_node = TreeNode()
                new_node.exp_kind = ExpKind.OP
                new_node.op = TokenType.OP_DIV
                new_node.child[0] = node
                new_node.child[1] = self.factor()                
                node = new_node
            else:
                break
        
        return node
    
    def factor(self):
        self.token : Token
        node = None

        # if (
        if self.token.type == TokenType.LPAREN:
            self.match(TokenType.LPAREN)
            node = self.exp()
            self.match(TokenType.RPAREN)

        # if number
        elif self.token.type == TokenType.NUM or self.token.type == TokenType.NUM_FLOAT:
            node = TreeNode()
            node.exp_kind = ExpKind.CONST

            if self.token.type == TokenType.NUM:                
                node.exp_type = ExpType.INTEGER
                node.integer = self.token.int_val
                self.match(TokenType.NUM)
            elif self.token.type == TokenType.NUM_FLOAT:                
                node.exp_type = ExpType.FLOAT
                node.float = self.token.float_val
                self.match(TokenType.NUM_FLOAT)
            else:
                self.error()

        else:
            self.error()

        return node
    
    def match(self, exp_type: TokenType):

        self.token : Token
        if self.token.type == exp_type:
            self.idx_token += 1

            if self.idx_token < len(self.list_tokens):
                self.token = self.list_tokens[self.idx_token]            
                return True
            else:
                return False
        else:
            self.error()
            return False
    
    def error(self):
        print('Error in line {}'.format(self.token.line_number))