from examples.calc.calc_parser_table import *
from examples.calc.calc_parser import *

class CalcLexer:
    def __init__(self):
        self.list_symbol = []
    
    def add_symbol(self, type=0, value=0):
        t = Symbol()
        t.type = type
        t.value = value
        self.list_symbol.append(t)
        
    def lexer(self, expr):
        idx_char = 0
        state = 0
        num = ''
        self.list_symbol = []
        
        while idx_char < len(expr) + 1:
            if idx_char < len(expr):
                c = expr[idx_char]
            else:
                c = '$'

            idx_char += 1

            if state == 0:
                if '0' <= c <= '9':
                    num = c
                    state = 1
                elif c in yy_token_names:
                    self.add_symbol(type=yy_token_names[c], value=c)
                
            elif state == 1:
                if '0' <= c <= '9':
                    num += c
                else:
                    self.add_symbol(type=number, value=int(num))
                    idx_char -= 1
                    state = 0

        return self.list_symbol

