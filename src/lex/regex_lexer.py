from src.lex.regex_parser_table import *

class RegExLexer:
    def __init__(self):
        self.list_symbol = []
    
    def add_token(self, type=0, value=0):
        t = TreeNode()
        t.type = type
        t.value = value
        t.idx_col = self.idx_char
        self.list_symbol.append(t)
    
    def lexer(self, expr):
        self.idx_char = 0
        state = 0
        self.list_symbol = []
        
        while self.idx_char < len(expr):
            c = expr[self.idx_char]
            self.idx_char += 1

            if state == 0:                
                if c == '\\':
                    # if escape character
                    state = 1
                elif c in yy_token_names:
                    self.add_token(type=yy_token_names[c], value=c)
                else:
                    if '0' <= c <= '9':
                        self.add_token(type=DIGIT, value=c)
                    else:
                        self.add_token(type=CHAR, value=c)
                
            elif state == 1:
                if c == 'd':
                    self.add_token(type=ESC, value=c)
                elif c == 'n':
                    self.add_token(type=CHAR, value='\n')
                else:
                    self.add_token(type=CHAR, value=c)
                state = 0

        return self.list_symbol